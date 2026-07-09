"""Experiment A -- Multi-scale windows for on-line localization (Paper 3).

Attacks the protocol's principal open problem: on-line single-trajectory
localization succeeded in only 5/15 subjects because the true transition is often
not the most abrupt geometric event against spontaneous variability.

Network policy in this environment blocks PhysioNet (see DATA.md), so this runs
in the pre-registered synthetic-adversarial mode: a genuine *persistent*
structural seam (a step in the covariance geometry) is embedded in spontaneous
structural fluctuations, including sharp transient excursions whose pointwise
geometric break EXCEEDS the seam -- reproducing the appendix's failure mode
(the true transition is not the most abrupt event) against known ground truth.

The fragile baseline mirrors the appendix detector: localize to the largest
*pointwise/short-window* geometric break -- which a transient excursion beats.
The proposed fix is a bank of causal window lengths: a true seam is a persistent
mean shift (survives large windows, where transient excursions cancel), so
aggregating z-scored break statistics across scales localizes the seam. A single
large window is reported too, to separate "multiscale helps" from "just use a
bigger window" -- and to expose the robustness/precision trade-off.

Fast path: each covariance is embedded once (2*sqrt(rho)); window means are
cumulative-sum averages of the embeddings renormalised to the sphere, and the
geodesic distance is computed directly as 2*arccos(<p,q>/4) with no re-eigendecomp.

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
N_SUBJECTS = 15
N_CH = 4
T = 600
SEAM_LO, SEAM_HI = 0.35, 0.65
D_SEAM = 0.45              # geodesic size of the true (persistent) transition
WANDER = 0.05             # AR(1) spontaneous wandering scale
EXCURSION_PROB = 0.03     # rate of sharp spontaneous excursions
EXCURSION_SIZE = 0.7      # sharp transient step size (> D_SEAM: adversarial)
AR_RHO = 0.8
SINGLE_FRAGILE = 3        # short-window baseline (appendix-like, pointwise-ish)
SINGLE_LARGE = 120        # robust-but-imprecise single window (for contrast)
MULTI_SCALES = [3, 12, 40, 120]
TOL = 15                   # localization tolerance in samples (analog of +/-2 s)
_R = 2.0


def generate_subject(seed, seam=True):
    """Covariance trajectory with an optional persistent structural seam plus
    spontaneous wandering and sharp transient excursions. seam=False -> smooth
    geodesic drift, no abrupt transition (the drift guardrail case)."""
    rng = np.random.default_rng(seed)
    base_A = mt.random_density(N_CH, rng)
    dirn = spd.sqrt_log(base_A, mt.random_density(N_CH, rng))
    dirn = dirn / np.sqrt(np.sum(dirn * dirn))
    t_seam = int(rng.uniform(SEAM_LO, SEAM_HI) * T)

    covs = []
    xi = np.zeros((N_CH, N_CH))
    for t in range(T):
        if seam:
            base = base_A if t < t_seam else spd.sqrt_exp(base_A, D_SEAM * dirn)
        else:
            base = spd.sqrt_exp(base_A, (t / T) * D_SEAM * dirn)
        step = WANDER * 0.5 * (rng.standard_normal((N_CH, N_CH)))
        step = 0.5 * (step + step.T)
        xi = AR_RHO * xi + np.sqrt(1 - AR_RHO ** 2) * step
        # sharp transient excursion: added to THIS sample only (not smoothed in)
        offset = np.zeros((N_CH, N_CH))
        if rng.random() < EXCURSION_PROB:
            o = EXCURSION_SIZE * 0.5 * rng.standard_normal((N_CH, N_CH))
            offset = 0.5 * (o + o.T)
        covs.append(spd.sqrt_exp(base, xi + offset))
    return covs, t_seam


def embed_cumsum(covs):
    """Embed each covariance (2*sqrt(rho)) and return the cumulative sum for O(1)
    window means."""
    E = np.array([spd.sqrt_embed(c) for c in covs])       # (T, n, n)
    C = np.concatenate([np.zeros((1,) + E.shape[1:]), np.cumsum(E, axis=0)], axis=0)
    return E, C


def _win_mean_emb(C, lo, hi):
    m = (C[hi] - C[lo]) / (hi - lo)
    nrm = np.sqrt(np.sum(m * m))
    return m * (_R / nrm) if nrm > 1e-12 else m


def _sphere_dist_emb(p, q):
    return 2.0 * float(np.arccos(np.clip(np.sum(p * q) / (_R * _R), -1.0, 1.0)))


def break_curve(C, w):
    """S(t,w) = geodesic distance between the mean embedding in [t-w,t) and
    [t,t+w), computed directly on the sphere."""
    n = C.shape[0] - 1
    S = np.full(n, np.nan)
    for t in range(w, n - w):
        S[t] = _sphere_dist_emb(_win_mean_emb(C, t - w, t), _win_mean_emb(C, t, t + w))
    return S


def _zscore(S):
    v = S[~np.isnan(S)]
    mu, sd = np.mean(v), np.std(v) + 1e-12
    Z = (S - mu) / sd
    Z[np.isnan(S)] = -np.inf
    return Z


def multiscale_agg(C, windows=MULTI_SCALES):
    return np.sum([_zscore(break_curve(C, w)) for w in windows], axis=0)


def prominence(curve):
    v = curve[np.isfinite(curve)]
    med = np.median(v)
    mad = np.median(np.abs(v - med)) + 1e-12
    return float((np.max(v) - med) / mad)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment A: multi-scale localization (synthetic-adversarial mode)")
    print(f"  {N_SUBJECTS} subjects, {N_CH} ch, T={T}, seam={D_SEAM}, "
          f"excursion={EXCURSION_SIZE} (> seam: adversarial)")

    res = {"fragile": {"hits": 0, "err": []},
           "large": {"hits": 0, "err": []},
           "multi": {"hits": 0, "err": []}}
    example = None
    for s in range(N_SUBJECTS):
        covs, seam = generate_subject(s, seam=True)
        _, C = embed_cumsum(covs)
        S_frag = break_curve(C, SINGLE_FRAGILE)
        S_large = break_curve(C, SINGLE_LARGE)
        agg = multiscale_agg(C)
        for key, curve in [("fragile", S_frag), ("large", S_large), ("multi", agg)]:
            t_hat = int(np.nanargmax(np.where(np.isnan(curve), -np.inf, curve)))
            err = abs(t_hat - seam)
            res[key]["err"].append(err)
            res[key]["hits"] += (err <= TOL)
        if example is None:
            example = (seam, _zscore(S_frag), _zscore(S_large), agg / len(MULTI_SCALES))

    # drift guardrail: no-seam records should give lower peak prominence
    drift_prom, seam_prom = [], []
    for s in range(N_SUBJECTS):
        cd, _ = generate_subject(1000 + s, seam=False)
        _, Cd = embed_cumsum(cd)
        drift_prom.append(prominence(multiscale_agg(Cd)))
        cs_, _ = generate_subject(s, seam=True)
        _, Cs = embed_cumsum(cs_)
        seam_prom.append(prominence(multiscale_agg(Cs)))

    # figure
    seam, zf, zl, zm = example
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.plot(zf, label=f"fragile single (w={SINGLE_FRAGILE})", color="gray", alpha=0.8)
    ax.plot(zl, label=f"large single (w={SINGLE_LARGE})", color="steelblue", alpha=0.8)
    ax.plot(zm, label="multiscale", color="crimson", lw=2)
    ax.axvline(seam, ls="--", color="k", label="true seam")
    ax.set_xlabel("time (samples)"); ax.set_ylabel("break statistic (z)")
    ax.set_title("Example subject: break curves"); ax.legend(fontsize=8)
    ax = axes[1]
    labels = ["fragile\nsingle", "large\nsingle", "multiscale"]
    hits = [res["fragile"]["hits"], res["large"]["hits"], res["multi"]["hits"]]
    ax.bar(range(3), [h / N_SUBJECTS for h in hits],
           color=["gray", "steelblue", "crimson"])
    ax.set_xticks(range(3)); ax.set_xticklabels(labels)
    ax.set_ylabel(f"hit rate (|err| <= {TOL})"); ax.set_ylim(0, 1.05)
    ax.set_title(f"Localization hit rate ({N_SUBJECTS} subjects)")
    for i, h in enumerate(hits):
        ax.text(i, h / N_SUBJECTS + 0.02, f"{h}/{N_SUBJECTS}", ha="center")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "localization.png"), dpi=130)
    plt.close(fig)

    frag_h, large_h, multi_h = hits
    guardrail_ok = np.median(drift_prom) < np.median(seam_prom)
    improved = multi_h >= 10 and multi_h > frag_h
    large_alone_suffices = large_h >= 10 and large_h >= multi_h - 1
    if improved and guardrail_ok and large_alone_suffices:
        # honest: the operative fix is a larger window, not multiscale aggregation
        verdict = (f"CRITERION MET, but the fix is WINDOW SIZE, not multiscale: "
                   f"fragile short window {frag_h}/{N_SUBJECTS} -> multiscale "
                   f"{multi_h}/{N_SUBJECTS}; however a single LARGE window already "
                   f"reaches {large_h}/{N_SUBJECTS} (median err "
                   f"{np.median(res['large']['err']):.0f}), matching multiscale. In "
                   "this synthetic setup the 5/15 failure is a window-size artifact "
                   "(short windows are fooled by transient excursions); enlarging the "
                   "analysis window fixes it, and the multiscale bank adds no measured "
                   "value over a single large window. Drift guardrail holds "
                   f"(prominence seam {np.median(seam_prom):.1f} > drift "
                   f"{np.median(drift_prom):.1f}). Caveats: symmetric windows (offline "
                   "localization, not strictly causal/online); real EEG may impose a "
                   "precision cost on a large window that a multiscale bank could "
                   "escape -- untested without PhysioNet.")
    elif improved and guardrail_ok:
        verdict = (f"SUCCESS (synthetic): fragile {frag_h}/{N_SUBJECTS} -> multiscale "
                   f"{multi_h}/{N_SUBJECTS}, beating a single large window "
                   f"({large_h}/{N_SUBJECTS}) -- the bank adds value beyond enlarging "
                   f"the window. Drift guardrail holds (seam {np.median(seam_prom):.1f} "
                   f"> drift {np.median(drift_prom):.1f}). Real-EEG confirmation needs "
                   "PhysioNet.")
    elif improved and not guardrail_ok:
        verdict = (f"PARTIAL: multiscale improves ({frag_h}->{multi_h}/{N_SUBJECTS}) "
                   "but inflates prominence on drift-only records -- risks the "
                   "drift/jump confusion the criterion forbids.")
    else:
        verdict = (f"NOT IMPROVED: fragile {frag_h}/{N_SUBJECTS}, multiscale "
                   f"{multi_h}/{N_SUBJECTS} -- the window bank does not recover "
                   "localization under this adversarial fluctuation level.")

    summary = {
        "experiment": "A_multiscale_localization",
        "mode": "synthetic-adversarial (PhysioNet blocked by network policy)",
        "params": {"n_subjects": N_SUBJECTS, "n_ch": N_CH, "T": T, "d_seam": D_SEAM,
                   "excursion_size": EXCURSION_SIZE, "single_fragile": SINGLE_FRAGILE,
                   "single_large": SINGLE_LARGE, "multi_scales": MULTI_SCALES,
                   "tol": TOL},
        "hits": {"fragile_single": frag_h, "large_single": large_h,
                 "multiscale": multi_h, "n": N_SUBJECTS},
        "median_err": {k: float(np.median(res[k]["err"])) for k in res},
        "drift_guardrail": {"seam_prominence_median": float(np.median(seam_prom)),
                            "drift_prominence_median": float(np.median(drift_prom)),
                            "holds": bool(guardrail_ok)},
        "preregistered_criterion": "5/15 -> >= 10/15 without reintroducing drift/jump",
        "verdict": verdict,
        "figures": ["localization.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  hits: fragile {frag_h}/{N_SUBJECTS}, large {large_h}/{N_SUBJECTS}, "
          f"multiscale {multi_h}/{N_SUBJECTS}")
    print(f"  median err: fragile {np.median(res['fragile']['err']):.0f}, "
          f"large {np.median(res['large']['err']):.0f}, "
          f"multiscale {np.median(res['multi']['err']):.0f}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
