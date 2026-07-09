# Experiment Suite — Live Status

Legend: ⬜ pre-registered · 🟨 implemented · 🟩 run · ✅ verdict issued

| # | Experiment | Paper | State | Verdict so far |
|---|---|---|---|---|
| **Shared** | `shared_lib` + self-tests | 1 & 3 | 🟩 | Self-tests reproduce K=1/4, Girsanov identifiability (HAC), the geometric jump guardrail, exact Hodge split. Adds `manifold_trajectory.py` (SPD trajectory sim + Cartan anti-development). Two real bugs found & fixed en route: HAC drift-test calibration, and a future-leakage bug in the predictability covariate. |
| **D** | drift_jump_confusion_sweep | 3 | ✅ | **CALIBRATIONAL for strong jumps, STRUCTURAL in one corner.** Strong jumps (collapse ≤ 0.3) stay separable from drift (AUC ≥ 0.85) — a threshold fix. Weak-but-detectable jumps (0.7) vs strong drift overlap (AUC → 0.67) — no threshold separates; a hybrid metric is indicated there. Longer windows worsen it (AUC 0.99→0.76 as T 200→800, holonomy accumulation). Stable (0.41 ± 0.03 across seed banks). Metric tails reproduced (sqrt kurtosis 0.4 vs AIRM 11). See `_results/README.md`. |
| **A** | localization_multiscale | 3 | ✅ | **Criterion met (2/15→15/15), but the fix is WINDOW SIZE, not multiscale.** Synthetic-adversarial (PhysioNet blocked by network policy). Short window 2/15; a single large window already 15/15, matching the multiscale bank → the 5/15 failure is a window-size artifact. Drift guardrail holds. Caveats: offline symmetric windows; real-EEG precision cost untested. |
| **B** | localization_priors | 3 | ✅ | **NO BENEFIT (mechanistic).** Causal smoothing of the predictability covariate monotonically degrades localization (0.36→0.07). An abrupt jump and a sharp excursion share a single-sample covariate signature, so smoothing blurs the jump faster than it denoises. The discriminator that works is persistence (window-mean, Exp A), not covariate smoothing. |
| **C** | cross_dataset | 3 | ✅ | **METHOD ROBUST via persistence.** A large persistence-sensitive window localizes robustly across paradigm strength (15/15 at every ratio) and fluctuation persistence (mild 15→13 as bursts approach window length). A+B+C synthesis: the 5/15 is a fragile-pointwise artifact fixed by a large window (not multiscale, not covariate smoothing); residual open problem = spontaneous bursts longer than the window. All synthetic (PhysioNet blocked); real-EEG confirmation outstanding. |
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
