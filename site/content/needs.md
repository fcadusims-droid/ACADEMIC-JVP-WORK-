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

- **A reader in the philosophy of action or of personal autonomy.** The 27 September 2026
  version argues that formal models of value change inherit the manipulation problem familiar
  from the autonomy literature (Christman, Mele, Fischer and Ravizza). A specialist is the right
  person to judge the indiscernibility argument (§5) and the case-by-case treatment of the models
  (§6), especially the reading of influence-aware alignment as the one history-sensitive
  exception (§6.8).
- **A reader in AI alignment.** §6.7 and §6.8 make claims about value learning, corrigibility and
  preference-influence work (Carroll et al. 2022, 2023, 2024) that someone from that field should
  check.
- **A reader in philosophical theology**, for the separate theological draft
  (`drafts/theological_companion.md`), which is not part of the current Paper 1.

## Paper 2 — *Does an Interoceptive Signal Mark the Transitions a Person Survives?*

- **A laboratory partner (open until 2026-12-23).** A real test needs a private cohort: a clean
  cardiac channel recorded before heavy sedation, concurrent raw EEG, outcome follow-up and severity
  covariates sufficient for matching. That exists in anaesthesiology and neurointensive-care
  laboratories, not in repositories. The design is in `drafts/paper2_data_specification.md`, and a
  verified shortlist of groups is in `drafts/paper2_candidate_groups.md`. If no partnership is under
  discussion by 2026-12-23, the paper stays in its data-requirements form.
- **A reader in heart-rate variability or neurointensive care**, to judge the estimability gate,
  its missing positive control and the follow-up analyses the paper specifies (§2.6).

## Paper 3 — *Five Ways a Covariance-Geometry EEG Method Appeared Validated*

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
