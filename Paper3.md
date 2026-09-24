# Five Ways an EEG Geometry Method Looked Validated and Was Not: A Pre-Registered Record, with Controls on the Field's Standard Pipeline and a Survey of Published Practice

João Vitor Perazzolo

September 23, 2026

## Table of Contents

**Abstract**

1. Why Report a Validation That Failed
2. The Method Under Test
3. Data, the Standard-Pipeline Control, and the Literature Survey
4. The Five Traps
   - 4.1 Centre Bias
   - 4.2 Nulls and Validation That Ignore Dependence
   - 4.3 Pseudo-Replication
   - 4.4 Ocular Contamination
   - 4.5 Confusion Between Recordings
   - 4.6 Summary
5. What Survives
6. Recommendations
7. Limitations
8. Conclusion

---

## Abstract

**What kind of paper this is.** This is a methodological negative. It reports how a geometric method for EEG — trace-normalized covariance matrices on the symmetric-positive-definite (SPD) manifold, read through a geodesic change-point statistic — passed a series of tests that later controls showed it had not passed. Every run was pre-registered before it was executed, and every control that overturned an earlier result is committed with its code. The paper does not offer the method for adoption. It offers the record of how it came to look validated, organized as five trap mechanisms. Each trap is reported with what it did to the result, the control that exposed it, whether the field's standard Riemannian pipeline falls into the same trap, and how often published studies leave it open.

**The five traps.** (1) *Centre bias*: every localization window was built symmetric about the true transition, so a detector that always guesses the middle scores every recording. Off-centre, the geometry's lead over a scalar band-power detector disappeared ($10/22$ versus $10/22$), and at twice the sample size a power analysis asked for, the scalar was ahead ($59/151$ versus $67/151$, not significant). (2) *Nulls and validation that ignore dependence*: permuting overlapping, autocorrelated windows as if they were exchangeable made an eyes-open/eyes-closed effect look significant in $14$ of $15$ subjects at a median ratio of about $3.3$; against the recording's own slow drift it is about $1.3$. (3) *Pseudo-replication*: seven sleep recordings were four people, so a record-level $p$ of $0.0078$ could not be matched at the subject level, where the smallest attainable one-sided $p$ is $0.0625$. (4) *Ocular contamination*: a sleep-staging association and an N2-versus-REM discrimination were carried by the horizontal-EOG channel in the covariance; without it, the geometry's association fell from $V=0.452$ to $0.021$. (5) *Confusion between recordings*: the one remaining real-data effect, eyes open versus closed, compares two separate recordings against the drift within one. It exceeds a same-state between-recording control only weakly, and per-channel relative alpha power separates the states more strongly than the geometry does.

**Are these traps of this method or of the field?** A pre-registered control ran the field's standard pipeline (covariance, then minimum distance to Riemannian mean, pyRiemann) through the four traps that apply to classification. **None of the four applied** on these data: the pipeline's accuracy barely moved without the EOG channel, did not "discriminate" two recordings of the same state above the pre-registered bar, and was not inflated by subject leakage or by shuffled validation. By the pre-registered rule, these are traps of *this method*, as used here. A pre-registered survey of 20 published covariance/Riemannian EEG studies qualifies that conclusion. Ocular handling was not reported in $7$ of $19$ studies where it applied, and $8$ more were unclear. Validation that ignored the dependence between trials or windows appeared in $4$ of $19$, with $8$ more unclear. One included study measured the dependence trap directly for the standard classifier, finding differences of up to $12.7$ % in accuracy between block-respecting and non-respecting cross-validation (Schroeder et al. 2025). The traps are therefore not properties of the standard pipeline on these data, but two of them are left open often enough in published practice that they cannot be treated as this method's alone.

**What survives.** A repair to the detection statistic (AUC $0.227 \to 0.813$), whose out-of-sample evidence for detecting a change of *state*, rather than of recording, is marginal. A base-metric result on synthetic data (a flat log-Euclidean metric removes a drift-versus-jump confusion). Nothing on real data that the method does better than a scalar baseline. The three-regime demarcation and the vector-bundle apparatus that the method was originally proposed with were never shown to work. They are set out in a separate draft, not here.

**Keywords:** EEG; covariance matrices; Riemannian geometry; SPD manifold; change-point detection; validation; cross-validation; pseudo-replication; ocular artifacts; negative results; pre-registration.

---

## 1. Why Report a Validation That Failed

A method can look validated for reasons that have nothing to do with whether it works. The reasons are rarely exotic. A window is placed where the answer is. A permutation null treats dependent samples as independent. Two nights of one person are counted as two people. An eye channel carries the effect. Two recordings differ because they are two recordings. Each of these is well known in the abstract (Hurlbert 1984; Lemm et al. 2011; Varoquaux et al. 2017), and each is easy to miss in a particular analysis, because the surrounding work looks careful.

This paper is the record of one method that fell into all five, in turn, and was pulled out of each by a pre-registered control. The method is not new in its ingredients. Covariance matrices on the SPD manifold have been used to classify EEG for more than a decade (Barachant et al. 2012, 2013; Congedo et al. 2017). What it added was a *single-trajectory* reading: a geodesic change-point statistic on a sequence of trace-normalized covariances, intended to localize and characterize a transition within one continuous recording. The motivating claim was that trace normalization makes the geometry blind to overall power and sensitive to the *structure* of spatial correlation, so that it would register structural transitions a power-based detector misses.

That claim did not survive. What makes the record worth reporting is how many times it *appeared* to survive, and why. Two further questions decide whether the record matters beyond this method. Does the field's standard pipeline fall into the same traps? And how often do published studies leave them open? Both were answered by pre-registered analyses (§3), and the answers are mixed (§4.6).

Every result cited here is a committed pre-registration, script and `result.json` in the accompanying repository. Where a later control overturned an earlier result, both are committed, and the earlier one is marked as withdrawn rather than removed.

## 2. The Method Under Test

**Representation.** A multichannel signal is cut into short overlapping windows. Each window's channel covariance matrix is floored at a small eigenvalue and divided by its trace, so that it lies on the manifold of unit-trace SPD matrices. Trace normalization removes the overall power scale: two windows that differ only by a gain factor map to the same point. The matrices are compared under the square-root (Bures-type) metric, in which $\rho \mapsto \sqrt{\rho}$ embeds the unit-trace SPD matrices in a sphere, and geodesic distance is the arc length between the embedded points (Bhatia 2007; see also Pennec et al. 2006 for the affine-invariant alternative).

**Detection and localization.** The windows' embedded coordinates are accumulated in a multivariate CUSUM. The change point is the argmax of the CUSUM curve. A detection statistic, the scale-normalized peak of that curve, decides whether a transition is present at all (§5).

**Discrimination.** To ask whether two states differ, the distance between the two states' mean geometries is divided by a within-state distance: the distance between the first-half and second-half means of each state (the *temporal-half* estimator), or, in an earlier version, the median distance between random interleaved halves (the *permutation* estimator). A ratio above one was read as "the states differ by more than each drifts".

**What the original proposal added, and why it is not tested here.** The method was first proposed as a much larger construction. A vector bundle carried a cross-scale coupling in its fibre, a jump-diffusion model governed the tangent flow, and three "regimes" (geodesic drift, isotropic dispersion, structural rank collapse) were to be demarcated by Lyapunov and statistical-complexity criteria. None of this survived contact with data. A pre-registered ablation found the fibre net negative: adding it lowered the discrimination ratio at both scalings tried. A pre-registered gate found the three-regime demarcation not externally falsifiable as defined: no corpus supplies an independent label, so the label would be the method's own output. The full construction is preserved in the repository (`drafts/paper3_protocol_full_2026-09-23.md`) as an unvalidated proposal. This paper is about the part that was tested: the trace-normalized SPD base and its CUSUM.

## 3. Data, the Standard-Pipeline Control, and the Literature Survey

**Data.** Two public PhysioNet corpora (Goldberger et al. 2000):
- The EEG Motor Movement/Imagery database (Schalk et al. 2004). Its one-minute eyes-open (R01) and eyes-closed (R02) baselines, and the rest (T0) intervals of its task runs, were used, in 15 subjects, on seven occipito-parietal channels in the alpha band.
- The Sleep-EDF sleep-cassette recordings (Kemp et al. 2000), on Fpz-Cz, Pz-Oz and horizontal EOG. The number of recordings varies by test, from seven cached recordings in early runs to all 153 in the last.

**The standard-pipeline control (`mdm_trap_control`).** To separate traps of this method from traps of the field, the field's standard classifier was put through the same controls. That classifier is covariance estimation with OAS shrinkage (Chen et al. 2010) followed by minimum distance to Riemannian mean (Barachant et al. 2012), as implemented in pyRiemann 0.12 (Barachant et al., pyRiemann). The criteria and the framing rule were fixed before the run (§4.6).

**The literature survey (`trap_literature_survey`).** Also pre-registered: a fixed Europe PMC query for open-access EEG studies using covariance or Riemannian/SPD features, 2012–2025. The first 20 eligible studies were taken in relevance order, with 7 screened out on the way, for example fNIRS-only or MEG-only studies, or studies with no covariance features in their own pipeline. Each trap was coded Yes (left open), No (addressed), Unclear or not applicable, by rules fixed in advance, and every code is committed with the sentence that supports it. There was one coder and no second rater, and only open-access papers were included (§7).

## 4. The Five Traps

### 4.1 Centre Bias

**Mechanism.** To test whether a detector localizes a transition, one cuts a window around it. If the window is symmetric about the transition, the right answer is always the centre, and any detector with a central tendency is rewarded for it.

**What it did here.** Every localization analysis in the project built its window symmetric about the known transition. A detector that always predicts the window centre scores every recording under that construction ($22/22$) and none once the transition is moved off-centre ($0/22$). The inflation mattered for the one comparison that favoured the method:
- Centred, the geodesic CUSUM led a scalar band-power CUSUM, $14/22$ against $9/22$ (McNemar $p = 0.227$, already not significant).
- Off-centre, they tied at $10/22$ versus $10/22$.
- On sleep onset, the geometry's $10/15$ in centred windows fell to $4/7$ off-centre on the recordings available for that check, tying the scalar's $4/7$.
- A pre-registered power-up on all $151$ usable sleep-cassette recordings ($78$ subjects), off-centre, with the detectors unchanged, then settled the comparison. The geodesic CUSUM localized $59/151$ and the scalar band-power CUSUM $67/151$ (McNemar $p\approx 0.38$). At subject level the counts were $32/78$ against $42/78$, and without the EOG channel $57/151$ against $66/151$. The pre-registered verdict is *inconclusive*, but at about twice the planned sample and with the direction favouring the scalar, the geometry does not improve on the scalar for sleep-transition localization.
- The benchmark against six standard change-point algorithms had placed the geodesic CUSUM at $10/15$ versus $8/15$ for the best baseline. That margin was inside binomial noise even before the centring was found, and the counts come from centred windows.

**Standard pipeline and literature.** Centre bias applies to localization, not to classification, so neither the MDM control nor the survey could test it. No study in the survey localized a transition in time.

### 4.2 Nulls and Validation That Ignore Dependence

**Mechanism.** Overlapping or adjacent windows of one recording are strongly autocorrelated. A permutation null that shuffles them as if exchangeable, or a cross-validation that assigns them to train and test at random, measures the effect against sampling noise alone. Almost any two stretches of signal then look different.

**What it did here.** Two results were inflated this way.
- The eyes-open/eyes-closed discrimination was first reported with a permutation estimator of within-state distance. On that estimator the ratio exceeded unity in $14$ of $15$ subjects at a median of about $3.3$. Because the permutation cancels the slow drift within a state, the estimator would flag almost any two recordings as different. Measured against each recording's own first-half-to-second-half drift instead, the median ratio is about $1.3$, above unity in $12$ of $15$ subjects (cross-subject Wilcoxon $p\approx 0.008$).
- An association between a geometric volatility proxy and sleep staging was first tested against an i.i.d. label-shuffle null whose $95$th percentile was $0.003$. Against a circular-shift null that preserves autocorrelation, the $95$th percentile is $0.171$.

The association ($V = 0.452$) survived the corrected null, only to fall to trap 4. A third result, an N2-versus-REM discrimination, was re-tested under a circular-shift null and survived it on all seven recordings checked; it is the discrimination §4.4 attributes to the EOG channel. The trap does not always change the verdict, but the corrected null always has to be run to know.

**Standard pipeline.** Within-recording N2-versus-REM classification (on Fpz-Cz, Pz-Oz and EOG) with shuffled folds exceeded contiguous (blocked) folds by a median of only $0.009$ over $151$ recordings, below the pre-registered $0.05$. So the trap did not apply to the standard pipeline on this task.

**Literature.** Validation that ignored dependence (random k-fold over trials or windows of one recording) was coded Yes in $4$ of $19$ studies where it applied, with $8$ Unclear because the fold construction was not described. One included study measured the effect directly for the standard classifier on block-design n-back data: accuracy differed by up to $12.7$ % between cross-validation that respected the block structure and cross-validation that did not (Schroeder et al. 2025). Whether the trap bites depends on the design. Sleep stages that alternate across a night are protected; conditions recorded in blocks are not.

### 4.3 Pseudo-Replication

**Mechanism.** Two recordings of one person are not two independent observations. Counting them as two inflates the effective sample (Hurlbert 1984).

**What it did here.** Sleep-EDF names its sleep-cassette files by subject and night. The seven recordings behind the sleep-staging association were four people. The record-level one-sided Wilcoxon $p$ of $0.0078$ therefore has no subject-level counterpart: with four subjects, the smallest attainable one-sided $p$ is $0.0625$. No significance claim was possible at the correct unit.

**Standard pipeline.** Pooled MDM classification, cross-validated with recordings as groups (so a subject's two nights could fall in train and test) and with subjects as groups, differed by $0.001$ in accuracy. The trap did not apply to the standard pipeline's accuracy on this task.

**Literature.** Pseudo-replication was coded Yes in $0$ of $9$ studies where it applied, with $4$ Unclear. Most BCI studies evaluate within subject, where the trap does not arise.

### 4.4 Ocular Contamination

**Mechanism.** If an eye-movement channel, or a frontal channel near the eyes, is in the covariance, and the conditions differ in eye movements, the "state" signal can be the eye.

**What it did here.** The sleep covariance included the horizontal-EOG channel, and REM is defined in part by rapid eye movements.
- The geometric volatility's association with AASM staging ($V = 0.452$) fell to $0.021$ without the EOG channel. EOG power alone bound more strongly ($V = 0.524$).
- An N2-versus-REM discrimination that had passed in $14$ of $15$ recordings held, without the EOG channel, in only $2$ of $4$ subjects on the recordings available for the check, against $4$ of $4$ with it.

In these channels, the signal was EOG. The EEG-only covariance here is a $2\times 2$ matrix, roughly one correlation and one variance ratio after normalization. So the result licenses "in these channels the signal was the eye", not "the geometry fails" in general.

**Standard pipeline.** Removing the EOG channel from within-record MDM classification of N2 versus REM lowered the median subject-level accuracy by only $0.007$, below the pre-registered $0.05$. The standard classifier on this task did not depend on the eye channel. The difference from our result is instructive. Our statistics were built to be blind to power and so leaned on correlation structure, where the EOG channel dominates. The classifier uses the full covariance and has other information available.

**Literature.** Ocular handling was not reported, in studies whose conditions plausibly differ in eye movements, in $7$ of $19$ studies where it applied, with $8$ Unclear. Examples of the No code, where ocular handling was reported: ICA removal of blink and saccade components, rejection of trials on EOG thresholds, or explicit exclusion of EOG channels.

### 4.5 Confusion Between Recordings

**Mechanism.** If each condition is recorded in its own run, "condition" and "recording" are the same variable. Impedance drift, a re-seated cap and elapsed time all differ between recordings. A statistic that compares two recordings in its numerator against variability *within* one recording in its denominator will call any two recordings different.

**What it did here.** The last real-data effect standing was eyes open versus eyes closed: the distance between the two recordings' mean geometries exceeds each recording's own drift in $12$ of $15$ subjects (median ratio $\approx 1.3$). The eyes-open and eyes-closed baselines are separate runs. A pre-registered control computed the same statistic on two separate recordings of the *same* state: the rest (T0) intervals of two task runs, whose occipital alpha power is consistent with eyes open in $14$ of $15$ subjects.
- The eyes-open/closed ratio exceeded that control in $11$ of $15$ subjects (control median $0.95$, one-sided Wilcoxon $p\approx 0.024$). The control is biased in the method's favour: its windows span about $61$ s against $26$ s, which inflates its denominator.
- A scalar baseline on the same channels and the same statistic — the per-channel relative alpha power — separated the two states far more strongly (median ratio $\approx 3.5$, paired Wilcoxon $p\approx 10^{-4}$).

The geometry therefore separates the states less strongly than per-channel alpha power. Whether it carries *any* information beyond alpha power was not tested; that would need an incremental comparison of the scalar alone against the scalar plus the geometry.

The same asymmetry was then found in the method's one out-of-sample success. The detection statistic had been validated on segments that spliced the eyes-open and eyes-closed runs, against null segments inside one run, at AUC $0.82$. Rebuilt on a common chunk structure, the statistic separates a change of state from a same-state change of recording at AUC $0.72$ (bar $0.70$, uncertainty about $\pm 0.1$ at $n = 15$). But a change of recording alone, with no change of state, fires it at AUC $0.74$ against segments within one recording.

**Standard pipeline.** Blocked-CV MDM classification of the two same-state recordings (T0 of R03 against T0 of R07) reached a median balanced accuracy of $0.65$, against $0.87$ for eyes open versus closed. That is below the pre-registered $0.70$, so by the rule the trap does not apply. But it is above chance: the standard pipeline also tells two recordings of one state apart to some degree, and a study that recorded each class in its own run would have no way to know how much of its accuracy that accounts for.

**Literature.** Classes confounded with recordings were coded Yes in $1$ of $17$ studies where the trap applied. In that study the two classes came from two different public datasets. Most BCI paradigms interleave conditions within runs, which protects them.

### 4.6 Summary

| Trap | What it did to this method | Control that exposed it | Standard pipeline (MDM) | Published studies left open |
|---|---|---|---|---|
| Centre bias | lead $14/22$ vs $9/22$ $\to$ tie $10/22$ vs $10/22$; $59/151$ vs $67/151$ at scale | off-centre windows; power-up | not applicable | not applicable (no localization studies) |
| Dependence ignored | ratio $\approx 3.3$ ($14/15$) $\to$ $\approx 1.3$; null 95th pct $0.003 \to 0.171$ | temporal-half estimator; circular-shift null | does not apply (+0.009) | $4/19$ ($8$ unclear); up to $12.7$ % in block designs (Schroeder et al. 2025) |
| Pseudo-replication | record-level $p = 0.0078$ with 4 subjects; best attainable $0.0625$ | subject as unit | does not apply (+0.001) | $0/9$ ($4$ unclear) |
| Ocular contamination | $V$ $0.452 \to 0.021$ without EOG | EOG ablation | does not apply (drop 0.007) | $7/19$ ($8$ unclear) |
| Recording confound | ratio exceeds a same-state control only weakly; alpha power stronger; detection AUC $0.74$ for a recording change alone | same-state between-recording controls | does not apply by the $0.70$ bar ($0.65$, above chance) | $1/17$ |

The pre-registered framing rule gives **traps of this method**: none of the four applicable traps moved the standard pipeline past its bar on these data. The survey qualifies the rule. Two of the traps — ocular handling and dependence-respecting validation — are left open or unreported in a large share of published studies. Another group has measured the dependence trap directly for the standard classifier (Schroeder et al. 2025). And the standard pipeline's $0.65$ on two same-state recordings shows the recording confound is not zero for it either. A fair summary is that this method fell into all five traps because of how it was built and tested — a power-blind statistic, symmetric windows, exchangeable-window nulls, an EOG channel in a small covariance, and a ratio that compared recordings against within-recording drift. The field's standard pipeline is more robust on the same data, but the practices that would expose these traps are not reported often enough to assume they are routinely checked.

## 5. What Survives

- **A repair to the detection statistic.** The original confidence statistic, peak-to-median of the CUSUM curve, scored AUC $0.227$ on sleep-onset detection: worse than chance, because a driftless random walk inflates a ratio whose denominator is the median. A scale-normalized peak lifted detection to AUC $\mathbf{0.813}$ with localization unchanged. Applied unchanged to a paradigm not used to select it, it held at AUC $0.824$, while the old statistic fell below chance again ($0.434$). §4.5 bounds what that held-out result shows: part of it is a change of recording, and the evidence for detecting a change of state is marginal.
- **A base-metric result, on synthetic data only.** Under the square-root metric, a weak structural collapse and a strong geodesic drift were confusable: worst-corner AUC $0.6525$. Under a flat log-Euclidean metric, which has no holonomy, the same corner reached AUC $0.9597$. This locates the confusion in the curvature of the square-root embedding. It has not been shown on real data.
- **A benchmark position.** As a detector the geodesic CUSUM was competitive but not superior: detection AUC $0.81$ after the repair, fourth of nineteen method-feature combinations, against the best baseline's $0.88$. On a synthetic structural transition at constant power it localized perfectly ($1.00$) against the best power-feature baseline's $0.75$. That $+0.25$ margin falls short of the $+0.30$ fixed in advance, so it is not established at the pre-registered level. On the mirror scenario, a pure power change, it scored $0.55$ against $1.00$, as its construction requires.

Nothing on real data that this method does better than a scalar baseline survived.

## 6. Recommendations

These follow from the record, and each has a direct test.

1. **Localization windows must not be centred on the answer.** Report a centre-prior baseline, and test with the transition off-centre or at a random position in the window.
2. **Nulls and cross-validation must respect the dependence in the data.** Use circular-shift or block-permutation nulls, and blocked, chronological, run-wise or subject-wise folds. Report the fold construction; in the survey it was unclear in $8$ of $19$ studies.
3. **The unit of inference must be the subject.** When several recordings come from one person, test at the subject level and state the smallest attainable $p$.
4. **Ocular handling must be reported, and tested where conditions differ in eye movements.** Re-run the analysis without the EOG and frontal channels, or after documented ocular removal, and report both.
5. **When conditions are recorded separately, a same-condition between-recording control is needed.** Also run a scalar baseline on the same channels with the same statistic. A geometric effect that a scalar reproduces more strongly is not evidence about geometry.
6. **Pre-register, and commit the controls that overturn a result alongside the result.** In this record the earlier, inflated numbers are what a reader most needs to see beside the corrected ones.

## 7. Limitations

- **The standard-pipeline control covers one classifier on two corpora.** It tests the traps in the form they take for classification; centre bias could not be tested this way.
- **The survey is small, open-access only, and single-coder.** Many codes are Unclear because studies do not describe what would be needed to code them. The counts describe reporting as much as practice.
- **The method's failures are specific to its construction.** They are not evidence that SPD geometry is uninformative for EEG. Riemannian classifiers work well in the settings they were designed for, and the standard-pipeline control is consistent with that.
- **Several controls use few subjects** (4 for the sleep EOG analyses, 15 for the eyes-open/closed controls), and are reported as descriptive where the unit of inference does not allow more.
- **AI assistance.** The analyses and much of the code and text of the underlying project were developed with substantial assistance from a generative AI model, as disclosed in the repository. The traps reported here were, in several cases, introduced and then caught within that process. Readers are asked to re-run the committed experiments rather than rely on the numbers as reported.

## 8. Conclusion

A trace-normalized SPD geometry read through a geodesic change-point statistic looked, at different times, like a structural-regime discriminator, a sleep-staging tracker and an on-line localizer. Each appearance was produced by one of five ordinary traps, and each was removed by a pre-registered control. The field's standard Riemannian pipeline, run through the same controls on the same data, did not fall into four of them. Published studies, however, leave two of them unreported or open often enough that the controls should be routine. The contribution is the record: what each trap did, the control that exposed it, and the numbers before and after.

---

## Data and Code Availability

Every analysis cited is a committed pre-registration, script and result in the accompanying repository (`experiments/paper3_geodesic_kinematics/` and `experiments/_results/`). The key controls are:

- `localization_centerbias_control` and `h1_powerup_offcentre` (centre bias);
- `eeg_reconciliation`, `regime_referent_nulls` and `discrimination_null_dependence_audit` (dependence);
- `regime_referent_eog_control` and `discrimination_eog_ablation` (ocular);
- `between_recording_control` and `detection_between_recording_control` (recording confound);
- `mdm_trap_control` (standard pipeline);
- `trap_literature_survey` (literature, with every code and its supporting quotation).

The data are public (PhysioNet).

## References

Adams, Ryan P., and MacKay, David J. C. 2007. "Bayesian Online Changepoint Detection." arXiv:0710.3742. (The standard Bayesian online change-point method; a baseline in the benchmark.)
Barachant, Alexandre, Bonnet, Stephane, Congedo, Marco, and Jutten, Christian. 2012. "Multiclass Brain-Computer Interface Classification by Riemannian Geometry." *IEEE Transactions on Biomedical Engineering* 59(4): 920-928.
Barachant, Alexandre, Bonnet, Stephane, Congedo, Marco, and Jutten, Christian. 2013. "Classification of Covariance Matrices Using a Riemannian-Based Kernel for BCI Applications." *Neurocomputing* 112: 172-178.
Barachant, Alexandre, Quentin Barthélemy, et al. "pyRiemann." Software, version 0.12. Zenodo. DOI: 10.5281/zenodo.593816.
Bhatia, Rajendra. 2007. *Positive Definite Matrices*. Princeton University Press.
Chen, Yilun, Ami Wiesel, Yonina C. Eldar, and Alfred O. Hero. 2010. "Shrinkage Algorithms for MMSE Covariance Estimation." *IEEE Transactions on Signal Processing* 58(10): 5016-5029. DOI: 10.1109/TSP.2010.2053029.
Congedo, Marco, Barachant, Alexandre, and Bhatia, Rajendra. 2017. "Riemannian Geometry for EEG-Based Brain-Computer Interfaces: A Primer and a Review." *Brain-Computer Interfaces* 4(3): 155-174.
Goldberger, Ary L., Luis A. N. Amaral, Leon Glass, Jeffrey M. Hausdorff, Plamen Ch. Ivanov, Roger G. Mark, et al. 2000. "PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals." *Circulation* 101(23): e215-e220. DOI: 10.1161/01.CIR.101.23.e215.
Hurlbert, Stuart H. 1984. "Pseudoreplication and the Design of Ecological Field Experiments." *Ecological Monographs* 54(2): 187-211. DOI: 10.2307/1942661.
Kemp, Bob, Aeilko H. Zwinderman, Bert Tuk, Hilbert A. C. Kamphuisen, and Josefien J. L. Oberye. 2000. "Analysis of a Sleep-Dependent Neuronal Feedback Loop: The Slow-Wave Microcontinuity of the EEG." *IEEE Transactions on Biomedical Engineering* 47(9): 1185-1194. DOI: 10.1109/10.867928. (The Sleep-EDF data.)
Lemm, Steven, Benjamin Blankertz, Thorsten Dickhaus, and Klaus-Robert Müller. 2011. "Introduction to Machine Learning for Brain Imaging." *NeuroImage* 56(2): 387-399. DOI: 10.1016/j.neuroimage.2010.11.004.
Pennec, Xavier, Fillard, Pierre, and Ayache, Nicholas. 2006. "A Riemannian Framework for Tensor Computing." *International Journal of Computer Vision* 66(1): 41-66.
Schalk, Gerwin, McFarland, Dennis J., Hinterberger, Thilo, Birbaumer, Niels, and Wolpaw, Jonathan R. 2004. "BCI2000: A General-Purpose Brain-Computer Interface (BCI) System." *IEEE Transactions on Biomedical Engineering* 51(6): 1034-1043. (The EEG Motor Movement/Imagery database.)
Schroeder, Felix, Stephen Fairclough, Frederic Dehais, and Matthew Richins. 2025. "The Impact of Cross-Validation Choices on pBCI Classification Metrics: Lessons for Transparent Reporting." *Frontiers in Neuroergonomics* 6: 1582724. DOI: 10.3389/fnrgo.2025.1582724.
Truong, Charles, Oudre, Laurent, and Vayatis, Nicolas. 2020. "Selective Review of Offline Change Point Detection Methods." *Signal Processing* 167: 107299. (The `ruptures` library: PELT, binary segmentation, windowed methods.)
Varoquaux, Gaël, Pradeep Reddy Raamana, Denis A. Engemann, Andrés Hoyos-Idrobo, Yannick Schwartz, and Bertrand Thirion. 2017. "Assessing and Tuning Brain Decoders: Cross-Validation, Caveats, and Guidelines." *NeuroImage* 145: 166-179. DOI: 10.1016/j.neuroimage.2016.10.038.
