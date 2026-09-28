# ACADEMIC-JVP-WORK-

> [!WARNING]
> **Work in progress, developed with generative AI.** All of the research here — papers, code,
> experiments, analyses, formal proofs and website — by João Vitor Perazzolo is being developed
> with the assistance of **Claude**, a generative AI model (Anthropic). AI assistance can
> introduce errors that look correct; several have already been found and corrected in this
> repository. **Please do not rely on what is stated here: re-run the experiments on your own
> computer and check whether the results match.** Confidence in this work should never be 100%,
> and none of it is ready for submission. Full statement: [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) ·
> open problems: [`OPEN_ISSUES.md`](OPEN_ISSUES.md).

Four papers by **João Vitor Perazzolo** (begun July 2026, last revised September 2026) and an in-silico
validation suite that tests their formal and statistical claims. The suite is
deliberately scoped by what simulation and available data *can* and *cannot*
establish for each paper.

**📄 Read it online: <https://fcadusims-droid.github.io/ACADEMIC-JVP-WORK-/>** — the
four papers as navigable web pages *and* as downloadable PDFs, every experiment with
its pre-registration, verdict, figures and raw results. The site is generated from
this repository and rebuilt on every push, so it never lags the work; see
[`site/README.md`](site/README.md) for how it is built and gated.

## The four papers (Papers 1–3 revised 28 September 2026; Paper 4 first version 28 September 2026)

- **`Paper1.md` — The Cybernetic Limits of Conversion: Why Models That Direct Value Change Cannot
  Tell Conversion from Manipulation.** Formal models used to direct or evaluate value change take
  their reference standard from the agent's attitudes (before the change, after it, or a fixed rule
  over both). Conversion and manipulation can share an attitudinal profile, so none of these models
  can tell them apart; the one history-sensitive proposal penalizes conversion along with
  manipulation. The two appendix computations were specified in advance and run; both predictions
  were met.
- **`Paper2.md` — Does an Interoceptive Signal Mark the Transitions a Person Survives? Data
  Requirements, and an Estimability Gate Reversed on Audit, in Public Post-Cardiac-Arrest
  Recordings.** What a test would need, a bounded audit of public corpora (one, I-CARE, qualifies),
  and a heart-period gate that failed as executed (6 of 21) but passes as written in the plan
  (16 of 21); a positive control passes in healthy subjects. Simulation audits of the planned
  statistics.
- **`Paper3.md` — Five Ways a Covariance-Geometry EEG Method Appeared Validated, and the Controls
  That Overturned It.** The validation record of a trace-normalized SPD geometry read through a
  geodesic CUSUM: five traps, the control that exposed each, the field's standard pipeline under the
  same controls, and a survey of published studies.
- **`Paper4.md` — Conversion and Its Counterfeits: Grace, Manipulation, and the Limits of
  Attitudinal Criteria.** Analytic theology, a companion to Paper 1: no criterion of grace made of
  attitudinal features can tell grace from its counterfeits; preparation, fruits and perseverance
  are signs, not criteria; what remains is a condition on the manner of the change. No experiments.

Papers 1–3 are logically independent; Paper 4 restates Paper 1's constraint in self-contained form. The earlier versions (26 September 2026) are kept, with their
titles marked as superseded, in [`archive/papers_2026-09-26_superseded/`](archive/papers_2026-09-26_superseded/).
The experiments specified in the new texts are listed in [`EXPERIMENTOS_2026-09-27.md`](EXPERIMENTOS_2026-09-27.md).

## The experiment suite (`experiments/`)

Computational experiments that check the papers' claims, each with a
`PRE-REGISTRATION.md` written **before** it is run, a machine-readable
`result.json`, and a verdict issued strictly against the pre-registered criterion —
never adjusted after seeing results. Negative and qualified results are reported as
such, not softened.

- **`shared_lib/`** — SPD/density-matrix geometry (square-root, affine-invariant,
  log-Euclidean, Bures-Wasserstein metrics), jump-diffusion simulation,
  Helmholtz-Hodge split, statistics. Self-tested (`test_shared_lib.py`).
- **`paper1_control_trilemma/`**, **`paper2_cbra_protocol/`**,
  **`paper3_geodesic_kinematics/`** — one directory per experiment.
- **`_results/`** — committed outputs (JSON metrics + figures). Raw data
  (`data/`, e.g. PhysioNet EEG/ECG) is **not** committed; see
  `paper3_geodesic_kinematics/DATA.md`.

**[`RESULTS.md`](RESULTS.md) summarises what all 54 experiments found**, organised by
paper, with the open questions at the end.

**`experiments/STATUS.md` is the authoritative live status** — the per-experiment
state and verdict for all runs, including the follow-ups that extend the original
core set.

## Methodology and reproducibility

**`METHODOLOGY.md`** states the protocol every result followed (pre-registration
before execution, verdicts against fixed criteria, raw `result.json` committed,
declared attempt budgets, audit before paper edits) and — the part that matters —
lists the occasions on which that protocol **cost** something: a halt obeyed when
continuing was tempting (B1), a bug fix that made the project's own negative result
stronger (Pan-Tompkins), a pre-registered arm that failed with its rescue labelled
post-hoc (A2), a correction favouring this project's own method quarantined with
full provenance (the Paper 3 benchmark), a claim **withdrawn from Paper 1 after it
had already been merged**, and — the entry to read first — the case where the
discarded result was the *exciting* one: a run refuting a load-bearing clause was
rejected because it rested on an instrument defect.

The work is citable (`CITATION.cff`), and `RELEASING.md` documents how to mint a
Zenodo DOI so the software can be cited independently of the papers.

The library core is installable and tested in CI:

```bash
pip install -e .                    # core (numpy/scipy/matplotlib)
pip install -e ".[data,benchmark]"  # + EDF/WFDB loaders and baseline methods
python -m experiments.shared_lib.test_shared_lib
```

## Setup

```bash
python -m pip install -r experiments/requirements.txt
python -m experiments.shared_lib.test_shared_lib          # verify the shared core
python -m experiments.paper3_geodesic_kinematics.<name>.run   # run an experiment
```

Real-data experiments download their PhysioNet records on first run, so they need network
access to physionet.org.
