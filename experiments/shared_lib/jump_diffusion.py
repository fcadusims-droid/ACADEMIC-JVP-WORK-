"""Tangent-space Poisson-Levy jump-diffusion simulators (Paper 3, Sec. 4).

The tangent-space trajectory is modelled by

    dX = mu(t) dt + sigma dW + J dN

with drift ``mu``, Gaussian *or* heavy-tailed (Student-t) diffusion, and a
Poisson jump ``dN`` whose intensity is tied to the estimator's local
conditional residual variance (Paper 3, Sec. 4.2). The three ground-truth
regimes the demarcation must separate are produced here with known labels:

* ``drift``     -- persistent geodesic drift (drift-dominated reorganisation);
* ``dispersion``-- zero-drift isotropic diffusion (undirected random walk);
* ``collapse``  -- diffusion with one abrupt rank-collapse jump.

None of this is evidence about a real system; it is synthetic ground truth for
verifying that the path-wise test is executable and discriminating.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "SimConfig",
    "simulate_regime",
    "conditional_residual_variance",
    "sample_jump_times",
]


@dataclass
class SimConfig:
    """Configuration for a synthetic tangent-space trajectory."""
    dim: int = 2                 # tangent-space dimension
    T: int = 400                 # number of steps
    dt: float = 1.0
    drift_strength: float = 0.05
    diffusion_scale: float = 1.0
    ar_rho: float = 0.5          # serial autocorrelation (so T_eff < T)
    heavy_tail_df: float | None = None  # None -> Gaussian; else Student-t d.o.f.
    jump_time: int | None = None        # step index of an abrupt jump
    jump_size: float = 6.0              # magnitude of the collapse jump
    seed: int | None = None


def _diffusion_increments(cfg: SimConfig, rng: np.random.Generator) -> NDArray:
    """AR(1)-correlated diffusion increments, Gaussian or Student-t."""
    if cfg.heavy_tail_df is None:
        raw = rng.standard_normal((cfg.T, cfg.dim))
    else:
        df = cfg.heavy_tail_df
        # scale so unit variance is comparable to the Gaussian case
        raw = rng.standard_t(df, size=(cfg.T, cfg.dim)) * np.sqrt((df - 2) / df)
    inc = np.empty_like(raw)
    inc[0] = raw[0]
    for t in range(1, cfg.T):
        inc[t] = cfg.ar_rho * inc[t - 1] + np.sqrt(1 - cfg.ar_rho ** 2) * raw[t]
    return inc * cfg.diffusion_scale * np.sqrt(cfg.dt)


def simulate_regime(regime: str, cfg: SimConfig):
    """Simulate one tangent-space trajectory of the named regime.

    Returns
    -------
    X : (T, dim) ndarray
        The cumulative tangent-space path.
    info : dict
        Ground-truth metadata: ``regime``, ``jump_time`` (or None),
        ``predictability_covariate`` (local conditional residual variance).
    """
    rng = np.random.default_rng(cfg.seed)
    inc = _diffusion_increments(cfg, rng)

    if regime == "drift":
        direction = rng.standard_normal(cfg.dim)
        direction /= np.linalg.norm(direction)
        mu = cfg.drift_strength * direction
        inc = inc + mu * cfg.dt
        jump_time = None
    elif regime == "dispersion":
        jump_time = None
    elif regime == "collapse":
        jump_time = cfg.jump_time if cfg.jump_time is not None else cfg.T // 2
        jdir = rng.standard_normal(cfg.dim)
        jdir /= np.linalg.norm(jdir)
        inc[jump_time] = inc[jump_time] + cfg.jump_size * jdir
    else:
        raise ValueError(f"unknown regime {regime!r}")

    X = np.cumsum(inc, axis=0)
    cov = conditional_residual_variance(X, ar_rho=cfg.ar_rho)
    info = {
        "regime": regime,
        "jump_time": jump_time,
        "predictability_covariate": cov,
        "increments": inc,
    }
    return X, info


def conditional_residual_variance(X: NDArray, ar_rho: float = 0.5,
                                  half_window: int = 10) -> NDArray:
    """Local conditional residual variance -- the predictability covariate.

    One-step AR prediction residual, squared and locally averaged in a causal
    window. Its peak marks maximal predictive breakdown; the jump search is
    anchored to it (Paper 3, Sec. 4.2 / 6.4). Blind search on the raw increment
    is proscribed because heavy tails create false peaks.
    """
    X = np.atleast_2d(X.T).T if X.ndim == 2 else X[:, None]
    T = X.shape[0]
    resid = np.zeros(T)
    pred = np.zeros_like(X)
    pred[1:] = X[:-1] + ar_rho * np.diff(X, axis=0)
    err = X - pred
    resid = np.sum(err ** 2, axis=1)
    # causal moving average
    out = np.zeros(T)
    for t in range(T):
        lo = max(0, t - half_window)
        out[t] = np.mean(resid[lo:t + 1])
    return out


def sample_jump_times(intensity: NDArray, rng: np.random.Generator) -> NDArray:
    """Sample Poisson jump indicators given a time-varying intensity ``lambda_t``.

    ``intensity`` is ``alpha * exp(-gamma_t)`` with ``gamma_t`` the local
    log-precision of the prediction residual (Paper 3 glossary).
    """
    p = 1.0 - np.exp(-np.clip(intensity, 0, None))
    return (rng.random(intensity.shape) < p).astype(int)
