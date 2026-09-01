# A Permanence-Aware On-Line Localizer: One Attempt at the ≥10/15 Band (Paper 3)

**Written before the run.** The detector below is fixed here in full; no parameter is
tuned after seeing results.

## The standing result this tries to move

`online_localization_cusum` tested two global, permanence-aware change-point detectors
on real eyes-open→eyes-closed EEG (eegmmidb, 15 subjects) and reached **8/15** — better
than the local window-mean (reported 4/15) but short of the pre-registered **SOLVED
band of ≥ 10/15**. Its diagnosis: spontaneous occipital alpha bursts are
*sustained-and-recurrent*, and even a global F-ratio or CUSUM can be pulled to a burst
that later returns to the pre-transition state, because neither explicitly requires the
post-transition segment to *stay* changed.

## The idea being tested

A single new detector that encodes permanence directly, rather than hoping the F-ratio's
scatter penalty or the CUSUM's tent length captures it. A genuine transition ends the
record in the *new* state; a burst ends it back in the *old* one. So anchor to where the
record actually ends and score each candidate split by whether its post-segment resembles
that terminal state:

For each split $\tau$ (with a minimum segment length), on the embedded trajectory,

$$\text{score}(\tau) = d(m_{\text{pre}}, m_{\text{post}})\cdot
   \max\!\Big(0,\ 1 - \frac{d(m_{\text{post}}, m_{\text{term}})}{d(m_{\text{pre}}, m_{\text{term}})}\Big),$$

where $m_{\text{pre}},m_{\text{post}}$ are the segment mean embeddings either side of
$\tau$, $m_{\text{term}}$ is the mean of the final quarter of the record, and $d$ is the
geodesic distance on the same radius-$R$ sphere the sister detectors use. The localized
point is $\arg\max_\tau \text{score}(\tau)$. A burst's post-segment returns toward the
pre-state and away from the terminal, so the permanence factor collapses it; a permanent
transition's post-segment matches the terminal, so the factor is ≈ 1 and the ordinary
between-mean distance stands.

This uses **no labels** — only the structural assumption that a single transition does
not return, which is the property Paper 3's whole method is about. It is the same data,
loader, embedding, sphere radius, minimum-segment length and ±2 s tolerance as
`online_localization_cusum`; only the statistic is new.

## Fixed parameters (no post-hoc tuning)

- terminal window = final **0.25** of the record (fixed here, not swept);
- minimum segment, segment seconds, step, tolerance, channels, band, subject count:
  **inherited unchanged** from `real_eeg_localization` / `online_localization_cusum`.

The window-mean, F-ratio and CUSUM detectors are re-run head-to-head on the identical
subjects so the comparison is exact, and the 8/15 CUSUM figure serves as the reproduction
check: if the baselines do not reproduce, the run is void.

## Pre-registered decision rule

- **MOVES THE BOUND** — the permanence detector reaches **≥ 10/15** hits (the original
  SOLVED band), *and* the baselines reproduce (best of window-mean/F-ratio/CUSUM within
  ±1 of the 8/15 already on record). Then Paper 3's on-line localization is solved on
  real EEG by this detector, and the appendix is updated from "materially better, not
  solved" to name it.
- **BOUND HOLDS** — the permanence detector scores < 10/15. Then the on-line
  localization limit stands, this idea is reported as tried-and-insufficient with its
  number, and no claim in Paper 3 changes except to record that a permanence-explicit
  detector was tested and did not clear the bar.
- **VOID** — the baselines do not reproduce (data/loader drift), so nothing is concluded.

One attempt. If the detector fails, that is the result; it is not re-parameterised.

## Status
Run (see the Addendum below for the one specification fix applied). Outcome:
**BOUND_HOLDS**. The permanence-aware detector localizes **3/15**, below CUSUM's 8/15
and the pre-registered ≥10/15 SOLVED band; baselines reproduced (window-mean 4, F-ratio
6, CUSUM 8). One idea, one specification fix, one attempt — no tuning loop. Paper 3's
'materially better, not solved' on-line localization claim stands unchanged. See
`_results/online_localization_permanence/result.json`.

## Addendum (specification defect, corrected before the recorded verdict)

The first run scored the permanence detector at 1/15, and a diagnosis of the curve
showed why: it peaked at $\tau \approx \text{min\_seg}$ (the earliest allowed split),
not at the transition. The cause is a **specification defect in the statistic, not a
property of the permanence idea**: the between-mean term $d(m_{\text{pre}},m_{\text{post}})$
was not size-weighted, so it spiked at the record boundaries — exactly the boundary
artefact the sister F-ratio removes with the standard change-point weighting
$\text{size}(\tau)=\tau(n-\tau)/n$ (zero at the ends, maximal at the centre), documented
in that detector's own code.

The statistic is corrected to $\text{score}(\tau)=\text{size}(\tau)\cdot
d(m_{\text{pre}},m_{\text{post}})\cdot\text{permanence}(\tau)$. This is justified
**outcome-independently** — the size factor is the textbook weighting every
change-point statistic uses, and its omission was an error, not a choice — so it is
applied once, the criterion (≥10/15) is unchanged, and if the corrected detector still
fails, that is the recorded result. This is a single specification fix, not the start
of a tuning loop.
