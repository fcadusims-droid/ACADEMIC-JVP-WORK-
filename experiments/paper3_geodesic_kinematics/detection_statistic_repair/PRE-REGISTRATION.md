# Repairing the Geodesic CUSUM's Detection Statistic (Paper 3)

**The most serious weakness in the most publishable paper.** The baseline benchmark
established that the geodesic CUSUM leads on *localisation* (10/15 vs the best
baseline's 8/15) but is the **worst method compared** on detection: its confidence
statistic scores AUC **0.227** at separating a real-transition segment from a null
within-stage segment, against 0.67–0.88 for the baselines. An AUC below 0.5 is not
merely poor — it is **anti-correlated**: the statistic is systematically *larger* on
segments containing no transition. The detector localises well when told a transition
exists, and cannot itself tell whether one does.

## Diagnosis (stated before the repair, and itself testable)

The benchmark's confidence statistic was the CUSUM curve's peak-to-median ratio,
`max|S| / median|S|`. Real and null segments were matched in length, so segment
length is *not* the confound. The suspected mechanism is the **shape** of the curve:

- Under a genuine change point the cumulative-sum curve is a **tent**: it rises to a
  peak and falls back, so `median|S|` is of the same order as `max|S|` and the ratio
  is modest (≈ 2 for an ideal triangle).
- Under no change point `S_t` is a **driftless random walk**, which spends much of its
  time near zero while still making large excursions, so `median|S|` is small and the
  ratio is *large*.

If that is right, the peak-to-median ratio rewards the null by construction, and the
sub-0.5 AUC is an artefact of statistic design rather than a property of the geometry.
The diagnosis is checked directly (H1 below) before any repair is scored, because a
repair that works for the wrong reason is worth little.

**H1 (diagnostic):** on null segments the CUSUM curve is less tent-like than on real
segments — measured as the $R^2$ of a best-fit symmetric tent — while its
peak-to-median ratio is *higher*. Both directions must hold for the diagnosis to stand.

## The four repairs, tested in order of cost

- **(a) Scale-normalised peak.** Replace the ratio with `max|S|` standardised by the
  segment's own increment scale and length, `max|S| / (σ̂ √n)` — the classical
  normalisation, which makes the statistic comparable across segments.
- **(b) Surrogate calibration.** Convert the raw peak into a per-segment *p*-value
  against a null built by block-bootstrapping that segment's own increments, so what
  is compared across segments is a calibrated tail probability rather than a raw
  magnitude.
- **(c) Tent shape rather than peak height.** Score the $R^2$ of a best-fit symmetric
  tent to `|S_t|`: a change point produces a triangular profile, a drift or random
  walk does not. This uses the geometry of the curve instead of its amplitude.
- **(d) Two-stage detector.** Use the `window_mean` break curve — whose AUC of 0.578
  is already the best of this paper's three detectors — as the **detection gate**, and
  the CUSUM purely as the **localiser**. This exploits the trade-off the benchmark
  itself exposed: the CUSUM bought localisation by selling detection.

## Pre-registered success criterion (fixed before running)

A repair **succeeds** if, on the same 15 Sleep-EDF recordings and the same real/null
segment pairs used in the benchmark:

- **detection AUC ≥ 0.70**, and
- **localisation ≥ 9/15** — i.e. it costs at most one hit against the current 10/15.

Both must hold. A repair that lifts AUC by sacrificing two or more localisation hits
is a different detector, not a fix, and is reported as such.

**If no repair passes**, the result is a **declared structural limitation**, and the
consequence for the paper is stated now so it cannot be softened later: Paper 3 must
retreat its ambition from *on-line demarcation* — which requires deciding whether a
transition is present — to **assisted localisation**, i.e. locating a transition whose
existence is established by other means. That retreat would be written into the
abstract and conclusion, not a footnote.

Ties are resolved toward the simplest repair. All four are reported with their full
numbers whether or not they pass; no threshold is adjusted after seeing results.

## Status
Run. Verdict: **REPAIRED — the weakness was statistic design, not geometry.**

H1 was confirmed in both directions *before* the repairs were scored: the CUSUM curve
is more tent-like on real transitions (median $R^2$ 0.826 vs 0.704) **and** the
peak-to-median ratio is higher on nulls (1.80 vs 1.53), which is exactly the predicted
mechanism.

| statistic | detection AUC | localisation | |
|---|---|---|---|
| peak/median (benchmark) | 0.227 | 10/15 | anti-correlated |
| **(a) scale-normalised** | **0.813** | **10/15** | **PASS** |
| (b) surrogate-calibrated | 0.391 | 10/15 | |
| (c) tent-shape $R^2$ | 0.653 | 10/15 | |
| (d) window-mean gate | 0.578 | 10/15 | |

The cheapest repair passes, and localisation is untouched because (a)–(c) rescore the
*same* curve. At 0.813 the detector ranks **fourth of nineteen** method-feature
combinations — competitive with, not superior to, the best baseline (0.880). The
retreat clause was therefore not triggered; Paper 3 keeps its on-line demarcation
ambition but now **specifies the detection statistic as part of the method**, which is
what it had left implicit. See `_results/detection_statistic_repair/result.json`.
