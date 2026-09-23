## The claim in one paragraph

Given a *single* multichannel record that crosses an abrupt transition, decide
whether the post-transition dynamics is a directed (drift-dominated) reorganization,
an undirected (diffusion-dominated) random walk, or a collapse of structure — from
one realization, with no ensemble. The standard discriminators for this question are
ensemble laws that are not identifiable from a single trajectory, which is exactly
the regime abrupt transitions in expensive-to-observe systems impose: one record per
transition.

This paper is logically independent of its two companions and stands or falls as a
time-series method.

## The construction

**A Riemannian vector bundle.** The instantaneous state is a point whose base is a
product of two trace-normalized SPD covariance-shape manifolds — one on a slow
timescale, one on a fast timescale of the same signal — with a normalized cross-scale
coupling statistic in the fibre. Trace normalization removes global-power and
broadband-gain confounds, so what is measured is *correlation geometry* rather than
amplitude. That choice is the method's central commitment, and it is two-edged: it is
why the method sees a structural transition carrying no power change, and why it is
blind to a pure power change.

**A jump-diffusion model.** A Poisson–Lévy jump term is added to drift and Gaussian
diffusion, with jump intensity tied to the estimator's local conditional residual
variance — so an abrupt transition is a discrete jump localized at maximal predictive
breakdown, not a smooth slide requiring unbounded drift.

**A single-trajectory test.** The ensemble displacement-scaling law is replaced by a
path-wise likelihood-ratio test: the trajectory is anti-developed once to a fixed
tangent space by Cartan development, so Girsanov's theorem identifies the drift from
a single path, with curvature entering only at second order as holonomy.

## What the suite established

**On real data, no structure beyond power yet.** On eyes-open versus eyes-closed EEG the geometry
registers a difference between two recordings that exceeds each one's internal drift (12/15
subjects, about a third). It beats a same-state between-recording control only weakly (11/15,
p ≈ 0.024), and a scalar baseline — per-channel relative alpha power on the same channels —
separates the states far more strongly (median ≈3.5 against ≈1.3; `between_recording_control`). On
Sleep-EDF (N2 versus REM, 14/15) it is attributed to the EOG channel in the covariance: without
it the discrimination holds in only 2 of 4 subjects (`discrimination_eog_ablation`). Within-trajectory
sleep-onset localization appeared to reach 10/15 against 4/15 on eyes-open/closed, which
was read as showing the limit was the *paradigm*, not the method. A later control withdrew
that reading: every localization window was centred on the true transition, so a detector
that always predicts the centre scores every recording; off-centre, sleep-onset
localization falls to 4/7 and ties a scalar band-power CUSUM
(`sleep_stage_localization`, `localization_centerbias_control`). On-line localization is open.

**Against standard baselines, with the defeat criterion fixed in advance.** The
protocol had never been compared to anything. It now has been — against BOCPD,
`ruptures` (PELT, binary segmentation, windowed), a Gaussian HMM and sliding-window
k-means, each given the same features (`baseline_benchmark`). The outcome is
genuinely mixed and is reported on three axes rather than summarized by the
flattering one: it leads on localization by a margin inside binomial noise; it is
competitive but not superior on detection; and on the structural-versus-power axis,
which is what the trace normalization is *for*, it is ahead of every power-based
pipeline while losing the mirror scenario exactly as its construction requires.
Reporting the mirror case is what makes the pair evidence rather than advocacy.

**A sub-chance result, diagnosed and repaired.** The benchmark initially made the
detector the *worst* method compared, at detection AUC 0.23 — not merely poor but
anti-correlated. The cause was the confidence statistic, not the geometry: the
benchmark scored peak-to-median on a curve that is a *tent* under a real change point
and a driftless random walk under none, which rewards the null by construction. The
diagnosis was stated as a falsifiable prediction and both halves were verified before
any repair was scored. Four repairs were pre-registered against a fixed bar; the
cheapest passed, lifting detection to 0.81 (`detection_statistic_repair`). The
original 0.23 is retained unaltered in the benchmark record.

**And then validated out of sample.** That repair was *chosen* on the same fifteen
records that exposed the problem, so on its own it showed only that some statistic
fits those records. Applied unchanged to a paradigm not used to select it, with the
bar fixed in advance, it holds at AUC 0.82 — and the old statistic fails sub-chance a
second time, which is what the mechanistic diagnosis predicted and what single-corpus
selection could not have shown (`detection_repair_heldout`).

**A corrected headline.** The appendix's ≈12× structural effect was traced to an
estimator choice and corrected to ≈3.3× — and then again to ≈1.3×, because the ≈3.3×
estimator treats overlapping, autocorrelated windows as exchangeable. Against within-state drift
the effect is above unity in 12 of 15 subjects; the paper now reports ≈1.3 (`eeg_reconciliation`), as a
difference between two recordings that a scalar alpha-power baseline beats (`between_recording_control`).

## Declared failure modes

The method has a structural region where a weak jump is not separable from drift at
any threshold (`drift_jump_confusion_sweep`), and longer windows make it worse
because holonomy accumulates. A flat log-Euclidean base metric resolves that corner
but costs weak-collapse jump power, so the recommendation is square-root primary with
a log-Euclidean cross-check (`base_metric_corner`, `log_euclidean_real_eeg`). On-line
localization of transitions that are not the dominant geometric event in their record
remains open, with the cause identified rather than merely observed.
