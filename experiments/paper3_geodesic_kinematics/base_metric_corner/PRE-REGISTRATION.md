# Base-Metric Change for the Exp D Structural Corner (Paper 3)

**Follow-up to Experiment D and the Hybrid probe.** Experiment D localized a
structural region — a *weak-but-detectable* jump (collapse factor ≈ 0.7) crossed
with *moderate/strong* geodesic drift — where the square-root-metric jump
statistic cannot separate a collapse from a drift (AUC → 0.61): a strong geodesic
drift, anti-developed by direct parallel transport on the curved (K = 1/4)
square-root sphere, accumulates a slowly-varying **holonomy** term whose peak
mimics a jump. The Hybrid probe then showed that a high-pass (drift-robust)
*statistic*, kept on the same square-root geometry, does **not** fix the corner
(worst AUC 0.65 → 0.61), and concluded that the confusion is not a low-frequency
contamination but a genuine limit of the square-root anti-development requiring
**a true base-metric change (not a filtered statistic)**.

This experiment runs that base-metric change.

## What "Bures / log-Euclidean" means here (a clarification, stated up front)

The square-root (Wigner–Yanase) metric this protocol commits to **already** is the
**Bures *angle*** geometry: `sqrt_distance = 2 arccos(tr √ρ₁ √ρ₂)`, i.e. the
spherical (arc-length) distance of the `2√ρ` embedding, a monotone function of the
quantum fidelity. So "Bures" in the *angle/sphere* sense is the baseline, not a new
metric. The genuinely distinct alternative base metrics on the SPD/density
manifold are:

- **Log-Euclidean** (Arsigny et al. 2006): the metric `log(ρ)`-pushforward of the
  Euclidean metric. It is **flat** — zero curvature, so the connection is trivial
  and **holonomy is identically zero**. A geodesic drift accumulates *no* holonomy
  here, so if the corner confusion is holonomy-driven (Exp D's diagnosis), this
  metric should remove it. Its own risk: near a rank collapse `log λ_min → −∞`, so
  a collapse is a *large* log-increment (potentially more detectable), but a drift
  wandering toward small eigenvalues could also inflate log-increments.
- **Bures–Wasserstein** (Bhatia–Jain–Lim 2019): the Wasserstein-2 geometry of
  centred Gaussians — the *chordal* fidelity distance, geodesically distinct from
  the Bures-angle sphere. A different curvature/connection again, gentler than
  log-Euclidean near collapse (contributes `√λ`, not `log λ`).
- **Affine-invariant (AIRM)** — already in `shared_lib`; near-singular distance
  diverges, so a collapse yields a heavy-tailed increment.

All four (square-root, log-Euclidean, Bures–Wasserstein, AIRM) are tested.

## Method

Reproduce the Exp D / Hybrid corner grid exactly — `drift_strength ∈
{0.0,…,0.4}` × `collapse_factor ∈ {0.7,0.5,0.3,0.1}`, SPD(3), the same simulator
`simulate_manifold_regime` and covariate-anchored jump statistic — and compute,
for **each base metric**, the discrimination `AUC(collapse vs drift)` and the jump
power on genuine strong collapses.

Anti-development convention. The first plan was a single common convention —
base-point log map + Euclidean first differences (`anti_develop_base`) — with the
pre-registered **validity guard** that the square-root column must reproduce the
corner confusion (worst corner AUC ≲ 0.7) under that convention, else fall back.
A pre-run sanity check (N = 25, single corner cell) **tripped that guard**: under
the base-point linearization the square-root corner AUC was ≈ 0.95, not ≈ 0.56 —
because the base-point linearization folds the path's holonomy into the base frame
and thereby *discards the very holonomy that is the corner phenomenon*. Per the
pre-registered fallback, the scored run therefore uses each metric's **proper
path-wise anti-development** (step log + that metric's parallel transport), which
correctly reflects each connection's holonomy:

- **square-root** — exact step-log + sphere transport (the true Exp D statistic;
  holonomy present, must reproduce the corner ≈ 0.56);
- **log-Euclidean** — flat, so parallel transport is the identity and the path-wise
  anti-development equals the base one exactly: `Δ log ρ`, zero holonomy;
- **affine-invariant (AIRM)** — whitening transport to the base frame.

The **base-linearized square-root** is retained as a *control* to demonstrate the
holonomy claim (it should read ≈ 0.95, i.e. discarding holonomy removes the
confusion). **Bures–Wasserstein** is retained only as a *supplementary,
base-linearized* column, explicitly flagged: its path-wise parallel transport is
not implemented, so the base-point BW log under-represents its holonomy and gives
an *optimistic* reference for BW, not a fair path-wise test. The decision rule
below is judged **only** on the fair path-wise alternatives (log-Euclidean, AIRM);
the criteria and thresholds are unchanged from first registration.

## Pre-registered success/failure criteria (mirroring the Hybrid probe)

Let `worst_m` be the minimum AUC over the corner cells (weak jump collapse 0.7 ×
drift ≥ 0.2) under base metric `m`, and `power_m` the minimum jump power on strong
collapses (collapse ≤ 0.3) at a 5% dispersion-calibrated threshold.

- **RESOLVED** if some alternative base metric reaches `worst_m ≥ 0.85` while
  keeping `power_m ≥ 0.80`. Then the corner is a **square-root-specific** geometric
  limit that a base-metric change repairs; Paper 3 should name that metric as the
  drift/jump-robust choice in the corner.
- **PARTIAL** if some alternative improves the worst corner AUC by `> 0.05` with
  `power_m ≥ 0.80` but does not reach 0.85. The corner is *ameliorable* by a metric
  change but not closed.
- **TRADE-OFF** if an alternative improves the corner AUC but drops `power_m` below
  0.80 — a metric that separates the corner only by dulling genuine jumps.
- **NO HELP / METRIC-INDEPENDENT LIMIT** if no base metric lifts the worst corner
  AUC above the square-root baseline by more than 0.05. Then the weak-jump ×
  strong-drift confusion is **not** specific to the square-root connection: it is an
  intrinsic overlap of the two regimes' anti-developed increment distributions,
  robust to the choice of base metric — a genuine limitation of the observable,
  which Paper 3 must state as such (the appendix's "hybrid metric will fix it"
  hope is then closed negative, and the honest position is that a weak partial
  collapse under strong drift is not asymptotically demarcated by *any* of the
  standard SPD base metrics).

## Stopping rule

One run: the four base metrics on the Exp D grid, plus the exact path-wise
square-root control, `N_SEEDS = 60`, whatever the criteria return is the verdict.
No re-tuning of the grid, seed count, jump statistic, or thresholds after seeing
results. A negative (metric-independent-limit) result is as informative as a
positive one and narrows the solution space for Paper 3's Sec 6.4 confounds.

## Status
Pre-registered. Not yet run.
