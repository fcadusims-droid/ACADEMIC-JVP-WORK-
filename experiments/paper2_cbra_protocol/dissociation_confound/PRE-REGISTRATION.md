# Experiment I2 — Does Criticality Alone Confound the Dissociation Test? (Paper 2, Sec 14.1)

**Extends Experiment I.** I tested whether a bare critical generator reproduces
the *stratified gating differential* the CBRA detection arm relies on, and found
it does (robustly, 15/24 cells). I did **not** test the *dissociation* test
(`M_diss`, Sec 14.1) — the statistic Experiment H's power analysis assumed is
valid and only asked whether it is well-powered. This is a real gap: H assumed
validity and measured power; I measured a different statistic's (`gating`)
confound. Neither checked whether `M_diss` itself is confoundable.

## Question
`M_diss` is diagnostic of an identity-linked channel because it shows a
preservation contrast: a macro-invariant survives a transition in the
identity-matched condition (S^{I+}) but not in the mismatched condition (S^{I-}).
Can a system with **zero identity-linked mechanism** — nothing that encodes or
reads "identity" at all — produce the *same qualitative contrast* merely because
S^{I+} corresponds to letting a critical/long-memory process **continue**
uninterrupted across the transition, while S^{I-} corresponds to **resetting**
it? If so, `M_diss` cannot distinguish "genuine identity-linked preservation"
from the trivial fact that any process with memory preserves more structure when
undisturbed than when perturbed — the confound would generalize from the gating
test to the dissociation test.

## Method
Three generators, all producing a macro-invariant preservation score `P`
(pre-transition vs post-transition state similarity) under a CONTINUE condition
(analogous to S^{I+}) and a RESET condition (analogous to S^{I-}):

1. **null (no dissociation)**: `P` is drawn from the same distribution under
   CONTINUE and RESET — no interaction, the honest negative control.
2. **identity-linked (the intended positive)**: `P` is high under CONTINUE and
   drops under RESET *because* the model explicitly encodes an identity-indexed
   channel that survives only when identity-matched continuity holds.
3. **bare critical (the confound candidate)**: a Galton-Watson critical branching
   process with NO identity mechanism whatsoever. CONTINUE lets the avalanche
   state carry over across the transition; RESET reinitializes it from a fresh
   seed. `P` is a generic macro-invariant (log avalanche size trajectory
   correlation) computed identically in both conditions.

Compute `D = mean(P | CONTINUE) − mean(P | RESET)` for each generator, across a
sweep of the branching ratio (criticality) and read-out noise, mirroring
Experiment I's grid.

## Pre-registered success criterion (M_diss survives)
The bare-critical generator's `D` stays well below the identity-linked
generator's `D` across the criticality/noise grid (e.g. < 40% of it), so a
plausible independent control (e.g. testing at sub-critical parameters, or a
magnitude threshold) could in principle separate "genuine identity dissociation"
from "any critical process with continuity broken." `M_diss` would need such a
control stated explicitly, but would not be fundamentally confounded.

## Pre-registered failure criterion (M_diss is confounded, like the gating test)
The bare-critical generator's `D` matches or exceeds the identity-linked
generator's `D` in a substantial part of the grid (as Experiment I found for
gating, at ≥ 50% of cells). This would mean `M_diss` — like the gating
differential — cannot on its own distinguish identity-linkage from generic
continuity-breaking in any near-critical system, and Sec 14.1 needs the same
demotion Sec 15.5 already gave the gating test.

## Stopping rule
One grid (criticality × read-out noise), matching Experiment I's parameter
ranges for direct comparability. No new discriminators invented mid-run.

## Status
Complete. See `../../_results/README.md` and `_results/dissociation_confound/result.json`.
Verdict: GROWING CONFOUND NEAR TRUE CRITICALITY (neither clean survival nor
clean confound — a third, more precise outcome than either pre-registered
branch anticipated; reported as such rather than forced into one bucket).
