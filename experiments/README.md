# In-Silico Validation Suite for the JVP Trilogy

Computational experiments that test the **methods and formal claims** of the three
papers in this repository. This suite is deliberately scoped by what simulation
*can* and *cannot* do for each paper.

## What in-silico work can and cannot establish here

The three papers have different epistemic status, so simulation resolves
different problems in each:

| Paper | What it is | What simulation **can** do | What it **cannot** do |
|---|---|---|---|
| **1 — Cybernetic Impossibility** | Dynamical-systems math applied by analogy to theology | Check whether the theorems hold numerically; try to *falsify* the Sec. 7.5/7.6 trichotomy defence with a real agent | Say anything about grace or metanoia — out of scope of any experiment |
| **2 — CBRA** | Statistical protocol on biological tissue | Test the *tool*: statistical power, false-positive rate, whether the added dissociation test is even feasible before spending on real subjects | Prove a "Lambda channel" exists in tissue — only real data can, and even that only partially |
| **3 — Geodesic Kinematics** | Inference method, already in contact with real EEG | Attack the two concrete open problems the appendix already isolated (localization 5/15; drift-vs-jump confusion) | — (this is where simulation pays off fastest) |

**Priority: Paper 3 first** (highest return per effort, problem already isolated),
**Paper 1 second** (checkable, and can falsify the defence as written),
**Paper 2 last** (only the statistical half is testable in silico).

## Pre-registration discipline

Every experiment has a `PRE-REGISTRATION.md` written **before** it is run, stating
its success/failure criterion in advance. This is the standard the papers
themselves claim to follow, and it is the guard against the one real risk here:
running simulations until one matches the desired conclusion — exactly the bias
Paper 2, Sec. 3.3 was written to prevent. Results are written to
`_results/<experiment>/` and never overwrite the pre-registration.

## Layout

```
experiments/
  shared_lib/                      SPD manifold, jump-diffusion, Helmholtz-Hodge,
                                   stats — shared by Papers 1 & 3. Self-tested.
  paper3_geodesic_kinematics/
    drift_jump_confusion_sweep/    Exp D  (run 1st: cheapest, most decisive)
    localization_multiscale/       Exp A
    localization_priors/           Exp B
    cross_dataset/                 Exp C
  paper1_control_trilemma/
    poincare_recurrence_check/     Exp G  (warm-up, trivial numeric check)
    tracking_cost_curve/           Exp F
    rl_agents_trichotomy/          Exp E
  paper2_cbra_protocol/
    dissociation_power_analysis/   Exp H
    criticality_sweep/             Exp I
    metabolic_null_resolution/     Exp J
  _results/                        experiment outputs (figures, JSON metrics)
```

## Recommended execution order

**D → A → B → C** (Phase 1, Paper 3), then **G → F → E** (Phase 2, Paper 1;
G is trivial and serves as a warm-up), then **H → I → J** (Phase 3, Paper 2).

Cheapest-and-most-decisive first within each phase.

## Setup

```bash
python -m pip install -r experiments/requirements.txt
python -m experiments.shared_lib.test_shared_lib     # verify the shared core
```

The shared-library self-tests reproduce the papers' own numerical claims
(square-root metric curvature K = 1/4 at N = 2,3,4; Girsanov drift identifiability
from one path; the covariate-anchored jump guardrail).

## Status

See `STATUS.md` for the live per-experiment state (pre-registered / implemented /
run / verdict).
