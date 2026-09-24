## What this paper is

A methodological negative. It records how a geometric method for EEG — trace-normalized
covariance matrices on the SPD manifold, read through a geodesic change-point statistic —
passed a series of tests that later, pre-registered controls showed it had not passed. The
record is organized as five trap mechanisms. For each it gives what the trap did to the result,
the control that exposed it, whether the field's standard Riemannian pipeline falls into it, and
how often published studies leave it open.

It is logically independent of its two companions.

## The five traps

- **Centre bias.** Localization windows were centred on the true transition, so a detector that
  guesses the middle scores every recording. Off-centre, the geometry's lead over a scalar
  detector became a tie (10/22 vs 10/22). At full scale the scalar was ahead (59/151 vs 67/151,
  not significant) (`localization_centerbias_control`, `h1_powerup_offcentre`).
- **Nulls and validation that ignore dependence.** Permuting autocorrelated windows as if
  exchangeable made an eyes-open/closed effect look like ≈3.3× and significant in 14/15. Against
  within-recording drift it is ≈1.3× (`eeg_reconciliation`, `regime_referent_nulls`).
- **Pseudo-replication.** Seven sleep recordings were four people. The record-level p of 0.0078
  had no subject-level counterpart (`regime_referent_eog_control`).
- **Ocular contamination.** A sleep-staging association and an N2-vs-REM discrimination were
  carried by the EOG channel in the covariance (`regime_referent_eog_control`,
  `discrimination_eog_ablation`).
- **Confusion between recordings.** The eyes-open/closed effect compares two separate
  recordings against the drift within one. It beats a same-state between-recording control
  only weakly, and per-channel alpha power separates the states more strongly. The detection
  statistic also fires on a change of recording alone (`between_recording_control`,
  `detection_between_recording_control`).

## Method or field?

- **Standard pipeline.** A pre-registered control ran the field's standard pipeline
  (covariance → MDM, pyRiemann) through the four traps that apply to classification. None
  applied at its pre-registered bar on these data (`mdm_trap_control`), so by the
  pre-registered rule these are traps of *this method*. Two same-state recordings were still
  told apart at 0.65: below the bar of 0.70, but above chance.
- **Design, not classifier.** The standard pipeline keeps absolute power, which this method
  divides out, and it was run on non-overlapping epochs. So the defensible reading is traps of
  this *design*. The paper offers this as interpretation: removing power removes the dominant
  signal and leaves the statistic answering to artefacts.
- **Published studies.** A pre-registered survey of 20 published covariance/Riemannian EEG
  studies measured what they report (`trap_literature_survey`). For two of the traps,
  published practice often does not let a reader rule them out:
  - ocular handling: unreported in 7/19 studies, unclear in 8 more (7–15/19);
  - dependence-respecting validation: not respected in 4/19, unclear in 8 more (4–12/19).

  One of those studies measured the dependence trap directly for the standard classifier, at up
  to 12.7 %.

## What survives

- A repair to the detection statistic (AUC 0.227 → 0.813). Its out-of-sample evidence for
  detecting a change of state is marginal.
- A synthetic base-metric result.
- On real data, nothing the method does better than a scalar baseline.

The original construction — vector bundle, jump-diffusion, three-regime demarcation — was never
shown to work. It is preserved as a draft in the repository, not presented in the paper.
