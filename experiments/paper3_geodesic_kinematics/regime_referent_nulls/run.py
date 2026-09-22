"""Does H2's AASM binding survive a correct (dependence-preserving) null, and is it the geometry?

Re-tests regime_external_referent (H2) after an external review: circular-shift and
record-level nulls replace the i.i.d. within-record shuffle, and two scalar baselines are run
through the identical median-split procedure. See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.regime_referent_nulls.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum, _R
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects, WIN_SEC, STEP_SEC, EIG_FLOOR,
)
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "regime_referent_nulls")
EXP_WIN = 10
N_SHIFT = 2000
DRIFT_STAGES = {"N2", "N3"}
DISP_STAGES = {"W", "REM"}
FEATURES = ["geo_vol", "scalar_vol", "scalar_level"]


def windows(data, fs, stage):
    """Same windows as H2; returns trace-normalised covs, raw log-power, majority labels."""
    w, step = int(WIN_SEC * fs), int(STEP_SEC * fs)
    covs, logp, labs = [], [], []
    for start in range(0, data.shape[1] - w + 1, step):
        raw = np.cov(data[:, start:start + w])
        logp.append(np.log(np.trace(raw) + 1e-12))
        covs.append(spd.trace_normalize(spd.eigfloor(raw, EIG_FLOOR)))
        ws = stage[start:start + w]
        vals, cnts = np.unique(ws[ws != ""], return_counts=True)
        labs.append(vals[np.argmax(cnts)] if len(vals) else "")
    return covs, np.array(logp), np.array(labs, dtype=object)


def rolling_mean(x, k):
    c = np.cumsum(np.concatenate([[0.0], x]))
    idx = np.arange(len(x))
    lo = np.maximum(0, idx - k)
    return (c[idx + 1] - c[lo]) / (idx + 1 - lo)


def features(covs, logp):
    E, _ = embed_cumsum(covs)
    En = E.reshape(len(covs), -1)
    cosang = np.clip(np.sum(En[:-1] * En[1:], axis=1) / (_R * _R), -1.0, 1.0)
    geo_step = 2.0 * np.arccos(cosang)
    geo_step = np.concatenate([geo_step, geo_step[-1:]])
    dlp = np.abs(np.diff(logp)); dlp = np.concatenate([dlp, dlp[-1:]])
    return {"geo_vol": rolling_mean(geo_step, EXP_WIN),
            "scalar_vol": rolling_mean(dlp, EXP_WIN),
            "scalar_level": logp}


def low_half(x):
    """1 = low half (mapped to 'drift'), 0 = high half, median split within record (as H2)."""
    return (x <= np.median(x)).astype(np.int8)


def mapped(labs):
    """1 = N2/N3, 0 = W/REM, -1 = excluded."""
    out = np.full(len(labs), -1, dtype=np.int8)
    out[np.isin(labs, list(DRIFT_STAGES))] = 1
    out[np.isin(labs, list(DISP_STAGES))] = 0
    return out


def cramers_v_binary(a, b):
    """V for two binary arrays (2x2 table) = |phi|."""
    n = len(a)
    if n == 0:
        return 0.0
    t = np.bincount(a * 2 + b, minlength=4).reshape(2, 2).astype(float)
    r = t.sum(1, keepdims=True); c = t.sum(0, keepdims=True)
    e = r @ c / n
    if np.any(e == 0):
        return 0.0
    return float(np.sqrt(np.sum((t - e) ** 2 / e) / n))


def pooled_v(recs, feat, shifts=None):
    a_all, b_all = [], []
    for i, r in enumerate(recs):
        lab = r["mapped"] if shifts is None else np.roll(r["mapped"], shifts[i])
        keep = lab >= 0
        a_all.append(r["reg"][feat][keep]); b_all.append(lab[keep])
    return cramers_v_binary(np.concatenate(a_all), np.concatenate(b_all))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    print("H2 re-test: circular-shift + record-level nulls, scalar baselines\n")

    recs, skipped = [], []
    for p, h in discover_subjects():
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            skipped.append(f"{pref}: {type(e).__name__}"); continue
        covs, logp, labs = windows(data, fs, stage)
        f = features(covs, logp)
        recs.append({"id": pref, "mapped": mapped(labs),
                     "reg": {k: low_half(v) for k, v in f.items()}})
        print(f"  {pref}: {len(covs)} windows, {int(np.sum(recs[-1]['mapped'] >= 0))} mapped")

    n_rec = len(recs)
    obs = {k: pooled_v(recs, k) for k in FEATURES}

    # circular-shift null (same shifts for every feature)
    null = {k: np.empty(N_SHIFT) for k in FEATURES}
    for s in range(N_SHIFT):
        shifts = [int(rng.integers(int(0.1 * len(r["mapped"])), int(0.9 * len(r["mapped"]))))
                  for r in recs]
        for k in FEATURES:
            null[k][s] = pooled_v(recs, k, shifts)
    p95 = {k: float(np.percentile(null[k], 95)) for k in FEATURES}
    p_shift = {k: float((np.sum(null[k] >= obs[k]) + 1) / (N_SHIFT + 1)) for k in FEATURES}

    # record level
    per_rec = []
    for r in recs:
        keep = r["mapped"] >= 0
        lab = r["mapped"][keep]
        row = {"record": r["id"]}
        for k in FEATURES:
            reg = r["reg"][k][keep]
            row[f"V_{k}"] = cramers_v_binary(reg, lab)
            row[f"d_{k}"] = float(np.mean(lab[reg == 1]) - np.mean(lab)) if np.any(reg == 1) else 0.0
        per_rec.append(row)
    d_geo = np.array([r["d_geo_vol"] for r in per_rec])
    p_rec = float(wilcoxon(d_geo, alternative="greater").pvalue)
    n_pos = int(np.sum(d_geo > 0))

    best_scalar = max(["scalar_vol", "scalar_level"], key=lambda k: obs[k])
    diff = np.array([r["V_geo_vol"] - r[f"V_{best_scalar}"] for r in per_rec])
    p_attr = float(wilcoxon(diff, alternative="greater").pvalue) if np.any(diff != 0) else 1.0

    survives = obs["geo_vol"] > p95["geo_vol"] and p_rec < 0.05
    attributable = survives and obs["geo_vol"] > max(obs["scalar_vol"], obs["scalar_level"]) and p_attr < 0.05
    cat = "A" if attributable else ("B" if survives else "C")

    head = {"A": "SURVIVES AND IS ATTRIBUTABLE TO THE GEOMETRIC PROXY",
            "B": "SURVIVES A CORRECT NULL BUT IS NOT ATTRIBUTABLE TO THE GEOMETRY",
            "C": "DOES NOT SURVIVE A CORRECT NULL -- H2's PARTIAL REPAIR IS WITHDRAWN"}[cat]
    body = (f"Geodesic-volatility V = {obs['geo_vol']:.3f}; circular-shift null 95th pct "
            f"{p95['geo_vol']:.3f} (p = {p_shift['geo_vol']:.4f}) -- versus H2's i.i.d. null 95th pct 0.003. "
            f"Record level (n = {n_rec}): N2/N3 enriched in the low-volatility half in {n_pos}/{n_rec} records, "
            f"one-sided Wilcoxon p = {p_rec:.4f}. Scalar baselines through the identical median split: "
            f"scalar power-volatility V = {obs['scalar_vol']:.3f} (shift p = {p_shift['scalar_vol']:.4f}), "
            f"scalar log-power level V = {obs['scalar_level']:.3f} (shift p = {p_shift['scalar_level']:.4f}); "
            f"per-record geo minus best scalar ({best_scalar}) one-sided Wilcoxon p = {p_attr:.4f}.")
    tail = {"A": " The association is real under dependence-preserving nulls and the geometric volatility "
                 "beats both scalar baselines. It is still a volatility proxy, not the paper's three-regime "
                 "demarcation, so it does not exercise that construct.",
            "B": " The association is real under dependence-preserving nulls, but a scalar measure does as well "
                 "or better, so what binds to AASM is non-stationarity tracking sleep stage -- not evidence for "
                 "the geometry and not a test of the three-regime demarcation.",
            "C": " H2's p = 0.0005 was an artefact of an i.i.d. null that ignored autocorrelation."}[cat]
    verdict = f"{head}. {body}{tail}"

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, k in zip(axes, FEATURES):
        ax.hist(null[k], bins=40, color="gray", alpha=0.7, label="circular-shift null")
        ax.axvline(obs[k], color="crimson", lw=2, label=f"obs V={obs[k]:.3f}")
        ax.axvline(p95[k], color="green", ls="--", label=f"95th={p95[k]:.3f}")
        ax.set_title(k); ax.set_xlabel("Cramér's V"); ax.legend(fontsize=8)
    fig.suptitle(f"H2 re-test: verdict {cat}")
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "regime_referent_nulls.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "regime_referent_nulls",
        "question": ("does H2's regime-vs-AASM association survive dependence-preserving nulls, and is "
                     "it attributable to the geometry rather than scalar non-stationarity?"),
        "n_records": n_rec, "records_skipped": skipped,
        "records_explanation": ("9 Sleep-EDF PSGs cached locally (downloads blocked by the cloud egress); "
                                "SC4041 has no hypnogram, SC4012 is truncated -> 7 usable"),
        "observed_V": obs, "circular_shift_null_p95": p95, "circular_shift_p": p_shift,
        "h2_iid_null_p95": 0.0026142460799346385,
        "record_level": {"n_enriched": n_pos, "wilcoxon_p_one_sided": p_rec, "per_record": per_rec},
        "attribution": {"best_scalar": best_scalar, "wilcoxon_p_geo_minus_scalar": p_attr},
        "preregistered_criterion": ("survives iff geo V > circular-shift 95th pct AND record-level Wilcoxon "
                                    "p<0.05; attributable iff also geo V > both scalar V AND per-record "
                                    "Wilcoxon (geo - best scalar) p<0.05"),
        "category": cat, "survives": bool(survives), "attributable": bool(attributable),
        "verdict": verdict, "figures": ["regime_referent_nulls.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n" + "=" * 72); print(verdict); print("=" * 72)


if __name__ == "__main__":
    main()
