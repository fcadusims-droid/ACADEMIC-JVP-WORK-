# Pre-registration — Do the window-permutation nulls behind the "14/15" discrimination survive dependence?

**Status:** pre-registered before the run. One run, no tuning loop.

## Why this exists
An external review found that `regime_external_referent` (H2) used a permutation null that
shuffles overlapping 2-s sliding windows as if they were independent, which destroys their
autocorrelation and makes the null too narrow (`regime_referent_nulls` confirmed: the null's
95th percentile widened 57-fold under a dependence-preserving null). A repository audit then
found the **same construction** in five other experiments, all of which permute individual
overlapping windows between stage/state groups:
`sleep_stage_localization` (A1 — the "N2-vs-REM discrimination 14/15" Paper 3 cites),
`sleep_structure_power_dissociation` (A2), `log_euclidean_real_eeg` (A3), `fibre_ablation`
(discrimination arm) and `eeg_reconciliation`. Their p-values may be anti-conservative.

## Test
A1's own statistic, imported unchanged (`_ratio`: geodesic distance between the N2 and REM
Fréchet means over the within-state temporal-halves distance), on the Sleep-EDF recordings
cached in this environment (7 of A1's 15; the rest cannot be downloaded here). Two nulls per
recording, 500 draws each:
- **Window permutation (A1's original):** pool N2 and REM windows, permute, split.
- **Circular shift (dependence-preserving):** rotate the whole-night stage-label sequence
  against the covariance series by an offset uniform in [0.1 L, 0.9 L], re-form the N2 and REM
  groups in temporal order, recompute the ratio (draws with < 10 windows in a group skipped).
Pass rule exactly as A1: ratio > 1 and p < 0.05.

## Pre-registered criterion
- **A1's discrimination survives** iff the number of recordings passing under the circular-
  shift null is at least the i.i.d. count minus one.
- Otherwise the "14/15" is attributed in part to an anti-conservative null; A1's claim, and the
  four other window-permutation results named above, are marked as resting on a null that
  ignores dependence, and Paper 3's use of the 14/15 is qualified accordingly.
- Either way, 7 recordings is a check, not a replacement for the 15-recording claim.
