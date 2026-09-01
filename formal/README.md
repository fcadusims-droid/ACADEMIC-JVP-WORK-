# Formal development (Lean 4)

Three files, machine-checked in CI — and, as of the environment change noted below,
locally as well:

- **`Trichotomy.lean`** — Paper 1 §7.5's Meta-Optimization Collapse Theorem: the
  exhaustiveness of the three cells and the impossibility of the forbidden object.
- **`ClassG.lean`** — Paper 1 §8.3's Class G: logical satisfiability of the
  ten-condition conjunction, exclusion of every near-miss, and the derivation of the
  filter's effective dimensionality.
- **`Escape.lean`** — Paper 1 §7.5's *escape horn*, closed by the stronger argument the
  escape experiments produced: an identity contract reads a coordinate that lives on a
  compact quotient, so a state that escapes in the radius stays recurrent in the
  observable. The axiom audit shows this consumes exactly `poincare_recurrence` — the
  same analytic axiom the bounded cell uses.

## How the "it compiles" claim is verified

By CI, and now also locally. `.github/workflows/tests.yml` has a `lean` job that installs
Lean 4 via `elan`, compiles every file in this directory, and separately greps for
`sorry` — a file that compiles *while containing* `sorry` proves nothing, and a green
build would otherwise hide it.

**Environment change (previously this said local checking was impossible).** Earlier the
authoring environment could not install a Lean toolchain, so CI was the only place the
compile claim existed. That is no longer true: `elan-init.sh` is reachable
(`raw.githubusercontent.com`) and the toolchain downloads from `releases.lean-lang.org`
(not `github.com`), so Lean 4.9.0 installs and **all three files were compiled locally**,
with the `#print axioms` output below read directly rather than from a CI log. CI remains
the authority of record — a claim that the development compiles should still be read as
"the last CI run said so" — but it is no longer the *only* place the claim can be checked.

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

Still **out of reach in this environment**, but the reason is now narrower and precisely
identified — the earlier "`github.com` returns 403" was too coarse. Retested after the
environment was loosened:

- **Mathlib source is now clonable.** `git ls-remote https://github.com/leanprover-community/mathlib4`
  succeeds — git smart-HTTP to `github.com` is permitted (even though a plain browser
  request to `github.com` still returns 403).
- **The prebuilt `olean` cache is blocked.** `lake exe cache get` downloads Mathlib's
  compiled artifacts from `mathlib4.blob.core.windows.net`, which the proxy refuses
  (`CONNECT tunnel failed, 502`). Without that cache, Mathlib must be built from source.
- **Building Mathlib from source in-session is infeasible** — it is hours of compute and
  gigabytes of `olean`, far outside a working session's budget.

So the blocker moved from "Mathlib is unreachable" to "Mathlib's *cache* is unreachable
and a cold source build is impractical". In an environment that either permits the cache
host or pre-stages the `olean`s, the two axioms would be replaced by Mathlib's
measure-theoretic and dynamical results and the `#print axioms` output would shrink
accordingly. Until then the honest position is unchanged: the *analytic* content is
assumed, the *logical* step from it to the trichotomy (and to the escape closure) is
verified.

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

## `Escape.lean` — what is and is not proved

**Not proved:** Poincaré recurrence itself — it is the analytic input, the *same* axiom
`Trichotomy.lean` declares.

**Proved:** the elementary core the escape experiments' conclusion rests on.

- `observable_tracks_reading` — an identity contract's value trajectory is *exactly* `g`
  of the reading's trajectory: a pure equality of sequences, needing no continuity. This
  is why escape in the radius is invisible to the contract, and it consumes **no** axioms.
- `escape_does_not_defeat_recurrence` — the load-bearing statement. A full state may leave
  every compact set (`¬ Bounded φ x`, the escape horn taken) while the identity contract,
  reading a coordinate on a compact quotient, stays recurrent — the two coexist, so escape
  buys no non-recurrence in the observable. Consumes exactly `poincare_recurrence`.
- `cardinal_bounded_reading_recurrent` / `closure_hypothesis_is_bounded_reading` — the same
  theorem is polymorphic in the reading, so it covers a *cardinal* (magnitude-reading)
  contract unchanged, **provided its reading lands in a bounded quotient**. That proviso is
  the whole content of the cardinal follow-up: the bounded and linear-on-bounded readings
  keep recurrence; the unbounded `e^{25}` reading is exactly the case the boundedness
  hypothesis excludes, so its apparent collapse is an artefact of an unbounded observable,
  not a persistence failure.

This is the formal counterpart of `escape_persistence_decider` and
`escape_cardinal_contract`: it makes precise that the escape horn closes by the *same*
recurrence argument as the bounded cell — "stronger and more general" is verified by the
axiom audit (both reduce to `poincare_recurrence`), not merely asserted.

## Reproducing locally

The toolchain is reachable from the authoring environment, so this now runs locally as
well as in CI:

```bash
curl -sSf -o elan-init.sh https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh
sh elan-init.sh -y --default-toolchain leanprover/lean4:v4.9.0
export PATH="$HOME/.elan/bin:$PATH"
lean formal/Trichotomy.lean
lean formal/ClassG.lean
lean formal/Escape.lean
```
