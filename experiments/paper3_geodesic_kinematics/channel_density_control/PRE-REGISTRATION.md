# Channel density: the two between-recording controls with 64 channels (E3.3)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E3.3). Paper placeholder: R3.3 (Paper 3, §3.8). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Method
`between_recording_control` and `detection_between_recording_control` are re-run with all 64 EEGMMIDB
channels in place of the seven occipito-parietal ones. Nothing else changes: filtering, windows,
statistics, subjects, seeds. The relative-alpha scalar is computed on the same 64 channels, since the
original code computes it on whatever channels the geometry uses.

## Criterion (the plan's)
The results depend on channel density if both hold:
- with 64 channels, the eyes-open/closed ratio exceeds the same-state control in at least 12 of 15
  subjects, with Wilcoxon p < 0.01 (one-sided, as in the original C1);
- the detection statistic separates a change of state from a same-state change of recording at
  AUC ≥ 0.80 (0.72 with seven channels).

## Reported
Per-subject ratios, the count, p, the two AUCs, and the same measures for relative alpha power with
64 channels.
