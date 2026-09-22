/-
  Machine-checked counterexamples to the POINTWISE axioms the first version of
  `Trichotomy.lean` and `Escape.lean` declared (Paper 1, §7.5).

  WHY THIS FILE EXISTS. An external review observed that the original axioms were
  stronger than the theorems they were named after, and so false under the intended
  reading:

  * `poincare_recurrence` said every bounded point of a measure-preserving flow is
    recurrent. Poincaré's theorem only gives *almost every* point. (Continuous witness:
    the pendulum separatrix — bounded, Liouville measure preserved, not recurrent.)
  * `conley_decomposition` said every bounded point is recurrent unless the flow is
    gradient-like. Conley's theorem is about the chain-recurrent *set* and ω-limit sets,
    not about the point itself. (Continuous witness: a point spiralling onto an attracting
    limit cycle — bounded, flow not gradient-like, point not recurrent.)

  With opaque predicates Lean cannot refute an axiom from the inside: it only checks
  modus ponens over whatever is declared. So the refutation has to be done in a concrete
  model, with the predicates *defined* rather than postulated. That is what this file
  does, for the smallest discrete models in which each failure occurs. Both are exact
  analogues of the continuous witnesses above: the exceptional point is a transient that
  never comes back, and it carries zero invariant measure.

  No axioms are declared; `#print axioms` at the bottom confirms each result rests on
  nothing beyond Lean's core logic.
-/

namespace JVP.Counterexamples

/-- `n`-fold iterate of a map: the discrete-time flow it generates. -/
def iter {α : Type} (f : α → α) : Nat → α → α
  | 0, x => x
  | n + 1, x => f (iter f n x)

/-- Discrete-topology recurrence: the orbit returns exactly to `x` at arbitrarily late times. -/
def Recurrent {α : Type} (f : α → α) (x : α) : Prop :=
  ∀ N : Nat, ∃ n, N < n ∧ iter f n x = x

/-! ## 1. Pointwise Poincaré is false

State space `Bool`, map `f _ = true`. The invariant probability is the point mass at
`true` (mass 0 on `false`). `false` is bounded (the space is finite), the map preserves the
measure, and `false` never returns. The recurrent set `{true}` has full measure — which is
exactly what the almost-everywhere theorem asserts, and all it asserts. -/

def pMap : Bool → Bool := fun _ => true

/-- The invariant probability measure: point mass at `true`. -/
def pMeasure (S : Bool → Bool) : Nat := if S true then 1 else 0

/-- Measure preservation: every set has the same measure as its preimage. -/
def PMeasurePreserving : Prop := ∀ S : Bool → Bool, pMeasure (fun x => S (pMap x)) = pMeasure S

theorem p_measure_preserving : PMeasurePreserving := fun _ => rfl

theorem p_false_not_recurrent : ¬ Recurrent pMap false := by
  intro h
  obtain ⟨n, hn, heq⟩ := h 0
  cases n with
  | zero => exact absurd hn (Nat.lt_irrefl 0)
  | succ k => exact Bool.noConfusion (show iter pMap (k + 1) false = false from heq)

/-- The exceptional set `{false}` is null, and the complement is recurrent — the true,
    almost-everywhere statement holds in this model. -/
theorem p_exceptional_set_null : pMeasure (fun x => x == false) = 0 := rfl

theorem p_true_recurrent : Recurrent pMap true := fun N => ⟨N + 1, Nat.lt_succ_self N, rfl⟩

/-- **The pointwise axiom fails**: a measure-preserving map on a finite (so bounded) space
    with a non-recurrent point. -/
theorem pointwise_poincare_false :
    PMeasurePreserving ∧ ∃ x, ¬ Recurrent pMap x :=
  ⟨p_measure_preserving, false, p_false_not_recurrent⟩

/-! ## 2. Pointwise Conley is false

Three states, `a ↦ b ↦ c ↦ b`: a transient `a` feeding a 2-cycle `{b, c}` — the discrete
limit cycle. The map is not gradient-like (no function strictly decreases along every
non-fixed step, because of the cycle), `a` is bounded (finite space), and `a` is not
recurrent. So `GradientLike ∨ Recurrent a` fails. The ω-limit set of `a` is the cycle
`{b, c}`, which *is* recurrent — the statement Conley's theorem actually licenses. -/

inductive S3 | a | b | c
  deriving DecidableEq

def cMap : S3 → S3
  | .a => .b
  | .b => .c
  | .c => .b

/-- Gradient-like: some Lyapunov function strictly decreases along every non-fixed step. -/
def GradientLike (f : S3 → S3) : Prop := ∃ V : S3 → Nat, ∀ x, f x ≠ x → V (f x) < V x

theorem c_not_gradient_like : ¬ GradientLike cMap := by
  intro ⟨V, hV⟩
  have h1 := hV .b (by decide)
  have h2 := hV .c (by decide)
  exact Nat.lt_asymm h1 h2

theorem c_never_returns_to_a : ∀ x, cMap x ≠ .a := by
  intro x; cases x <;> decide

theorem c_a_not_recurrent : ¬ Recurrent cMap .a := by
  intro h
  obtain ⟨n, hn, heq⟩ := h 0
  cases n with
  | zero => exact absurd hn (Nat.lt_irrefl 0)
  | succ k => exact c_never_returns_to_a _ heq

/-- The cycle points are recurrent: what the ω-limit form of the theorem guarantees. -/
theorem c_b_recurrent : Recurrent cMap .b := by
  intro N
  refine ⟨2 * N + 2, by omega, ?_⟩
  suffices h : ∀ m, iter cMap (2 * m) .b = .b by exact h (N + 1)
  intro m
  induction m with
  | zero => rfl
  | succ k ih =>
    show cMap (cMap (iter cMap (2 * k) .b)) = .b
    rw [ih]; rfl

/-- **The pointwise axiom fails**: not gradient-like, and a bounded non-recurrent point. -/
theorem pointwise_conley_false : ¬ (GradientLike cMap ∨ Recurrent cMap .a) := by
  intro h
  cases h with
  | inl hg => exact c_not_gradient_like hg
  | inr hr => exact c_a_not_recurrent hr

end JVP.Counterexamples

#print axioms JVP.Counterexamples.pointwise_poincare_false
#print axioms JVP.Counterexamples.pointwise_conley_false
#print axioms JVP.Counterexamples.p_true_recurrent
#print axioms JVP.Counterexamples.c_b_recurrent
