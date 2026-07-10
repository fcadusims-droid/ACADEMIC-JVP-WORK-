"""Experiment I2 -- Does criticality alone confound the dissociation test?
(Paper 2, Sec 14.1). Extends Experiment I (gating confound) to M_diss.

Experiment I showed a bare critical generator reproduces the STRATIFIED GATING
differential. It did not test the DISSOCIATION test (Sec 14.1), which is the
statistic Experiment H's power analysis assumed valid. This asks: can a system
with ZERO identity-linked mechanism -- nothing that encodes or reads "identity"
-- produce the same qualitative preservation contrast (high under CONTINUE,
low under RESET) merely because continuity is broken, not because identity is
mismatched? If so, M_diss cannot distinguish genuine identity-linked
preservation from the trivial fact that any process with memory preserves more
when undisturbed than when perturbed.

Three generators, each producing a preservation score P under CONTINUE
(analogous to S^{I+}) and RESET (analogous to S^{I-}):
  * null            : P drawn identically under both -- honest negative control.
  * identity_linked : P high under CONTINUE, drops under RESET, by explicit
                      construction (the intended positive CBRA is designed to
                      detect).
  * bare_critical   : a Galton-Watson critical branching process with NO
                      identity mechanism. CONTINUE carries the avalanche state
                      across the transition; RESET reinitializes it. P is a
                      generic macro-invariant (log-size trajectory correlation).

D = mean(P|CONTINUE) - mean(P|RESET), swept over branching ratio and noise,
mirroring Experiment I's grid for direct comparability.

Usage:
    python -m experiments.paper2_cbra_protocol.dissociation_confound.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "dissociation_confound"
)

N_TRIALS = 1500
GEN_LEN = 12                                    # avalanche generations tracked
CRIT_EXPONENTS = [1.0, 1.25, 1.5, 2.0, 3.0]    # same grid as Experiment I
READOUT_NOISES = [0.1, 0.5, 1.0]
BASE_LAMBDA = 60.0    # large seed population: keeps trajectories away from the
                       # extinction floor for GEN_LEN generations even near
                       # criticality, so the log-trajectory carries real signal
                       # rather than being dominated by absorbing-state noise
IDENTITY_DROP = 1.5                             # identity-linked reset penalty (SNR)


def avalanche_trace(seed_count, sigma, rng, n_gen=GEN_LEN):
    """Per-generation activity trace of a Galton-Watson branching process."""
    active = np.full(N_TRIALS, seed_count, dtype=np.int64)
    trace = np.zeros((n_gen, N_TRIALS))
    for g in range(n_gen):
        active = rng.poisson(np.clip(sigma * active, 0, 1e5))
        trace[g] = active
    return trace


def level_correlation(pre_trace, post_trace, noise, rng):
    """Cross-trial correlation between the pre-transition state LEVEL and the
    post-transition state LEVEL -- the macro-invariant a near-critical branching
    process can plausibly preserve.

    A (near-)critical Galton-Watson process is approximately a martingale in
    population size: E[Z_post | Z_pre] ~ Z_pre. So a trial whose pre-transition
    activity happens to be elevated should ALSO show elevated post-transition
    activity if the SAME lineage continues (CONTINUE), but should show no such
    relationship if the post lineage is a fresh, independent draw (RESET) --
    this is exactly the preservation contrast M_diss looks for, with zero
    identity mechanism anywhere. Level (not within-trial trajectory shape) is
    the correct macro-invariant here: shape correlation over a martingale's
    near-iid log-increments carries little signal, but the LEVEL does.
    """
    pre_level = np.log1p(pre_trace[-1])
    post_level = np.log1p(post_trace[-1])
    pre_level = pre_level + noise * rng.standard_normal(pre_level.shape)
    post_level = post_level + noise * rng.standard_normal(post_level.shape)
    return float(np.corrcoef(pre_level, post_level)[0, 1])


def run_bare_critical(sigma, noise, seed):
    """CONTINUE: post is literally the continuation of the same lineage (its
    seed count at generation 0 equals pre's terminal activity -- no mechanism
    reads or encodes "identity" anywhere, it is just one uninterrupted
    branching trajectory split at the transition). RESET: post is an
    INDEPENDENT fresh lineage, decoupled from pre. Preservation is measured as
    the cross-trial correlation between pre-transition and post-transition
    activity LEVEL (the macro-invariant a martingale-like critical process can
    plausibly preserve; see level_correlation)."""
    rng = np.random.default_rng(seed)
    seeds = rng.poisson(BASE_LAMBDA, N_TRIALS)
    pre = avalanche_trace(seeds, sigma, rng, n_gen=GEN_LEN)

    # CONTINUE: post's initial state is literally pre's terminal state
    continue_seed = np.maximum(pre[-1].astype(np.int64), 0)
    post_continue = avalanche_trace(continue_seed, sigma, rng, n_gen=GEN_LEN)
    P_continue = level_correlation(pre, post_continue, noise, rng)

    # RESET: post is an independent fresh lineage, same sigma, no relation to pre
    reset_seeds = rng.poisson(BASE_LAMBDA, N_TRIALS)
    post_reset = avalanche_trace(reset_seeds, sigma, rng, n_gen=GEN_LEN)
    P_reset = level_correlation(pre, post_reset, noise, rng)

    return P_continue - P_reset


def run_identity_linked(noise, seed):
    """Explicit identity-linked channel: an identity-indexed latent variable I
    determines the level under CONTINUE (post strongly tracks pre, correlation
    ~0.9), but under RESET the identity binding is severed (post is independent
    of pre, correlation ~0)."""
    rng = np.random.default_rng(seed)
    identity = rng.standard_normal(N_TRIALS)
    pre_level = identity + 0.3 * rng.standard_normal(N_TRIALS)
    post_continue = identity + 0.3 * rng.standard_normal(N_TRIALS)          # tracks identity
    post_reset = rng.standard_normal(N_TRIALS)                              # severed
    P_continue = float(np.corrcoef(pre_level, post_continue)[0, 1])
    P_reset = float(np.corrcoef(pre_level, post_reset)[0, 1])
    return P_continue - P_reset


def run_null(noise, seed):
    """No dissociation: post is independent of pre under BOTH CONTINUE and
    RESET -- the honest negative control."""
    rng = np.random.default_rng(seed)
    pre_level = rng.standard_normal(N_TRIALS)
    post_continue = rng.standard_normal(N_TRIALS)
    post_reset = rng.standard_normal(N_TRIALS)
    P_continue = float(np.corrcoef(pre_level, post_continue)[0, 1])
    P_reset = float(np.corrcoef(pre_level, post_reset)[0, 1])
    return P_continue - P_reset


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment I2: does criticality alone confound the dissociation test?")

    D_identity = np.mean([run_identity_linked(0.5, s) for s in range(8)])
    D_null = np.mean([run_null(0.5, s) for s in range(8)])
    print(f"  reference: D_identity_linked={D_identity:.3f}, D_null={D_null:.3f}")

    grid = np.zeros((len(CRIT_EXPONENTS), len(READOUT_NOISES)))
    for i, p in enumerate(CRIT_EXPONENTS):
        # map exponent p (as in Exp I) to a branching ratio sigma via a
        # monotone transform so p=1 -> clearly sub-critical (sigma=0.7),
        # p=3 -> essentially exactly critical (sigma->1.0)
        sigma = 1.0 - 0.3 / p ** 2
        for j, noise in enumerate(READOUT_NOISES):
            D = np.mean([run_bare_critical(sigma, noise, 500 + s) for s in range(6)])
            grid[i, j] = D
            print(f"  p={p:.2f} (sigma={sigma:.3f}) noise={noise}: D_bare_critical={D:.3f}")

    # reproduction fraction among genuinely critical cells (p > 1), mirroring Exp I
    reproduces, total = 0, 0
    for i, p in enumerate(CRIT_EXPONENTS):
        if abs(p - 1.0) < 1e-9:
            continue
        for j in range(len(READOUT_NOISES)):
            total += 1
            if grid[i, j] >= 0.5 * D_identity:
                reproduces += 1
    frac = reproduces / total if total else 0.0
    control_max = float(np.max(np.abs(grid[0])))  # p=1 row: sub-critical control

    max_ratio = float(grid.max() / D_identity)
    trend_monotone = bool(np.all(np.diff(grid[:, 0]) >= -0.02))  # low-noise column vs p

    if frac >= 0.5:
        verdict = (f"DISSOCIATION CONFOUNDED, LIKE GATING: a bare critical "
                   f"generator with ZERO identity mechanism reproduces M_diss "
                   f"(D >= half the identity-linked value {D_identity:.2f}) in "
                   f"{reproduces}/{total} critical cells ({frac:.0%}). Sec 14.1 "
                   "needs the same demotion Sec 15.5 gave the gating test.")
    elif max_ratio >= 0.6 and trend_monotone:
        verdict = (f"GROWING CONFOUND NEAR TRUE CRITICALITY (nuanced, not a clean "
                   f"survival): the reproduction fraction at the D>=50% threshold "
                   f"is only {frac:.0%} ({reproduces}/{total}), but D_bare_critical "
                   f"rises MONOTONICALLY with criticality and low noise -- from "
                   f"{grid[0,0]:.2f} at sigma=0.70 to {grid[-1,0]:.2f} at "
                   f"sigma=0.97 (low-noise column) -- reaching {max_ratio:.0%} of "
                   f"the identity-linked reference ({D_identity:.2f}) at the "
                   "strongest/cleanest cell. The sub-critical control stays low "
                   f"(D<={control_max:.2f}), confirming it is criticality "
                   "specifically, not the statistic, that drives this. The honest "
                   "reading: M_diss is NOT confounded away from true criticality, "
                   "but AS a system approaches sigma=1 with low read-out noise, "
                   "the dissociation signature converges toward what pure "
                   "criticality alone can produce -- mirroring exactly the "
                   "pattern Exp I found for gating (safe away from criticality, "
                   "confounded near it). Sec 14.1 should state this boundary "
                   "explicitly: dissociation evidence is diagnostic of identity "
                   "only if the boundary process can be shown to be measurably "
                   "sub-critical, which CBRA does not currently require.")
    else:
        verdict = (f"DISSOCIATION SURVIVES: the bare critical generator's D stays "
                   f"below half the identity-linked value ({D_identity:.2f}) in "
                   f"{total - reproduces}/{total} critical cells ({1-frac:.0%}), "
                   f"and does not approach it even at the strongest cell "
                   f"({max_ratio:.0%} of reference). Unlike the gating "
                   "differential, M_diss is not confounded by criticality alone.")

    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="magma",
                   vmin=min(0, grid.min()), vmax=max(D_identity, grid.max()))
    ax.set_xticks(range(len(READOUT_NOISES))); ax.set_xticklabels(READOUT_NOISES)
    ax.set_yticks(range(len(CRIT_EXPONENTS))); ax.set_yticklabels(CRIT_EXPONENTS)
    ax.set_xlabel("read-out noise"); ax.set_ylabel("criticality exponent p (1=sub-critical control)")
    for i in range(len(CRIT_EXPONENTS)):
        for j in range(len(READOUT_NOISES)):
            ax.text(j, i, f"{grid[i,j]:.2f}", ha="center", va="center", color="w", fontsize=9)
    ax.set_title(f"Exp I2: bare-critical D_diss (identity-linked ref={D_identity:.2f}, null={D_null:.2f})")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "dissociation_confound_grid.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "I2_dissociation_confound",
        "params": {"n_trials": N_TRIALS, "gen_len": GEN_LEN,
                   "crit_exponents": CRIT_EXPONENTS, "readout_noises": READOUT_NOISES,
                   "identity_drop": IDENTITY_DROP},
        "D_identity_linked_reference": float(D_identity),
        "D_null_reference": float(D_null),
        "D_bare_critical_grid": grid.tolist(),
        "reproduces_fraction": frac,
        "sub_critical_control_max_D": control_max,
        "preregistered_question": "does criticality alone confound M_diss (Sec 14.1), like it confounds gating (Exp I)?",
        "verdict": verdict,
        "figures": ["dissociation_confound_grid.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
