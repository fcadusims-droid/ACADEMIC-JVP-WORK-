Some of what this work needs cannot be done by the author alone, or by running more code. This
page lists those needs: for each one, what is needed, from whom, and which experiment or paper
depends on it. If you can help with any item, please open an issue on the
[GitHub repository](https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-/issues).

## Anyone

- **Reproduce the experiments.** Every experiment has a pre-registration, a `run.py` and a
  committed `result.json`. Running them on your own machine and reporting whether the numbers
  match is the most useful check there is. A failed reproduction will be recorded. See
  [Reproduce](reproduce.html).

## Paper 1 — *The Cybernetic Limits of Conversion*

- **A reader in the philosophy of action.** Paper 1 is addressed to that field, and §7 argues
  with Callard, Paul and Pettigrew. The errors found so far — axioms stated more strongly than the
  theorems they named, "proves" where only an argument was given — are the kind a specialist sees
  in minutes. Most needed: a reading of §6 and of the system-boundary argument (§6.5).
- **The system-boundary section — being written by the author.** Whether relativity to the
  observer's system boundary trivializes the thesis is the paper's central open question. By
  decision it is being written by the author, not by the AI assistant. Support notes:
  `drafts/boundary_section_support.md`.
- **A reader in philosophical theology.** The theological applications (grace, sanctity, acedia,
  resurrection) were moved to a separate draft, `drafts/theological_companion.md`. It needs a
  reader from that field before it becomes a paper.
- *Not currently planned:* a real reinforcement-learning agent for the exogenous-cost experiment
  (`tracking_cost_curve`, now a 2-D field). It would matter only if Paper 1 were aimed at an AI
  alignment venue, and the chosen venue is the philosophy of action.

## Paper 2 — *The Conditional Biological Requirements Architecture*

- **A laboratory partner (open until 2026-12-23).** The protocol's positive arm needs data that no
  public repository holds together:
  - raw multichannel EEG with a concurrent cardiac channel;
  - a contrast between transitions that preserve the person and matched transitions that do not
    (for example, emergence from anaesthesia versus non-recovery after cardiac arrest);
  - hours of recording around each transition;
  - about 40 participants per condition.

  This exists in anaesthesiology and neurointensive-care laboratories, not in repositories. The
  design, with its numbers, is in `drafts/paper2_data_specification.md`. The analysis would be
  registered before any data are seen. If no partnership is under discussion by 2026-12-23,
  Paper 2 moves to a short data-requirements version. A verified shortlist of groups that have
  recorded raw EEG with simultaneous ECG in coma or anaesthesia is in
  `drafts/paper2_candidate_groups.md`. None meets all three properties as published; the closest
  (post-cardiac-arrest coma with survivors and non-survivors in one cohort) lacks only length.
- **Proxy data with a known ground truth, for the 95 % precondition.** The positive rung requires
  a proxy that captures about 95 % of the variance of the process it stands in for. Quantifying
  this for cardio-interoceptive proxies needs recordings in which the proxied process is also
  measured directly. Until such data exist, the precondition is stated as a limit on the positive
  arm, not as a measured property.
- **A reader in anaesthesiology or neurointensive care.** For this paper, that reader is also the
  most likely route to the data.
- *Deferred:* a sensitivity test for the protocol's Test Two (covariance rotation), using a
  network model in which the rotation is emergent rather than injected. It waits on the
  partnership decision above. If Paper 2 is reduced, Test Two may leave the protocol altogether.

## Paper 3 — *Five Ways an EEG Geometry Method Looked Validated and Was Not*

- **A reader in EEG or brain–computer-interface methods.** Paper 3 is the record of five traps:
  centre bias, dependence-blind nulls, pseudo-replication, ocular contamination and confusion
  between recordings. For each it gives the control that exposed it, a check of the field's
  standard Riemannian pipeline, and a survey of published studies. A specialist is the right
  person to judge whether the standard-pipeline control and the survey are fair.
- **A second, independent coder for the literature survey.** The 20 studies were coded by one
  coder. Every code is committed with the quoted sentence that supports it
  (`experiments/_results/trap_literature_survey/result.json`), so a second coder can re-code
  them without re-reading the papers from scratch. Agreement between two coders would make the
  counts citable.
