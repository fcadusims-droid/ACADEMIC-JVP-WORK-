# Paper 1 development plan (2026-09-26): assessment and decisions

A colleague's plan for Paper 1, assessed point by point against the text, the repository and
the literature. The author asked for it to be read, judged and carried out in order. For each
point this file records whether it was accepted and why, and what was done. Decisions that
belong to the author are marked as such.

**Facts checked before deciding.**
- Paper 1 is 31,418 words without its references (body 26,212; Appendix A 5,206).
- §7 alone is 12,586 words, of which §7.8 (related work) is 3,500.
- The "Abstract" section is 2,227 words, because it holds much of the front matter.

## Phase 1: scope decisions

### 1.1 Where the paper claims novelty — **accepted, with a correction to the evidence and to the wording**
- **The contradiction is real.** The objection table answers "your trilemma just rediscovers
  known limits of control" by placing the novelty in "the joint exhaustiveness argument". §7.6
  concedes that the top-level thesis is definitional, and §7.5 ("The status of the
  exhaustiveness premise, stated honestly") concedes that exhaustiveness rests on a definition
  of control. So the novelty sits exactly where the paper admits triviality.
- **One correction to the evidence.** The plan cites `OPEN_ISSUES.md`, where exhaustiveness is
  "essentially excluded middle". That remark is about Case 3 of the Meta-Optimization Collapse
  Theorem: the three *dynamical cases* are exhaustive by Helmholtz–Hodge plus excluded middle.
  It is not about the trilemma's *three control strategies*. Both exhaustiveness claims are
  weak, so the conclusion stands, but they are different claims and the paper should not run
  them together.
- **The thesis adopted.** The literature search (phase 3, `references/paper1_phase3_literature.md`)
  requires one change to the plan's wording. Dietrich and List's model is not control (nothing
  in it steers), and Bradley's generalised conditioning *represents* a change of fundamental
  desires. Stated as "the dominant formal models are instances of control", the thesis is false
  of the first and has a counterexample in the second. The version adopted:

  > Formal models that direct or evaluate value change locate a fixed evaluative point.
  > *(Originally "direct, evaluate or explain". The author removed "explain" on 2026-09-26, because every explanation fixes some invariant.)*
  > Used to direct change, they are control in the paper's sense and inherit the trilemma. Used
  > only to represent change, they represent it as reabsorption (a moving coordinate within a
  > fixed higher-order structure), or as a change of fundamental values about whose production
  > they are silent.

  This is substantive and contestable, and it can be checked case by case, which is what the
  plan asked for.
- **Consequence.** §7.8 stops being "related work" and becomes the paper's core section (new
  §8), with Dietrich and List, Bradley/Becker, Hansson and Bykvist added. The trilemma is
  presented as the frame, conceded to be definitional, not as the discovery.

### 1.2 Cutting machinery that does not serve the thesis

- **§5 taxonomy (R/P/M/Lambda) — accepted, with one qualification.**
  - The claim that §7 uses only identity preservation and agency preservation is not quite
    right. The theorem's cases are named by the taxonomy: Case 2 is "Class M dispersion", and
    Case 3's limit cycle is Class P. Class G's conditions 1, 6 and 7 are stated in terms of
    Lambda.
  - The *names* are used 18 (M), 12 (P), 9 (R) and 59 (Lambda) times, so they have to be
    defined in the body. The four subsections of argument do not.
  - **Done:** §5 and §6 are reduced to one short section with a four-line definition, and the
    comparison table moves to the appendix.
- **§9 U-limit — partly rejected. It is compressed, not removed.**
  - The plan's reading is that it mainly serves the theology. It does more than that. §7.8.5,
    the non-vacuity check, lists "the conversion of the hostile" as a member of the unanchored
    class. For a hostile subject, Class G's receptivity gate (condition 9: the coupling varies
    with orientation) is closed, so Class G cannot cover that member. The U-limit is the profile
    that does.
  - Appendix A.4 also cedes abrupt, topology-changing reorderings "to Class G and the U-limit".
  - Removing the U-limit would leave a member of the paper's own non-vacuity class without a
    profile.
  - It also speaks to a live debate in the philosophy of action: manipulation versus
    non-manipulative transformation. A unilateral change and a coercive one are identical at the
    moment of the jump and differ only afterwards.
  - **Done:** §9 is reduced to about a third. The theological register and the long synergetics
    analogy move to `drafts/theological_companion.md`. The predicate stays in Appendix A.7.
- **Appendix A.4 (in-silico validation) — accepted.**
  - Simulations do not validate a definitional thesis. The satisfiability witness for Class G
    (`class_g_coherence`) answers a real objection and stays. It is in A.6, not A.4.
  - The numerical check of the finite-gain agency cost (`tracking_cost_curve`) supports the one
    non-analytic claim (§7.6, "costing"). But the claim follows from the control theory already
    cited in §7.3 (funnel and prescribed-performance control). One sentence and a pointer are
    enough.
  - **Done:** A.4 moved verbatim to `experiments/paper1_control_trilemma/IN_SILICO_RECORD.md`;
    §7.7 is reduced to a pointer paragraph.

### 1.3 Target journal — **decided provisionally; this is the author's call and the one decision to override if he disagrees**

Limits checked on the journals' own pages on 2026-09-26:

| Journal | Length | Abstract | Checked |
|---|---|---|---|
| *Synthese* | "does not prescribe a word or page limit … typically between 15 and 30 printed journal pages" | 150–250 words | yes, Springer submission guidelines |
| *Philosophical Studies* | "ordinarily do not exceed 10,000 words, but longer submissions will be considered" | 150–250 words | yes, Springer submission guidelines |
| *European Journal of Philosophy* | reported as "the norm is around 9,000 words … unusual … more than 12,000" | — | no: the publisher page refused access; search summary only |
| *Ergo* | reported as no word limit, "lengthier" papers needing "more news value" | — | no: the journal site blocked automated access; search summary only |
| *Inquiry* | not found | — | no |

- **Recommendation: *Synthese*.** It publishes formal work in the philosophy of action and
  decision theory, and it has no hard limit. Thirty printed pages is roughly 13,000–15,000
  words including notes and appendix.
- **Target: at most 15,000 words all in**, against 31,418 before this restructure and 29,123 after it. The front matter moved into §2 and the new §7.4 was added, so the structural cuts alone save little. The alternative, *Philosophical
  Studies*, would mean about 10,000 words.
- **Order.** The final trim to the target comes last, after the author's two sections (phase
  2). Those sections add text and change what the paper needs.

## Phase 2: the two arguments the plan reserved for the author — **accepted; now §6.6 and §8.4**

*Outcome (2026-09-26):* both sections were drafted with Claude in the project's chat and revised by the author, and inserted as §6.6 and §8.4. The author chose answer A to the influence objection, in a restricted form, and narrowed the thesis to models that direct or evaluate value change ("explain" removed). What follows records how the support material was prepared.

The plan assigns both to the author, and so did an earlier review for the boundary section.
They were not written here. Support material:
- **2.1 The boundary section.**
  - `drafts/boundary_section_support.md` gains a §7 with the plan's three observations and an
    assessment of each. I agree with all three.
  - One caveat on the proposed criterion. Practical identity (Korsgaard) and identification
    (Frankfurt) are *contents* that conversion may itself change. A boundary drawn by them
    risks changing with the event it is meant to classify.
  - The formal accountability relation already in §4.3 (responsibility-bearing history,
    non-branching trajectory) persists through conversion, and may serve better.
- **2.2 The common-influence objection.** A new file, `drafts/influence_objection_support.md`,
  sets out both answers the plan allows, with the textual hooks for each:
  - Class G is narrower than ordinary influence. Condition 10 and the unanchored restriction
    exclude influence whose efficacy runs through the agent's current evaluative standards.
  - The identification is accepted, and the contribution is showing why only this form
    survives.

## Phase 3: literature — **done**

`references/paper1_phase3_literature.md`. In short:
- **Dietrich and List:** the fixed point, not control; it forces the wording above.
- **Bradley 2009:** prior art on reabsorption (Becker's invariant tastes, "as ad hoc" as
  postulating taste change), plus a representation-only counterexample to the loose wording.
- **Hansson 1995:** fixed revision postulates.
- **Bykvist 2006:** a fixed higher-order rule, the precursor of Pettigrew.
- **Carroll et al. 2022:** the cost of exogenous preference shifts is recognized, and judging it
  needs a fixed reference.
- **Counterexamples:** none found among models that *direct* change. The search was not
  systematic.
- **Engagement:** all of these are now engaged in the paper (§7.3, §7.6, §8).

## Phase 4: rewriting and clean-up

- **4.1 Terminology — accepted.** If a term needs discounting, change the term.
  - "Trilemma of Cybernetic Impossibility" becomes "the control trilemma".
  - "Paradox of Exogenous Annihilation" becomes the exogenous horn, and "annihilation" (the
    limit $D_{ag}\to 0$) becomes "agency collapse".
  - "Bellman collapse" becomes the optimization horn (incommensurable objectives).
  - "Transcendental" is dropped. Read against Stroud (1968), a transcendental argument has the
    form "X is a necessary condition of the possibility of Y; Y; so X". The paper's argument
    is a limit on what a framework can formulate, not an argument of that form. The subtitle
    changes accordingly.
  - The note on terminology is deleted, because the terms no longer need it. The conditioned
    sense of the claim is stated once, in §2.
- **4.2 Conclusion — accepted.** The ",," typo is fixed, and the unqualified "the result is
  transcendental" is replaced by the qualified claim the paragraph itself goes on to state.
- **4.3 Objection table — accepted, in part now.**
  - The novelty row is rewritten now (it follows from 1.1).
  - Rows that depend on the author's phase-2 arguments wait: the boundary, and ordinary
    influence.
- **4.4 Final sweep and gate — accepted.**
  - Every "impossibility", "cannot" and "transcendental" was checked.
  - The forbidden-phrase gate gains rules for the retired terms.

## Freeze criterion for Paper 1 (adopted from the plan)

Paper 1 freezes when all of these hold:
1. the boundary section is in the paper — **done**, §6.6 (drafted with Claude, revised by the author);
2. the answer to the common-influence objection is in the paper — **done**, §8.4 (drafted with Claude, revised by the author);
3. Dietrich and List have been engaged — **done**;
4. the text is within the chosen journal's length.

After that, only a reader in the field, and no further audit round.
