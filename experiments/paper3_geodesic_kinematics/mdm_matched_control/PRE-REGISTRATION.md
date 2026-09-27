# Matched control: the standard pipeline given this method's design (E3.1)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E3.1). Paper placeholder: R3.1 (Paper 3, §3.7). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Question
Does the standard pipeline (OAS covariance → MDM) fall into the dependence, ocular or recording
trap when it receives the same design as the method under test: trace normalization and
overlapping windows?

## Method: `mdm_trap_control` with exactly two changes
1. Each OAS covariance is divided by its trace.
2. Overlapping windows replace non-overlapping epochs:
   - eyes-open/closed task (EEGMMIDB R01, R02, and the T0 intervals of R03 and R07): 1 s windows,
     0.25 s step;
   - sleep (Sleep-EDF cassette): 2 s windows, 1 s step. A window is kept only if every sample lies
     in one scored N2 or REM stage.

Nothing else changes: pyRiemann 0.12, `MDM(metric="riemann")`, balanced accuracy, the same channels
and filtering, blocked folds (five contiguous folds within each class), shuffled `KFold(5,
random_state=0)`, `GroupKFold(5)` by recording and by subject, at least 20 windows per class, 15 EEG
subjects, and all usable sleep recordings.

## Criteria (the plan's)
- **Dependence (T4):** median over recordings of (shuffled − blocked) ≥ 0.05.
- **Pseudo-replication (T3):** pooled accuracy grouped by recording minus grouped by subject ≥ 0.05.
  (The original `mdm_trap_control` code used 0.03; the plan and the paper say 0.05, and 0.05 governs.)
- **Ocular (T1):** median subject-level accuracy drop without EOG ≥ 0.05. The one-sided Wilcoxon p is
  reported, but it is not part of the criterion. The original code also required p < 0.05; whether
  that stricter version holds is reported too.
- **Recording (T2):** median balanced accuracy on two same-state recordings (T0 of R03 against T0 of
  R07) ≥ 0.70.

## Reading rule (the plan's)
- If at least one of dependence, ocular or recording crosses its bar, the traps are **traps of the
  design** (trace normalization plus overlap, which this control does not separate), and §4.1 stands.
- If none does, the traps belong to the geodesic CUSUM itself, and §4.1's interpretation must be
  withdrawn.
- T3 is reported but is not part of the rule.

## Reported
The four numbers, each with its median and the per-subject (or per-recording) interquartile range
and min–max; `result.json`; the commit hash.
