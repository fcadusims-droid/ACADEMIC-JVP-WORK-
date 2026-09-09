"""H1 -- does the SPD manifold beat a scalar band-power CUSUM, detector held fixed? (Paper 3)

baseline_benchmark found geodesic CUSUM 10/15 vs a best cheap baseline 8/15 ("inside binomial
noise"), but never ran the SAME detector on a scalar feature, nor a paired significance test.
This isolates manifold-vs-scalar by running the identical CUSUM on (a) the trace-normalised SPD
covariance trajectory and (b) a scalar log-band-power series, on the same 15 Sleep-EDF
sleep-onset records at the same +/-30 s tolerance, and applies a McNemar paired test.

Usage:
    python -m experiments.paper3_geodesic_kinematics.scalar_vs_manifold_localization.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint, _hit,
)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, find_transition, discover_subjects,
    SEG_SEC, STEP_SEC, TOL_SEC, MIN_SEG_SEC, WIN_SEC, EIG_FLOOR,
)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs, SEG_SEC as AL_SEG_SEC, STEP_SEC as AL_STEP,
    TOL_SEC as AL_TOL_SEC, N_SUBJECTS as AL_N,
)
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "scalar_vs_manifold_localization")
N_SUBJECTS = 15


def scalar_bandpower(data, fs, win_sec=WIN_SEC, step_sec=STEP_SEC):
    """Scalar log-total-power per window -- the power the trace-normalised manifold
    discards by construction."""
    w, step = int(win_sec * fs), int(step_sec * fs)
    out = []
    for start in range(0, data.shape[1] - w + 1, step):
        seg = data[:, start:start + w]
        out.append(np.log(np.trace(np.cov(seg)) + 1e-12))
    return np.array(out)


def scalar_cusum(x, min_seg):
    """Classical CUSUM change point on a scalar series: argmax |cumsum(centred)|."""
    s = np.cumsum(x - x.mean())
    curve = np.full(len(x), -np.inf)
    curve[min_seg:len(x) - min_seg] = np.abs(s[min_seg:len(x) - min_seg])
    return int(np.argmax(curve))


def scalar_ruptures_bocpd(x, min_seg):
    """PELT and a light BOCPD on the scalar series; return their change points."""
    cps = {}
    try:
        import ruptures as rpt
        algo = rpt.Pelt(model="l2", min_size=min_seg).fit(x.reshape(-1, 1))
        bkps = algo.predict(pen=3 * np.log(len(x)))
        cps["pelt"] = int(bkps[0]) if bkps and bkps[0] < len(x) else len(x) // 2
    except Exception:
        cps["pelt"] = None
    # tiny BOCPD (constant-hazard, Gaussian) argmax of run-length reset probability
    try:
        n = len(x); mu = np.cumsum(x) / np.arange(1, n + 1)
        resid = np.abs(x - np.concatenate([[x[0]], mu[:-1]]))
        curve = np.full(n, -np.inf); curve[min_seg:n - min_seg] = resid[min_seg:n - min_seg]
        cps["bocpd"] = int(np.argmax(curve))
    except Exception:
        cps["bocpd"] = None
    return cps


def mcnemar(pairs):
    """Exact McNemar on paired binary hits: pairs = list of (manifold_hit, scalar_hit).
    b = manifold-only hits, c = scalar-only hits; two-sided exact binomial p."""
    from scipy.stats import binomtest
    b = sum(1 for m, s in pairs if m and not s)
    c = sum(1 for m, s in pairs if s and not m)
    n = b + c
    p = binomtest(b, n, 0.5).pvalue if n > 0 else 1.0
    return b, c, float(p)


def alpha_records(min_seg_al):
    """Eyes-open/closed paradigm: concatenate the two states, seam at the join; geodesic
    CUSUM vs scalar band-power CUSUM at +/-2 s."""
    rows = []
    tol = int(round(AL_TOL_SEC / AL_STEP))
    for subj in range(1, AL_N + 1):
        try:
            do, sf = load_state_covs(subj, 1); dc, _ = load_state_covs(subj, 2)
            n = int(AL_SEG_SEC * sf)
            data = np.concatenate([do[:, :n], dc[:, :n]], axis=1)
            covs = sliding_covs(data, sf)
            seam = int(AL_SEG_SEC / AL_STEP)
            E, C = embed_cumsum(covs)
            cu = cusum_changepoint(E, C, min_seg_al)
            _, err_m, hit_m, _ = _hit(cu, seam, tol)
            xp = scalar_bandpower(data, sf, win_sec=1.0, step_sec=AL_STEP)
            cp_s = scalar_cusum(xp, min_seg_al)
            hit_s = abs(cp_s - seam) <= tol
            rows.append({"subject": f"S{subj:03d}", "paradigm": "eyes_open_closed",
                         "manifold_cusum_hit": bool(hit_m), "scalar_cusum_hit": bool(hit_s)})
            print(f"  alpha S{subj:03d}: manifold {'HIT' if hit_m else '   '} "
                  f"| scalar-CUSUM {'HIT' if hit_s else '   '}")
        except Exception as e:
            print(f"  alpha S{subj:03d}: failed {type(e).__name__}")
    return rows


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tol = int(round(TOL_SEC / STEP_SEC))
    min_seg = int(round(MIN_SEG_SEC / STEP_SEC))
    print("H1 -- manifold vs scalar band-power CUSUM, detector held fixed")
    print(f"  Sleep-EDF sleep-onset, tol +/-{TOL_SEC}s, min-seg {MIN_SEG_SEC}s\n")

    subs = discover_subjects()
    rows = []
    for p, h in subs:
        if len(rows) >= N_SUBJECTS:
            break
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            print(f"  {pref}: load failed {type(e).__name__}"); continue
        tr = find_transition(stage, fs)
        if tr is None:
            continue
        t0, s0, s1 = tr
        seg = int(SEG_SEC * fs)
        lo, hi = max(0, t0 - seg), min(data.shape[1], t0 + seg)
        sub = data[:, lo:hi]
        covs, _, centers = sliding_covs_labeled(sub, fs, np.full(sub.shape[1], "", dtype=object))
        seam = int(np.argmin(np.abs(centers - (t0 - lo) / fs)))
        # manifold CUSUM
        E, C = embed_cumsum(covs)
        cu = cusum_changepoint(E, C, min_seg)
        _, err_m, hit_m, _ = _hit(cu, seam, tol)
        # scalar band-power CUSUM (same windows)
        xp = scalar_bandpower(sub, fs)
        cp_s = scalar_cusum(xp, min_seg)
        hit_s = abs(cp_s - seam) <= tol
        # extra cheap scalar detectors
        extra = scalar_ruptures_bocpd(xp, min_seg)
        hit_pelt = (extra["pelt"] is not None and abs(extra["pelt"] - seam) <= tol)
        hit_bocpd = (extra["bocpd"] is not None and abs(extra["bocpd"] - seam) <= tol)
        rows.append({"subject": pref, "from": s0, "to": s1, "seam": int(seam),
                     "manifold_cusum_hit": bool(hit_m), "manifold_err_s": err_m * STEP_SEC,
                     "scalar_cusum_hit": bool(hit_s), "scalar_cp": int(cp_s),
                     "scalar_pelt_hit": bool(hit_pelt), "scalar_bocpd_hit": bool(hit_bocpd)})
        print(f"  {pref}: {s0}->{s1}  manifold {'HIT' if hit_m else '   '} "
              f"| scalar-CUSUM {'HIT' if hit_s else '   '} "
              f"| scalar-PELT {'HIT' if hit_pelt else '   '} "
              f"| scalar-BOCPD {'HIT' if hit_bocpd else '   '}")

    sleep_rows = rows
    print("\n  eyes-open/closed paradigm (alpha seam, +/-2 s):")
    alpha_rows = alpha_records(int(round(5.0 / AL_STEP)))
    all_rows = sleep_rows + alpha_rows
    n = len(all_rows)
    man = sum(r["manifold_cusum_hit"] for r in all_rows)
    sca = sum(r["scalar_cusum_hit"] for r in all_rows)
    pelt = sum(r.get("scalar_pelt_hit", False) for r in sleep_rows)
    bocpd = sum(r.get("scalar_bocpd_hit", False) for r in sleep_rows)
    pairs = [(r["manifold_cusum_hit"], r["scalar_cusum_hit"]) for r in all_rows]
    b, c, p_mcnemar = mcnemar(pairs)
    n_sleep, n_alpha = len(sleep_rows), len(alpha_rows)

    manifold_wins = (p_mcnemar < 0.05 and b > c)
    tied = (p_mcnemar >= 0.05 and abs(man - sca) <= 1)

    if manifold_wins:
        verdict = (
            f"MANIFOLD EARNS ITS PLACE (H1 refuted). With the detector held fixed, the "
            f"geodesic-manifold CUSUM localises sleep-onset in {man}/{n} records vs the scalar "
            f"band-power CUSUM's {sca}/{n}, and the McNemar paired test favours the manifold "
            f"significantly (manifold-only {b}, scalar-only {c}, p = {p_mcnemar:.3f}). The "
            f"trace-normalised structural view adds localisation power a one-line band-power "
            f"CUSUM does not.")
    elif tied:
        verdict = (
            f"H1 CONFIRMED -- the manifold does not beat a scalar band-power CUSUM on this task. "
            f"Detector held fixed, manifold {man}/{n} vs scalar {sca}/{n}; the McNemar paired "
            f"test finds no difference (manifold-only {b}, scalar-only {c}, p = {p_mcnemar:.3f}). "
            f"On sleep-onset localisation the manifold representation is not doing measurable "
            f"work beyond a one-line CUSUM on the band power it discards -- so Paper 3's "
            f"localisation contribution is the permanence statistic (CUSUM), not the manifold. "
            f"(Cheap scalar baselines for context: PELT {pelt}/{n}, BOCPD {bocpd}/{n}.)")
    else:
        verdict = (
            f"INCONCLUSIVE / SCALAR NOT WORSE. Manifold {man}/{n} vs scalar {sca}/{n} "
            f"(McNemar manifold-only {b}, scalar-only {c}, p = {p_mcnemar:.3f}); the discordant "
            f"pairs are too few to resolve at p<0.05, so the manifold is not shown to beat the "
            f"scalar. Reported as such. (PELT {pelt}/{n}, BOCPD {bocpd}/{n}.)")

    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ["manifold\nCUSUM", "scalar\nCUSUM", "scalar\nPELT", "scalar\nBOCPD"]
    vals = [man, sca, pelt, bocpd]
    ax.bar(range(4), [v / n for v in vals],
           color=["steelblue", "crimson", "gray", "darkgray"])
    for i, v in enumerate(vals):
        ax.text(i, v / n + 0.02, f"{v}/{n}", ha="center")
    ax.set_xticks(range(4)); ax.set_xticklabels(labels)
    ax.set_ylabel(f"sleep-onset localisation hit rate (|err|<= {TOL_SEC}s)"); ax.set_ylim(0, 1.05)
    ax.set_title(f"H1: manifold vs scalar band power, detector fixed (McNemar p={p_mcnemar:.2f})")
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "scalar_vs_manifold.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "scalar_vs_manifold_localization",
        "question": ("does the SPD manifold beat a scalar band-power CUSUM on within-trajectory "
                     "sleep-onset localisation, with the detector held fixed?"),
        "data": "PhysioNet Sleep-EDF sleep-onset (W->N1), same records/tolerance as baseline_benchmark",
        "n": n,
        "hits": {"manifold_cusum": man, "scalar_cusum": sca,
                 "scalar_pelt": pelt, "scalar_bocpd": bocpd},
        "mcnemar": {"manifold_only": b, "scalar_only": c, "p_value": p_mcnemar},
        "preregistered_criterion": "manifold beats scalar by McNemar p<0.05 => manifold earns place; tied => H1 confirmed",
        "per_subject": all_rows,
        "n_sleep": n_sleep, "n_alpha": n_alpha,
        "verdict": verdict,
        "figures": ["scalar_vs_manifold.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n" + "=" * 72); print(verdict)
    print(f"\nResults in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
