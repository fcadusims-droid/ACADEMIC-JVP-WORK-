# Open issues — all three papers are work in progress

**Freeze criterion (adopted 2026-09-23).** After the items of the current development plan (Paper 3: the MDM control, the literature survey and the restructure; Paper 1: the boundary section, now §6.6, drafted with Claude and revised by the author; Paper 2: the partnership decision), only factual-error corrections enter the papers. No new experiment is run unless a decision point depends on its result. The public list of what the work needs from others is on the site's [Needs](https://fcadusims-droid.github.io/ACADEMIC-JVP-WORK-/needs.html) page and in `site/content/needs.md`.

**None of the three papers is ready for submission.** This file used to be titled
"Submission readiness" and declared Paper 3 "ready first"; that was premature and is
withdrawn. What follows is what remains open for each paper, including problems found by
external review. It is a working list, not a checklist toward a deadline.

## Paper 3 — *Five Ways an EEG Geometry Method Looked Validated and Was Not*

- **Restructured (2026-09-23) as a methodological negative, per the author's decision.** The
  earlier protocol text (vector bundle, jump-diffusion, three-regime demarcation) is preserved in
  `drafts/paper3_protocol_full_2026-09-23.md`.
- **Framing follows the pre-registered rule: traps of this method, read as traps of this
  design.** `mdm_trap_control` found none of the four applicable traps moved the field's
  standard covariance→MDM pipeline past its bar. But the control changed the design as well as
  the classifier: it keeps each epoch's amplitude (no trace normalization) and uses non-overlapping
  epochs. The paper now says so, and labels as interpretation its explanation of why the
  standard pipeline escaped. Band-pass filtering followed by trace normalization removes the
  amplitude of a band relative to the rest of the spectrum, not power in general. Where the
  states differ in that amplitude (alpha, eyes open vs closed), that leaves correlation structure and artefacts to
  carry it.
- **Not run: a matched control.** The same MDM on trace-normalized covariances of overlapping
  windows would say which difference protects the standard pipeline. By the freeze criterion it
  is not run unless a decision depends on it.
- **The survey measures reporting, not the presence of a trap.** Ocular handling is unreported in
  7/19 studies, 7–15/19 counting the unclear codes. Dependence-blind validation is 4/19,
  4–12/19 counting them. The paper gives ranges and does not claim the traps are general
  properties of the field.
- **The survey had one coder.** A second, independent coder of the 20 studies (every code is
  quoted, so re-coding is straightforward) would make the counts citable. Listed on the site's
  Needs page.
- **Not tested: whether the geometry carries information beyond per-channel alpha power.**
  That needs an incremental comparison (scalar alone versus scalar plus geometry). By the freeze
  criterion it is not run unless a decision depends on it.
- **The recording confound for the standard pipeline is below the bar but not zero**
  (0.65 on two same-state recordings; chance 0.50, eyes open vs closed 0.87). The abstract and
  conclusion now say "below the pre-registered bar, but above chance".
- **A reader in EEG or brain–computer-interface methods** is the most useful next step (Needs page).

## Paper 1 — *The Cybernetic Limits of Conversion*

- **The formalization rested on false axioms (now corrected).** The first `Trichotomy.lean`
  declared pointwise versions of Poincaré and Conley that are false;
  `formal/Counterexamples.lean` refutes them and the files now assume the true forms. The
  consequence for the paper: the forbidden object is excluded only for states typical of the flow's invariant measure — almost every initial condition for conservative dynamics, but nothing about the transients of dissipative dynamics, where the exclusion rests on an interpretive argument (§6.5). Case 3's exhaustiveness is essentially
  excluded middle; the argumentative load now sits on the interpretation of the cells.
- **Internal consistency of claim strength.** The abstract, orientation and conclusion said
  "proves"; §2.1 said the paper presents no deductive proof; §6.7 concedes the top-level
  thesis is definitional. The wording has been aligned to §6.7; any new text should keep to it.
- **Open problem.** Characterising the admissible identity contracts (§6.5) remains open and
  may be ill-posed under §2.2's pragmatic reading.
- **The Class-G / reabsorption line depends on the system boundary.** Including the trigger's
  source in the system makes the flow autonomous again, and the same event then reads as
  reabsorption. §6.6 (added 2026-09-26) answers this with an admissibility criterion: the boundary
  of the bearer of the responsibility-bearing history (§4.3). It adds that the enlarged boundary
  changes the subject of the claim. Still open, and stated there: genuine joint agents, and cases
  where responsibility attributions are themselves contested.
- **Framing (decided 2026-09-23).** Paper 1 is addressed to the philosophy of action, where §7 already argues with Callard, Paul and Pettigrew. The theological sections (formerly §§10–12) were moved to `drafts/theological_companion.md`, a second paper still to be written that cites the first. The formalism was moved into Appendix A (2026-09-24). The body now states in words: the contract *I* (§2.2, §4); the distinction between a non-tracking trigger and deviation-penalizing tracking (§6.3, §6.5); the identity-bearing/agency-bearing vocabulary and the two constraints (§6.1); the theorem's three cases (§6.5); and the Class G definition, with its ten conditions in words (§8.3). The equations, the theorem's formal statement, the simulation numbers and the U-limit predicate are in the appendix, moved verbatim, so every checked sentence is still in the paper. The system-boundary argument is now §6.6 (see below).
- **Restructured around its substantive claim (2026-09-26).** A colleague's plan, assessed and carried out point by point in `drafts/paper1_restructure_plan.md`. What changed:
  - The contribution is no longer the trilemma's "joint exhaustiveness", which §6.7 concedes is definitional. It is the case-by-case claim of section 7 (formerly §7.8, "related work"): the formal models of value change on offer each hold an evaluative point fixed.
  - Dietrich and List, Hansson, Bradley (Becker's thesis), Bykvist and Carroll et al. 2022 were verified and engaged (`references/paper1_phase3_literature.md`). No model that *directs* a change of fundamental values without a fixed reference was found. Bradley's generalised conditioning *represents* such a change without saying what produces it, which is why the thesis is worded as it is.
  - Retired terms: "transcendental", "annihilation", "Bellman collapse", "Trilemma of Cybernetic Impossibility". The note on terminology is gone, and a gate rule blocks the old terms.
  - §5–6 were compressed. The U-limit (§9) was compressed, not removed, because the conversion of the hostile in §7.6 needs it. The in-silico appendix moved to `experiments/paper1_control_trilemma/IN_SILICO_RECORD.md`.
  - The full earlier text is `drafts/paper1_full_2026-09-26.md`.
- **The two arguments the plan reserved for the author are in the paper (2026-09-26).** Both were drafted with Claude in the project's chat and revised by the author; neither was written by the author alone (`AI_DISCLOSURE.md`).
  - (1) §6.6, the system boundary. It gives an admissibility criterion, argues that the enlarged boundary changes the subject, and leaves joint agents open.
  - (2) §8.4, "Is Class G just ordinary interpersonal influence?". It chooses answer A in a restricted form, with an *anchored* criterion: endorsable ex ante by the pre-change standards. Answer B was rejected because it contradicts §7.4, where persuasion by reasons is Bradley's first model and so falls under the endogenous horn.
  - The objection table has a new row.
  - The thesis wording was narrowed by the author: models that **direct or evaluate** value change, no longer "explain". With "explain" the thesis would be close to trivial, since every explanation fixes some invariant.
- **Target journal and length (decided by the author, 2026-09-26; target corrected the same day).** *Synthese*, whose guideline of 15–30 printed pages covers the whole article. Target: body plus notes at most 13,500 words; appendix at most 2,500; uncited references leave the list.
  - **Met (2026-09-26), after two approved rounds of cuts.** Body plus notes: 13,297 words (25,428 before the cuts). Appendix: 2,427 (5,070 before). References: 56 (64 before).
  - The earlier texts are preserved: `drafts/paper1_precut_2026-09-26.md` before round 1, and `drafts/paper1_precut_round2_2026-09-26.md` before round 2 and the appendix cuts. What was cut, and why, is in `drafts/paper1_cut_map.md`.
  - §8.4's manipulation paragraph now rests on condition 8 of §8.3 (no fixed optimum target), and says the reading is an interpretation of that condition, not a consequence of it. No condition was added to §8.3, so `class_g_coherence` and `class_g_independence` still test the definition in the paper.
  - The phrase "external gift" remains in two places: the row for condition 9 in the §8.3 table, and the matching row of the A.5 table. It is left for the author to decide, since the §8.3 tables were protected.
- **Freeze criterion for Paper 1.** Paper 1 freezes when all four hold:
  1. the boundary section is in the paper — **done**, §6.6;
  2. the answer to the common-influence objection is in the paper — **done**, §8.4;
  3. Dietrich and List have been engaged — **done**, §7.4;
  4. the text is within the chosen journal's length — **done** (13,297 of 13,500 body words; 2,427 of 2,500 appendix words).

  **Paper 1 is frozen (2026-09-26).** Only corrections of factual error enter it. What remains is a reader in the field (site Needs page).

  After that, only a reader in the field, and no further audit round.

## Paper 2 — *The Conditional Biological Requirements Architecture*

- **Format.** It cannot be a Registered Report: that format requires in-principle
  acceptance of the Stage-1 protocol before data collection and analysis, and the analysis
  has already been run. Compatible forms, if and when it is finished, are a protocol paper
  with a pre-registered negative result or a data/resource paper on the data requirements.
  (This file previously labelled it "Registered Report format"; that was wrong.)
- **Scope of the negative.** The 6/21 (29%) against a 60% bar is a result on one
  post-cardiac-arrest corpus whose sedation, temperature management and pressors plausibly
  suppress the signal; it is not a verdict on the architecture. The title and abstract now
  say "in public data" and name the corpus confound.
- **Positive arm.** Not executable on public data as of 2026-09 (`cbra_dataset_inventory`).
- **Route (decided 2026-09-23): partnership first, until 2026-12-23.** The data the positive arm needs exist in anaesthesiology and neurointensive-care laboratories, not in repositories. A data specification for a partner lab is in `drafts/paper2_data_specification.md`, as a draft for the author to review and sign; it has not been sent. A shortlist of candidate groups is in `drafts/paper2_candidate_groups.md` (2026-09-24). Each group has at least one verified study that recorded raw EEG with simultaneous ECG in coma or anaesthesia; none meets all three data properties as published. A *new* collection with the protocol registered first could be a genuine Registered Report. That is distinct from the I-CARE analysis, which cannot be one. If no partnership is under discussion by 2026-12-23, the paper moves to the reduced version: a short data-requirements paper with the I-CARE negative, without Paper 1's vocabulary (Class G, contract *I*).
- **Test Two sensitivity (deferred).** Test Two has shown specificity but has no emergent true positive. The planned test uses a network model in which the rotation is emergent, not injected, and pre-registers the model family and the hit rate across its parameter space, not a first positive case. It waits on the route decision above: under the reduced version, Test Two may leave the protocol.
- **The 95 % variance-capture precondition.** This needs proxy recordings with directly measured ground truth, which are not public. Until they exist, it is stated as a limit on the positive arm.

## Not blocked on the papers, but pending

- Mint a Zenodo DOI (`RELEASING.md`) — a software-citation step, not a readiness signal.
