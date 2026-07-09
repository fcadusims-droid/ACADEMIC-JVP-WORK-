# Paper 1 — Control Trilemma (Phase 2)

Checkable dynamical-systems claims, and the experiment that can *falsify* the
Sec. 7.5/7.6 defence as written. Simulation says nothing about grace or metanoia —
that is out of scope of any experiment.

| Exp | Folder | Tests |
|---|---|---|
| **G** | `poincare_recurrence_check/` | The "recurrence fraction ≈ 1" numeric claim (warm-up) — ✅ **CONFIRMED** |
| **F** | `tracking_cost_curve/` | Is the exogenous-horn cost curve actually monotone/graded? |
| **E** | `rl_agents_trichotomy/` | Do real learning/evolution agents obey the trichotomy — or falsify it? |

Machinery: `../shared_lib/helmholtz_hodge.py` (gradient/rotational split for the
trichotomy classification). Exp E needs `gymnasium`/`torch` (see
`../requirements.txt`). Each folder has a `PRE-REGISTRATION.md`.

**Honest commitment:** Exp E's decisive cases are the adversarial ones (pure
novelty search, intrinsic curiosity, PBT meta-optimisation). Falsification of the
trichotomy is to be reported as prominently as confirmation.
