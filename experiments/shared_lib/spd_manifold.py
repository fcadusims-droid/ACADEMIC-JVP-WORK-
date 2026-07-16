"""SPD / density-matrix manifold utilities for the Paper 3 kinematics protocol.

This module implements the two metrics the protocol contrasts:

* The **square-root (Wigner-Yanase) metric**. A trace-normalised SPD (density)
  matrix ``rho`` is mapped by ``Phi(rho) = 2 * sqrtm(rho)``. Since
  ``||2 sqrt(rho)||_F^2 = 4 tr(rho) = 4`` for unit trace, the image lies on a
  Hilbert-Schmidt sphere of radius ``R = 2`` in the space of symmetric matrices.
  That sphere has *constant* sectional curvature ``K = 1/R^2 = 1/4`` at every
  channel dimension ``N`` (Paper 3, Sec. 6.2). Under this embedding the log/exp
  maps, geodesic distance and parallel transport are the exact round-sphere
  formulas -- so Cartan anti-development is exact and holonomy is *known*, not
  estimated.

* The **affine-invariant metric (AIRM)** on the full SPD cone, used as the
  contrast metric whose diffusion increments are heavy-tailed near rank collapse.

Nothing here is evidence about any real system. It is measurement geometry.

References
----------
Bhatia (2007) *Positive Definite Matrices*; Pennec, Fillard, Ayache (2006);
Amari (2016) *Information Geometry*.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "sqrtm_psd",
    "logm_psd",
    "expm_sym",
    "trace_normalize",
    "eigfloor",
    # square-root metric
    "sqrt_embed",
    "sqrt_unembed",
    "sqrt_distance",
    "sqrt_log",
    "sqrt_exp",
    "sqrt_parallel_transport",
    # affine-invariant metric
    "airm_distance",
    "airm_log",
    "airm_exp",
    # log-Euclidean metric
    "logeuclid_distance",
    "logeuclid_log",
    # Bures-Wasserstein metric
    "bures_wasserstein_distance",
    "bures_log",
    # verification
    "sectional_curvature_sqrt",
]

_EPS = 1e-12


def _sym(A: NDArray) -> NDArray:
    """Symmetrise (kills numerical asymmetry from eig round-trips)."""
    return 0.5 * (A + A.swapaxes(-1, -2))


def _eigh_psd(A: NDArray):
    """Eigendecomposition of a symmetric matrix, eigenvalues clipped positive."""
    w, V = np.linalg.eigh(_sym(A))
    w = np.clip(w, _EPS, None)
    return w, V


def sqrtm_psd(A: NDArray) -> NDArray:
    """Symmetric positive-(semi)definite matrix square root."""
    w, V = _eigh_psd(A)
    return _sym((V * np.sqrt(w)) @ V.swapaxes(-1, -2))


def logm_psd(A: NDArray) -> NDArray:
    """Matrix logarithm of an SPD matrix (real symmetric result)."""
    w, V = _eigh_psd(A)
    return _sym((V * np.log(w)) @ V.swapaxes(-1, -2))


def expm_sym(A: NDArray) -> NDArray:
    """Matrix exponential of a symmetric matrix."""
    w, V = np.linalg.eigh(_sym(A))
    return _sym((V * np.exp(w)) @ V.swapaxes(-1, -2))


def trace_normalize(A: NDArray) -> NDArray:
    """Project an SPD matrix onto the unit-trace density manifold.

    Removes the global-power / broadband-gain confound so only correlation
    *shape* survives (Paper 3, Sec. 3.1).
    """
    tr = np.trace(A, axis1=-1, axis2=-2)[..., None, None]
    return A / np.clip(tr, _EPS, None)


def eigfloor(A: NDArray, eps: float = 1e-6) -> NDArray:
    """Clip eigenvalues to a strict positive floor (numerical conditioning).

    Keeps the log-map, estimator and parallel transport well defined near a
    rank collapse (Paper 3 glossary, ``P_eps``). Under the square-root metric
    the floor's role is conditioning, not preventing a distance divergence.
    """
    w, V = np.linalg.eigh(_sym(A))
    w = np.clip(w, eps, None)
    return _sym((V * w) @ V.swapaxes(-1, -2))


# --------------------------------------------------------------------------
# Square-root (Wigner-Yanase) metric: exact round sphere of radius 2.
# --------------------------------------------------------------------------
_R = 2.0  # sphere radius of the 2*sqrt(rho) embedding on the unit-trace manifold


def sqrt_embed(rho: NDArray) -> NDArray:
    """Embed a unit-trace density matrix onto the HS sphere: ``2 sqrt(rho)``."""
    return 2.0 * sqrtm_psd(rho)


def sqrt_unembed(X: NDArray) -> NDArray:
    """Inverse embedding: ``(X/2)^2`` back to a density matrix."""
    H = X / 2.0
    return trace_normalize(_sym(H @ H))


def _hs_inner(A: NDArray, B: NDArray) -> float:
    return float(np.sum(A * B))


def sqrt_distance(rho1: NDArray, rho2: NDArray) -> float:
    """Geodesic distance on the radius-2 sphere between two density matrices.

    ``d = 2 * arccos( tr( sqrt(rho1) sqrt(rho2) ) )`` -- the Bures-angle /
    Wigner-Yanase distance.
    """
    s1, s2 = sqrtm_psd(rho1), sqrtm_psd(rho2)
    c = np.clip(_hs_inner(s1, s2), -1.0, 1.0)
    return 2.0 * float(np.arccos(c))


def _sphere_log(p: NDArray, q: NDArray) -> NDArray:
    """Log map on a sphere of radius ``_R`` centred at the origin (ambient coords)."""
    cos_t = np.clip(_hs_inner(p, q) / (_R * _R), -1.0, 1.0)
    theta = np.arccos(cos_t)
    if theta < 1e-9:
        return np.zeros_like(p)
    # component of q orthogonal to p, rescaled to arc length theta*R
    u = q - cos_t * p
    nrm = np.sqrt(_hs_inner(u, u))
    if nrm < 1e-12:
        return np.zeros_like(p)
    return (_R * theta) * (u / nrm)


def _sphere_exp(p: NDArray, v: NDArray) -> NDArray:
    """Exp map on a sphere of radius ``_R`` (ambient coords)."""
    vnrm = np.sqrt(_hs_inner(v, v))
    if vnrm < 1e-12:
        return p.copy()
    ang = vnrm / _R
    return np.cos(ang) * p + np.sin(ang) * (_R * v / vnrm)


def sqrt_log(rho_base: NDArray, rho_pt: NDArray) -> NDArray:
    """Log map at ``rho_base`` toward ``rho_pt``, returned in embedding coords."""
    p = sqrt_embed(rho_base)
    q = sqrt_embed(rho_pt)
    return _sphere_log(p, q)


def sqrt_exp(rho_base: NDArray, v: NDArray) -> NDArray:
    """Exp map at ``rho_base`` of embedding-coordinate tangent ``v``."""
    p = sqrt_embed(rho_base)
    return sqrt_unembed(_sphere_exp(p, v))


def sqrt_parallel_transport(rho_from: NDArray, rho_to: NDArray, v: NDArray) -> NDArray:
    """Parallel transport tangent ``v`` from ``rho_from`` to ``rho_to`` on the sphere.

    Standard round-sphere transport along the connecting geodesic; being an
    isometry it preserves the inner products entering the Girsanov log-likelihood
    (Paper 3, Sec. 6.2 Stage 1).
    """
    p = sqrt_embed(rho_from)
    q = sqrt_embed(rho_to)
    log_pq = _sphere_log(p, q)
    dist = np.sqrt(_hs_inner(log_pq, log_pq))
    if dist < 1e-12:
        return v.copy()
    u = log_pq / dist  # unit tangent at p toward q
    ang = dist / _R
    v_par = _hs_inner(v, u)          # component along transport direction
    v_perp = v - v_par * u           # component orthogonal (unchanged)
    # rotate the (u, p) plane by angle `ang`
    transported = (
        v_perp
        + v_par * (np.cos(ang) * u - np.sin(ang) * (p / _R))
    )
    return transported


# --------------------------------------------------------------------------
# Affine-invariant metric (AIRM) on the full SPD cone -- contrast metric.
# --------------------------------------------------------------------------
def airm_distance(A: NDArray, B: NDArray) -> float:
    """Affine-invariant Riemannian distance ``||log(A^-1/2 B A^-1/2)||_F``."""
    wA, VA = _eigh_psd(A)
    inv_sqrt = _sym((VA / np.sqrt(wA)) @ VA.T)
    M = _sym(inv_sqrt @ B @ inv_sqrt)
    w, _ = np.linalg.eigh(M)
    w = np.clip(w, _EPS, None)
    return float(np.sqrt(np.sum(np.log(w) ** 2)))


def airm_log(A: NDArray, B: NDArray) -> NDArray:
    """AIRM log map at ``A`` toward ``B`` (tangent = symmetric matrix)."""
    wA, VA = _eigh_psd(A)
    sqrtA = _sym((VA * np.sqrt(wA)) @ VA.T)
    inv_sqrt = _sym((VA / np.sqrt(wA)) @ VA.T)
    return _sym(sqrtA @ logm_psd(_sym(inv_sqrt @ B @ inv_sqrt)) @ sqrtA)


def airm_exp(A: NDArray, V: NDArray) -> NDArray:
    """AIRM exp map at ``A`` of tangent ``V``."""
    wA, VA = _eigh_psd(A)
    sqrtA = _sym((VA * np.sqrt(wA)) @ VA.T)
    inv_sqrt = _sym((VA / np.sqrt(wA)) @ VA.T)
    return _sym(sqrtA @ expm_sym(_sym(inv_sqrt @ V @ inv_sqrt)) @ sqrtA)


# --------------------------------------------------------------------------
# Log-Euclidean metric: the FLAT metric log(A) |-> symmetric-matrix space.
# Geodesics are straight lines in the log domain, so the connection is flat and
# holonomy is identically zero -- the natural contrast to the curved square-root
# sphere for the Exp D drift/holonomy corner (a geodesic drift accumulates NO
# holonomy here). Distance is ||log A - log B||_F (Arsigny et al. 2006).
# --------------------------------------------------------------------------
def logeuclid_distance(A: NDArray, B: NDArray) -> float:
    """Log-Euclidean distance ``||log(A) - log(B)||_F``."""
    return float(np.sqrt(np.sum((logm_psd(A) - logm_psd(B)) ** 2)))


def logeuclid_log(A: NDArray, B: NDArray) -> NDArray:
    """Log-Euclidean log map at ``A`` toward ``B``.

    Because the metric is flat under ``A |-> log(A)``, the tangent increment is
    simply ``log(B) - log(A)`` and parallel transport is the identity -- there is
    no holonomy for a curved-path drift to accumulate.
    """
    return _sym(logm_psd(B) - logm_psd(A))


# --------------------------------------------------------------------------
# Bures-Wasserstein metric: the Wasserstein-2 geometry of centred Gaussians.
# Distinct from the square-root sphere (which realises the Bures *angle*): the BW
# distance is the *chordal* fidelity distance and its geodesics/connection differ.
# --------------------------------------------------------------------------
def _sqrtm_product(A: NDArray, B: NDArray) -> NDArray:
    """Matrix square root of the (non-symmetric) product ``A B`` for SPD A, B.

    Computed as ``A^{1/2} (A^{1/2} B A^{1/2})^{1/2} A^{-1/2}`` so it is real and
    squares back to ``A B`` exactly (avoids a complex scipy.sqrtm on a
    non-symmetric matrix).
    """
    wA, VA = _eigh_psd(A)
    sqrtA = _sym((VA * np.sqrt(wA)) @ VA.T)
    inv_sqrtA = _sym((VA / np.sqrt(wA)) @ VA.T)
    inner = sqrtm_psd(_sym(sqrtA @ B @ sqrtA))
    return sqrtA @ inner @ inv_sqrtA


def bures_wasserstein_distance(A: NDArray, B: NDArray) -> float:
    """Bures-Wasserstein distance ``sqrt(tr A + tr B - 2 tr (A^{1/2} B A^{1/2})^{1/2})``."""
    wA, VA = _eigh_psd(A)
    sqrtA = _sym((VA * np.sqrt(wA)) @ VA.T)
    inner = sqrtm_psd(_sym(sqrtA @ B @ sqrtA))
    val = np.trace(A) + np.trace(B) - 2.0 * np.trace(inner)
    return float(np.sqrt(max(val, 0.0)))


def bures_log(A: NDArray, B: NDArray) -> NDArray:
    """Bures-Wasserstein log map at ``A`` toward ``B`` (tangent = symmetric matrix).

    The BW geodesic from ``A`` to ``B`` is
    ``gamma(t) = (1-t)^2 A + t^2 B + t(1-t)[(AB)^{1/2} + (BA)^{1/2}]``,
    so ``Log_A(B) = gamma'(0) = (AB)^{1/2} + (BA)^{1/2} - 2A = 2 sym((AB)^{1/2}) - 2A``
    (Bhatia, Jain & Lim 2019). Zero iff ``B = A``.
    """
    sp = _sqrtm_product(A, B)
    return _sym(2.0 * _sym(sp) - 2.0 * A)


# --------------------------------------------------------------------------
# Verification: sectional curvature of the square-root sphere == 1/4.
# --------------------------------------------------------------------------
def sectional_curvature_sqrt(rho: NDArray, n_planes: int = 20,
                             rng: np.random.Generator | None = None) -> NDArray:
    """Empirical sectional curvature of the square-root metric at ``rho``.

    The image of the density manifold is an open region of a Euclidean sphere of
    radius ``R = 2`` in the space of symmetric matrices, whose shape operator is
    ``S = -(1/R) I`` on the tangent space. By the Gauss equation the sectional
    curvature of every tangent 2-plane is ``1/R^2 = 1/4``. This samples random
    tangent 2-planes and returns the measured curvature per plane; the array
    should be ``0.25`` to numerical precision, at any ``N`` (Paper 3, Sec. 6.2).
    """
    rng = np.random.default_rng() if rng is None else rng
    p = sqrt_embed(rho)  # point on sphere, ambient symmetric-matrix coords
    d = p.shape[-1]

    def rand_sym():
        M = rng.standard_normal((d, d))
        return _sym(M)

    def project_tangent(W):
        # tangent to sphere at p = component orthogonal to the radial dir p/R
        radial = p / _R
        return W - _hs_inner(W, radial) * radial

    out = np.empty(n_planes)
    for i in range(n_planes):
        X = project_tangent(rand_sym())
        Y = project_tangent(rand_sym())
        # Gram-Schmidt so the plane is well conditioned
        X = X / np.sqrt(_hs_inner(X, X))
        Y = Y - _hs_inner(Y, X) * X
        Y = Y / np.sqrt(_hs_inner(Y, Y))
        # shape operator S = -(1/R) Id  ->  <S X, X> = -1/R, etc.
        # K = ( <SX,X><SY,Y> - <SX,Y>^2 ) / ( |X|^2|Y|^2 - <X,Y>^2 )
        sXX = -(1.0 / _R) * _hs_inner(X, X)
        sYY = -(1.0 / _R) * _hs_inner(Y, Y)
        sXY = -(1.0 / _R) * _hs_inner(X, Y)
        denom = _hs_inner(X, X) * _hs_inner(Y, Y) - _hs_inner(X, Y) ** 2
        out[i] = (sXX * sYY - sXY ** 2) / denom
    return out
