# Fibre ablation — does the bundle apparatus earn its place? (Paper 3)

## Why this experiment exists
An external review observed that **no committed result isolates the contribution of the
fibre**. A direct audit of the codebase confirms something stronger:

- `stats_utils.t_eff_product` — the only cross-scale-coupling helper in the shared library —
  is **never called** by any experiment (it appears only in its own definition and `__all__`).
- No experiment constructs a bundle point. `manifold_trajectory` carries SPD base operations
  only; there is no Sasaki metric, no Ehresmann connection, no coupling matrix.
- Every validated result to date — trace normalization, the window-size finding, the
  detection-statistic repair, the base-metric corner result — is a property of the
  **trace-normalized SPD base alone**.

So the fibre (§3.2), the Sasaki-type metric and the Ehresmann connection (§3.3) — roughly half
the paper's construction — are not merely un-isolated but **unexercised**. The conclusion that
gap licenses is uncomfortable and must be tested rather than argued away: on what is measured,
Paper 3 may be a paper about trace-normalized SPD covariance with long causal windows. That is
a legitimate paper, but it is not the one written, and it is much shorter.

## Question
Does adding the fibre — the normalized cross-scale coupling carried in the Sasaki-type metric —
**materially improve** demarcation over the trace-normalized SPD base alone, on real data?

## Construction (Paper 3's own spec, not a strawman)
- **Base** (§3.1): trace-normalized SPD covariance of the slow band, embedded as `2·sqrt(rho)`;
  geodesic distance on the sphere, exactly as every committed experiment computes it.
- **Fibre** (§3.2): the phase–amplitude coupling matrix, phase of the slow carrier modulating
  the high-frequency envelope, `C_xs[i,j] = <exp(i·phi_L^(i)) · E_H^(j)>`, normalized as the
  paper specifies — divided by the **geometric** mean of the two block traces,
  `C~ = C_xs / sqrt(Tr(P_fL)·Tr(P_EfH))`, which is what makes it invariant under independent
  rescaling of the two bands.
- **Sasaki-type metric** (§3.3): `||M||^2 = ||M_base||^2 + ||∇_b C~||^2`. The connection is the
  paper's canonical choice (parallel transport on the base). *Implementation note, declared in
  advance:* between consecutive windows the covariant difference is taken as the plain
  difference of normalized coupling matrices in a fixed frame — a small-step approximation to
  transport-without-rotation. This is stated as an approximation rather than hidden; it can
  only *favour* the fibre arm, since it omits a transport correction that would subtract a
  component of the change.

## Arms (identical data, windows, detectors and tolerance)
- **A — base only**: the committed method.
- **B — base + fibre (Sasaki)**: the paper's full construction.
- **C — fibre only**: control. Does the coupling carry any demarcation signal at all?

## Tasks
1. **Within-trajectory localization** of the eyes-open/eyes-closed seam (geodesic CUSUM,
   tolerance ±2 s, 15 subjects) — the operational task.
2. **Between-state structural discrimination** under the committed within-state permutation
   null — the claim Paper 3 now leads with.

## Pre-registered criterion
The fibre **earns its place** iff arm B materially beats arm A on at least one task:
- localization: **≥ +3 hits out of 15**, or
- discrimination: **≥ +3 passing subjects out of 15**, with a higher median ratio.

Anything less is **NO MATERIAL GAIN**: the bundle apparatus is not doing measurable work on
this signal, and Paper 3's validated content is the base.

## Interpretive guard (fixed in advance, so a null cannot be spun)
A null from arm B is ambiguous between "the fibre carries nothing here" and "the coupling
estimator is broken". Arm C plus the self-test below separate them:
- if the self-test passes and arm C carries signal, a null in B is a **real** negative about
  the fibre's added value on this signal;
- if arm C is at chance *and* the self-test fails, the run is reported as an **instrument
  failure**, not as evidence against the fibre.

## Declared implementation choice: fibre scaling (fixed before the run)
A null could be manufactured by units alone: the base embedding has fixed norm 2 while the
normalized coupling has whatever magnitude the signal gives it, so a tiny fibre block would
make arm B collapse onto arm A trivially. To prevent that, arm B is reported at **two**
scalings, both fixed here:
- **B-literal**: the Sasaki metric exactly as §3.3 writes it, base and fibre added unweighted.
- **B-equal**: the fibre block rescaled so its median increment magnitude equals the base's,
  i.e. the fibre given *equal say*. This is deliberately **favourable to the fibre**.
If neither beats arm A by the margin above, the null is not an artefact of units.

## Distance convention (fixed before the run)
All three arms are scored with the *same* Euclidean distance on their own feature vectors, so
the comparison is about information content rather than metric choice. For the base this is the
chordal proxy of the committed sphere distance, which is monotone in it.

## Self-test gating the run
On a synthetic 2-channel signal with a **known injected PAC change at a known seam** (coupling
present before, absent after, base shape held fixed), the fibre arm must localize that seam
within tolerance. A coupling estimator that cannot see a coupling change it was handed cannot
be trusted to report its absence on real data. The run aborts if this fails.

## Attempt budget
**One run. No tuning loop.** Bands, windows, tolerance, arms and the criterion above are fixed
here, before execution. An instrument defect is fixed on the instrument and recorded as an
addendum; the threshold is never moved.

## Status
**Run. Verdict: NO MATERIAL GAIN — the bundle apparatus does not earn its place on this
signal.** Self-test **passed** and is what makes the null readable: the fibre arm localized an
injected PAC change to **1.25 s** while the base arm missed it by **14.25 s**, so the coupling
estimator demonstrably sees a coupling change the base cannot. On 15 real eyes-open/closed
subjects: base **10/15** localization and **7/15** discrimination (median ratio 1.26); the best
fibre-augmented arm reaches **11/15** and **9/15** (median ratio 1.16) — deltas of **+1** and
**+2**, both short of the pre-registered **+3**. The fibre-only control is weak but not inert
(2/15 localization, 3/15 discrimination). Adding the fibre also *lowers* the median
discrimination ratio (1.26 → 1.08 literal, 1.16 equal-weight), i.e. it dilutes rather than
sharpens. Conclusion: the coupling is measurable and genuinely discriminative for
coupling-carried transitions (self-test), but **redundant with the base** on the paper's own
worked paradigm. No threshold moved; one run, no tuning.
