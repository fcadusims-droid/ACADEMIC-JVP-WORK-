# Does an Interoceptive Signal Mark the Transitions a Person Survives? Data Requirements, and a Failed Estimability Gate on Public Post-Cardiac-Arrest Recordings

João Vitor Perazzolo

27 September 2026

**Article type:** Empirical article

**Keywords:** heart-rate variability; time irreversibility; surrogate data; cardiac arrest; negative results

---

## Take-home message

Testing whether a bodily signal marks transitions a person survives, not transitions generally, needs concurrent neural and cardiac recordings, a matched recovery/non-recovery contrast and long records. One public corpus has all three. On it, a pre-specified heart-period nonlinearity gate found structure in 6 of 21 patients, below its 60% bar.

## Abstract

Physiological signals change at transitions such as emergence from anaesthesia or recovery from coma, and some interoceptive signals modulate how the brain responds to external input. Whether any such signal carries information specific to transitions the person survives, as opposed to transitions in general, has not been tested, and it is not obvious what a test would require. This article states the requirements and reports the attempt to meet them with public data. A test needs three properties in the same records: a cardiac channel recorded concurrently with EEG; a contrast between transitions followed by recovery and transitions not followed by recovery, matchable on severity; and records long enough for a subsampling-robust estimate of distance to criticality, since near-critical dynamics is the leading rival explanation of structured transitional signals. A bounded audit of five families of public corpora found one that satisfies all three: the I-CARE post-cardiac-arrest database. The first pre-specified step, a check that the heart-period series carries nonlinear structure beyond linear surrogates, was met in 6 of 21 pilot patients (29%; 95% CI 14–50%), below a 60% bar, so the analysis stopped. The failure most plausibly reflects the known loss of heartbeat time irreversibility in disease, compounded by sedation, temperature management and vasopressors; because the gate lacked a positive control, it is uninformative until one is run. Simulation audits of the planned statistics are reported with the limits they impose on any future test.

## Purpose

The aim was to test whether a residual interoceptive signal, left after a strong model of ordinary physiology has absorbed what it can, predicts transitions after which a person recovers differently from transitions after which they do not, when the two are matched on their surface dynamics. The motivation is philosophical: debates about personal persistence contrast a person resuming her life with her not doing so, and it is an open question whether any physiological signal is sensitive to that contrast rather than to transitions as such. Before any such test, three things had to be settled: what data it needs, whether public data provide it, and whether the first precondition, a structured interoceptive signal, holds in those data. The article reports all three. The main test was not run, because the precondition failed at a threshold fixed in the analysis plan (§2.7 states what the record shows about when it was fixed). The article claims nothing about identity, consciousness or any mechanism of persistence.

## 1. Introduction

Interoceptive signals can gate the brain's response to external input. Spontaneous fluctuations in the cortical response to heartbeats predict whether a faint visual stimulus is detected (Park et al. 2014), and the cardiac cycle modulates somatosensory perception and evoked potentials (Al et al. 2020). The efficacy of an external perturbation in general depends on the state of the system it perturbs: the plasticity induced by transcranial magnetic stimulation depends on real-time EEG-defined excitability states (Zrenner et al. 2018). State-dependent efficacy is therefore an ordinary property of neural dynamics, not a marker of anything more specific.

This article asks a narrower question. Suppose a residual interoceptive signal, left after ordinary physiology has been modelled, predicts a state transition. Is its predictive value the same for transitions after which the person recovers and for transitions after which the person does not, when the two are matched on surface dynamics? A signal that tracks transitions generically should predict both alike. A signal whose predictive value depends on whether the person recovers would be tracking something about the contrast between recovery and non-recovery, which is the contrast that matters in debates about personal persistence. The article does not assume that such a signal exists, and it does not equate non-recovery with the loss of personal identity; that equation is a philosophical position the design would have to declare and defend.

The question is hard to test for three reasons. Recovery and non-recovery must be observed in comparable patients, which in practice means coma after cardiac arrest, where outcome is known and EEG is recorded for prognosis. Near-critical dynamics, for which there is evidence in cortical tissue (Beggs and Plenz 2003), generically produces structured, nonlinear transitional signals, so any test must control for the distance to criticality of the processes involved, and estimating that from spatially subsampled recordings requires long records and a subsampling-robust estimator (Wilting and Priesemann 2018). And the contrast between recovery and non-recovery is defined by outcome, so it is confounded with severity, which must be matched.

## 2. Methods

### 2.1 Data requirements

A test of the question requires three properties to hold simultaneously in the same records.

- **P1, concurrent substrate.** A cardiac channel (ECG, or a derived heart-period series) recorded simultaneously with EEG.
- **P2, contrast.** Transitions followed by recovery and transitions not followed by recovery, in patients who can be matched on severity and on the gross dynamics of the transition. Simulations of the planned dissociation statistic (§2.5, §3.3) show that false positives inflate with any mismatch in surface dynamics, from 0.05 with perfect matching to 0.16 at a mismatch of 0.3 standard deviations, so matching must be tight and audited.
- **P3, length.** Records long enough, with enough channels, for a multistep-regression estimate of the branching ratio (Wilting and Priesemann 2018).

### 2.2 Dataset audit

A bounded, documentation-level search was fixed before any dataset was inspected. It covered five families: anaesthesia banks with neuromonitoring and vital signs (VitalDB); intensive-care waveform banks (MIMIC-III/IV Waveform, eICU); sleep banks with ECG (Sleep-EDF, SHHS, MASS); seizure EEG corpora (TUH EEG, CHB-MIT); and post-cardiac-arrest coma corpora (I-CARE). For each candidate, the three properties and open access were assessed from its published documentation. The audit was run in July 2026 and repeated in September 2026. It is a directed search, not a systematic review, and a corpus outside these families could satisfy the requirements.

### 2.3 Corpus

The I-CARE database (Amorim et al. 2023a, 2023b; version 2.1) contains continuous EEG from comatose patients after cardiac arrest, with ECG where available. Its public training set covers 607 patients and more than 32,000 hours of EEG. Outcome is the Cerebral Performance Category at follow-up: good (CPC 1–2) or poor (CPC 3–5, from severe disability to death). In a sample of 60 patients, 45 (75%) had both ECG and EEG segments. The data are distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 licence.

### 2.4 The estimability gate

The planned analysis treated as its first precondition that the interoceptive signal carry structure beyond a linear Gaussian process, possibly observed through a static nonlinearity, which is the null that IAAFT surrogates represent. This precondition was tested first, with a stopping rule: if fewer than 60% of pilot patients showed such structure, the analysis would stop.

**Pilot set.** Patients were taken in the database's record order, targeting about 20. A patient was included if at least one ECG segment loaded and yielded at least 200 R-peaks.

**Signal.** R-peaks were detected with an adaptive Pan–Tompkins detector (Pan and Tompkins 1985). The heart-period (RR) series was resampled evenly at 4 Hz.

**Statistic.** Time-reversal asymmetry at lag one sample, $T = \langle d^3 \rangle / \langle d^2 \rangle^{3/2}$ with $d_t = x_{t+1} - x_t$, which is zero in expectation for a time-reversible process such as a linear Gaussian one.

**Null.** 200 iterative amplitude-adjusted Fourier-transform (IAAFT) surrogates per patient, which preserve the power spectrum and the amplitude distribution and destroy nonlinear phase structure (Schreiber and Schmitz 1996). A patient's series counted as structured if the observed statistic fell outside the surrogate distribution at two-sided p < 0.05.

**Decision.** Pass if the fraction of structured patients was at least 0.60.

Two features of the gate should be stated plainly. First, it was applied to the RR series itself, not to a residual left after a model of ordinary physiology. The plan justified this as the cleaner qualification of the observable's own structure. It is a different test: a signal can fail to be structured on its own and still leave a structured residual, or the reverse. Second, the gate had no positive control. It was not shown to pass on a population in which heart-period nonlinearity is expected.

### 2.5 Simulation audits of the planned statistics

Before the gate was run, the statistics planned for the later stages were audited on synthetic data. Two of them recur below. The *stratified gating differential* is the difference in the success rate of an external perturbation between moments when the interoceptive state is receptive and moments when it is not, contrasted with a placebo perturbation delivered without regard to that state. The *dissociation statistic* is the interaction between the interoceptive residual and the recovery/non-recovery class in predicting the transition. The models are low-dimensional and their units arbitrary; the audits establish properties of the statistics, not of physiology.

- **Common-generator subtraction.** A synthetic common driver acted on both a boundary proxy and an outcome variable, with or without a genuine gating coupling. The planned test regressed out a noisy measurement of the driver and tested the residual interaction against an autocorrelation-preserving block-permutation null.
- **Criticality.** A probabilistic branching network at the critical point, without gating, was compared with a gated counterpart on both statistics, varying read-out noise and the sign of feedback.
- **Branching-ratio estimation.** The naive lag-one estimator and the multistep-regression estimator were compared on short, subsampled, continuous traces.
- **Matching.** False-positive rates of the dissociation statistic were mapped over sample size, effect size and matching quality.
- **Residual-structure tests.** Two tests proposed for qualifying a residual were examined: a variance change-point test and a test for rotation of the eigenvectors of a delay-embedded covariance matrix.

### 2.6 Planned follow-up analyses

Four analyses are specified here, before they are run, to settle what the failed gate means.

- **Positive control.** The identical gate is applied to healthy young and elderly subjects of the Fantasia database (Iyengar et al. 1996). The gate is informative about I-CARE only if it passes in the healthy young group.
- **Beat-indexed, multiscale version.** The asymmetry statistic is recomputed on the beat-indexed RR series, without interpolation, at scales 1 to 10 beats, following the multiscale approach of Costa et al. (2005), with ectopic and artefactual beats removed, and judged against the same 0.60 bar. This addresses two weaknesses of the gate: interpolation at 4 Hz with a lag of one sample measures asymmetry over 0.25 s, and arrhythmia inflates the statistic.
- **Full pilot by outcome.** The beat-indexed statistic is compared between good-outcome and poor-outcome patients in a larger I-CARE sample of 50 patients per group. This is descriptive and does not test the dissociation.
- **Audit re-check.** The classification of the seizure corpora is re-checked against the files themselves, since many recordings in clinical EEG corpora include an ECG channel, and the available EEG signals in VitalDB are re-checked against its track list.

### 2.7 Provenance

The plans for the audit and the gate were written in the author's repository. For both, the plan and the result entered the repository in the same commit, so their order cannot be verified from the record. The R-peak detector was changed during the analysis. A fixed-threshold detector found 55 peaks in a 118-minute record and was replaced by the adaptive detector. Under the fixed-threshold detector the structured fraction had been 0.42, so the result under both detectors was computed. Both fall below the 0.60 bar, and the decision does not depend on the change.

## 3. Results

### 3.1 Dataset audit

One corpus satisfied all three properties (Table 1).

**Table 1.** Public corpora against the three data requirements, as assessed from documentation.

| Corpus | P1 concurrent EEG + cardiac | P2 recovery / non-recovery contrast | P3 length | Notes |
|---|---|---|---|---|
| I-CARE (post-cardiac-arrest) | yes, where ECG available | yes (CPC 1–2 vs 3–5) | yes | between-patient contrast; severity must be matched |
| VitalDB (surgical) | classified as no (processed depth index, not raw EEG) | no (almost all recover) | yes | EEG signals to be re-checked (R2.4) |
| MIMIC-III/IV Waveform (ICU) | no concurrent raw EEG | yes | yes | |
| Sleep-EDF, SHHS, MASS (sleep) | yes in SHHS and MASS | no (sleep is reversible) | yes | supplies only the recovery arm |
| TUH EEG, CHB-MIT (seizure) | classified as no; see §2.6 | no | yes | classification to be re-checked (R2.4) |

The contrast in I-CARE is between patients, not within a patient, and patients with good and poor outcomes differ systematically in their post-arrest EEG; that difference is the basis of EEG-based prognosis. Matching on surface dynamics is therefore demanding even where the contrast exists.

### 3.2 Estimability gate

Of 24 patients examined in record order, 3 had no segment long enough to yield 200 R-peaks. Of the remaining 21, 6 showed time-reversal asymmetry outside the IAAFT surrogate distribution (29%; Wilson 95% CI 14–50%), below the 0.60 bar. The analysis stopped, and the dissociation was not run. Three of the six structured series had |T| > 0.5, a magnitude more consistent with arrhythmia than with the asymmetry of normal heart-rate dynamics, so 29% may overstate the structured fraction.

### 3.3 Simulation audits

The audits constrain any future test more than the gate does.

**Common-generator subtraction.** Against a linearly acting common driver, the residual test kept a nominal false-positive rate and full power, provided the null preserved autocorrelation. A naive shuffle inflated false positives about threefold. Against a driver that itself carried an interaction term, the test produced false positives at a rate that grew with record length, reaching about 0.9 at the longest records simulated. The rate depended on how well the driver was measured: about 0.1 when the proxy captured 95% of the driver's variance, 0.3 at 89% and 0.6 at 75%. Subtracting the proxy's interaction term did not help. This is the time-series form of a known result: controlling for a confounder measured with error leaves residual confounding, and more data make spurious significance more likely (Westfall and Yarkoni 2016).

**Criticality.** A critical branching network without any gating reproduced the stratified gating differential in 15 of 24 parameter cells (62%), with magnitude matching or exceeding that of the gated network as criticality strengthened. A non-critical control returned a differential of about zero. Under a clean read-out with weak homeostatic feedback, the ungated network produced a differential of about −0.25, larger in magnitude than the +0.07 to +0.12 of the gated network, with sign set by what the read-out tracked. Neither a directional criterion nor generalization across network topologies separated the two, which is what critical universality predicts (Kinouchi and Copelli 2006). The dissociation statistic was more robust but not immune: at the strongest cell, the ungated network reached about 73% of the value produced by a signal that was genuinely class-dependent.

**Branching-ratio estimation.** On short subsampled traces, the naive lag-one estimator read a true branching ratio of 0.94 as about 0.79 and certified about 79% of near-critical systems as safely subcritical. The multistep-regression estimator read it as about 0.92, accepted about 90% of genuinely subcritical systems and rejected about 83% of near-critical ones, reproducing the bias reported by Wilting and Priesemann (2018).

**Matching.** Imperfect matching raised the false-positive rate of the dissociation statistic from 0.05 at perfect matching to 0.16 at a standardized mismatch of 0.3 and 0.35 at 0.6, independent of sample size. With matching at or below 0.3, a moderate effect (signal-to-noise ratio 0.8) required about 40 patients per condition for 80% power.

**Residual-structure tests.** Both proposed tests failed as discriminators. A variance change-point test on a residual computed against a model fitted before the transition detects any change of regime, because the model is misspecified afterwards. The eigenvector-rotation test is degenerate for a two-dimensional delay embedding. For a stationary series, the covariance of $(x_t, x_{t-\tau})$ has equal diagonal entries, so its eigenvectors are $(1, 1)/\sqrt{2}$ and $(1, -1)/\sqrt{2}$ whatever the signal. The principal axis sits at 45° when the autocovariance at lag $\tau$ is positive and at 135° when it is negative. The test is blind to amplitude, reports a 90° rotation whenever a change of frequency flips the sign of the lag-$\tau$ autocovariance, and is dominated by noise when that autocovariance is near zero. A simulation confirmed all three behaviours (Appendix A). Both tests were dropped from the protocol.

### 3.4 Follow-up analyses

[RESULTS R2.1–R2.4 — pending experiments E2.1–E2.4]

## 4. Discussion

The main test of this article could not be run. The one public corpus with the required contrast did not provide a structured interoceptive signal in most patients at the pre-specified threshold, and the analysis stopped as planned.

The failure was predictable. The time irreversibility of the heartbeat is highest in healthy young people and declines with age and heart disease (Costa et al. 2005). Comatose patients after cardiac arrest are older on average, have usually arrested because of heart disease, and are sedated, cooled and often on vasopressors. A low structured fraction in this population says little about interoceptive signals in general and nothing about the question the gate was meant to open. A literature check before the analysis would have predicted the result, and a positive control on healthy subjects should have been part of the gate. The follow-up analyses of §2.6 add both, and until they are run the failure should be read as uninformative about the instrument's sensitivity.

The simulation audits carry the more durable lessons. Any test of whether an interoceptive state gates the efficacy of a perturbation must contend with four facts. State-dependent efficacy is produced by critical dynamics without any gating mechanism (compare Kinouchi and Copelli 2006). Subtracting a common generator measured with error manufactures interactions, increasingly with more data (compare Westfall and Yarkoni 2016). Contrasts defined by outcome manufacture dissociations unless matching is tight. And distance to criticality, which must be controlled, is underestimated by naive estimators on subsampled data (Wilting and Priesemann 2018). None of these is new in isolation; together they set a bar that no available public dataset meets.

The conceptual limits of the question are as important as the empirical ones. The recovery/non-recovery contrast is between patients and defined by outcome, so it is confounded with severity. Treating non-recovery as a transition across which a person does not persist is a substantive philosophical position, not a clinical fact. And an interoceptive signal that gates perception is not thereby a signal of anything about the person beyond her physiological state. A future test would need a private cohort with a clean cardiac channel recorded before heavy sedation, concurrent raw EEG, outcome follow-up, and severity covariates sufficient for matching, together with an argument, which this article does not supply, for why an interoceptive signal is the right place to look.

## 5. Conclusion

A test of whether an interoceptive signal is specific to transitions a person survives requires concurrent EEG and cardiac recordings, a matched recovery/non-recovery contrast, and long records. One public corpus, I-CARE, has all three. On it, the first pre-specified step failed: heart-period nonlinearity exceeded linear surrogates in 6 of 21 patients, below a 60% bar. The failure is consistent with the known loss of heartbeat time irreversibility in disease, and the gate lacked a positive control that would show whether it can pass at all. Simulation audits show that state-dependent perturbation efficacy is produced by critical dynamics alone, that subtracting a noisily measured common generator manufactures interactions, and that outcome-defined contrasts manufacture dissociations unless matching is tight.

---

## Appendix A. Degeneracy of the Two-Dimensional Eigenvector-Rotation Test

Sinusoids were sampled at 100 Hz with additive Gaussian noise (standard deviation 0.3); AR(1) series had unit innovation variance. All series were embedded as $(x_t, x_{t-5})$. The angle of the leading eigenvector of the embedded covariance was computed before and after an imposed change.

| Change imposed | Angle before → after | Test output |
|---|---|---|
| Amplitude ×4, same frequency | 45.0° → 45.0° | no rotation |
| Sinusoid 3 Hz → 14 Hz | 45.0° → 135.1° | 90° "rotation" |
| AR(1) coefficient 0.5 → −0.5 | 42.9° → 135.1° | 90° "rotation" |
| AR(1) coefficient 0.5 → 0.95 | 59.1° → 45.0° | noise (lag-5 autocovariance near zero before) |

---

## Declarations

**Use of generative AI.** The analyses, code and text of the underlying project were developed with substantial assistance from a large language model (Claude, Anthropic), and this manuscript was drafted by that model on 27 September 2026 from the author's earlier drafts and experimental record. The simulation in Appendix A was run by the model. The author reviewed the manuscript and takes full responsibility for its content. [AUTHOR TO CONFIRM OR AMEND BEFORE SUBMISSION.]

**Data availability.** I-CARE and Fantasia are available from PhysioNet under their respective licences. Per-patient statistics, analysis plans and code are in the author's repository (`experiments/paper2_cbra_protocol/`, `experiments/_results/`). [LINK AND COMMIT HASH TO BE ADDED.]

**Ethics.** Only publicly available, de-identified data were analysed. No ethical approval was required.

**Competing interests.** None.

**Funding.** None.

---

## References

Al, E., Iliopoulos, F., Forschack, N., Nierhaus, T., Grund, M., Motyka, P., Gaebler, M., Nikulin, V. V., & Villringer, A. (2020). Heart–brain interactions shape somatosensory perception and evoked potentials. *Proceedings of the National Academy of Sciences, 117*(19), 10575–10584.

Amorim, E., Zheng, W., Ghassemi, M., et al. (2023a). The International Cardiac Arrest Research Consortium Electroencephalography Database. *Critical Care Medicine, 51*(12), 1802–1811. https://doi.org/10.1097/CCM.0000000000006074

Amorim, E., Zheng, W., Lee, J. W., Herman, S., Ghassemi, M., Sivaraju, A., Gaspard, N., Hofmeijer, J., van Putten, M. J. A. M., Reyna, M., Clifford, G., & Westover, B. (2023b). *I-CARE: International Cardiac Arrest REsearch consortium Database* (Version 2.1) [Data set]. PhysioNet. https://doi.org/10.13026/m33r-bj81

Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits. *Journal of Neuroscience, 23*(35), 11167–11177.

Costa, M., Goldberger, A. L., & Peng, C.-K. (2005). Broken asymmetry of the human heartbeat: Loss of time irreversibility in aging and disease. *Physical Review Letters, 95*, 198102. https://doi.org/10.1103/PhysRevLett.95.198102

Iyengar, N., Peng, C.-K., Morin, R., Goldberger, A. L., & Lipsitz, L. A. (1996). Age-related alterations in the fractal scaling of cardiac interbeat interval dynamics. *American Journal of Physiology–Regulatory, Integrative and Comparative Physiology, 271*(4), R1078–R1084. https://doi.org/10.1152/ajpregu.1996.271.4.R1078

Kinouchi, O., & Copelli, M. (2006). Optimal dynamical range of excitable networks at criticality. *Nature Physics, 2*(5), 348–351. https://doi.org/10.1038/nphys289

Pan, J., & Tompkins, W. J. (1985). A real-time QRS detection algorithm. *IEEE Transactions on Biomedical Engineering, 32*(3), 230–236.

Park, H.-D., Correia, S., Ducorps, A., & Tallon-Baudry, C. (2014). Spontaneous fluctuations in neural responses to heartbeats predict visual detection. *Nature Neuroscience, 17*(4), 612–618.

Schreiber, T., & Schmitz, A. (1996). Improved surrogate data for nonlinearity tests. *Physical Review Letters, 77*(4), 635–638.

Westfall, J., & Yarkoni, T. (2016). Statistically controlling for confounding constructs is harder than you think. *PLOS ONE, 11*(3), e0152719. https://doi.org/10.1371/journal.pone.0152719

Wilting, J., & Priesemann, V. (2018). Inferring collective dynamical states from widely unobserved systems. *Nature Communications, 9*, 2325.

Zrenner, C., Desideri, D., Belardinelli, P., & Ziemann, U. (2018). Real-time EEG-defined excitability states determine efficacy of TMS-induced plasticity in human motor cortex. *Brain Stimulation, 11*(2), 374–389.
