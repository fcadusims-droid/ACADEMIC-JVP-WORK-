# Formal development (Lean 4)

Four files, machine-checked in CI — and, as of the environment change noted below,
locally as well:

- **`Trichotomy.lean`** — Paper 1 §6.5's Meta-Optimization Collapse Theorem (formal statement in the paper's Appendix A.3): the
  exhaustiveness of the three cells and the *almost-everywhere* exclusion of the forbidden
  object (corrected; see below).
- **`Counterexamples.lean`** — machine-checked refutations, in concrete models and with no
  axioms, of the two *pointwise* axioms the first version of `Trichotomy.lean` and
  `Escape.lean` declared.
- **`ClassG.lean`** — Paper 1 §8.3's Class G (symbolic conditions and satisfiability tests in Appendix A.5): logical satisfiability of the
  ten-condition conjunction, exclusion of every near-miss, and the derivation of the
  filter's effective dimensionality.
- **`Escape.lean`** — Paper 1 §6.5's *escape horn*, closed by the stronger argument the
  escape experiments produced: an identity contract reads a coordinate that lives on a
  compact quotient, so a state that escapes in the radius stays recurrent in the
  observable — for readings typical of the quotient flow's invariant measure (almost every initial reading when that measure is Lebesgue, as for the quasi-periodic escapers tested). The axiom audit shows this consumes
  exactly `poincare_recurrence_ae`, the same analytic axiom the bounded cell uses.

## How the "it compiles" claim is verified

By CI, and now also locally. `.github/workflows/tests.yml` has a `lean` job that installs
Lean 4 via `elan`, compiles every file in this directory, and separately greps for
`sorry` — a file that compiles *while containing* `sorry` proves nothing, and a green
build would otherwise hide it.

**Environment change (previously this said local checking was impossible).** Earlier the
authoring environment could not install a Lean toolchain, so CI was the only place the
compile claim existed. That is no longer true: `elan-init.sh` is reachable
(`raw.githubusercontent.com`) and the toolchain downloads from `releases.lean-lang.org`
(not `github.com`), so Lean 4.9.0 installs and **all the files were compiled locally**,
with the `#print axioms` output below read directly rather than from a CI log. CI remains
the authority of record — a claim that the development compiles should still be read as
"the last CI run said so" — but it is no longer the *only* place the claim can be checked.

## `Trichotomy.lean` — what is and is not proved

### Correction first: the original axioms were false

The first version of this file declared `poincare_recurrence` ("every bounded point of a
measure-preserving flow is recurrent") and `conley_decomposition` ("every bounded point is
recurrent unless the flow is gradient-like"). An external review pointed out that both are
**strictly stronger than the theorems they are named after, and false** under the intended
reading:

- Poincaré's theorem gives recurrence of *almost every* point. A point on the pendulum's
  separatrix is bounded, the flow preserves Liouville measure, and it is not recurrent.
- Conley's theorem concerns ω-limit sets and the chain-recurrent *set*. A point spiralling
  onto an attracting limit cycle is bounded, the flow is not gradient-like (it has a periodic
  orbit), and the point is not recurrent. Chain recurrence is also far weaker than recurrence.

`Counterexamples.lean` now refutes both statements in the smallest discrete models where they
fail (`pointwise_poincare_false`, `pointwise_conley_false`), with **no axioms at all**. With
opaque predicates Lean could never have caught this: it verifies modus ponens over whatever is
declared. So the earlier headline "compiles over two undischarged axioms" was not an honest
dependency statement — the dependency was on two false statements — and the earlier plan to
"discharge them from Mathlib" could never have worked, because Mathlib proves the correct forms.
The error was ours and is recorded in `METHODOLOGY.md`.

The entropy hypothesis of the old `no_positive_entropy_without_recurrence` also did no work:
the proof discarded it (`rintro ⟨_, hnr⟩`). It has been removed rather than kept as decoration.

### What the corrected file declares and proves

**Declared as axioms — now true statements of the named theorems:**

- `poincare_recurrence_ae` — under a finite invariant measure, the non-recurrent points form a
  null set (Mathlib: `MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem`).
- `conley_omega` — a bounded orbit's ω-limit set is nonempty and lies in the chain-recurrent
  set (Conley 1978).

**Proved** (elementary, from those axioms):

- `trichotomy_exhaustive` — every orbit is convergent (ω-limit at rest), unbounded, or bounded
  with an ω-limit set that is chain-recurrent and not at rest. Exhaustiveness is excluded
  middle; Conley contributes only the chain-recurrence of the third cell.
- `forbidden_object_null` — bounded non-recurrence under measure preservation is confined to a
  **null set**. That is the whole content of the "forbidden object" result.

**What this costs Paper 1.** The exclusion holds for states typical of the invariant measure, not for every state. For conservative flows that is almost every initial condition; for **dissipative** flows the invariant measure lives on the attractor, the basin's transients are null for it though Lebesgue-generic, and Poincaré says nothing about them;
exceptional trajectories (separatrices, transients) exist. Case 3 means *asymptotically
chain-recurrent*, which is what the prose of §6.5 (classifying by attractor type) already
described, but which is weaker than the "recurrent" the first formal file asserted. The
load-bearing fact is recurrence on a compact set with an invariant measure; positive entropy
contributes nothing to the exclusion. §6.5 now says so.

### On discharging the axioms from Mathlib

The corrected axioms *are* dischargeable in principle; the old ones never were. In this
environment it is still impractical: Mathlib's source is clonable, but its prebuilt `olean`
cache host (`mathlib4.blob.core.windows.net`) is refused by the proxy and a cold source build
is hours of compute. Until then the analytic content is assumed and the logical step is
verified — with the difference that what is assumed is now true.

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

**Not proved:** Poincaré recurrence itself — the analytic input, now in its true
almost-everywhere form `poincare_recurrence_ae`, the same axiom `Trichotomy.lean` declares.
(The first version stated it pointwise; see the correction above.)

**Proved:**

- `observable_tracks_reading` — an identity contract's value trajectory is *exactly* `g` of the
  reading's trajectory: a pure equality of sequences, no continuity. Consumes **no** axioms.
- `escape_does_not_defeat_recurrence` — a full state may leave every compact set while an
  identity contract whose reading recurs keeps recurring in its observable; escape in the
  radius is invisible to it. After the correction the recurrence of the reading is a
  *hypothesis* (the reading lies outside the Poincaré-exceptional null set), and the theorem
  consumes no analytic axiom.
- `reading_recurrent_ae`, `cardinal_bounded_reading_recurrent_ae`,
  `closure_hypothesis_is_bounded_reading` — the non-recurrent readings form a null set whenever
  the reading's space carries a finite invariant measure, which a bounded (compact) reading
  supplies and the unbounded `e^{25}` reading does not.

So the escape horn closes by the same **almost-everywhere** recurrence argument as the bounded
cell. A single trajectory whose reading lies in the exceptional null set is not covered; that
is a real, if narrow, weakening of what the first version claimed.

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
lean formal/Counterexamples.lean
```
