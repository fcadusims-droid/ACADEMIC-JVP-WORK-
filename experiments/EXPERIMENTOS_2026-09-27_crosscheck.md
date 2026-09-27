# Cross-check: the 2026-09-27 experiment plan against the 54 experiments already in the repository

The author asked (27 September 2026) that no experiment be repeated. Each experiment in
`EXPERIMENTOS_2026-09-27.md` was compared with the existing experiments before any was run.

| Plan | What it asks | Closest existing experiment | Already done? | Action |
|---|---|---|---|---|
| E3.1 | MDM given trace normalization and overlapping windows | `mdm_trap_control` (non-overlapping epochs, no trace normalization) | No: the existing one is the unmatched control that E3.1 exists to complement | New: `mdm_matched_control` |
| E3.2 | Logistic regression on alpha power, with and without tangent-space geometry, leave one subject out | `between_recording_control` (distance ratios, no incremental model) | No | New: `alpha_incremental_test` |
| E3.3 | The two between-recording controls with 64 channels | `between_recording_control` and `detection_between_recording_control` (7 channels) | No: no experiment used 64 channels | New: `channel_density_control` |
| E3.4 | Intra-rater re-coding of the survey | `trap_literature_survey` (first coding) | Not yet due | Deferred: not before 2026-10-07 (`experiments/E3.4_DEFERRED.md`) |
| E2.1 | Positive control of the gate on Fantasia | none (Fantasia appears nowhere in the repository) | No | New: `fantasia_positive_control` |
| E2.2 | Beat-indexed multiscale asymmetry, Fantasia and the 21 I-CARE patients | `cbra_boundary_residual` (single scale, the gate itself) | No | New: `multiscale_asymmetry` |
| E2.3 | I-CARE, 50 good against 50 poor outcome, descriptive | `cohort_reestimation_blocked` (a different re-test, documented as blocked, never run) | No | New: `icare_outcome_descriptive` |
| E2.4 | ECG channels in CHB-MIT files; raw EEG in VitalDB tracks | `cbra_dataset_inventory` and `dataset_viability_gate` (documentation only: "typically no concurrent cardiac channel") | No: the files themselves were never checked | New: `audit_recheck` |
| E1.1 | Output against full-state tracking | `tracking_cost_curve` (agency cost of full tracking; no output-only arm, no null space) | No | New: `output_vs_fullstate_tracking` |
| E1.2 | Kac return time against dimension on a torus rotation | `poincare_recurrence_check` (Lorenz recurrence fraction; no dimension scaling) | No | New: `kac_recurrence_dimension` |

**Result.** None of the ten was already done. Nine are run; E3.4 waits for its date. All results
go into one file, `experiments/RESULTADOS_2026-09-27.md`.
