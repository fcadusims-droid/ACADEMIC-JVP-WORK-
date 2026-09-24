# Paper 3 — EEG geometry method (Phase 1 plan)

*Planning note from Phase 1. The experiments added since, and every verdict, are in
`../STATUS.md` and `../../RESULTS.md`. Paper 3 is now a methodological negative (*Five Ways
an EEG Geometry Method Looked Validated and Was Not*).*

The only paper already in contact with real data (EEG), with two concrete open
problems the earlier protocol text isolated. Highest return per effort.

| Exp | Folder | Attacks |
|---|---|---|
| **D** | `drift_jump_confusion_sweep/` | Is the drift-vs-jump confusion structural or calibrational? (diagnostic, run first) |
| **A** | `localization_multiscale/` | Recover on-line localization (5/15 → ≥10/15) with multi-scale windows |
| **B** | `localization_priors/` | Smooth the predictability covariate before anchoring the jump |
| **C** | `cross_dataset/` | Separate "method fails" from "this paradigm is adversarial" |

Data: see `DATA.md`. Machinery: `../shared_lib/` (SPD manifold, jump-diffusion,
stats). Each folder has a `PRE-REGISTRATION.md` fixing its success/failure
criterion before the run.

**A+B+C stopping rule:** if localization does not robustly exceed ~8–10/15 across
seeds after all three, report as a confirmed limitation — do not keep tuning.
