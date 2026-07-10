# Hybrid drift-robust jump statistic for the Exp D corner (Paper 3)

**Run after** Experiment D localized a structural region — weak-but-detectable
jump (collapse ≈ 0.7) × moderate/strong geodesic drift — where the square-root
jump statistic cannot separate a collapse from a drift (AUC → 0.61), and flagged
it as needing a "method change (hybrid metric)".

## Hypothesis
The confusion comes from a strong geodesic drift accumulating a **slowly-varying
holonomy term** (from direct-transport anti-development) whose peak mimics a jump.
A jump is a *high-frequency* event (single-step increment); drift + holonomy is
*low-frequency* (a slow trend). So **high-pass filtering** the anti-developed
increments (subtracting a local moving average) — kept on the same square-root
geometry, so jump power is preserved — should remove the drift/holonomy trend and
leave an abrupt jump, recovering separability in the corner.

## Pre-registered success/failure criteria
- **Recovered** if the hybrid lifts the worst weak-jump × strong-drift AUC to
  ≥ 0.85 while keeping jump power on genuine strong collapses ≥ 0.80.
- **Partial** if AUC improves by > 0.05 with jump power preserved, but does not
  reach 0.85.
- **Costs power** if AUC improves but strong-collapse jump power drops below 0.80.
- **No help** if the worst corner AUC does not improve — then the confusion is not
  a low-frequency contamination, the corner is a genuine geometric limit, and a
  true base-metric change (not a filtered statistic) is required.

## Stopping rule
One hybrid (high-pass) tested against the Exp D grid; whatever the outcome, it is
reported against these criteria. A negative result narrows the solution space and
is as informative as a positive one.

## Status
Run. Verdict: **NO HELP** — worst corner AUC 0.65 → 0.61 (jump power preserved,
1.00). The drift contamination is *not* low-frequency; high-passing cannot remove
it. Combined with the appendix's already-failed λ_min-persistence discriminator,
this confirms the corner is a genuine geometric limit of the square-root
anti-development requiring a true base-metric change, and rules out two classes of
statistical fix (high-pass filtering; λ_min persistence).
