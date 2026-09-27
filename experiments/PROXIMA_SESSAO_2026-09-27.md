# Handoff: the 2026-09-27 experiments (stopped at the author's request)

The session ended before any experiment was run: the author's usage limit was about to run out.
**No experiment of `EXPERIMENTOS_2026-09-27.md` has been run and no result exists.**

## Done
- The three papers were replaced by the 27 September 2026 versions. The old ones are in
  `archive/papers_2026-09-26_superseded/`, with titles marked as old.
- E0, as far as this environment allows. The plan and the papers were committed and pushed before
  any run (commit `778a02b`). One `PRE-REGISTRATION.md` per experiment was committed before any run
  (commit `fbe4b6f`).
- Deviation from E0: no Zenodo or OSF release could be made from this environment. **The author
  should create it before the experiments are run.**
- Cross-check against the 54 existing experiments (`EXPERIMENTOS_2026-09-27_crosscheck.md`): none is
  a repeat.
- Code written but **not run**:
  - E1.1 (`paper1_control_trilemma/output_vs_fullstate_tracking/run.py`);
  - E1.2 (`paper1_control_trilemma/kac_recurrence_dimension/run.py`).

## To do next session, in the plan's order
E3.1 → E3.2 → E2.1 → E2.2 → E3.3 → E1.1 → E1.2 → E2.3 → E2.4. E3.4 is not due before 2026-10-07
(`E3.4_DEFERRED.md`).

| Plan | Directory | Code | Data |
|---|---|---|---|
| E3.1 | `paper3_geodesic_kinematics/mdm_matched_control` | to write (copy `mdm_trap_control`, change 2 things) | Sleep-EDF (7 GB, `experiments/data/sleep-edfx`) + EEGMMIDB, both cached in this container but not committed |
| E3.2 | `paper3_geodesic_kinematics/alpha_incremental_test` | to write | EEGMMIDB |
| E3.3 | `paper3_geodesic_kinematics/channel_density_control` | to write (re-run the two controls with 64 channels) | EEGMMIDB |
| E2.1 | `paper2_cbra_protocol/fantasia_positive_control` | to write | Fantasia (PhysioNet; download started and stopped) |
| E2.2 | `paper2_cbra_protocol/multiscale_asymmetry` | to write | Fantasia + first ECG segment of the 21 I-CARE pilot patients |
| E2.3 | `paper2_cbra_protocol/icare_outcome_descriptive` | to write | I-CARE (metadata + ECG, about 3 MB per segment) |
| E2.4 | `paper2_cbra_protocol/audit_recheck` | to write | CHB-MIT EDF headers; VitalDB API |
| E1.1 | `paper1_control_trilemma/output_vs_fullstate_tracking` | **ready** | none |
| E1.2 | `paper1_control_trilemma/kac_recurrence_dimension` | **ready** | none |

A new container may not have the cached data. Downloads from PhysioNet ran at about 300 KB/s in
this one, so Sleep-EDF (7 GB) would take hours.

## Found while preparing, to be reported with the results
- **The I-CARE gate as applied differs from its description.** Paper 2 §2.4, the original
  pre-registration and the plan all say the RR series was resampled at 4 Hz. The code that produced
  6 of 21 computes T on the beat-indexed series, after a 0.3–2.0 s filter and a 4-MAD trim, with no
  interpolation. E2.1 and E2.2 were pre-registered to run both versions.
- **Two passages of Paper 2 have no committed result in the repository:** the common-generator audit
  in §3.3 (false positives growing with record length; 0.1, 0.3 and 0.6 at 95%, 89% and 75% proxy
  fidelity) and the degeneracy table in Appendix A. The older `residual_tests_exercise` reached the
  opposite verdict on the residual-structure tests.
- When results exist: each new experiment needs an entry in `experiments/current_use.json` (the site
  build requires it), and all results go into one file, `experiments/RESULTADOS_2026-09-27.md`.
