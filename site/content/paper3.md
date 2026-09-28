## What this paper is

The full validation record of a method that reads trace-normalized channel covariances on the
SPD manifold through a geodesic cumulative-sum (CUSUM) change-point statistic. Five traps made it
look validated, each removed by a specific control. The paper does not offer the method for
adoption.

## The five traps

- **Centre bias.** Localization windows centred on the transition. Off-centre, the geometry's
  lead over a scalar detector became a tie (10/22 vs 10/22). On all 151 usable sleep recordings
  the scalar was slightly ahead (geometry 59/151, scalar 67/151; McNemar p ≈ 0.38).
- **Dependence ignored.** Permutation nulls on overlapping windows made an eyes-open/closed
  ratio look like ≈3.3; against within-recording drift it was ≈1.3.
- **Pseudo-replication.** Seven sleep recordings came from four people; no subject-level
  significance was possible.
- **Ocular contamination.** Without the eye channel, a sleep-staging association fell from
  V = 0.452 to 0.021; EOG power alone was more strongly associated with stage.
- **Recording confound.** Eyes open and closed were separate recordings; relative alpha power
  separated them far more strongly than the geometry, and a change of recording alone fired the
  detector.

## The field's standard pipeline

The standard covariance → minimum-distance-to-mean pipeline, put through the same controls,
crossed none of the pre-specified bars. Given the method's trace-normalized, overlapping
covariances (the matched control), it fell into the ocular trap (accuracy drop 0.092) and no
other, so the eye channel's dominance is attributed to trace normalization; the other traps arose
in how the method was evaluated. There was no evidence that the geometry adds information beyond
relative alpha power (11 of 15 subjects improved, Wilcoxon p = 0.76), and with 64 channels state
detection fell below chance (AUC 0.41).

## A survey of published practice

In 20 open-access covariance-based EEG studies, ocular handling was not reported in 7 of 19
(7–15 counting unclear codes) and dependence-blind validation appeared in 4 of 19 (4–12). The
counts describe reporting, not the presence of a trap, and the survey had one coder.

## Recommendations

Off-centre localization with a centre-prior baseline; dependence-respecting nulls and folds;
the subject as the unit of inference; reported and tested ocular handling; a same-condition
between-recording control and a scalar baseline; and, for pipelines that combine band-pass
filtering with trace normalization, a relative band-power baseline on the unfiltered signal.
