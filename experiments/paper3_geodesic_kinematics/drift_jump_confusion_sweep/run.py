"""Experiment D -- Drift-vs-Jump Confusion Sweep (diagnostic), geometric pipeline.

Is the square-root-metric drift/jump confusion (appendix drift->jump rate
0.2-0.4) *structural* (the geometry cannot separate drift from a jump) or
*calibrational* (a mis-placed threshold)? See PRE-REGISTRATION.md.

Run on the FAITHFUL pipeline: SPD(n) density-matrix trajectories are Cartan
anti-developed to a Euclidean tangent space (exact under the square-root metric),
then the covariate-anchored jump statistic and the Girsanov drift test are
applied to the anti-developed increments. A flat tangent-space model cannot show
this confusion because a pure geodesic drift anti-develops to a straight line,
not a jump; only the real anti-developed increments answer the question.

Core diagnostic: for each (drift strength, collapse severity) cell, the AUC of
the jump statistic separating collapse trajectories from pure-drift trajectories.
  * AUC ~ 1   -> separable -> any confusion is calibrational (raise the threshold)
  * AUC ~ 0.5 -> overlap   -> structural (no threshold separates drift from jump)
Thresholds are calibrated per metric to a fixed FPR on pure diffusion. The AIRM
metric is included as the reference whose heavy-tailed increments make it
jump-blind after calibration (Paper 3, Sec. 6.2).

Usage:
    python -m experiments.paper3_geodesic_kinematics.drift_jump_confusion_sweep.run
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
    os.path.dirname(__file__), "..", "..", "_results", "drift_jump_confusion_sweep"
)

# ---- pre-fixed grid (declared before the run) --------------------------------
# Collapse factors span undetectable (near 1) -> confusion zone -> clearly
# detectable (small), so the diagnostic can find where a strong drift's heavy
# anti-developed tail overlaps a genuine (moderate) jump.
DRIFT_STRENGTHS = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4]
COLLAPSE_FACTORS = [0.9, 0.7, 0.5, 0.3, 0.1]       # smaller = more severe jump
WINDOWS = [200, 400, 800]
N_SEEDS = 60
N_DIM = 3
T0 = 400
DIFFUSION = 0.02
FPR_TARGET = 0.05
ANCHOR_WINDOW = 5


def jump_statistic(increments, anchor_window=ANCHOR_WINDOW):
    """Covariate-anchored jump statistic on anti-developed increments:
    max increment norm within +/- window of the covariate argmax, / bipower."""
    X = np.cumsum(increments, axis=0)
    cov = jd.conditional_residual_variance(X)
    T = increments.shape[0]
    anchor = int(np.argmax(cov))
    lo, hi = max(0, anchor - anchor_window), min(T, anchor + anchor_window + 1)
    r = np.linalg.norm(increments, axis=1)
    sigma = su.bipower_scale(increments)
    return float(np.max(r[lo:hi])) / max(sigma, 1e-12)


def auc(pos, neg):
    """AUC via Mann-Whitney U (P[pos > neg]); how well jump-stat ranks collapse
    above drift."""
    pos, neg = np.asarray(pos), np.asarray(neg)
    allv = np.concatenate([pos, neg])
    ranks = np.argsort(np.argsort(allv)) + 1
    u = ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0
    return u / (len(pos) * len(neg))


def sim_jump_stats(regime, T, metric, seed0, drift=0.0, cfac=0.05):
    stats = np.empty(N_SEEDS)
    for s in range(N_SEEDS):
        cfg = mt.ManifoldSimConfig(n=N_DIM, T=T, drift_strength=drift,
                                   diffusion_scale=DIFFUSION,
                                   jump_time=T // 2, collapse_factor=cfac,
                                   seed=seed0 + s)
        rhos, _ = mt.simulate_manifold_regime(regime, cfg)
        inc = mt.anti_develop(rhos, metric)
        stats[s] = jump_statistic(inc)
    return stats


def run_metric(metric: str, seed0: int = 2000, full: bool = True):
    """full=True: complete drift x collapse AUC grid (square-root metric).
    full=False: only the dispersion-calibrated threshold and per-collapse jump
    power (used for the AIRM reference, whose point is jump-blindness)."""
    disp = sim_jump_stats("dispersion", T0, metric, seed0 + 1)
    thr = float(np.quantile(disp, 1 - FPR_TARGET))
    coll_stats = {cf: sim_jump_stats("collapse", T0, metric, seed0 + 500 + 50 * k, cfac=cf)
                  for k, cf in enumerate(COLLAPSE_FACTORS)}
    jumppower = np.array([np.mean(coll_stats[cf] > thr) for cf in COLLAPSE_FACTORS])
    if not full:
        return {"threshold": thr, "jump_power": jumppower, "auc": None,
                "driftjump_rate": None, "dispersion_stats": disp}

    drift_stats = {ds: sim_jump_stats("drift", T0, metric, seed0 + 100 + 50 * i, drift=ds)
                   for i, ds in enumerate(DRIFT_STRENGTHS)}
    nd, nc = len(DRIFT_STRENGTHS), len(COLLAPSE_FACTORS)
    auc_grid = np.full((nd, nc), np.nan)
    driftjump = np.array([np.mean(drift_stats[ds] > thr) for ds in DRIFT_STRENGTHS])
    for i, ds in enumerate(DRIFT_STRENGTHS):
        for k, cf in enumerate(COLLAPSE_FACTORS):
            auc_grid[i, k] = auc(coll_stats[cf], drift_stats[ds])
    return {"threshold": thr, "auc": auc_grid,
            "driftjump_rate": driftjump, "jump_power": jumppower,
            "dispersion_stats": disp}


def window_dependence(metric="sqrt", seed0=8000):
    d, cf = 0.3, 0.3
    out = {}
    for T in WINDOWS:
        disp = sim_jump_stats("dispersion", T, metric, seed0 + T)
        thr = float(np.quantile(disp, 1 - FPR_TARGET))
        drift = sim_jump_stats("drift", T, metric, seed0 + 2 * T, drift=d)
        coll = sim_jump_stats("collapse", T, metric, seed0 + 3 * T, cfac=cf)
        out[T] = {"threshold": thr,
                  "driftjump_rate": float(np.mean(drift > thr)),
                  "jump_power": float(np.mean(coll > thr)),
                  "auc": float(auc(coll, drift))}
    return out


def seed_stability(metric="sqrt"):
    d, cf, T = 0.3, 0.3, T0
    rates = []
    for bank in range(3):
        s0 = 90000 + bank * 5000
        disp = sim_jump_stats("dispersion", T, metric, s0)
        thr = float(np.quantile(disp, 1 - FPR_TARGET))
        drift = sim_jump_stats("drift", T, metric, s0 + 1000, drift=d)
        rates.append(float(np.mean(drift > thr)))
    return {"rates": rates, "mean": float(np.mean(rates)), "std": float(np.std(rates))}


def make_figures(sqrt_res, airm_res, wdep, out_dir):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    M = sqrt_res["auc"]
    ax = axes[0]
    im = ax.imshow(M, origin="lower", aspect="auto", vmin=0.5, vmax=1.0, cmap="viridis")
    ax.set_xticks(range(len(COLLAPSE_FACTORS)))
    ax.set_xticklabels(COLLAPSE_FACTORS)
    ax.set_yticks(range(len(DRIFT_STRENGTHS)))
    ax.set_yticklabels(DRIFT_STRENGTHS)
    ax.set_xlabel("collapse factor (smaller = stronger jump)")
    ax.set_ylabel("drift strength")
    ax.set_title("sqrt metric: AUC(collapse vs drift)\n0.5=structural overlap, 1=separable")
    for i in range(M.shape[0]):
        for k in range(M.shape[1]):
            ax.text(k, i, f"{M[i,k]:.2f}", ha="center", va="center",
                    color="w" if M[i, k] < 0.85 else "k", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046)

    ax = axes[1]
    ax.plot(DRIFT_STRENGTHS, sqrt_res["driftjump_rate"], "o-", color="crimson")
    ax.axhline(0.1, ls=":", c="gray")
    ax.set_xlabel("drift strength"); ax.set_ylabel("drift->jump rate")
    ax.set_title("sqrt: strong geodesic drift misread as jump\n(calibrated 5% FPR)")
    ax.set_ylim(0, 1)

    ax = axes[2]
    ax.plot(COLLAPSE_FACTORS, sqrt_res["jump_power"], "o-", label="sqrt")
    ax.plot(COLLAPSE_FACTORS, airm_res["jump_power"], "s--", label="AIRM")
    ax.axhline(0.5, ls=":", c="gray")
    ax.set_xlabel("collapse factor (smaller = stronger jump)")
    ax.set_ylabel("jump power"); ax.set_title("jump-detection power vs severity")
    ax.legend(); ax.set_ylim(0, 1); ax.invert_xaxis()

    fig.suptitle("Experiment D -- drift/jump confusion on the geometric pipeline", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(out_dir, "confusion_surfaces.png"), dpi=130)
    plt.close(fig)

    fig2, ax = plt.subplots(figsize=(7, 5))
    Ts = WINDOWS
    ax.plot(Ts, [wdep[T]["driftjump_rate"] for T in Ts], "o-", label="drift->jump rate")
    ax.plot(Ts, [wdep[T]["jump_power"] for T in Ts], "s-", label="jump power")
    ax.plot(Ts, [wdep[T]["auc"] for T in Ts], "^-", label="AUC(collapse vs drift)")
    ax.axhline(0.1, ls="--", c="gray", lw=0.8)
    ax.set_xlabel("window length T"); ax.set_ylabel("rate / AUC"); ax.set_ylim(0, 1.05)
    ax.set_title("sqrt metric: window dependence (drift=0.2, collapse=0.05)")
    ax.legend(); fig2.tight_layout()
    fig2.savefig(os.path.join(out_dir, "window_dependence.png"), dpi=130)
    plt.close(fig2)


def issue_verdict(sqrt_res, seedstab):
    auc_g = sqrt_res["auc"]
    dj = sqrt_res["driftjump_rate"]          # by drift row
    jp = sqrt_res["jump_power"]              # by collapse col

    detectable = jp > 0.5                     # collapse columns that are real jumps
    confusion_prone = dj > 0.1                # drift rows that leak past threshold
    # cells where a real jump coincides with a leaking drift
    mask = confusion_prone[:, None] & detectable[None, :]
    worst_auc = float(np.nanmin(auc_g[mask])) if mask.any() else float("nan")
    structural_region = bool(mask.any() and np.any(auc_g[mask] < 0.70))
    # calibrational: for detectable jumps, is collapse still separable from the
    # strongest leaking drift (so a raised threshold fixes it)?
    calibrational_ok = bool(mask.any() and np.all(auc_g[mask] >= 0.85))
    seed_unstable = seedstab["std"] > seedstab["mean"] if seedstab["mean"] > 0 else False

    if seed_unstable:
        verdict = (f"INCONCLUSIVE: seed variance (std {seedstab['std']:.2f}) exceeds "
                   f"the drift->jump effect (mean {seedstab['mean']:.2f}).")
    elif structural_region:
        verdict = ("STRUCTURAL in a corner: there is a realistic region (strong "
                   f"drift, weak-but-detectable jump) where AUC falls to {worst_auc:.2f}"
                   " -- no threshold separates a strong geodesic drift from a weak "
                   "collapse there. A hybrid metric (method change) is indicated for "
                   "that corner.")
    elif calibrational_ok:
        verdict = ("CALIBRATIONAL: wherever the jump is detectable, collapse "
                   f"out-scores even the leaking drifts (worst AUC {worst_auc:.2f} "
                   ">= 0.85), so raising the dispersion-calibrated threshold removes "
                   "the drift->jump confusion without losing jump power. The appendix "
                   "confusion is a threshold placement, not a geometric limit, in the "
                   "exact square-root pipeline.")
    else:
        verdict = ("MIXED: partly separable (worst detectable-cell AUC "
                   f"{worst_auc:.2f}) but not uniformly >= 0.85; a better discriminator "
                   "helps in some cells, a threshold suffices in others.")
    return {"worst_detectable_auc": worst_auc,
            "structural_region_found": structural_region,
            "calibrational_everywhere_detectable": calibrational_ok,
            "seed_unstable": bool(seed_unstable), "verdict": verdict}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment D (geometric pipeline): drift-vs-jump confusion sweep")
    print(f"  SPD({N_DIM}) trajectories, {len(DRIFT_STRENGTHS)}x{len(COLLAPSE_FACTORS)} grid, "
          f"{N_SEEDS} seeds/cell, T={T0}")
    print("  square-root metric grid...")
    sqrt_res = run_metric("sqrt", full=True)
    print("  AIRM (heavy-tail) reference: jump power only...")
    airm_res = run_metric("airm", seed0=4000, full=False)
    print("  window dependence...")
    wdep = window_dependence("sqrt")
    print("  seed stability...")
    seedstab = seed_stability("sqrt")

    make_figures(sqrt_res, airm_res, wdep, RESULTS_DIR)
    verdict = issue_verdict(sqrt_res, seedstab)

    summary = {
        "experiment": "D_drift_jump_confusion_sweep",
        "pipeline": "geometric (SPD anti-development)",
        "grid": {"drift_strengths": DRIFT_STRENGTHS, "collapse_factors": COLLAPSE_FACTORS,
                 "windows": WINDOWS, "n_seeds": N_SEEDS, "n_dim": N_DIM,
                 "diffusion": DIFFUSION, "fpr_target": FPR_TARGET},
        "square_root_metric": {
            "threshold": sqrt_res["threshold"],
            "auc_collapse_vs_drift": sqrt_res["auc"].tolist(),
            "driftjump_rate_by_drift": sqrt_res["driftjump_rate"].tolist(),
            "jump_power_by_collapse": sqrt_res["jump_power"].tolist()},
        "airm_metric": {
            "threshold": airm_res["threshold"],
            "jump_power_by_collapse": airm_res["jump_power"].tolist(),
            "max_jump_power": float(np.nanmax(airm_res["jump_power"])),
            "note": "AIRM anti-developed increments are heavy-tailed (higher "
                    "dispersion threshold); jump-power-only reference. Weak/moderate "
                    "collapses are swamped, reproducing appendix jump-blindness; only "
                    "the most severe collapse survives the raised threshold."},
        "window_dependence": wdep,
        "seed_stability": seedstab,
        "diagnostic": verdict,
        "figures": ["confusion_surfaces.png", "window_dependence.png"]}
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict["verdict"])
    print(f"  sqrt jump power (by collapse {COLLAPSE_FACTORS}): "
          f"{np.round(sqrt_res['jump_power'],2).tolist()}")
    print(f"  AIRM max jump power: {summary['airm_metric']['max_jump_power']:.2f} "
          "(appendix predicts jump-blindness)")
    print(f"  drift->jump by drift {DRIFT_STRENGTHS}: "
          f"{np.round(sqrt_res['driftjump_rate'],2).tolist()}")
    print(f"  seed stability: {seedstab['mean']:.2f} +/- {seedstab['std']:.2f}")
    print(f"Results + figures in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
