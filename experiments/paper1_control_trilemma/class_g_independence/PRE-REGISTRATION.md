# Class G Condition Independence — Effective Dimensionality of the Filter (Paper 1 §8.3)

**Process note, stated first.** This document was written **after** the run, not
before, which is a departure from the protocol in `METHODOLOGY.md` and is recorded
rather than hidden. The lapse is mitigated but not excused by the nature of the
experiment: it is a **measurement with no success/failure threshold**. It reports a
co-failure matrix and a count derived from it; there is no bar that could have been
moved after seeing results, and no outcome that would have counted as "success" to
steer toward. Had it carried a pass/fail criterion, the missing pre-registration
would have invalidated it.

## Motivation

`class_g_coherence` established that the ten-condition conjunction is satisfiable and
discriminating. An audit of its raw output then surfaced something that experiment did
not test: **three of the five near-misses fail more conditions than the filter table
predicts** —

| control | predicted failures | actual failures |
|---|---|---|
| classical damping | 2, 5 | 2, 5, **6, 7** |
| ungated forcing | 9 | **3**, 9 |
| endogenous feedback | 10 | **1**, 10 |

Only coercion and the commensurable drive matched exactly. If a single perturbation can
knock out four conditions, then "a conjunction of ten conditions" carries more
rhetorical weight than logical content, and the discrepancy should be quantified.

## Question

Are §8.3's ten conditions independent, or does the filter have lower **effective
dimensionality**?

## Method

For each condition $i$, apply the most **surgical** perturbation available — one
designed to violate $i$ while disturbing as little else as possible — and then measure
the entire ten-condition battery. Entry $(i,j)$ of the resulting co-failure matrix
records whether perturbing for $i$ also breaks $j$.

Two perturbations required new (default-inert) parameters on the witness, added so that
the targeting could be surgical rather than blunt:
- condition 1 is broken by moving the landscape-modifying bump from the barrier top
  onto the $M$ well, so the external field still *exists* (leaving 9 and 10 untouched)
  but no longer *lowers the barrier*;
- condition 6 is broken by phase diffusion, which decorrelates the identity observable
  **without** collapsing the phases, so the tangential spectrum (5) and aperiodicity (7)
  should survive.

Both defaults are zero, and the coherence experiment was re-run to confirm its result
is unchanged (witness still 10/10, all five near-misses still excluded).

## Reported quantities

- **Breakable in isolation** — conditions for which a perturbation exists breaking that
  one and no other. This count is the filter's effective dimensionality.
- **Entailments** $i \Rightarrow j$ — where every perturbation breaking $i$ also breaks $j$.
- **Co-failure clusters** — conditions with identical failure signatures.

A dependency is further classified as **logical** (true of any witness) or
**construction-specific** (possibly separable in another system); that classification is
argued, not measured, and is labelled as such.

## Status
Run. Verdict: **effective dimensionality ≈ 6, not 10.** Six conditions (1, 2, 3, 4, 6, 9)
break in isolation; four (5, 7, 8, 10) never do. Measured entailments: $5\Rightarrow6$,
$5\Rightarrow7$, $8\Rightarrow7$, $10\Rightarrow1$. Two are **logical** — an incommensurable
drive is aperiodic by definition (so $8\Rightarrow7$ admits no separating construction),
and a collapsed phase is a constant, hence without correlation power and trivially
periodic (so $5\Rightarrow6,7$). The satisfiability and discrimination results are
untouched; what changes is the weight the count of ten can bear, now declared in
§8.3. See `_results/class_g_independence/result.json`.
