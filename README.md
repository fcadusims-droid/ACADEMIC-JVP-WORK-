# ACADEMIC-JVP-WORK-

Three interlinked papers by **João Vitor Perazzolo** (July 2026) and an in-silico
validation suite that tests their formal and statistical claims. The suite is
deliberately scoped by what simulation and available data *can* and *cannot*
establish for each paper.

## The trilogy

- **`Paper1.md` — The Cybernetic Impossibility of Conversion.** A transcendental
  negative critique: given a definition of control as directed change relative to a
  held-fixed evaluative structure, agency-preserving *conversion* (the
  transformation of that structure) cannot be formulated as control without
  collapsing into tautology, annihilation, or incommensurable indeterminacy. Its
  load-bearing formal result is a *Meta-Optimization Collapse Theorem* (a
  trichotomy), and it defines the residual admissibility profile **Class G**.

- **`Paper2.md` — The Conditional Biological Requirements Architecture (CBRA).** A
  strict *eliminative* statistical protocol for whether a biological state
  transition preserves a hidden, identity-indexed boundary organization. It depends
  conceptually on Paper 1 (Class G, the contract *I*) but its empirical fate does
  not feed back. Its secure contribution is eliminative; its positive arm (a
  boundary-residual *dissociation*) is heavily conditioned.

- **`Paper3.md` — The Kinematics of Geodesic Flow on Riemannian Vector Bundles.** A
  single-trajectory, jump-diffusion method for demarcating three geometric regimes
  (asymptotic geodesic drift, isotropic fibre dispersion, structural rank collapse)
  of a non-stationary multichannel signal on a curved state space. It is *logically
  independent* of the two companions and stands or falls as a time-series method.

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

**`experiments/STATUS.md` is the authoritative live status** — the per-experiment
state and verdict for all runs, including the follow-ups that extend the original
core set.

## Setup

```bash
python -m pip install -r experiments/requirements.txt
python -m experiments.shared_lib.test_shared_lib          # verify the shared core
python -m experiments.paper3_geodesic_kinematics.<name>.run   # run an experiment
```

Real-data experiments download their PhysioNet records on first run (network is
reachable through the environment's proxy).
