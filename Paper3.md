# Five Ways a Covariance-Geometry EEG Method Appeared Validated, and the Controls That Overturned It

João Vitor Perazzolo

27 September 2026

---

## Abstract

**Background.** EEG validation results can be inflated by evaluation designs unrelated to whether a method works. Such traps are rarely reported as they occur.

**New method.** We report the full validation record of a method that reads trace-normalized channel covariances on the symmetric positive-definite (SPD) manifold through a geodesic cumulative-sum (CUSUM) change-point statistic.

**Results.** Five traps inflated performance: localization windows centred on the transition, nulls ignoring dependence between windows, recordings counted as subjects, an eye channel inside the covariance, and conditions confounded with recordings. After correction, the method's lead over a scalar power detector disappeared (59/151 against 67/151 sleep transitions localized; McNemar p ≈ 0.38), and a sleep-staging association fell from Cramér's V = 0.452 to 0.021 without the eye channel.

**Comparison with existing methods.** The standard minimum-distance-to-Riemannian-mean pipeline crossed none of the pre-specified bars. Given trace-normalized, overlapping covariances, it became dependent on the eye channel (accuracy drop 0.092 against 0.007) but showed no other trap. There was no evidence that the geometry adds information beyond relative alpha power (Wilcoxon p = 0.76), and with 64 channels its state detection fell below chance (AUC 0.41). In 20 published covariance-based EEG studies, ocular contamination could not be ruled out in 7–15 of 19 and dependence-blind validation in 4–12 of 19.

**Conclusions.** One trap, ocular dependence, belonged to the design, most plausibly to trace normalization, which removes amplitude and leaves correlation structure, where the eye channel weighed most. The others arose in how the method was evaluated. We recommend six controls.

**Keywords:** EEG; covariance matrices; Riemannian geometry; change-point detection; cross-validation; negative results

### Highlights

- A covariance-geometry EEG method passed five validations later controls reversed.
- Each false pass had an ordinary cause, from centred windows to eye channels.
- The standard Riemannian pipeline crossed no pre-specified bar on the same data.
- With this method's covariances, the standard classifier relied on the eye channel.
- Published covariance-EEG studies often omit the controls that expose these traps.

---

## 1. Introduction

A method can appear validated for reasons that have nothing to do with whether it works. An evaluation window is placed where the answer lies. A permutation null treats dependent samples as exchangeable. Two nights of one person are counted as two people. An eye channel carries the effect. Two recordings differ because they are two recordings. Each of these problems is familiar in the abstract. Pseudo-replication was named in ecology four decades ago (Hurlbert 1984). The dependence of cross-validation estimates on the structure of neuroimaging data is well documented (Lemm et al. 2011; Varoquaux et al. 2017; Schroeder et al. 2025). The confounding of EEG classes with recording blocks was shown to produce spurious decoding in a widely cited case (Li et al. 2021). Reporting standards for EEG and MEG ask authors to describe the choices that would expose them (Pernet et al. 2020).

The problems are nonetheless easy to miss inside a particular analysis, because the surrounding work looks careful. This paper reports one method that fell into all five in turn, and the control that exposed each. The method is not new in its ingredients. Covariance matrices on the SPD manifold have been used to classify EEG for more than a decade (Barachant et al. 2012, 2013; Congedo et al. 2017). What it added was a single-trajectory reading: a geodesic change-point statistic on a sequence of trace-normalized covariances, intended to localize and characterize a transition within one continuous recording. The motivating claim was that trace normalization makes the geometry blind to overall power and sensitive to the structure of spatial correlation, so that it would register transitions that a power-based detector misses. That claim did not survive.

The record is useful for three reasons. It shows how each trap operated on real numbers. It separates traps of this method from traps of the field, by running the field's standard pipeline through the same controls. And it measures, in a small survey, how often published studies report enough to rule the traps out. The paper does not offer the method for adoption.

## 2. Materials and Methods

### 2.1 Data

Two public PhysioNet corpora were used (Goldberger et al. 2000; Pollard et al. 2026).

**EEG Motor Movement/Imagery Database** (Schalk et al. 2004). We used the one-minute eyes-open (run R01) and eyes-closed (run R02) baselines and the rest intervals (T0) of task runs R03 and R07, in 15 subjects. Analyses used seven occipito-parietal channels (O1, Oz, O2, PO3, POz, PO4, Pz), band-pass filtered to 8–13 Hz except where stated.

**Sleep-EDF Expanded, sleep-cassette recordings** (Kemp et al. 2000). We used channels Fpz-Cz, Pz-Oz and horizontal EOG, band-pass filtered to 0.5–30 Hz and standardized per channel over the recording. Most subjects contributed two nights. Early analyses used between 7 and 15 recordings, depending on what had been downloaded; the final localization analysis attempted all 153 recordings and used the 151 with a qualifying transition, from 78 subjects.

All data are de-identified and publicly available. No new data were collected.

### 2.2 The method under test

**Representation.** The band-passed, standardized signal was cut into overlapping windows: 1 s with a 0.25 s step for the eyes-open/closed analyses, and 2 s with a 1 s step for sleep. Each window's channel covariance was floored at a small eigenvalue and divided by its trace, which places it on the manifold of unit-trace SPD matrices and removes overall power: two windows that differ by a gain factor map to the same point. Matrices were compared under the square-root metric, in which $\rho \mapsto \sqrt{\rho}$ embeds unit-trace SPD matrices in a sphere and geodesic distance is arc length between embedded points (Bhatia 2007; see Pennec et al. 2006 for the affine-invariant alternative).

**Localization.** The embedded coordinates were accumulated in a multivariate CUSUM, and the change point was taken as the argmax of $|S_t|$.

**Detection.** Whether a segment contains a transition at all was scored first by the peak-to-median ratio $\max|S| / \operatorname{median}|S|$, and after repair (§3.9) by the scale-normalized peak $\max|S| / (\hat\sigma \sqrt{n})$, where $\hat\sigma$ is the segment's increment scale and $n$ its length.

**Discrimination.** To ask whether two states differ, the distance between the states' mean geometries was divided by a within-state distance. Two within-state estimators were used: the median distance between randomly interleaved halves (the *permutation* estimator, used first) and the distance between the first-half and second-half means of each state (the *temporal-half* estimator).

The method was first proposed as a larger construction with a vector-bundle fibre and a three-regime demarcation. A planned ablation found the fibre lowered discrimination, and a planned gate found the demarcation had no external label against which it could be tested. Neither is evaluated here; the paper concerns the trace-normalized SPD base and its CUSUM.

### 2.3 Localization task and comparator

For sleep, the transition in each recording was the first stage boundary involving Wake or REM with at least 90 s of a single stage on each side. The analysis window ran from 45 s before to 135 s after the transition, so the transition sat at one quarter of the window. A localization counted as correct if the estimated change point lay within ±30 s, one scoring epoch, of the scored boundary. The scalar comparator was the same CUSUM applied to the log trace of the window covariance, that is, to log broadband power. Neither detector was tuned on these data. The eyes-open/closed localization task concatenated an eyes-open and an eyes-closed segment, each amplitude-normalized so that the seam was not a power step. The early localization comparisons of §3.1 used 22 records: 15 eyes-open/closed concatenations and 7 sleep recordings.

### 2.4 Controls for the five traps

- **Centre bias.** A centre-prior detector that always predicts the window centre, and windows with the transition off-centre.
- **Dependence.** Circular-shift nulls that preserve autocorrelation, in place of i.i.d. label shuffles, and the temporal-half estimator in place of the permutation estimator.
- **Pseudo-replication.** Inference at the level of subjects, with the smallest attainable p-value reported.
- **Ocular contamination.** Every sleep analysis repeated without the EOG channel, and EOG power alone as a competitor.
- **Recording confound.** The discrimination statistic computed on two separate recordings of the same state (T0 of R03 against T0 of R07), whose occipital alpha power is consistent with eyes open in 14 of 15 subjects; and a scalar baseline on the same channels with the same statistic, per-channel relative alpha power (8–13 Hz over 1–40 Hz power, on the unfiltered signal).

### 2.5 Standard-pipeline control

To separate traps of this method from traps of the field, the standard pipeline was put through the same controls: covariance estimation with oracle approximating shrinkage (Chen et al. 2010) followed by minimum distance to Riemannian mean (MDM; Barachant et al. 2012), as implemented in pyRiemann 0.12 (Barachant et al. n.d.). The pipeline used the band-passed signal, standardized per channel over the recording, without trace normalization, on non-overlapping epochs: the 30 s scoring epochs for sleep, and 2 s epochs for the motor/imagery corpus. The pre-specified criteria were: a shuffled-minus-blocked cross-validation difference of at least 0.05 (dependence); a difference of at least 0.05 between grouping folds by recording and by subject (pseudo-replication); an accuracy drop of at least 0.05 without EOG (ocular); and balanced accuracy of at least 0.70 on two same-state recordings (recording confound). The framing rule, fixed before the run, was that a trap the standard pipeline also fell into would be reported as a trap of the field.

This control differs from the method under test in three ways at once: the classifier, the absence of trace normalization, and the absence of overlap. Section 2.6 adds the control that separates them.

### 2.6 Matched control and incremental test (specified before execution)

**Matched control.** The MDM classifier of §2.5 is run on trace-normalized covariances of overlapping windows with the windowing of §2.2, on the same tasks and with the same criteria. If the standard pipeline falls into at least one of the dependence, ocular or recording traps under these conditions, the traps are properties of the design (trace normalization and overlap, which this control does not separate) rather than of the geodesic CUSUM. If it falls into none, they are properties of the CUSUM reading, and the interpretation of §4.1 is withdrawn.

**Incremental test.** On non-overlapping 2 s epochs of the eyes-open and eyes-closed baselines, a logistic model with per-channel relative alpha power is compared with the same model plus geometric features: the tangent-space coordinates of the trace-normalized covariance at the training set's Riemannian mean. Both are evaluated by leave-one-subject-out cross-validation, so that no recording of the test subject is seen in training. The geometry carries information beyond alpha power if the held-out log-loss improves in at least 11 of 15 subjects and a paired Wilcoxon test gives p < 0.05. The same models are also trained to separate the two same-state recordings, where both should be at chance.

**Channel density.** The sleep covariance in this record is 3 × 3, or 2 × 2 without EOG, and a 2 × 2 unit-trace matrix has two degrees of freedom. To test whether the negative results depend on that dimension, the two between-recording controls, for discrimination (§2.4) and for detection (§3.5), are repeated with all 64 channels of the motor/imagery corpus. The results depend on channel density if, with 64 channels, the eyes-open/closed ratio exceeds the same-state control in at least 12 of 15 subjects (Wilcoxon p < 0.01), and the detection statistic separates a change of state from a same-state change of recording at AUC ≥ 0.80, against 0.72 with seven channels.

### 2.7 Literature survey

A fixed Europe PMC query, `(EEG OR electroencephalogra*) AND ("Riemannian" OR "covariance matrices" OR "SPD matrices") AND OPEN_ACCESS:y AND PUB_YEAR:[2012 TO 2025]`, was walked in the order returned. The first 20 eligible studies were included; 7 were screened out on the way (for example, fNIRS-only or MEG-only studies, or studies without covariance features). For each study and trap, a code of Yes (left open), No (addressed), Unclear or Not applicable was assigned by rules fixed in advance, and the sentence supporting each code was archived. The survey measures what studies report, not whether a trap was present. There was one coder. An intra-rater re-coding after at least two weeks, blind to the first codes, is planned as a check on coding stability; it is not a substitute for an independent second coder.

### 2.8 Statistics

Paired detector comparisons used the exact McNemar test on discordant pairs. Within-subject comparisons across subjects used the Wilcoxon signed-rank test. Proportions are reported with Wilson 95% confidence intervals. Associations between a binary geometric regime label and sleep stage used Cramér's V, tested against circular-shift nulls. Detection was scored by the area under the ROC curve (AUC) for transition segments against length-matched segments within one stage.

### 2.9 Pre-specification and provenance

Each analysis has a written plan fixing its question, method, criterion and stopping rule, archived with its code and raw output in the accompanying repository. For five of the analyses reported here, the plan was committed before the result: the standard-pipeline control, the off-centre localization power-up, the two between-recording controls, and the literature survey. For the others, the plan and the result entered the repository in the same commit, so their order cannot be verified from the record. Commit timestamps in a repository controlled by the author are not independent evidence of order in any case. The analyses in §2.6 were specified in a version of this manuscript and in pre-registration files committed before they were run (commit `fbe4b6f`), and their results were committed afterwards (commit `46b168f`). No external registry was used.

## 3. Results

### 3.1 Centre bias

Every localization analysis in the early record built its window symmetric about the known transition. Under that construction a centre-prior detector scores every recording (22/22) and, off-centre, none (0/22). The inflation affected the one comparison that had favoured the method. Centred, the geodesic CUSUM led the scalar CUSUM, 14/22 against 9/22 (McNemar p = 0.227, already not significant). Off-centre they tied, 10/22 against 10/22. On sleep onset, the geometry's 10/15 in centred windows fell to 4/7 off-centre on the recordings then available, tying the scalar's 4/7. An earlier benchmark against six standard change-point algorithms (Adams and MacKay 2007; Truong et al. 2020), which had placed the geodesic CUSUM at 10/15 against 8/15 for the best baseline, also used centred windows.

A power-up on all 151 usable sleep-cassette recordings, with off-centre windows and the detectors unchanged, settled the comparison. The geodesic CUSUM localized 59/151 transitions (39%, 95% CI 32–47%) and the scalar CUSUM 67/151 (44%, 37–52%; McNemar p ≈ 0.38). At the subject level the counts were 32/78 against 42/78; without the EOG channel, 57/151 against 66/151. The pre-specified verdict is inconclusive. With about twice the sample a power analysis had asked for and the direction favouring the scalar, the geometry does not improve on log broadband power for sleep-transition localization.

### 3.2 Nulls and validation that ignore dependence

Overlapping windows of one recording are strongly autocorrelated. Two results were inflated by treating them as exchangeable. With the permutation estimator, the eyes-open/closed discrimination ratio exceeded one in 14 of 15 subjects at a median of about 3.3. The permutation cancels slow drift within a state, so the estimator would flag almost any two recordings as different. Measured against each recording's own first-half-to-second-half drift, the median ratio was about 1.3, above one in 12 of 15 subjects (Wilcoxon p ≈ 0.008).

An association between a geometric volatility label and sleep stage was first tested against an i.i.d. label shuffle, whose 95th percentile of Cramér's V was 0.003. Against a circular-shift null the 95th percentile was 0.171. The observed association (V = 0.452) exceeded both, and fell instead to the ocular control (§3.4). An N2-versus-REM discrimination also survived a circular-shift null on all seven recordings checked, and was also attributable to the EOG channel. The corrected null does not always change the verdict, but it must be run to know.

### 3.3 Pseudo-replication

The seven recordings behind the sleep-staging association came from four subjects. The record-level one-sided Wilcoxon p = 0.0078 has no subject-level counterpart: with four subjects, the smallest attainable one-sided p is 0.0625. No significance claim was possible at the correct unit.

### 3.4 Ocular contamination

The sleep covariance included the horizontal-EOG channel, and REM is defined in part by rapid eye movements. Without the EOG channel, the geometric volatility's association with sleep stage fell from V = 0.452 to 0.021, and EOG power alone was more strongly associated with stage (V = 0.524). The N2-versus-REM discrimination had passed in 14 of 15 recordings under a window-permutation null and in all 7 recordings re-tested under a circular-shift null (§3.2). On those 7 recordings, from 4 subjects, it held without EOG in 4 recordings and 2 subjects, against all 7 and all 4 with it. In these channels the signal was the eye. Because the EEG-only covariance is 2 × 2, this licenses a conclusion about these channels, not about covariance geometry in general.

### 3.5 Recording confound

After the corrections above, the remaining real-data effect was that eyes-open and eyes-closed recordings differed by more than each drifted internally (median ratio ≈ 1.3). The two states are separate runs. On two separate recordings of the same state, the same statistic had a median of 0.95, and the eyes-open/closed ratio exceeded this control in 11 of 15 subjects (one-sided Wilcoxon p ≈ 0.024). The control is biased in the method's favour: its windows span about 61 s against 26 s, which inflates its denominator. Per-channel relative alpha power, on the same channels with the same statistic, separated the states far more strongly (median ratio ≈ 3.5, paired Wilcoxon p ≈ 10⁻⁴).

The same asymmetry was present in the method's one out-of-sample detection success. Validated on segments that spliced the eyes-open and eyes-closed runs, against nulls within one run, the repaired detection statistic reached AUC 0.82. Rebuilt on a common chunk structure, it separated a change of state from a same-state change of recording at AUC 0.72, just above a pre-specified bar of 0.70 with an uncertainty of about ±0.1 at n = 15. A change of recording alone, with no change of state, fired it at AUC 0.74 against segments within one recording.

### 3.6 The standard pipeline

None of the four applicable traps moved the standard pipeline past its pre-specified bar (Table 1). Shuffled folds exceeded blocked folds by a median of 0.009 over 151 recordings in within-recording N2-versus-REM classification. Grouping folds by recording or by subject changed pooled accuracy by 0.001. Removing EOG lowered median subject-level accuracy by 0.007. On two same-state recordings, blocked cross-validation gave a median balanced accuracy of 0.65, against 0.87 for eyes open versus closed: below the bar of 0.70, but above chance.

Two qualifications apply. The epochs were non-overlapping, so the small shuffled-minus-blocked difference shows that this epoch design does not create the dependence, not that the classifier resists it. Standard practice does not guard against it by construction: the pyRiemann motor-imagery example cross-validates with shuffled k-fold over epochs (Barachant et al. n.d.), which is harmless on interleaved trial designs and not on block designs (Schroeder et al. 2025). And the 0.65 on same-state recordings shows that the recording confound is not zero for the standard pipeline either.

### 3.7 Matched control

The matched control reproduced one trap. With trace-normalized covariances of overlapping windows, removing the EOG channel lowered the standard classifier's N2-versus-REM accuracy by a median of 0.092 across 78 subjects (interquartile range 0.049–0.132; one-sided Wilcoxon p = 8.4 × 10⁻¹⁵), against 0.007 without trace normalization, crossing the bar of 0.05. The dependence trap did not appear: shuffled folds exceeded blocked folds by a median of 0.003 over 151 recordings (interquartile range 0.002–0.006). Nor did the recording confound: on two same-state recordings the median balanced accuracy was 0.608 (interquartile range 0.538–0.692), against 0.849 for eyes open versus closed and a bar of 0.70; without trace normalization it had been 0.65. Grouping folds by recording or by subject changed pooled accuracy by less than 0.001. Under the pre-specified reading rule, one crossing suffices to attribute the traps to the design; §4.1 explains why the attribution holds for the ocular trap only.

### 3.8 Information beyond alpha power, and channel density

**Information beyond alpha power.** Adding the geometric features lowered held-out log-loss in 11 of 15 subjects (median log-loss 0.518 without, 0.373 with) but raised it sharply in the other four, in one case from 0.876 to 1.629, and the paired Wilcoxon test was not significant (two-sided p = 0.76). The pre-specified criterion required both conditions and was not met: there is no evidence that the geometry carries information about eye state beyond per-channel relative alpha power. On two same-state recordings both models were at chance (median balanced accuracy 0.53 and 0.55; median log-loss 0.695 and 0.721, against 0.693 for chance).

**Channel density.** With 64 channels, the eyes-open/closed geometric ratio exceeded the same-state control in 13 of 15 subjects (one-sided Wilcoxon p = 0.0017; median 1.24 against 0.78), meeting the first half of the criterion; with seven channels it had been 11 of 15 (p = 0.024). The detection half failed: the statistic separated a change of state from a same-state change of recording at AUC 0.41, below chance and far below the bar of 0.80. It responded more to a change of recording than to a change of state (AUC 0.57 and 0.46, each against segments within one recording). The conjoint criterion was not met. More channels improved discrimination and worsened detection, and with 64 channels relative alpha power still separated the states more strongly (median ratio 4.01, against 0.98 for the same-state control).

### 3.9 What survives

**A repair to the detection statistic.** The original peak-to-median statistic scored AUC 0.227 on sleep-onset detection, worse than chance, because under no change point the CUSUM is a driftless random walk whose median is small, which inflates the ratio. The scale-normalized peak raised detection to AUC 0.813 with localization unchanged. Applied without change to the eyes-open/closed paradigm, it held at 0.824, while the old statistic fell to 0.434. Section 3.5 bounds what this held-out result shows.

**A base-metric result, on synthetic data only.** Under the square-root metric, a weak structural collapse and a strong geodesic drift were confusable (worst-corner AUC 0.653). Under the flat log-Euclidean metric the same corner reached 0.960, which locates the confusion in the curvature of the square-root embedding.

**A benchmark position.** As a detector, the repaired CUSUM ranked fourth of nineteen method-feature combinations (AUC 0.81 against 0.88 for the best). On a synthetic transition in correlation structure at constant power it localized perfectly (1.00) against the best power-feature baseline's 0.75. That margin of 0.25 falls short of the 0.30 set in the analysis plan. On the mirror scenario, a pure power change, it scored 0.55 against 1.00, as its construction requires.

No result survived showing that the method does better than a scalar baseline on real data.

### 3.10 Literature survey

Of the 20 included studies, trap codes were as follows (Yes = left open; the range adds Unclear codes):

- ocular handling not reported where conditions plausibly differ in eye movements: 7 of 19 (7–15 of 19);
- validation that ignored dependence between trials or windows: 4 of 19 (4–12 of 19);
- pseudo-replication: 0 of 9 (0–4 of 9);
- classes confounded with recordings: 1 of 17 (1–3 of 17);
- centre bias: not applicable to any study, none of which localized a transition in time.

A Yes for ocular handling means that no handling was reported, not that the study was contaminated. One included study measured the dependence trap directly for the standard classifier on block-design n-back data, finding accuracy differences of up to 12.7% between cross-validation that respected the block structure and cross-validation that did not (Schroeder et al. 2025).

**Table 1.** Summary of the five traps.

| Trap | Effect on this method | Control that exposed it | Standard pipeline (MDM) | MDM, trace-normalized, overlapping windows | Published studies: Yes (Yes + Unclear) |
|---|---|---|---|---|---|
| Centre bias | lead 14/22 vs 9/22 → tie 10/22 vs 10/22; 59/151 vs 67/151 at scale | off-centre windows; power-up | not applicable | not applicable | not applicable |
| Dependence ignored | ratio ≈ 3.3 (14/15) → ≈ 1.3 (12/15); null 95th percentile 0.003 → 0.171 | temporal-half estimator; circular-shift null | below bar (+0.009; non-overlapping epochs) | below bar (+0.003) | 4/19 (12/19) |
| Pseudo-replication | p = 0.0078 on 7 recordings of 4 subjects; best attainable 0.0625 | subject as unit | below bar (0.001) | below bar (< 0.001) | 0/9 (4/9) |
| Ocular contamination | V 0.452 → 0.021 without EOG | EOG ablation | below bar (0.007) | crosses (0.092) | 7/19 (15/19) |
| Recording confound | ratio exceeds same-state control weakly; alpha power stronger; AUC 0.74 for a recording change alone | same-state between-recording controls | below bar (0.65; above chance) | below bar (0.608) | 1/17 (3/17) |

## 4. Discussion

### 4.1 What the design explains

By the rule fixed in advance, these are traps of this method: the standard pipeline did not fall into them on the same data. The matched control (§3.7) shows how much of that difference the method's design explains. Given the same design, the standard classifier fell into the ocular trap and into neither the dependence nor the recording trap.

Two design differences were candidates for protecting the standard pipeline. The first, amplitude, is supported by the matched control. This method band-pass filtered the signal, standardized each channel over the recording, and divided each window's covariance by its trace. What that removes depends on the task. In sleep it removed epoch-to-epoch amplitude, which differs between N2 and REM and which the standard covariance kept. In the eyes-open/closed task, the scalar that beat the geometry was relative alpha power, alpha over broadband power on the unfiltered signal. That is also a normalized quantity, but it keeps the share of alpha within each channel, which is exactly what changes when the eyes close. The geometry lost it in two steps: filtering to the alpha band left no other band to compare against, and trace normalization removed the total alpha amplitude. What remained was correlation structure, where an artefact channel such as EOG carries the most weight, and once the standard classifier was given trace-normalized covariances it relied on the EOG channel too. The matched control changed overlap at the same time, but overlap has no evident route to channel reliance, so we attribute the ocular trap to trace normalization; that attribution is an inference, not a separate test.

The second candidate, overlap, is not supported: with overlapping windows the standard classifier's shuffled folds exceeded blocked folds by only 0.003. The method's dependence trap arose instead in its own nulls and within-state estimator (§3.2), which treated overlapping windows as exchangeable. The recording confound was not reproduced either, which places it most plausibly in the way the method's ratio compared two recordings against drift within one.

In hindsight the loss of alpha information was predictable. The method was built to be blind to power, and the alpha response to eye closure is a power effect. The design made the failure foreseeable, and the project did not foresee it. We report it as such rather than as a discovery. The incremental test (§3.8) found no evidence that, on the one real-data effect that survived the other controls, the geometry adds information beyond alpha power: it helped in 11 of 15 subjects but hurt sharply in the rest. What was never tested on real data is the claim that motivated the design: that transitions exist in which correlation structure changes while power does not, and that the geometry detects them better than a power detector. The only evidence for it is synthetic (§3.9), and there the pre-specified margin was not met.

### 4.2 Relation to prior work

The recording confound of §3.5 is a small-scale version of the block-design problem documented by Li et al. (2021), in which classes recorded in separate blocks were decoded from temporal and recording differences rather than from the stimuli. The dependence trap is the one Schroeder et al. (2025) measured for the standard classifier, and whose consequences for cross-validation Varoquaux et al. (2017) and Lemm et al. (2011) describe in general. What this record adds is the sequence: each trap produced a result that looked like validation, each was removed by a specific control, and the standard pipeline, on the same data, was more robust: for a design reason in the case of the eye channel, and because the method's own evaluation created the trap in the other cases.

### 4.3 Recommendations

1. **Localization windows must not be centred on the answer.** Report a centre-prior baseline and test with the transition at an off-centre or random position.
2. **Nulls and cross-validation must respect dependence.** Use circular-shift or block-permutation nulls, and blocked, chronological, run-wise or subject-wise folds. Report the fold construction, which was unclear in 8 of 19 surveyed studies.
3. **The unit of inference must be the subject.** When several recordings come from one person, test at the subject level and state the smallest attainable p-value.
4. **Ocular handling must be reported and tested** where conditions differ in eye movements: repeat the analysis without EOG and frontal channels, or after documented ocular artefact removal, and report both.
5. **When conditions are recorded separately, include a same-condition between-recording control and a scalar baseline** on the same channels with the same statistic. A geometric effect that a scalar reproduces more strongly is not evidence about geometry.

For pipelines that combine band-pass filtering with trace normalization, we add a sixth: run a relative band-power baseline on the unfiltered signal before interpreting any geometric effect.

### 4.4 Limitations

The standard-pipeline control covers one classifier on two corpora and cannot test centre bias, which applies only to localization. The matched control changed trace normalization and overlap together, so the attribution of the ocular trap to trace normalization rests on the mechanism of §4.1 rather than on a separate test. The channel-density test used the eyes-open/closed task, so whether denser montages change the sleep results is untested. The sleep analyses used two EEG channels, and several controls used few subjects (four for the method's sleep EOG analyses, fifteen for the eyes-open/closed controls); where the unit of inference does not allow more, results are reported descriptively. The survey is small, restricted to open-access studies, and single-coded; its counts describe reporting, and the Unclear codes make each count the lower end of a range. The method's failures are specific to its construction and are not evidence that SPD geometry is uninformative for EEG; Riemannian classifiers perform well in the settings they were designed for, and the standard-pipeline control is consistent with that.

## 5. Conclusions

A trace-normalized SPD geometry read through a geodesic change-point statistic appeared, at different times, to discriminate structural regimes, to track sleep stages and to localize transitions within a single recording. Each appearance was produced by an ordinary trap, and each was removed by a specific control. The standard Riemannian pipeline, run through the same controls, did not cross the pre-specified bars. Given the method's trace-normalized, overlapping covariances, it fell into the ocular trap and no other: trace normalization most plausibly explains the eye channel's dominance, while the remaining traps arose in how the method was evaluated. There was no reliable evidence that the geometry adds information beyond alpha power, and more channels did not rescue detection. Published studies often do not report enough to rule out two of the traps, which is reason to make the controls routine.

---

## Declarations

**Use of generative AI.** The analyses, code and text of the underlying project were developed with substantial assistance from a large language model (Claude, Anthropic), and this manuscript was drafted by that model on 27 September 2026 from the author's earlier drafts and experimental record. Several of the traps reported here were introduced and then caught within that process. The author reviewed the manuscript and takes full responsibility for its content. Readers are asked to re-run the archived analyses rather than rely on the reported numbers.

**CRediT authorship contribution statement.** João Vitor Perazzolo: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Writing – review and editing, Visualization.

**Ethics.** The study used only publicly available, de-identified data. No ethical approval was required.

**Data and code availability.** Data are available from PhysioNet. Code, analysis plans and raw results are available in the author's repository, https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK- (`experiments/paper3_geodesic_kinematics/`, `experiments/_results/`; pre-registration of the §2.6 analyses `fbe4b6f`, results `46b168f`).

**Competing interests.** None.

**Funding.** This research received no specific grant.

---

## References

Adams, R. P., & MacKay, D. J. C. (2007). Bayesian online changepoint detection. arXiv:0710.3742.

Barachant, A., Bonnet, S., Congedo, M., & Jutten, C. (2012). Multiclass brain–computer interface classification by Riemannian geometry. *IEEE Transactions on Biomedical Engineering, 59*(4), 920–928.

Barachant, A., Bonnet, S., Congedo, M., & Jutten, C. (2013). Classification of covariance matrices using a Riemannian-based kernel for BCI applications. *Neurocomputing, 112*, 172–178.

Barachant, A., Barthélemy, Q., et al. (n.d.). *pyRiemann* (Version 0.12) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.593816

Bhatia, R. (2007). *Positive definite matrices*. Princeton University Press.

Chen, Y., Wiesel, A., Eldar, Y. C., & Hero, A. O. (2010). Shrinkage algorithms for MMSE covariance estimation. *IEEE Transactions on Signal Processing, 58*(10), 5016–5029. https://doi.org/10.1109/TSP.2010.2053029

Congedo, M., Barachant, A., & Bhatia, R. (2017). Riemannian geometry for EEG-based brain–computer interfaces: A primer and a review. *Brain-Computer Interfaces, 4*(3), 155–174.

Goldberger, A. L., Amaral, L. A. N., Glass, L., Hausdorff, J. M., Ivanov, P. Ch., Mark, R. G., et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. *Circulation, 101*(23), e215–e220. https://doi.org/10.1161/01.CIR.101.23.e215

Hurlbert, S. H. (1984). Pseudoreplication and the design of ecological field experiments. *Ecological Monographs, 54*(2), 187–211. https://doi.org/10.2307/1942661

Kemp, B., Zwinderman, A. H., Tuk, B., Kamphuisen, H. A. C., & Oberye, J. J. L. (2000). Analysis of a sleep-dependent neuronal feedback loop: The slow-wave microcontinuity of the EEG. *IEEE Transactions on Biomedical Engineering, 47*(9), 1185–1194. https://doi.org/10.1109/10.867928

Lemm, S., Blankertz, B., Dickhaus, T., & Müller, K.-R. (2011). Introduction to machine learning for brain imaging. *NeuroImage, 56*(2), 387–399. https://doi.org/10.1016/j.neuroimage.2010.11.004

Li, R., Johansen, J. S., Ahmed, H., Ilyevsky, T. V., Wilbur, R. B., Bharadwaj, H. M., & Siskind, J. M. (2021). The perils and pitfalls of block design for EEG classification experiments. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 43*(1), 316–333. https://doi.org/10.1109/TPAMI.2020.2973153

Pennec, X., Fillard, P., & Ayache, N. (2006). A Riemannian framework for tensor computing. *International Journal of Computer Vision, 66*(1), 41–66.

Pernet, C., Garrido, M. I., Gramfort, A., Maurits, N., Michel, C. M., Pang, E., et al. (2020). Issues and recommendations from the OHBM COBIDAS MEEG committee for reproducible EEG and MEG research. *Nature Neuroscience, 23*(12), 1473–1483. https://doi.org/10.1038/s41593-020-00709-0

Pollard, T., Moody, B. E., Lehman, L.-W. H., Gow, B. J., Fernandes, C., Xie, C., et al. (2026). PhysioNet as a global platform for biomedical research. *Nature Health, 1*(8), 792–795. https://doi.org/10.1038/s44360-026-00096-z

Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A general-purpose brain–computer interface (BCI) system. *IEEE Transactions on Biomedical Engineering, 51*(6), 1034–1043.

Schroeder, F., Fairclough, S., Dehais, F., & Richins, M. (2025). The impact of cross-validation choices on pBCI classification metrics: Lessons for transparent reporting. *Frontiers in Neuroergonomics, 6*, 1582724. https://doi.org/10.3389/fnrgo.2025.1582724

Truong, C., Oudre, L., & Vayatis, N. (2020). Selective review of offline change point detection methods. *Signal Processing, 167*, 107299.

Varoquaux, G., Raamana, P. R., Engemann, D. A., Hoyos-Idrobo, A., Schwartz, Y., & Thirion, B. (2017). Assessing and tuning brain decoders: Cross-validation, caveats, and guidelines. *NeuroImage, 145*, 166–179. https://doi.org/10.1016/j.neuroimage.2016.10.038
