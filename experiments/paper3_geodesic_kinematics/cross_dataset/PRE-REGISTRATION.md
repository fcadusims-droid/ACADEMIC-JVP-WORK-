# Experiment C — Cross-Dataset Test on a Stronger Structural Transition (Paper 3)

**Run order: 4th.**

## Question
Does on-line localization fail because *the method* is inadequate, or because
*this paradigm* (eyes-open/eyes-closed alpha against spontaneous alpha) is
adversarial — the spontaneous fluctuation is as large as the transition? Test on
a dataset where the transition is structurally stronger than the background
oscillation.

## Method
Apply the same square-root-metric detector (with the Exp A/B improvements) to a
paradigm with slower but more consistent structural transitions:
- **Primary:** PhysioNet Sleep-EDF sleep-stage transitions (slower, more
  consistent than alpha).
- **Secondary (if a public set is available):** an anesthesia induction/emergence
  record.
Same ±2 s (or stage-appropriate tolerance) localization scoring.

## Pre-registered success criterion
Localization materially better than the 5/15 alpha baseline on at least one
alternative paradigm, **isolating** "the method fails" from "this paradigm is bad
for the method". A clear win here + failure on alpha ⇒ scope statement, not method
death.

## Pre-registered failure criterion
If localization is at chance on a paradigm whose transition is *known* to be
structurally strong, that is stronger evidence of a genuine method limitation than
the alpha failure alone, and must be reported as such.

## Stopping rule
Part of the A+B+C decision: after C, issue a clear verdict — ready for
pre-registration of a confirmatory study, or needs a structural method change
(e.g. replacing the square-root metric with a hybrid metric, which is a change of
method, not a tuning fix).

## Data
See `../DATA.md`. Sleep-EDF is openly downloadable from PhysioNet.

## Status
Pre-registered. Not yet implemented.
