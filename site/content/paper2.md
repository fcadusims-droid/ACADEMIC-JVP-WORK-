## The question

Some interoceptive signals modulate how the brain responds to external input. Does any such
signal carry information specific to transitions a person *survives*, recovery as opposed to
non-recovery, when the two are matched on their surface dynamics? The paper does not assume such
a signal exists, and it does not equate non-recovery with loss of personal identity.

## What a test would need

Three properties in the same records:

- **P1:** a cardiac channel recorded concurrently with EEG;
- **P2:** transitions followed by recovery and transitions not followed by recovery, matchable
  on severity;
- **P3:** records long enough for a subsampling-robust estimate of distance to criticality, the
  leading rival explanation of structured transitional signals.

A bounded audit of five families of public corpora found one that has all three: the I-CARE
post-cardiac-arrest database.

## What happened

The first planned step checked whether the heart-period series carries nonlinear structure
beyond linear (IAAFT) surrogates in at least 60% of patients. As executed it passed in 6 of 21
pilot patients (29%), and the analysis stopped. An audit then found that the executed statistic
departed from the written plan: the code used the beat-indexed series, while the plan specified
4 Hz resampling. Follow-up analyses, specified before they were run, found:

- **The gate as written:** structure in 16 of 21 patients (76%), above the bar.
- **A beat-indexed multiscale version:** 15 of 21 (71%).
- **A positive control (Fantasia):** the gate passes in healthy young adults under both
  versions (19 and 17 of 20).
- **By outcome (50 + 50 patients, descriptive):** no clear difference (p = 0.16), but the groups
  differ markedly in age and arrest rhythm, so matching, not estimability, is the binding
  constraint.
- **Audit re-check:** VitalDB, classified from its documentation as lacking raw EEG, has it in
  5,871 of 6,388 cases; Table 1 is corrected.

## What the simulation audits show

- State-dependent perturbation efficacy is produced by critical dynamics without any gating.
- Subtracting a noisily measured common generator manufactures interactions, more so with more
  data.
- Outcome-defined contrasts manufacture dissociations unless matching is tight; about 40
  patients per condition are needed for 80% power at a moderate effect.
- Naive branching-ratio estimators on subsampled data certify near-critical systems as safely
  subcritical.
