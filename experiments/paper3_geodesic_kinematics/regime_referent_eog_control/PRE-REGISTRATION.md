# Pre-registration — Is the geometry's advantage over scalars really the eye?

**Status:** pre-registered before the run. One run, no tuning loop. Written in response to a
second external review of `regime_referent_nulls`, whose two new objections are checked in the
code and both hold:

1. **Pseudo-replication.** The 7 records are 4 subjects: Sleep-EDF names are `SC4ssN`, subject
   `ss`, night `N`, so SC4001/SC4002 (subject 00), SC4011 (01), SC4021/SC4022 (02),
   SC4031/SC4032 (03). The record-level Wilcoxon p = 0.0078 is the smallest value attainable at
   n = 7 (1/128) and treats two nights of one person as independent. At the subject level
   (n = 4) the smallest attainable one-sided p is 1/16 = 0.0625, so the pre-registered p < 0.05
   **cannot be reached with these data whatever the effect**. Verdict (A)'s record-level clauses
   rest on pseudo-replication.
2. **The EOG channel.** The "geometry" is SPD(3) over `EEG Fpz-Cz`, `EEG Pz-Oz`, `EOG horizontal`,
   each channel z-scored (`sleep_stage_localization.load_subject`). The trace-normalised covariance
   mostly carries inter-channel correlation; Fpz sits beside the eyes, and W and REM are the stages
   with eye movement. The most economical hypothesis is that geodesic volatility measures the
   coupling of eye movement into frontal EEG. The scalar baselines already run (total power,
   log-power, mean relative delta) do not carry that information, so beating them does not isolate
   the geometry.

## Data
The same 7 cached recordings, windows (2 s, 1 s step), AASM mapping and within-record median
split as `regime_referent_nulls`. **The unit of inference is the subject (n = 4)**: per-subject V
is the mean of its nights' V.

## Features (each median-split within record, exactly as before)
- **geo_vol** — geodesic volatility on SPD(3) with EOG (the feature under test; unchanged).
- **geo_vol_eeg** — the same construction on SPD(2) over Fpz-Cz and Pz-Oz only (EOG removed).
- **fpz_eog_corr_vol** — rolling mean (10 windows) of |Δ corr(Fpz-Cz, EOG)| per window.
- **fpz_eog_corr_level** — |corr(Fpz-Cz, EOG)| per window.
- **eog_pow_vol** — rolling mean (10 windows) of |Δ log EOG power|.
- **eog_pow_level** — log EOG power.
The four EOG-carrying scalars are the reviewer's fair baselines.

## Pre-registered criteria
Let E* be the EOG-carrying scalar with the highest pooled V.
- **Attributable to the eye** iff E*'s pooled V ≥ geo_vol's, or E* ≥ geo_vol in at least 2 of the
  4 subjects. The "attributable to the geometry" clause of `regime_referent_nulls` is then
  withdrawn in favour of "attributable to EOG coupling".
- **Geometry survives the EOG control** iff geo_vol exceeds E* pooled **and** in 4/4 subjects.
  Even then it is reported as *consistent in 4/4 subjects, not significant*: with 4 subjects no
  one-sided test can reach p < 0.05.
- Otherwise: **not established**.
- **EEG-only geometry (secondary, same comparison):** if geo_vol_eeg exceeds E* in 4/4 subjects,
  the geometric signal is not carried by the EOG channel alone; if it falls to or below E*, the
  EOG channel carries it.
- Whatever the outcome, verdict (A) of `regime_referent_nulls` is downgraded on its record-level
  clauses for pseudo-replication; that is a fact about the design, not a test result.
