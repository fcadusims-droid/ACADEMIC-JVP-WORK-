# Real-EEG Localization — the outstanding confirmation for A/B/C (Paper 3)

**Run after** A, B, C established, on synthetic ground truth, that within-trajectory
localization is solved by a large *persistence-sensitive* window (not multiscale,
not covariate smoothing). PhysioNet was network-blocked at the time; it is now
reachable, so the synthetic conclusion is tested on the appendix's real paradigm.

## Data
PhysioNet EEG Motor Movement/Imagery (`eegbci`), 15 subjects, run 1 (eyes-open) vs
run 2 (eyes-closed). Eyes-closed raises occipital alpha — a change in spatial
correlation *structure*, the transition the trace-normalised geometry is built for.
Occipito-parietal channels (O1, Oz, O2, PO3, POz, PO4, Pz), alpha band 8–13 Hz.

## Two questions (mirroring the appendix)
1. **Between-record structural discrimination** (the appendix's validated 20/20):
   geodesic distance between the eyes-open and eyes-closed mean covariances vs
   within-state distance.
2. **Within-trajectory localization** (the 5/15 open problem): concatenate an
   eyes-open and an eyes-closed segment (amplitude-normalised so the seam is
   structural, not a power step) and score the fragile pointwise, single-large,
   and multiscale detectors against the known seam (±2 s tolerance).

## Pre-registered success/failure criteria
- **Discrimination replicates** if the between/within ratio exceeds 1 in ≥ 80 %
  of subjects (≥ 12/15).
- **The synthetic persistence fix transfers** if the large window localizes in
  ≥ 60 % of subjects (≥ 9/15) AND beats the fragile pointwise detector.
- **SPLIT** (the honest middle outcome, matching the appendix) if discrimination
  replicates but the large window does *not* reach 9/15 — i.e. real spontaneous
  alpha behaves like the sustained-burst regime Exp C flagged as the residual
  limitation.
- **Weak structural signal** if discrimination itself fails (< 12/15) — then the
  localization comparison is inconclusive.

## Stopping rule
One run over the 15 pre-fixed subjects; no tolerance or channel tuning to move the
outcome. Whatever the verdict, it is reported against these criteria.

## Status
Run. Verdict: **SPLIT** — discrimination replicates (12/15), within-trajectory
localization stays hard on real EEG even for the large window (4/15 vs fragile
2/15). Structural discrimination validated; on-line localization remains the
open problem, exactly as the appendix and Exp C anticipated.
