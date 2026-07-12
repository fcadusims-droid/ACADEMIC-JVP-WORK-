# Global permanence-aware localization on REAL EEG (Paper 3 headline claim)

**Run after** `real_eeg_localization` showed the window-mean persistence detector
— which solved the *synthetic* localization (2/15 → 15/15) — stalls on **real**
EEG (large window 4/15, fragile 2/15). The diagnosed reason: spontaneous alpha
bursts are *sustained*, so a window-mean cannot separate "sustained-and-recurrent"
(a burst that passes and the pre-state returns) from "sustained-and-permanent"
(the true transition). This is the single most consequential open problem in the
trilogy — it is Paper 3's **headline operational claim** (localize a transition
*within one continuous trajectory*), and it has not yet been attacked with a tool
built for the transient-vs-permanent distinction.

## The tool the window-mean lacks: a GLOBAL change-point view
The window-mean is *local* — it compares two adjacent short windows, so a large
transient burst beats the true seam. The fix is a statistic that sees the **whole
trajectory** and asks, for a candidate change-point τ, whether the record splits
into two internally-homogeneous, mutually-distant regimes that each *persist* —
which a transient burst cannot satisfy, because averaging [τ, end] over a
burst-that-returns washes the burst back toward the pre-state.

Two global detectors are tested, both permanence-aware by construction:

1. **Geodesic change-point F-ratio (duration-penalized LR)**: for each candidate
   split τ (with a minimum segment length), score
   `F(τ) = d(mean_pre, mean_post) / (scatter_pre + scatter_post)`, where the
   scatter is the mean geodesic dispersion of each segment about its Fréchet mean.
   A permanent shift maximizes between-mean distance at low within-scatter; a
   burst inflates the scatter of the segment that contains the burst-and-return,
   so it is penalized. `argmax_τ F` is the estimate. This is the minimum-duration
   likelihood-ratio the last review asked for.
2. **Geodesic CUSUM**: project each window's tangent deviation from the global
   Fréchet mean onto the first-quarter→last-quarter change direction, and take the
   classical CUSUM change-point `argmax_t |S_t|` (min segment enforced). A
   permanent step gives a tent peaking at the step whose height scales with the
   *remaining record length*; a transient burst gives a smaller bump scaling with
   its short duration — the permanence advantage, from standard change-point theory.

## Tested DIRECTLY on real EEG — no synthetic tuning
Same 15 cached subjects, same channels/band/segments as `real_eeg_localization`;
concatenate an eyes-open and an eyes-closed segment (each amplitude-normalised, so
the seam is structural) and ask each detector to find the seam blind. The
window-mean large-window detector is re-run head-to-head as the baseline. **No
parameter is fit on the real data**; the detectors are specified here before the
run. The last review's warning is explicit: synthetic detector engineering has
diminishing returns because it risks solving the *model* of the problem, so this
is judged on real EEG only, with a one-to-two-attempt budget.

## Pre-registered success/failure criteria (localization hit = |err| ≤ 2 s)
- **SOLVED** if a global detector reaches **≥ 10/15** — it localizes the real
  transition, turning Paper 3's headline claim from "open" to "supported on real
  EEG". Report which detector and its median error.
- **MATERIALLY BETTER** if a global detector reaches **8–9/15** — a real,
  substantial improvement over the window-mean's 4/15, though not a full solution;
  the claim is "improved but still imperfect".
- **MARGINAL** if the best global detector reaches **6–7/15** — better than the
  window-mean but inside the zone the review flagged: give it its budget, then
  accept the honest conclusion below rather than chase more detectors.
- **REAL METHOD LIMITATION (not a bug)** if the best global detector is **≤ 5/15**,
  i.e. no better than the window-mean. Combined with the marginal case, the honest
  verdict then becomes: **the trace-normalised geometry discriminates a structural
  regime (validated, `eeg_reconciliation`) but does not localize the transition
  on-line within a single trajectory of this signal type — a genuine limitation of
  the method, not a bug to hunt indefinitely.** This is a publishable negative
  result and bounds Paper 3's operational claim honestly.

## Stopping rule
Two global detectors (F-ratio, CUSUM), one run each on the 15 real subjects.
Whatever the outcome, it is reported against these criteria. The source of truth
is `_results/online_localization_cusum/result.json`; the verdict is held to the
hit count it shows and does not round toward the headline claim. If neither global
tool clears the marginal band, the "real method limitation" verdict is issued and
no further detector is proposed on this signal — the budget is spent.

## Status
Run. Verdict: **MATERIALLY BETTER, NOT SOLVED** — the global CUSUM reaches
**8/15** (median err 2.0 s), **doubling** the local window-mean's **4/15** on the
same real subjects. The permanence principle — implemented as a *global*
change-point view rather than a local window comparison — is a real, principled
improvement to Paper 3's headline on-line-localization claim, but it does not
reach the SOLVED band (≥10/15): ~half the subjects still fail, often badly
(5–13 s errors), because real spontaneous alpha bursts are both sustained *and*
geometrically comparable to the transition.

Detector comparison (localization hit = |err| ≤ 2 s, 15 real subjects):

| detector | hits | note |
|---|---|---|
| window-mean (local, baseline) | 4/15 | the detector that stalled |
| F-ratio (global weighted LR) | 6/15 | boundary spike fixed by the textbook `n_pre·n_post/N` weighting (3/15 → 6/15); hits ⊂ CUSUM |
| **CUSUM (global)** | **8/15** | best; strictly contains the window-mean's hits, adds 4 subjects |

CUSUM strictly dominates and its hits are a superset of both others, so 8/15 is
the honest ceiling of this attempt (no ensemble exceeds it). Budget (1–2 attempts)
spent; per the stopping rule, no further detector is proposed. Honest bound for
Paper 3: the trace-normalised geometry **discriminates** a structural regime
(validated, `eeg_reconciliation`) and a global CUSUM **roughly doubles** on-line
localization on real EEG, but **on-line single-trajectory localization is improved,
not solved** — it remains a real, partial limitation for this signal type. Source
of truth: `_results/online_localization_cusum/result.json`.
