# Experiment AD — Window-Length Tension and Causal-vs-Offline Localization (Paper 3)

**Reconciles Experiments A and D**, closing a gap an independent review of this
repo identified: A concluded the localization fix is a **large** window; D found
that **longer** windows (T 200→800) make the drift/jump AUC *worse*
(0.99→0.76), because a longer look-back accumulates more chance of a
geometry-induced spurious event. Neither experiment tested this tension on a
single, shared apparatus, and A's large window is **symmetric** — i.e.
*offline* localization (it uses future data), not the *causal/online*
demarcation that is literally the headline operational claim of Paper 3's
abstract. The caveat was stated in A but its consequence was never measured.

## Question
1. On one detector and one generator family, does a large window that fixes
   localization *also* start firing spuriously on drift-only (no-seam) records
   as it grows — the same tension D found, now inside A's own apparatus?
2. How much localization accuracy is lost by using a genuinely **causal**
   (backward-only, no future data) window statistic instead of the symmetric
   window Experiment A actually used? Is there a window length that is *both*
   causal-accurate *and* guarded against drift-only false fires?

## Method
Reuse Experiment A's generator (`generate_subject`) and embedding machinery
(`embed_cumsum`) unmodified. Sweep window length `w` over a range from short to
large relative to the T=600 record. For each `w`, build two break-curve
variants:
  * **symmetric** (Experiment A's original): compares the mean embedding in
    `[t-w, t)` to `[t, t+w)` — uses future data, offline.
  * **causal**: compares the mean embedding in the recent window `[t-w, t)` to
    the entire **older history** `[0, t-w)` — uses only data up to `t`, online.

For each `(w, variant)` cell, measure on 15 subjects each:
  * seam-localization hit rate (`|argmax − true seam| ≤ tol`, as in A);
  * drift-only (no-seam) peak break-curve prominence, to see whether it grows
    with `w` (the same failure mode D found, inside this apparatus).

## Pre-registered success criterion
A window range exists where (a) causal localization hit rate is close to the
symmetric (offline) rate (within ~2/15), **and** (b) drift-only prominence stays
well below the seam prominence at that same window — i.e. a causal,
false-fire-guarded window exists and Paper 3's causal/online claim is
recoverable, not just its offline relative.

## Pre-registered failure criterion
Either (a) causal accuracy trails symmetric accuracy substantially at every
window that also guards against drift-only false fires (the online claim is not
recoverable with this apparatus, and Paper 3's abstract should be corrected to
state the method as offline/pooled), or (b) drift-only prominence grows with
window length inside this apparatus too (confirming the D-style tension is not
an artifact of D's specific geometric pipeline but a general property of
large-window detectors).

## Stopping rule
One window sweep, both variants, on Experiment A's existing generator
parameters (d_seam=0.45, excursion_size=0.7) for direct comparability. No new
generator tuning.

## Status
Complete. See `../../_results/README.md` and `_results/causal_vs_offline_localization/result.json`.
Verdict: CAUSAL CLAIM RECOVERABLE, AT AN EXPLICIT REPORTING-LAG COST — a more
precise outcome than either pre-registered branch: the causal claim survives
with the correct detector design (adjacent windows, not naive all-history), but
carries a quantified reporting lag (minimum 10 samples / 2% of the record at the
smallest guarded window). The D-style window tension was tested for directly and
did NOT reproduce inside this apparatus — the A/D "tension" is not a shared-window
conflict but two different sub-problems (localization vs drift/jump demarcation)
with independent, non-conflicting window dependencies.
