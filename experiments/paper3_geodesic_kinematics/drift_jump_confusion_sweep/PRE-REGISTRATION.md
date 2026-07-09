# Experiment D — Drift-vs-Jump Confusion Sweep (Paper 3)

**Run order: 1st.** Cheapest and most decisive: it is a diagnostic, not a new
discriminator. Three discriminators already failed (Paper 3 appendix); before
trying a fourth, find out whether the problem is *structural* (the square-root
geometry genuinely cannot separate the two in certain regimes) or a *threshold
calibration* problem.

## Question
Under the committed square-root (Wigner-Yanase) metric, a substantial fraction of
pure-drift trajectories are misclassified as jumps (drift→jump rate ≈ 0.2–0.4,
appendix). Is this confusion boundary structural or calibrational?

## Method
Systematic grid over **drift intensity × jump severity × window length**
(and metric: square-root vs affine-invariant as a reference). For each cell,
simulate many single trajectories with known ground truth using
`shared_lib.jump_diffusion`, run the `shared_lib.stats_utils` Girsanov drift LRT
and covariate-anchored jump GLR, and record the confusion matrix. Plot the
drift→jump misclassification rate as a surface over the grid.

## Pre-registered success criterion (of the diagnostic, not of the method)
The sweep **succeeds as a diagnostic** if it yields a clear, reproducible verdict:
either (a) a monotone confusion boundary that a single recalibrated threshold
collapses below 0.1 drift→jump while holding jump power > 0.5 — i.e. the problem
is *calibrational and fixable*; or (b) a region of the grid where **no** threshold
separates drift from jump at fixed jump power — i.e. the problem is *structural*
and the honest consequence is a method change (hybrid metric), not a tuning fix.

## Pre-registered failure criterion
The diagnostic is inconclusive if the confusion surface is dominated by
seed-to-seed variance larger than the drift/jump effect (as the appendix's
"permanence" discriminator was), in which case no verdict on structural-vs-
calibrational can be issued and that itself must be reported.

## Stopping rule
One systematic sweep with pre-fixed grid and ≥ 50 seeds per cell. Do not add
discriminators inside this experiment; its only job is to characterise the
existing confusion boundary.

## Status
Pre-registered. Not yet implemented.
