# I-CARE by outcome: descriptive (E2.3)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E2.3). Paper placeholder: R2.3 (Paper 2, §3.4). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

**This does not test the dissociation. It is description only.**

## Selection (the plan's, operationalized now)
- The first 50 patients with good outcome (CPC 1–2) and the first 50 with poor outcome (CPC 3–5), in
  the order of the training-set RECORDS file of I-CARE 2.1.
- A patient qualifies if one of their ECG segments gives **30 minutes of clean ECG**. That is defined
  now as: after E2.2's 20% local-median cleaning, the retained RR intervals of one hourly segment sum
  to at least 1800 s.
- A patient's ECG segments are tried in order, at most 3 per patient, to bound downloads. Patients
  with no qualifying segment in those 3 are skipped and counted.
- The summary uses the first 1800 s of retained beats of the qualifying segment, so all patients
  contribute the same length.

## Measure and test
E2.2's summary (mean |z| over scales 1–10, 100 IAAFT surrogates per scale), compared between the two
groups with a two-sided Mann–Whitney U test. The per-subject p and the structured fraction are
reported as well.

## Covariates
From each patient's metadata file: age, sex, shockable initial rhythm, target temperature
management, and CPC.

## Reported
The distributions by group, the p-value, and the covariates.
