# H1 — does the manifold beat a scalar, holding the detector fixed? (Paper 3)

**Written before the run.** `baseline_benchmark` already found geodesic CUSUM localises
sleep-onset in **10/15** records against a best cheap baseline of **8/15** and read that
two-recording margin as "inside binomial noise, not a demonstrated advantage". It did **not**
do the two things that would settle H1:

1. A **matched-detector** comparison. Every cheap baseline there used a *different algorithm*
   (ruptures/BOCPD/HMM/k-means) from the geodesic method's CUSUM, so a difference could be the
   detector, not the representation. This runs the **same CUSUM** on a **scalar band-power**
   series and on the SPD-manifold trajectory, so the only thing that differs is manifold-vs-scalar.
2. A **formal paired significance test** on the hit difference, rather than the eyeball
   "inside binomial noise".

The trace-normalised geometry is *power-blind by construction* (it discards the very band power
the scalar detector uses), and sleep-onset (W→N1) is partly a *power* event (occipital alpha
drops). So the sharp question is whether the manifold's power-blind structural view localises
sleep-onset any better than a one-line CUSUM on total band power.

## Method (both real paradigms already in the suite, pooled for paired power)
Following the H1 plan's "same 15–16 records already used (Sleep-EDF **and** eyes-open/closed)",
the matched-detector comparison is run on **both** paradigms and the paired hits pooled for one
McNemar test, so the discordant-pair count is large enough to resolve: Sleep-EDF sleep-onset at
±30 s, and eyes-open/closed alpha at ±2 s. Each record contributes one paired (manifold-hit,
scalar-hit) outcome at its own paradigm tolerance.
For each record, at its transition (sleep-onset, or the eyes-open/closed seam):
- **manifold–CUSUM:** the committed geodesic CUSUM on the trace-normalised SPD covariance
  trajectory (reused verbatim from `online_localization_cusum`).
- **scalar–CUSUM:** the classical CUSUM (argmax |cumsum of the centred series|) on a **scalar
  band-power** series — `log Tr(cov)` per window, the power the manifold throws away. Same
  windows, same min-segment guard, same tolerance.
- For breadth, also `ruptures` PELT and BOCPD on the same scalar series.

## Pre-registered criterion
- **Manifold earns its place (refutes H1):** manifold–CUSUM beats scalar–CUSUM by a
  **McNemar paired test at p < 0.05** on the 15 records (i.e. the discordant pairs favour the
  manifold significantly). Then the geometry adds something a scalar cannot.
- **H1 confirmed (bad news for Paper 3's geometry):** the two are statistically tied
  (McNemar p ≥ 0.05) and the manifold's hit count is within 1 of the scalar's. Then, on this
  task, the manifold representation is not doing measurable work beyond a one-line band-power
  CUSUM, and Paper 3's localisation contribution is the *permanence statistic* (CUSUM), not the
  *manifold*.
- **Inconclusive:** discordant-pair count too small for McNemar to resolve (report exact
  binomial and stop).

## Attempt budget
**One run, no tuning loop.** Detector, feature, tolerance and the test are fixed here. This is a
head-to-head with a fixed criterion, not a search for a configuration where the manifold wins.

## Status
Pre-registered. Not yet run.
