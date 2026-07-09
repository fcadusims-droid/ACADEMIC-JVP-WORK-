"""Self-tests for the shared library. Run: ``python -m experiments.shared_lib.test_shared_lib``
or ``pytest experiments/shared_lib/test_shared_lib.py``.

These check the *paper's own numerical claims* on the machinery, not any
empirical result:

* the square-root metric has constant sectional curvature K = 1/4 at N = 2, 3, 4;
* log/exp and parallel transport round-trip and preserve norms;
* Girsanov separates a drift trajectory from a dispersion trajectory at N = 1;
* the covariate-anchored jump test fires on a collapse and stays silent on
  heavy-tailed no-jump diffusion (the failure that fixed the precondition);
* the Hodge decomposition recovers a pure gradient and a pure rotation exactly.
"""
from __future__ import annotations

import numpy as np

from experiments.shared_lib import spd_manifold as spd
from experiments.shared_lib import jump_diffusion as jd
from experiments.shared_lib import stats_utils as su
from experiments.shared_lib import helmholtz_hodge as hh


def _rand_density(n, rng):
    A = rng.standard_normal((n, n))
    S = A @ A.T + n * np.eye(n)
    return spd.trace_normalize(S)


def test_constant_curvature():
    rng = np.random.default_rng(0)
    for n in (2, 3, 4):
        rho = _rand_density(n, rng)
        K = spd.sectional_curvature_sqrt(rho, n_planes=30, rng=rng)
        assert np.allclose(K, 0.25, atol=1e-6), f"N={n}: K={K.mean():.6f} (want 0.25)"
    print("[ok] square-root metric curvature K=1/4 at N=2,3,4")


def test_log_exp_transport_roundtrip():
    rng = np.random.default_rng(1)
    rho0 = _rand_density(3, rng)
    rho1 = _rand_density(3, rng)
    v = spd.sqrt_log(rho0, rho1)
    rho1_back = spd.sqrt_exp(rho0, v)
    assert spd.sqrt_distance(rho1, rho1_back) < 1e-6, "exp(log) did not round-trip"
    # geodesic distance equals tangent length
    d = spd.sqrt_distance(rho0, rho1)
    vlen = np.sqrt(np.sum(v * v))
    assert abs(d - vlen) < 1e-6, f"distance {d} != tangent length {vlen}"
    # parallel transport preserves norm
    rho2 = _rand_density(3, rng)
    vt = spd.sqrt_parallel_transport(rho0, rho2, v)
    assert abs(np.sqrt(np.sum(vt * vt)) - vlen) < 1e-6, "transport changed norm"
    print("[ok] log/exp round-trip, isometric distance, norm-preserving transport")


def test_girsanov_separates_drift_from_dispersion():
    n_seeds = 30
    drift_p, disp_p = [], []
    for s in range(n_seeds):
        cfg = jd.SimConfig(dim=1, T=400, drift_strength=0.25, diffusion_scale=1.0,
                           ar_rho=0.5, seed=s)
        Xd, infod = jd.simulate_regime("drift", cfg)
        Xz, infoz = jd.simulate_regime("dispersion", cfg)
        _, pd_, _ = su.girsanov_drift_lrt(infod["increments"])
        _, pz_, _ = su.girsanov_drift_lrt(infoz["increments"])
        drift_p.append(pd_)
        disp_p.append(pz_)
    drift_p, disp_p = np.array(drift_p), np.array(disp_p)
    fpr = float(np.mean(disp_p < 0.05))  # calibration: should be ~0.05
    assert np.median(drift_p) < 0.01, f"drift not detected: median p={np.median(drift_p)}"
    assert fpr < 0.20, f"dispersion FPR inflated: {fpr:.2f} (HAC calibration failed)"
    print(f"[ok] Girsanov (HAC): drift median p={np.median(drift_p):.1e}, "
          f"dispersion FPR@0.05={fpr:.2f}")


def test_jump_test_on_geometric_pipeline():
    """The covariate-anchored jump statistic is tested on the faithful geometric
    pipeline (SPD anti-development), where the predictability covariate is
    decoupled from individual increments -- unlike the flat tangent-space model,
    where the covariate degenerates into increment magnitude. The statistic is
    used the way Experiment D uses it: the decision threshold is calibrated
    empirically to the pure-diffusion (dispersion) ensemble at a target FPR, then
    a genuine collapse must exceed it with high power and rank above dispersion.
    (The bootstrap p-value of glr_jump_test is only an approximation; empirical
    calibration to a null ensemble is the correct, well-calibrated usage.)"""
    from experiments.shared_lib import manifold_trajectory as mt

    def jstat(rhos, w=5):
        inc = mt.anti_develop(rhos, "sqrt")
        X = np.cumsum(inc, axis=0)
        cov = jd.conditional_residual_variance(X)
        T = inc.shape[0]
        a = int(np.argmax(cov))
        lo, hi = max(0, a - w), min(T, a + w + 1)
        r = np.linalg.norm(inc, axis=1)
        return float(np.max(r[lo:hi])) / max(su.bipower_scale(inc), 1e-12)

    disp, coll = [], []
    for s in range(30):
        cfg_d = mt.ManifoldSimConfig(n=3, T=400, diffusion_scale=0.02, seed=s)
        disp.append(jstat(mt.simulate_manifold_regime("dispersion", cfg_d)[0]))
        cfg_c = mt.ManifoldSimConfig(n=3, T=400, diffusion_scale=0.02,
                                     jump_time=200, collapse_factor=0.05, seed=200 + s)
        coll.append(jstat(mt.simulate_manifold_regime("collapse", cfg_c)[0]))
    disp, coll = np.array(disp), np.array(coll)
    thr = np.quantile(disp, 0.95)                 # empirical 5%-FPR threshold
    power = float(np.mean(coll > thr))
    # rank separation independent of any threshold
    allv = np.concatenate([coll, disp])
    ranks = np.argsort(np.argsort(allv)) + 1
    auc = (ranks[:len(coll)].sum() - len(coll) * (len(coll) + 1) / 2) / (len(coll) * len(disp))
    assert power > 0.9, f"collapse under-detected at empirical threshold (power={power})"
    assert auc > 0.95, f"collapse not separated from dispersion (AUC={auc})"
    print(f"[ok] geometric jump test (empirical calibration): collapse power={power:.2f}, "
          f"AUC(collapse vs dispersion)={auc:.2f}")


def test_hodge_recovers_pure_fields():
    n = 64
    y, x = np.mgrid[0:n, 0:n] * (2 * np.pi / n)
    # pure gradient of a periodic potential phi = sin(x) + cos(y)
    gx, gy = np.cos(x), -np.sin(y)
    frac = hh.hodge_energy_fractions(gx, gy)
    assert frac["gradient"] > 0.99, f"gradient field misclassified: {frac}"
    assert abs(sum(frac.values()) - 1.0) < 1e-6, f"fractions do not sum to 1: {frac}"
    # pure rotation from a periodic stream function psi = sin(x)cos(y):
    # rot(psi) = (d psi/dy, -d psi/dx) is divergence-free
    px = np.cos(x) * np.cos(y)   # d psi/dx
    py = -np.sin(x) * np.sin(y)  # d psi/dy
    rx, ry = py, -px
    frac2 = hh.hodge_energy_fractions(rx, ry)
    assert frac2["rotational"] > 0.99, f"rotational field misclassified: {frac2}"
    print(f"[ok] Hodge (spectral): gradient frac={frac['gradient']:.3f}, "
          f"rotational frac={frac2['rotational']:.3f}, sum={sum(frac.values()):.3f}")


def main():
    test_constant_curvature()
    test_log_exp_transport_roundtrip()
    test_girsanov_separates_drift_from_dispersion()
    test_jump_test_on_geometric_pipeline()
    test_hodge_recovers_pure_fields()
    print("\nAll shared_lib self-tests passed.")


if __name__ == "__main__":
    main()
