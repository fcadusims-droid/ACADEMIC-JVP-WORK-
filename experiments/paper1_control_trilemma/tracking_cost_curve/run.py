"""Experiment F -- Cost curve of the exogenous (coercion) horn (Paper 1, Sec 7.3).

Sec 7.3 (as edited) claims finite-gain trajectory-tracking control pays a GRADED,
MONOTONE agency cost: as tracking gain k rises, the agency diffusion D_ag -> 0 and
the parallel agency eigenvalue lambda_parallel -> -infinity, with the
perfect-tracking limit recovering the annihilation claim. This checks whether the
curve is actually monotone and graded.

Agent: a double-well explorer -- intrinsic dynamics dx = (x - x^3) dt + sigma dW,
whose "agency" is spontaneous hopping between the wells at x = +/-1. Tracking
control to the reference x_ref = 0 with proportional gain k gives
dx = ((1-k) x - x^3) dt + sigma dW. This deliberately has a bifurcation at k = 1
(the origin turns stable), which is the sharpest test of "graded": a coercion cost
with a bifurcation is monotone but not smooth.

Measured per gain:
  * lambda_parallel -- the local closed-loop eigenvalue at the operating point,
    estimated from the relaxation (autocorrelation) time of the tracked coordinate;
  * D_ag -- the residual agency diffusion, estimated as the stationary variance of
    the state around the reference (how much exploration survives).

Usage:
    python -m experiments.paper1_control_trilemma.tracking_cost_curve.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "tracking_cost_curve"
)

GAINS = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0]
SIGMA = 0.5
DT = 0.01
T_STEPS = 200_000
BURN = 20_000
N_SEEDS = 6


def simulate(gain, sigma, seed):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal()
    xs = np.empty(T_STEPS)
    sqdt = np.sqrt(DT)
    for t in range(T_STEPS):
        drift = (1.0 - gain) * x - x ** 3
        x = x + drift * DT + sigma * sqdt * rng.standard_normal()
        xs[t] = x
    return xs[BURN:]


def relaxation_lambda(xs, dt):
    """Estimate the dominant relaxation rate from the autocorrelation time of the
    tracked coordinate: acf ~ exp(t/tau) with tau the integrated autocorr time,
    so lambda_parallel = -1/tau. Robust to the nonlinearity."""
    x = xs - xs.mean()
    var = np.dot(x, x) / len(x)
    if var < 1e-12:
        return -np.inf
    # integrated autocorrelation time via the sum of positive-lag acf
    maxlag = 2000
    acf = np.array([np.dot(x[:-k], x[k:]) / (len(x) - k) for k in range(1, maxlag)]) / var
    # cut at first non-positive value
    stop = np.argmax(acf <= 0) if np.any(acf <= 0) else len(acf)
    tau = (0.5 + np.sum(acf[:stop])) * dt
    return -1.0 / max(tau, 1e-9)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment F: tracking cost curve (double-well agent under coercive gain)")
    D_ag, lam = [], []
    for k in GAINS:
        vs, ls = [], []
        for s in range(N_SEEDS):
            xs = simulate(k, SIGMA, seed=s)
            vs.append(np.var(xs))
            ls.append(relaxation_lambda(xs, DT))
        D_ag.append(np.mean(vs))
        lam.append(np.mean(ls))
        print(f"  gain={k:5.2f}: D_ag(var)={D_ag[-1]:.4f}, lambda_parallel={lam[-1]:.3f}")

    D_ag = np.array(D_ag)
    lam = np.array(lam)
    gains = np.array(GAINS)

    # monotonicity checks (allowing tiny numerical noise)
    d_ag_monotone = bool(np.all(np.diff(D_ag) <= 1e-3))
    lam_monotone = bool(np.all(np.diff(lam) <= 1e-2))
    # "graded" = no local jump much larger than its neighbours (a bifurcation
    # would show a step near k=1 that dwarfs the smooth decay elsewhere). Compare
    # the drop straddling k=1 to the median drop.
    steps = -np.diff(D_ag)
    near1 = steps[max(0, np.searchsorted(gains, 1.0) - 1)]
    graded = bool(near1 < 3 * np.median(steps[steps > 0]))

    if d_ag_monotone and lam_monotone and graded:
        verdict = (f"CLAIM CONFIRMED: both curves are monotone and graded. D_ag falls "
                   f"smoothly {D_ag[0]:.2f} -> {D_ag[-1]:.4f} (approaching the "
                   f"annihilation limit D_ag -> 0) and lambda_parallel drops "
                   f"{lam[0]:.2f} -> {lam[-1]:.1f} toward -infinity as gain rises. The "
                   "double-well bifurcation at k=1 is washed out by the exploratory "
                   "noise, so the agency cost is genuinely graded -- no discontinuity, "
                   "no non-monotonicity. Sec 7.3's 'graded, monotone' finite-gain "
                   "cost is numerically vindicated.")
    elif d_ag_monotone and lam_monotone:
        verdict = (f"CLAIM HOLDS, near-critical: both curves monotone (D_ag "
                   f"{D_ag[0]:.2f} -> {D_ag[-1]:.4f}, lambda {lam[0]:.2f} -> "
                   f"{lam[-1]:.1f}) but the drop concentrates at the k=1 bifurcation "
                   "-- monotone but not uniformly smooth. 'Graded' should be read as "
                   "monotone-through-a-bifurcation.")
    elif not lam_monotone:
        verdict = (f"DEFECT: lambda_parallel is NOT monotone in gain "
                   f"(max increase {np.max(np.diff(lam)):.3f}); Sec 7.3's monotone "
                   "cost claim fails for this agent and must be corrected.")
    else:
        verdict = (f"PARTIAL: lambda_parallel is monotone but D_ag is not "
                   f"(max increase {np.max(np.diff(D_ag)):.3f}); the residual-agency "
                   "cost is non-monotone, contradicting the graded-cost claim.")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    ax.plot(gains, D_ag, "o-", color="crimson")
    ax.axvline(1.0, ls=":", color="gray"); ax.text(1.02, D_ag.max() * 0.8, "bifurcation k=1", fontsize=8)
    ax.set_xlabel("tracking gain k"); ax.set_ylabel("D_ag  (stationary variance)")
    ax.set_title("Residual agency diffusion vs gain"); ax.set_yscale("log")
    ax = axes[1]
    ax.plot(gains, lam, "s-", color="steelblue")
    ax.axhline(0, ls=":", color="gray"); ax.axvline(1.0, ls=":", color="gray")
    ax.set_xlabel("tracking gain k"); ax.set_ylabel("lambda_parallel (relaxation rate)")
    ax.set_title("Parallel agency eigenvalue vs gain")
    fig.suptitle("Exp F: exogenous-horn cost curve (double-well agent)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "cost_curve.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "F_tracking_cost_curve",
        "agent": "double-well explorer dx=(x-x^3)dt+sigma dW, tracked to x_ref=0",
        "params": {"gains": GAINS, "sigma": SIGMA, "dt": DT, "T_steps": T_STEPS,
                   "n_seeds": N_SEEDS},
        "D_ag_by_gain": D_ag.tolist(),
        "lambda_parallel_by_gain": lam.tolist(),
        "D_ag_monotone": d_ag_monotone,
        "lambda_monotone": lam_monotone,
        "graded_no_bifurcation_step": graded,
        "preregistered_criterion": "both curves monotone and graded (D_ag->0, lambda->-inf)",
        "verdict": verdict,
        "figures": ["cost_curve.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
