"""Experiment G -- Poincaré recurrence fraction of the Lorenz attractor.

Verifies the "recurrence fraction ~ 1" claim Paper 1 makes in support of the
Case-3 (bounded recurrence) horn of the Meta-Optimization trichotomy but never
shows computed. See PRE-REGISTRATION.md for the success/failure criteria.

Usage:
    python -m experiments.paper1_control_trilemma.poincare_recurrence_check.run
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy.integrate import solve_ivp
from scipy.spatial import cKDTree

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "poincare_recurrence_check"
)


def lorenz(t, s, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    x, y, z = s
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def integrate_lorenz(t_max=200.0, dt=0.01, transient=20.0, seed=0):
    """Integrate onto the attractor and drop the transient."""
    rng = np.random.default_rng(seed)
    s0 = rng.standard_normal(3) * 5 + np.array([1.0, 1.0, 20.0])
    t_eval = np.arange(0, t_max, dt)
    sol = solve_ivp(lorenz, (0, t_max), s0, t_eval=t_eval,
                    rtol=1e-9, atol=1e-9, method="RK45")
    traj = sol.y.T
    keep = sol.t >= transient
    return traj[keep]


def recurrence_fraction(traj, eps, min_gap_steps):
    """Fraction of points that have >=1 recurrence within eps, excluding a
    temporal Theiler window of `min_gap_steps` around each point (so that
    trivially-close temporal neighbours do not count as recurrences)."""
    tree = cKDTree(traj)
    n = len(traj)
    recurs = 0
    for i in range(n):
        idx = tree.query_ball_point(traj[i], eps)
        # exclude self and the Theiler window
        far = [j for j in idx if abs(j - i) > min_gap_steps]
        if far:
            recurs += 1
    return recurs / n


def characteristic_scale(traj):
    """A defensible epsilon band: fractions of the attractor's RMS extent."""
    span = np.sqrt(np.mean(np.sum((traj - traj.mean(0)) ** 2, axis=1)))
    return span


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Integrating Lorenz attractor...")
    traj = integrate_lorenz(t_max=200.0, dt=0.01, transient=20.0, seed=0)
    print(f"  {len(traj)} points on the attractor after transient")

    span = characteristic_scale(traj)
    dt = 0.01
    theiler = int(1.0 / dt)  # 1 time unit Theiler window

    eps_fracs = [0.01, 0.02, 0.05, 0.1, 0.15, 0.2]
    results = []
    for f in eps_fracs:
        eps = f * span
        frac = recurrence_fraction(traj, eps, theiler)
        results.append({"eps_frac_of_span": f, "eps": float(eps),
                        "recurrence_fraction": float(frac)})
        print(f"  eps = {f:.2f} * span ({eps:6.2f}):  recurrence fraction = {frac:.4f}")

    # pre-registered criterion: >= 0.95 over a defensible eps band
    band = [r for r in results if r["eps_frac_of_span"] >= 0.05]
    passing = [r for r in band if r["recurrence_fraction"] >= 0.95]
    verdict_pass = len(passing) >= 1
    smallest_pass = min((r["eps_frac_of_span"] for r in passing), default=None)

    summary = {
        "experiment": "G_poincare_recurrence",
        "attractor": "Lorenz (sigma=10, rho=28, beta=8/3)",
        "n_points": len(traj),
        "attractor_rms_span": float(span),
        "theiler_window_steps": theiler,
        "sweep": results,
        "preregistered_criterion": "recurrence fraction >= 0.95 over eps >= 0.05*span",
        "verdict": ("CONFIRMED: text's 'recurrence fraction ~ 1' holds"
                    if verdict_pass else
                    "NOT CONFIRMED: fraction below 0.95; text must state eps regime"),
        "smallest_eps_frac_meeting_0.95": smallest_pass,
    }
    out_path = os.path.join(RESULTS_DIR, "result.json")
    with open(out_path, "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 60)
    print(summary["verdict"])
    print(f"  (recurrence >= 0.95 first reached at eps = "
          f"{smallest_pass} * span)" if smallest_pass else "")
    print(f"Results written to {os.path.relpath(out_path)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
