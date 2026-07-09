# Data access notes — Paper 3 experiments

The Paper 3 experiments (A, B, C) need real EEG. None of it is committed to the
repo; each experiment downloads or expects a local path.

## PhysioNet EEG Motor Movement/Imagery (Exp A, B — the appendix paradigm)
- The eyes-open (R01) / eyes-closed (R02) baseline runs are the structural
  transition used in the appendix.
- Openly downloadable from PhysioNet (`eegmmidb`). ~1.6 GB for all 109 subjects;
  the appendix used ≤ 20 subjects, so a subset suffices.
- Loader expectation: EDF files under `data/eegmmidb/`. The multiscale detector
  reads channel covariance sequences, not raw EDF, so a small preprocessing step
  (bandpass → sliding-window covariance → rank-floor → trace-normalise) sits in
  each experiment's `run.py`.

## PhysioNet Sleep-EDF (Exp C — stronger structural transition)
- Sleep-stage transitions; slower but more consistent than spontaneous alpha.
- Openly downloadable from PhysioNet (`sleep-edfx`).
- Loader expectation: EDF + hypnogram annotations under `data/sleep-edfx/`.

## Anesthesia (Exp C secondary — optional)
- Only if a suitable public induction/emergence record is found. Not required for
  the A+B+C verdict.

## Offline / no-network fallback
When EEG is unavailable, each Paper 3 experiment can run in `--synthetic` mode on
`shared_lib.jump_diffusion` trajectories with an injected structural transition,
to validate the *detector logic* (not the real-data claim). The real-data verdict
requires the PhysioNet records above.

## Network status in this environment (2026-07)
**PhysioNet is blocked by the environment's network policy** — the agent proxy
returns 403 to `CONNECT physionet.org:443` (only package registries such as PyPI
are on the allowlist). Real EEG therefore cannot be downloaded here. The Paper 3
experiments run in the synthetic-adversarial mode described above: a known
structural transition is embedded in spontaneous structural fluctuations large
enough to reproduce the appendix's failure mode (the true transition is not the
most abrupt geometric event), so the *method improvement* (multi-scale windows,
covariate smoothing) can be tested against ground truth. This validates the tool,
not the real-data 5/15 → 10/15 claim, which still requires the PhysioNet records
on a network-enabled environment.
