## Getting the code

```bash
git clone https://github.com/fcadusims-droid/academic-jvp-work-.git
cd academic-jvp-work-
pip install -e .
```

## Running an experiment

Every experiment is a module. The pattern is uniform:

```bash
python -m experiments.<paper_dir>.<experiment>.run
```

For example:

```bash
python -m experiments.paper1_control_trilemma.class_g_coherence.run
python -m experiments.paper3_geodesic_kinematics.baseline_benchmark.run
python -m experiments.paper3_geodesic_kinematics.detection_repair_heldout.run
```

Each run writes `experiments/_results/<experiment>/result.json` and its figures. The
committed copies of both are what this site displays, so a re-run that disagrees with
what you see here is a reproduction failure worth reporting.

## Shared library and self-tests

The geometry lives in `experiments/shared_lib/`: SPD and density-matrix metrics
(square-root, affine-invariant, log-Euclidean, Bures–Wasserstein), jump-diffusion
simulation, and Cartan anti-development.

```bash
python -m experiments.shared_lib.test_shared_lib
```

The self-tests check defining identities rather than outputs — that the self-log is
zero, that a Bures–Wasserstein geodesic reaches its endpoint, that $(AB)^{1/2}$
squares to $AB$, that the flat metric's base-point and path-wise anti-developments
agree. Two real bugs were caught this way: a HAC drift-test calibration error, and a
future-leakage bug in the predictability covariate.

## Data

Datasets are not committed. Each runner fetches what it needs from PhysioNet into
`experiments/data/`, which is gitignored. See the [data](data.html) page for what is
used where.

## Continuous integration

The test suite runs on every push. This site is rebuilt and redeployed on every push
to the default branch, so the papers, the experiment pages and the figures shown here
track the repository rather than a snapshot of it.

## Formal artefacts

`formal/` carries a Lean 4 formalization of the trichotomy. It compiles with no
`sorry`, and its axioms are audited and listed in `formal/README.md` — the audit
matters more than the compilation, since a formalization is only as strong as what it
assumes.

## Citing

`CITATION.cff` at the repository root carries the machine-readable citation metadata,
and `.zenodo.json` the archival record.
