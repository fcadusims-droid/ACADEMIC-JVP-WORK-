# §12 residual tests — executability and specificity exercise (Paper 2)

**Written before the run.** A coverage audit found two of Paper 2 §12's three residual tests
**unexercised**: `idempotent_rotation_stat` (Test Two) is defined in `shared_lib` and never
called by any experiment, and the **multivariate** IAAFT of Test Three is only reimplemented
locally in a univariate form inside `cbra_boundary_residual`. The reviewer's rule was "run it or
remove it from the abstract; what is not legitimate is selling in the abstract what never ran."
This runs it, in the repository's own *syntactic-consistency* register (§15.1): the goal is to
show the instruments are executable and behave as §12 claims on data of known character — not to
make any biological claim.

## What is tested
- **Test Two (idempotent covariance rotation, §12.2 / §15.4 specificity).** The statistic must
  *fire* on a genuine orthogonal rotation of the covariance eigenframe and stay *silent* on the
  two nulls §12.2 names as things a stochastic surge produces: a heavy-tailed amplitude excursion
  with an unchanged eigenframe, and a pure eigenvalue rescaling. This is Test Two's specificity,
  which §15.4 exists to establish and which no experiment had checked.
- **Test Three (multivariate IAAFT, §12.3).** Multivariate IAAFT surrogates must (a) preserve the
  series' linear structure (auto- and cross-spectrum) — the self-test below — and (b) give a
  discriminating nonlinear statistic that lies *inside* the 99.9% surrogate band on a linear
  multivariate process (false-positive control) and *outside* it on a nonlinear one (power).
- **The declared honest limit (§12.3, §15.4).** The exercise must also reproduce the paper's own
  concession: a low-dimensional deterministic chaotic generator (Lorenz) **rejects** the IAAFT
  null. Passing Test Three means "not linear noise" and nothing more; a nonlinear-but-non-boundary
  system passes. Demonstrating this is part of the pre-registered success, not a failure.

## Pre-registered criteria (fixed now)
- **Test Two PASS:** rotation statistic ≥ **0.30 rad** for the genuine eigenframe rotation, and
  ≤ **0.10 rad** for *both* the heavy-tailed surge and the pure rescaling. (A stochastic surge
  leaves the eigenframe invariant, so its angle must be near zero.)
- **Test Three PASS:** using a one-sided rank surrogate test at level α = 0.05 (nonlinear
  determinism gives the real series a lower nonlinear-prediction error than its linear
  surrogates), the linear-VAR false-positive rate is ≤ **0.10** (nominal-ish at α = 0.05); the
  nonlinear positive control rejects the linear-noise null in ≥ **95%** of repeats; and the
  Lorenz series also rejects (the honest limit, reproduced not hidden).
- **FAIL** in either direction is reported as such: a statistic that cannot discriminate the cases
  §12 says it discriminates would mean the §12 text overstates the instruments, and the honest
  consequence is to weaken §12 or remove the untested claim from the abstract.

## Self-test gating the run
Multivariate IAAFT must actually preserve the cross-spectrum, or Test Three is meaningless. Before
any result is read, the surrogate ensemble's mean cross-correlation between channels must match the
real series' within **0.05**. If it does not, the surrogate generator is broken and the run aborts
— an instrument failure, not evidence about the tests.

## Instrument-failure addendum (recorded before a valid result was read)
The first execution produced no trustworthy Test Three number: the "linear" VAR was not forced
stationary (occasional spectral radius > 1 gave it growth, so it was not a clean linear null and
over-rejected at 23%), the nonlinear generator was a static `lin²` transform that **overflowed**,
and a 99.9% band cannot be estimated from ~50 surrogates. These are instrument defects, fixed
before any valid result was read: the VAR is now rescaled to spectral radius 0.85; the nonlinear
positive control is a **coupled Hénon map** (nonlinear dynamics, bounded — the canonical
surrogate-test positive control, since a static transform is largely undone by IAAFT's amplitude
match); and the 99.9% band is replaced by a one-sided **rank test at α = 0.05** with 99 surrogates
per repeat, which is estimable. The genuine-rotation case in Test Two was also mis-constructed — a
random-plane frame rotation moved the leading eigenvector by only 0.24 rad, under the 0.30 fire
bar; it now rotates the principal axis by a known 0.6 rad. The **bars themselves were not moved**;
what changed are the generators and the surrogate-test construction, so that the bars are scored
against valid instruments.

## Attempt budget
**One valid run, no tuning loop.** Generators, statistics and the bars above are fixed here. An
instrument defect is fixed on the instrument and recorded (above); the thresholds are not moved.

## Status
Pre-registered. Not yet run.
