# Beat-indexed, multiscale time irreversibility (E2.2)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E2.2). Paper placeholder: R2.2 (Paper 2, §3.4). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Data
- Fantasia: the 40 subjects of E2.1, beats from annotations.
- The 21 I-CARE pilot patients, using the first ECG segment of each (the pilot's rule), with R-peaks
  from the pilot's adaptive detector.
- **Reproduction check, fixed now:** the original gate is re-run on these segments first. Each
  patient's number of RR intervals must equal the `n_rr` recorded in
  `cbra_boundary_residual/result.json`. If it does not, the segment differs from the pilot's, and
  that is reported.

## Method (the plan's steps)
1. RR series indexed by beat, without interpolation.
2. An RR interval is removed as ectopic or artefactual if it differs by more than 20% from the median
   of the centred 5-beat window around it. Removed intervals are deleted, not replaced. No other
   cleaning is applied.
3. For each scale τ = 1…10, the coarse-grained series is the mean of non-overlapping blocks of τ
   beats. T is computed at lag 1 on it.
4. For each scale, 100 IAAFT surrogates of that coarse-grained series, and the z-score of T against
   them.
5. Subject summary: the mean of |z| over the 10 scales.
6. p: surrogate j gets the same summary, computing its z at each scale against the other 99. p is
   the fraction of the 100 surrogates whose summary is at least the real one, as the plan states;
   (count + 1)/101 is reported too.

**Structured if p < 0.05.** Bar: 0.60 per group.

## Also run (secondary, on the same 21 I-CARE segments)
The gate as described in the paper (4 Hz interpolation), for comparison with E2.1's secondary arm.

## Reported
The fraction in each group (Fantasia young, Fantasia elderly, I-CARE), and how many of the 6
originally structured I-CARE patients remain structured after cleaning.
