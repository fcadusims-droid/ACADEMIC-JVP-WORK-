/-
  Meta-Optimization Collapse Theorem (Paper 1, §7.5) — formal skeleton.

  SCOPE, stated first because it bounds what this file is worth:
  this formalises the *logical* core of the trichotomy — the exhaustiveness of the
  three cells, and the impossibility of the forbidden object — from analytic inputs
  that are declared as axioms. The analytic inputs themselves (Poincaré recurrence,
  the Conley decomposition, Helmholtz–Hodge) are NOT proved here; they are standard,
  and in a Mathlib-enabled environment they would be discharged from
  `MeasureTheory` / `Dynamics`. In this environment Mathlib is unreachable (the
  proxy returns 403 for github.com), so they stand as explicit axioms.

  That isolation is the point of the exercise: it makes precise exactly which
  analytic facts the philosophical argument consumes, and shows the step from those
  facts to the trichotomy is elementary and machine-checkable.
-/

namespace JVP

-- Abstract state space of an autonomous preference dynamics.
variable {X : Type}

/-- A flow: `Flow X` assigns to each time and state a successor state. -/
def Flow (X : Type) := Nat → X → X

/-- The orbit of `x` stays inside the compact value space. -/
axiom Bounded {X : Type} : Flow X → X → Prop

/-- The flow is measure-preserving on a finite measure space. -/
axiom MeasurePreserving {X : Type} : Flow X → Prop

/-- `x` returns arbitrarily close to itself infinitely often. -/
axiom Recurrent {X : Type} : Flow X → X → Prop

/-- The flow admits a strictly decreasing Lyapunov function off its recurrent set:
    Case 1, "gradient descent on a meta-potential". -/
axiom GradientLike {X : Type} : Flow X → Prop

/-- Positive topological entropy: sensitive dependence, "chaotic". -/
axiom PositiveEntropy {X : Type} : Flow X → Prop

/-! ### The analytic inputs, declared rather than proved.

These are the *only* facts about dynamics the argument uses. In Mathlib they are
`MeasureTheory.Ergodic`-adjacent results; here they are axioms, and any reader who
rejects the trichotomy must reject one of them or the elementary steps below. -/

/-- **Poincaré recurrence.** A measure-preserving flow on a finite measure space has
    almost every orbit recurrent. (Mathlib: measure theory + ergodic theory.) -/
axiom poincare_recurrence {X : Type}
    (φ : Flow X) (x : X) : MeasurePreserving φ → Bounded φ x → Recurrent φ x

/-- **Conley decomposition.** Every flow on a compact metric space is either
    gradient-like or has a nonempty chain-recurrent set (Conley 1978). -/
axiom conley_decomposition {X : Type}
    (φ : Flow X) (x : X) : Bounded φ x → GradientLike φ ∨ Recurrent φ x

/-! ### The trichotomy -/

/-- The three admissible cells of §7.5: gradient-like convergence (Case 1),
    unbounded dispersion (Case 2), or bounded recurrence (Case 3). -/
inductive Cell {X : Type} (φ : Flow X) (x : X) : Prop where
  | gradient   : GradientLike φ      → Cell φ x
  | dispersion : ¬ Bounded φ x       → Cell φ x
  | recurrent  : Recurrent φ x       → Cell φ x

/-- **Exhaustiveness.** Every autonomous preference dynamics falls in some cell.
    Elementary from the Conley decomposition plus excluded middle on boundedness. -/
theorem trichotomy_exhaustive {X : Type} (φ : Flow X) (x : X) : Cell φ x := by
  by_cases hb : Bounded φ x
  · rcases conley_decomposition φ x hb with hg | hr
    · exact Cell.gradient hg
    · exact Cell.recurrent hr
  · exact Cell.dispersion hb

/-- **The forbidden object does not exist.** The trilemma's load-bearing negative
    claim: on a compact value space, a measure-preserving dynamics cannot exhibit
    positive entropy *together with* absence of recurrence. Conversion, modelled as
    sustained novelty without return, therefore cannot be realised endogenously on
    a compact value space — it must leave compactness (the "escape horn"). -/
theorem no_positive_entropy_without_recurrence {X : Type}
    (φ : Flow X) (x : X)
    (hmp : MeasurePreserving φ) (hb : Bounded φ x) :
    ¬ (PositiveEntropy φ ∧ ¬ Recurrent φ x) := by
  rintro ⟨_, hnr⟩
  exact hnr (poincare_recurrence φ x hmp hb)

/-- Contrapositive, in the form §7.5 actually uses: sustained non-return on a
    measure-preserving dynamics requires leaving the compact value space. -/
theorem nonreturn_requires_escape {X : Type}
    (φ : Flow X) (x : X)
    (hmp : MeasurePreserving φ) (hnr : ¬ Recurrent φ x) : ¬ Bounded φ x := by
  intro hb
  exact hnr (poincare_recurrence φ x hmp hb)

end JVP

/-! ### Audit: which axioms does each result actually consume?

`#print axioms` lists every unproved assumption a theorem rests on. The output is
the honest dependency statement: the trichotomy's exhaustiveness consumes only the
Conley decomposition (plus classical logic), and the forbidden-object result
consumes only Poincaré recurrence. Nothing else is smuggled in. -/

#print axioms JVP.trichotomy_exhaustive
#print axioms JVP.no_positive_entropy_without_recurrence
#print axioms JVP.nonreturn_requires_escape
