# H4 — is any public dataset viable for the CBRA positive arm? (Paper 2)

**Written before the inventory.** `dataset_viability_gate` (Phase 0) concluded I-CARE is the only
public corpus with all three CBRA properties, but I-CARE then failed the estimability gate (B1,
29%). H4 asks the complementary question the reviewer posed: is there **any** public dataset that
satisfies all three properties simultaneously, so the positive arm could be re-tested on a cleaner
cohort (H3)? This is a systematic inventory, not a simulation, and its value is that either
outcome is decisive:
- **Confirm (the bottleneck is data):** no public dataset has raw EEG + concurrent ECG + an
  I⁺/I⁻ (recovery vs non-recovery / consciousness contrast) + MR-length records → the positive
  arm is not executable on public data as of the inventory date, and H3's re-test has no venue.
- **Refute (the valuable outcome):** such a dataset exists → name it; it becomes H3's target.

## The three properties (from `dataset_viability_gate`)
1. **Raw EEG + concurrent cardiac** (ECG/PPG) in the same records — not a derived index (BIS).
2. **I⁺/I⁻ contrast** — paired transitions of different identity-status (recovery vs
   non-recovery, or consciousness vs not) with matchable surface dynamics.
3. **MR-length** — records long enough for a subsampling-robust criticality estimate.

## Method
Enumerate the credible public candidates and score each against the three properties, recording
host reachability (access is not the same as suitability). Candidates fixed in advance:
I-CARE, VitalDB, MIMIC-III/IV Waveform, Sleep-EDF / SHHS / MASS sleep banks, TUH EEG / CHB-MIT
seizure banks, and the openlists/meagmohit electrophysiology catalogues for anything missed.

## Pre-registered criterion
- **Not executable (confirm):** exactly the datasets `dataset_viability_gate` named clear the
  substrate+length bar but fail property 2 (pure I⁺) or property 1 (index not raw EEG), and none
  clears all three except I-CARE (which fails estimability, not viability) → the positive arm's
  bottleneck is data availability, recorded with the inventory date.
- **New venue (refute):** a named dataset clears all three → H3 acquires a target.

## Status
Pre-registered. Not yet run.
