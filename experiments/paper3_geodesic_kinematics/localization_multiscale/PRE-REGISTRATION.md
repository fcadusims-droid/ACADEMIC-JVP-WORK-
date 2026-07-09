# Experiment A — Multi-Scale Windows for On-Line Localization (Paper 3)

**Run order: 2nd.** Highest-priority *method-improvement* experiment: it targets
the protocol's principal open problem (on-line single-trajectory localization
succeeded in only 5/15 subjects; the true transition is often not the most abrupt
geometric event against spontaneous EEG variability).

## Question
Does running the causal detector at **multiple window lengths simultaneously** and
aggregating (by a vote or an aggregated likelihood ratio) recover on-line
localization, without reintroducing the drift/jump problem?

## Method
Extend the single-scale square-root-metric detector to a bank of causal window
lengths. Aggregate the per-scale break statistics into one localization decision.
Evaluate on the same concatenated eyes-open/eyes-closed records used in the
appendix (15 subjects), scored by whether the declared break falls within ±2 s of
the true seam. Baseline is the single-scale 5/15.

## Pre-registered success criterion
Improvement from **5/15 to at least 10/15** with error < 2 s, on the same
subjects, **without** reintroducing the drift/jump confusion (checked by carrying
Exp D's confusion metric on the same runs).

## Pre-registered failure criterion
If multi-scale aggregation does not reach ~8–10/15 robustly across random seeds
(seed variance smaller than the improvement), it is reported as **not a fix**, not
retried with ever-more scales.

## Stopping rule (honest, from the plan)
If after A + B + C localization does not robustly exceed ~8–10/15 across seeds,
report as a **confirmed limitation**, not hidden behind more attempts.

## Data
PhysioNet EEG Motor Movement/Imagery (eyes-open/eyes-closed records), as in the
appendix. `cross_dataset/` (Exp C) tests a different paradigm. See
`../DATA.md` for access notes.

## Status
Pre-registered. Not yet implemented.
