/-
  Meta-Optimization Collapse Theorem (Paper 1, §7.5) — formal skeleton, CORRECTED.

  WHAT CHANGED, AND WHY. The first version of this file declared two axioms named after
  Poincaré and Conley that were strictly stronger than those theorems and false under the
  intended reading (an external review caught it; `formal/Counterexamples.lean` refutes both
  in concrete models with no axioms at all):

  * old `poincare_recurrence`: every bounded point of a measure-preserving flow is recurrent.
    Poincaré gives only *almost every* point (pendulum separatrix: bounded, measure preserved,
    not recurrent).
  * old `conley_decomposition`: every bounded point is recurrent unless the flow is
    gradient-like. Conley is about ω-limit sets and the chain-recurrent *set*, and chain
    recurrence is much weaker than recurrence (a point spiralling onto a limit cycle: bounded,
    flow not gradient-like, point not recurrent).

  So the earlier "compiles over two undischarged axioms" was not an honest dependency
  statement: it depended on two statements the named theorems do not support, and
  discharging them from Mathlib was never possible, because Mathlib proves the correct forms.

  This version declares the correct forms and proves only what follows from them. The
  consequences for Paper 1 are real and are stated in §7.5:

  1. The forbidden object (bounded non-recurrence under measure preservation) is excluded for
     **almost every** initial condition, not every. Exceptional trajectories exist; they form a
     null set of the invariant measure.
  2. The entropy hypothesis did no logical work in the old proof (it was discarded by
     `rintro ⟨_, hnr⟩`). It is removed rather than kept as decoration: the load-bearing fact is
     recurrence, not chaos.
  3. The three cells are exhaustive by excluded middle on the asymptotic behaviour of the
     orbit. Conley's theorem contributes one thing — that a bounded orbit's ω-limit set lies in
     the chain-recurrent set — and chain recurrence is weaker than recurrence, so "Case 3" is
     *asymptotically chain-recurrent*, not "recurrent". A transient spiralling onto a limit
     cycle is in Case 3 by this definition, as the prose of §7.5 (which classifies by attractor)
     already has it.

  With opaque predicates, Lean verifies only the propositional step from these axioms. That is
  all this file claims.
-/

namespace JVP

/-- A flow: `Flow X` assigns to each time and state a successor state. -/
def Flow (X : Type) := Nat → X → X

/-- The orbit of `x` stays inside the compact value space. -/
axiom Bounded {X : Type} : Flow X → X → Prop

/-- The flow preserves a finite measure. -/
axiom MeasurePreserving {X : Type} : Flow X → Prop

/-- `x` returns arbitrarily close to itself infinitely often (pointwise recurrence). -/
axiom Recurrent {X : Type} : Flow X → X → Prop

/-- A set of states has measure zero for the flow's invariant finite measure. -/
axiom NullSet {X : Type} : Flow X → (X → Prop) → Prop

/-- The ω-limit set of `x` consists of rest points (the orbit settles to equilibria):
    Case 1, convergence onto a fixed evaluative point. -/
axiom OmegaAtRest {X : Type} : Flow X → X → Prop

/-- The ω-limit set of `x` is nonempty and contained in the chain-recurrent set. -/
axiom OmegaChainRecurrent {X : Type} : Flow X → X → Prop

/-! ### The analytic inputs, in their correct forms. -/

/-- **Poincaré recurrence (almost everywhere).** For a flow preserving a finite measure, the
    set of points that are not recurrent is null. (Mathlib: `MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem`, via
    `MeasurePreserving.conservative` on a finite measure.) -/
axiom poincare_recurrence_ae {X : Type} (φ : Flow X) :
    MeasurePreserving φ → NullSet φ (fun x => ¬ Recurrent φ x)

/-- **Conley (ω-limit form).** On a compact metric space every ω-limit set is nonempty and
    lies in the chain-recurrent set (Conley 1978). -/
axiom conley_omega {X : Type} (φ : Flow X) (x : X) :
    Bounded φ x → OmegaChainRecurrent φ x

/-! ### The trichotomy, classified by asymptotic behaviour -/

/-- The three cells of §7.5. Case 3 is *asymptotically chain-recurrent and not at rest* —
    not "recurrent". -/
inductive Cell {X : Type} (φ : Flow X) (x : X) : Prop where
  | convergent : Bounded φ x → OmegaAtRest φ x → Cell φ x
  | dispersion : ¬ Bounded φ x → Cell φ x
  | recurrent  : Bounded φ x → OmegaChainRecurrent φ x → ¬ OmegaAtRest φ x → Cell φ x

/-- **Exhaustiveness.** By excluded middle on boundedness and on whether the orbit settles;
    Conley supplies only the chain-recurrence of Case 3's limit set. -/
theorem trichotomy_exhaustive {X : Type} (φ : Flow X) (x : X) : Cell φ x := by
  by_cases hb : Bounded φ x
  · by_cases hr : OmegaAtRest φ x
    · exact Cell.convergent hb hr
    · exact Cell.recurrent hb (conley_omega φ x hb) hr
  · exact Cell.dispersion hb

/-- **The forbidden object is null.** Under measure preservation, the states whose orbit never
    returns — with or without positive entropy, which does no work here — form a null set. The
    trilemma's load-bearing exclusion holds for almost every initial condition, and no more. -/
theorem forbidden_object_null {X : Type} (φ : Flow X) (hmp : MeasurePreserving φ) :
    NullSet φ (fun x => ¬ Recurrent φ x) :=
  poincare_recurrence_ae φ hmp

end JVP

/-! ### Axiom audit

`trichotomy_exhaustive` consumes `conley_omega` (and classical logic); `forbidden_object_null`
consumes `poincare_recurrence_ae`. Both analytic axioms are now true statements of the
named theorems. -/

#print axioms JVP.trichotomy_exhaustive
#print axioms JVP.forbidden_object_null
