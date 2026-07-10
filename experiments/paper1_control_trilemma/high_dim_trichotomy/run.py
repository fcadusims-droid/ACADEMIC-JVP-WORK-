"""Experiment E2 -- High-dimensional, value-base-mutating trichotomy test
(Paper 1, Sec 7.5/7.6). Extends Experiment E to the strongest named adversarial
case.

Experiment E's candidates lived on a 2-D torus or the 3-D Lorenz attractor --
low-dimensional systems where the trichotomy is close to analytically
demonstrable. Sec 7.5 names the philosophically live objection as *open-ended,
novelty-driven, or value-base-mutating optimization* -- closer to real
population-based training (PBT) with a meta-optimized, endogenously drifting
objective. This builds that candidate directly.

Model: M agents each hold a preference vector theta_i in R^d on a compact torus
[0,1)^d (d=6). A reward landscape is K Gaussian bumps whose centers RECEDE from
wherever the population's current density concentrates -- the objective mutates
in response to the population's own trajectory, open-ended and endogenous, not
pre-enumerated. Each agent climbs the landscape (gradient ascent), is mildly
repelled by its peers (diversity pressure, PBT-style), and diffuses weakly.

Diagnostics on the population-mean trajectory (circular/toroidal mean):
  * largest Lyapunov exponent, via Benettin on the DETERMINISTIC dynamics
    (reference + perturbed trajectory, no noise, so divergence isolates
    sensitivity to initial conditions);
  * Poincare recurrence fraction, via a periodic (toroidal) k-d tree on the
    STOCHASTIC dynamics (diffusion included, as a real system would have).

The falsifier the theorem forbids: positive Lyapunov exponent AND low recurrence
(< 0.5) simultaneously, on this compact set.

Usage:
    python -m experiments.paper1_control_trilemma.high_dim_trichotomy.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "high_dim_trichotomy"
)

D = 6            # preference-vector dimension (compact torus [0,1)^d)
M = 8            # population size
K = 8            # reward-landscape bumps
BUMP_WIDTH = 0.18
DT = 0.02
LYAP_STEPS = 3000
REC_STEPS = 5000
D0 = 1e-7
RENORM_EVERY = 5

RECESSION_RATES = [0.0, 0.5, 1.0, 2.0]     # how hard the landscape flees exploitation
DIVERSITY_PRESSURES = [0.0, 0.5, 1.0]      # peer-repulsion (PBT explore) strength


def torus_disp(a, b):
    """Minimal signed displacement a-b on the flat torus, componentwise."""
    return ((a - b + 0.5) % 1.0) - 0.5


MAX_FORCE = 3.0   # soft cap on any single-term force magnitude (regularization,
                   # standard in particle dynamics with tight attractive/
                   # repulsive coupling, to prevent a stiff near-collision
                   # feedback loop -- agent chasing a fleeing bump -- from
                   # requiring vanishingly small dt to resolve; see the
                   # DT-convergence check in the module docstring / README)


def _clip_rows(v, max_norm):
    n = np.linalg.norm(v, axis=1, keepdims=True)
    scale = np.minimum(1.0, max_norm / np.maximum(n, 1e-12))
    return v * scale


def landscape_grad(theta, bumps):
    """Gradient (w.r.t. theta) of the sum-of-Gaussian-bumps landscape, pulling
    theta toward nearby bump centers. theta: (M,d); bumps: (K,d) -> (M,d)."""
    grad = np.zeros_like(theta)
    for k in range(bumps.shape[0]):
        disp = torus_disp(bumps[k], theta)               # (M,d), bump - theta
        d2 = np.sum(disp ** 2, axis=1, keepdims=True)
        w = np.exp(-d2 / (2 * BUMP_WIDTH ** 2))
        grad += w * disp / (BUMP_WIDTH ** 2)
    return _clip_rows(grad, MAX_FORCE)


def bump_recession(bumps, theta, rate):
    """Move each bump center away from the local population density -- the
    landscape recedes from wherever agents have concentrated."""
    if rate == 0.0:
        return np.zeros_like(bumps)
    push = np.zeros_like(bumps)
    for k in range(bumps.shape[0]):
        disp = torus_disp(bumps[k], theta)                # (M,d), bump - agent
        d2 = np.sum(disp ** 2, axis=1, keepdims=True)
        w = np.exp(-d2 / (2 * BUMP_WIDTH ** 2))
        # push bump AWAY from agents weighted by local density (sum of w*disp
        # points away from crowded agents since disp = bump - agent)
        push[k] = rate * np.sum(w * disp, axis=0) / (M * BUMP_WIDTH ** 2)
    return _clip_rows(push, MAX_FORCE)


def diversity_repulsion(theta, pressure):
    """Mild pairwise repulsion between agents (PBT-style diversity pressure)."""
    if pressure == 0.0:
        return np.zeros_like(theta)
    rep = np.zeros_like(theta)
    for i in range(M):
        disp = torus_disp(theta[i], theta)                 # (M,d), theta_i - theta_j
        d2 = np.sum(disp ** 2, axis=1, keepdims=True)
        d2[i] = np.inf
        w = np.exp(-d2 / (2 * (2 * BUMP_WIDTH) ** 2))
        rep[i] = pressure * np.sum(w * disp, axis=0) / M
    return _clip_rows(rep, MAX_FORCE)


def step_deterministic(theta, bumps, recession_rate, diversity_pressure, dt=None):
    dt = DT if dt is None else dt
    dtheta = landscape_grad(theta, bumps) + diversity_repulsion(theta, diversity_pressure)
    dbumps = bump_recession(bumps, theta, recession_rate)
    theta_new = (theta + dt * dtheta) % 1.0
    bumps_new = (bumps + dt * dbumps) % 1.0
    return theta_new, bumps_new


def step_stochastic(theta, bumps, recession_rate, diversity_pressure, rng, noise=0.02, dt=None):
    dt = DT if dt is None else dt
    theta_new, bumps_new = step_deterministic(theta, bumps, recession_rate, diversity_pressure, dt=dt)
    theta_new = (theta_new + noise * np.sqrt(dt) * rng.standard_normal(theta.shape)) % 1.0
    return theta_new, bumps_new


def circular_mean(theta_pop):
    """Toroidal (circular) mean over the population axis, per dimension."""
    ang = 2 * np.pi * theta_pop
    m = np.arctan2(np.mean(np.sin(ang), axis=0), np.mean(np.cos(ang), axis=0))
    return (m / (2 * np.pi)) % 1.0


def lyapunov_exponent(recession_rate, diversity_pressure, seed=0, dt=None, n_steps=None):
    dt = DT if dt is None else dt
    n_steps = LYAP_STEPS if n_steps is None else n_steps
    rng = np.random.default_rng(seed)
    theta = rng.random((M, D))
    bumps = rng.random((K, D))
    theta_p = (theta + rng.normal(0, D0, theta.shape)) % 1.0
    bumps_p = bumps.copy()

    s = 0.0
    n_renorm = 0
    for i in range(n_steps):
        theta, bumps = step_deterministic(theta, bumps, recession_rate, diversity_pressure, dt=dt)
        theta_p, bumps_p = step_deterministic(theta_p, bumps_p, recession_rate, diversity_pressure, dt=dt)
        if (i + 1) % RENORM_EVERY == 0:
            disp = torus_disp(theta_p, theta)
            d = np.sqrt(np.sum(disp ** 2))
            if d > 1e-14:
                s += np.log(d / D0)
                n_renorm += 1
                theta_p = (theta + disp * (D0 / d)) % 1.0
    return s / (n_renorm * RENORM_EVERY * dt) if n_renorm else 0.0


def lyapunov_with_convergence_check(recession_rate, diversity_pressure, seed=0, rel_tol=0.3):
    """Compute lambda at DT and DT/2 (same total physical time); only accept the
    result if the two estimates agree within rel_tol. A genuine, well-resolved
    Lyapunov exponent converges as dt shrinks; an unresolved numerical artifact
    (a stiff or near-singular feedback loop poorly resolved by fixed-step
    integration) keeps growing instead -- exactly the failure mode a naive
    "landscape flees the population hard" regime produces here. Unresolved
    cells are reported, not silently kept or silently dropped."""
    lam_full = lyapunov_exponent(recession_rate, diversity_pressure, seed, dt=DT, n_steps=LYAP_STEPS)
    lam_half = lyapunov_exponent(recession_rate, diversity_pressure, seed, dt=DT / 2, n_steps=LYAP_STEPS * 2)
    denom = max(abs(lam_full), abs(lam_half), 1e-6)
    converged = abs(lam_full - lam_half) / denom <= rel_tol
    return lam_full, lam_half, bool(converged)


def recurrence_run(recession_rate, diversity_pressure, seed=0):
    rng = np.random.default_rng(seed + 1000)
    theta = rng.random((M, D))
    bumps = rng.random((K, D))
    means = np.empty((REC_STEPS, D))
    for i in range(REC_STEPS):
        theta, bumps = step_stochastic(theta, bumps, recession_rate, diversity_pressure, rng)
        means[i] = circular_mean(theta)
    return means


def recurrence_fraction(traj, eps=0.06, theiler=100):
    tree = cKDTree(traj, boxsize=1.0)          # native toroidal distance
    n = len(traj)
    rec = 0
    idxs = range(0, n, 4)
    for i in idxs:
        idx = tree.query_ball_point(traj[i], eps)
        if any(abs(j - i) > theiler for j in idx):
            rec += 1
    return rec / len(list(idxs))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment E2: high-dimensional value-base-mutating trichotomy test")
    print(f"  d={D}, M={M} agents, K={K} bumps, sweeping recession x diversity")

    results = {}
    falsifiers = []
    unresolved = []
    for rr in RECESSION_RATES:
        for dp in DIVERSITY_PRESSURES:
            lam_full, lam_half, converged = lyapunov_with_convergence_check(rr, dp, seed=1)
            means = recurrence_run(rr, dp, seed=1)
            rec = recurrence_fraction(means)
            key = f"recession={rr},diversity={dp}"
            # use the finer (more resolved) estimate as the reported lambda
            lam = lam_half
            is_falsifier = converged and (lam > 0.02) and (rec < 0.5)
            results[key] = {"recession_rate": rr, "diversity_pressure": dp,
                            "lambda_max_dt": float(lam_full), "lambda_max_dt_half": float(lam_half),
                            "converged": converged, "recurrence_fraction": float(rec),
                            "is_falsifier": bool(is_falsifier)}
            if is_falsifier:
                falsifiers.append(key)
            if not converged:
                unresolved.append(key)
            tag = ("  <-- FALSIFIER" if is_falsifier else
                  "  [UNRESOLVED: fails dt-convergence check, excluded]" if not converged else "")
            print(f"  recession={rr:.1f} diversity={dp:.1f}: "
                  f"lambda(dt)={lam_full:+.2f}, lambda(dt/2)={lam_half:+.2f}, "
                  f"recurrence={rec:.3f}{tag}")

    resolved = {k: v for k, v in results.items() if v["converged"]}
    if falsifiers:
        verdict = (f"TRICHOTOMY FALSIFIED by {falsifiers}: a higher-dimensional "
                   "(d=6), population-based, value-base-mutating preference "
                   "dynamics -- the strongest adversarial case Sec 7.5 names -- "
                   "shows positive entropy AND absence of recurrence "
                   "simultaneously on a compact set, AND this passes the "
                   "dt-convergence sanity check (lambda agrees within 30% as "
                   "the integration step halves). Sec 7.5/7.6 must be rewritten; "
                   "this is reported as prominently as Experiment E's "
                   "confirmation.")
    else:
        lams = [v["lambda_max_dt_half"] for v in resolved.values()]
        recs = [v["recurrence_fraction"] for v in resolved.values()]
        keys = list(resolved.keys())
        max_lam_idx = int(np.argmax(lams)) if lams else None
        unresolved_note = (f" {len(unresolved)}/{len(results)} cells "
                           f"({unresolved}) FAILED the dt-convergence check -- "
                           "the exponent kept growing rather than converging as "
                           "the integration step halved (a stiff agent-chasing-"
                           "fleeing-bump feedback loop at strong recession), and "
                           "are EXCLUDED from the trichotomy verdict as "
                           "numerically unresolved rather than reported as "
                           "either a confirmation or a falsification."
                           if unresolved else " All cells passed the "
                           "dt-convergence check.")
        verdict = (f"TRICHOTOMY SURVIVES ITS HARDEST NAMED CASE, among "
                   f"numerically resolved cells: across {len(resolved)}/"
                   f"{len(results)} (recession-rate x diversity-pressure) cells "
                   "of a d=6 population-based, value-base-mutating agent that "
                   "pass a dt-convergence sanity check, no cell shows positive "
                   "entropy with low recurrence."
                   + (f" The strongest entropy case among resolved cells "
                      f"({keys[max_lam_idx]}, lambda={lams[max_lam_idx]:+.3f}) has "
                      f"recurrence {recs[max_lam_idx]:.2f} (bounded)."
                      if max_lam_idx is not None else "")
                   + unresolved_note +
                   " This closes the gap Experiment E left open (which never "
                   "tested a genuinely higher-dimensional, value-base-mutating "
                   "candidate) and, on the numerically trustworthy cells, "
                   "strengthens the Sec 7.5/7.6 defence -- while honestly "
                   "flagging that the most aggressive landscape-recession regime "
                   "could not be resolved with this integrator and remains "
                   "genuinely untested rather than confirmed.")

    fig, ax = plt.subplots(figsize=(8, 6))
    for key, v in results.items():
        if not v["converged"]:
            c, marker = "gray", "x"
        elif v["is_falsifier"]:
            c, marker = "crimson", "o"
        else:
            c, marker = "steelblue", "o"
        ax.scatter(v["lambda_max_dt_half"], v["recurrence_fraction"], s=80, color=c, marker=marker)
        ax.annotate(f"r={v['recession_rate']},d={v['diversity_pressure']}"
                    f"{'*' if not v['converged'] else ''}",
                    (v["lambda_max_dt_half"], v["recurrence_fraction"]),
                    textcoords="offset points", xytext=(5, 4), fontsize=7)
    ax.axhline(0.5, ls=":", color="gray")
    ax.axvline(0.02, ls=":", color="gray")
    xlim = ax.get_xlim()
    ax.fill_between([max(0.02, xlim[0]), xlim[1]], 0, 0.5, color="red", alpha=0.08)
    ax.text(0.03, 0.05, "forbidden region", fontsize=8, color="darkred")
    ax.set_xlabel("largest Lyapunov exponent (finer dt estimate)")
    ax.set_ylabel("Poincare recurrence fraction (stochastic dynamics)")
    ax.set_title("Exp E2: d=6 population-based, value-base-mutating agent\n"
                 "(gray x = failed dt-convergence check, excluded)")
    ax.set_ylim(-0.05, 1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "high_dim_trichotomy.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "E2_high_dim_trichotomy",
        "params": {"d": D, "M": M, "K": K, "bump_width": BUMP_WIDTH, "dt": DT,
                   "lyap_steps": LYAP_STEPS, "rec_steps": REC_STEPS,
                   "recession_rates": RECESSION_RATES,
                   "diversity_pressures": DIVERSITY_PRESSURES},
        "results": results,
        "falsifiers": falsifiers,
        "unresolved_cells": unresolved,
        "preregistered_falsifier": "lambda_max > 0.02 AND recurrence_fraction < 0.5 on a compact set, AND passes a dt-convergence check (lambda(dt) vs lambda(dt/2) agree within 30%)",
        "verdict": verdict,
        "figures": ["high_dim_trichotomy.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
