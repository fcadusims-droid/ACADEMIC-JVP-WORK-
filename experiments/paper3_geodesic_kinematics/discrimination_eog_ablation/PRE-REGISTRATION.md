# Pre-registration — Is the sleep "structural discrimination" also the eye?

**Status:** pre-registered before the run. One run, no tuning loop.

## Why this exists
`regime_referent_eog_control` found that the geodesic-volatility association with AASM staging is
carried by the EOG channel: geometry with EOG V = 0.452, without EOG V = 0.021, EOG power alone
V = 0.524. Paper 3 presents as validated core the N2-versus-REM **structural discrimination** of
`sleep_stage_localization` (A1; "14/15 recordings"), computed on the same SPD(3) covariance over
Fpz-Cz, Pz-Oz and horizontal EOG. REM is defined in part by rapid eye movements. The same
confound may carry that claim too.

## Test
A1's statistic (`_ratio`), imported unchanged, on the 7 cached recordings (4 subjects), with the
dependence-preserving circular-shift null of `discrimination_null_dependence_audit` (500 draws),
computed on (a) SPD(3) with EOG, as A1 did, and (b) SPD(2) over Fpz-Cz and Pz-Oz only. Pass rule
as A1: ratio > 1 and p < 0.05. Subject-level reporting: a subject passes if all its recordings pass.

## Pre-registered criterion
- **Discrimination survives without the eye** iff the EEG-only arm passes in at least as many
  subjects as the with-EOG arm, minus one.
- Otherwise the sleep replication of structural sensitivity is **attributed to the EOG channel**,
  and Paper 3 may not cite the sleep 14/15 as evidence that the EEG geometry is sensitive to
  structural regime.
- n = 4 subjects: descriptive, no significance claim at the subject level.
