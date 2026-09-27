# Recurrence time against dimension (E1.2)

**Written and committed before the run, on 27 September 2026.** Plan: `EXPERIMENTOS_2026-09-27.md`
(E1.2). Paper placeholder: R-A2 (Paper 1, Appendix A.2). The criterion below is the plan's, unchanged; choices the plan
leaves open are fixed here, before any data are analysed. Any later change is recorded as a deviation,
with its reason, before its result is read.

**Deviation from E0, recorded now.** The plan asks for a GitHub release archived on Zenodo, or an OSF
registration, before any run. Neither can be made from this environment. The only evidence of order is
the GitHub push of this file and pull request #56, both before the run. That is weaker than an
external DOI, as the papers themselves note about author-controlled repositories.

## Model (the plan's)
- Rotation of the torus, θ ↦ θ + α (mod 1), with α_i the fractional part of √p_i for the primes 2,
  3, 5, 7 and 11. Dimension d = 1…5 uses the first d of them.
- Return set A: the box of side 0.1 centred at (0.5, …, 0.5), so μ(A) = 10⁻ᵈ.
- 200 initial points drawn uniformly in A (seed 0). For each, the number of steps n ≥ 1 until the
  first return to A, with a limit of 10⁷ steps.

## Criterion (the plan's)
- In each d, the mean return time is within ±15% of 10ᵈ.
- The least-squares slope of log₁₀(mean) against d is between 0.9 and 1.1.

## Reported
The mean and standard deviation for each d, and the slope. Points that hit the step limit are
counted and reported.
