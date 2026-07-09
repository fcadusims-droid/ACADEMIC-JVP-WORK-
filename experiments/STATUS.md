# Experiment Suite — Live Status

Legend: ⬜ pre-registered · 🟨 implemented · 🟩 run · ✅ verdict issued

| # | Experiment | Paper | State | Verdict so far |
|---|---|---|---|---|
| **Shared** | `shared_lib` + self-tests | 1 & 3 | 🟩 | All self-tests pass; reproduces K=1/4, Girsanov identifiability, jump guardrail, exact Hodge split |
| **D** | drift_jump_confusion_sweep | 3 | ⬜ | — |
| **A** | localization_multiscale | 3 | ⬜ | — |
| **B** | localization_priors | 3 | ⬜ | — |
| **C** | cross_dataset | 3 | ⬜ | — |
| **G** | poincare_recurrence_check | 1 | ✅ | **CONFIRMED** — recurrence fraction ≥ 0.95 for ε ≥ 0.05·span (0.978→0.995); drops to 0.51 at ε=0.01·span. Text's "≈1" holds but should state the ε regime. |
| **F** | tracking_cost_curve | 1 | ⬜ | — |
| **E** | rl_agents_trichotomy | 1 | ⬜ | — |
| **H** | dissociation_power_analysis | 2 | ⬜ | — |
| **I** | criticality_sweep | 2 | ⬜ | — |
| **J** | metabolic_null_resolution | 2 | ⬜ | — |

## Recommended execution order
**D → A → B → C**  (Phase 1, Paper 3)
**G → F → E**  (Phase 2, Paper 1)
**H → I → J**  (Phase 3, Paper 2)

## Notes
- Each experiment writes machine-readable results to `_results/<experiment>/`.
- Verdicts are always issued against the `PRE-REGISTRATION.md` criteria written
  before the run — never adjusted after seeing results.
