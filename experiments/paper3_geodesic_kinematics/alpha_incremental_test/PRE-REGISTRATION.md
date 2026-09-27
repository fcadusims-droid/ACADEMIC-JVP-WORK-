# Does the geometry carry information beyond relative alpha power? (E3.2)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E3.2). Paper placeholder: R3.2 (Paper 3, §3.8). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Data
- EEGMMIDB, subjects 1–15, runs R01 (eyes open) and R02 (eyes closed).
- Channels O1, Oz, O2, PO3, POz, PO4, Pz; non-overlapping 2 s epochs.
- Control task: the T0 intervals of R03 against those of R07 (both eyes open), same epoching.

## Models
- **A:** logistic regression on per-channel relative alpha power (8–13 Hz over 1–40 Hz, Hann
  periodogram of the unfiltered epoch; the `rel_alpha` function of `between_recording_control`).
- **B:** A plus the tangent-space coordinates of the trace-normalized covariance of the alpha-filtered
  epoch. The epoch uses the per-channel z-scored alpha signal of `load_run`, the covariance has the
  same small eigenvalue floor as the method, and the tangent space is taken at the Riemannian mean of
  the training set (pyRiemann `TangentSpace(metric="riemann")`, fitted on the training fold only).
  7 channels give 28 coordinates.
- **Fixed now:** features are standardized with a scaler fitted on the training fold; sklearn
  `LogisticRegression(C=1.0, max_iter=5000)` (L2, lbfgs).

## Validation
Leave one subject out. Metric: log-loss on the held-out subject's epochs.

## Criterion (the plan's)
The geometry carries information beyond alpha power if B's log-loss is lower than A's in at least
11 of 15 subjects **and** a paired Wilcoxon test gives p < 0.05. The plan does not say which side,
so the test is two-sided, the more conservative choice; the one-sided p is reported too.

## Control
The same two models, trained to separate T0 of R03 from T0 of R07, "should both be at chance". Chance
is judged descriptively, from the median held-out balanced accuracy and the log-loss against ln 2 ≈
0.693, with per-subject values. No pass/fail bar is set for the control, because the plan gives none.
