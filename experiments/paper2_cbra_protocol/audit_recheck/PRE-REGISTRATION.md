# Re-checking the dataset audit's P1 column (E2.4)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E2.4). Paper placeholder: R2.4 (Paper 2, §3.4). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## CHB-MIT
- The first 30 EDF files listed in the database's RECORDS file.
- Only the EDF header is read, via an HTTP range request.
- A file counts as having a cardiac channel if any signal label contains "ECG" or "EKG"
  (case-insensitive).
- Reported: files with a cardiac channel out of 30, and the patients involved.

## TUH EEG
Access requires an application, which this environment does not have, so it is not checked.

## VitalDB
- The open track list (`https://api.vitaldb.net/trks`) is searched for raw EEG waveform tracks,
  meaning names containing `EEG` but not only the BIS index, and the number of cases with them is
  counted.
- If the API cannot be reached, this part is reported as not done.

## Scope (the plan's)
Even with ECG or raw EEG, these corpora lack the recovery/non-recovery contrast. The only aim is to
correct column P1 of Table 1.
