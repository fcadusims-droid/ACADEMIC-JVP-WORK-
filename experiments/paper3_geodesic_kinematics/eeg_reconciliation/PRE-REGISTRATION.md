# Reconciling the real-EEG structural-discrimination ratio (Paper 3 appendix)

**Run after** `real_eeg_localization` reported a between/within structural
distance ratio with **median ≈ 1.7** (3/15 subjects below 1) on real
eyes-open/eyes-closed occipital-alpha EEG, whereas the Paper 3 appendix reports
the same discrimination at **median ≈ 12** (20/20 subjects > 1, range ≈ 2–36,
single-subject factor ≈ 19). That is a large, unexplained gap between the
committed code and the printed claim, and it must be reconciled on the *same
data* before either number can be trusted.

## The identified difference (the only variable changed here)
The two analyses differ in the **within-state distance** (the denominator of the
ratio); the between-state numerator is identical. The appendix names its
denominator explicitly — *"a within-state permutation null"* (Paper 3 §7.6,
real-data probe). `real_eeg_localization` instead used a **temporal-half split**:
`within(covs) = d(mean(covs[:h]), mean(covs[h:]))` — the distance between the
mean of the first half and the mean of the second half of the state's windows.

These are not the same quantity:
- **Temporal-half** measures the distance a state's mean *drifts* from its first
  half to its second half. Occipital alpha waxes and wanes on a ~10 s scale, so
  over a 26 s segment the two contiguous halves differ by that slow
  non-stationarity → a **large** denominator → a **small** ratio.
- **Random permutation** partitions the same windows into two *interleaved*
  random groups. Each group is a mix of early and late windows, so slow drift
  cancels in both group means → the denominator measures only estimation noise
  → a **small** denominator → a **large** ratio.

## Hypothesis
The appendix's median ≈ 12 is reproducible on the same cached 15 subjects, same
channels, same band, same segment length — the *only* change being the
within-state estimator from temporal-half to the appendix's random-permutation
null. The temporal-half ratio (≈ 1.7) and the permutation ratio (≈ 12) are both
correct measurements of *different* quantities; the appendix figure is not a
data error but a denominator that cancels within-state drift.

## Pre-registered success/failure criteria
Same 15 subjects, `CHANNELS`/`ALPHA_BAND`/`SEG_SEC` held identical to
`real_eeg_localization` (occipito-parietal, 8–13 Hz, 26 s). Compute the ratio
under **both** within-state estimators per subject.

- **Reconciled** if the random-permutation ratio has median in **[8, 20]** with
  **≥ 14/15** subjects > 1 (i.e. it lands in the appendix's stated band, median
  ≈ 12 / 20-of-20), *and* the temporal-half ratio reproduces the earlier
  median ≈ 1.7 (≈ [1.3, 2.3]). Then the gap is explained: it is entirely the
  within-state estimator, and the honest reported number depends on which
  within-state null one commits to.
- **Partially reconciled** if the permutation ratio rises materially above the
  temporal-half ratio (median lifts by ≥ 3×) but does not reach the appendix's
  [8, 20] band — then the estimator explains part of the gap and a residual
  (channels, segment length, subject sample) remains, to be named.
- **Not the cause** if the permutation ratio's median stays below 3× the
  temporal-half median — then the within-state null is *not* what separates
  1.7 from 12, and the discrepancy points elsewhere (channel set, segment
  length, or an optimistic appendix figure), which must then be stated plainly.

A per-subject **permutation-null p-value** is also reported (fraction of
random within-state split distances ≥ the between-state distance): this is the
appendix's actual significance claim (p ≈ 5×10⁻⁴ single-subject; p < 10⁻⁵
Wilcoxon across subjects) and lets us check the *significance* claim, not just
the ratio magnitude.

## Stopping rule
One reconciliation run on the 15 cached subjects. Whatever the outcome, the
**source of truth is `result.json`**: the verdict states which within-state
estimator the reported ratio came from, gives both numbers, and does not round
the honest figure toward the appendix's if the data do not support it.

## Status
Run. Verdict: **SIGNIFICANCE REPRODUCED, MAGNITUDE NOT** — falls in the
pre-registered "not the cause / points elsewhere" numeric bin, but the fuller
honest reading is a *partial* reconciliation.

On the same 15 subjects/channels/band/segment, switching only the within-state
denominator to the appendix's random-permutation null lifts the median ratio
from **1.28** (temporal-half, 12/15 > 1) to **3.33** (14/15 > 1, a 2.6× lift —
just under the pre-registered 3× "partial" bar) and makes the discrimination
significant in **14/15** subjects (median permutation p ≈ 0.0025, near the
appendix's single-subject 5×10⁻⁴; Wilcoxon vs unity p ≈ 6×10⁻⁵). So the
appendix's **direction and significance replicate** — the within-state estimator
*is* most of why my earlier 1.7 looked so much weaker than the printed claim.

But the permutation null does **not** reach the appendix's **magnitude** band
[8, 20] (median ≈ 12): the median is 3.33, and the secondary `sweep.py` grid
shows **no** segment (20–58 s) × covariance-window (0.5–2 s) choice reaches it
either — the maximum median across the whole grid is **5.4** (58 s / 2 s window).
The appendix's median-≈12 / range-2–36 figure is therefore **optimistic on this
data**; the defensible reported ratio is **~3–5** (permutation null) or **~1.3**
(temporal-half). Source of truth: `_results/eeg_reconciliation/result.json` and
`sweep.json`.
