# Experiment H — Statistical Power of the Dissociation Test (Paper 2)

**Run order: 8th (first of Phase 3).** Simulation cannot confirm CBRA; it can only
say whether the statistical design is feasible.

## Question
The identity-linkage dissociation test `M_diss` (Paper 2, Sec. 14.1) contrasts an
identity-linked channel against a generic structured process. At what **sample
size, SNR, and degree of matching** between the `S^{I+}` and `S^{I-}` conditions
does the interaction test reach reasonable power (e.g. 80%)?

## Method
Simulate synthetic data under two hypotheses — "channel linked to identity `I`"
vs. "generic structured process" — with controlled SNR and `S^{I+}`/`S^{I-}`
matching. Sweep sample size × SNR × matching. Estimate the power of the
interaction test to distinguish the two hypotheses at each grid cell.

## Pre-registered success criterion (of the design, not of CBRA)
A clearly identified region of (sample size, SNR, matching) reaching ≥ 80% power
**within ranges realistic for experimental anesthesiology** (sample sizes on the
order of what such studies actually recruit).

## Pre-registered failure criterion
If ≥ 80% power requires sample sizes or SNR that are unrealistic for the target
experiments, that is a **practical limitation** and must be stated in the paper as
such — not only the ethical caveat already present.

## Stopping rule
One pre-fixed grid. The deliverable is a feasibility verdict, not a positive
biological result.

## Status
Pre-registered. Not yet implemented.
