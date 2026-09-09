# H5 — does a 2025 lexicographic-heads corrigibility agent escape the trilemma? (Paper 1)

**Written before the run.** Paper 1 §2.1(iii) names its own failure condition: "the three horns
turned out not to be jointly exhaustive, leaving a fourth control strategy unexamined." A 2025
construction is a credible candidate for that fourth strategy: *Core Safety Values for Provably
Corrigible Agents* (arXiv:2507.20964) builds an agent from **five structurally separated utility
heads combined lexicographically** and proves exact corrigibility — agency-preserving deference to
an external principal. If such an agent realises *agency-preserving value reordering* autonomously,
it is the forbidden object the Meta-Optimization Collapse Theorem says cannot exist. Paper 1 §7.8
does not cite it (it postdates the draft). This is the test.

## What is tested
Model the lexicographic-heads agent as an **autonomous value dynamics** on a compact space and
classify it with the *same* instruments `rl_agents_trichotomy` uses (largest Lyapunov exponent as
entropy proxy; Poincaré recurrence fraction; Helmholtz–Hodge gradient/rotational split), plus the
agency-bearing diffusion `D_ag` (asymptotic exploration) that §7.3 uses to detect horn-2 collapse.
Two readings of "lexicographic heads":
- **satisfiable heads** — each head has a reachable optimum; the agent pursues head 1 until
  satisfied, then head 2, … (an autonomous value-base switch, like E2's value-mutating agent);
- **inexhaustible/incommensurable heads** — heads that can never be jointly satisfied (the §8.3
  incommensurable-drive reading).

## Pre-registered classification criterion (fixed now)
For each variant, classify by the committed rule `classify(λ, R)`:
- **Case 1** (λ < 0, gradient-dominated) ⇒ the agent installs a *fixed higher-order objective*
  (the lexicographic order), i.e. **horn 1** (endogenous reabsorption, §7.6). Trilemma exhaustivity
  **holds** against this candidate.
- **Case 3 / 3\*** (bounded recurrence, λ ≈ 0 or λ>0 with R high) ⇒ conservative circulation on the
  compact quotient, **not** the forbidden object; exhaustivity **holds**.
- **FALSIFIER** (λ > 0, recurrence R < 0.5, *and* `D_ag` bounded away from 0 = agency preserved,
  *and* a genuine value-base reordering occurs) ⇒ the fourth strategy exists; §2.1(iii) fired and
  §7.5/§7.6 must be rewritten.
- Additionally: if `D_ag → 0` at the attractor, the construction is *not* agency-preserving value
  change (horn-2 flavour), which also is not a fourth horn.

Run the Class G ten-condition filter (`class_g_coherence` machinery) on the agent as a secondary
check: passing would make it a Class G occupant (the admissible residual, not a refutation);
failing places it with the near-misses.

## Conceptual sub-question (recorded, not scored)
2507.20964 also proves a corrigibility-violation predicate is *undecidable by reduction to the
halting problem*. Paper 1 §2.1 denies formal kinship with Gödel/Rice ("analogy of form"). Decide
whether that halting result bears on Paper 1's object: it concerns **decidability of a predicate
over agent-programs**, whereas the theorem is a **dynamical statement about flows** — different
objects — so record whether §2.1's "no formal kinship" survives or needs the narrower wording
"kinship via halting for the decision problem, but the central result is dynamical".

## Attempt budget
**One run, no tuning loop.** Fields, classifier and criteria fixed here. The agent is given its
best chance to escape (the incommensurable variant is built precisely to avoid a fixed optimum);
whatever the classifier returns is reported.

## Status
Pre-registered. Not yet run.
