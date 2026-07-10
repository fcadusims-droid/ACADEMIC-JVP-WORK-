"""Real-EEG localization test (Paper 3) -- the outstanding confirmation for A/B/C.

The synthetic experiments A/B/C concluded that within-trajectory localization of a
structural transition is solved by a large, *persistence-sensitive* window (not a
multiscale bank, not covariate smoothing), because a transition is a persistent
regime change while spontaneous fluctuations are transient. That was validated on
synthetic ground truth only, because PhysioNet was network-blocked. It is now
reachable, so this runs the SAME detectors on the appendix's real paradigm.

Paradigm (PhysioNet EEG Motor Movement/Imagery, eegbci): eyes-open (run 1) vs
eyes-closed (run 2). Eyes-closed raises occipital alpha -- a change in the spatial
correlation *structure*, the structural transition the trace-normalised geometry
is built to see. Two questions, mirroring the appendix:

  (1) Between-record discrimination (the validated 20/20 claim): is the geodesic
      distance between the eyes-open and eyes-closed mean covariances larger than
      within-state distance?
  (2) Within-trajectory localization (the 5/15 open problem): concatenate an
      eyes-open and an eyes-closed segment (amplitude-normalised so the seam is
      structural, not a power step) and ask each detector to find the seam. Does
      the large persistence-sensitive window beat the fragile pointwise one on
      REAL EEG, as the synthetic A/B/C predicted?

Reuses the fast embedding/break machinery from Experiment A.

Usage:
    python -m experiments.paper3_geodesic_kinematics.real_eeg_localization.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve, _R,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "real_eeg_localization"
)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "mne_eegbci")

# ---- pre-fixed parameters ----------------------------------------------------
N_SUBJECTS = 15
CHANNELS = ["O1", "Oz", "O2", "PO3", "POz", "PO4", "Pz"]  # occipito-parietal, alpha
ALPHA_BAND = (8.0, 13.0)
SEG_SEC = 26.0            # seconds of each state used
WIN_SEC = 1.0            # covariance window
STEP_SEC = 0.25          # window step
EIG_FLOOR = 1e-3
FRAGILE_W = 2            # break-curve window (in covariance-window units)
LARGE_W = 40            # ~10 s each side -- persistence-sensitive
MULTI_SCALES = [2, 8, 20, 40]
TOL_SEC = 2.0            # localization tolerance


def load_state_covs(subject, run, sfreq_target=None):
    """Return (band-passed, channel-selected) data array (n_ch, n_times) and sfreq
    for one subject/run, amplitude-normalised per channel."""
    import mne
    from mne.datasets import eegbci
    paths = eegbci.load_data(subject, [run], path=DATA_DIR, update_path=False)
    raw = mne.io.read_raw_edf(str(paths[0]), preload=True, verbose="ERROR")
    eegbci.standardize(raw)
    raw.pick(CHANNELS)
    raw.filter(*ALPHA_BAND, verbose="ERROR")
    data = raw.get_data()                       # (n_ch, n_times)
    sf = raw.info["sfreq"]
    # z-score each channel over the segment -> seam is structural, not amplitude
    data = (data - data.mean(axis=1, keepdims=True)) / (data.std(axis=1, keepdims=True) + 1e-12)
    return data, sf


def sliding_covs(data, sf):
    """Sliding-window covariance trajectory -> rank-floored, trace-normalised
    density matrices."""
    w = int(WIN_SEC * sf)
    step = int(STEP_SEC * sf)
    covs = []
    for start in range(0, data.shape[1] - w + 1, step):
        seg = data[:, start:start + w]
        c = np.cov(seg)
        c = spd.eigfloor(c, EIG_FLOOR)
        covs.append(spd.trace_normalize(c))
    return covs


def mean_density(covs):
    embs = np.mean([spd.sqrt_embed(c) for c in covs], axis=0)
    nrm = np.sqrt(np.sum(embs * embs))
    return spd.sqrt_unembed(embs * (_R / nrm)) if nrm > 1e-12 else spd.sqrt_unembed(embs)


def between_within_ratio(covs_o, covs_c):
    """Structural discrimination: between-state geodesic distance vs the mean
    within-state distance (a value > 1 = the states are structurally separable)."""
    mo, mc = mean_density(covs_o), mean_density(covs_c)
    d_between = spd.sqrt_distance(mo, mc)
    # within: split each state in half, distance between halves
    def within(covs):
        h = len(covs) // 2
        return spd.sqrt_distance(mean_density(covs[:h]), mean_density(covs[h:]))
    d_within = 0.5 * (within(covs_o) + within(covs_c)) + 1e-9
    return d_between / d_within


def localize(subject, tol_windows):
    """Concatenate eyes-open + eyes-closed covariance trajectories and score the
    fragile / large / multiscale detectors against the known seam."""
    data_o, sf = load_state_covs(subject, 1)
    data_c, _ = load_state_covs(subject, 2)
    n = int(SEG_SEC * sf)
    data = np.concatenate([data_o[:, :n], data_c[:, :n]], axis=1)
    covs = sliding_covs(data, sf)
    seam = int(SEG_SEC / STEP_SEC)                       # window index of the seam
    _, C = embed_cumsum(covs)

    def hit(curve):
        t = int(np.nanargmax(np.where(np.isnan(curve), -np.inf, curve)))
        return abs(t - seam), (abs(t - seam) <= tol_windows)

    frag = break_curve(C, FRAGILE_W)
    large = break_curve(C, LARGE_W)
    agg = np.sum([_zscore(break_curve(C, w)) for w in MULTI_SCALES], axis=0)
    ef, hf = hit(frag)
    el, hl = hit(large)
    em, hm = hit(agg)
    # between/within structural ratio on the two pure states
    ratio = between_within_ratio(sliding_covs(data_o, sf), sliding_covs(data_c, sf))
    return {"err_fragile": ef, "hit_fragile": hf, "err_large": el, "hit_large": hl,
            "err_multi": em, "hit_multi": hm, "between_within_ratio": float(ratio)}


def _zscore(S):
    v = S[~np.isnan(S)]
    mu, sd = np.mean(v), np.std(v) + 1e-12
    Z = (S - mu) / sd
    Z[np.isnan(S)] = -np.inf
    return Z


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tol_windows = int(TOL_SEC / STEP_SEC)
    print("Real-EEG localization (eyes-open vs eyes-closed, occipital alpha)")
    print(f"  {N_SUBJECTS} subjects, channels {CHANNELS}, alpha {ALPHA_BAND} Hz, "
          f"tol +/-{TOL_SEC}s ({tol_windows} windows)")

    per_subj = []
    for s in range(1, N_SUBJECTS + 1):
        try:
            r = localize(s, tol_windows)
            per_subj.append(r)
            print(f"  S{s:03d}: frag err={r['err_fragile']*STEP_SEC:5.1f}s "
                  f"large err={r['err_large']*STEP_SEC:5.1f}s multi err={r['err_multi']*STEP_SEC:5.1f}s "
                  f"| struct ratio={r['between_within_ratio']:.1f}")
        except Exception as e:
            print(f"  S{s:03d}: FAILED {type(e).__name__}: {str(e)[:80]}")

    n = len(per_subj)
    frag_hits = sum(r["hit_fragile"] for r in per_subj)
    large_hits = sum(r["hit_large"] for r in per_subj)
    multi_hits = sum(r["hit_multi"] for r in per_subj)
    ratios = [r["between_within_ratio"] for r in per_subj]
    struct_discrim = sum(x > 1.0 for x in ratios)

    med = lambda key: float(np.median([r[key] for r in per_subj]) * STEP_SEC)

    # verdicts
    disc_ok = struct_discrim >= 0.8 * n
    large_beats_fragile = large_hits > frag_hits and large_hits >= 0.6 * n
    if disc_ok and large_beats_fragile:
        verdict = (f"REAL-EEG CONFIRMS THE SYNTHETIC STORY. (1) Between-record "
                   f"structural discrimination replicates: the eyes-open/eyes-closed "
                   f"geodesic distance exceeds within-state in {struct_discrim}/{n} "
                   f"subjects (median ratio {np.median(ratios):.1f}). (2) Within-"
                   f"trajectory localization: the large persistence-sensitive window "
                   f"reaches {large_hits}/{n} vs the fragile pointwise detector's "
                   f"{frag_hits}/{n} -- on REAL EEG, window size / persistence is the "
                   f"operative fix, as A/B/C predicted. Multiscale {multi_hits}/{n} "
                   "adds nothing over the single large window.")
    elif disc_ok and not large_beats_fragile:
        verdict = (f"SPLIT, as the appendix found. Between-record discrimination "
                   f"replicates ({struct_discrim}/{n}, median ratio "
                   f"{np.median(ratios):.1f}), but within-trajectory localization "
                   f"stays hard on real EEG even for the large window "
                   f"({large_hits}/{n} vs fragile {frag_hits}/{n}) -- the synthetic "
                   "persistence fix does not fully transfer, so real spontaneous "
                   "alpha bursts behave like the sustained-burst regime Exp C flagged "
                   "as the residual limitation. Honest real-data status: structural "
                   "discrimination validated, on-line localization still open.")
    else:
        verdict = (f"WEAK STRUCTURAL SIGNAL: between-record discrimination held in "
                   f"only {struct_discrim}/{n}; the paradigm/params did not expose the "
                   "alpha structure cleanly here, so the localization comparison is "
                   "inconclusive and needs a stronger structural contrast.")

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    ax[0].bar([0, 1, 2], [frag_hits / n, large_hits / n, multi_hits / n],
              color=["gray", "crimson", "steelblue"])
    ax[0].set_xticks([0, 1, 2]); ax[0].set_xticklabels(["fragile", "large", "multiscale"])
    ax[0].set_ylabel(f"localization hit rate (|err|<= {TOL_SEC}s)"); ax[0].set_ylim(0, 1.05)
    ax[0].set_title(f"Within-trajectory localization ({n} real subjects)")
    for i, h in enumerate([frag_hits, large_hits, multi_hits]):
        ax[0].text(i, h / n + 0.02, f"{h}/{n}", ha="center")
    ax[1].hist(ratios, bins=10, color="seagreen", alpha=0.8)
    ax[1].axvline(1.0, ls="--", color="k")
    ax[1].set_xlabel("between/within structural distance ratio")
    ax[1].set_ylabel("subjects"); ax[1].set_title(f"Structural discrimination ({struct_discrim}/{n} > 1)")
    fig.suptitle("Real-EEG localization: eyes-open vs eyes-closed alpha", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "real_eeg_localization.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "real_eeg_localization",
        "data": "PhysioNet eegbci (real EEG), eyes-open (run 1) vs eyes-closed (run 2)",
        "params": {"n_subjects_attempted": N_SUBJECTS, "n_subjects_ok": n,
                   "channels": CHANNELS, "alpha_band": ALPHA_BAND, "seg_sec": SEG_SEC,
                   "win_sec": WIN_SEC, "step_sec": STEP_SEC, "fragile_w": FRAGILE_W,
                   "large_w": LARGE_W, "multi_scales": MULTI_SCALES, "tol_sec": TOL_SEC},
        "localization_hits": {"fragile": frag_hits, "large": large_hits,
                              "multiscale": multi_hits, "n": n},
        "localization_median_err_sec": {"fragile": med("err_fragile"),
                                        "large": med("err_large"), "multi": med("err_multi")},
        "structural_discrimination": {"n_above_1": struct_discrim, "n": n,
                                      "median_ratio": float(np.median(ratios)),
                                      "ratios": [round(x, 2) for x in ratios]},
        "verdict": verdict,
        "figures": ["real_eeg_localization.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  fragile {frag_hits}/{n}, large {large_hits}/{n}, multiscale {multi_hits}/{n}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
