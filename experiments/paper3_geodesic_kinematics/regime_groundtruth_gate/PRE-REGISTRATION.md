# Phase 0 — Viability gate for the three-regime demarcation (Paper 3)

**Written before any dataset is inspected.** This gate decides whether Paper 3's *titular*
claim — that a single trajectory can be sorted into asymptotic geodesic drift, isotropic
fibre dispersion, or structural rank collapse — is testable **at all** on accessible data,
before a line of demarcation-scoring code is written.

## Why this gate exists
A coverage audit found that the three-regime demarcation has **never been run end-to-end on
a record**. Twenty-one experiments test *components* — localization, detection, the base
metric, structure-versus-power discrimination — and none issues the three-way verdict. An
external review then identified the likely reason, which an earlier roadmap had treated as a
configuration detail: **regime ground truth is the whole obstacle**. EEG supplies *states*
(N2, REM, eyes-closed); the demarcation claims *kinematic regimes* (drift / diffusion /
collapse). A state label is not a regime label, and scoring a three-way verdict against one
would be measuring agreement with the wrong thing.

## The single question
Does there exist **≥ 1 openly accessible, non-synthetic corpus** in which all **three**
properties hold simultaneously in the same records?

1. **Externally established regime ground truth.** The post-transition dynamics must carry a
   drift / diffusion / collapse label established **independently of this protocol** — by a
   controlled physical parameter, a known governing equation, or an accepted domain
   criterion. A label produced by the protocol itself, or a *state* label standing in for a
   regime, does not count.
2. **The protocol's own input requirements.** Multichannel, with separable slow and fast
   timescales and a trackable cross-scale coupling (Paper 3 §2), so the construction is
   applicable rather than forced.
3. **Post-transition length for the asymptotics.** §7 anchors the demarcation to asymptotic
   Lyapunov stability and to long-run stationarity of statistical complexity, "on a timescale
   long enough to exclude transient confounds". The record must supply that horizon after the
   transition, not merely span it.

## Decision criterion (fixed now, before looking)
- **PASS** — a non-synthetic corpus meeting all three is found and **named**. The
  three-regime demarcation is then executable, and the follow-up experiment runs it with the
  three-arm design below.
- **FAIL** — no such corpus is accessible. **This is a result, not a postponement.** Paper 3
  must then state that its titular claim is **not testable on existing accessible data**, in
  the same register the companion paper states its own halted arm — and the demarcation
  remains an unexercised construct rather than a supported one.
- **PARTIAL** — a corpus meets 1 and 2 but not 3 (or is paywalled/registration-gated rather
  than open). Reported as such, naming exactly what is missing, since that is actionable.

## Anti-rescue guard
Synthetic data satisfies property 1 by construction and is therefore **excluded from the PASS
condition** and listed separately as calibration-only. The repeated lesson of this suite is
that synthetic performance overstates real performance (Exp A: $2/15 \to 15/15$ synthetic
became $4/16 \to 7/16$ real); a synthetic-only PASS would restate that error as a finding.

## The design this gate unlocks (pre-registered here so it cannot be chosen after the fact)
If PASS, the demarcation experiment runs **three arms plus a co-primary baseline**:
- **Euclidean** (no trace normalization, no manifold),
- **trace-normalized flat** (log-Euclidean; zero holonomy),
- **trace-normalized curved** (square-root sphere; the paper's committed geometry),
- **co-primary comparator:** a simple three-state statistical classifier given the same
  features.

This is fixed in advance because the honest prior says it may hurt: the base-metric result
found holonomy *manufactures* pseudo-jumps and the **flat** metric wins the confusable
corner, and the fibre ablation found the bundle net negative. If flat ties curved and both
beat Euclidean only on the structure-versus-power axis, the supported claim is about
**trace normalization**, not about fibre-bundle geometry — and the three-arm design forces
that finding here rather than at review.

## Attempt budget
**One assessment.** The criterion above is fixed; a corpus that fails property 1 is not
promoted by relaxing what counts as a regime label.

## Status
**Run. Verdict: FAIL — and the reason is structural, which makes it a result rather than a
postponement.** All four candidate hosts answered 2xx/3xx, so access is not the obstacle;
property 1 is. No accessible non-synthetic corpus supplies an external
drift/dispersion/collapse label. The diagnosis is visible in Paper 3 §2 itself: the three
regimes are declared *operationally defined geometric regimes … not domain categories*. If the
regimes are defined **by** the protocol's own criteria, an external referent does not exist to
be found — the label *is* the protocol's output, so "does it classify correctly?" has no
independent truth-maker. The strongest candidate (JHU turbulence) fails not for want of rigour
but because its externally controlled transition is **binary**, and structural rank collapse has
no counterpart in it. What remains is (a) estimator recovery on synthetic generators —
*calibration*, not validation of the taxonomy — and (b) agreement with a binary domain
transition covering at most two of three regimes under a mapping the paper declines to make.
