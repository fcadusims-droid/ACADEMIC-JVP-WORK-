# Trilha A3 — Log-Euclidean Base Metric on Real EEG, and the Weak-Collapse Cost (Paper 3)

**Closes the loop the BaseMetric experiment left open.** BaseMetric
(`base_metric_corner`) showed *synthetically* that switching the anti-development
base metric from the committed square-root (Bures-angle) sphere to the flat
**log-Euclidean** metric resolves the Exp D weak-collapse × strong-drift corner
(worst-corner AUC 0.65 → 0.96), because a flat connection accumulates zero holonomy
so a drift cannot manufacture a jump. Two things were never checked: (1) whether the
log-Euclidean geometry is even *viable* on **real** EEG detection tasks (the corner
result was synthetic), and (2) the **cost** of the switch — its jump power on a
*weak* collapse, which the BaseMetric grid computed but the paper never states.

## Part 1 — Real-EEG viability: square-root vs log-Euclidean, same tasks
On the same 15 Sleep-EDF recordings and pipeline as Trilha A1, run **both** the
structural-discrimination and the localization tasks under **each** base metric:

- **square-root**: the committed round-sphere geometry (geodesic distance =
  `2 arccos(tr √ρ₁ √ρ₂)`), mean on the sphere, CUSUM on the sphere embedding —
  A1's exact detectors.
- **log-Euclidean**: the flat metric. Each covariance is embedded as
  `flatten(log ρ)` (a Euclidean vector, since the metric is flat), so the mean is
  the Euclidean mean of the log-embeddings, distances are Euclidean, and the CUSUM
  is the ordinary Euclidean cumulative-sum change-point on those vectors.

Metrics compared per recording: the N2-vs-REM between/within ratio (structural
discrimination) and the sleep-onset CUSUM localization hit (±30 s), under each
geometry.

- **Pre-registered read:** log-Euclidean is *viable on real EEG* if its
  discrimination pass-rate and localization hit-rate are **within 2/15** of the
  square-root detectors' (i.e. the flat metric does not break real structural
  detection). If log-Euclidean **matches or beats** square-root, that strengthens
  it as a usable alternative; if it is **> 2/15 worse**, the flat metric's
  real-EEG cost is recorded as a reason the square-root sphere stays the default.

## Part 2 — The weak-collapse jump-power cost (state the number)
From the BaseMetric grid (recomputed here for a self-contained record, same
generator), report the jump power at the **weak** collapse (factor 0.7) under each
metric, alongside the corner-AUC gain, so the paper carries the full trade-off:

- **Pre-registered reporting:** the pair (weak-collapse jump power, worst-corner
  AUC) for square-root vs log-Euclidean. The expected shape (from BaseMetric) is
  that log-Euclidean wins the corner (AUC ↑) but loses weak-collapse sensitivity
  (power ↓); the number is stated, not spun. No threshold is tuned.

## Verdict logic
The experiment reports a **trade-off table**, not a winner: (corner AUC, weak-
collapse power, real-EEG discrimination, real-EEG localization) for square-root and
log-Euclidean. The honest recommendation follows the numbers — log-Euclidean as a
*corner-specific* base metric (drift/jump-robust) if and only if its real-EEG
detection is non-inferior and its weak-collapse cost is acceptable for the target
application; otherwise the square-root sphere stays primary with log-Euclidean a
cross-check in the drift/jump corner (the BaseMetric recommendation, now tested on
real data).

## Fixed choices
Same 15 Sleep-EDF recordings/loader/bands/windows/permutation count as A1; same
BaseMetric generator and jump statistic for Part 2. No tuning of the 2/15 viability
band or any threshold after seeing results. Raw per-recording both-metric results
and the trade-off table go to `_results/log_euclidean_real_eeg/result.json`; the
prose claims no more than the table supports and records the recordings-vs-subjects
non-independence.

## Status
Run. Verdict: **trade-off, tested on real data.** Part 1 (real Sleep-EDF):
log-Euclidean is **viable** — N2-vs-REM discrimination sqrt 14/15 vs log-Euclidean
**15/15** (higher ratios throughout), sleep-onset localization sqrt 10/15 vs
log-Euclidean 10/15 (identical); within the pre-registered 2/15 band, and if
anything slightly better for discrimination. Part 2 (same generator as BaseMetric):
log-Euclidean wins the drift/jump corner (worst-corner AUC 0.65 → 0.96) but loses
weak-collapse sensitivity (factor-0.7 jump power **0.85 → 0.22**), recovering on
stronger collapses. Honest recommendation: log-Euclidean as a corner-specific
base metric / cross-check, square-root sphere primary (far higher weak-collapse
power). See `_results/log_euclidean_real_eeg/result.json`.
