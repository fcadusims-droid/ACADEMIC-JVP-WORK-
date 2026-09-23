# Pre-registration: how common are these five traps in published covariance/Riemannian EEG studies?

**Status:** pre-registered before any paper was selected or read. Selection and coding rules fixed
here. One pass, no re-selection.

## Why this exists
Paper 3 is being restructured as a methodological negative built on five trap mechanisms:
- (1) centre bias;
- (2) a null or validation that ignores dependence between windows;
- (3) pseudo-replication;
- (4) ocular contamination;
- (5) confusion between recordings.

A reviewer will ask whether these are traps of this method or of the field.
`mdm_trap_control` tests the field's standard pipeline. This survey asks the complementary
question: how often do published studies leave these traps open?

Without the survey, the claim that the traps are general is asserted, not shown.

## Selection (fixed)
- **Source:** Europe PMC REST API (`europepmc/webservices/rest/search`), `resultType=core`, default
  relevance order, restricted to open-access full text.
- **Query (verbatim):**
  `(EEG OR electroencephalogra*) AND ("Riemannian" OR "covariance matrices" OR "SPD matrices") AND OPEN_ACCESS:y AND PUB_YEAR:[2012 TO 2025]`
- **Inclusion:**
  - An empirical study using EEG covariance or SPD-matrix features to classify, discriminate or
    detect brain states, conditions or transitions.
  - Full text retrievable from Europe PMC.
- **Exclusion:**
  - reviews and tutorials;
  - simulation-only studies;
  - non-EEG modalities only (MEG-only or fMRI-only);
  - papers whose methods section cannot be retrieved.
- **Stopping rule:** walk the results in the returned order and include the first **20** papers
  that meet the criteria. Record every excluded paper and the reason.

## Coding (fixed)
Each trap is coded for each paper as **Yes** (left open), **No** (addressed) or **Unclear**. Each
code is recorded with the sentence(s) from the paper that support it. Where a trap does not arise
in the study's design, it is coded **N/A**.

1. **Centre bias.** Applies only to studies that localize a transition in time. **Yes** if the
   analysis window is built around the known transition and no off-centre or shifted-window
   control is reported.
2. **Dependence ignored in validation or nulls.** Applies to any study that reports
   cross-validated accuracy or a permutation or resampling p-value.
   - **Yes:** epochs or windows from the same continuous recording are assigned to train and test
     folds at random (i.i.d. k-fold or shuffled split), or permuted as if exchangeable, with no
     blocking by time, trial block, session or subject.
   - **No:** folds are blocked (chronological, session-wise, subject-wise, or leave-one-run-out).
   - **Unclear:** the fold construction is not described.
3. **Pseudo-replication.** Applies to studies pooling several recordings per subject.
   - **Yes:** multiple recordings of the same subject are treated as independent units in the
     statistical inference, or subjects are not grouped when pooled data are split into train
     and test.
4. **Ocular contamination.** Applies to studies whose conditions plausibly differ in eye movements
   or blinks: eyes open or closed, sleep stages, visual or attentional tasks, motor imagery with
   cues, emotion with visual stimuli.
   - **Yes:** EOG or frontal channels are in the covariance and no ocular artefact removal
     (regression, ICA ocular components, rejection) or EOG control is reported.
   - **No:** such removal or control is reported, or the frontal and EOG channels are excluded.
5. **Recording confound.** Applies when the classes come from separate recordings (runs or
   sessions).
   - **Yes:** each class was recorded in its own run or session, so class is confounded with
     recording, and no same-condition cross-run control is reported.
   - **No:** conditions are interleaved within runs (for example, cue-based trials).

## Reporting
- A per-paper table with codes and supporting quotations.
- For each trap, the number coded Yes over the number where it applies (Yes + No + Unclear),
  and the number of Unclear codes shown separately.

No threshold is set in advance for calling a trap "common". The counts are reported as they are,
and Paper 3's framing follows `mdm_trap_control` together with these counts.

## Declared limits
- **One coder** (the AI assistant, under the author's direction), with no second rater. Every
  code carries its quotation, so any reader can re-code.
- **Open-access only.** This may not represent the whole literature.
- **n = 20.** The counts are descriptive only.
