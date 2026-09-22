# Open issues — all three papers are work in progress

**None of the three papers is ready for submission.** This file used to be titled
"Submission readiness" and declared Paper 3 "ready first"; that was premature and is
withdrawn. What follows is what remains open for each paper, including problems found by
external review. It is a working list, not a checklist toward a deadline.

## Paper 3 — *Kinematics of Geodesic Flow*

- **The title and scope promise what the abstract denies.** The title names a geodesic-flow
  protocol on Riemannian vector bundles for the asymptotic demarcation of three regimes. The
  abstract (correctly) says the three-regime demarcation has never been run end-to-end, the
  bundle apparatus is net negative where tested, and detection does not beat standard
  baselines. An external review recommends re-scoping the paper to what survived — the
  structure-versus-power behaviour of the trace-normalised SPD base — with the fibre and the
  three regimes moved to future work. That is an authorial decision and has not been made.
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
- **The external-referent result tests a proxy, not the demarcation.** The AASM binding
  (`regime_external_referent`, re-tested in `regime_referent_nulls`) is a geodesic-volatility
  median split, not the drift/diffusion/jump or Lyapunov/complexity demarcation the paper
  describes. See `STATUS.md` for what survives the corrected nulls.
- **Power.** The H1 comparison is underpowered (n = 22); the pre-registered power-up needs
  ~74 records and is blocked in the cloud environment (`round2_blocked_on_session_egress`).

## Paper 1 — *The Cybernetic Impossibility of Conversion*

- **The formalization rested on false axioms (now corrected).** The first `Trichotomy.lean`
  declared pointwise versions of Poincaré and Conley that are false;
  `formal/Counterexamples.lean` refutes them and the files now assume the true forms. The
  consequence for the paper: the forbidden object is excluded for *almost every* initial
  condition, not every, and the positive-entropy clause does no work (§7.5).
- **Internal consistency of claim strength.** The abstract, orientation and conclusion said
  "proves"; §2.1 said the paper presents no deductive proof; §7.6 concedes the top-level
  thesis is definitional. The wording has been aligned to §7.6; any new text should keep to it.
- **Open problem.** Characterising the admissible identity contracts (§7.5) remains open and
  may be ill-posed under §2.2's pragmatic reading.
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
