# Positive control for the estimability gate: Fantasia (E2.1)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E2.1). Paper placeholder: R2.1 (Paper 2, §3.4). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Data
PhysioNet Fantasia, 20 young (f1y01–f1y10, f2y01–f2y10) and 20 elderly (f1o01–f1o10, f2o01–f2o10)
subjects, about 120 min each. R-peaks come from the database's reviewed beat annotations (annotator
`ecg`), not from a detector.

## A discrepancy found while preparing this plan, recorded before the run
- The paper (§2.4), the original pre-registration and the experiment plan all say the RR series was
  resampled evenly at 4 Hz.
- The code that produced 6 of 21 (`cbra_boundary_residual/run.py`) does not resample. It computes T on
  the **beat-indexed** RR series, after keeping RR within 0.3–2.0 s, trimming at 4 MAD of the median,
  and removing the mean.
- Both versions are run here, so the positive control speaks to the gate as it was applied and to the
  gate as it is described:
  - **Primary, gate as applied:** exactly `rr_tachogram`'s cleaning, then `time_reversal_asymmetry`
    at lag 1 and `boundary_structure` (200 IAAFT surrogates with 100 iterations; two-sided p =
    (#|T_surr| ≥ |T_obs| + 1)/201; structured if p < 0.05). Seed 0.
  - **Secondary, gate as described:** the same cleaned RR series, linearly interpolated at 4 Hz on
    the beat-time grid, then T at lag one sample and the same surrogate test.

## Criterion (the plan's)
The gate is sensitive if the structured fraction among the young is at least 0.60. The primary
version decides. The secondary version is reported beside it with its own verdict. If the young
fraction is below 0.60, the I-CARE failure says nothing about I-CARE.

**Prediction (Costa et al. 2005):** young above elderly.

## Reported
The fraction in each group, and T and p for each subject, under both versions.
