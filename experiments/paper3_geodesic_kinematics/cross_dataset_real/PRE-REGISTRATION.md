# Experiment C (real data) — Is on-line localization governed by the measured transition/fluctuation ratio, across real paradigms?

**Follows:** `cross_dataset` (synthetic Exp C), which is explicit that "**C itself remains
untested on real data** — its content is robustness across paradigm strength and
fluctuation persistence, which needs corpora varying along those axes, not a second
analysis of one corpus." This experiment supplies exactly that.

## Question
The synthetic Exp C swept the **transition-to-spontaneous-fluctuation ratio** and found
that on-line localization is *governed by that ratio*: at ratio ≈ 1 (the eyes-open/closed
alpha regime) localization is hard, and it improves as the transition grows structurally
larger than the background. The claim was validated on synthetic ground truth only.

Does that mechanism hold on **real** recordings? Concretely: if we **measure** the
transition/fluctuation ratio directly on each real recording, does that measured ratio
predict how well the geodesic detector localizes the transition — across two real
paradigms that sit at opposite ends of the ratio axis?

## Why this is not a repeat of an existing experiment
- `real_eeg_localization` / `abc_real_eeg` compare **window size vs multiscale** *within one
  corpus*; they never relate a measured per-recording ratio to localization, and never
  pool paradigms.
- `sleep_stage_localization` (A1) reports a discrimination ratio for a *different* stage
  pair (N2/REM) and a separate localization count; it never tests whether the ratio
  **governs** localization.
- The object here is the **cross-paradigm ratio → localization relationship measured on
  real data** — Exp C's specific content, which none of the above tests.

## Data (both already staged; PhysioNet reachable)
Two real paradigms spanning the ratio axis, analysed with **one unified detector**
(geodesic CUSUM, the winner of `online_localization_cusum` and `sleep_stage_localization`):
- **Low-ratio paradigm** — eegmmidb eyes-open (R01) vs eyes-closed (R02) occipital alpha
  (spontaneous alpha bursts as large as the transition). Loader reused verbatim from
  `real_eeg_localization`.
- **High-ratio paradigm** — Sleep-EDF wake→sleep-onset (W→N1), a slow, consistent
  structural reorganization. Loader and transition finder reused verbatim from
  `sleep_stage_localization`.

## Measured quantities (fixed definitions, computed on the √-embedding sphere, radius R=2)
For each recording, over the analysis segment around the true seam:
- **Transition size** Δ = geodesic distance between the pre-seam and post-seam state
  centroids (mean √-embeddings, renormalised to R).
- **Spontaneous fluctuation** φ = mean over the two states of the *median* geodesic
  distance of each within-state window embedding to its own state centroid.
- **Measured ratio** R = Δ / φ.
- **Normalised localization error** e_norm = |τ̂ − τ_true| / (N_windows / 2), where τ̂ is
  the geodesic-CUSUM change point. This is **tolerance-free** (a fraction of the segment
  half-length), so the two paradigms — which live on different time scales — are directly
  comparable and the different absolute tolerances of A1 / real_eeg cannot confound the
  test. Lower e_norm = better localization.

## Pre-registered success criterion (C's mechanism holds on real data)
Across the **pooled** real recordings (both paradigms), higher measured ratio ⇒ better
localization:
- **PRIMARY:** Spearman ρ(R, e_norm) ≤ **−0.40** with p < 0.05 (higher ratio → smaller
  normalised error), **and** the paradigm ordering is consistent:
  median R(sleep) > median R(alpha) **and** median e_norm(sleep) < median e_norm(alpha).
- **QUALIFIED:** −0.40 < ρ ≤ −0.20 (ratio is predictive but not decisive).
- **FAILURE / real negative:** ρ > −0.20, or the wrong sign, or the paradigm ordering is
  violated ⇒ the ratio mechanism does **not** transfer to real data, and the localization
  limitation is not explained by paradigm strength. Reported as a genuine negative, not
  softened.

## Secondary (descriptive, no threshold — declared so it cannot be tuned)
Exp C's second axis is **fluctuation persistence** (a spontaneous burst longer than the
window looks permanent within it). Per recording, measure the within-state persistence
time of the distance-to-centroid series (lag where its autocorrelation falls below 1/e),
in seconds and in window units, and report whether the residual high-ratio misses coincide
with long within-state persistence. Descriptive only — Exp C already registered this as the
residual risk, so it is reported, not scored.

## Attempt budget & anti-tuning rule
**One run. No tuning loop.** Ratio, e_norm and the criterion above are fixed here, before
the run. If an instrument defect surfaces (degenerate covariance, NaN, a loader mismatch),
the **instrument** is fixed and the fix recorded as an addendum with an outcome-independent
justification — the **threshold is never moved**, per `METHODOLOGY.md`.

## Self-test gating the run (fails the build rather than producing a result)
Before any real recording is read, the ratio estimator is checked on two **synthetic**
recordings with a *known* high vs low transition/fluctuation ratio: it must (a) order them
correctly (R_high > R_low) and (b) give a smaller e_norm for the high-ratio one. If either
check fails, the run aborts — a ratio estimator that cannot see a ratio it was handed
cannot be trusted to measure one on real data.

## Status
**Run. Verdict: NOT SUPPORTED AT STRENGTH (pre-registration's negative branch).**
Across 22 real recordings (15 alpha + 7 sleep) the measured ratio is right-signed on
localization error (Spearman ρ = −0.36, p = 0.099) — Exp C's direction — but it does not
clear the −0.40 bar and is not significant at this n. The paradigm-ordering assumption is
**refuted**: measured, sleep-onset (W→N1) is *not* a higher-ratio transition than
eyes-open/closed alpha (median R 0.68 vs 0.69) and localizes no better (median e_norm
0.156 vs 0.078). Two consequences: (i) the design did not actually span the ratio axis —
W→N1 is a gradual, low-ratio transition on this geometry; (ii) Exp C's synthetic "robust
across paradigm strength" (15/15 at every ratio) does **not** transfer, the same
synthetic-overstates-real pattern already documented for Exp A. Self-test passed (the ratio
estimator ordered two known synthetic ratios correctly: R = 20.4 vs 3.5). No threshold
moved. The fair test — a genuinely high-ratio real transition (e.g. N2↔REM) as the high
end — is **registered here as a follow-up**, not run post-hoc to chase the bar.
(SC4012 was skipped: a truncated staged EDF, `filesize 8450048 != expected`.)
