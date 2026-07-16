# Trilha A1 — Sleep-Stage Structural Discrimination + Localization (Paper 3)

**Generalization test for the trace-normalized SPD geometry and the geodesic
CUSUM detector on a *second, independent* real paradigm.** The appendix's
eyes-open/eyes-closed test discriminated the structural regime (14/15) but
localization within one trajectory stalled at 4–5/15, because spontaneous alpha
bursts are *sustained* and geometrically larger than the transition. Sleep-stage
transitions are the opposite kind of event: **slow, consistent, and physiologically
structural** (spindles, delta, REM eye-movements reorganize the spatial correlation
between anterior EEG, posterior EEG, and EOG). If the CUSUM detector generalizes,
it should localize sleep-stage transitions better than it localized the spontaneous
alpha seam; if it does not, the localization limit is the *method's*, not the
eyes-open/closed paradigm's — either outcome is publishable.

## Data
PhysioNet **Sleep-EDF** (`sleep-edfx`, sleep-cassette), first 15 usable subjects
(first-night recordings). Channels: **EEG Fpz-Cz, EEG Pz-Oz, EOG horizontal**
(→ SPD(3)); 100 Hz. Hypnogram annotations give the 30-s sleep stage
(W, N1, N2, N3/N4, REM). Bandpass 0.5–30 Hz; each channel z-scored so a transition
is a change of *correlation structure*, not of overall power (the trace
normalization removes power anyway). Covariance windows 2 s, step 1 s, rank-floored
and trace-normalized — the same pipeline as the appendix, only the data source and
window scale (sleep is slower than alpha) differ.

## Test 1 — Structural discrimination (N2 vs REM), permutation null
The two most-populated, structurally distinct stages: **N2** (spindles/K-complexes,
frontocentral) vs **REM** (rapid eye movements dominate EOG, low-amplitude mixed EEG).
For each subject pool the covariance windows of all N2 epochs and all REM epochs and
compute the between-stage vs within-stage geodesic-distance ratio, with the
**within-state permutation null this repo commits to** (random interleaved
relabelings of the pooled windows, so slow within-stage drift cancels). A subject
passes if the observed between/within ratio exceeds its permutation null at
p < 0.05 **and** ratio > 1.

- **Pre-registered success:** structural discrimination in **≥ 12/15** subjects.
- **Failure:** < 12/15 — the geometry does not generalize its *discrimination*
  claim to sleep structure (reported as such, not softened).

## Test 2 — Stage-transition localization within one trajectory
For each subject take the **first clean stage transition** in the hypnogram of a
structural type (a switch into or out of REM, or Wake↔N2/N3) with **≥ 90 s** of
contiguous single-stage recording on each side. Build the covariance trajectory over
[t0−90 s, t0+90 s] (z-scored per channel), and run the three detectors head-to-head,
reusing the appendix code verbatim: the **window-mean** break curve (baseline), the
**geodesic F-ratio**, and the **geodesic CUSUM**. A hit is a detected change-point
within **±30 s** (±1 epoch, the scorer's own resolution) of the hypnogram transition.

- **Pre-registered success (generalization):** CUSUM localizes **≥ 10/15**.
- **Informative failure:** if CUSUM stalls at **~8/15 or below**, the localization
  limit is the *method's* (a geodesic change-point on trace-normalized covariance),
  **not** the eyes-open/closed paradigm's — closing that question honestly, since a
  slow consistent structural transition is the easiest case localization could face.
- Between 8 and 10 is reported as "materially better, not solved," mirroring the
  appendix's own bands.

## Fixed choices (declared before the run)
Subjects: first 15 sleep-cassette recordings that (a) load, (b) have ≥ 1 qualifying
N2 and REM epoch bank for Test 1, and (c) have ≥ 1 qualifying transition for Test 2;
recordings failing (b)/(c) are skipped and the next downloaded subject substituted,
recorded explicitly. No tuning of bands, windows, tolerance, or the detectors after
seeing results. Detectors are imported unchanged from `online_localization_cusum` /
`localization_multiscale`; only the data loader is new. Raw per-subject results and
both verdicts go to `_results/sleep_stage_localization/result.json`; the prose
verdict states no more than the per-subject table supports.

## Stopping rule
One run over the 15 subjects for both tests. Whatever the two pre-registered bands
return is the verdict. A localization failure here is a *stronger* negative than the
eyes-open/closed one (sleep transitions are the easy case), and is reported as the
method bound it is.

## Status
Pre-registered. Not yet run.
