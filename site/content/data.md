Every dataset used is public. None is redistributed here: `experiments/data/` is
gitignored, and each experiment's runner downloads what it needs. What *is* committed
is the record — pre-registrations, `result.json` files, and figures — so that a
result can be inspected without re-acquiring the data, and re-derived by anyone who
does acquire it.

## Corpora

**Sleep-EDF Expanded** (PhysioNet). Polysomnography with expert sleep staging. Used
for structural discrimination (N2 versus REM), for within-trajectory sleep-onset
localization, for the structure-versus-power dissociation, for the log-Euclidean
comparison on real EEG, and as the corpus for the baseline benchmark and the
detection-statistic repair. Fifteen recordings from eight subjects — both nights per
subject, which is why the recording count and the subject count differ and are
reported separately.

**EEG Motor Movement/Imagery database** (PhysioNet; Schalk et al. 2004). Used twice.
First for the original feasibility probe: a *power* transition (rest versus hand
movement) that the trace-normalized geometry is predicted to miss, and a *structural*
transition (eyes-open versus eyes-closed) that it is predicted to catch — both
predictions held, and the contrast is the result. Second, and independently, as the
held-out corpus for validating the detection-statistic repair on a paradigm that
played no part in selecting it.

**I-CARE** (PhysioNet). Post-cardiac-arrest ICU cohort with concurrent EEG and ECG
and a recovery-versus-non-recovery contrast. The only public corpus found to carry
all three properties CBRA's positive arm requires. It is where that arm was tested,
and where it halted.

## Synthetic generators

A substantial fraction of the suite is synthetic by design rather than by
necessity — the questions are about *instruments*, and an instrument is best
characterized against a signal of known character. The jump-diffusion simulators, the
double-well explorer, the Class G witness and its near-misses, the criticality
generators and the IAAFT surrogate machinery all live in `experiments/shared_lib/`
and in the individual runners.

The scope limit is stated wherever it applies: a synthetic result is evidence about
the method, never about biology.

## Provenance and the gate

Which datasets were even *candidates* is itself a pre-registered result. The
viability gate searched for corpora with concurrent cardiac and neural recording, an
I+/I− contrast, and adequate record length. VitalDB is purely I+; the sleep banks are
all I+; MIMIC-scale ICU data lacks concurrent EEG; seizure banks lack cardiac
recording and the I-status contrast. I-CARE passed, narrowly, subject to two further
empirical gates — and one of those gates is what stopped the track.
