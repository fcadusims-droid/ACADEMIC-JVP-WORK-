# Does the §14.1 sub-criticality control actually recover M_diss's power? (Paper 2)

**Run after** Experiment I2 (`dissociation_confound`) showed a bare critical
generator with **zero identity mechanism** reproduces the dissociation signature
`D_bare_critical`, growing monotonically with the branching ratio σ and reaching
**73% of the identity-linked reference** (0.66 vs 0.90) at the cleanest,
most-critical cell (σ=0.967, read-out noise 0.1), while the sub-critical control
(σ=0.70) stays at 11% (0.10). I2's verdict added to §14.1 the condition that a
dissociation result is identity-diagnostic **only if the boundary process can be
shown to be measurably sub-critical**. That control was written into the paper but
never tested. This tests it.

## The exact question (pre-registered)
Conditioning on the sub-criticality control — distance-to-criticality *measured*
from a short, noisy recording and *required* above a threshold — does M_diss
recover diagnostic power against I2's pure critical generator, in the cells where
it previously reached 73% of the reference? The control has two coupled halves and
both are tested:

1. **Efficacy given σ (oracle).** If the true σ were known and the control
   accepted only systems with σ below a cut, how far does the residual confound
   (max/mean `D_bare_critical/D_ref` among accepted systems) fall? This bounds the
   best case the control *concept* can achieve.
2. **Executability (realistic).** σ is not known — it must be estimated from a
   short, noisy recording (the physiological regime the paper targets). Using a
   standard branching-ratio (Harris ratio-of-totals) estimator with subsampling on
   a bounded recording, form a bootstrap upper confidence bound on σ̂ and accept a
   system only if that bound certifies σ < cut. The decisive risk: near-critical
   confounded systems whose σ̂ fluctuates or is biased **low** get *false-certified*
   as safe, so the residual confound among accepted systems stays high — the
   control fails not in concept but because the secondary measurement lacks power.

Three arms are compared at the adversarial cell (read-out noise 0.1, where the
confound is largest): **no control** (accept all; reproduces I2's up-to-73%),
**oracle control** (accept true σ < cut), **realistic control** (accept only
bootstrap-certified σ < cut on a short recording). The gap between oracle and
realistic isolates whether any failure is the control *concept* or the
*measurement*.

## Fixed parameters (before the run)
- Confound signal `D_bare_critical(σ, noise)` and reference `D_ref`: reused
  verbatim from I2 (`run_bare_critical`, `run_identity_linked`), averaged over 8
  seeds. Population σ grid: 10 values evenly in [0.70, 0.97] (safe → near-critical).
- Control cut: **σ_cut = 0.90** (require certified margin 1−σ ≥ 0.10), 95th-
  percentile bootstrap upper bound (B=200), certify safe if that bound < σ_cut.
- Realistic recording budget (headline): **N_aval = 40** avalanches, **6** observed
  generations, seed population Poisson(10), subsampling **f = 0.5**. Also swept:
  N_aval ∈ {20, 40, 80, 160, 400} to quantify how much data the control needs.
- "Genuinely sub-critical" reference systems for the acceptance/discrimination
  check: true σ ≤ 0.80. "Confounded" systems: true σ ≥ 0.92.

## Pre-registered success / failure thresholds (which one counts as "works")
Primary metric = **residual confound** = mean `D_bare_critical/D_ref` among systems
the control certifies as sub-critical, at read-out noise 0.1, realistic budget.
No-control baseline reaches up to 73%.

- **CONTROL WORKS — §14.1 validated in practice** if the realistic control brings
  the residual confound to **≤ 30% of reference** *and* keeps a usable acceptance
  rate of genuinely sub-critical systems (**≥ 50%** at true σ ≤ 0.80). Both must
  hold: low residual confound AND the control is not "safe" merely by rejecting
  everything. Then the measured-sub-criticality control is executable and effective;
  the loop closes.
- **CONTROL FAILS / NOT EXECUTABLE — new, more serious limitation** if EITHER
  (a) the realistic residual confound stays **> 40% of reference** because the
  short-data σ̂ false-certifies confounded near-critical systems (quantified by the
  acceptance rate at true σ ≥ 0.92 being non-negligible), OR
  (b) reaching ≤ 30% residual confound forces the acceptance of genuinely
  sub-critical systems **< 20%** (safe only by being unusable), OR
  (c) at the realistic budget the estimator cannot separate σ=0.925 from σ=0.80 —
  certification power < 0.5 — so distance-to-criticality is not reliably measurable
  on short/noisy data. Then the control §14.1 promises is **not executable in
  practice**, and that must return to the text as an added honesty condition, not a
  solved problem.
- **PARTIAL / PRECONDITIONED** if the control reaches the "works" bar only at a
  data budget larger than the realistic headline (report the required N_aval as an
  explicit precondition), or lands in 30–40% residual confound.

The oracle arm is reported alongside so the diagnosis is unambiguous: oracle-works
+ realistic-fails ⇒ the limitation is *measurement* (scenario b of the brief);
oracle-fails ⇒ the control concept itself is too weak.

## Stopping rule
One run of the three-arm pipeline plus the budget sweep, on the fixed parameters
above. The verdict is issued against these thresholds; the source of truth is
`_results/subcriticality_control/result.json`. Given this closes a correction both
author and assistant already wrote into §14.1, the reading is held *strictly* to
the numbers — a residual confound of 45% is reported as a failure of the control,
not softened toward "mostly works".

## Status
Run. Verdict: **CONTROL WORKS — BUT ONLY WITH A SUBSAMPLING-ROBUST ESTIMATOR;
§14.1 must specify one.** The pre-registered "works" bar (≤30% residual confound
with ≥50% acceptance of genuinely sub-critical systems) is cleared on the
physiological observable *only* by a subsampling-robust estimator; the naive one
fails.

| arm | residual confound / ref | accept(safe σ≤0.80) | reject(confounded σ≥0.92) |
|---|---|---|---|
| no control (I2 baseline) | 38% mean / **70% worst** | — | — |
| oracle (true σ known) | 27% | — | — |
| clean separable avalanches (N=40, ratio est.) | **24%** | 100% | 100% |
| continuous subsampled + **naive** slope | **35%** ✗ | 100% | only 21% |
| continuous subsampled + **MR** estimator | **29%** ✓ | 90% | 83% |

The decisive detail (and the trap avoided): the naive lag-1 slope on a short
continuous subsampled stream is **attenuated toward zero** (true σ=0.94 → σ̂=0.79),
the *dangerous* direction — it false-certifies 79% of confounded near-critical
systems as safe (the known subsampling bias, Wilting & Priesemann 2018). Had the
test stopped at cleanly separated avalanches it would have read a clean, generous
"works". The subsampling-robust multistep-regression estimator removes the
attenuation (σ=0.94 → σ_MR=0.92) and **restores** the control — but only marginally
(29%, right at the bar; 83% of confounded rejected, not 100%).

**Honest close:** the §14.1 sub-criticality control is executable and recovers
M_diss's diagnostic power **provided distance-to-criticality is measured with a
subsampling-robust estimator (MR-type) or from cleanly segmented avalanches — not a
naive estimator, which fails.** That estimator requirement is the added condition
§14.1 must name; with it, the loop closes. Source of truth:
`_results/subcriticality_control/result.json`.
