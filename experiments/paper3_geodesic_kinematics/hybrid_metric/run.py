"""Hybrid drift-robust jump statistic for the Exp D structural corner (Paper 3).

Experiment D found a structural region -- weak-but-detectable jump (collapse ~0.7)
crossed with moderate/strong geodesic drift -- where the square-root-metric jump
statistic cannot separate a collapse from a drift (AUC -> 0.61): a strong geodesic
drift, anti-developed by direct parallel transport, accumulates a slowly-varying
holonomy term whose peak looks like a jump. Exp D flagged that corner as needing a
"method change (hybrid metric)".

This tests a concrete drift-robust component, kept on the SAME square-root geometry
(so jump power is preserved): a jump is a HIGH-frequency event (a single-step
increment), whereas the drift+holonomy contamination is LOW-frequency (a slow
accumulating trend). High-pass filtering the anti-developed increments (subtract a
local moving average) should remove the drift/holonomy trend while leaving an
abrupt jump almost untouched -- so the residual jump statistic separates collapse
from drift in the corner, without hurting jump power on genuine collapses.

Compares the original square-root jump statistic against the hybrid (high-pass)
one on the Exp D grid, reporting AUC(collapse vs drift) and jump power for both.

Usage:
    python -m experiments.paper3_geodesic_kinematics.hybrid_metric.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

from experiments.shared_lib import manifold_trajectory as mt
from experiments.shared_lib import jump_diffusion as jd
from experiments.shared_lib import stats_utils as su

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "hybrid_metric"
)

DRIFT_STRENGTHS = [0.0, 0.1, 0.2, 0.3, 0.4]
COLLAPSE_FACTORS = [0.7, 0.5, 0.3, 0.1]     # weak (corner) -> strong (control)
N_SEEDS = 60
N_DIM = 3
T0 = 400
DIFFUSION = 0.02
FPR_TARGET = 0.05
ANCHOR_WINDOW = 5
HP_WINDOW = 15                               # high-pass moving-average width


def _anchored_max(rnorm, cov, anchor_window=ANCHOR_WINDOW):
    T = len(rnorm)
    a = int(np.argmax(cov))
    lo, hi = max(0, a - anchor_window), min(T, a + anchor_window + 1)
    return float(np.max(rnorm[lo:hi]))


def jump_stat_original(inc):
    """Square-root-metric jump statistic (as in Exp D): covariate-anchored max
    increment norm / bipower scale."""
    cov = jd.conditional_residual_variance(np.cumsum(inc, axis=0))
    rnorm = np.linalg.norm(inc, axis=1)
    return _anchored_max(rnorm, cov) / max(su.bipower_scale(inc), 1e-12)


def jump_stat_hybrid(inc, hp_window=HP_WINDOW):
    """Drift-robust hybrid: high-pass the anti-developed increments (subtract a
    centered moving average, removing the slow drift/holonomy trend), then apply
    the same covariate-anchored jump statistic to the residual. An abrupt jump
    survives the high-pass (a single spike is barely dented by a width-15 average);
    a slow drift/holonomy trend is removed."""
    trend = uniform_filter1d(inc, size=hp_window, axis=0, mode="nearest")
    r = inc - trend
    cov = jd.conditional_residual_variance(np.cumsum(r, axis=0))
    rnorm = np.linalg.norm(r, axis=1)
    return _anchored_max(rnorm, cov) / max(su.bipower_scale(r), 1e-12)


def auc(pos, neg):
    pos, neg = np.asarray(pos), np.asarray(neg)
    allv = np.concatenate([pos, neg])
    ranks = np.argsort(np.argsort(allv)) + 1
    u = ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0
    return u / (len(pos) * len(neg))


def sim_stats(regime, seed0, drift=0.0, cfac=0.05):
    orig = np.empty(N_SEEDS)
    hyb = np.empty(N_SEEDS)
    for s in range(N_SEEDS):
        cfg = mt.ManifoldSimConfig(n=N_DIM, T=T0, drift_strength=drift,
                                   diffusion_scale=DIFFUSION, jump_time=T0 // 2,
                                   collapse_factor=cfac, seed=seed0 + s)
        rhos, _ = mt.simulate_manifold_regime(regime, cfg)
        inc = mt.anti_develop(rhos, "sqrt")
        orig[s] = jump_stat_original(inc)
        hyb[s] = jump_stat_hybrid(inc)
    return orig, hyb


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Hybrid drift-robust jump statistic vs the Exp D structural corner")

    # dispersion for per-statistic thresholds
    disp_o, disp_h = sim_stats("dispersion", 3000)
    thr_o = float(np.quantile(disp_o, 1 - FPR_TARGET))
    thr_h = float(np.quantile(disp_h, 1 - FPR_TARGET))

    drift_o, drift_h = {}, {}
    for i, ds in enumerate(DRIFT_STRENGTHS):
        drift_o[ds], drift_h[ds] = sim_stats("drift", 300_000 + 100 * i, drift=ds)
    coll_o, coll_h = {}, {}
    for k, cf in enumerate(COLLAPSE_FACTORS):
        coll_o[cf], coll_h[cf] = sim_stats("collapse", 100_000 + 100 * k, cfac=cf)

    nd, nc = len(DRIFT_STRENGTHS), len(COLLAPSE_FACTORS)
    auc_o = np.zeros((nd, nc)); auc_h = np.zeros((nd, nc))
    for i, ds in enumerate(DRIFT_STRENGTHS):
        for k, cf in enumerate(COLLAPSE_FACTORS):
            auc_o[i, k] = auc(coll_o[cf], drift_o[ds])
            auc_h[i, k] = auc(coll_h[cf], drift_h[ds])
    power_o = np.array([np.mean(coll_o[cf] > thr_o) for cf in COLLAPSE_FACTORS])
    power_h = np.array([np.mean(coll_h[cf] > thr_h) for cf in COLLAPSE_FACTORS])

    # the corner = weak jump (collapse 0.7, col 0) x moderate/strong drift (rows >=2)
    corner_o = auc_o[2:, 0]
    corner_h = auc_h[2:, 0]
    worst_o = float(np.min(auc_o[2:, 0]))
    worst_h = float(np.min(auc_h[2:, 0]))
    # jump power on genuine strong collapses (collapse <= 0.3, cols 2,3)
    strong_power_o = float(np.min(power_o[2:]))
    strong_power_h = float(np.min(power_h[2:]))

    recovered = worst_h >= 0.85 and strong_power_h >= 0.8
    improved = worst_h > worst_o + 0.05
    if recovered:
        verdict = (f"HYBRID RECOVERS THE CORNER: the high-pass drift-robust statistic "
                   f"lifts the worst weak-jump x strong-drift AUC from {worst_o:.2f} "
                   f"(square-root) to {worst_h:.2f} (>= 0.85), while keeping jump "
                   f"power on genuine strong collapses ({strong_power_h:.2f}). The "
                   "structural corner Exp D flagged is a fixable drift/holonomy "
                   "contamination, not an intrinsic geometric limit: high-passing the "
                   "anti-developed increments removes the slow holonomy trend a strong "
                   "geodesic drift accumulates, leaving the abrupt jump. The hybrid "
                   "keeps the square-root geometry (hence jump sensitivity) and adds "
                   "only a drift-robust high-pass -- exactly the 'hybrid metric' Exp D "
                   "called for.")
    elif improved and strong_power_h >= 0.8:
        verdict = (f"HYBRID HELPS BUT DOES NOT FULLY CLOSE THE CORNER: worst corner "
                   f"AUC {worst_o:.2f} -> {worst_h:.2f} (jump power preserved "
                   f"{strong_power_h:.2f}). The drift/holonomy contamination is partly "
                   "high-frequency, so a single high-pass reduces but does not "
                   "eliminate the confusion; a stronger drift model (e.g. along-path "
                   "transport) would be the next step.")
    elif improved:
        verdict = (f"HYBRID IMPROVES SEPARABILITY BUT COSTS JUMP POWER: corner AUC "
                   f"{worst_o:.2f} -> {worst_h:.2f}, but jump power on strong collapses "
                   f"drops to {strong_power_h:.2f} (from {strong_power_o:.2f}) -- the "
                   "high-pass also dents genuine jumps, so it is not a free fix.")
    else:
        verdict = (f"HYBRID DOES NOT HELP: worst corner AUC {worst_o:.2f} -> "
                   f"{worst_h:.2f}. The drift/jump confusion is not a low-frequency "
                   "contamination removable by high-passing; the corner is a genuine "
                   "geometric limit of the square-root anti-development, and a true "
                   "metric change (not a filtered statistic) is required.")

    # figure: AUC grids original vs hybrid + jump power
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for ax, M, title in [(axes[0], auc_o, "square-root: AUC(collapse vs drift)"),
                         (axes[1], auc_h, "HYBRID (high-pass): AUC")]:
        im = ax.imshow(M, origin="lower", aspect="auto", vmin=0.5, vmax=1.0, cmap="viridis")
        ax.set_xticks(range(nc)); ax.set_xticklabels(COLLAPSE_FACTORS)
        ax.set_yticks(range(nd)); ax.set_yticklabels(DRIFT_STRENGTHS)
        ax.set_xlabel("collapse factor"); ax.set_ylabel("drift strength"); ax.set_title(title)
        for i in range(nd):
            for k in range(nc):
                ax.text(k, i, f"{M[i,k]:.2f}", ha="center", va="center",
                        color="w" if M[i, k] < 0.85 else "k", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046)
    ax = axes[2]
    ax.plot(COLLAPSE_FACTORS, power_o, "o-", label="square-root")
    ax.plot(COLLAPSE_FACTORS, power_h, "s--", label="hybrid")
    ax.axhline(0.8, ls=":", color="gray"); ax.set_xlabel("collapse factor")
    ax.set_ylabel("jump power"); ax.set_title("jump power preserved?"); ax.legend()
    ax.set_ylim(0, 1.05); ax.invert_xaxis()
    fig.suptitle("Hybrid drift-robust jump statistic vs Exp D corner", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "hybrid_metric.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "hybrid_metric_drift_robust_jump",
        "params": {"drift_strengths": DRIFT_STRENGTHS, "collapse_factors": COLLAPSE_FACTORS,
                   "n_seeds": N_SEEDS, "n_dim": N_DIM, "diffusion": DIFFUSION,
                   "hp_window": HP_WINDOW},
        "auc_square_root": auc_o.tolist(),
        "auc_hybrid": auc_h.tolist(),
        "jump_power_square_root": power_o.tolist(),
        "jump_power_hybrid": power_h.tolist(),
        "worst_corner_auc_square_root": worst_o,
        "worst_corner_auc_hybrid": worst_h,
        "min_strong_jump_power_hybrid": strong_power_h,
        "verdict": verdict,
        "figures": ["hybrid_metric.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  worst corner AUC: square-root {worst_o:.2f} -> hybrid {worst_h:.2f}")
    print(f"  strong-jump power: square-root {strong_power_o:.2f} -> hybrid {strong_power_h:.2f}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
