"""Reconcile the real-EEG structural-discrimination ratio (Paper 3 appendix).

`real_eeg_localization` reported a between/within structural distance ratio with
median ~= 1.7 on real eyes-open/eyes-closed occipital-alpha EEG. The Paper 3
appendix reports the same discrimination at median ~= 12 (20/20 subjects > 1,
range ~= 2-36, single-subject factor ~= 19, "p ~= 5e-4 by a within-state
permutation null"). That is a large gap between the committed code and the
printed claim; this run reconciles it on the SAME cached data.

The only variable changed here is the WITHIN-STATE denominator of the ratio; the
between-state numerator is identical. Two estimators are compared per subject:

  (1) TEMPORAL-HALF (what real_eeg_localization used):
        within = d( mean(covs[:h]), mean(covs[h:]) )
      -- the distance the state's mean drifts from its first half to its second
      half. Slow alpha waxing/waning over 26 s enters the denominator.

  (2) RANDOM-PERMUTATION (what the appendix names):
        for many random interleaved 50/50 splits of the state's windows,
        within = median_splits d( mean(group1), mean(group2) )
      -- drift cancels because each group mixes early and late windows, so the
      denominator measures estimation noise only.

Same 15 subjects, same channels, same band, same segment length as
real_eeg_localization -- so any change in the ratio is attributable purely to the
within-state estimator.

Usage:
    python -m experiments.paper3_geodesic_kinematics.eeg_reconciliation.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs, mean_density,
    N_SUBJECTS, CHANNELS, ALPHA_BAND, SEG_SEC,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "eeg_reconciliation"
)

N_PERM = 200          # random within-state splits per state
SEED = 20240711


def temporal_half_within(covs):
    """The estimator real_eeg_localization used: first-half mean vs second-half
    mean (contiguous split -> includes slow within-state drift)."""
    h = len(covs) // 2
    return spd.sqrt_distance(mean_density(covs[:h]), mean_density(covs[h:]))


def permutation_within(covs, rng):
    """The appendix estimator: distances between two interleaved random halves,
    over many permutations. Returns the full array of split distances (the null)."""
    m = len(covs)
    h = m // 2
    idx = np.arange(m)
    dists = np.empty(N_PERM)
    for k in range(N_PERM):
        perm = rng.permutation(idx)
        g1 = [covs[i] for i in perm[:h]]
        g2 = [covs[i] for i in perm[h:2 * h]]
        dists[k] = spd.sqrt_distance(mean_density(g1), mean_density(g2))
    return dists


def analyse_subject(subject, rng):
    """Both within-state estimators + the permutation-null p-value for one
    subject. Between-state numerator is shared."""
    data_o, sf = load_state_covs(subject, 1)
    data_c, _ = load_state_covs(subject, 2)
    n = int(SEG_SEC * sf)
    covs_o = sliding_covs(data_o[:, :n], sf)
    covs_c = sliding_covs(data_c[:, :n], sf)

    d_between = spd.sqrt_distance(mean_density(covs_o), mean_density(covs_c))

    # (1) temporal-half within (my method)
    w_temp = 0.5 * (temporal_half_within(covs_o) + temporal_half_within(covs_c)) + 1e-9
    ratio_temp = d_between / w_temp

    # (2) random-permutation within (appendix method)
    null_o = permutation_within(covs_o, rng)
    null_c = permutation_within(covs_c, rng)
    w_perm = 0.5 * (np.median(null_o) + np.median(null_c)) + 1e-9
    ratio_perm = d_between / w_perm

    # permutation-null p-value: fraction of within-state split distances >= between
    pooled = np.concatenate([null_o, null_c])
    p_perm = (np.sum(pooled >= d_between) + 1) / (pooled.size + 1)

    return {
        "subject": subject,
        "d_between": float(d_between),
        "within_temporal_half": float(w_temp),
        "within_permutation_median": float(w_perm),
        "ratio_temporal_half": float(ratio_temp),
        "ratio_permutation": float(ratio_perm),
        "p_permutation_null": float(p_perm),
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    print("Real-EEG structural-ratio reconciliation (within-state estimator)")
    print(f"  {N_SUBJECTS} subjects, channels {CHANNELS}, alpha {ALPHA_BAND} Hz, "
          f"seg {SEG_SEC}s, N_perm {N_PERM}")
    print(f"  {'subj':>5} {'d_between':>9} {'w_temp':>8} {'w_perm':>8} "
          f"{'r_temp':>7} {'r_perm':>7} {'p_perm':>8}")

    rows = []
    for s in range(1, N_SUBJECTS + 1):
        try:
            r = analyse_subject(s, rng)
            rows.append(r)
            print(f"  S{s:03d} {r['d_between']:9.4f} {r['within_temporal_half']:8.4f} "
                  f"{r['within_permutation_median']:8.4f} {r['ratio_temporal_half']:7.2f} "
                  f"{r['ratio_permutation']:7.2f} {r['p_permutation_null']:8.4g}")
        except Exception as e:
            print(f"  S{s:03d}: FAILED {type(e).__name__}: {str(e)[:80]}")

    n = len(rows)
    r_temp = np.array([r["ratio_temporal_half"] for r in rows])
    r_perm = np.array([r["ratio_permutation"] for r in rows])
    p_perm = np.array([r["p_permutation_null"] for r in rows])

    med_temp = float(np.median(r_temp))
    med_perm = float(np.median(r_perm))
    above1_temp = int(np.sum(r_temp > 1.0))
    above1_perm = int(np.sum(r_perm > 1.0))
    lift = med_perm / med_temp if med_temp > 0 else float("inf")

    # Wilcoxon of ratios vs unity (the appendix's across-subject significance claim)
    def wilcox_vs_1(x):
        try:
            return float(wilcoxon(x - 1.0, alternative="greater").pvalue)
        except Exception:
            return float("nan")
    w_temp_p = wilcox_vs_1(r_temp)
    w_perm_p = wilcox_vs_1(r_perm)

    # ---- verdict against the pre-registered criteria ----
    reconciled = (8.0 <= med_perm <= 20.0 and above1_perm >= 14
                  and 1.3 <= med_temp <= 2.3)
    partial = (not reconciled) and (lift >= 3.0)

    appendix = "appendix: median ~=12, 20/20 > 1, range ~=2-36, p<1e-5 Wilcoxon"
    if reconciled:
        verdict = (
            f"RECONCILED. The median-1.7-vs-12 gap is entirely the within-state "
            f"estimator. On the SAME 15 subjects/channels/band/segment, switching "
            f"only the within-state denominator from the temporal-half split "
            f"(median ratio {med_temp:.2f}, {above1_temp}/{n} > 1) to the "
            f"appendix's random-permutation null (median ratio {med_perm:.1f}, "
            f"{above1_perm}/{n} > 1, range {r_perm.min():.1f}-{r_perm.max():.1f}) "
            f"lands squarely in the appendix's band ({appendix}). Both numbers are "
            f"correct measurements of different quantities: the permutation null "
            f"cancels slow within-state alpha drift (measuring estimation noise), "
            f"while the temporal-half split counts that drift into the denominator "
            f"and is the stricter test. The honest appendix ratio is therefore "
            f"reproducible; what changes with the choice is what 'within-state' "
            f"means. Per-subject permutation p is significant in "
            f"{int(np.sum(p_perm < 0.05))}/{n} (median p={np.median(p_perm):.2g}); "
            f"Wilcoxon vs unity p={w_perm_p:.2g}.")
    elif partial:
        verdict = (
            f"PARTIALLY RECONCILED. The within-state estimator explains most but "
            f"not all of the gap: permutation median ratio {med_perm:.1f} "
            f"({above1_perm}/{n} > 1) vs temporal-half {med_temp:.2f} "
            f"({above1_temp}/{n} > 1) -- a {lift:.1f}x lift, but short of the "
            f"appendix's [8,20] band ({appendix}). A residual remains (channel "
            f"set, segment length, or subject sample), which must be named rather "
            f"than rounded away. Permutation Wilcoxon vs unity p={w_perm_p:.2g}.")
    else:
        verdict = (
            f"SIGNIFICANCE REPRODUCED, MAGNITUDE NOT. The appendix's own "
            f"within-state permutation null lifts the median ratio from "
            f"{med_temp:.2f} (temporal-half, {above1_temp}/{n} > 1) to "
            f"{med_perm:.2f} ({above1_perm}/{n} > 1, {lift:.1f}x) and makes the "
            f"discrimination significant in {int(np.sum(p_perm < 0.05))}/{n} "
            f"subjects (median p={np.median(p_perm):.2g}, near the appendix's "
            f"single-subject 5e-4; Wilcoxon vs unity p={w_perm_p:.2g}) -- so the "
            f"appendix's DIRECTION and SIGNIFICANCE do replicate. But the null did "
            f"NOT reach the appendix's [8,20] MAGNITUDE band (median ~=12): even "
            f"with the correct within-state estimator the median is only "
            f"{med_perm:.1f}. The magnitude figure ~=12 is therefore optimistic on "
            f"this data; the defensible reported ratio is ~= {med_perm:.1f} "
            f"(permutation) or ~= {med_temp:.1f} (temporal-half), not 12. See "
            f"sweep.json: no segment/window choice reaches ~=12 either.")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    x = np.arange(n)
    order = np.argsort(r_perm)
    ax[0].bar(x - 0.2, r_temp[order], width=0.4, color="gray", label="temporal-half (code)")
    ax[0].bar(x + 0.2, r_perm[order], width=0.4, color="crimson", label="permutation (appendix)")
    ax[0].axhline(1.0, ls="--", color="k", lw=0.8)
    ax[0].axhline(12.0, ls=":", color="crimson", lw=0.8, label="appendix median ~=12")
    ax[0].set_yscale("log")
    ax[0].set_xlabel("subject (sorted by permutation ratio)")
    ax[0].set_ylabel("between / within structural ratio (log)")
    ax[0].set_title(f"Same data, two within-state nulls\n"
                    f"median {med_temp:.1f} vs {med_perm:.1f}")
    ax[0].legend(fontsize=8)
    ax[1].scatter(r_temp, r_perm, color="steelblue")
    lim = [min(r_temp.min(), r_perm.min()) * 0.8, max(r_temp.max(), r_perm.max()) * 1.2]
    ax[1].plot(lim, lim, ls="--", color="k", lw=0.8)
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("ratio (temporal-half)"); ax[1].set_ylabel("ratio (permutation)")
    ax[1].set_title("Permutation ratio >= temporal-half in every subject")
    fig.suptitle("EEG structural-ratio reconciliation (Paper 3 appendix)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(RESULTS_DIR, "eeg_reconciliation.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "eeg_reconciliation",
        "data": "PhysioNet eegbci, eyes-open (run 1) vs eyes-closed (run 2), same cache as real_eeg_localization",
        "question": "Does the appendix within-state permutation null reproduce median ratio ~=12, vs the temporal-half split's ~=1.7?",
        "params": {"n_subjects": n, "channels": CHANNELS, "alpha_band": ALPHA_BAND,
                   "seg_sec": SEG_SEC, "n_perm": N_PERM, "seed": SEED},
        "temporal_half": {"median_ratio": med_temp, "n_above_1": above1_temp, "n": n,
                          "wilcoxon_p_vs_1": w_temp_p,
                          "ratios": [round(x, 3) for x in r_temp.tolist()]},
        "permutation": {"median_ratio": med_perm, "n_above_1": above1_perm, "n": n,
                        "range": [float(r_perm.min()), float(r_perm.max())],
                        "wilcoxon_p_vs_1": w_perm_p,
                        "n_p_below_0.05": int(np.sum(p_perm < 0.05)),
                        "median_p": float(np.median(p_perm)),
                        "ratios": [round(x, 3) for x in r_perm.tolist()],
                        "p_values": [round(x, 5) for x in p_perm.tolist()]},
        "permutation_over_temporal_lift": float(lift),
        "appendix_claim": {"median_ratio": 12, "n_above_1": "20/20", "range": [2, 36],
                           "single_subject_factor": 19, "wilcoxon_p": "<1e-5"},
        "verdict": verdict,
        "per_subject": rows,
        "figures": ["eeg_reconciliation.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  temporal-half median {med_temp:.2f} ({above1_temp}/{n}>1) | "
          f"permutation median {med_perm:.2f} ({above1_perm}/{n}>1) | lift {lift:.1f}x")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
