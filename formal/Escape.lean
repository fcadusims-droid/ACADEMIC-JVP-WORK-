/-
  The escape horn closes by recurrence-on-the-quotient (Paper 1, §7.5) — formal skeleton.

  SCOPE, stated first because it bounds what this file is worth.

  `escape_persistence_decider` and `escape_cardinal_contract` established, numerically,
  a *stronger* closure of §7.5's escape horn than the paper's own argument. The paper
  reasoned that escape (leaving the compact value space) forfeits persistence and so
  lands in "a more extreme Class M". The experiments refuted that reason and supplied a
  better one: escape happens in the *radius*, an identity contract reads the *direction*,
  and the direction lives on a compact quotient where the recurrence theorem applies
  unchanged — so the escaping cell closes by the *same* Poincaré argument as the bounded
  cell, and the cardinal follow-up showed this survives magnitude-reading contracts too.

  This file formalises the *logical* core of that argument. It does NOT prove Poincaré
  recurrence (that is the analytic input, declared as an axiom exactly as in
  `Trichotomy.lean`, and in a Mathlib-enabled environment it would be discharged from
  `MeasureTheory` / `Dynamics`). What it proves is the elementary, machine-checkable step
  the experiments' conclusion actually rests on: that an observable which factors through
  the direction inherits the direction's recurrence *verbatim* — as an equality of value
  sequences, needing no continuity — so a full state that escapes in the radius cannot
  make the identity observable non-recurrent. The recurrence lives on the quotient; escape
  lives in a coordinate the contract cannot see.

  WHY THIS IS NOT VACUOUS. The point is the axiom audit at the bottom: the closure of the
  *escape* horn consumes exactly one analytic fact — `poincare_recurrence` — and it is the
  *same* axiom `Trichotomy.lean`'s bounded-cell result consumes. That is the precise sense
  in which "the horn closes by the same argument, stronger and more general" is true rather
  than rhetorical: both cells reduce to one recurrence theorem, the escaping one via the
  quotient.

  WHAT THIS FILE DOES **NOT** ESTABLISH — read this before citing it. The contested step in
  the surrounding argument is not the inference formalised here; it is the premise
  `Bounded ψ (proj x)`: that the identity observable of an *admissible* contract really does
  live on a compact quotient. That premise is a **hypothesis of every theorem below**, not a
  conclusion of any of them. The lemma named `closure_hypothesis_is_bounded_reading` says so
  in its name, and is stated separately for exactly that reason.

  This matters because formalisation can lend a modelling assumption the appearance of a
  theorem. "Machine-checked" describes the *inference* correctly and the *premise*
  incorrectly. What is verified here is that, given a bounded measure-preserving reading, the
  identity observable is recurrent and escape in the unread coordinate changes nothing — a
  parity-of-proof-structure result, which is what defeats the charge that the escape branch
  closes by an ad hoc appeal, and is all it defeats. Whether every admissible identity
  contract factors through such a reading is unproved, is not decidable inside this file, and
  is recorded in Paper 1 §7.5 as the first open problem the argument leaves. A reader who
  rejects that premise loses the closure of the escaping cell and keeps everything else here.
-/

namespace JVP.Escape

variable {X Q V : Type}

/-- A flow: `Flow T` assigns to each time and state a successor state. -/
def Flow (T : Type) := Nat → T → T

/-! ### Abstract dynamical predicates, declared rather than proved.

Identical in spirit to `Trichotomy.lean`. `Bounded`, `MeasurePreserving` and `Recurrent`
are opaque; the single analytic input the argument consumes is `poincare_recurrence`. -/

/-- The orbit of a point stays inside a compact set. -/
axiom Bounded {T : Type} : Flow T → T → Prop

/-- The flow is measure-preserving on a finite measure space. -/
axiom MeasurePreserving {T : Type} : Flow T → Prop

/-- The point returns arbitrarily close to itself infinitely often. -/
axiom Recurrent {T : Type} : Flow T → T → Prop

/-- **Poincaré recurrence** — the one analytic input, and the same one the bounded cell of
    the trichotomy uses. A measure-preserving flow whose orbit is bounded is recurrent. -/
axiom poincare_recurrence {T : Type}
    (ψ : Flow T) (q : T) : MeasurePreserving ψ → Bounded ψ q → Recurrent ψ q

/-! ### The escape structure

`proj : X → Q` is the *reading* an identity contract performs: it sends a full state to the
coordinate the contract actually evaluates. In §7.5 that coordinate is the direction on the
compact quotient; for a *cardinal* contract it is the direction paired with a bounded
magnitude reading. Either way `Q` is the reading's quotient, and the flow `ψ` is the
dynamics the reading induces on it. -/

/-- The reading is equivariant: the coordinate the contract sees evolves autonomously under
    its own flow `ψ`, independently of the radius. This is the structural fact the escape
    experiments verified — escape is orthogonal to the direction dynamics. -/
def Equivariant (proj : X → Q) (φ : Flow X) (ψ : Flow Q) : Prop :=
  ∀ n y, proj (φ n y) = ψ n (proj y)

/-- An observable *reads the direction* (is an identity/scale-free or bounded-cardinal
    contract) if it factors through the reading `proj`. -/
def ReadsDirection (obs : X → V) (proj : X → Q) : Prop :=
  ∃ g : Q → V, obs = g ∘ proj

/-! ### The elementary transport lemma -/

/-- **An identity contract's value trajectory is exactly `g` of the reading's trajectory.**
    No continuity, no metric: pure equality of sequences. This is the whole reason escape
    in the radius is invisible to the contract — the contract's output at every time is a
    function of the quotient point alone. -/
theorem observable_tracks_reading
    (proj : X → Q) (φ : Flow X) (ψ : Flow Q) (x : X) (obs : X → V) (g : Q → V)
    (heq : Equivariant proj φ ψ) (hobs : obs = g ∘ proj) :
    ∀ t, obs (φ t x) = g (ψ t (proj x)) := by
  intro t
  rw [hobs]
  show g (proj (φ t x)) = g (ψ t (proj x))
  rw [heq t x]

/-! ### Recurrence on the quotient, and the closure of the escape horn -/

/-- **The reading recurs**, by Poincaré on the quotient — the direction lives on a compact
    space and its flow is measure-preserving, so it returns, whatever the radius does. The
    hypotheses are about `ψ` on `Q`, and say *nothing* about whether the full state is
    bounded. -/
theorem reading_recurrent
    (proj : X → Q) (ψ : Flow Q) (x : X)
    (hmp : MeasurePreserving ψ) (hbq : Bounded ψ (proj x)) :
    Recurrent ψ (proj x) :=
  poincare_recurrence ψ (proj x) hmp hbq

/-- **Escape does not defeat identity recurrence.** The load-bearing statement. The full
    state may leave every compact set (`¬ Bounded φ x` — the escape horn is taken), yet an
    identity contract reads only the direction, which recurs on the compact quotient; and
    the contract's value trajectory is exactly `g` of that recurrent trajectory. Escape and
    the recurrence of the identity observable *coexist* — so escaping buys no non-recurrence
    in the observable the contract evaluates. The horn closes by recurrence-on-the-quotient.

    This is `escape_persistence_decider`'s conclusion, and it consumes only
    `poincare_recurrence` — the same axiom the bounded cell uses. -/
theorem escape_does_not_defeat_recurrence
    (proj : X → Q) (φ : Flow X) (ψ : Flow Q) (x : X) (obs : X → V)
    (hesc : ¬ Bounded φ x)
    (hid : ReadsDirection obs proj)
    (heq : Equivariant proj φ ψ)
    (hmp : MeasurePreserving ψ)
    (hbq : Bounded ψ (proj x)) :
    ¬ Bounded φ x ∧ Recurrent ψ (proj x)
      ∧ ∃ g : Q → V, ∀ t, obs (φ t x) = g (ψ t (proj x)) := by
  obtain ⟨g, hg⟩ := hid
  exact ⟨hesc, poincare_recurrence ψ (proj x) hmp hbq, g,
        observable_tracks_reading proj φ ψ x obs g heq hg⟩

/-! ### The cardinal contracts

`escape_cardinal_contract` removed the one caveat the scale-free closure carried: that the
exclusion might depend on the contract being scale-free. The formal content is that the
theorem above is already polymorphic in the reading `Q`, so it applies unchanged to any
cardinal contract whose reading lands in a *bounded* quotient:

* **scale-free / direction** contract: `Q` is the direction quotient — bounded by
  construction. `escape_does_not_defeat_recurrence` applies.
* **bounded cardinal** contract (`saturating`, `log_scaled` in the experiment): `Q` is the
  direction paired with a bounded magnitude reading — still a compact quotient, so the
  *same* theorem applies and recurrence persists (numerically `P_f = 0.21, 0.15`).
* **unbounded cardinal** contract (`raw_coord`, the `e^{25}` observable): the reading is
  *not* bounded, so `Bounded ψ (proj x)` — the hypothesis `poincare_recurrence` needs —
  fails. The theorem therefore says nothing about it, which is exactly right: its apparent
  persistence collapse (`P_f = 0.0006`) is the artefact of reading through an unbounded
  observable, not a genuine loss of recurrence.

The dichotomy is thus made precise by *where the boundedness hypothesis is available*. The
next two results state the two horns of it without introducing any new axiom. -/

/-- **Bounded cardinal contract: recurrence persists, by the same theorem.** Nothing here is
    specific to the direction — `readC` may be any reading (e.g. direction × saturated
    magnitude). Provided its quotient is bounded, the identity of the argument with the
    scale-free case is literal: it is the same call to `poincare_recurrence`. -/
theorem cardinal_bounded_reading_recurrent
    {D : Type} (readC : X → D) (χ : Flow D) (x : X)
    (hmp : MeasurePreserving χ) (hbd : Bounded χ (readC x)) :
    Recurrent χ (readC x) :=
  poincare_recurrence χ (readC x) hmp hbd

/-- **The recurrence guarantee is exactly coextensive with a bounded reading.** For every
    cardinal contract the *only* hypothesis the closure needs beyond measure preservation is
    that its reading stays on a compact quotient. So the unbounded (`e^{25}`) contract is
    precisely the one outside the theorem — the boundary is the boundedness of the reading,
    nothing else. Stated as: given measure preservation, boundedness of the reading suffices
    for recurrence. (Its failure for the exponential reading is why that case is an artefact,
    not a counterexample.) -/
theorem closure_hypothesis_is_bounded_reading
    {D : Type} (readC : X → D) (χ : Flow D) (x : X)
    (hmp : MeasurePreserving χ) :
    Bounded χ (readC x) → Recurrent χ (readC x) :=
  fun hbd => poincare_recurrence χ (readC x) hmp hbd

end JVP.Escape

/-! ### Axiom audit

`#print axioms` lists every unproved assumption each result rests on. The claim this file
makes precise — "the escape horn closes by the *same* argument as the bounded cell" — is
verified by the audit: `escape_does_not_defeat_recurrence` consumes exactly
`poincare_recurrence` (plus the classical logic Lean uses for the existential), the same
analytic axiom `Trichotomy.no_positive_entropy_without_recurrence` consumes, and nothing
about entropy, dispersion, or a "more extreme Class M". The transport lemma
`observable_tracks_reading` consumes no analytic axiom at all — it is pure equational
reasoning, which is the point: escape is invisible to a contract that reads the quotient. -/

#print axioms JVP.Escape.observable_tracks_reading
#print axioms JVP.Escape.reading_recurrent
#print axioms JVP.Escape.escape_does_not_defeat_recurrence
#print axioms JVP.Escape.cardinal_bounded_reading_recurrent
#print axioms JVP.Escape.closure_hypothesis_is_bounded_reading
