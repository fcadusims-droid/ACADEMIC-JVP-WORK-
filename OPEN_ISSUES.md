# Open issues — all three papers are work in progress

**Freeze criterion (adopted 2026-09-23).** After the items of the current development plan (Paper 3: the MDM control, the literature survey and the restructure; Paper 1: the author's boundary section; Paper 2: the partnership decision), only factual-error corrections enter the papers. No new experiment is run unless a decision point depends on its result. The public list of what the work needs from others is on the site's [Needs](https://fcadusims-droid.github.io/ACADEMIC-JVP-WORK-/needs.html) page and in `site/content/needs.md`.

**None of the three papers is ready for submission.** This file used to be titled
"Submission readiness" and declared Paper 3 "ready first"; that was premature and is
withdrawn. What follows is what remains open for each paper, including problems found by
external review. It is a working list, not a checklist toward a deadline.

## Paper 3 — *Five Ways an EEG Geometry Method Looked Validated and Was Not*

- **Restructured (2026-09-23) as a methodological negative, per the author's decision.** The
  earlier protocol text (vector bundle, jump-diffusion, three-regime demarcation) is preserved in
  `drafts/paper3_protocol_full_2026-09-23.md`.
- **Framing follows the pre-registered rule: traps of this method.** `mdm_trap_control` found
  none of the four applicable traps moved the field's standard covariance→MDM pipeline past its
  bar. The survey (`trap_literature_survey`) qualifies this: ocular handling is left open or
  unreported in 7/19 studies (8 unclear), and dependence-blind validation in 4/19 (8 unclear).
  The paper says both things. It does not claim the traps are general properties of the field.
- **The survey had one coder.** A second, independent coder of the 20 studies (every code is
  quoted, so re-coding is straightforward) would make the counts citable. Listed on the site's
  Needs page.
- **Not tested: whether the geometry carries information beyond per-channel alpha power.**
  That needs an incremental comparison (scalar alone versus scalar plus geometry). By the freeze
  criterion it is not run unless a decision depends on it.
- **The recording confound for the standard pipeline is below the bar but not zero**
  (0.65 on two same-state recordings). A reader in EEG methods should judge whether that
  deserves more than the paper gives it.
- **A reader in EEG or brain–computer-interface methods** is the most useful next step (Needs page).

## Paper 1 — *The Cybernetic Limits of Conversion*

- **The formalization rested on false axioms (now corrected).** The first `Trichotomy.lean`
  declared pointwise versions of Poincaré and Conley that are false;
  `formal/Counterexamples.lean` refutes them and the files now assume the true forms. The
  consequence for the paper: the forbidden object is excluded only for states typical of the flow's invariant measure — almost every initial condition for conservative dynamics, but nothing about the transients of dissipative dynamics, where the exclusion rests on an interpretive argument (§7.5). Case 3's exhaustiveness is essentially
  excluded middle; the argumentative load now sits on the interpretation of the cells.
- **Internal consistency of claim strength.** The abstract, orientation and conclusion said
  "proves"; §2.1 said the paper presents no deductive proof; §7.6 concedes the top-level
  thesis is definitional. The wording has been aligned to §7.6; any new text should keep to it.
- **Open problem.** Characterising the admissible identity contracts (§7.5) remains open and
  may be ill-posed under §2.2's pragmatic reading.
- **The Class-G / reabsorption line depends on the system boundary.** Including the trigger's
  source in the system makes the flow autonomous again, and the same event then reads as
  reabsorption. §7.5 now states the boundary as an observer's pragmatic choice (like *I*, §2.2);
  whether a principled criterion for drawing it exists is open.
- **Framing (decided 2026-09-23).** Paper 1 is addressed to the philosophy of action, where §7.8 already argues with Callard, Paul and Pettigrew. The theological sections (formerly §§10–12) were moved to `drafts/theological_companion.md`, a second paper still to be written that cites the first. Still open for the author: whether to move the formalism into an appendix, as a reviewer suggested; and writing the central argument that relativity to the system boundary does not trivialize the thesis (see `drafts/boundary_section_support.md`). That section should be written by the author.

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
- **Route (decided 2026-09-23): partnership first, until 2026-12-23.** The data the positive arm needs exist in anaesthesiology and neurointensive-care laboratories, not in repositories. A data specification for a partner lab is in `drafts/paper2_data_specification.md`, as a draft for the author to review and sign; it has not been sent. A *new* collection with the protocol registered first could be a genuine Registered Report. That is distinct from the I-CARE analysis, which cannot be one. If no partnership is under discussion by 2026-12-23, the paper moves to the reduced version: a short data-requirements paper with the I-CARE negative, without Paper 1's vocabulary (Class G, contract *I*).
- **Test Two sensitivity (deferred).** Test Two has shown specificity but has no emergent true positive. The planned test uses a network model in which the rotation is emergent, not injected, and pre-registers the model family and the hit rate across its parameter space, not a first positive case. It waits on the route decision above: under the reduced version, Test Two may leave the protocol.
- **The 95 % variance-capture precondition.** This needs proxy recordings with directly measured ground truth, which are not public. Until they exist, it is stated as a limit on the positive arm.

## Not blocked on the papers, but pending

- Mint a Zenodo DOI (`RELEASING.md`) — a software-citation step, not a readiness signal.
