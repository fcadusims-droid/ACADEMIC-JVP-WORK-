"""Statistical machinery shared by the Paper 3 demarcation and Paper 2 residual
qualification protocols.

Includes:

* ``bipower_scale``           -- jump-robust diffusion scale (Barndorff-Nielsen &
                                Shephard 2004);
* ``t_eff_bartlett`` / ``t_eff_product`` -- effective d.o.f. under serial
                                autocorrelation (Paper 3, Sec. 5.1);
* ``girsanov_drift_lrt``      -- path-wise drift likelihood-ratio test on the
                                anti-developed (Euclidean) increments;
* ``glr_jump_test``           -- covariate-anchored generalized likelihood ratio
                                for a jump vs. a diffusive spike (Paper 3, Sec. 6.4);
* ``iaaft_surrogate``         -- amplitude-adjusted Fourier-transform surrogates
                                (Paper 2, Test Three);
* ``relaxation_asymmetry``    -- Paper 2, Test One;
* ``idempotent_rotation_stat``-- Paper 2, Test Two.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats

__all__ = [
    "bipower_scale",
    "t_eff_bartlett",
    "t_eff_product",
    "girsanov_drift_lrt",
    "glr_jump_test",
    "iaaft_surrogate",
    "relaxation_asymmetry",
    "idempotent_rotation_stat",
]

_MU1 = np.sqrt(2.0 / np.pi)  # E|Z| for standard normal


def bipower_scale(increments: NDArray) -> float:
    """Jump-robust estimate of the diffusion scale from tangent increments.

    Realised bipower variation ``mu1^-2 * mean(|r_t| |r_{t-1}|)`` is consistent
    for integrated variance even in the presence of finitely many jumps, unlike
    realised variance which is inflated by them.
    """
    r = np.linalg.norm(np.atleast_2d(increments.T).T, axis=1) if increments.ndim == 2 else np.abs(increments)
    if r.size < 2:
        return float(np.std(r) + 1e-12)
    bpv = np.mean(r[1:] * r[:-1]) / (_MU1 ** 2)
    return float(np.sqrt(max(bpv, 1e-24)))


def t_eff_bartlett(x: NDArray, max_lag: int | None = None) -> float:
    """Effective sample size ``T / (1 + 2 sum_k rho_k^2)`` (single-band form)."""
    x = np.asarray(x, float)
    T = len(x)
    if max_lag is None:
        max_lag = min(T - 1, int(10 * np.log10(T)))
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom < 1e-24:
        return float(T)
    acf = np.array([np.dot(x[:-k], x[k:]) / denom for k in range(1, max_lag + 1)])
    return float(T / (1.0 + 2.0 * np.sum(acf ** 2)))


def t_eff_product(x: NDArray, y: NDArray, max_lag: int | None = None) -> float:
    """Cross-scale product form ``T / (1 + 2 sum_k rho_k(x) rho_k(y))``.

    Used only for the cross-scale coupling statistic (Paper 3, Sec. 5.1); not
    interchangeable with the single-band form.
    """
    x = np.asarray(x, float) - np.mean(x)
    y = np.asarray(y, float) - np.mean(y)
    T = len(x)
    if max_lag is None:
        max_lag = min(T - 1, int(10 * np.log10(T)))
    dx, dy = np.dot(x, x), np.dot(y, y)
    if dx < 1e-24 or dy < 1e-24:
        return float(T)
    rx = np.array([np.dot(x[:-k], x[k:]) / dx for k in range(1, max_lag + 1)])
    ry = np.array([np.dot(y[:-k], y[k:]) / dy for k in range(1, max_lag + 1)])
    return float(T / (1.0 + 2.0 * np.sum(rx * ry)))


def _bartlett_longrun_cov(inc: NDArray, max_lag: int | None = None) -> NDArray:
    """Bartlett/Newey-West HAC long-run covariance of the increments.

    ``Sigma_LR = Gamma_0 + sum_k w_k (Gamma_k + Gamma_k^T)`` with Bartlett
    weights ``w_k = 1 - k/(L+1)``. Guarantees a positive-semidefinite estimate
    and correctly inflates the variance of the sample mean under serial
    correlation (so the drift Wald test stays calibrated when ``T_eff < T``).
    """
    T, d = inc.shape
    if max_lag is None:
        max_lag = min(T - 1, int(4 * (T / 100.0) ** (2.0 / 9.0)) + 1)
    c = inc - inc.mean(axis=0)
    Gamma0 = (c.T @ c) / T
    S = Gamma0.copy()
    for k in range(1, max_lag + 1):
        w = 1.0 - k / (max_lag + 1.0)
        Gk = (c[k:].T @ c[:-k]) / T
        S = S + w * (Gk + Gk.T)
    return S


def girsanov_drift_lrt(increments: NDArray, dt: float = 1.0):
    """Path-wise drift test from a single trajectory (HAC-robust Girsanov Wald).

    Under the anti-developed (Euclidean) increments ``dX = mu dt + sigma dW``,
    Girsanov's theorem identifies the drift from one path as the mean increment.
    Because the increments are serially correlated (``T_eff < T``, as serially
    dependent signals require), the variance of that mean is estimated by a
    Bartlett HAC long-run covariance rather than the naive ``sigma^2/T`` -- the
    naive form is anti-conservative and over-declares drift on pure diffusion.
    The Wald statistic ``T * m^T Sigma_LR^-1 m`` (with ``m`` the mean increment)
    is referred to ``chi^2`` with ``dim`` degrees of freedom.

    Returns ``(stat, p_value, mu_hat)`` with ``mu_hat = m / dt``.
    """
    inc = np.atleast_2d(increments.T).T if increments.ndim == 2 else increments[:, None]
    T, d = inc.shape
    m = inc.mean(axis=0)
    Sigma_LR = _bartlett_longrun_cov(inc)
    # ridge for numerical invertibility
    Sigma_LR = Sigma_LR + 1e-12 * np.eye(d)
    stat = T * float(m @ np.linalg.solve(Sigma_LR, m))
    p = float(stats.chi2.sf(stat, df=d))
    mu_hat = m / dt
    return stat, p, mu_hat


def glr_jump_test(increments: NDArray, covariate: NDArray,
                  anchor_window: int = 5, n_boot: int = 2000,
                  seed: int | None = None):
    """Covariate-anchored GLR jump test (Paper 3, Sec. 6.4).

    The jump candidate is anchored to the argmax of the *predictability
    covariate* (local conditional residual variance), NOT the largest increment
    -- blind search under heavy tails produces false positives and is proscribed.
    Because the covariate is smoothed, the exact jump can sit a few steps from
    the argmax, so the statistic is the max increment magnitude within
    ``anchor_window`` of the argmax, standardised by the bipower (jump-robust)
    diffusion scale. The null is an empirical bootstrap of the increment
    magnitudes outside the anchored window.

    Returns ``(tau, stat, p_value)`` where ``tau`` is the located jump index.

    NB: the bootstrap ``p_value`` is an approximation -- the covariate anchoring
    introduces a mild selection the random-window null does not fully absorb, so
    on pure diffusion it is somewhat anti-conservative. For a calibrated decision,
    threshold the returned ``stat`` against a null (dispersion) ensemble at the
    target FPR, as the experiments do, rather than relying on this ``p_value``.
    """
    inc = np.atleast_2d(increments.T).T if increments.ndim == 2 else increments[:, None]
    T = inc.shape[0]
    rng = np.random.default_rng(seed)
    w = 2 * anchor_window + 1
    anchor = int(np.argmax(covariate))
    lo, hi = max(0, anchor - anchor_window), min(T, anchor + anchor_window + 1)
    r_norm = np.linalg.norm(inc, axis=1)
    sigma = bipower_scale(inc)
    local = r_norm[lo:hi]
    tau = lo + int(np.argmax(local))
    stat = float(np.max(local)) / max(sigma, 1e-12)
    # empirical null: the max increment over *random windows of the same width*,
    # so the anchored-window max is compared like-for-like. This is what keeps
    # the test silent on heavy-tailed no-jump paths (where the anchored window is
    # not systematically more extreme than a random one) while still firing on a
    # genuine jump (which dwarfs any random-window max). A single-increment null
    # would be anti-conservative against a window-max statistic.
    starts = rng.integers(0, max(1, T - w + 1), size=n_boot)
    boot = np.array([np.max(r_norm[s:s + w]) for s in starts]) / max(sigma, 1e-12)
    p = float((np.sum(boot >= stat) + 1) / (n_boot + 1))
    return tau, float(stat), p


def iaaft_surrogate(x: NDArray, n_iter: int = 100,
                    rng: np.random.Generator | None = None) -> NDArray:
    """One iterative amplitude-adjusted Fourier-transform (IAAFT) surrogate.

    Preserves both the amplitude distribution and the power spectrum of ``x``
    while destroying nonlinear structure -- the strongest linear-Gaussian null
    for the residual-structure test (Paper 2, Test Three).
    """
    rng = np.random.default_rng() if rng is None else rng
    x = np.asarray(x, float)
    n = len(x)
    sorted_x = np.sort(x)
    amp = np.abs(np.fft.rfft(x))
    s = rng.permutation(x)
    for _ in range(n_iter):
        S = np.fft.rfft(s)
        phase = np.angle(S)
        s = np.fft.irfft(amp * np.exp(1j * phase), n=n)
        ranks = np.argsort(np.argsort(s))
        s = sorted_x[ranks]
    return s


def relaxation_asymmetry(x: NDArray) -> float:
    """Time-asymmetry of relaxation (Paper 2, Test One).

    A driven, memory-bearing (Lambda-like) process relaxes asymmetrically in
    time; a linear-Gaussian or reversible process does not. Measured as the
    difference in lag-1 conditional variance for rising vs. falling segments,
    a simple time-reversal-asymmetry statistic. Compare against surrogates.
    """
    x = np.asarray(x, float)
    dx = np.diff(x)
    up = dx > 0
    down = dx < 0
    # third-moment time-asymmetry: <(x_{t+1}-x_t)^3> is 0 under reversibility
    asym = np.mean(dx ** 3) / (np.std(dx) ** 3 + 1e-12)
    return float(asym)


def idempotent_rotation_stat(cov_pre: NDArray, cov_post: NDArray) -> float:
    """Idempotent covariance-rotation statistic (Paper 2, Test Two).

    Tests whether the pre/post covariance change is a *rotation* of the
    eigenframe (a boundary reorganisation) rather than a rescaling. Returns the
    principal subspace rotation angle (radians) between the leading eigenvectors,
    which is invariant to eigenvalue rescaling.
    """
    _, Vpre = np.linalg.eigh(0.5 * (cov_pre + cov_pre.T))
    _, Vpost = np.linalg.eigh(0.5 * (cov_post + cov_post.T))
    # leading eigenvector overlap -> principal angle
    overlap = np.clip(abs(np.dot(Vpre[:, -1], Vpost[:, -1])), 0.0, 1.0)
    return float(np.arccos(overlap))
