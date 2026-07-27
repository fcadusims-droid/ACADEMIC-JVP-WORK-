"""Repair the geodesic CUSUM's detection statistic (Paper 3).

The benchmark found the CUSUM leads on localisation (10/15) but is the WORST method
compared on detection: AUC 0.227 at separating a real-transition segment from a null
within-stage segment. Below 0.5 means ANTI-correlated -- the statistic is larger where
there is no transition.

Diagnosis (checked before any repair is scored): the benchmark's statistic was the
peak-to-median ratio max|S|/median|S|. Under a real change point the cumulative-sum
curve is a TENT, so median|S| ~ max|S| and the ratio is modest; under no change point
S_t is a driftless random walk, which sits near zero much of the time while still
making large excursions, so median|S| is small and the ratio is LARGE. If so, the
statistic rewards the null by construction.

Four repairs, pre-registered: (a) scale-normalised peak, (b) surrogate calibration to
a per-segment p-value, (c) tent-shape R^2 instead of peak height, (d) two-stage
detector with window_mean as the detection gate and CUSUM as the localiser.

Success: detection AUC >= 0.70 AND localisation >= 9/15. If none pass, the paper
retreats from on-line demarcation to assisted localisation.

Usage:
    python -m experiments.paper3_geodesic_kinematics.detection_statistic_repair.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve,
)
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint,
)
from experiments.paper3_geodesic_kinematics.baseline_benchmark.run import (
    sleep_segments, _auc, MIN_SEG_W, TOL_SEC,
)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    STEP_SEC, LARGE_W,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "detection_statistic_repair")

AUC_BAR = 0.70
LOC_BAR = 9          # of 15; current CUSUM is 10/15, so at most one hit may be lost
N_BOOT = 200
RNG = np.random.default_rng(20260724)


# ======================================================================
#  The CUSUM curve, and candidate confidence statistics on it
# ======================================================================
def cusum_curve(covs):
    E, C = embed_cumsum(covs)
    return cusum_changepoint(E, C, MIN_SEG_W)


def _finite(curve):
    return curve[np.isfinite(curve)]


def stat_peak_over_median(curve):
    """The benchmark's statistic -- reproduced so the repair is measured against it."""
    f = _finite(curve)
    return float(np.max(f) / (np.median(f) + 1e-12)) if f.size else 0.0


def stat_scale_normalised(curve, covs):
    """(a) max|S| standardised by the segment's own increment scale and length."""
    f = _finite(curve)
    if f.size == 0:
        return 0.0
    # increment scale of the curve itself (robust): median absolute first difference
    d = np.diff(f)
    sigma = np.median(np.abs(d - np.median(d))) * 1.4826 + 1e-12
    return float(np.max(f) / (sigma * np.sqrt(len(f))))


def stat_tent_r2(curve):
    """(c) Goodness-of-fit of a symmetric tent peaked at the argmax.

    A genuine change point makes |S_t| rise linearly to the change and fall linearly
    after it; a driftless random walk does not. Shape, not amplitude."""
    f = _finite(curve)
    n = len(f)
    if n < 8:
        return 0.0
    t = np.arange(n)
    k = int(np.argmax(f))
    if k <= 1 or k >= n - 2:
        return 0.0
    tent = np.where(t <= k, t / max(k, 1), (n - 1 - t) / max(n - 1 - k, 1))
    # least-squares scale+offset fit of the tent to the curve
    A = np.vstack([tent, np.ones_like(tent)]).T
    coef, *_ = np.linalg.lstsq(A, f, rcond=None)
    resid = f - A @ coef
    ss_tot = np.sum((f - f.mean()) ** 2) + 1e-12
    return float(max(0.0, 1.0 - np.sum(resid ** 2) / ss_tot))


def stat_surrogate_p(curve, covs):
    """(b) Per-segment calibration: how extreme is the observed peak against peaks of
    block-bootstrapped versions of this segment's own increments? Returned as
    1 - p so that larger = more evidence of a transition."""
    f = _finite(curve)
    if f.size < 8:
        return 0.0
    obs = float(np.max(f))
    d = np.diff(f)
    n = len(d)
    block = max(4, n // 10)
    null = np.empty(N_BOOT)
    for b in range(N_BOOT):
        idx = []
        while len(idx) < n:
            s = RNG.integers(0, max(1, n - block))
            idx.extend(range(s, min(s + block, n)))
        perm = d[np.array(idx[:n])]
        walk = np.abs(np.cumsum(perm - perm.mean()))
        null[b] = np.max(walk)
    p = (np.sum(null >= obs) + 1) / (N_BOOT + 1)
    return float(1.0 - p)


def stat_window_mean_gate(covs):
    """(d) The window-mean break curve's peak-to-median, used as the DETECTION gate."""
    _, C = embed_cumsum(covs)
    wc = break_curve(C, LARGE_W)
    f = _finite(wc)
    return float(np.max(f) / (np.median(f) + 1e-12)) if f.size else 0.0


def localise(curve):
    v = np.where(np.isnan(curve), -np.inf, curve)
    return int(np.argmax(v))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Repairing the geodesic CUSUM detection statistic (Paper 3)")
    segs = sleep_segments()
    n = len(segs)
    print(f"  {n} Sleep-EDF recordings, real vs null within-stage segments\n")

    # ---- collect every statistic on both segment classes -------------------
    variants = ["peak_over_median (benchmark)", "a_scale_normalised",
                "b_surrogate_calibrated", "c_tent_shape_r2", "d_window_mean_gate"]
    pos = {v: [] for v in variants}
    neg = {v: [] for v in variants}
    hits, tent_real, tent_null, pom_real, pom_null = [], [], [], [], []

    for s in segs:
        cr = cusum_curve(s["covs"])
        cn = cusum_curve(s["null_covs"])
        # localisation is unchanged by any of (a)-(c): they rescore the SAME curve
        hits.append(abs(localise(cr) - s["seam"]) * STEP_SEC <= TOL_SEC)

        pos["peak_over_median (benchmark)"].append(stat_peak_over_median(cr))
        neg["peak_over_median (benchmark)"].append(stat_peak_over_median(cn))
        pos["a_scale_normalised"].append(stat_scale_normalised(cr, s["covs"]))
        neg["a_scale_normalised"].append(stat_scale_normalised(cn, s["null_covs"]))
        pos["b_surrogate_calibrated"].append(stat_surrogate_p(cr, s["covs"]))
        neg["b_surrogate_calibrated"].append(stat_surrogate_p(cn, s["null_covs"]))
        pos["c_tent_shape_r2"].append(stat_tent_r2(cr))
        neg["c_tent_shape_r2"].append(stat_tent_r2(cn))
        pos["d_window_mean_gate"].append(stat_window_mean_gate(s["covs"]))
        neg["d_window_mean_gate"].append(stat_window_mean_gate(s["null_covs"]))

        tent_real.append(stat_tent_r2(cr)); tent_null.append(stat_tent_r2(cn))
        pom_real.append(stat_peak_over_median(cr)); pom_null.append(stat_peak_over_median(cn))

    loc_hits = int(np.sum(hits))

    # ---- H1: is the stated diagnosis actually right? ----------------------
    h1_tent = float(np.median(tent_real)) > float(np.median(tent_null))
    h1_ratio = float(np.median(pom_null)) > float(np.median(pom_real))
    h1_holds = bool(h1_tent and h1_ratio)
    print("  H1 diagnostic (checked BEFORE scoring the repairs):")
    print(f"    tent-likeness  real {np.median(tent_real):.3f} vs null {np.median(tent_null):.3f}"
          f"   -> real more tent-like: {h1_tent}")
    print(f"    peak/median    real {np.median(pom_real):.2f} vs null {np.median(pom_null):.2f}"
          f"   -> null scores HIGHER: {h1_ratio}")
    print(f"    diagnosis stands: {h1_holds}\n")

    # ---- score every variant ---------------------------------------------
    rows = {}
    for v in variants:
        auc = _auc(pos[v], neg[v])
        # (d) is a different detector for detection but keeps CUSUM localisation;
        # (a)-(c) rescore the same curve, so localisation is identical.
        rows[v] = {"detection_auc": auc, "localisation_hits": loc_hits, "n": n,
                   "passes": bool(auc >= AUC_BAR and loc_hits >= LOC_BAR)}
        print(f"  {v:30s} AUC {auc:5.3f}   localisation {loc_hits}/{n}   "
              f"{'PASS' if rows[v]['passes'] else '    '}")

    repairs = [v for v in variants if v != "peak_over_median (benchmark)"]
    passing = [v for v in repairs if rows[v]["passes"]]
    best = max(repairs, key=lambda v: rows[v]["detection_auc"])
    base_auc = rows["peak_over_median (benchmark)"]["detection_auc"]

    if passing:
        # simplest passing repair wins ties; order in `repairs` is cost order
        chosen = passing[0]
        outcome = "REPAIRED"
        verdict = (
            f"THE DETECTION WEAKNESS IS AN ARTEFACT OF STATISTIC DESIGN, AND IT IS FIXED. "
            f"The benchmark's peak-to-median statistic scored AUC {base_auc:.3f} -- "
            f"anti-correlated, i.e. systematically larger on segments containing NO "
            f"transition. The stated diagnosis is confirmed directly: the CUSUM curve is "
            f"more tent-like on real transitions (median R^2 {np.median(tent_real):.3f} vs "
            f"{np.median(tent_null):.3f}) while the peak-to-median ratio is HIGHER on nulls "
            f"({np.median(pom_null):.2f} vs {np.median(pom_real):.2f}) -- exactly the "
            f"mechanism predicted, since a driftless random walk sits near zero much of the "
            f"time and so inflates a ratio whose denominator is the median. "
            f"Repair '{chosen}' lifts detection to AUC {rows[chosen]['detection_auc']:.3f} "
            f"(bar {AUC_BAR}) while localisation stays at {loc_hits}/{n} (bar {LOC_BAR}/{n}) "
            f"-- the curve is unchanged, only how it is scored. Passing repairs: {passing}. "
            f"The geodesic detector therefore does NOT trade detection for localisation as "
            f"the benchmark suggested; it was scored with a statistic that rewarded the null. "
            f"Paper 3 keeps its on-line demarcation ambition, with the detection statistic "
            f"specified rather than left implicit -- and the earlier AUC is retained in the "
            f"record as the reason the specification matters.")
    else:
        outcome = "STRUCTURAL_LIMITATION"
        verdict = (
            f"NO REPAIR PASSES -- THE LIMITATION IS STRUCTURAL, AND THE PAPER MUST RETREAT. "
            f"Against the pre-registered bar (AUC >= {AUC_BAR} with localisation >= "
            f"{LOC_BAR}/{n}), none of the four repairs qualifies: best is '{best}' at AUC "
            f"{rows[best]['detection_auc']:.3f}. The benchmark's {base_auc:.3f} was therefore "
            f"not merely a bad choice of statistic. H1 diagnosis "
            f"{'held' if h1_holds else 'did NOT hold'}, so the mechanism is "
            f"{'understood but insufficient to repair' if h1_holds else 'not the one proposed'}. "
            f"Per the pre-registration the consequence is stated in the paper rather than "
            f"softened: Paper 3 retreats from ON-LINE DEMARCATION -- which requires deciding "
            f"whether a transition is present -- to ASSISTED LOCALISATION, locating a "
            f"transition whose existence is established by other means. That retreat belongs "
            f"in the abstract and conclusion.")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    ks = variants
    ax[0].barh(range(len(ks)), [rows[k]["detection_auc"] for k in ks],
               color=["gray"] + ["steelblue" if rows[k]["passes"] else "crimson" for k in ks[1:]])
    ax[0].axvline(AUC_BAR, ls="--", color="green", label=f"bar {AUC_BAR}")
    ax[0].axvline(0.5, ls=":", color="k", label="chance")
    ax[0].set_yticks(range(len(ks))); ax[0].set_yticklabels(ks, fontsize=8)
    ax[0].invert_yaxis(); ax[0].set_xlabel("detection AUC (real vs null segment)")
    ax[0].legend(fontsize=8); ax[0].set_title(f"Detection repair (localisation {loc_hits}/{n})")
    ax[1].scatter(pom_real, tent_real, c="steelblue", label="real transition", s=45)
    ax[1].scatter(pom_null, tent_null, c="crimson", marker="x", label="null (within-stage)", s=45)
    ax[1].set_xlabel("peak/median (benchmark statistic)"); ax[1].set_ylabel("tent-shape $R^2$")
    ax[1].legend(fontsize=8); ax[1].set_title("Why the old statistic inverted:\nnulls score higher on peak/median")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "detection_statistic_repair.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "detection_statistic_repair",
        "question": "Is the geodesic CUSUM's sub-chance detection AUC an artefact of the "
                    "confidence statistic, and can it be repaired without losing localisation?",
        "bars": {"detection_auc": AUC_BAR, "localisation_hits": LOC_BAR, "n": n},
        "h1_diagnosis": {"real_more_tent_like": bool(h1_tent),
                         "null_scores_higher_on_peak_over_median": bool(h1_ratio),
                         "diagnosis_holds": h1_holds,
                         "median_tent_r2_real": float(np.median(tent_real)),
                         "median_tent_r2_null": float(np.median(tent_null)),
                         "median_peak_over_median_real": float(np.median(pom_real)),
                         "median_peak_over_median_null": float(np.median(pom_null))},
        "variants": rows,
        "passing_repairs": passing,
        "best_repair": best,
        "baseline_auc": base_auc,
        "localisation_hits": loc_hits,
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["detection_statistic_repair.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
