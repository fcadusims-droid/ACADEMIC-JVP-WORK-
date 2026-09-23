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

- **A reader in the philosophy of action.** Paper 1 is addressed to that field, and §7.8 argues
  with Callard, Paul and Pettigrew. The errors found so far — axioms stated more strongly than the
  theorems they named, "proves" where only an argument was given — are the kind a specialist sees
  in minutes. Most needed: a reading of §7 and of the system-boundary argument (§7.5).
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
  Paper 2 moves to a short data-requirements version.
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

## Paper 3 — *Geodesic Kinematics on the Covariance Manifold*

- **A reader in EEG or brain–computer-interface methods.** Paper 3 is being restructured as a
  methodological negative: five ways an EEG geometry method looked validated and was not (centre
  bias, a null that ignores dependence, pseudo-replication, ocular contamination, and confusion
  between recordings). The claim that these are traps of the *field*, not only of this method,
  rests on a control run on the field's standard pipeline and on a survey of published studies.
  A specialist is the right person to check both.
