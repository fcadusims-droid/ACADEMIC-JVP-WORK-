"""Experiment H -- Statistical power of the dissociation test (Paper 2, Sec 14.1).

Simulation cannot confirm CBRA; it can only say whether the M_diss design is
feasible. The identity-linkage dissociation contrasts an identity-linked channel
against a generic structured process: under the identity-linked hypothesis a
macro-invariant is PRESERVED through the transition in the identity-matched
condition (S^{I+}) but NOT in the mismatched condition (S^{I-}); a generic
structured process shows no such identity-conditional dissociation.

Modelled as an interaction: the preservation score (pre->post change of the
macro-invariant) differs between S^{I+} and S^{I-} by an effect delta under the
identity-linked hypothesis, and by 0 under the generic hypothesis. Imperfect
matching between the two conditions injects a per-experiment confound that both
lowers power and, uncontrolled, inflates the false-positive rate.

Sweep sample size (per condition) x effect size (SNR = delta/sigma) x matching
quality, and report the power to distinguish the two hypotheses. The deliverable
is a feasibility verdict against realistic experimental-anesthesiology sample
sizes -- NOT a biological result.

Usage:
    python -m experiments.paper2_cbra_protocol.dissociation_power_analysis.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "dissociation_power_analysis"
)

# ---- pre-fixed grid ----------------------------------------------------------
SAMPLE_SIZES = [5, 10, 20, 40, 80]           # per condition
SNRS = [0.3, 0.5, 0.8, 1.2]                  # Cohen's d = delta / sigma
MATCHINGS = [0.0, 0.3, 0.6]                  # confound sd (fraction of sigma)
N_EXP = 3000
ALPHA = 0.05
REALISTIC_N = 20                              # typical anesthesiology per-group n


def one_experiment(n, snr, matching, delta_true, rng):
    """Return the interaction test p-value for one simulated experiment."""
    confound = rng.normal(0, matching)               # per-experiment mismatch
    ip = rng.normal(0.0, 1.0, n)                      # S^{I+}: invariant preserved
    im = rng.normal(delta_true + confound, 1.0, n)   # S^{I-}: not preserved (+delta)
    # two-sample t-test on the preservation score (interaction contrast)
    _, p = stats.ttest_ind(im, ip)
    return p


def power_at(n, snr, matching, rng, delta_true=None):
    delta = snr if delta_true is None else delta_true
    rejects = 0
    for _ in range(N_EXP):
        p = one_experiment(n, snr, matching, delta, rng)
        rejects += (p < ALPHA)
    return rejects / N_EXP


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment H: dissociation-test power analysis")
    rng = np.random.default_rng(0)

    # power grids, one per matching level
    grids = {}
    fpr = {}
    for m in MATCHINGS:
        G = np.zeros((len(SNRS), len(SAMPLE_SIZES)))
        for i, snr in enumerate(SNRS):
            for j, n in enumerate(SAMPLE_SIZES):
                G[i, j] = power_at(n, snr, m, rng)
        grids[m] = G
        # false-positive rate under H0 (delta=0) at the realistic n, mid SNR slot
        fpr[m] = power_at(REALISTIC_N, 0.0, m, rng, delta_true=0.0)
        print(f"  matching sd={m}: FPR@H0={fpr[m]:.3f}")

    # find, per matching, the smallest n reaching 80% power at each SNR
    def min_n_for_power(G, target=0.8):
        out = {}
        for i, snr in enumerate(SNRS):
            idx = np.where(G[i] >= target)[0]
            out[snr] = (SAMPLE_SIZES[idx[0]] if len(idx) else None)
        return out

    feasible = {}
    for m in MATCHINGS:
        feasible[m] = min_n_for_power(grids[m])
        print(f"  matching sd={m}: min n for 80% power by SNR: {feasible[m]}")

    # verdict: is 80% power reachable at a realistic n (<= ~40) for a plausible
    # effect (SNR ~ 0.5-0.8) under realistic matching (sd ~ 0.3)?
    realistic_matching = 0.3
    plausible_snr = 0.8
    n_needed = feasible[realistic_matching].get(plausible_snr)
    fpr_ok = fpr[realistic_matching] < 0.10
    if n_needed is not None and n_needed <= 40 and fpr_ok:
        verdict = (f"FEASIBLE: at a moderate effect (SNR={plausible_snr}) and "
                   f"realistic matching (sd={realistic_matching}), 80% power is "
                   f"reached at n={n_needed} per condition -- within experimental-"
                   f"anesthesiology reach. FPR stays controlled ({fpr[realistic_matching]:.2f}). "
                   "The dissociation design is statistically executable.")
    elif n_needed is not None and n_needed <= 100:
        verdict = (f"MARGINAL: 80% power at SNR={plausible_snr}, matching "
                   f"sd={realistic_matching} needs n={n_needed} per condition -- "
                   "large but not impossible; the paper should state this sample-size "
                   "demand as a practical limitation.")
    else:
        verdict = (f"UNDERPOWERED at realistic sizes: 80% power at SNR="
                   f"{plausible_snr}, matching sd={realistic_matching} needs n>"
                   f"{SAMPLE_SIZES[-1]} per condition -- beyond typical anesthesiology "
                   "recruitment. This is a practical (not only ethical) limitation "
                   "and must be stated in the paper.")
    if not fpr_ok:
        verdict += (f" WARNING: imperfect matching inflates the false-positive rate "
                    f"to {fpr[realistic_matching]:.2f} at n={REALISTIC_N} -- matching "
                    "must be tight or the interaction contrast confounded.")

    # figure: power heatmaps per matching + min-n bars
    fig, axes = plt.subplots(1, len(MATCHINGS), figsize=(16, 5), sharey=True)
    for ax, m in zip(axes, MATCHINGS):
        im = ax.imshow(grids[m], origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis")
        ax.set_xticks(range(len(SAMPLE_SIZES))); ax.set_xticklabels(SAMPLE_SIZES)
        ax.set_yticks(range(len(SNRS))); ax.set_yticklabels(SNRS)
        ax.set_xlabel("n per condition"); ax.set_title(f"matching sd={m}\nFPR@H0={fpr[m]:.2f}")
        for i in range(len(SNRS)):
            for j in range(len(SAMPLE_SIZES)):
                ax.text(j, i, f"{grids[m][i,j]:.2f}", ha="center", va="center",
                        color="w" if grids[m][i, j] < 0.6 else "k", fontsize=8)
    axes[0].set_ylabel("effect size (SNR = delta/sigma)")
    fig.suptitle("Exp H: dissociation-test power (80% target) vs n, SNR, matching", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(RESULTS_DIR, "power_grids.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "H_dissociation_power_analysis",
        "params": {"sample_sizes": SAMPLE_SIZES, "snrs": SNRS, "matchings": MATCHINGS,
                   "n_exp": N_EXP, "alpha": ALPHA, "realistic_n": REALISTIC_N},
        "power_grids": {str(m): grids[m].tolist() for m in MATCHINGS},
        "false_positive_rate_by_matching": {str(m): fpr[m] for m in MATCHINGS},
        "min_n_for_80pct_power": {str(m): {str(k): v for k, v in feasible[m].items()}
                                  for m in MATCHINGS},
        "preregistered_criterion": "80% power at realistic anesthesiology n and SNR",
        "verdict": verdict,
        "figures": ["power_grids.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
