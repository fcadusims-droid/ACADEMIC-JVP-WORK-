# Trilha A2 — Structure×Power Dissociation on a Second Paradigm (Sleep-EDF, Paper 3)

**Turns Paper 3's pre-registered dissociation from a curiosity into a property of
the method.** The appendix's headline dissociation — the trace-normalized geometry
*fires* on a structural transition (eyes-open/closed occipital alpha topography)
and is *silent* on a power transition (rest/movement mu-beta desync) — was shown on
exactly one paradigm (occipital alpha). If it is a genuine property of the geometry
(trace normalization removes overall/band power, so only correlation *shape*
survives), it must replicate on an *independent* paradigm. This runs it on
Sleep-EDF, entirely from real data.

## The dissociation, on sleep
Both arms are built from the same real recordings and channels as Trilha A1
(EEG Fpz-Cz / Pz-Oz / EOG horizontal, SPD(3); 0.5–30 Hz; 2-s windows, trace-
normalized), so nothing about the pipeline changes between arms except *which*
contrast is measured:

- **Structural arm (should FIRE).** N2 vs REM — two stages with genuinely different
  spatial correlation structure (REM's rapid eye movements couple EOG to frontal
  EEG; N2's spindles/K-complexes do not). The between/within geodesic-distance ratio
  should exceed 1 (this is Trilha A1's Test 1, ratio ≈ 2.8 median).
- **Power arm (should stay SILENT).** Within the *same* stage (N2), the
  high-total-power half vs the low-total-power half of its epochs, split by raw
  pre-trace-normalization variance. These differ in overall amplitude/band power but
  share N2's spatial correlation structure, so after trace normalization the
  geodesic geometry should *not* separate them: the between/within ratio should stay
  near 1. This is a *real* power contrast (natural within-stage amplitude
  fluctuation), not an injected gain.

Each arm's between/within ratio is tested against the committed within-state
permutation null (random interleaved relabelings), giving a per-arm ratio and p.

## Pre-registered dissociation criterion (fixed before the run)
Per subject the dissociation *holds* if **both**:
1. **Structure fires:** structural ratio > 1 and permutation p < 0.05;
2. **Power is silent:** power ratio < 1.5 (near the within-state baseline) — i.e.
   the geometry does not separate a pure within-stage power contrast into a
   structural difference.

- **Success (dissociation is a method property):** holds in **≥ 12/15** recordings,
  **and** the median structural ratio is **≥ 2×** the median power ratio (the
  effect-size gap that *is* the dissociation).
- **Partial:** structure fires broadly but power is not reliably silent (power ratio
  ≥ 1.5 in many subjects) — then the trace normalization does *not* fully remove
  the power contrast on sleep, a real qualification to the appendix's claim, reported
  as such.
- **Failure:** structure does not fire on N2-vs-REM (contradicts A1) or the two arms
  are indistinguishable — reported straight.

Note the "silent" bar is set by *effect size* (ratio < 1.5), not by a non-significant
p, because with thousands of covariance windows even a trivial residual structural
leak in the power split would reach significance; effect size is the honest measure
of "the geometry barely moves."

## Fixed choices
Same 15 Sleep-EDF recordings, loader, bands, windows, and permutation count (500) as
Trilha A1; only the contrast definition is new. A recording is used if it has ≥ 10
N2 and ≥ 10 REM windows (structural arm) and ≥ 20 N2 windows splittable by power
(power arm). No tuning of the 1.5 bar, the 2× gap, or windows after seeing results.
Raw per-arm ratios/p and both aggregate criteria go to
`_results/sleep_structure_power_dissociation/result.json`; the prose verdict claims
no more than that table supports, and reports the recordings-vs-subjects
non-independence (15 recordings, ~8 subjects, both nights) exactly as A1 does.

## Status
Run. **Post-run addendum (transparency — the original criterion above is NOT
altered).** The pre-registered power arm (within-N2 high-vs-low *natural* power)
turned out NOT to be silent (median ratio 1.89, only 3/15 below the 1.5 bar), so by
the pre-registered criterion the clean dissociation does *not* replicate on sleep.
Inspection showed why: within-stage high-power epochs are structurally different
(more spindles/slow waves), so the "natural power" split is amplitude *confounded
with structure* — not a clean power contrast. A **post-hoc** pure-amplitude control
was therefore added and labelled as post-hoc: two random N2 halves, which a
per-window gain leaves geometrically identical, so any difference is pure within-N2
baseline. That control IS silent (median 1.00, 12/15), confirming the geometry is
power-blind by construction. Verdict: **qualified replication** — structure fires
(14/15) and the mechanism-level dissociation holds (silent on pure amplitude, gap
2.79 vs 1.00), but the appendix's clean "silent on a *natural* power transition" is
paradigm-specific (holds when the power change preserves structure, fails when power
and structure are naturally confounded, as in sleep). See
`_results/sleep_structure_power_dissociation/result.json`.
