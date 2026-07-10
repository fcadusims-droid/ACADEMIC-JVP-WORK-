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
**Verdict: CALIBRATIONAL for the strongest jump, STRUCTURAL over a weak-jump × strong-drift region.**

Run on the faithful geometric pipeline (SPD(3) trajectories → exact square-root
Cartan anti-development → covariate-anchored jump test + Girsanov drift test).
Grid: drift strength × collapse severity, 60 seeds/cell, thresholds calibrated
per metric to a 5 % FPR on pure diffusion.

**AUC(collapse vs drift)** — 0.5 = structural overlap, 1 = separable
(rows = drift strength, cols = collapse factor; smaller factor = stronger jump):

| drift ↓ / collapse → | 0.9 | 0.7 | 0.5 | 0.3 | 0.1 |
|---|---|---|---|---|---|
| 0.00 | 0.49 | 0.90 | 1.00 | 1.00 | 1.00 |
| 0.05 | —    | 0.82 | 1.00 | 0.99 | 1.00 |
| 0.10 | —    | 0.72 | 0.94 | 0.98 | 1.00 |
| 0.20 | —    | **0.61** | 0.78 | 0.92 | 0.99 |
| 0.30 | —    | 0.65 | 0.74 | 0.86 | 0.98 |
| 0.40 | —    | 0.64 | 0.72 | 0.78 | 0.93 |

(The collapse = 0.9 column is not a detectable jump — sqrt jump power there is only
0.13 — so its AUC is meaningless and greyed out.)

**Findings**
1. **Only the strongest jump (collapse = 0.1) stays cleanly separable from drift
   at every drift strength (AUC ≥ 0.93).** For the strong-but-not-extreme jump
   (collapse 0.3) separability is high at weak drift (≥ 0.98) but slips to 0.78 at
   the strongest drift (0.4) — so "raise the threshold" fixes the confusion only
   for the extreme-jump column, not uniformly.
2. **As the jump weakens, it collapses into drift — a structural *region*, not a
   single corner.** AUC falls monotonically as collapse → 0.7 and drift grows:
   0.78 (collapse 0.3, drift 0.4) → 0.72 (collapse 0.5, drift 0.4) → **0.61**
   (collapse 0.7, drift 0.2, the worst detectable cell). Across that
   weak-jump × moderate/strong-drift triangle no threshold separates a geodesic
   drift from a weak collapse. A hybrid metric (a method change, not a tuning fix)
   is indicated for that region.
3. **Longer windows make it worse:** AUC at (drift 0.3, collapse 0.3) falls
   0.99 → 0.90 → 0.76 as T goes 200 → 400 → 800, because a longer path accumulates
   more holonomy drift and more chance of a jump-like anti-developed excursion.
4. **Metric tails, honestly measured — the strong appendix contrast is NOT
   reproduced at these parameters:** the reproducible pure-diffusion excess
   kurtosis of the anti-developed increment norms is ≈ 0.0 (square-root) vs ≈ 0.4
   (AIRM) at the experiment's diffusion scale — both close to Gaussian, *not* the
   appendix's ≈ 4.5 vs ≈ 20 heavy-tail split. (An earlier draft of this note cited
   "≈ 0.4 vs ≈ 11" from an out-of-band probe run at a larger diffusion scale; that
   is not what this experiment's own parameters produce, and the number is now
   computed inside `run.py` and stored in `result.json`.) This is the *reason*
   for finding 5.
5. **Consistent honest non-reproduction:** AIRM was *not* jump-blind here (jump
   power 0.85–1.0 for detectable collapses) — precisely because, at this
   diffusion scale, its diffusion increments are only mildly heavy-tailed
   (finding 4), so a rank-collapse jump still stands out under AIRM. The
   appendix's AIRM jump-blindness assumes the strongly heavy-tailed regime, which
   this parameter setting does not enter. Reported, not hidden.
6. **Stable:** the headline drift→jump rate is 0.41 ± 0.03 across disjoint seed
   banks — a real effect, not seed noise.

*(Seed hygiene: the per-cell seed blocks were re-spaced during review — the
original 50-seed spacing with 60 seeds/cell made adjacent cells share 10 seeds;
after re-spacing to non-overlapping blocks the conclusion is unchanged, worst
detectable AUC 0.61 vs 0.67 before.)*

**Consequence for the method (the pre-registration's decision):** the square-root
pipeline is sound for strong transitions (the extreme-jump column separates
cleanly at all drift); its residual drift/jump confusion is a weak-jump ×
strong-drift *region*, and the honest fix is a hybrid metric there rather than
abandoning the square-root commitment. Not a wholesale method change.

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

## Experiment I — Criticality confound robustness (Paper 2, Sec 15.5)
**Verdict: CONFOUND ROBUST — Sec 15.5's concession stands; the defensible arm is eliminative.**

Separating statistic = the standardised x:c interaction coefficient (zero for an
additive latent process, nonzero for a multiplicative gate or a super-linear
critical response). Reference: gated signal D=1.22, additive null D=0.01.

Critical-generator D (susceptibility exponent p × read-out noise; p=1 is the
non-critical control):

| p \ noise | 0.1 | 0.5 | 1.0 |
|---|---|---|---|
| 1.0 (control) | 0.01 | 0.00 | 0.00 |
| 1.25 | 0.95 | 0.26 | 0.13 |
| 1.5 | 1.29 | 0.58 | 0.31 |
| 2.0 | 1.41 | 1.09 | 0.73 |
| 3.0 | 1.35 | 1.31 | 1.21 |

- A genuinely critical generator (p>1) reproduces the gating differential in
  **15/24 cells (62%)** — robustly at moderate/strong criticality (p≥1.5) across
  read-out noise and homeostatic feedback, with magnitude that **matches or
  exceeds** the gated signal as criticality grows.
- The non-critical control (p=1) gives D≈0, matching the additive null — the
  statistic itself is valid; it is criticality, not an artifact, that confounds.
- Only mild criticality (p≈1.25) under heavy read-out noise fails to reproduce it.

The gating test is thoroughly confounded by criticality, so CBRA's defensible
contribution is the **negative/eliminative arm**, not detection — corroborating
Sec 15.5 rather than rescuing the naive gating test.

Files: `criticality_sweep/result.json`, `criticality_sweep/criticality_grid.png`.

---

## Experiment J — Metabolic null resolution (Paper 2, Sec 7.2)
**Verdict: RESOLUTION THRESHOLD EXISTS and scales with diffusion length — the qualitative claim is now a number.**

Spectral energy-diffusion model: an active boundary injects structure at scale
ell; diffusion low-passes it over length L_D; an operational null at resolution h
absorbs all scales coarser than h. The surviving structured residual is measured
vs h.

| diffusion length L_D (·ell) | 0.05 | 0.08 | 0.12 | 0.18 | 0.25 |
|---|---|---|---|---|---|
| absorption threshold h\* (·ell) | 0.73 | 0.77 | 0.81 | 0.85 | 0.93 |

- The null absorbs the structured boundary residual **only when its resolution is
  finer than h\* ≈ 0.7–0.9 ell**; coarser than that, the residual survives.
- h\* **grows monotonically with the diffusion length** — a longer diffusion
  length smears the boundary signature to a coarser scale, so a coarser null
  already absorbs it. Sec 7.2's weak-vs-strong-null distinction is
  resolution-driven and quantified: **strong null := resolution < h\*(L_D)**.
- **Metabolism matters:** with metabolic maintenance the structured residual is
  **20× larger** (2.89 vs 0.14) than with the boundary spectrum collapsed toward
  the smooth background — exactly the role Sec 7.2 gives metabolic expenditure in
  keeping the memory kernel from collapsing.

Files: `metabolic_null_resolution/result.json`, `metabolic_null_resolution/null_resolution.png`.

---

## Experiment I2 — Does criticality confound the dissociation test? (Paper 2, Sec 14.1)
**Extends Experiment I**, closing a gap an independent review of this repo identified: I
tested whether criticality confounds the *gating* differential; it never tested
the *dissociation* test (`M_diss`) that Experiment H's power analysis assumed
was valid. This experiment builds a generator with **zero identity mechanism**
— a bare critical branching process where CONTINUE means the same lineage
carries across the transition and RESET means a fresh independent lineage
replaces it — and asks whether continuity alone (no identity information
anywhere) reproduces the preservation contrast `M_diss` treats as diagnostic of
identity-linkage.

**Verdict: GROWING CONFOUND NEAR TRUE CRITICALITY — nuanced, not a clean survival.**

| criticality σ (noise=0.1) | 0.70 | 0.81 | 0.87 | 0.93 | 0.97 |
|---|---|---|---|---|---|
| D_bare_critical | 0.10 | 0.30 | 0.41 | 0.53 | **0.66** |

Reference: `D_identity_linked = 0.90` (explicit identity mechanism),
`D_null = -0.02` (honest negative control), sub-critical control D ≤ 0.10.

- Only 3/12 critical cells cross the pre-registered 50%-of-reference threshold
  (25%), so this is **not** a clean "confounded like gating" result.
- But `D_bare_critical` rises **monotonically** with criticality and falling
  read-out noise, reaching **73% of the identity-linked reference** at the
  strongest, cleanest cell (σ=0.97, noise=0.1) — a system with *zero* identity
  mechanism gets within shouting distance of what an explicit identity channel
  produces, purely from continuity vs reset.
- This mirrors Experiment I's own pattern for the gating differential exactly:
  safe away from criticality, confounded near it.
- **Consequence for the paper:** `M_diss` is not diagnostic of identity per se
  near true criticality without an independent control showing the boundary
  process is measurably sub-critical — a requirement Sec 14.1 does not
  currently state. This is the same class of correction Sec 15.5 already gave
  the gating test, now shown to extend to the dissociation test as well.

Files: `dissociation_confound/result.json`, `dissociation_confound/dissociation_confound_grid.png`.

---

## Experiment AD — Window Tension & Causal-vs-Offline Localization (Paper 3)
**Reconciles Experiments A and D**, closing a second gap the review identified:
A's fix used a large **symmetric** (offline, future-using) window; D found
longer windows *worsen* drift/jump discrimination. Neither was tested on a
shared apparatus, and A's caveat ("offline, not the causal/online claim the
abstract makes") was never followed to its consequence.

**Verdict: CAUSAL CLAIM RECOVERABLE, AT AN EXPLICIT REPORTING-LAG COST.**

- A **naive** causal design (recent window vs. *all* unweighted past history)
  fails badly (best 8/15) — it never forgets the pre-seam regime, so the
  reference stays permanently contaminated after a transition. This is a
  detector-design pitfall, not proof causal detection is impossible.
- The **standard** causal design (two adjacent backward-looking windows) is
  mathematically *identical* to the symmetric statistic, shifted in time by
  exactly `w` samples (`S_causal[t] = S_symmetric[t−w]`, an exact identity). Once
  its estimate is corrected for that definitional reporting lag, it **matches
  the offline result exactly (15/15 at every guarded window)**.
- **The honest cost:** even the best causal design cannot report a transition
  until `w` samples after it happened. The smallest reliably-guarded window
  still pays a **10-sample (2% of the 600-sample record) reporting lag** — a
  real, quantified, previously unstated price of the "causal/online" claim.
- **The A/D tension did not reproduce here:** drift-only false-fire prominence
  *fell* with window size in this apparatus (6.3→2.0), the opposite of D's
  finding. This means A and D's window preferences are not in conflict on a
  shared statistic — they are two **different sub-problems** (break-curve
  localization vs. Girsanov-geometry drift/jump demarcation) with independent
  window dependencies, and Paper 3 can use different windows for each without
  contradiction, provided this is stated explicitly rather than left as an
  unresolved tension.

Files: `causal_vs_offline_localization/result.json`, `causal_vs_offline_localization/causal_vs_offline.png`.

---

## Experiment E2 — High-Dimensional, Value-Base-Mutating Trichotomy Test (Paper 1)
**Extends Experiment E** to close the third gap the review identified: E's
candidates were all low-dimensional (2-D torus / 3-D Lorenz); the text's own
hardest named objection is *open-ended, novelty-driven, value-base-mutating
optimization* in a genuinely higher-dimensional, population setting. This builds
that candidate directly: `M=8` agents on a `d=6` compact torus, climbing a
reward landscape whose bumps **recede from wherever the population concentrates**
— the objective mutates in response to the population's own trajectory.

**Verdict: TRICHOTOMY SURVIVES ITS HARDEST NAMED CASE — and the stiff-integrator follow-up turns the previously-"unresolved" cells from *excluded* into *conclusively diagnosed*.**

The first E2 run (fixed-step Euler on a hard force cap) found an apparent falsifier
at strong recession whose Lyapunov estimate **kept growing as the step shrank** and
had to be **excluded as numerically unresolved** (7/12 cells) — honest, but it left
the most adversarial regime genuinely untested.

**Path-2 follow-up (this run):** the integrator was rebuilt — smooth (tanh) force
saturation instead of a C0 clip, RK4 instead of Euler, vectorised, with cells
**classified by their resolution scaling** at `dt = DT, DT/2, DT/4` (an adaptive
stiff LSODA solver was tried first but was too slow to sweep). The result is
stronger than mere exclusion:

- **4/12 cells converge** to a genuine, resolution-stable Lyapunov exponent — all
  Case-1 convergent (λ ≈ −5 to −23) with high recurrence (≥ 0.94). No falsifier.
- **8/12 strong-recession cells are resolution-divergent**: their apparent positive
  exponent **grows as the step shrinks**. A dedicated scaling probe at recession 2
  is the smoking gun — λ = **121 → 217 → 528 → 722** as `dt = DT → DT/8`, i.e.
  **λ·dt roughly constant**. That 1/dt scaling is the definitive signature of a
  **numerical artifact** (trajectories separating by a fixed factor *per step* — a
  near-discontinuous flow direction when a fleeing bump passes through an agent —
  not per unit time). A genuine Lyapunov exponent converges; a 1/dt-diverging one
  **does not exist**, so these cells have no genuine positive exponent and are
  **not falsifiers**.
- **The crux:** the one low-recurrence cell that *could* have been a falsifier
  (recession 2, diversity 0, recurrence 0.34) is exactly one of these
  resolution-divergent artifacts — its "positive λ" is not genuine.

So on the hardest named case, **no cell is a genuine falsifier**, and the
strong-recession regime that the first run left open is now conclusively a
numerical artifact rather than an untested falsifier candidate — the stiff-
integrator investigation **strengthens** the Sec 7.5/7.6 defence. (A small residual
honesty: `λ·dt` is only *roughly* constant — λ grows ~6× while dt shrinks 8× — so
the scaling is near-1/dt, not textbook-exact; either way it diverges rather than
converges, which is all the argument needs.)

Files: `high_dim_trichotomy/result.json`, `high_dim_trichotomy/high_dim_trichotomy.png`.

---

## Real-EEG localization — the outstanding A/B/C confirmation (Paper 3)
**Verdict: SPLIT, exactly as the appendix found — structural discrimination validated on real EEG, on-line localization still open.**

PhysioNet became reachable, so the A/B/C detectors were run on the appendix's real
paradigm: PhysioNet `eegbci`, 15 subjects, eyes-open (run 1) vs eyes-closed
(run 2), occipito-parietal channels, alpha 8–13 Hz.

| detector | localization hits (\|err\| ≤ 2 s) | median err |
|---|---|---|
| fragile pointwise (w=2) | 2/15 | ~14 s |
| **large window (w=40, ~10 s)** | **4/15** | ~9 s |
| multiscale bank | 4/15 | ~9 s |

- **Between-record structural discrimination replicates:** the eyes-open/eyes-closed
  geodesic distance exceeds within-state distance in **12/15** subjects (median
  ratio 1.7) — the trace-normalised geometry sees the alpha structural change, as
  the appendix's 20/20 claimed (weaker here only because of a harsher within-state
  estimate and a smaller channel set).
- **Within-trajectory localization stays hard on real EEG**, even for the large
  window (4/15 vs fragile 2/15). The large window *does* beat the fragile detector
  — confirming the **direction** of the synthetic A/B/C mechanism (persistence
  helps) — but does not solve it, because **real spontaneous alpha bursts are
  sustained**, i.e. exactly the sustained-fluctuation regime Exp C flagged as the
  detector's residual limitation (a burst longer than the window looks permanent
  within it). Multiscale adds nothing over the single large window, as A found.

This is the honest real-data status: **structural discrimination validated; the
5/15 within-trajectory localization is confirmed as a genuine open problem, not a
synthetic artifact**, and its cause is the one Exp C predicted. (EEG is not
committed; `experiments/**/data/` is git-ignored — MNE re-downloads it.)

Files: `real_eeg_localization/result.json`, `real_eeg_localization/real_eeg_localization.png`,
`real_eeg_localization/PRE-REGISTRATION.md`.

---

## Hybrid drift-robust jump statistic — the Exp D corner fix attempt (Paper 3)
**Verdict: NO HELP — the corner is a genuine geometric limit, not a filterable contamination.**

Exp D flagged its structural corner (weak jump × strong drift) as needing a
"hybrid metric". This tests the obvious one: on the same square-root geometry
(so jump power is preserved), high-pass filter the anti-developed increments —
subtract a local moving average — on the hypothesis that a jump is high-frequency
(single step) while the confusing drift/holonomy term is a slow low-frequency
trend.

Worst weak-jump × strong-drift AUC(collapse vs drift):

| statistic | worst corner AUC | strong-jump power |
|---|---|---|
| square-root (Exp D) | 0.65 | 1.00 |
| hybrid (high-pass) | **0.61** | 1.00 |

The high-pass does **not** recover the corner (it is marginally worse), though it
preserves jump power — so the drift contamination is **not** a slow trend: it is
high-frequency (single-step holonomy spikes indistinguishable from a jump). This
is why it survives high-passing, and why the appendix's λ_min-persistence
discriminator also failed. **The corner is a genuine geometric limit of the
square-root anti-development, requiring a true base-metric change (e.g. along-path
transport, or a different base metric), not a filtered statistic.** The result is
negative but informative: it rules out two classes of cheap statistical fix and
confirms Exp D's "structural, not calibrational" diagnosis of that region.

Files: `hybrid_metric/result.json`, `hybrid_metric/hybrid_metric.png`,
`hybrid_metric/PRE-REGISTRATION.md`.

---

## All fifteen experiments complete

| # | Paper | Headline |
|---|---|---|
| G | 1 | Lorenz recurrence ≈1 confirmed (ε ≥ 0.05·span) |
| D | 3 | Drift/jump confusion is calibrational except a weak-jump×strong-drift corner (structural) |
| A | 3 | Localization fix is window **size**, not the multiscale bank |
| B | 3 | Covariate smoothing is the wrong prior for abrupt jumps (degrades localization) |
| C | 3 | Localization solved by **persistence** (large window); robust across paradigm & burst duration |
| F | 1 | Finite-gain agency cost is graded & monotone — Sec 7.3 confirmed |
| E | 1 | **Trichotomy holds** — no positive-entropy-without-recurrence falsifier on a compact set |
| H | 2 | Dissociation test is matching-limited (validity, not just power) |
| I | 2 | Criticality confound is **robust** — Sec 15.5 stands, eliminative arm only |
| J | 2 | Metabolic null has a resolution threshold h\*≈0.7–0.9 ell scaling with L_D |
| **I2** | 2 | Extends I to `M_diss`: **growing confound near true criticality** (73% of identity-linked signal at the cleanest cell) |
| **AD** | 3 | Reconciles A/D: causal localization **recoverable at a quantified reporting-lag cost**; A/D's "tension" doesn't reproduce on a shared apparatus |
| **E2** | 1 | Extends E to a d=6 population, value-base-mutating agent: trichotomy **survives**; the strong-recession "falsifier" is **conclusively diagnosed as a 1/dt numerical artifact** (λ=121→217→528→722 as dt→DT/8) by a rebuilt stiff/RK4 integrator — no genuine falsifier |
| **Real-EEG** | 3 | A/B/C on real PhysioNet EEG: structural discrimination **replicates (12/15)**; within-trajectory localization **still hard (large 4/15 vs fragile 2/15)** — the 5/15 open problem is confirmed real, caused by sustained alpha (Exp C's predicted limitation) |
| **Hybrid** | 3 | Attempted drift-robust hybrid for the Exp D corner: high-pass filtering **does NOT help** (AUC 0.65→0.61, power preserved) — the corner is a genuine geometric limit needing a real base-metric change, not a filtered statistic |

**Cross-cutting honesty:** four real bugs were found and fixed en route — two in
`shared_lib` (HAC drift-test calibration; a future-leakage bug in the
predictability covariate) and two in the extension experiments (a degenerate
CONTINUE/RESET design in I2, fixed via cross-trial level correlation; a
mathematically-exact reporting-lag identity in AD, and a numerically-divergent
Lyapunov estimate in E2, caught by an explicit dt-convergence gate rather than
reported as a falsifier). Paper 3's synthetic-adversarial experiments (A/B/C) were
run while PhysioNet was unreachable; it later became reachable and the **real-EEG
confirmation is now done** (above): structural discrimination replicates (12/15)
and the 5/15 within-trajectory localization limitation is confirmed as real, with
the cause Exp C predicted. A fifth data-hygiene issue was fixed during a rigorous
review (an out-of-band, non-reproducible kurtosis figure in D, replaced by a
diagnostic computed inside `run.py`). Every verdict was issued against a
pre-registration written before the run.
