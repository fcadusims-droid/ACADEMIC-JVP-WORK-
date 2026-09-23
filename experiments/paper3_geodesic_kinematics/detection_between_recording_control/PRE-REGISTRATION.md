# Pre-registration: does the held-out detection AUC detect a state change, or a recording change?

**Status:** pre-registered before the run. One run, no tuning loop.

## Why this exists
`detection_repair_heldout` validated the scale-normalised CUSUM detection statistic out of sample:
AUC 0.824 on eegmmidb eyes-open/closed, above a 0.70 bar. Its **positive** segments splice two
separate recordings, R01 (eyes open) and R02 (eyes closed). Its **null** segments lie inside one
recording. That is the same asymmetry `between_recording_control` found in the eyes-open/closed
ratio: a statistic that fires on any change of recording would pass this test without detecting
any change of state. It is the last positive real-data result in Paper 3, so it needs the
control.

## Design
- **Statistic:** the scale-normalised CUSUM peak, `stat_scale_normalised(cusum_curve(covs), covs)`,
  imported unchanged from `detection_statistic_repair`.
- **Pipeline:** the covariance pipeline of `detection_repair_heldout`, unchanged:
  - occipito-parietal channels, alpha 8–13 Hz, filtered and z-scored per run;
  - 1 s windows with a 0.25 s step;
  - eigen-floored, trace-normalised covariances.
- **Data:** subjects S001–S015. Runs R01, R02, R03 and R07; R03 and R07 are the real open/close-fist
  task runs.

### Chunk construction
T0 rest exists only as 4.2 s intervals separated by 4.1 s of task. So that every condition has
the same chunk structure, all segments are built from **4.2 s chunks spaced 8.3 s apart** (the T0
spacing), 6 chunks per side:
- In R03 and R07, the chunks are the first 6 or 12 T0 intervals.
- In R01 and R02, the chunks start at 0, 8.3, 16.6, … s.

### Segment types
- **OC:** 6 chunks of R01 followed by 6 chunks of R02. The recording changes and the state
  changes.
- **SS:** 6 T0 chunks of R03 followed by 6 T0 chunks of R07. The recording changes and the state
  does not. `between_recording_control` found T0 alpha consistent with eyes open in 14/15
  subjects.
- **WN (within-recording null):** 12 T0 chunks of R03. Neither the recording nor the state
  changes.

## Pre-registered criteria
**Primary, D1 — does detection see the state beyond the recording change?** Compute the AUC of
the statistic with OC as positives and SS as negatives.
- **State detection shown** iff AUC(OC vs SS) ≥ 0.70, the same bar as the held-out test.
- **Not shown** iff AUC(OC vs SS) < 0.60. Then the held-out 0.824 is not evidence of state
  detection, and Paper 3 must say so.
- Between the two, **weak / inconclusive**.

**Secondary, D2 — how much does a recording change alone fire the statistic?** Compute
AUC(SS vs WN). If it is ≥ 0.70, the statistic responds to recording changes by itself, which is
the confound this control exists to measure.

**Also reported:** AUC(OC vs WN). This is the held-out design rebuilt on the chunked
construction, and it shows whether chunking itself changes the held-out figure.

## Declared limits
- SS compares task-run rest periods, not a second pure baseline. Task context (cueing,
  post-movement rebound) differs from R01, and that difference could raise SS's statistic. This
  biases D1 **against** the method. D2 measures the recording-plus-context change directly.
- n = 15 subjects. The AUCs are unpaired, over 15 positives and 15 negatives, so an AUC has an
  uncertainty of roughly ±0.1.
