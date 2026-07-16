"""Base-metric change for the Exp D structural corner (Paper 3).

Experiment D localized a corner -- weak jump (collapse ~0.7) x moderate/strong
geodesic drift -- where the square-root-metric jump statistic cannot separate a
collapse from a drift (AUC -> 0.61): a strong geodesic drift accumulates a slow
HOLONOMY term on the curved (K=1/4) square-root sphere whose peak mimics a jump.
The Hybrid probe showed a high-pass *statistic* on the same geometry does not fix
it, and concluded a true BASE-METRIC CHANGE is required. This runs that change.

Metrics are anti-developed PATH-WISE (each metric's own connection / holonomy),
which is essential: the corner confusion IS the square-root sphere's holonomy, a
path effect. (A base-point linearization that folds the path into the base frame
removes the holonomy and would spuriously "fix" every metric -- demonstrated here
by the `sqrt_base` control, which lifts the square-root corner from ~0.56 to ~0.95
precisely because it discards the holonomy.)

Fair path-wise comparison (each has a correct path-wise anti-development):
  * square-root (Wigner-Yanase / Bures ANGLE) -- committed baseline, exact
    step-log + sphere parallel transport (holonomy present);
  * log-Euclidean -- FLAT: zero curvature, so parallel transport is the identity
    and a geodesic drift accumulates ZERO holonomy -- the decisive test of whether
    the corner is holonomy-driven;
  * affine-invariant (AIRM) -- whitening transport; near-singular distance
    diverges (heavy-tailed collapse increment).

Supplementary (base-point linearized, flagged): Bures-Wasserstein (Wasserstein-2
geometry). Its path-wise parallel transport is not implemented, so it is developed
by the base-point BW log map; that convention under-represents its holonomy, so it
is an OPTIMISTIC reference for BW, not a fair path-wise test. Included because the
user asked for the Bures metric and the square-root baseline already realizes the
Bures *angle*.

Usage:
    python -m experiments.paper3_geodesic_kinematics.base_metric_corner.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.shared_lib import manifold_trajectory as mt
from experiments.shared_lib import jump_diffusion as jd
from experiments.shared_lib import stats_utils as su

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "base_metric_corner"
)

DRIFT_STRENGTHS = [0.0, 0.1, 0.2, 0.3, 0.4]
COLLAPSE_FACTORS = [0.7, 0.5, 0.3, 0.1]     # weak (corner) -> strong (control)
N_SEEDS = 60
N_DIM = 3
T0 = 400
DIFFUSION = 0.02
FPR_TARGET = 0.05
ANCHOR_WINDOW = 5

# fair path-wise metrics (correct anti-development for each) + supplementary/controls
PATHWISE = ["sqrt", "log_euclidean", "airm"]
SUPP = ["bures", "sqrt_base"]
ALL_KEYS = PATHWISE + SUPP
FAIR_ALTERNATIVES = ["log_euclidean", "airm"]     # judged by the decision rule
LABELS = {"sqrt": "square-root (Bures angle, path-wise)",
          "log_euclidean": "log-Euclidean (flat, zero holonomy)",
          "airm": "affine-invariant (path-wise)",
          "bures": "Bures-Wasserstein (base-linearized*)",
          "sqrt_base": "square-root (base-linearized control)"}


def _anti_dev(rhos, key):
    if key == "sqrt":
        return mt.anti_develop(rhos, "sqrt")            # exact path-wise, holonomy present
    if key == "log_euclidean":
        return mt.anti_develop(rhos, "log_euclidean")   # flat: path-wise == base, zero holonomy
    if key == "airm":
        return mt.anti_develop(rhos, "airm")            # whitening transport
    if key == "bures":
        return mt.anti_develop_base(rhos, "bures")      # base-linearized (no BW transport)
    if key == "sqrt_base":
        return mt.anti_develop_base(rhos, "sqrt")       # holonomy-removing control
    raise ValueError(key)


def _anchored_max(rnorm, cov, anchor_window=ANCHOR_WINDOW):
    T = len(rnorm)
    a = int(np.argmax(cov))
    lo, hi = max(0, a - anchor_window), min(T, a + anchor_window + 1)
    return float(np.max(rnorm[lo:hi]))


def jump_stat(inc):
    """Covariate-anchored jump statistic (identical form to Exp D / Hybrid),
    metric-agnostic: it consumes whatever anti-developed increments it is given."""
    cov = jd.conditional_residual_variance(np.cumsum(inc, axis=0))
    rnorm = np.linalg.norm(inc, axis=1)
    return _anchored_max(rnorm, cov) / max(su.bipower_scale(inc), 1e-12)


def auc(pos, neg):
    pos, neg = np.asarray(pos), np.asarray(neg)
    allv = np.concatenate([pos, neg])
    ranks = np.argsort(np.argsort(allv)) + 1
    u = ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0
    return u / (len(pos) * len(neg))


def sim_stats(regime, seed0, drift=0.0, cfac=0.05):
    out = {k: np.empty(N_SEEDS) for k in ALL_KEYS}
    for s in range(N_SEEDS):
        cfg = mt.ManifoldSimConfig(n=N_DIM, T=T0, drift_strength=drift,
                                   diffusion_scale=DIFFUSION, jump_time=T0 // 2,
                                   collapse_factor=cfac, seed=seed0 + s)
        rhos, _ = mt.simulate_manifold_regime(regime, cfg)
        for k in ALL_KEYS:
            out[k][s] = jump_stat(_anti_dev(rhos, k))
    return out


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Base-metric change vs the Exp D structural corner (Paper 3)")

    disp = sim_stats("dispersion", 3000)
    thr = {k: float(np.quantile(disp[k], 1 - FPR_TARGET)) for k in ALL_KEYS}

    drift_stats = {ds: sim_stats("drift", 300_000 + 100 * i, drift=ds)
                   for i, ds in enumerate(DRIFT_STRENGTHS)}
    coll_stats = {cf: sim_stats("collapse", 100_000 + 100 * k, cfac=cf)
                  for k, cf in enumerate(COLLAPSE_FACTORS)}

    nd, nc = len(DRIFT_STRENGTHS), len(COLLAPSE_FACTORS)
    auc_grid = {k: np.zeros((nd, nc)) for k in ALL_KEYS}
    power = {k: np.zeros(nc) for k in ALL_KEYS}
    for k in ALL_KEYS:
        for i, ds in enumerate(DRIFT_STRENGTHS):
            for j, cf in enumerate(COLLAPSE_FACTORS):
                auc_grid[k][i, j] = auc(coll_stats[cf][k], drift_stats[ds][k])
        power[k] = np.array([np.mean(coll_stats[cf][k] > thr[k]) for cf in COLLAPSE_FACTORS])

    # corner = weak jump (collapse 0.7, col 0) x moderate/strong drift (rows >= 2)
    worst = {k: float(np.min(auc_grid[k][2:, 0])) for k in ALL_KEYS}
    strong_power = {k: float(np.min(power[k][2:])) for k in ALL_KEYS}  # collapse <= 0.3

    print("\n  worst corner AUC (weak jump x strong drift) and strong-jump power:")
    for k in ALL_KEYS:
        print(f"    {LABELS[k]:42s}: worst_corner_AUC={worst[k]:.3f}  strong_power={strong_power[k]:.3f}")

    baseline = worst["sqrt"]
    # validity: the path-wise square-root MUST reproduce the corner confusion
    sqrt_reproduces = baseline <= 0.70
    # corroboration: base-linearization removes the holonomy (control >> baseline)
    holonomy_shown = worst["sqrt_base"] > baseline + 0.15

    resolved = [k for k in FAIR_ALTERNATIVES if worst[k] >= 0.85 and strong_power[k] >= 0.80]
    partial = [k for k in FAIR_ALTERNATIVES
               if worst[k] > baseline + 0.05 and strong_power[k] >= 0.80 and worst[k] < 0.85]
    tradeoff = [k for k in FAIR_ALTERNATIVES if worst[k] > baseline + 0.05 and strong_power[k] < 0.80]
    best_alt = max(FAIR_ALTERNATIVES, key=lambda k: worst[k])

    valid_note = ("" if sqrt_reproduces else
                  f" WARNING: the path-wise square-root did NOT reproduce the corner "
                  f"(worst={baseline:.2f} > 0.70); the run's premise is broken and the "
                  f"comparison is inconclusive.")
    corrob = (f" The base-linearized square-root control confirms the corner is "
              f"holonomy: folding the path into the base frame lifts it "
              f"{baseline:.2f} -> {worst['sqrt_base']:.2f}, i.e. discarding the "
              f"holonomy alone removes the confusion." if holonomy_shown else "")
    bures_note = (f" (Supplementary, base-linearized Bures-Wasserstein: worst corner "
                  f"{worst['bures']:.2f}, power {strong_power['bures']:.2f} -- optimistic, "
                  f"since its holonomy is not path-wise-transported.)")

    if resolved:
        best = max(resolved, key=lambda k: worst[k])
        outcome = "RESOLVED"
        verdict = (
            f"RESOLVED BY A BASE-METRIC CHANGE. The {LABELS[best]} base metric lifts "
            f"the worst weak-jump x strong-drift corner AUC from {baseline:.2f} "
            f"(square-root, path-wise) to {worst[best]:.2f} (>= 0.85) while keeping jump "
            f"power on genuine strong collapses at {strong_power[best]:.2f} (>= 0.80). "
            f"Because log-Euclidean is FLAT -- zero holonomy -- a strong geodesic drift "
            f"can no longer manufacture the holonomy pseudo-jump that fooled the "
            f"square-root statistic, so the weak collapse separates from the drift. The "
            f"Exp D corner is therefore a SQUARE-ROOT-CONNECTION (holonomy) limit that a "
            f"flat base metric repairs -- exactly the base-metric change the Hybrid "
            f"probe said was required, and which no same-geometry statistic could "
            f"supply.{corrob} Paper 3 Sec 6.4 should name {LABELS[best]} as the "
            f"drift/jump-robust base metric in the weak-collapse x strong-drift "
            f"corner.{bures_note}{valid_note}")
    elif partial:
        best = max(partial, key=lambda k: worst[k])
        outcome = "PARTIAL"
        verdict = (
            f"PARTIALLY AMELIORATED, NOT CLOSED. The {LABELS[best]} base metric improves "
            f"the worst corner AUC {baseline:.2f} -> {worst[best]:.2f} (jump power "
            f"{strong_power[best]:.2f} preserved) but falls short of 0.85. A base-metric "
            f"change moves the corner the right way -- part of the confusion is the "
            f"square-root connection -- but a residual, metric-robust overlap of a weak "
            f"collapse and a strong drift remains.{corrob}{bures_note}{valid_note}")
    elif tradeoff:
        best = max(tradeoff, key=lambda k: worst[k])
        outcome = "TRADEOFF"
        verdict = (
            f"SEPARATES ONLY BY DULLING JUMPS. The {LABELS[best]} base metric raises the "
            f"corner AUC {baseline:.2f} -> {worst[best]:.2f} but its jump power on strong "
            f"collapses falls to {strong_power[best]:.2f} (< 0.80): it buys corner "
            f"separability by flattening genuine jumps, not a free fix.{corrob}{bures_note}{valid_note}")
    else:
        outcome = "NO_HELP_METRIC_INDEPENDENT"
        verdict = (
            f"NO HELP -- A METRIC-INDEPENDENT LIMIT. No fair path-wise base metric lifts "
            f"the worst corner AUC more than 0.05 above the square-root baseline "
            f"({baseline:.2f}): log-Euclidean {worst['log_euclidean']:.2f} (power "
            f"{strong_power['log_euclidean']:.2f}), affine-invariant {worst['airm']:.2f} "
            f"(power {strong_power['airm']:.2f}). Crucially the FLAT log-Euclidean metric "
            f"-- exactly zero holonomy, so a geodesic drift cannot manufacture a holonomy "
            f"pseudo-jump -- still fails, which shows the weak-jump x strong-drift "
            f"confusion is NOT reducible to the square-root connection's holonomy but is "
            f"an INTRINSIC overlap of the two regimes' anti-developed increment "
            f"distributions. The appendix's hope that a hybrid/other metric would fix the "
            f"corner is closed NEGATIVE across the standard SPD base metrics, and Paper 3 "
            f"Sec 6.4/7 must state a weak partial collapse under strong drift as a genuine "
            f"limitation of the observable.{corrob}{bures_note}{valid_note}")

    # ---- figure ----------------------------------------------------------
    show = PATHWISE + ["bures"]
    fig, axes = plt.subplots(1, len(show) + 1, figsize=(4.5 * (len(show) + 1), 4.5))
    for ax, k in zip(axes[:-1], show):
        Mgrid = auc_grid[k]
        im = ax.imshow(Mgrid, origin="lower", aspect="auto", vmin=0.5, vmax=1.0, cmap="viridis")
        ax.set_xticks(range(nc)); ax.set_xticklabels(COLLAPSE_FACTORS)
        ax.set_yticks(range(nd)); ax.set_yticklabels(DRIFT_STRENGTHS)
        ax.set_xlabel("collapse factor"); ax.set_ylabel("drift strength")
        ax.set_title(f"{LABELS[k]}\nAUC(collapse vs drift)", fontsize=8)
        for i in range(nd):
            for j in range(nc):
                ax.text(j, i, f"{Mgrid[i,j]:.2f}", ha="center", va="center",
                        color="w" if Mgrid[i, j] < 0.85 else "k", fontsize=7)
    ax = axes[-1]
    for k in show:
        ax.plot(COLLAPSE_FACTORS, power[k], "o-", label=LABELS[k].split(" (")[0], markersize=4)
    ax.axhline(0.8, ls=":", color="gray"); ax.set_xlabel("collapse factor")
    ax.set_ylabel("jump power"); ax.set_title("jump power by base metric", fontsize=8)
    ax.legend(fontsize=6); ax.set_ylim(0, 1.05); ax.invert_xaxis()
    fig.suptitle("Base-metric change vs the Exp D weak-jump x strong-drift corner "
                 "(path-wise anti-development)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "base_metric_corner.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "base_metric_corner",
        "question": "Does a true base-metric change (log-Euclidean / affine-invariant; "
                    "Bures-Wasserstein supplementary) fix the Exp D weak-jump x "
                    "strong-drift corner the square-root metric and high-pass hybrid could not?",
        "params": {"drift_strengths": DRIFT_STRENGTHS, "collapse_factors": COLLAPSE_FACTORS,
                   "n_seeds": N_SEEDS, "n_dim": N_DIM, "diffusion": DIFFUSION},
        "anti_development": "path-wise (each metric's own connection) for sqrt/log_euclidean/"
                            "airm; base-point linearization for bures (supplementary) and "
                            "sqrt_base (holonomy-removing control)",
        "auc_grids": {k: auc_grid[k].tolist() for k in ALL_KEYS},
        "jump_power": {k: power[k].tolist() for k in ALL_KEYS},
        "worst_corner_auc": worst,
        "strong_jump_power": strong_power,
        "sqrt_pathwise_reproduces_corner": bool(sqrt_reproduces),
        "base_linearization_removes_holonomy": bool(holonomy_shown),
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["base_metric_corner.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
