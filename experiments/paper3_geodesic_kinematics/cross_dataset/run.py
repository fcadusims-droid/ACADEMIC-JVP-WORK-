"""Experiment C -- Cross-dataset test: is it the method or the paradigm? (Paper 3)

The appendix's on-line localization failed (5/15) on the eyes-open/eyes-closed
alpha paradigm, where the spontaneous structural fluctuation is as large as the
transition. C asks whether that is a method failure or a paradigm that is
adversarial *for* the method. On a paradigm where the transition is structurally
STRONGER than the background (sleep-stage transitions; anesthesia
induction/emergence), the method should localize well.

PhysioNet Sleep-EDF is also blocked by the environment network policy (see
DATA.md), so this reproduces the question synthetically: sweep the
**transition-to-spontaneous-fluctuation ratio** and measure localization for both
the fragile pointwise detector and the persistence-sensitive window-mean detector.
Low ratio ~1 = the alpha regime (A/B); high ratio = a strong structural paradigm
(sleep/anesthesia). If localization is governed by that ratio, the 5/15 is
paradigm-limited, not a fundamental method failure.

Reuses the fast embedding/cumsum machinery from Experiment A.

Usage:
    python -m experiments.paper3_geodesic_kinematics.cross_dataset.run
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
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve, _R,
)

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "cross_dataset"
)

# ---- pre-fixed parameters ----------------------------------------------------
N_SUBJECTS = 15
N_CH = 4
T = 600
SEAM_LO, SEAM_HI = 0.35, 0.65
EXCURSION_SIZE = 0.5              # fixed spontaneous excursion scale
EXCURSION_PROB = 0.03
WANDER = 0.05
AR_RHO = 0.8
# transition strength relative to the spontaneous excursion (the swept ratio)
RATIOS = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
# fluctuation persistence: single-sample (transient) -> sustained bursts (real alpha)
BURST_DURATIONS = [1, 10, 30, 60, 100]
FRAGILE_W = 3
LARGE_W = 120
TOL = 15


def generate_subject(seed, seam_size, burst_duration=1):
    """burst_duration=1 -> transient single-sample excursions (favourable to a
    window-mean); larger -> SUSTAINED spontaneous structural bursts (as real alpha
    bursts are), which a window-mean cannot average away."""
    rng = np.random.default_rng(seed)
    base_A = mt.random_density(N_CH, rng)
    dirn = spd.sqrt_log(base_A, mt.random_density(N_CH, rng))
    dirn = dirn / np.sqrt(np.sum(dirn * dirn))
    t_seam = int(rng.uniform(SEAM_LO, SEAM_HI) * T)
    base_B = spd.sqrt_exp(base_A, seam_size * dirn)
    # pre-plan sustained bursts: random start times, each lasting burst_duration,
    # a temporary base offset in a random direction
    n_bursts = max(1, int(EXCURSION_PROB * T / max(burst_duration, 1)))
    burst_active = np.zeros(T)
    burst_dir = {}
    for _ in range(n_bursts):
        t0 = int(rng.integers(20, T - 20 - burst_duration))
        if abs(t0 - t_seam) < burst_duration + 5:
            continue
        bd = rng.standard_normal((N_CH, N_CH)); bd = 0.5 * (bd + bd.T)
        for tt in range(t0, t0 + burst_duration):
            burst_active[tt] = 1
            burst_dir[tt] = bd
    covs = []
    xi = np.zeros((N_CH, N_CH))
    for t in range(T):
        base = base_A if t < t_seam else base_B
        step = WANDER * 0.5 * rng.standard_normal((N_CH, N_CH))
        step = 0.5 * (step + step.T)
        xi = AR_RHO * xi + np.sqrt(1 - AR_RHO ** 2) * step
        offset = np.zeros((N_CH, N_CH))
        if burst_active[t]:
            o = EXCURSION_SIZE * 0.5 * burst_dir[t]
            offset = 0.5 * (o + o.T)
        covs.append(spd.sqrt_exp(base, xi + offset))
    return covs, t_seam


def hit_rate(seam_size, detector, burst_duration=1):
    hits = 0
    for s in range(N_SUBJECTS):
        covs, seam = generate_subject(s, seam_size, burst_duration)
        _, C = embed_cumsum(covs)
        curve = break_curve(C, detector)
        t_hat = int(np.nanargmax(np.where(np.isnan(curve), -np.inf, curve)))
        hits += (abs(t_hat - seam) <= TOL)
    return hits


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment C: method-vs-paradigm (transition/fluctuation ratio sweep)")
    print(f"  excursion size fixed at {EXCURSION_SIZE}; sweeping seam size")

    frag, large = [], []
    for r in RATIOS:
        seam_size = r * EXCURSION_SIZE
        fh = hit_rate(seam_size, FRAGILE_W)
        lh = hit_rate(seam_size, LARGE_W)
        frag.append(fh)
        large.append(lh)
        print(f"  ratio={r:4.2f} (seam={seam_size:.2f}): fragile {fh:2d}/{N_SUBJECTS}, "
              f"large-window {lh:2d}/{N_SUBJECTS}")

    frag = np.array(frag)
    large = np.array(large)

    # --- second axis: fluctuation PERSISTENCE at the adversarial ratio 1 ---------
    # transient excursions are averaged away by a window mean; sustained bursts
    # (as real alpha bursts are) are NOT -- this is the likely real-EEG difficulty.
    print("  --- sustained-burst sweep at ratio 1 (seam = excursion size) ---")
    burst_large = []
    for bd in BURST_DURATIONS:
        lh = hit_rate(EXCURSION_SIZE, LARGE_W, burst_duration=bd)
        burst_large.append(lh)
        print(f"  burst_duration={bd:3d}: large-window {lh:2d}/{N_SUBJECTS}")
    burst_large = np.array(burst_large)

    # A+B+C stopping-rule verdict
    large_strong = large[RATIOS.index(2.0)]
    large_alpha_transient = large[RATIOS.index(1.0)]      # transient bursts
    large_alpha_sustained = burst_large[-1]               # longest sustained burst
    frag_alpha = frag[RATIOS.index(1.0)]
    if large_alpha_transient >= 12 and large_alpha_sustained >= 10:
        verdict = (f"METHOD ROBUST via PERSISTENCE: the persistence-sensitive large "
                   f"window localizes the transition robustly across paradigm "
                   f"strength (>= {int(large.min())}/{N_SUBJECTS} at every ratio, "
                   f"including the adversarial ratio 1 where the fragile pointwise "
                   f"detector gets {frag_alpha}/{N_SUBJECTS}) AND across fluctuation "
                   f"persistence -- degrading only mildly to "
                   f"{large_alpha_sustained}/{N_SUBJECTS} when spontaneous bursts "
                   f"approach the window length ({BURST_DURATIONS[-1]} vs window "
                   f"{LARGE_W}). A+B+C stopping rule: the localization failure (5/15) "
                   "is resolved by a large, persistence-sensitive window -- NOT by a "
                   "multiscale bank (Exp A: no gain over a single large window) and "
                   "NOT by covariate smoothing (Exp B: degrades it). The residual "
                   "risk is a spontaneous structural burst LONGER than the analysis "
                   "window, which would look permanent within it; that is the one "
                   "regime still needing a permanence-to-record-end test. Ready for a "
                   "confirmatory pre-registration; real-EEG confirmation still needs "
                   "PhysioNet.")
    elif large_alpha_transient >= 12 and large_alpha_sustained < 10:
        verdict = (f"SPLIT: robust to transient fluctuations "
                   f"({large_alpha_transient}/{N_SUBJECTS}) but sustained bursts "
                   f"defeat the window mean ({large_alpha_sustained}/{N_SUBJECTS}) -- "
                   "a confirmed limitation needing a permanence discriminator.")
    elif large_strong >= 12 and large_alpha_transient < 10:
        verdict = (f"PARADIGM-LIMITED: {large_alpha_transient}/{N_SUBJECTS} at ratio "
                   f"1 vs {large_strong}/{N_SUBJECTS} at ratio 2 -- governed by "
                   "paradigm strength.")
    else:
        verdict = (f"METHOD-LIMITED: large-window reaches only {large_strong}/"
                   f"{N_SUBJECTS} even at a strong ratio; a structural change is "
                   "indicated.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.plot(RATIOS, frag / N_SUBJECTS, "o-", color="gray", label=f"fragile (w={FRAGILE_W})")
    ax.plot(RATIOS, large / N_SUBJECTS, "s-", color="crimson", label=f"large window (w={LARGE_W})")
    ax.axvline(1.0, ls=":", color="k", alpha=0.6); ax.text(1.02, 0.08, "alpha", fontsize=8)
    ax.axvline(2.0, ls=":", color="green", alpha=0.6); ax.text(2.02, 0.08, "sleep/anes.", fontsize=8)
    ax.set_xlabel("transition / spontaneous-fluctuation ratio (transient bursts)")
    ax.set_ylabel(f"hit rate (|err| <= {TOL})"); ax.set_ylim(0, 1.05)
    ax.set_title("Paradigm strength (transient fluctuations)"); ax.legend()
    ax = axes[1]
    ax.plot(BURST_DURATIONS, burst_large / N_SUBJECTS, "s-", color="crimson")
    ax.set_xlabel("spontaneous-burst duration (samples), at ratio 1")
    ax.set_ylabel(f"large-window hit rate (|err| <= {TOL})"); ax.set_ylim(0, 1.05)
    ax.set_title("Fluctuation persistence defeats the window mean")
    fig.suptitle(f"Exp C: method vs paradigm ({N_SUBJECTS} subjects)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(RESULTS_DIR, "ratio_sweep.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "C_cross_dataset",
        "mode": "synthetic (Sleep-EDF blocked by network policy) -- ratio sweep proxy",
        "params": {"n_subjects": N_SUBJECTS, "n_ch": N_CH, "T": T,
                   "excursion_size": EXCURSION_SIZE, "ratios": RATIOS,
                   "fragile_w": FRAGILE_W, "large_w": LARGE_W, "tol": TOL},
        "fragile_hits_by_ratio": {str(r): int(h) for r, h in zip(RATIOS, frag)},
        "large_window_hits_by_ratio": {str(r): int(h) for r, h in zip(RATIOS, large)},
        "large_window_hits_by_burst_duration_at_ratio1": {
            str(bd): int(h) for bd, h in zip(BURST_DURATIONS, burst_large)},
        "preregistered_question": "method failure vs adversarial paradigm",
        "verdict": verdict,
        "figures": ["ratio_sweep.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
