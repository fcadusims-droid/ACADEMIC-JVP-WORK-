# Value-Base Discontinuity Probe — Resolving E2's Open Strong-Recession Regime (Paper 1)

**Follow-up to Experiment E2** (`high_dim_trichotomy`). E2 left one regime
genuinely open. In the 8/12 strongest-recession cells the apparent largest
Lyapunov exponent *grows* as the fixed integration step shrinks
(recession=2, diversity=0 probe: λ = 121 → 217 → 528 → 722 as dt = DT → DT/8, a
~6-fold rise), so it is **not** a genuine finite exponent. E2 could not decide
between two readings, and its pre-registration's "λ ~ 1/dt ⇒ artifact" rule meant
it could not, by construction, return a falsifier from this regime:

- **(a) Numerical/coordinate artifact.** The divergence is an integration
  artifact of a *non-smooth vector field* that a fixed-step integrator cannot
  resolve — in which case the true finite-time Lyapunov exponent is finite and
  the cell lands in the trichotomy after all (Sec 7.5/7.6 holds even here).
- **(b) Genuine quasi-discontinuous value-base mutation.** The chase dynamics
  themselves generate a genuine near-discontinuity — the abrupt value-base
  reconfiguration Paper 1 associates with metanoia — for which the smooth-flow
  Poincaré-recurrence premise of the trichotomy does not straightforwardly
  apply, and which could constitute a genuine escape route.

The decisive cell (recession=2, diversity=0) is also the only cell with low
recurrence (0.344 < 0.5), so whether it is a **falsifier** of the trichotomy
turns entirely on reading (a) vs (b).

## The mathematical fact this probe rests on

For a **Lipschitz-continuous** vector field on a compact set, the finite-time
largest Lyapunov exponent is finite and well-defined, and any convergent
integrator's estimate **must** converge to it as the local truncation error → 0
(for RK4, as dt → 0; equivalently, as an adaptive solver's tolerance → 0).
Non-convergence as the error → 0 is therefore a signature of **genuine
non-smoothness** (a non-Lipschitz field), not of a finite chaotic exponent.

So the question "(a) artifact vs (b) genuine discontinuity" is exactly the
question **"is the E2 vector field genuinely non-Lipschitz, and if so, is the
non-smoothness intrinsic to the value dynamics or an incidental coordinate
artifact?"**

## The suspected source of non-smoothness (to be tested, not assumed)

E2's forces use `torus_disp` — the **minimal-image** displacement
`((a-b+0.5) % 1) - 0.5`. This is **C0-discontinuous on the torus cut locus**
(each coordinate's displacement flips sign at half-period), a jump of order
`w · 1 / σ²` in the force (up to ≈0.6 per bump per crossing at the reported
weights). This discontinuity is imposed by the *minimal-image coordinate
convention*, **not** by the value dynamics: it is a seam in the chart, not an
abrupt reordering of the objective. If it is the source of the divergence, the
divergence is reading (a) — and specifically a coordinate artifact, not metanoia.

## Method — a smoothness decomposition

The same d=6, M=8-agent, K=8-bump population-based value-base-mutating dynamics
as E2, integrated three ways to separate the sources of the divergence:

1. **Minimal-image field, dt-refinement** (reproduce/extend E2): compute the
   Benettin λ at dt = DT/2, DT/4, DT/8, DT/16 with RK4. Expected: does not
   converge (confirms the field, as coordinatised, is non-smooth).
2. **Smooth-periodic field, dt-refinement** (the control): replace the
   minimal-image Gaussian kernel with a genuinely **C∞ periodic** kernel — a
   von-Mises / wrapped-Gaussian form
   `w = exp((Σ_j cos 2π(b_j−θ_j) − d) / (4π²σ²))`, whose gradient is
   `Σ w · sin 2π(b−θ)/(2πσ²)` — which agrees with the minimal-image Gaussian to
   O(Δ²) for small displacements but is differentiable everywhere on the torus
   (no cut locus). Compute the Benettin λ at the same dt ladder. A C∞ field on a
   compact torus **is** Lipschitz, so λ **must** converge; the empirical question
   is only its **sign** and the accompanying **recurrence**.
3. **Adaptive error-controlled confirmation** on the decisive cell
   (recession=2, diversity=0): compute λ with `scipy.integrate.solve_ivp`
   (DOP853, adaptive) over a tolerance sweep rtol ∈ {1e-6, 1e-9, 1e-12} for both
   fields, to confirm the smooth-field limit is a genuine error→0 limit and not a
   fixed-step-family coincidence.

Supporting diagnostics:

- **Local-Lipschitz probe**: along a trajectory in the worst cell, estimate the
  empirical local Lipschitz constant `‖f(x+δ)−f(x)‖/‖δ‖` of each field. The
  minimal-image field should show large jumps at cut-locus crossings; the smooth
  field should be bounded.
- **Recurrence on the smooth field**: recompute the Poincaré recurrence fraction
  of the stochastic dynamics with the smooth kernel for the divergent cells
  (especially recession=2, diversity=0), since the low 0.344 recurrence must also
  be checked to be free of the minimal-image seam before it can support a
  falsifier.

## Pre-registered decision rule (written before the run)

Let λ\* be the smooth-field, dt-converged (and adaptive-confirmed) largest
Lyapunov exponent for the strong-recession cells, and R\* the smooth-field
recurrence fraction.

- **Outcome A — ARTIFACT / trichotomy holds.** If the smooth field's λ\*
  **converges** (flat under dt-refinement and matching the adaptive limit) and is
  **≤ 0**, *or* is **> 0 with R\* ≥ 0.5**, then the E2 divergence was a
  non-smoothness of the *minimal-image coordinate seam* plus fixed-step
  integration — reading (a). Every cell then lands in the trichotomy, and
  Sec 7.5/7.6 is strengthened, with the E2 open regime **closed in favour of the
  theorem**.
- **Outcome B — FALSIFIER / genuine escape route.** If the smooth field's λ\*
  **converges to a genuine positive value AND R\* < 0.5** (positive entropy with
  no recurrence on a compact set), the trichotomy is **falsified by its own
  hardest named case**, and Sec 7.5/7.6 must be rewritten. This is to be reported
  as prominently as a confirmation. Alternatively, if even the **C∞** field's λ
  provably fails to converge (which for a Lipschitz field should not happen, and
  would require ruling out a bug), the strong-recession regime hosts a genuine
  intrinsic non-smoothness — a legitimate quasi-discontinuous value-base mutation
  — which is likewise reading (b) and must be reported as a genuine open escape
  route, not an artifact.
- **Outcome C — STILL UNRESOLVED.** If the results are mixed (e.g. the smooth
  field converges for some divergent cells but the decisive low-recurrence cell
  remains ambiguous), report the regime as still open but **narrowed**, naming
  exactly which cell(s) resist resolution.

The verdict is issued strictly against this rule. Because the smooth-periodic
kernel is not a tuning knob but a *removal of an incidental coordinate seam* (it
is arguably a more faithful model of the same PBT value dynamics than the
minimal-image one), replacing the field is a legitimate resolution of the open
question, not a search for a desired conclusion. Whatever sign λ\* takes on the
smooth field is reported as the answer.

## Stopping rule

One run: the 8 divergent cells on both fields at the dt ladder above, the
adaptive-tolerance confirmation on the decisive cell, the local-Lipschitz probe,
and smooth-field recurrence on the divergent cells. Budget: a single
implementation, target < 15 minutes runtime. Whatever the decision rule returns
is the verdict; no re-tuning of kernel width, recession grid, or thresholds after
seeing results.

## Status
Pre-registered. Not yet run.
