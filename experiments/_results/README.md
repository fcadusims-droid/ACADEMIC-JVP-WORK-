# Results — Proof Record

This folder is the committed record of every experiment run: machine-readable
`result.json` metrics and the figures, one subfolder per experiment. Verdicts are
issued against each experiment's `PRE-REGISTRATION.md`, written before the run.
Nothing here is evidence about any real physical/biological/theological system —
it validates the papers' *methods and numeric claims*.

Regenerate any result with `python -m experiments.<paper>.<experiment>.run`.

---

## Experiment G — Poincaré recurrence of the Lorenz attractor (Paper 1)
**Verdict: CONFIRMED (with an ε caveat the text should state).**

The text's "recurrence fraction ≈ 1" holds as literally computed for ε ≥ 0.05·span:

| ε / attractor span | 0.01 | 0.02 | 0.05 | 0.10 | 0.15 | 0.20 |
|---|---|---|---|---|---|---|
| recurrence fraction | 0.51 | 0.85 | 0.98 | 0.99 | 0.99 | 0.99 |

At very small ε (0.01·span) it drops to 0.51, so "≈ 1" is true above ε ≈ 0.05·span
and the paper should state that regime rather than leaving the claim unqualified.
Files: `poincare_recurrence_check/result.json`.

---

## Experiment D — Drift-vs-Jump confusion sweep (Paper 3)
**Verdict: CALIBRATIONAL for strong jumps, STRUCTURAL in one corner.**

Run on the faithful geometric pipeline (SPD(3) trajectories → exact square-root
Cartan anti-development → covariate-anchored jump test + Girsanov drift test).
Grid: drift strength × collapse severity, 60 seeds/cell, thresholds calibrated
per metric to a 5 % FPR on pure diffusion.

**AUC(collapse vs drift)** — 0.5 = structural overlap, 1 = separable
(rows = drift strength, cols = collapse factor; smaller factor = stronger jump):

| drift ↓ / collapse → | 0.9 | 0.7 | 0.5 | 0.3 | 0.1 |
|---|---|---|---|---|---|
| 0.00 | 0.52 | 0.91 | 0.99 | 1.00 | 1.00 |
| 0.05 | —    | 0.85 | 0.98 | 1.00 | 1.00 |
| 0.10 | —    | 0.69 | 0.92 | 0.98 | 1.00 |
| 0.20 | —    | 0.70 | 0.80 | 0.94 | 1.00 |
| 0.30 | —    | 0.74 | 0.83 | 0.92 | 0.98 |
| 0.40 | —    | **0.67** | 0.74 | 0.85 | 0.96 |

(The collapse = 0.9 column is not a detectable jump — sqrt jump power there is only
0.07 — so its AUC is meaningless and greyed out.)

**Findings**
1. **Strong jumps (collapse ≤ 0.3) stay separable from drift (AUC ≥ 0.85) at every
   drift strength** → the confusion there is a *threshold placement*: raising the
   dispersion-calibrated threshold removes it without losing jump power.
2. **Weak-but-detectable jumps (collapse = 0.7) collapse into strong drift**
   (AUC → 0.67 at drift 0.4) → *structural*: no threshold separates a strong
   geodesic drift from a weak collapse there. A hybrid metric (a method change,
   not a tuning fix) is indicated for that corner.
3. **Longer windows make it worse:** AUC at (drift 0.3, collapse 0.3) falls
   0.99 → 0.90 → 0.76 as T goes 200 → 400 → 800, because a longer path accumulates
   more holonomy drift and more chance of a jump-like anti-developed excursion.
4. **Metric tails reproduced:** pure-diffusion excess kurtosis is ≈ 0.4 under the
   square-root metric vs ≈ 11 under AIRM (appendix: ≈ 4.5 vs ≈ 20) — same
   direction and order of magnitude.
5. **Honest non-reproduction:** AIRM was *not* jump-blind here (jump power
   0.73–1.0), because a rank-*collapse* jump produces a diverging increment
   detectable under both metrics; the appendix's AIRM jump-blindness concerns
   jumps comparable to diffusion, not rank collapse. Reported, not hidden.
6. **Stable:** the headline drift→jump rate is 0.41 ± 0.03 across disjoint seed
   banks — a real effect, not seed noise.

**Consequence for the method (the pre-registration's decision):** the square-root
pipeline is sound for strong transitions; its residual drift/jump confusion is a
localized weak-jump corner, and the honest fix is a hybrid metric there rather
than abandoning the square-root commitment. Not a wholesale method change.

Files: `drift_jump_confusion_sweep/result.json`,
`drift_jump_confusion_sweep/confusion_surfaces.png`,
`drift_jump_confusion_sweep/window_dependence.png`.

---

## Experiment A — Multi-scale localization (Paper 3)
**Verdict: criterion met (2/15 → 15/15), but the operative fix is WINDOW SIZE, not the multiscale bank.**

PhysioNet is blocked by the environment network policy, so this ran in the
pre-registered synthetic-adversarial mode: a persistent structural seam embedded
in spontaneous fluctuations with sharp transient excursions larger than the seam.

| detector | hits (\|err\| ≤ 15) | median err |
|---|---|---|
| fragile short window (w=3) | 2/15 | 131 |
| single large window (w=120) | 15/15 | 0 |
| multiscale bank | 15/15 | 0 |

- The short-window baseline reproduces the appendix's failure mode (transient
  excursions beat the true seam → 2/15).
- Both a single large window and the multiscale bank fully recover (15/15) → in
  this synthetic setup the 5/15 failure is a **window-size artifact**, fixable by
  enlarging the analysis window; the multiscale aggregation adds no measured value
  over a single large window.
- Drift guardrail holds (peak prominence on true seams 16.3 vs 5.4 on no-seam
  drift records — the detector does not manufacture a seam where there is none).
- **Caveats:** symmetric windows = *offline* localization, not strictly
  causal/online; and real EEG may impose a precision cost on a large window that a
  multiscale bank could escape — untested without PhysioNet.

Files: `localization_multiscale/result.json`, `localization_multiscale/localization.png`.

---

## Experiment B — Covariate smoothing prior (Paper 3)
**Verdict: NO BENEFIT (mechanistic) — smoothing γ_t is the wrong prior for abrupt transitions.**

Sweep the causal smoothing bandwidth `h` of the predictability covariate before
the jump argmax, on heavy-tailed diffusion with sharp spontaneous excursions
(~ jump size) that fool the raw argmax.

| bandwidth h | 0 | 1 | 2 | 4 | 8 | 12 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|
| localization accuracy | **0.36** | 0.29 | 0.24 | 0.18 | 0.19 | 0.10 | 0.09 | 0.07 |

Smoothing **monotonically degrades** localization. Mechanism: an abrupt jump and a
sharp spontaneous excursion have the *same single-sample* covariate signature, so
smoothing cannot separate them — it blurs the jump's peak (~1/h) faster than it
suppresses transient spikes (~1/√h), lowering SNR. The discriminator that *does*
work is **persistence** (a jump changes the regime; an excursion does not), which
a window-mean statistic exploits (Exp A) and a covariate argmax cannot.

Together A + B say: for abrupt transitions among comparable spontaneous events,
pointwise/covariate localization is not rescuable by smoothing; only a
persistence-sensitive (window-mean) statistic localizes reliably — and the
operative knob there is window size.

Files: `localization_priors/result.json`, `localization_priors/smoothing_sweep.png`.

---

## Experiment C — Method vs paradigm (Paper 3)
**Verdict: METHOD ROBUST via PERSISTENCE (with one residual open problem).**

Sleep-EDF is also blocked by network policy, so this sweeps two axes synthetically:
transition/spontaneous-fluctuation *ratio* (paradigm strength) and fluctuation
*persistence* (transient → sustained bursts).

Localization hit rate (|err| ≤ 15), 15 subjects:

| ratio (transient) | 0.5 | 0.75 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|
| fragile (w=3) | 1 | 1 | 11 | 15 | 15 | 15 |
| large window (w=120) | 15 | 15 | 15 | 15 | 15 | 15 |

| burst duration @ ratio 1 | 1 | 10 | 30 | 60 | 100 |
|---|---|---|---|---|---|
| large window | 15 | 15 | 15 | 14 | 13 |

- The persistence-sensitive large window localizes robustly across **paradigm
  strength** (15/15 at every ratio, where the fragile detector fails at low ratio)
  **and** across **fluctuation persistence** (mild 15→13 only as bursts approach
  the window length, 100 vs 120).
- **Residual open problem:** a spontaneous structural burst *longer than the
  analysis window* looks permanent within it — the one regime a window mean can't
  resolve; it needs a permanence-to-record-end test.

### A + B + C synthesis (Paper 3 localization)
The appendix 5/15 failure is a **fragile-pointwise-detector artifact** in an
adversarial ratio regime. It is resolved by a **large, persistence-sensitive
window** — because a transition is a *persistent* regime change while spontaneous
excursions are *transient*. The multiscale bank (A) adds nothing over a single
large window; covariate smoothing (B) actively hurts. The honest fix for Paper 3
is: use a large window and state a scope bound for spontaneous bursts longer than
that window. **All synthetic (PhysioNet blocked); real-EEG confirmation outstanding.**

Files: `cross_dataset/result.json`, `cross_dataset/ratio_sweep.png`.

---

## Experiment F — Exogenous-horn cost curve (Paper 1, Sec 7.3)
**Verdict: CLAIM CONFIRMED — the finite-gain agency cost is graded and monotone.**

A double-well explorer (`dx = (x − x³)dt + σ dW`, intrinsic hopping between wells)
is tracked to `x_ref = 0` with proportional gain `k`, sweeping `k`.

| gain k | 0 | 0.5 | 1.0 | 2.0 | 5.0 | 12.0 |
|---|---|---|---|---|---|---|
| D_ag (stationary variance) | 0.85 | 0.44 | 0.24 | 0.099 | 0.031 | 0.012 |
| λ∥ (relaxation rate) | −0.09 | −0.23 | −0.51 | −1.28 | −4.06 | −11.5 |

Both curves are **monotone** and **graded**: `D_ag → 0` (approaching the
annihilation limit) and `λ∥ → −∞` smoothly as gain rises. The double-well
bifurcation at `k=1` is washed out by the exploratory noise, so there is no
discontinuity — Sec 7.3's "graded, monotone" finite-gain cost is numerically
vindicated (as opposed to the perfect-tracking limit, which is the annihilation).

Files: `tracking_cost_curve/result.json`, `tracking_cost_curve/cost_curve.png`.

---

## Experiment E — Trichotomy test (Paper 1, Sec 7.5/7.6)
**Verdict: TRICHOTOMY HOLDS — no falsifier; the Sec 7.5/7.6 defence survives its strongest candidates.**

Endogenous-preference dynamics implemented directly as flows on a compact space,
classified by largest Lyapunov exponent λ (entropy proxy), Poincaré recurrence R,
and the Helmholtz–Hodge gradient/rotational split.

| candidate | λ_max | recurrence | Hodge (grad/rot) | class |
|---|---|---|---|---|
| gradient | −39.4 | 0.998 | 1.00 / 0.00 | Case 1 (convergent) |
| hamiltonian | +0.05 | 1.000 | 0.00 / 1.00 | Case 3 (conservative) |
| curiosity | −19.7 | 1.000 | 1.00 / 0.00 | Case 1 (convergent) |
| novelty search | — | 1.000 | — | Case 3 (bounded recurrence) |
| Lorenz chaos | +0.88 | 0.995 | — | Case 3\* (chaotic but recurrent) |

The forbidden object — **positive entropy AND absence of recurrence on a compact
set** — appears in none of them. The strongest positive-entropy case (Lorenz,
λ=+0.88) is chaotic yet recurrent (0.995); **pure novelty search on the compact
torus is bounded-recurrent (1.00), not sustained-novel**. Sustained novelty
without return requires a *non-compact* value space — the escape (Case 2) horn —
exactly as the Meta-Optimization Collapse Theorem predicts. (2-D autonomous flows
are non-chaotic by Poincaré–Bendixson, reinforcing the bound; the Lorenz case
supplies the genuine positive-entropy test in 3-D.)

Files: `rl_agents_trichotomy/result.json`, `rl_agents_trichotomy/trichotomy.png`.

---

## Experiment H — Dissociation-test power (Paper 2, Sec 14.1)
**Verdict: MARGINAL feasibility — and matching is a VALIDITY issue, not just a power one.**

Power/validity of the `M_diss` interaction test, sweeping sample size × effect
size (SNR) × matching quality between the S^{I+} and S^{I−} conditions.

Minimum n per condition for 80% power:

| matching sd | SNR 0.3 | 0.5 | 0.8 | 1.2 |
|---|---|---|---|---|
| 0.0 (perfect) | — | 80 | 40 | 20 |
| 0.3 | — | — | 40 | 20 |
| 0.6 | — | — | 80 | 20 |

False-positive rate under H0 (no true dissociation), n=20:

| matching sd | 0.0 | 0.3 | 0.6 |
|---|---|---|---|
| FPR@H0 | 0.045 | **0.159** | **0.353** |

- **The headline is validity, not power:** imperfect matching between S^{I+} and
  S^{I−} inflates the false-positive rate 3–7× (0.05 → 0.16 → 0.35), *independent
  of sample size* — a confounded interaction contrast manufactures dissociations
  that aren't there. The test is only valid with tight matching (sd ≲ 0.3·σ).
- **Power:** even with tight matching, a moderate effect (SNR 0.8) needs n≈40 per
  condition; small effects (SNR ≤ 0.5) are out of reach at realistic sizes.
- **Consequence:** the design is executable but demands (i) tight, independently
  verified matching and (ii) large samples — a *practical* limitation the paper
  should state alongside the ethical one.

Files: `dissociation_power_analysis/result.json`, `dissociation_power_analysis/power_grids.png`.

---

## Pending
I, J (Paper 2) — pre-registered, not yet run. See `../STATUS.md`.
