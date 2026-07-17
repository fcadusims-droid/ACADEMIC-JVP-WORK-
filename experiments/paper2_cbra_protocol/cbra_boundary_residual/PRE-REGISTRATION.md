# Trilha B1 — Is the CBRA Boundary Residual Estimable on I-CARE? (Paper 2)

**The first, gating step of Trilha B.** Before any dissociation (B3) or
sub-criticality control (B2), the architecture requires that a *structured boundary
residual* ε^b even exists in the data: an interoceptive (cardiac) observable that,
after an operational null removes its linearly-predictable part, carries structure
a linear-Gaussian process does not (Paper 2 §12.3, the IAAFT-surrogate
qualification). If the residual does not survive that null here, **Trilha B stops** —
there is nothing to dissociate, and that is a publishable negative, not a step to
work around.

## Two parts

### Part A — ECG-coverage gate (Fase 0's B1 empirical gate) — ALREADY RUN
Confirm the concurrent cardiac+neural substrate exists at usable scale. Result
(recorded in `result.json`): of 60 sampled I-CARE patients, **45 (75%) have both
ECG and EEG** segments, many with 100–250 hourly segments. The gate PASSES: a large
concurrent ECG+EEG subset exists. (I-CARE stores ECG and EEG as separate
`*_ECG.mat` / `*_EEG.mat` files per hourly segment; ECG is 1-channel 500 Hz, ~3 MB.)

### Part B — Boundary-residual structure test (pre-registered here, before running)
For each of a pilot set of patients with ECG:
1. **Boundary observable.** Detect R-peaks in the ECG and form the interoceptive
   boundary series — the instantaneous heart-period (RR-interval) series,
   evenly resampled — the cardio-interoceptive receptivity-boundary proxy of Path C.
2. **Operational null.** Fit a linear autoregressive model (the linearly-predictable
   part) as the minimal operational null; the boundary *residual* is what a linear
   model does not capture, but the surrogate test below tests the observable's own
   nonlinear structure directly, which is the cleaner and more standard
   qualification.
3. **Structure test (IAAFT).** Generate IAAFT surrogates (which preserve the linear
   autocorrelation/power spectrum and the amplitude distribution but destroy
   nonlinear/phase structure) and compare a **nonlinearity statistic** — the
   **time-reversal asymmetry** of the boundary series (zero for a linear-Gaussian
   process; not preserved by IAAFT) — of the real series against the surrogate
   distribution. The boundary is *structured* for that patient if the real statistic
   lies outside the surrogate distribution at p < 0.05 (two-sided).

## Pre-registered decision rule (fixed before running Part B)
Let f be the fraction of pilot patients whose boundary series shows significant
nonlinear structure vs IAAFT.

- **B1 PASSES (residual estimable) → proceed to B2** if **f ≥ 0.60** (a clear
  majority of patients carry boundary structure a linear-Gaussian null does not
  reproduce). The boundary residual is estimable, so the dissociation has something
  to test.
- **B1 FAILS (residual not structured) → Trilha B STOPS** if f < 0.60. Reported as
  a publishable negative: "on I-CARE ECG the interoceptive boundary carries no
  structure beyond a linear-Gaussian null in the majority of patients, so the CBRA
  boundary residual is not estimable and the dissociation is not executable" — an
  added data-availability/estimability condition on §14.1, not a contortion.
- The 0.60 bar is set as a clear majority; it is not tuned after seeing results, and
  f is reported exactly with the per-patient p-values.

## Scope honesty (stated now)
This is the *gating* B1 only. It establishes whether ε^b is estimable; it does
**not** run B2 (MR sub-criticality certification) or B3 (the matched I+/I−
dissociation, which additionally needs the EEG side and audited surface-dynamics
matching to sd ≤ 0.3σ across recovery vs non-recovery). Those are the larger,
signal-heavy remaining steps, licensed only if B1 passes here. Nothing in B1
establishes anything about identity, the soul, or personal continuity — at most that
an interoceptive boundary observable is structured, the weakest necessary
precondition of the whole architecture.

## Fixed choices
Pilot set: the first N patients from RECORDS that have ≥ 1 ECG segment that loads
and yields ≥ 200 usable R-peaks; N targeted at ~20 (bounded by download, ~3 MB per
ECG segment). R-peak detection: band-pass + robust peak-finding; RR series resampled
to 4 Hz. IAAFT: 200 surrogates, standard iterative amplitude-adjusted algorithm.
No tuning of the statistic, surrogate count, or the 0.60 bar after seeing results.
Raw per-patient statistic/p and the verdict go to
`_results/cbra_boundary_residual/result.json`; the prose claims no more than that.

## Status
Part A (ECG-coverage gate): run — PASS (45/60 = 75% have ECG+EEG). Part B (residual
structure): run — **B1 FAILS, Trilha B STOPS.** Only **6/21 (29%)** evaluable pilot
patients show significant interoceptive-boundary nonlinearity vs IAAFT (3/24 short
segments excluded), below the 60% bar. Honesty notes recorded in the verdict: the
initial fixed-threshold R-peak detector was inadequate and was replaced with an
adaptive Pan-Tompkins detector *before* reading the result — which made the negative
*stronger* (29% vs 42%), a defect fix not outcome tuning; and 3 of the 6 "structured"
cases have |T_rev| > 0.5, likely arrhythmia rather than interoceptive nonlinearity,
so 29% is if anything an over-count. Per the pre-registered rule, **B2 and B3 are NOT
run.** Combined with Fase 0 (I-CARE is the only public dataset with the I+/I−
contrast), the CBRA dissociation is effectively not executable on available public
data — an added §14.1 estimability condition. See
`_results/cbra_boundary_residual/result.json`.
