"""Experiment A -- Multi-scale windows for on-line localization (Paper 3).

Attacks the protocol's principal open problem: on-line single-trajectory
localization succeeded in only 5/15 subjects because the true transition is
often not the most abrupt geometric event against spontaneous variability.

Network policy in this environment blocks PhysioNet (see DATA.md), so this runs
in the pre-registered synthetic-adversarial mode: a genuine structural transition
(a step in the covariance geometry) is embedded in spontaneous structural
fluctuations large enough that a single-scale detector localizes to the wrong
(spontaneous) event -- reproducing the 5/15 failure mode against known ground
truth. The question is whether a bank of causal window lengths recovers
localization. This validates the *method improvement*, not the real-data claim.

Mechanism under test: a true seam is a *persistent* mean shift (survives large
windows, where spontaneous excursions cancel), whereas a spontaneous excursion is
*transient* (dominates only small windows). Aggregating causal break statistics
across scales -- especially large ones -- should localize the persistent seam.

Usage:
    python -m experiments.paper3_geodesic_kinematics.localization_multiscale.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.shared_lib import spd_manifold as spd
from experiments.shared_lib import manifold_trajectory as mt

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "localization_multiscale"
)

# ---- pre-fixed parameters ----------------------------------------------------
N_SUBJECTS = 15            # mirror the appendix
N_CH = 4
T = 600
SEAM_LO, SEAM_HI = 0.35, 0.65
D_SEAM = 0.45             # geodesic size of the true transition
WANDER = 0.05            # AR(1) spontaneous wandering scale
EXCURSION_PROB = 0.04    # rate of spontaneous large excursions
EXCURSION_SIZE = 0.5     # size of a spontaneous excursion (>= D_SEAM: adversarial)
AR_RHO = 0.8
SINGLE_SCALE = 40
MULTI_SCALES = [15, 30, 60, 100]
TOL = 12                  # localization tolerance in samples (analog of +/-2 s)


def _sphere_mean(covs):
    """Approximate Frechet mean on the square-root sphere: average the 2*sqrt(rho)
    embeddings, renormalise to the sphere, map back."""
    embs = np.mean([spd.sqrt_embed(c) for c in covs], axis=0)
    nrm = np.sqrt(np.sum(embs * embs))
    embs = embs * (2.0 / nrm) if nrm > 1e-12 else embs
    return spd.sqrt_unembed(embs)


def generate_subject(seed, seam=True):
    """A covariance trajectory with (optionally) a persistent structural seam
    embedded in spontaneous structural fluctuations. If seam=False the base drifts
    smoothly (a geodesic) with no abrupt transition -- the drift guardrail case."""
    rng = np.random.default_rng(seed)
    base_A = mt.random_density(N_CH, rng)
    dirn = spd.sqrt_log(base_A, mt.random_density(N_CH, rng))
    dirn = dirn / np.sqrt(np.sum(dirn * dirn))
    base_B = spd.sqrt_exp(base_A, D_SEAM * dirn)      # a fixed geodesic distance away
    t_seam = int(rng.uniform(SEAM_LO, SEAM_HI) * T)

    covs = []
    xi = np.zeros((N_CH, N_CH))
    for t in range(T):
        if seam:
            base = base_A if t < t_seam else base_B
        else:
            # smooth geodesic drift from A to B across the whole record (no seam)
            base = spd.sqrt_exp(base_A, (t / T) * D_SEAM * dirn)
        # AR(1) tangent wandering + occasional large spontaneous excursion
        step = WANDER * 0.5 * (rng.standard_normal((N_CH, N_CH)))
        step = 0.5 * (step + step.T)
        if rng.random() < EXCURSION_PROB:
            step = step + EXCURSION_SIZE * 0.5 * (rng.standard_normal((N_CH, N_CH)))
            step = 0.5 * (step + step.T)
        xi = AR_RHO * xi + np.sqrt(1 - AR_RHO ** 2) * step
        covs.append(spd.sqrt_exp(base, xi))
    return covs, t_seam


def break_curve(covs, w):
    """Causal/anticausal geodesic break statistic S(t,w) = distance between the
    mean covariance in [t-w,t) and [t,t+w)."""
    n = len(covs)
    S = np.full(n, np.nan)
    for t in range(w, n - w):
        mpre = _sphere_mean(covs[t - w:t])
        mpost = _sphere_mean(covs[t:t + w])
        S[t] = spd.sqrt_distance(mpre, mpost)
    return S


def _zscore(S):
    v = S[~np.isnan(S)]
    mu, sd = np.mean(v), np.std(v) + 1e-12
    Z = (S - mu) / sd
    Z[np.isnan(S)] = -np.inf
    return Z


def single_scale_localize(covs, w=SINGLE_SCALE):
    S = break_curve(covs, w)
    return int(np.nanargmax(S)), S


def multiscale_localize(covs, windows=MULTI_SCALES):
    curves = [_zscore(break_curve(covs, w)) for w in windows]
    agg = np.sum(curves, axis=0)          # aggregate z-scored breaks across scales
    return int(np.argmax(agg)), agg


def prominence(curve):
    v = curve[np.isfinite(curve)]
    med = np.median(v)
    mad = np.median(np.abs(v - med)) + 1e-12
    return float((np.max(v) - med) / mad)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment A: multi-scale localization (synthetic-adversarial mode)")
    print(f"  {N_SUBJECTS} subjects, {N_CH} ch, T={T}, seam dist={D_SEAM}, "
          f"excursion size={EXCURSION_SIZE} (>= seam: adversarial)")

    single_hits, multi_hits = 0, 0
    single_err, multi_err = [], []
    example = None
    for s in range(N_SUBJECTS):
        covs, seam = generate_subject(s, seam=True)
        t1, S1 = single_scale_localize(covs)
        t2, agg = multiscale_localize(covs)
        e1, e2 = abs(t1 - seam), abs(t2 - seam)
        single_err.append(e1)
        multi_err.append(e2)
        single_hits += (e1 <= TOL)
        multi_hits += (e2 <= TOL)
        if example is None:
            example = (covs, seam, S1, agg, t1, t2)

    # drift guardrail: no-seam subjects should not yield a confident localization
    single_drift_prom, multi_drift_prom = [], []
    single_seam_prom, multi_seam_prom = [], []
    for s in range(N_SUBJECTS):
        cd, _ = generate_subject(1000 + s, seam=False)
        single_drift_prom.append(prominence(break_curve(cd, SINGLE_SCALE)))
        multi_drift_prom.append(prominence(multiscale_localize(cd)[1]))
        cs_, _ = generate_subject(s, seam=True)
        single_seam_prom.append(prominence(break_curve(cs_, SINGLE_SCALE)))
        multi_seam_prom.append(prominence(multiscale_localize(cs_)[1]))

    # figures
    covs, seam, S1, agg, t1, t2 = example
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.plot(_zscore(S1), label=f"single scale (w={SINGLE_SCALE})", color="gray")
    ax.plot(agg / len(MULTI_SCALES), label="multiscale (mean z)", color="crimson")
    ax.axvline(seam, ls="--", color="k", label="true seam")
    ax.axvline(t1, ls=":", color="gray"); ax.axvline(t2, ls=":", color="crimson")
    ax.set_xlabel("time (samples)"); ax.set_ylabel("break statistic (z)")
    ax.set_title("Example subject: break curves"); ax.legend()

    ax = axes[1]
    ax.bar([0, 1], [single_hits / N_SUBJECTS, multi_hits / N_SUBJECTS],
           color=["gray", "crimson"])
    ax.set_xticks([0, 1]); ax.set_xticklabels(["single scale", "multiscale"])
    ax.set_ylabel(f"hit rate (|err| <= {TOL})"); ax.set_ylim(0, 1)
    ax.set_title(f"Localization hit rate ({N_SUBJECTS} subjects)")
    for i, h in enumerate([single_hits, multi_hits]):
        ax.text(i, h / N_SUBJECTS + 0.02, f"{h}/{N_SUBJECTS}", ha="center")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "localization.png"), dpi=130)
    plt.close(fig)

    # pre-registered criterion: 5/15 -> >= 10/15 without reintroducing drift/jump
    improved = multi_hits >= 10 and multi_hits > single_hits
    guardrail_ok = np.median(multi_drift_prom) < np.median(multi_seam_prom)
    if improved and guardrail_ok:
        verdict = (f"SUCCESS (synthetic): multiscale {multi_hits}/{N_SUBJECTS} vs "
                   f"single {single_hits}/{N_SUBJECTS}; drift guardrail holds "
                   "(lower prominence on no-seam drift than on true seams). The "
                   "multiscale mechanism recovers localization in principle; a "
                   "real-EEG confirmation still requires PhysioNet.")
    elif improved and not guardrail_ok:
        verdict = (f"PARTIAL: multiscale improves localization ({multi_hits}/"
                   f"{N_SUBJECTS}) but inflates prominence on drift-only records "
                   "-- it risks reintroducing the drift/jump confusion the "
                   "criterion forbids.")
    else:
        verdict = (f"NOT IMPROVED: multiscale {multi_hits}/{N_SUBJECTS} vs single "
                   f"{single_hits}/{N_SUBJECTS}; the window bank does not recover "
                   "localization under this adversarial fluctuation level.")

    summary = {
        "experiment": "A_multiscale_localization",
        "mode": "synthetic-adversarial (PhysioNet blocked by network policy)",
        "params": {"n_subjects": N_SUBJECTS, "n_ch": N_CH, "T": T,
                   "d_seam": D_SEAM, "excursion_size": EXCURSION_SIZE,
                   "single_scale": SINGLE_SCALE, "multi_scales": MULTI_SCALES,
                   "tol": TOL},
        "single_scale_hits": single_hits,
        "multiscale_hits": multi_hits,
        "single_scale_median_err": float(np.median(single_err)),
        "multiscale_median_err": float(np.median(multi_err)),
        "drift_guardrail": {
            "multi_drift_prominence_median": float(np.median(multi_drift_prom)),
            "multi_seam_prominence_median": float(np.median(multi_seam_prom)),
            "holds": bool(guardrail_ok)},
        "preregistered_criterion": "5/15 -> >= 10/15 without reintroducing drift/jump",
        "verdict": verdict,
        "figures": ["localization.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  single-scale hits: {single_hits}/{N_SUBJECTS} (median err "
          f"{np.median(single_err):.0f}); multiscale: {multi_hits}/{N_SUBJECTS} "
          f"(median err {np.median(multi_err):.0f})")
    print(f"  drift guardrail prominence: seam {np.median(multi_seam_prom):.1f} "
          f"vs drift {np.median(multi_drift_prom):.1f}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
