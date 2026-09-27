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

The first pre-specified step checked whether the heart-period series carries nonlinear
structure beyond linear (IAAFT) surrogates. It passed in 6 of 21 pilot patients (29%), below a
60% bar, and the analysis stopped. The failure most plausibly reflects the known loss of
heartbeat time irreversibility in disease, compounded by sedation, cooling and vasopressors.
The gate had no positive control, so it is uninformative until one is run; the paper specifies
one (the Fantasia database), a beat-indexed multiscale version, an outcome comparison and an
audit re-check.

## What the simulation audits show

- State-dependent perturbation efficacy is produced by critical dynamics without any gating.
- Subtracting a noisily measured common generator manufactures interactions, more so with more
  data.
- Outcome-defined contrasts manufacture dissociations unless matching is tight; about 40
  patients per condition are needed for 80% power at a moderate effect.
- Naive branching-ratio estimators on subsampled data certify near-critical systems as safely
  subcritical.
