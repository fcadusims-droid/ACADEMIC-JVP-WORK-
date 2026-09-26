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

Three papers by **João Vitor Perazzolo** (begun July 2026, last revised September 2026) and an in-silico
validation suite that tests their formal and statistical claims. The suite is
deliberately scoped by what simulation and available data *can* and *cannot*
establish for each paper.

**📄 Read it online: <https://fcadusims-droid.github.io/ACADEMIC-JVP-WORK-/>** — the
three papers as navigable web pages *and* as downloadable PDFs, every experiment with
its pre-registration, verdict, figures and raw results. The site is generated from
this repository and rebuilt on every push, so it never lags the work; see
[`site/README.md`](site/README.md) for how it is built and gated.

## The trilogy

- **`Paper1.md` — The Cybernetic Limits of Conversion.** A negative critique:
  given a definition of control as directed change relative to a held-fixed evaluative
  structure, agency-preserving *conversion* (the transformation of that structure)
  cannot be formulated as control without collapsing into tautology, agency collapse,
  or incommensurable indeterminacy. That top level is conceded to be definitional; the
  substantive claim is that the formal models of value change on offer each hold such
  a structure fixed. Its
  load-bearing formal result is a *Meta-Optimization Collapse Theorem* (a
  trichotomy), and it defines the residual admissibility profile **Class G**. It is
  addressed to the philosophy of action; its formal statements are collected in an appendix,
  and its theological applications are in a separate draft (`drafts/theological_companion.md`).

- **`Paper2.md` — The Conditional Biological Requirements Architecture (CBRA).** A
  strict *eliminative* statistical protocol for whether a biological state
  transition preserves a hidden, identity-indexed boundary organization. It depends
  conceptually on Paper 1 (Class G, the contract *I*) but its empirical fate does
  not feed back. Its secure contribution is eliminative; its positive arm (a
  boundary-residual *dissociation*) is heavily conditioned. Run once on the only public corpus
  with the right structure (I-CARE), it halted at its own gate (6 of 21 patients against a 60 %
  bar). The paper now specifies the data a test would need, and a partner laboratory is being
  sought until 2026-12-23.

- **`Paper3.md` — Five Ways an EEG Geometry Method Looked Validated and Was Not.** A methodological negative: how a trace-normalized SPD
  geometry method for EEG looked validated and was not, through five traps (centre bias,
  dependence-blind nulls, pseudo-replication, ocular contamination, recording confound), each
  with the pre-registered control that exposed it, a check of the field's standard
  Riemannian pipeline, and a survey of published studies. The earlier protocol (vector
  bundle, three-regime demarcation) is preserved as a draft. It is *logically independent*
  of the two companions.

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

Real-data experiments download their PhysioNet records on first run (network is
reachable through the environment's proxy).
