# Output tracking versus full-state tracking (E1.1)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E1.1). Paper placeholder: R-A1 (Paper 1, Appendix A.1). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Model (the plan's)
- dx = (−x + c·y + u)dt + σ dW_x ;  dy = (−y + c·x + v)dt + σ dW_y ;  σ = 1.
- Reference: r(t) = 0 for t < 1000, and 1 from t = 1000 (the new target).
- Output tracking: u = −k(x − r), v = 0. Full-state tracking: u = −k(x − r), v = −k·y.
- k ∈ {0, 0.5, 1, 2, 5, 10, 20, 50}; c ∈ {0, 0.3}.
- Euler–Maruyama, dt = 0.001, T = 2000.
- 10 seeds (0–9).

## Fixed now
- Initial state x = y = 0.
- Common random numbers: for a given seed, the same Wiener increments are used in every condition.
- Variances are taken over t ∈ [1200, 2000]: the second half, minus the first 200 time units after
  the step. Each run's own mean over that window is subtracted.
- The criteria are applied to the seed-mean variance; per-seed values are reported too.
- "Falls monotonically" means the seed mean decreases strictly across the eight values of k, checked
  for both values of c.

## Criterion (the plan's)
- **Full-state:** var(y) falls monotonically and is below 5% of σ²/2 at k = 50.
- **Output only:** var(y) stays within ±10% of σ²/2 at every k when c = 0, and is at least 90% of
  σ²/2 at k = 50 when c = 0.3.

## Reported
A table of var(y) and var(x − r) by k, c and condition.
