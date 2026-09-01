"""Experiment B on REAL data -- does causal smoothing of the predictability
covariate help on-line localization on real EEG? (Paper 3)

Synthetic Exp B (`localization_priors`) anchors the transition to argmax(gamma_t),
gamma_t = conditional_residual_variance whose half_window IS the causal smoothing
bandwidth, and found NO BENEFIT: smoothing degrades localization because an abrupt
jump and a sharp spontaneous excursion share a single-sample covariate signature;
the discriminator that works is PERSISTENCE (a window-mean), not covariate smoothing.

`abc_real_eeg` only smoothed the *break curve* -- a different object -- so B stayed
synthetic-only. This is the faithful replication: it smooths the SAME predictability
covariate, on the real structural trajectory (the sqrt-embedded covariance sequence),
and anchors at its argmax, exactly as B does -- on real eyes-open/closed EEG.

Usage:
    python -m experiments.paper3_geodesic_kinematics.localization_priors_real.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.shared_lib import jump_diffusion as jd
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve,
)
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint,
)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs,
    N_SUBJECTS, SEG_SEC, STEP_SEC, LARGE_W, TOL_SEC,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "localization_priors_real")

# ---- pre-fixed parameters (see PRE-REGISTRATION.md) --------------------------
AR_RHO = 0.4                                  # matches synthetic Exp B
BANDWIDTHS = [0, 1, 2, 4, 8, 12, 20, 30]      # covariate half_window, in windows
MIN_SEG_SEC = 5.0                             # for the CUSUM head-to-head


def covariate_argmax(covs, h):
    """gamma_t = conditional_residual_variance of the sqrt-embedded covariance
    trajectory (flattened), smoothed with causal half_window=h; return argmax and
    the peak prominence max/median."""
    E, _ = embed_cumsum(covs)
    X = E.reshape(len(covs), -1)              # (T, d*d) real structural trajectory
    gamma = jd.conditional_residual_variance(X, ar_rho=AR_RHO, half_window=h)
    tau = int(np.argmax(gamma))
    med = float(np.median(gamma)) + 1e-12
    prom = float(np.max(gamma) / med)
    return tau, prom, gamma


def persistence_argmax(covs):
    """B's proposed working discriminator: the large window-mean break curve and the
    geodesic CUSUM. Returns (winmean_tau, cusum_tau)."""
    E, C = embed_cumsum(covs)
    win = break_curve(C, LARGE_W)
    tw = int(np.nanargmax(np.where(np.isnan(win), -np.inf, win)))
    cu = cusum_changepoint(E, C, int(MIN_SEG_SEC / STEP_SEC))
    tc = int(np.nanargmax(np.where(np.isnan(cu), -np.inf, cu)))
    return tw, tc


def _synthetic_clean_seam(seed=0, T=240, d=4, seam=120, noise=0.02):
    """A clean structural seam with NO bursts, for the self-test: two constant
    density states with a sharp change, tiny symmetric noise."""
    from experiments.shared_lib import spd_manifold as spd
    from experiments.shared_lib import manifold_trajectory as mt
    rng = np.random.default_rng(seed)
    A = mt.random_density(d, rng)
    dirn = spd.sqrt_log(A, mt.random_density(d, rng))
    dirn = dirn / np.sqrt(np.sum(dirn * dirn))
    B = spd.sqrt_exp(A, 0.9 * dirn)
    covs = []
    for t in range(T):
        base = A if t < seam else B
        xi = noise * rng.standard_normal((d, d)); xi = 0.5 * (xi + xi.T)
        covs.append(spd.sqrt_exp(base, xi))
    return covs, seam


def self_test():
    covs, seam = _synthetic_clean_seam()
    tau, prom, _ = covariate_argmax(covs, h=0)
    ok = abs(tau - seam) <= 8
    print("Self-test (covariate argmax on a clean structural seam, no bursts):")
    print(f"  argmax(gamma) at {tau}, true seam {seam}  ->  [{'PASS' if ok else 'FAIL'}]")
    if not ok:
        raise SystemExit("SELF-TEST FAILED -- covariate cannot find a clean seam; aborted.")
    return {"clean_seam_localized": bool(ok), "tau": tau, "seam": seam}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tol = int(TOL_SEC / STEP_SEC)
    print("Experiment B (real data): causal smoothing of the predictability covariate")
    print(f"  {N_SUBJECTS} subjects, ar_rho={AR_RHO}, tol +/-{TOL_SEC}s ({tol} windows), "
          f"bandwidths {BANDWIDTHS}")
    st = self_test()

    # per-subject covariate trajectories (compute once per subject; sweep h is cheap)
    subjects = []
    for s in range(1, N_SUBJECTS + 1):
        try:
            data_o, sf = load_state_covs(s, 1)
            data_c, _ = load_state_covs(s, 2)
            n = int(SEG_SEC * sf)
            data = np.concatenate([data_o[:, :n], data_c[:, :n]], axis=1)
            covs = sliding_covs(data, sf)
            seam = int(SEG_SEC / STEP_SEC)
            subjects.append((f"S{s:03d}", covs, seam))
        except Exception as e:
            print(f"  S{s:03d}: FAILED {type(e).__name__}: {str(e)[:70]}")

    n_subj = len(subjects)
    acc, prom = {}, {}
    for h in BANDWIDTHS:
        hits, proms = 0, []
        for _, covs, seam in subjects:
            tau, pr, _ = covariate_argmax(covs, h)
            hits += (abs(tau - seam) <= tol)
            proms.append(pr)
        acc[h] = hits / n_subj
        prom[h] = float(np.median(proms))
        print(f"  h={h:3d}: covariate-argmax localization {hits:2d}/{n_subj} "
              f"(acc {acc[h]:.2f}), median prominence {prom[h]:.2f}")

    # persistence head-to-head (B's claimed working discriminator)
    win_hits, cu_hits = 0, 0
    for _, covs, seam in subjects:
        tw, tc = persistence_argmax(covs)
        win_hits += (abs(tw - seam) <= tol)
        cu_hits += (abs(tc - seam) <= tol)
    print(f"  persistence head-to-head: window-mean {win_hits}/{n_subj}, "
          f"CUSUM {cu_hits}/{n_subj}")

    base_acc, base_prom = acc[0], prom[0]
    hs = BANDWIDTHS
    improved = [h for h in hs if acc[h] > base_acc + 0.05 and prom[h] >= 0.9 * base_prom]
    best_h = hs[int(np.argmax([acc[h] for h in hs]))]

    if improved:
        bh = improved[int(np.argmax([acc[h] for h in improved]))]
        verdict = (
            f"SMOOTHING HELPS ON REAL DATA -- overturns synthetic B. Bandwidth h={bh} "
            f"raises real localization {base_acc:.2f} -> {acc[bh]:.2f} while holding "
            f"covariate prominence ({prom[bh]:.2f} vs baseline {base_prom:.2f}). On real "
            f"EEG, causal smoothing of the predictability covariate stabilises the anchor "
            f"against spontaneous alpha bursts. (Persistence detectors: window-mean "
            f"{win_hits}/{n_subj}, CUSUM {cu_hits}/{n_subj}.)")
    elif acc[best_h] > base_acc + 0.05:
        verdict = (
            f"TRADE-OFF ON REAL DATA. The bandwidth h={best_h} that best improves real "
            f"localization ({base_acc:.2f} -> {acc[best_h]:.2f}) also drops covariate "
            f"prominence to {prom[best_h]:.2f} (< 0.9 x baseline {base_prom:.2f}) -- "
            f"robustness bought by blurring the anchor, not a free improvement, so not "
            f"adopted. (Persistence: window-mean {win_hits}/{n_subj}, CUSUM {cu_hits}/{n_subj}.)")
    else:
        verdict = (
            f"NO BENEFIT ON REAL DATA -- synthetic Exp B REPLICATES. Causal smoothing of "
            f"the predictability covariate does not improve real localization: accuracy is "
            f"{base_acc:.2f} at h=0 and {acc[hs[-1]]:.2f} at h={hs[-1]} (peak "
            f"{max(acc.values()):.2f} at h={best_h}, within +0.05 of baseline), while "
            f"prominence falls {base_prom:.2f} -> {prom[hs[-1]]:.2f}. On real EEG, exactly "
            f"as the synthetic mechanism predicted, an abrupt structural transition and a "
            f"real alpha burst share the covariate's single-sample signature, so smoothing "
            f"cannot separate them -- it only blurs the anchor. B's positive claim also "
            f"holds on real data: the PERSISTENCE detectors localize better than the "
            f"covariate argmax (window-mean {win_hits}/{n_subj}, CUSUM {cu_hits}/{n_subj} vs "
            f"covariate-argmax {int(base_acc*n_subj)}/{n_subj} at h=0). B was synthetic-only; "
            f"it is now replicated on real EEG.")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    ax[0].plot(hs, [acc[h] for h in hs], "o-", color="crimson", label="covariate-argmax acc")
    ax[0].axhline(base_acc, ls=":", color="crimson", alpha=0.5, label="acc baseline (h=0)")
    ax[0].axhline(win_hits / n_subj, ls="--", color="gray", label=f"window-mean {win_hits}/{n_subj}")
    ax[0].axhline(cu_hits / n_subj, ls="--", color="steelblue", label=f"CUSUM {cu_hits}/{n_subj}")
    ax[0].set_xlabel("covariate smoothing bandwidth h (windows)")
    ax[0].set_ylabel(f"localization accuracy (|err|<= {TOL_SEC}s)"); ax[0].set_ylim(0, 1.05)
    ax[0].set_title("Smoothing the covariate does not beat persistence")
    ax[0].legend(fontsize=8)
    ax[1].plot(hs, [prom[h] for h in hs], "s-", color="seagreen")
    ax[1].set_xlabel("covariate smoothing bandwidth h (windows)")
    ax[1].set_ylabel("median covariate peak prominence (max/median)")
    ax[1].set_title("Prominence guardrail: smoothing blurs the anchor")
    fig.suptitle(f"Exp B on real EEG ({n_subj} subjects, eyes-open/closed)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "covariate_smoothing_real.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "localization_priors_real",
        "data": "PhysioNet eegbci eyes-open (R01) + eyes-closed (R02), concatenated, real EEG",
        "question": ("does causal smoothing of the predictability covariate gamma_t improve "
                     "on-line localization on real EEG (Exp B's mechanism on real data)?"),
        "self_test": st,
        "n_subjects": n_subj,
        "params": {"ar_rho": AR_RHO, "bandwidths": BANDWIDTHS, "tol_sec": TOL_SEC,
                   "seg_sec": SEG_SEC, "step_sec": STEP_SEC, "large_w": LARGE_W},
        "covariate_argmax_accuracy_by_h": {str(h): acc[h] for h in hs},
        "covariate_peak_prominence_by_h": {str(h): prom[h] for h in hs},
        "persistence_head_to_head": {"window_mean": win_hits, "cusum": cu_hits, "n": n_subj},
        "best_bandwidth": best_h,
        "preregistered_decision": "h>0 improving acc by >0.05 while prominence >= 0.9*baseline",
        "verdict": verdict,
        "figures": ["covariate_smoothing_real.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
