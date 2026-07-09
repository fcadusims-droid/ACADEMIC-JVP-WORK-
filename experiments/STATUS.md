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
| **F** | tracking_cost_curve | 1 | ✅ | **CLAIM CONFIRMED.** Double-well explorer under tracking gain: D_ag falls 0.85→0.012 and λ∥ drops −0.09→−11.5, both monotone and graded (the k=1 bifurcation is washed out by exploratory noise). Sec 7.3's graded-monotone finite-gain agency cost is numerically vindicated. |
| **E** | rl_agents_trichotomy | 1 | ✅ | **TRICHOTOMY HOLDS — defence survives.** No candidate is the forbidden positive-entropy-plus-no-recurrence object: gradient→Case 1, hamiltonian→Case 3 (λ≈0, 100% rotational), curiosity→Case 1, novelty search→bounded-recurrent (R=1.0), Lorenz chaos→positive entropy (λ=+0.88) but recurrent (0.995). Sustained novelty without return needs a non-compact space (the escape horn), as the theorem predicts. Sec 7.5/7.6 vindicated. |
| **H** | dissociation_power_analysis | 2 | ✅ | **MARGINAL feasibility; matching is a validity issue.** Imperfect S^{I+}/S^{I−} matching inflates the false-positive rate 3–7× (0.05→0.16→0.35) independent of sample size — the interaction contrast is confounded unless matching is tight (sd≲0.3σ). Even then a moderate effect (SNR 0.8) needs n≈40/condition. Executable but demands tight matching + large samples — a practical limitation, not just ethical. |
| **I** | criticality_sweep | 2 | ✅ | **CONFOUND ROBUST.** A genuinely critical generator (susceptibility exponent p>1) reproduces the gating differential in 15/24 cells (62%), robustly at p≥1.5 across noise/feedback, matching/exceeding the gated signal as criticality grows. Non-critical control (p=1) gives D≈0 (statistic valid). Sec 15.5's concession stands — CBRA's defensible arm is eliminative, not detection. |
| **J** | metabolic_null_resolution | 2 | ✅ | **RESOLUTION THRESHOLD QUANTIFIED.** The null absorbs the structured boundary residual only when its resolution is finer than h*≈0.7–0.9 ell, and h* grows monotonically with the diffusion length (0.73→0.93 as L_D 0.05→0.25·ell). Strong null := resolution < h*(L_D). Metabolism keeps the residual 20× more structured. Sec 7.2's qualitative claim is now a number. |

## Recommended execution order
**D → A → B → C**  (Phase 1, Paper 3)
**G → F → E**  (Phase 2, Paper 1)
**H → I → J**  (Phase 3, Paper 2)

## Notes
- Each experiment writes machine-readable results to `_results/<experiment>/`.
- Verdicts are always issued against the `PRE-REGISTRATION.md` criteria written
  before the run — never adjusted after seeing results.
