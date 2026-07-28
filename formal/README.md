# Formal development (Lean 4)

Two files, machine-checked in CI:

- **`Trichotomy.lean`** — Paper 1 §7.5's Meta-Optimization Collapse Theorem: the
  exhaustiveness of the three cells and the impossibility of the forbidden object.
- **`ClassG.lean`** — Paper 1 §8.3's Class G: logical satisfiability of the
  ten-condition conjunction, exclusion of every near-miss, and the derivation of the
  filter's effective dimensionality.

## How the "it compiles" claim is verified

By CI, not by assertion. `.github/workflows/tests.yml` has a `lean` job that installs
Lean 4 via `elan`, compiles every file in this directory, and separately greps for
`sorry` — a file that compiles *while containing* `sorry` proves nothing, and a green
build would otherwise hide it.

This matters because **the authoring environment has no Lean toolchain and cannot
install one**: the agent proxy denies `github.com` by egress policy (HTTP 403, and the
proxy documentation says to report such denials rather than route around them). So
nothing here can be checked locally, and CI is the only place the claim exists at all.
Any statement in this repository that the formal development compiles should be read
as "the last CI run said so".

## `Trichotomy.lean` — what is and is not proved

**Proved** (elementary, machine-checked):

- `trichotomy_exhaustive` — every autonomous preference dynamics falls in one of the
  three cells: gradient-like, unbounded dispersion, bounded recurrence.
- `no_positive_entropy_without_recurrence` — on a compact value space a
  measure-preserving dynamics cannot exhibit positive entropy *together with* absence
  of recurrence. This is the "forbidden object" the in-silico experiments searched
  for and failed to find.
- `nonreturn_requires_escape` — sustained non-return requires leaving the compact
  value space.

**Declared as axioms**, not proved — the analytic inputs: `poincare_recurrence` and
`conley_decomposition` (Conley 1978).

### On discharging those axioms from Mathlib

This was attempted and is **blocked**, not merely undone. Mathlib is fetched from
`github.com`, which the session's egress policy denies with HTTP 403. The proxy's own
documentation classifies that as an organization policy denial and instructs that it
be reported rather than retried or worked around, so no route-around was attempted.

The blocked host is `github.com`. In an environment permitting it, the two axioms
would be replaced by Mathlib's measure-theoretic and dynamical results, and the
`#print axioms` output would shrink accordingly. Until then the honest position is
unchanged: the *analytic* content is assumed, the *logical* step from it to the
trichotomy is verified.

The value of the exercise does not depend on discharging them. `#print axioms` prints
the exact dependency set of each theorem, showing that exhaustiveness consumes only
the Conley decomposition plus classical logic and the forbidden-object result consumes
only Poincaré recurrence. A reader who wants to reject the trichotomy must reject one
of two named theorems or an elementary inference.

## `ClassG.lean` — what is and is not proved

**Not proved, and no propositional argument could prove it:** that a dynamical system
in Class G exists. That is what the numerical witness in `class_g_coherence` is for.

**Proved:** that the ten conditions are jointly satisfiable *together with the
entailments Paper 1 asserts between them*, that each of the five near-misses is
excluded while remaining a consistent assignment, and that the effective
dimensionality is six.

Ten unconstrained booleans would be satisfiable for a boring reason. The content is in
the entailments — §8.3 claims some conditions imply others, and if those claims were
inconsistent with the conjunction, Class G would be empty for a reason no amount of
numerical search would explain.

The result worth having is a convergence: the entailment structure written down from
the *prose* reproduces exactly the set `class_g_independence` found breakable in
isolation — {1, 2, 3, 4, 6, 9} — which was obtained by perturbing a simulation and was
never fitted to this model.

### A disambiguation the formalisation forced

Paper 1 says condition 8 "entails" condition 7: an incommensurable drive is aperiodic
by definition, i.e. `c8 → c7`. But the co-failure matrix reports that *breaking* 8
also breaks 7, which is `¬c8 → ¬c7`, i.e. `c7 → c8` — the **converse**.

Both hold for the §8.3 witness, and the prose runs them together, but they are
different claims with different status: the first is true of any witness; the second
only of a construction whose aperiodicity comes solely from incommensurability. They
are separated in `ClassG.lean` as `logicalEntailments` and `constructionEntailments`,
and the separation is what makes the effective-dimensionality count come out right —
assuming only the logical ones gives a different answer.

## Reproducing locally

```bash
curl -sSf -o elan-init.sh https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh
sh elan-init.sh -y --default-toolchain leanprover/lean4:v4.9.0
export PATH="$HOME/.elan/bin:$PATH"
lean formal/Trichotomy.lean
lean formal/ClassG.lean
```
