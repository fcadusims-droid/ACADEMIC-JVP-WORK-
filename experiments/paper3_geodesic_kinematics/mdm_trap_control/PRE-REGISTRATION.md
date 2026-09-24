# Pre-registration: do this suite's traps affect the field's standard Riemannian pipeline?

**Status:** pre-registered before the run. One run, no tuning loop.

## Why this exists
Paper 3 is being restructured as a methodological negative. The paper documents how an
SPD-geometry EEG method looked validated and was not, through five trap mechanisms. A reviewer
will ask whether these are traps of *this* method or of the *field*. If they are traps of this
method only, the paper is a report of the author's own errors. If they are traps of the field,
the paper has general value.

What decides this is putting the field's standard classifier through the same controls. That
classifier is the covariance → MDM pipeline (minimum distance to Riemannian mean;
Barachant et al. 2012; pyRiemann). Of the five mechanisms, centre bias applies to localization,
not to classification, so it is not tested here. The other four are.

## Pipeline (fixed)
- **Classifier:** `pyriemann.estimation.Covariances(estimator="oas")` followed by
  `pyriemann.classification.MDM(metric="riemann")`, pyRiemann 0.12, defaults otherwise.
- **Metric:** balanced accuracy.
- **Sleep data:** PhysioNet Sleep-EDF sleep-cassette, all 153 cached recordings.
  - Loader: `sleep_stage_localization.load_subject` (0.5–30 Hz; the per-channel z-scoring is a
    diagonal congruence, to which the affine-invariant MDM is invariant).
  - Channels: Fpz-Cz, Pz-Oz and horizontal EOG.
  - Epochs: 30 s, labelled from the hypnogram.
  - Classes: N2 versus REM.
  - A record is used if it has at least 20 epochs of each class.
- **Eyes-open/closed data:** PhysioNet eegmmidb S001–S015.
  - Channels: the 7 occipito-parietal channels of `real_eeg_localization`, 8–13 Hz.
  - Epochs: 2 s, non-overlapping.
  - Recordings: R01 (eyes open) and R02 (eyes closed); T0 rest intervals of R03 and R07, using
    only epochs lying entirely inside one T0 interval.
  - Classes are balanced by truncating the larger class, in time order.
- **"Blocked" cross-validation:** 5 contiguous folds in time within each class, so that
  neighbouring epochs do not straddle train and test.

## Tests and pre-registered criteria
Each test asks whether the trap *applies to the standard pipeline*.

**T1 — Ocular contamination (EOG).**
- Design: within-record blocked 5-fold MDM, N2 versus REM, with and without the EOG channel.
  Accuracies are averaged per subject: the mean over that subject's records.
- Criterion: applies iff the median subject-level drop (with EOG minus without) is ≥ 0.05
  **and** the one-sided Wilcoxon p across subjects is < 0.05.

**T2 — Recording confound.**
- Design: within-subject blocked 5-fold MDM on two separate recordings of the *same* state,
  T0(R03) versus T0(R07).
- Criterion: applies iff the median subject balanced accuracy is ≥ 0.70. That is, the standard
  pipeline "discriminates" two recordings of one state as if they were two states.
- Reported alongside: R01 versus R02 (eyes open versus closed).

**T3 — Pseudo-replication (subject leakage).**
- Design: pooled cross-record MDM, N2 versus REM, on all usable records, evaluated two ways:
  - 5-fold `GroupKFold` with groups = recording (the two nights of a subject can fall in train
    and test);
  - the same with groups = subject.
- Criterion: applies iff the recording-grouped accuracy exceeds the subject-grouped accuracy by
  ≥ 0.03.

**T4 — Dependence between windows.**
- Design: within-record N2 versus REM, 5-fold CV with epochs shuffled (i.i.d. `KFold`, shuffle,
  seed 0) versus blocked 5-fold.
- Criterion: applies iff the median record-level difference (shuffled minus blocked) is ≥ 0.05.

## Framing decision (pre-registered)
- **If ≥ 2 of T1–T4 apply:** the paper is framed as traps of the field. The standard pipeline
  falls into them too.
- **If none applies:** it is framed as traps of this method, with the standard pipeline as a
  counter-example.
- **If exactly one applies:** the framing is mixed and stated trap by trap.

## Declared limits
- **MDM is a classifier, not a change-point method.** The traps are tested in the form they take
  for classification.
- **T4 compares two estimates of accuracy.** It shows how much i.i.d. validation flatters the
  pipeline, not a p-value's validity.
- **Subject counts:** n = 15 subjects for T2, and roughly 78 for T1 and T3. Sleep T1 accuracies
  are averaged per subject before the test.
