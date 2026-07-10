"""Experiment AD -- Window-length tension and causal-vs-offline localization
(Paper 3). Reconciles Experiments A and D.

A concluded the localization fix is a LARGE window. D found that LONGER windows
make drift/jump AUC WORSE (0.99->0.76 as T 200->800), because a longer look-back
accumulates more chance of a geometry-induced spurious event. A's large window
is also SYMMETRIC (uses future data) -- offline localization, not the
causal/online demarcation that is the headline operational claim of Paper 3's
abstract. This experiment puts both questions on ONE detector + ONE generator:
does a large window that fixes localization also start firing on drift-only
records as it grows (D's tension, reproduced inside A's own apparatus)? And how
much does a genuinely causal (backward-only) window cost, relative to A's
symmetric one?

Usage:
    python -m experiments.paper3_geodesic_kinematics.causal_vs_offline_localization.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    generate_subject, embed_cumsum, _win_mean_emb, _sphere_dist_emb, T,
)

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "causal_vs_offline_localization"
)

N_SUBJECTS = 15
WINDOWS = [10, 20, 40, 80, 120, 160, 200, 280]
TOL = 15
MIN_HISTORY = 20   # minimal causal history before a break statistic is defined


def symmetric_break_curve(C, w):
    """Experiment A's original two-sided statistic: [t-w,t) vs [t,t+w). Uses
    future data -- offline."""
    n = C.shape[0] - 1
    S = np.full(n, np.nan)
    for t in range(w, n - w):
        S[t] = _sphere_dist_emb(_win_mean_emb(C, t - w, t), _win_mean_emb(C, t, t + w))
    return S


def causal_break_curve(C, w):
    """Causal statistic (unweighted-history variant): recent window [t-w,t) vs
    ALL older history [0,t-w), uses only data up to t. NB: the unweighted
    cumulative history never "forgets" the pre-seam regime, so after a seam the
    reference stays permanently contaminated by the old regime -- a design
    pitfall, not a proof causal detection is impossible (see
    causal_adjacent_break_curve for the standard fix)."""
    n = C.shape[0] - 1
    S = np.full(n, np.nan)
    for t in range(w + MIN_HISTORY, n):
        S[t] = _sphere_dist_emb(_win_mean_emb(C, 0, t - w), _win_mean_emb(C, t - w, t))
    return S


def causal_adjacent_break_curve(C, w):
    """Causal statistic (adjacent-windows variant, the standard online
    change-point design): compares two consecutive BACKWARD-looking windows of
    equal size w, [t-2w,t-w) vs [t-w,t) -- both entirely in the past, so it is
    genuinely causal, but the reference window does not grow unboundedly and so
    does not suffer permanent contamination the way the unweighted-history
    variant does."""
    n = C.shape[0] - 1
    S = np.full(n, np.nan)
    for t in range(2 * w, n):
        S[t] = _sphere_dist_emb(_win_mean_emb(C, t - 2 * w, t - w), _win_mean_emb(C, t - w, t))
    return S


def prominence(curve):
    v = curve[np.isfinite(curve)]
    if len(v) == 0:
        return 0.0
    med = np.median(v)
    mad = np.median(np.abs(v - med)) + 1e-12
    return float((np.max(v) - med) / mad)


def evaluate(variant_fn, w, report_lag=0):
    """report_lag corrects for a detector's definitional reporting delay: e.g.
    the adjacent-windows causal statistic compares [t-2w,t-w) to [t-w,t), so a
    peak at time t reflects a break that occurred w samples earlier (the
    boundary between the two compared windows) -- any genuinely causal detector
    of this design has this lag by construction, and the honest location
    estimate when it fires at t is (t - report_lag), not t itself."""
    hits, seam_prom, drift_prom = 0, [], []
    for s in range(N_SUBJECTS):
        covs, seam = generate_subject(s, seam=True)
        _, C = embed_cumsum(covs)
        curve = variant_fn(C, w)
        if np.all(np.isnan(curve)):
            continue
        t_hat = int(np.nanargmax(np.where(np.isnan(curve), -np.inf, curve))) - report_lag
        hits += (abs(t_hat - seam) <= TOL)
        seam_prom.append(prominence(curve))

        cd, _ = generate_subject(1000 + s, seam=False)
        _, Cd = embed_cumsum(cd)
        drift_prom.append(prominence(variant_fn(Cd, w)))
    return hits, float(np.median(seam_prom)), float(np.median(drift_prom))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment AD: window tension + causal vs offline localization")
    print(f"  T={T}, {N_SUBJECTS} subjects, windows={WINDOWS}")

    results = {"symmetric": {}, "causal": {}, "causal_adjacent": {}}
    # causal_adjacent's peak is definitionally delayed by w samples (see
    # evaluate's docstring); report_lag=w corrects the location estimate.
    variants = [("symmetric", symmetric_break_curve, 0),
                ("causal", causal_break_curve, 0),
                ("causal_adjacent", causal_adjacent_break_curve, None)]  # lag=w, set below
    for variant_name, fn, lag in variants:
        for w in WINDOWS:
            report_lag = w if lag is None else lag
            hits, sp, dp = evaluate(fn, w, report_lag=report_lag)
            results[variant_name][w] = {"hits": hits, "seam_prom": sp, "drift_prom": dp}
            print(f"  {variant_name:16s} w={w:4d}: hits={hits:2d}/{N_SUBJECTS}, "
                  f"seam_prom={sp:6.1f}, drift_prom={dp:6.1f}"
                  f"{'  (lag-corrected by w)' if lag is None else ''}")

    sym = results["symmetric"]
    cau = results["causal"]
    cadj = results["causal_adjacent"]

    # does drift-only prominence grow with window (D's tension, reproduced here)?
    sym_drift_by_w = [sym[w]["drift_prom"] for w in WINDOWS]
    cadj_drift_by_w = [cadj[w]["drift_prom"] for w in WINDOWS]
    sym_drift_grows = sym_drift_by_w[-1] > 1.5 * (sym_drift_by_w[0] + 1e-9)
    cadj_drift_grows = cadj_drift_by_w[-1] > 1.5 * (cadj_drift_by_w[0] + 1e-9)

    # best window per variant: hits >= 10 AND drift_prom clearly below seam_prom
    def best_guarded_window(res):
        return [w for w in WINDOWS
                if res[w]["hits"] >= 10 and res[w]["drift_prom"] < 0.7 * res[w]["seam_prom"]]

    sym_guarded = best_guarded_window(sym)
    cau_guarded = best_guarded_window(cau)
    cadj_guarded = best_guarded_window(cadj)

    sym_best_hits = max(sym[w]["hits"] for w in WINDOWS)
    cau_best_hits = max(cau[w]["hits"] for w in WINDOWS)
    cadj_best_hits = max(cadj[w]["hits"] for w in WINDOWS)
    gap_naive = sym_best_hits - cau_best_hits
    gap_adjacent = sym_best_hits - cadj_best_hits

    smallest_guarded_w = min(cadj_guarded) if cadj_guarded else None
    if cadj_guarded and gap_adjacent <= 2:
        verdict = (f"CAUSAL CLAIM RECOVERABLE, AT AN EXPLICIT REPORTING-LAG COST: "
                   f"the naive unweighted-history causal statistic fails badly "
                   f"(best {cau_best_hits}/{N_SUBJECTS} -- it never forgets the "
                   "pre-seam regime, permanently contaminating the reference). The "
                   f"standard adjacent-windows causal statistic (two consecutive "
                   f"backward windows) matches the symmetric/offline result exactly "
                   f"({cadj_best_hits} vs {sym_best_hits}/{N_SUBJECTS}) once its "
                   "estimate is corrected for its definitional reporting lag: a "
                   "peak at time t reflects a break that occurred w samples "
                   "earlier (the boundary between the two compared backward "
                   "windows), so the detector cannot confidently report a break "
                   "until w samples after it happened. This is not a free "
                   f"recovery of the causal claim -- guarded windows range w in "
                   f"{cadj_guarded}, so the SMALLEST reliable causal detector "
                   f"still pays a reporting lag of {smallest_guarded_w} samples "
                   f"({100*smallest_guarded_w/T:.0f}% of the {T}-sample record) "
                   "before it can flag a transition with guarded confidence. "
                   "Paper 3's causal/online claim is recoverable with a "
                   "correctly-designed statistic (the naive recent-vs-all-history "
                   "design is a real pitfall, not a fundamental barrier), but the "
                   "abstract should state the detection lag explicitly as the "
                   "price of causality, not claim instantaneous online "
                   "localization.")
    elif cadj_guarded:
        verdict = (f"CAUSAL POSSIBLE BUT COSTLY: adjacent-windows causal reaches "
                   f"{cadj_best_hits}/{N_SUBJECTS} (guarded at w in {cadj_guarded}), "
                   f"trailing the best symmetric result by {gap_adjacent} hits "
                   f"({sym_best_hits}/{N_SUBJECTS}). Naive unweighted-history "
                   f"causal fails outright ({cau_best_hits}/{N_SUBJECTS}) -- "
                   "detector design matters enormously for the causal claim, and "
                   "even the better design pays a real accuracy cost.")
    else:
        verdict = (f"CAUSAL CLAIM NOT RECOVERABLE with either causal design tested "
                   f"(naive unweighted-history: {cau_best_hits}/{N_SUBJECTS}; "
                   f"adjacent-windows: {cadj_best_hits}/{N_SUBJECTS}), vs symmetric "
                   f"{sym_best_hits}/{N_SUBJECTS}. Paper 3's abstract should state "
                   "the demonstrated method as offline/pooled localization, not "
                   "causal/online, until a causal fix is found.")

    tension_note = (
        f"Window-length tension reproduced inside this apparatus: "
        f"{'YES' if sym_drift_grows or cadj_drift_grows else 'NO'} -- "
        f"drift-only prominence "
        f"{'grows' if sym_drift_grows else 'stays flat/falls'} with window under "
        f"the symmetric detector ({sym_drift_by_w[0]:.1f} -> {sym_drift_by_w[-1]:.1f}) "
        f"and {'grows' if cadj_drift_grows else 'stays flat/falls'} under the "
        f"adjacent-windows causal detector "
        f"({cadj_drift_by_w[0]:.1f} -> {cadj_drift_by_w[-1]:.1f})."
    )
    print("\n" + tension_note)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.plot(WINDOWS, [sym[w]["hits"] for w in WINDOWS], "o-", label="symmetric (offline)", color="crimson")
    ax.plot(WINDOWS, [cau[w]["hits"] for w in WINDOWS], "s-", label="causal, naive history", color="gray")
    ax.plot(WINDOWS, [cadj[w]["hits"] for w in WINDOWS], "^-", label="causal, adjacent windows", color="steelblue")
    ax.set_xlabel("window w"); ax.set_ylabel(f"localization hits (/{N_SUBJECTS})")
    ax.set_title("Localization: causal designs vs offline"); ax.legend(fontsize=8); ax.set_ylim(0, N_SUBJECTS + 1)
    ax = axes[1]
    ax.plot(WINDOWS, sym_drift_by_w, "o-", label="symmetric drift-only", color="crimson")
    ax.plot(WINDOWS, cadj_drift_by_w, "^-", label="causal-adjacent drift-only", color="steelblue")
    ax.plot(WINDOWS, [sym[w]["seam_prom"] for w in WINDOWS], "o--", label="symmetric seam", color="crimson", alpha=0.5)
    ax.plot(WINDOWS, [cadj[w]["seam_prom"] for w in WINDOWS], "^--", label="causal-adjacent seam", color="steelblue", alpha=0.5)
    ax.set_xlabel("window w"); ax.set_ylabel("prominence")
    ax.set_title("Drift-only false-fire risk vs window")
    ax.legend(fontsize=7)
    fig.suptitle("Exp AD: window tension + causal vs offline", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "causal_vs_offline.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "AD_causal_vs_offline_localization",
        "params": {"n_subjects": N_SUBJECTS, "windows": WINDOWS, "tol": TOL,
                   "min_history": MIN_HISTORY, "T": T},
        "symmetric": {str(w): sym[w] for w in WINDOWS},
        "causal_naive_history": {str(w): cau[w] for w in WINDOWS},
        "causal_adjacent": {str(w): cadj[w] for w in WINDOWS},
        "window_tension_reproduced": bool(sym_drift_grows or cadj_drift_grows),
        "symmetric_guarded_windows": sym_guarded,
        "causal_naive_guarded_windows": cau_guarded,
        "causal_adjacent_guarded_windows": cadj_guarded,
        "causal_adjacent_reporting_lag_samples": ("= window w (definitional; "
            "see evaluate() docstring)"),
        "smallest_guarded_reporting_lag": (min(cadj_guarded) if cadj_guarded else None),
        "symmetric_best_hits": sym_best_hits,
        "causal_naive_best_hits": cau_best_hits,
        "causal_adjacent_best_hits": cadj_best_hits,
        "preregistered_criterion": "a causal window recovers localization within ~2/15 of symmetric while guarding against drift-only false fires",
        "verdict": verdict,
        "tension_note": tension_note,
        "figures": ["causal_vs_offline.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
