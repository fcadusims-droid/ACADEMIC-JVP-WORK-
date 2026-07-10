# Experiment E2 — High-Dimensional, Value-Base-Mutating Trichotomy Test (Paper 1)

**Extends Experiment E**, closing a gap an independent review of this repo
identified. E's candidates (gradient, hamiltonian, curiosity, novelty search,
Lorenz) all lived on a 2-D torus or 3-D Lorenz attractor — low-dimensional
systems where the trichotomy is close to analytically demonstrable. The paper's
own Sec 7.5 names the philosophically live objection as *open-ended,
novelty-driven, or value-base-mutating optimization* in a genuinely
higher-dimensional setting — closer to real population-based training (PBT) with
meta-optimized objectives. E never built this candidate. Also noted: E's
`novelty_search` entry has `lambda_max: null` (no entropy diagnostic was even
computed for the one low-dimensional candidate that came closest to this
objection).

## Question
Does a **higher-dimensional (d=6), population-based, value-base-mutating**
preference dynamics — where the reward landscape itself drifts *in response to*
the population's own trajectory (open-ended, endogenous, not pre-enumerated) —
produce the forbidden object: **positive entropy on the attractor AND absence of
recurrence**, on a compact value space? This is the single strongest adversarial
case the text itself names.

## Method
`M` agents, each with a preference vector `theta_i` in `R^d` (d=6) on a compact
torus `[0,1)^d`. A reward landscape is a sum of `K` Gaussian bumps whose CENTERS
RECEDE from wherever the population's recent density has concentrated (the
landscape is revised in response to the population's own exploitation — genuinely
open-ended and value-base-mutating, not a fixed or pre-enumerated objective).
Each agent's `theta_i` evolves by (a) gradient ascent on the current landscape at
its position, (b) mild repulsion from other agents (diversity pressure, as in
PBT explore/exploit), (c) small diffusion. Measure the **population-mean**
trajectory (the aggregate value-base state) for:
  * largest Lyapunov exponent (Benettin method, generalizes to any dimension);
  * Poincaré recurrence fraction (k-d tree, dimension-agnostic).

Hodge decomposition is 2-D-only in `shared_lib` and is not required: the
falsification criterion is purely `lambda_max > 0 AND recurrence < 0.5`, which
needs only the two diagnostics above.

## Pre-registered falsification target
A run with **positive Lyapunov exponent AND low recurrence fraction (< 0.5)**
simultaneously, on the compact torus. If found, the Meta-Optimization Collapse
Theorem (Sec 7.5/7.6) is **falsified** by its own named hardest case, and that
section must be rewritten.

## Pre-registered success criterion (for the theorem)
Across a sweep of the landscape's recession rate (how aggressively the reward
mutates away from exploited regions) and the population's diversity-pressure
strength, every run lands in the trichotomy (negative Lyapunov = convergent,
or positive/near-zero Lyapunov with high recurrence = bounded). No run is both
chaotic and non-recurrent.

## Stopping rule
One sweep (recession rate × diversity pressure), `M=8` agents, `d=6`, moderate
step count (bounded by runtime, target < 5 minutes). This is the single most
adversarial case named in the text; if it survives, the trichotomy's defence is
substantially strengthened. If it falls, that must be reported as prominently
as Experiment E's confirmation.

## Status
Complete. See `../../_results/README.md` and `_results/high_dim_trichotomy/result.json`.
Verdict: TRICHOTOMY SURVIVES ITS HARDEST NAMED CASE, AMONG NUMERICALLY RESOLVED
CELLS — an important methodological complication surfaced mid-run: the
strongest-recession cells (7/12) failed a dt-convergence sanity check (the
apparent Lyapunov exponent grew without bound as the integration step shrank,
rather than converging — one cell even flipped sign between dt and dt/2). These
were excluded as numerically unresolved rather than reported as either a
confirmation or a falsification (mirroring Paper 3's own appendix precedent for
a controlled failure). Among the 5/12 cells that passed convergence, no
falsifier appeared.

