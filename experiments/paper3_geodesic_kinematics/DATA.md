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

## PhysioNet Sleep-EDF (Trilha A — sleep second paradigm)
- Sleep-stage transitions; slower but more consistent than spontaneous alpha.
- Openly downloadable from PhysioNet (`sleep-edfx`, sleep-cassette).
- Loader expectation: EDF + hypnogram annotations under `data/sleep-edfx/`.
- Used by `sleep_stage_localization` (A1), `sleep_structure_power_dissociation`
  (A2), and `log_euclidean_real_eeg` (A3), via `pyedflib`. Channels EEG Fpz-Cz /
  Pz-Oz / EOG horizontal.

## PhysioNet I-CARE (Trilha B — the CBRA I+/I− substrate, Paper 2)
- Post-cardiac-arrest coma cohort with concurrent EEG (22-ch) and ECG (1-ch,
  500 Hz), CPC recovery-vs-non-recovery outcome.
- Openly downloadable from PhysioNet (`i-care`, CC-BY-NC-SA). ECG segments ~3 MB,
  EEG segments ~57 MB; ECG and EEG stored as separate `*_ECG.mat` / `*_EEG.mat`.
- Used by `cbra_boundary_residual` (B1) under `data/icare/`, via `scipy.io.loadmat`.

## Anesthesia (optional, unused)
- Only if a suitable public induction/emergence record is found. Not required.

## Network status in this environment
**PhysioNet is reachable in this environment** (general outbound HTTPS goes through
the agent proxy; an earlier note here that it was blocked was stale). Real EEG/ECG
is therefore downloaded and used directly. Raw records are **not committed** — the
`data/` tree is gitignored; only pre-registrations, code, `result.json`, and
figures are committed. To reproduce, run each experiment's `run.py`; the loaders
download or expect the records above under `experiments/data/`.

The real-data verdicts (e.g. localization 5/15 on eyes-open/closed, generalizing to
sleep-onset 10/15 on Sleep-EDF; the CBRA boundary residual failing to be estimable
on I-CARE) are computed on the downloaded PhysioNet records, not on synthetic
proxies. Synthetic-adversarial runs (`shared_lib.jump_diffusion` /
`manifold_trajectory` with an injected transition) remain available for
detector-logic validation with ground truth, and are used where noted, but the
real-data claims rest on the PhysioNet records.
