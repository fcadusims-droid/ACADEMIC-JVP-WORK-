"""SPD-manifold trajectory simulation and Cartan anti-development (Paper 3).

This is the faithful substrate the flat tangent-space simulator only approximates.
A state is a trace-normalised density matrix; a trajectory is a sequence of them.
The three ground-truth regimes are produced on the manifold:

* ``drift``      -- persistent *geodesic* motion (parallel-transported velocity)
                    plus small isotropic diffusion;
* ``dispersion`` -- zero-mean isotropic diffusion, no net direction;
* ``collapse``   -- diffusion plus one abrupt eigenvalue (rank) collapse.

``anti_develop`` maps a trajectory to a Euclidean semimartingale in the tangent
space at the base point, by log-mapping each step and parallel-transporting it
back to the base. Under the **square-root** metric this is exact (constant
curvature). Under the **affine-invariant** metric the distance to a near-singular
matrix diverges, so a rank collapse produces a heavy-tailed anti-developed
increment -- which is exactly why AIRM is jump-blind after calibration and the
square-root metric is committed to (Paper 3, Sec. 6.2).

Why this matters for Experiment D: a flat tangent-space model cannot show a
geometry-induced drift/jump confusion, because a pure geodesic drift
anti-develops to a straight line, not a jump. Running the demarcation on the
real anti-developed increments is the only way to decide whether the appendix's
residual confusion is structural to the square-root geometry or an artifact of
the estimator.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from . import spd_manifold as spd

__all__ = ["ManifoldSimConfig", "random_density", "simulate_manifold_regime",
           "anti_develop", "flatten_sym", "smallest_eig"]


@dataclass
class ManifoldSimConfig:
    n: int = 3                 # channel dimension (SPD(n))
    T: int = 400
    drift_strength: float = 0.02
    diffusion_scale: float = 0.02
    jump_time: int | None = None
    collapse_factor: float = 0.05   # smallest eigenvalue multiplied by this at the jump
    eig_floor: float = 1e-4
    seed: int | None = None


def random_density(n: int, rng: np.random.Generator) -> NDArray:
    A = rng.standard_normal((n, n))
    S = A @ A.T + n * np.eye(n)
    return spd.trace_normalize(S)


def _tangent_basis_project(rho: NDArray, M: NDArray) -> NDArray:
    """Project a symmetric matrix onto the tangent space of the sphere at rho."""
    p = spd.sqrt_embed(rho)
    radial = p / 2.0                       # sphere radius R = 2
    return M - np.sum(M * radial) * radial


def _random_tangent(rho: NDArray, rng: np.random.Generator, scale: float) -> NDArray:
    """Gaussian random tangent vector at rho (random magnitude AND direction).

    Diffusion must have random magnitude, not a fixed step length -- a
    fixed-length step makes every increment norm identical and the jump
    statistic degenerate.
    """
    n = rho.shape[0]
    M = 0.5 * (rng.standard_normal((n, n)) + rng.standard_normal((n, n)).T)
    return scale * _tangent_basis_project(rho, M)


def _unit_tangent(rho: NDArray, rng: np.random.Generator, scale: float) -> NDArray:
    """A persistent drift direction of fixed magnitude ``scale`` (unit-normalised)."""
    n = rho.shape[0]
    M = 0.5 * (rng.standard_normal((n, n)) + rng.standard_normal((n, n)).T)
    M = _tangent_basis_project(rho, M)
    nrm = np.sqrt(np.sum(M * M))
    return scale * M / nrm if nrm > 1e-12 else np.zeros_like(M)


def smallest_eig(rho: NDArray) -> float:
    return float(np.linalg.eigvalsh(0.5 * (rho + rho.T))[0])


def simulate_manifold_regime(regime: str, cfg: ManifoldSimConfig):
    """Simulate an SPD(n) density-matrix trajectory of the named regime.

    Returns ``(rhos, info)`` with ``rhos`` a list of ``T`` density matrices.
    """
    rng = np.random.default_rng(cfg.seed)
    rho = random_density(cfg.n, rng)
    rhos = [rho]

    # a persistent geodesic velocity direction (fixed magnitude, embedding coords)
    vel = _unit_tangent(rho, rng, cfg.drift_strength)
    jump_time = None
    if regime == "collapse":
        jump_time = cfg.jump_time if cfg.jump_time is not None else cfg.T // 2

    for t in range(1, cfg.T):
        p = spd.sqrt_embed(rho)
        step = _random_tangent(rho, rng, cfg.diffusion_scale)
        if regime == "drift":
            step = step + vel
        if regime == "collapse" and t == jump_time:
            # abrupt rank collapse: push the smallest eigenvalue down
            w, V = np.linalg.eigh(0.5 * (rho + rho.T))
            w = np.clip(w, cfg.eig_floor, None)
            w[0] = w[0] * cfg.collapse_factor
            rho_new = spd.trace_normalize((V * w) @ V.T)
            rhos.append(rho_new)
            rho = rho_new
            continue
        p_new = spd._sphere_exp(p, step)
        rho = spd.sqrt_unembed(p_new)
        # keep the velocity parallel-transported so drift stays geodesic
        if regime == "drift":
            vel = spd.sqrt_parallel_transport(rhos[-1], rho, vel)
        rhos.append(rho)

    info = {"regime": regime, "jump_time": jump_time,
            "min_eig": np.array([smallest_eig(r) for r in rhos])}
    return rhos, info


def flatten_sym(M: NDArray) -> NDArray:
    """Flatten a symmetric matrix to a vector preserving the HS (Frobenius) norm.

    Diagonal entries kept as-is; off-diagonal entries scaled by sqrt(2) so that
    the Euclidean norm of the vector equals the Frobenius norm of the matrix.
    """
    n = M.shape[0]
    iu = np.triu_indices(n, k=1)
    diag = np.diag(M)
    off = M[iu] * np.sqrt(2.0)
    return np.concatenate([diag, off])


def anti_develop(rhos, metric: str = "sqrt") -> NDArray:
    """Cartan anti-development to the tangent space at the base point.

    For each step, log-map the increment at the previous point and parallel-
    transport it back to the base, then flatten. Returns an ``(T-1, D)`` array of
    Euclidean increments.

    metric = 'sqrt' : exact round-sphere development (square-root/Wigner-Yanase).
    metric = 'airm' : affine-invariant; increments are whitening-transported to
                      the base frame. The distance to a near-singular matrix
                      diverges, so a collapse yields a heavy-tailed increment.
    """
    base = rhos[0]
    incs = []
    if metric == "sqrt":
        for t in range(1, len(rhos)):
            v = spd.sqrt_log(rhos[t - 1], rhos[t])                 # tangent at t-1
            v0 = spd.sqrt_parallel_transport(rhos[t - 1], base, v)  # to base
            incs.append(flatten_sym(v0))
    elif metric == "airm":
        # whitening transport to the base frame: V |-> base^{-1/2} V base^{-1/2}
        wB, VB = np.linalg.eigh(0.5 * (base + base.T))
        wB = np.clip(wB, 1e-12, None)
        inv_sqrt_base = (VB / np.sqrt(wB)) @ VB.T
        for t in range(1, len(rhos)):
            v = spd.airm_log(rhos[t - 1], rhos[t])                 # tangent at t-1
            v0 = inv_sqrt_base @ v @ inv_sqrt_base
            incs.append(flatten_sym(0.5 * (v0 + v0.T)))
    else:
        raise ValueError(f"unknown metric {metric!r}")
    return np.array(incs)
