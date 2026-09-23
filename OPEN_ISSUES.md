# Open issues — all three papers are work in progress

**None of the three papers is ready for submission.** This file used to be titled
"Submission readiness" and declared Paper 3 "ready first"; that was premature and is
withdrawn. What follows is what remains open for each paper, including problems found by
external review. It is a working list, not a checklist toward a deadline.

## Paper 3 — *Geodesic Kinematics on the Covariance Manifold*

- **Title and scope (resolved by retitling).** The earlier title promised a geodesic-flow protocol
  on Riemannian vector bundles for the asymptotic demarcation of three regimes, which the abstract
  then denied. An external review recommended re-scoping to the structure-versus-power behaviour
  of the trace-normalised base; `between_recording_control` then removed that support. A later
  review proposed framing the paper by what it delivers. The paper is now titled *Geodesic
  Kinematics on the Covariance Manifold: A Proposed Single-Trajectory Protocol for Regime Change,
  with Its Benchmarks and Failure Modes*; the bundle and the three-regime demarcation are kept in
  the body as a proposed extension. Whether to cut them entirely remains open.
- **Localization numbers are inflated by a centring artefact.** Every within-trajectory
  localization run places the true transition at the window centre by construction; a
  trivial "always predict the middle" detector scores 22/22 there and 0/22 off-centre
  (`localization_centerbias_control`). The previously quoted "10/15 vs the best baseline's
  8/15" must not be used as an argument for the method; off-centre, the manifold ties a
  scalar band-power CUSUM exactly (10/22 vs 10/22).
- **The structural-scenario result falls short of its own bar.** On a structural transition
  with power held constant the geometry localizes at 1.00 against the best power baseline's
  0.75 — a +0.25 margin, short of the +0.30 fixed in advance. It is not established at the
  pre-registered level.
- **The external-referent result tests a proxy, and its advantage is the eye.** The AASM binding
  (`regime_external_referent`) is a geodesic-volatility median split, not the demarcation. Its
  re-test survives a dependence-preserving null, but the 7 recordings are 4 subjects (no
  significance claim is possible) and the covariance includes horizontal EOG: EOG power alone
  binds more strongly, and without EOG the geometry's association nearly vanishes
  (`regime_referent_eog_control`).
- **The sleep structural discrimination is the eye too.** A1's N2-vs-REM 14/15 holds in only 2 of
  4 subjects without the EOG channel (`discrimination_eog_ablation`). What remains is the
  eyes-open/closed difference, modest against within-recording drift (12/15 subjects, median
  ≈1.3; the often-quoted ≈3.3 uses a permutation estimator that ignores autocorrelation).
- **The eyes-open/closed result is a between-recording difference, and power carries it better.**
  `between_recording_control`: it exceeds a same-state between-recording control only weakly
  (task-run rest periods, 11/15, p ≈ 0.024, with a control biased in the method's favour), and a
  scalar per-channel relative-alpha-power baseline separates the states far more strongly (median
  ≈3.5 vs ≈1.3, p ≈ 10⁻⁴). It is described as "a difference between two recordings that exceeds
  each one's internal drift", not as structural discrimination. T0 eyes-open status is not
  documented by PhysioNet; alpha power is only consistent with eyes open (14/15).
- **Detection's out-of-sample evidence is marginal.** `detection_between_recording_control`: a
  change of recording alone fires the scale-normalised statistic (AUC 0.74); a change of state is
  separated from a same-state recording change at AUC 0.72, just above the 0.70 bar (±0.1 at
  n = 15). A larger held-out set with same-state between-recording nulls is needed.
- **Geometry vs scalar, overall.** On no task has the geometry yet been shown to add anything over
  a scalar carrying the same channels: centring-corrected localization ties a scalar, and the
  stage-association advantage was EOG power. A fair test needs EEG-only covariances and scalar
  baselines from the same channels, on more subjects.
- **Power (resolved against the method).** The H1 power-up ran on all 151 usable Sleep-EDF
  sleep-cassette recordings (78 subjects), off-centre (`h1_powerup_offcentre`): manifold 59/151 vs
  scalar 67/151 (p ≈ 0.38), subject level 32/78 vs 42/78 (p ≈ 0.12), the same without EOG.
  Pre-registered verdict inconclusive, but at twice the planned n and with the direction favouring
  the scalar, the geometry adds nothing to sleep-transition localization.

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
- **Framing** (philosophy of action / analytic theology vs an alignment venue) is undecided.

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

## Not blocked on the papers, but pending

- Mint a Zenodo DOI (`RELEASING.md`) — a software-citation step, not a readiness signal.
