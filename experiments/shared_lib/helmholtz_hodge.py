"""Discrete Helmholtz-Hodge decomposition of a sampled vector field.

Used by Paper 1, Experiment E: a preference-dynamics flow ``theta_dot = f(theta)``
is decomposed into a curl-free (gradient) part, a divergence-free (rotational)
part, and a harmonic remainder. The Meta-Optimization Collapse trichotomy
(Paper 1, Sec. 7.5) predicts an autonomous preference dynamics on a compact
value space must fall into exactly one of:

* Case 1 -- **gradient descent on a meta-potential** (curl-free dominant);
* Case 2 -- **unbounded dispersion** (escapes the compact set);
* Case 3 -- **bounded recurrence** (divergence-free / conservative dominant).

The falsifying object the experiment hunts for is a field with *positive entropy
on the attractor AND absence of recurrence* on a compact set -- which the theorem
says cannot exist. This module supplies the gradient/rotational energy split.

Implementation note. The decomposition is spectral (Fourier), which makes the
gradient (longitudinal) and rotational (transverse) projections *exactly*
orthogonal by Parseval -- there is no boundary leakage as there is with
collocated finite differences. For each wavevector ``k`` the gradient part of
``F_hat`` is the projection onto ``k`` and the rotational part is the orthogonal
complement; the ``k = 0`` mode is the uniform (harmonic) drift. Periodic
boundary conditions are the natural choice here because a compact value space
of preference parameters is typically angular. A pure gradient recovers
gradient-fraction 1 and a pure rotation rotational-fraction 1, to numerical
precision, at every interior point.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "hodge_decomposition_2d",
    "hodge_energy_fractions",
]


def hodge_decomposition_2d(u: NDArray, v: NDArray):
    """Spectral Helmholtz decomposition of a 2-D field ``F = (u, v)``.

    ``F = grad(phi) + rot(psi) + harmonic``. In Fourier space the gradient
    (curl-free) part is the projection of ``F_hat(k)`` onto ``k`` and the
    rotational (divergence-free) part is its orthogonal complement; the ``k = 0``
    component is the uniform harmonic drift. Returns a dict with the
    ``gradient``, ``rotational`` and ``harmonic`` components as real ``(x, y)``
    tuples.
    """
    ny, nx = u.shape
    ky = 2 * np.pi * np.fft.fftfreq(ny)
    kx = 2 * np.pi * np.fft.fftfreq(nx)
    KX, KY = np.meshgrid(kx, ky)
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0  # protect the mean mode

    U = np.fft.fft2(u)
    V = np.fft.fft2(v)

    # longitudinal (gradient) projection: ( (k.F)/|k|^2 ) k
    kdotF = KX * U + KY * V
    gx_hat = (kdotF / k2) * KX
    gy_hat = (kdotF / k2) * KY
    # kill the mean mode in the gradient part (it is harmonic, not gradient)
    gx_hat[0, 0] = 0.0
    gy_hat[0, 0] = 0.0

    gx = np.real(np.fft.ifft2(gx_hat))
    gy = np.real(np.fft.ifft2(gy_hat))

    # harmonic = uniform (k=0) drift
    hx = np.full_like(u, np.real(U[0, 0]) / (nx * ny))
    hy = np.full_like(v, np.real(V[0, 0]) / (nx * ny))

    # rotational = remainder (divergence-free, mean removed)
    rx = u - gx - hx
    ry = v - gy - hy

    return {
        "gradient": (gx, gy),
        "rotational": (rx, ry),
        "harmonic": (hx, hy),
    }


def hodge_energy_fractions(u: NDArray, v: NDArray) -> dict:
    """Fraction of field energy in each Hodge component (exactly summing to 1).

    A curl-free-dominant field (gradient fraction near 1) is Case 1 (gradient
    descent on a meta-potential); a divergence-free-dominant field (rotational
    fraction near 1) is Case 3 (bounded recurrence / conservative circulation).
    Neither realises conversion -- that is the point of the trichotomy.
    """
    comp = hodge_decomposition_2d(u, v)
    total = float(np.sum(u ** 2 + v ** 2)) + 1e-24
    return {name: float(np.sum(a ** 2 + b ** 2) / total)
            for name, (a, b) in comp.items()}
