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

## Pending
B, C (Paper 3), F, E (Paper 1), H, I, J (Paper 2) — pre-registered, not yet run.
See `../STATUS.md`.
