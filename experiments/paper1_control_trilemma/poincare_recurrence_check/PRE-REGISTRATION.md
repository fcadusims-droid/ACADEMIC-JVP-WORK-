# Experiment G — Poincaré Recurrence Fraction of the Lorenz Attractor (Paper 1)

**Run order: 5th (first of Phase 2).** Trivial and cheap — a warm-up that also
discharges a specific numeric claim the text makes but never shows computed.

## Question
Paper 1 states a "recurrence fraction ≈ 1" for the Lorenz attractor in support of
the Case-3 (bounded recurrence) horn of the Meta-Optimization trichotomy. Is that
number actually what a direct computation gives?

## Method
Integrate the Lorenz system on its attractor; compute the Poincaré recurrence
fraction (the fraction of points whose forward trajectory returns to within
`epsilon` of the start within the observation window) as a function of `epsilon`
and integration length. Report the value and its dependence on `epsilon`.

## Pre-registered success criterion
The recurrence fraction is **≈ 1** (≥ 0.95) over a defensible band of `epsilon`
and long integration — confirming the text's claim as literally computed, with the
`epsilon`/time dependence stated explicitly.

## Pre-registered failure criterion
If the recurrence fraction is materially below the claimed ≈ 1 for any reasonable
`epsilon`, or depends so strongly on `epsilon` that "≈ 1" is only true in a
degenerate limit, the text's unqualified claim must be corrected to state the
`epsilon`/time regime in which it holds.

## Stopping rule
One clean computation with an `epsilon` sweep. This is a verification, not a
search.

## Status
Pre-registered. Not yet implemented.
