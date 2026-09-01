# Experiment B (real data) — Does causal smoothing of the predictability covariate help localization on real EEG?

**Follows:** `localization_priors` (synthetic Exp B) and the note in `abc_real_eeg`/STATUS:
"B smooths the predictability covariate **inside the jump-anchoring pipeline**, a different
object [from the break curve the ABC-Real analogue smoothed], so **B remains
synthetic-only**." This is the true replication — it smooths the *same object* B smooths.

## Question
Synthetic Exp B anchors the transition to `argmax(gamma_t)`, where `gamma_t` is the
predictability covariate `shared_lib.jump_diffusion.conditional_residual_variance` and its
`half_window` **is** the causal smoothing bandwidth. B swept that bandwidth and found
**NO BENEFIT (mechanistic)**: smoothing degrades localization, because an abrupt jump and a
sharp spontaneous excursion share a single-sample covariate signature, so smoothing blurs
the jump's peak faster than it suppresses spikes; the discriminator that works is
**persistence** (a window-mean), which a covariate argmax cannot exploit.

Does that mechanistic finding replicate on **real EEG**?

## Why this is the replication, not the `abc_real_eeg` analogue
- `abc_real_eeg` smoothed the **break curve** `S(t,w)` (a geodesic window-mean difference)
  → 7/16 vs 7/16, no help. That is a *different object*.
- This smooths the **predictability covariate `gamma_t`** and anchors at its `argmax` — Exp
  B's exact pipeline — on real EEG. The covariate is computed on the real structural
  trajectory (the √-embedded covariance sequence `E_t`, flattened), whose increments spike
  at a structural regime change and are transiently perturbed by real alpha bursts (the
  real counterpart of B's synthetic excursions).

## Data (already staged; loader reused verbatim)
eegmmidb eyes-open (R01) vs eyes-closed (R02), occipito-parietal alpha, concatenated with a
known seam at the join — the appendix paradigm where the 4–5/15 localization problem lives.
Loader `load_state_covs`/`sliding_covs` reused from `real_eeg_localization`; the covariate
from `shared_lib.jump_diffusion` unchanged.

## Method (fixed)
For each of the 15 subjects: build the √-embedded covariance trajectory `E_t` (flattened),
compute `gamma_t = conditional_residual_variance(E_flat, ar_rho=0.4, half_window=h)`, anchor
the transition at `argmax(gamma_t)`, and score a hit as `|argmax − seam| ≤ TOL` (TOL = 2 s =
8 windows, matching `real_eeg_localization`). Sweep `h ∈ {0,1,2,4,8,12,20,30}` windows
(matching synthetic B). `ar_rho = 0.4` matches synthetic B. Head-to-head: the persistence
detectors (large window-mean break curve; geodesic CUSUM) on the identical records, to test
B's claim that *persistence*, not covariate smoothing, is the operative discriminator.

## Sharpness guardrail (real)
Report the covariate peak prominence `max(gamma)/median(gamma)` at each `h`. B's guardrail
was "smoothing must not blur a genuine sharp jump"; the real counterpart is that prominence
must not collapse.

## Pre-registered decision
- **SUCCESS (smoothing helps on real data — would overturn B):** some `h > 0` with
  localization accuracy `> acc(0) + 0.05` **and** peak prominence `≥ 0.9 · prominence(0)`.
- **TRADE-OFF:** the only `h` that improves localization drops prominence by `> 10%`
  (robustness bought at the cost of the anchor) — smoothing not adopted.
- **NO BENEFIT (replicates synthetic B):** localization does not improve with `h` (flat or
  monotone decline). In this case the replication also checks B's *positive* claim — that a
  persistence detector localizes better than the covariate argmax on the same real records.

## Attempt budget & anti-tuning rule
**One run. No tuning loop.** Bandwidth grid, `ar_rho`, tolerance and the decision above are
fixed here before the run. An instrument defect is fixed on the instrument (recorded as an
addendum, outcome-independent), never by moving a threshold — per `METHODOLOGY.md`.

## Self-test gating the run
On a synthetic trajectory with a single clean structural seam and **no** bursts, the
covariate argmax at `h = 0` must localize the seam within tolerance — a covariate that
cannot find a clean structural jump cannot be trusted to be fooled by a real one. Run
aborts if it fails.

## Status
**Run. Verdict: NO BENEFIT ON REAL DATA — synthetic Exp B replicates.** Self-test passed
(covariate argmax found a clean structural seam at h=0). On 15 real subjects, causal
smoothing of the predictability covariate does **not** improve localization: covariate-argmax
accuracy is 1/15 at *every* bandwidth (0.07, flat), while peak prominence falls monotonically
12.33 → 1.70 as h grows — smoothing only blurs the anchor, exactly the mechanism synthetic B
described (an abrupt structural transition and a real alpha burst share the covariate's
single-sample signature). B's *positive* claim also holds on real data: the persistence
detectors localize better than the covariate argmax (window-mean **4/15**, CUSUM **8/15** vs
covariate-argmax **1/15**). B was synthetic-only; it is now replicated on real EEG. One run,
no tuning, no threshold moved.
