# Formal skeleton (Lean 4) — Meta-Optimization Collapse Theorem

Machine-checked skeleton of Paper 1 §7.5's trichotomy. Compiles under Lean 4
(`lean Trichotomy.lean`, exit 0, no errors, **no `sorry`**).

## What is and is not proved

**Proved here** (elementary, machine-checked):
- `trichotomy_exhaustive` — every autonomous preference dynamics falls in one of the
  three cells: gradient-like (Case 1), unbounded dispersion (Case 2), bounded
  recurrence (Case 3).
- `no_positive_entropy_without_recurrence` — the trilemma's load-bearing negative:
  on a compact value space a measure-preserving dynamics cannot exhibit positive
  entropy *together with* absence of recurrence. This is the "forbidden object" the
  in-silico experiments (E, E2, E2-Res) searched for and failed to find.
- `nonreturn_requires_escape` — the contrapositive §7.5 actually uses: sustained
  non-return requires leaving the compact value space (the "escape horn").

**Declared as axioms, not proved** — the analytic inputs:
- `poincare_recurrence` — measure-preserving flow on a finite measure space has
  almost every orbit recurrent;
- `conley_decomposition` — every flow on a compact metric space is gradient-like or
  has a nonempty chain-recurrent set (Conley 1978).

Both are standard and would be discharged from Mathlib's measure theory and
dynamics libraries. **Mathlib is unreachable in this environment** (the agent proxy
returns HTTP 403 for `github.com`), so they stand as axioms rather than imports.
That is the honest state: the *analytic* content is assumed, the *logical* step from
it to the trichotomy is verified.

## Why this is still worth having

`#print axioms` (run at the end of the file) prints the exact dependency set of each
theorem. The output shows the exhaustiveness result consumes only the Conley
decomposition plus classical logic, and the forbidden-object result consumes only
Poincaré recurrence — nothing else is smuggled in. Isolating precisely which
analytic facts the philosophical argument rests on is the deliverable; a reader who
wants to reject the trichotomy must now reject one of two named theorems or an
elementary inference, rather than the informal prose.

## Reproducing

```bash
curl -sSf -o elan-init.sh https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh
sh elan-init.sh -y --default-toolchain leanprover/lean4:v4.9.0
export PATH="$HOME/.elan/bin:$PATH"
lean formal/Trichotomy.lean
```
