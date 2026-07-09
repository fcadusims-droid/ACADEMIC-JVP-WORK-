"""Experiment E -- Trichotomy test with endogenous-preference dynamics (Paper 1).

The Meta-Optimization Collapse Theorem (Sec 7.5/7.6) claims an autonomous
preference dynamics theta_dot = f(theta) on a COMPACT value space falls into a
trichotomy: Case 1 gradient descent on a meta-potential (converges), Case 2
unbounded dispersion (escapes -- impossible on a compact set), Case 3 bounded
recurrence (conservative circulation). The falsifying object the theorem forbids
is a compact-set dynamics with POSITIVE ENTROPY on its attractor AND ABSENCE OF
RECURRENCE simultaneously -- sustained novelty that never returns.

Rather than train noisy RL, the candidate preference dynamics are implemented
directly as flows on a compact space and classified with three measured
quantities:
  * largest Lyapunov exponent lambda_max (Benettin)  -- entropy proxy;
  * Poincare recurrence fraction R                    -- does it return?
  * Helmholtz-Hodge gradient/rotational energy split  -- Case 1 vs Case 3.

The decisive adversarial candidates named in the text are pure novelty search and
intrinsic curiosity (plus deterministic chaos as the strongest positive-entropy
case). The theorem predicts every compact-set candidate is recurrent -- even the
chaotic and novelty-seeking ones -- so no falsifier exists.

Usage:
    python -m experiments.paper1_control_trilemma.rl_agents_trichotomy.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

from experiments.shared_lib import helmholtz_hodge as hh

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "rl_agents_trichotomy"
)

TWO_PI = 2 * np.pi


# ---- candidate preference dynamics on the torus [0,1)^2 (compact) ------------
def f_gradient(p):
    """Case 1 expected: gradient descent on a meta-potential V = -cos-cos."""
    x, y = p
    return np.array([-TWO_PI * np.sin(TWO_PI * x), -TWO_PI * np.sin(TWO_PI * y)])


def f_hamiltonian(p):
    """Case 3 expected: conservative circulation theta_dot = J grad H."""
    x, y = p
    dHdx = TWO_PI * np.sin(TWO_PI * x)
    dHdy = TWO_PI * np.sin(TWO_PI * y)
    return np.array([dHdy, -dHdx])


def f_curiosity(p, t):
    """Intrinsic curiosity: gradient ascent on a slowly drifting reward landscape
    (a non-autonomous meta-objective). Bounded to the torus."""
    x, y = p
    phase = 0.3 * t
    return np.array([TWO_PI * np.sin(TWO_PI * (x - 0.1 * np.cos(phase))),
                     TWO_PI * np.sin(TWO_PI * (y - 0.1 * np.sin(phase)))]) * 0.5


def integrate_torus(f, p0, dt=0.01, n=40000, non_autonomous=False):
    """RK4 on the torus (wrap to [0,1)); returns the trajectory."""
    p = np.array(p0, float)
    traj = np.empty((n, 2))
    for i in range(n):
        t = i * dt
        if non_autonomous:
            k1 = f(p, t); k2 = f(p + 0.5 * dt * k1, t + 0.5 * dt)
            k3 = f(p + 0.5 * dt * k2, t + 0.5 * dt); k4 = f(p + dt * k3, t + dt)
        else:
            k1 = f(p); k2 = f(p + 0.5 * dt * k1)
            k3 = f(p + 0.5 * dt * k2); k4 = f(p + dt * k3)
        p = (p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)) % 1.0
        traj[i] = p
    return traj


def novelty_search(p0, dt=0.01, n=40000, sigma=0.06, archive_stride=15):
    """Pure novelty search on the torus: velocity = repulsion from the density of
    an archive of previously visited points. The strongest adversarial candidate
    -- does it sustain novelty without returning on a compact space?"""
    p = np.array(p0, float)
    traj = np.empty((n, 2))
    archive = [p.copy()]
    for i in range(n):
        arch = np.array(archive)
        d = (p - arch + 0.5) % 1.0 - 0.5          # torus displacement to archive
        dist2 = np.sum(d ** 2, axis=1)
        w = np.exp(-dist2 / (2 * sigma ** 2))     # kernel density weights
        force = np.sum(w[:, None] * d, axis=0)    # repel away from dense regions
        nf = np.linalg.norm(force)
        if nf > 1e-9:
            force = force / nf
        p = (p + dt * force) % 1.0
        traj[i] = p
        if i % archive_stride == 0:
            archive.append(p.copy())
    return traj


def lorenz_traj(dt=0.01, n=40000, seed=0):
    """Deterministic chaos on a compact attractor: positive entropy, recurrent."""
    from scipy.integrate import solve_ivp
    rng = np.random.default_rng(seed)
    s0 = rng.standard_normal(3) * 5 + np.array([1, 1, 20.0])

    def lor(t, s):
        x, y, z = s
        return [10 * (y - x), x * (28 - z) - y, x * y - 8 / 3 * z]
    t_eval = np.arange(0, n * dt, dt)
    sol = solve_ivp(lor, (0, n * dt), s0, t_eval=t_eval, rtol=1e-9, atol=1e-9)
    return sol.y.T[2000:]


# ---- diagnostics -------------------------------------------------------------
def recurrence_fraction(traj, eps_frac=0.05, theiler=100):
    span = np.sqrt(np.mean(np.sum((traj - traj.mean(0)) ** 2, axis=1)))
    eps = eps_frac * span
    tree = cKDTree(traj)
    n = len(traj)
    rec = 0
    for i in range(0, n, 3):   # subsample for speed
        idx = tree.query_ball_point(traj[i], eps)
        if any(abs(j - i) > theiler for j in idx):
            rec += 1
    return rec / len(range(0, n, 3))


def _rk4_auto(f, p, dt):
    k1 = f(p); k2 = f(p + 0.5 * dt * k1)
    k3 = f(p + 0.5 * dt * k2); k4 = f(p + dt * k3)
    return p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def lyapunov_torus(f, p0, dt=0.005, n=20000, d0=1e-8):
    """Benettin largest Lyapunov exponent on the torus (RK4). Note: by
    Poincare-Bendixson a 2D autonomous flow cannot be chaotic, so this is <= 0
    for the smooth fields here; it is measured, not assumed."""
    p = np.array(p0, float)
    q = p + np.array([d0, 0.0])
    s = 0.0
    for _ in range(n):
        p = _rk4_auto(f, p, dt) % 1.0
        q = _rk4_auto(f, q, dt) % 1.0
        dv = (q - p + 0.5) % 1.0 - 0.5
        d = np.linalg.norm(dv)
        if d > 1e-14:
            s += np.log(d / d0)
            q = p + dv * (d0 / d)
    return s / (n * dt)


def lyapunov_lorenz(dt=0.005, n=20000, d0=1e-9):
    def lor(s):
        x, y, z = s
        return np.array([10 * (y - x), x * (28 - z) - y, x * y - 8 / 3 * z])
    rng = np.random.default_rng(1)
    p = rng.standard_normal(3) * 5 + np.array([1, 1, 20.0])
    for _ in range(2000):
        p = p + dt * lor(p)
    q = p + np.array([d0, 0, 0])
    s = 0.0
    for _ in range(n):
        p = p + dt * lor(p); q = q + dt * lor(q)
        dv = q - p; d = np.linalg.norm(dv)
        if d > 1e-14:
            s += np.log(d / d0); q = p + dv * (d0 / d)
    return s / (n * dt)


def hodge_fractions_of_field(f, res=48):
    xs = (np.arange(res) + 0.5) / res
    U = np.zeros((res, res)); V = np.zeros((res, res))
    for iy, y in enumerate(xs):
        for ix, x in enumerate(xs):
            v = f(np.array([x, y]))
            U[iy, ix] = v[0]; V[iy, ix] = v[1]
    return hh.hodge_energy_fractions(U, V)


def classify(lam, rec):
    if lam < -0.05:
        return "Case 1 (convergent / gradient)"
    if lam > 0.05 and rec < 0.5:
        return "FALSIFIER (positive entropy, no recurrence)"
    if lam > 0.05:
        return "Case 3* (positive entropy, RECURRENT -- chaotic but returns)"
    return "Case 3 (bounded recurrence / conservative)"


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment E: trichotomy test of endogenous-preference dynamics")
    results = {}

    # 2D torus candidates. `field` is an autonomous snapshot used for the
    # Lyapunov and Hodge diagnostics (curiosity's drifting reward is frozen at
    # t=0 for these); the trajectory uses the full (possibly non-autonomous) flow.
    curiosity_snapshot = lambda p: f_curiosity(p, 0.0)
    specs = [
        ("gradient", lambda: integrate_torus(f_gradient, [0.45, 0.55]), f_gradient),
        ("hamiltonian", lambda: integrate_torus(f_hamiltonian, [0.45, 0.55]), f_hamiltonian),
        ("curiosity", lambda: integrate_torus(f_curiosity, [0.45, 0.55], non_autonomous=True), curiosity_snapshot),
        ("novelty_search", lambda: novelty_search([0.45, 0.55]), None),
    ]
    for name, traj_fn, field in specs:
        traj = traj_fn()
        rec = recurrence_fraction(traj)
        if name == "novelty_search":
            lam = np.nan  # memory-dependent (non-Markov); recurrence is the test
        else:
            lam = lyapunov_torus(field, [0.45, 0.55])
        hodge = hodge_fractions_of_field(field) if field is not None else None
        klass = ("Case 3 (bounded recurrence)" if (name == "novelty_search" and rec > 0.5)
                 else "FALSIFIER" if (name == "novelty_search" and rec < 0.5)
                 else classify(lam, rec))
        results[name] = {"lambda_max": (None if np.isnan(lam) else float(lam)),
                         "recurrence_fraction": float(rec),
                         "hodge": hodge, "class": klass}
        lam_s = "n/a" if np.isnan(lam) else f"{lam:+.3f}"
        hs = "" if hodge is None else f", grad={hodge['gradient']:.2f}/rot={hodge['rotational']:.2f}"
        print(f"  {name:15s}: lambda={lam_s}, recurrence={rec:.3f}{hs} -> {klass}")

    # Lorenz: the strongest positive-entropy candidate (3D, compact attractor)
    ltraj = lorenz_traj()
    lrec = recurrence_fraction(ltraj)
    llam = lyapunov_lorenz()
    lklass = classify(llam, lrec)
    results["lorenz_chaos"] = {"lambda_max": float(llam), "recurrence_fraction": float(lrec),
                               "hodge": None, "class": lklass}
    print(f"  {'lorenz_chaos':15s}: lambda={llam:+.3f}, recurrence={lrec:.3f} -> {lklass}")

    falsifiers = [k for k, v in results.items() if "FALSIFIER" in v["class"]]
    if falsifiers:
        verdict = (f"TRICHOTOMY FALSIFIED by {falsifiers}: a compact-set preference "
                   "dynamics shows positive entropy AND absence of recurrence -- the "
                   "object Sec 7.5/7.6 says cannot exist. That section must be "
                   "rewritten.")
    else:
        pos_entropy = [k for k, v in results.items()
                       if v["lambda_max"] is not None and v["lambda_max"] > 0.05]
        verdict = (f"TRICHOTOMY HOLDS: every compact-set candidate lands in the "
                   f"trichotomy and NONE is the forbidden positive-entropy-plus-no-"
                   f"recurrence object. The strongest positive-entropy cases "
                   f"({pos_entropy or 'lorenz_chaos'}) are chaotic yet RECURRENT "
                   f"(Lorenz lambda={llam:+.2f} but recurrence {lrec:.2f}); novelty "
                   f"search on the compact torus is bounded-recurrent "
                   f"({results['novelty_search']['recurrence_fraction']:.2f}), not "
                   "sustained-novel. Sustained novelty without return requires a "
                   "non-compact value space -- the escape (Case 2) horn -- exactly as "
                   "the Meta-Optimization Collapse Theorem predicts. Sec 7.5/7.6 "
                   "survives its strongest adversarial candidates.")

    # figure
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, v in results.items():
        lam = v["lambda_max"]
        x = 0.0 if lam is None else lam
        ax.scatter(x, v["recurrence_fraction"], s=90)
        ax.annotate(name, (x, v["recurrence_fraction"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax.axhline(0.5, ls=":", color="gray")
    ax.axvline(0.0, ls=":", color="gray")
    ax.fill_between([0.05, ax.get_xlim()[1] if ax.get_xlim()[1] > 0.05 else 1], 0, 0.5,
                    color="red", alpha=0.08)
    ax.text(0.06, 0.05, "forbidden region\n(pos. entropy, no recurrence)",
            fontsize=8, color="darkred")
    ax.set_xlabel("largest Lyapunov exponent (entropy proxy)")
    ax.set_ylabel("Poincare recurrence fraction")
    ax.set_title("Exp E: endogenous-preference dynamics in the trichotomy")
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "trichotomy.png"), dpi=130)
    plt.close(fig)

    summary = {"experiment": "E_rl_agents_trichotomy",
               "candidates": results,
               "preregistered_falsifier": "compact-set dynamics with positive entropy AND no recurrence",
               "verdict": verdict, "figures": ["trichotomy.png"]}
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
