# Benchmark Against Competing Change-Point Methods (Paper 3)

**The second blocking weakness, and it is entirely computational.** Paper 3 proposes
a detector and has never compared it to anything. No methods reviewer accepts a new
change-point detector without a comparison to the state of the art, and the question
*"why not just use an HMM / BOCPD / PELT?"* currently has no answer with a number
attached. This experiment supplies one, and — because the honest answer might be
"the baselines win" — it pre-registers **what would count as defeat** before running.

## Methods compared

**This paper's detectors** (on the trace-normalized SPD manifold):
- **geodesic CUSUM** — the global, permanence-aware detector (A1's best, 10/15);
- **geodesic F-ratio** — size-weighted change-point likelihood ratio;
- **window-mean break curve** — the local persistence detector.

**Generic change-point baselines** (offline unless noted), each given the *same*
windowed covariance sequence, vectorized:
- **BOCPD** (Adams & MacKay 2007) — the standard Bayesian **online** method;
- **PELT**, **BinSeg**, **Window** (`ruptures`; Truong et al. 2020);
- **Gaussian HMM** (`hmmlearn`, 2 states) — the field-standard brain-state model
  (Vidaurre et al., Baker et al.), change point read off the Viterbi state switch;
- **sliding-window k-means** (Allen et al. style), change point at the cluster switch.

**Feature sets.** Each baseline is run on the input most favourable to it, and the
comparison is reported per feature set, because the feature choice is exactly what is
at issue:
- `cov` — vectorized trace-normalized covariance (the *same* information the geometry
  receives; the fairest head-to-head);
- `logcov` — log-Euclidean vectorization (a strong Riemannian-flavoured baseline);
- `power` — per-channel band power (what a power-based pipeline sees).

The Riemannian-EEG literature (Barachant et al. 2012, 2013; Congedo, Barachant &
Bhatia 2017) is *related work rather than a baseline*: those methods classify
covariance matrices between **known labelled classes**, whereas this protocol
demarcates a regime change **within a single unlabelled trajectory**. That difference
is stated in the paper; the `logcov` baselines above are the closest runnable proxy
for a Riemannian-feature approach to the present task.

## Data

- **Real:** Sleep-EDF, the 15 recordings and the wake→sleep-onset transitions used in
  Trilha A1, with the hypnogram as ground truth. Identical loader, windows (2 s / 1 s
  step), band, and ±30 s tolerance — nothing is re-tuned for this comparison.
- **Null (false-alarm) segments:** for each recording, a segment of equal length lying
  entirely *within* one stage, so there is no true transition to find.
- **Synthetic characterization**, with exact ground truth, to establish *when*
  geometry helps and when it does not:
  - **S1 — structure changes, power preserved**: the decisive case the trace
    normalization is designed for, and where a power-based pipeline must fail;
  - **S2 — power changes, structure preserved**: the mirror case, where the geometry
    is blind *by construction* and power-based methods must win.
  Reporting both is the point: a one-sided demonstration would be advocacy.

## Metrics

1. **Hit rate** — |detected − true| ≤ 30 s on real transitions.
2. **Median absolute error** (seconds).
3. **Detection AUC** — each method's own confidence/prominence statistic, scored on
   real-transition segments versus null segments. This is the false-alarm axis and is
   **threshold-free**, so no method is advantaged by a tuned cut-off.
4. **Runtime** per record (feasibility of online operation).

Online/offline status is reported per method and comparisons are read within class:
BOCPD is genuinely online; `ruptures`, the HMM, and this paper's global detectors are
retrospective. Claiming a delay advantage over an offline method would be meaningless.

## Pre-registered decision rule (fixed before running; this is the defeat criterion)

Let `H*` be the best baseline hit rate on the real Sleep-EDF task and `H_g` the
geodesic CUSUM's.

- **WIN** — `H_g > H*`. The contribution is established with a number, and the paper
  may claim performance.
- **TIE** — `|H_g − H*| ≤ 1` recording. Then the contribution is **not performance**:
  the paper must be rewritten to claim *geometric interpretability and the structural/
  power dissociation*, not accuracy. This is a real outcome and must not be reported
  as a win.
- **LOSS** — `H_g ≤ H* − 2`. Reported plainly. The paper becomes "when the geometry
  helps and when it does not", which remains publishable and is more useful than an
  inflated victory.

**Separate, independent axis — the scenario advantage.** In S1 (structural transition
with power preserved), the claim is established if the geodesic CUSUM's hit rate
exceeds the best `power`-feature baseline by **≥ 0.30**. This can hold even under TIE
or LOSS above, and is the specific claim the trace normalization licenses. Symmetrically,
**S2 is expected to be a loss for the geometry**, and a failure to lose there would
indicate the S2 construction is not actually power-only and would invalidate the pair.

No threshold, tolerance, window, or feature definition is changed after seeing
results. Raw per-method, per-recording numbers go to
`_results/baseline_benchmark/result.json`; the prose verdict claims no more than that
table supports.

## Hyperparameter sensitivity and cost (reported alongside)

A grid over covariance window (1–4 s), band, and the CUSUM's minimum-segment
constraint, reported as a sensitivity map, plus per-record runtime for every method —
both are cheap, expected by reviewers, and currently absent from the paper.

## Status
Run. Mixed verdict across the three axes, reported without weighting toward the paper:

- **Localisation — WIN, but inside noise.** Geodesic CUSUM **10/15** vs best baseline
  (`rupturesWindow[logcov]`) **8/15**. Clears the pre-registered bar; a two-recording
  margin on fifteen is not a demonstrated performance advantage.
- **False-alarm discrimination — LOSS, and the worst of every method compared.**
  Detection AUC **0.23** against 0.67 for the best baseline and 0.88 at the top. Below
  0.5 means the detector's own confidence statistic is *anti*-correlated with whether a
  real transition is present: it localises well when told one exists, but cannot tell a
  real transition from a quiet stretch of a single stage. This belongs in Paper 3's
  limitations, prominently.
- **Scenario axis — advantage real but short of the bar.** S1 (structural transition,
  power held constant) geodesic **1.00** vs best power-feature baseline **0.75**
  (+0.25 against a +0.30 bar → **not established**). S2 (pure power change) geodesic
  **0.55** vs power baseline **1.00** — losing as designed, which validates the pair.

**Provenance, recorded because the correction favoured this paper's own method.** A
first run returned **LOSS** (10/15 vs a reported 14/15). It was invalid, and was caught
by a check independent of the outcome: power-feature baselines were scoring 1.00 on S1,
where total power is constant and a power method cannot beat chance. Cause: a
centre-bias leak from three sources — detector fallbacks returning the record midpoint
(which *was* the answer, since segments were cut symmetrically around the transition),
an HMM/k-means heuristic preferring the most central switch, and a fixed midpoint seam
in the synthetic scenarios. All three fixed (no-detection sentinel; largest-mean-shift
selection; randomised seam; jittered real windows), moving baselines by up to ten
recordings (HMM[cov] 14/15 → 4/15). See `_results/baseline_benchmark/result.json`.
