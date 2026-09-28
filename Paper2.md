# Does an Interoceptive Signal Mark the Transitions a Person Survives? Data Requirements, and an Estimability Gate Reversed on Audit, in Public Post-Cardiac-Arrest Recordings

João Vitor Perazzolo

27 September 2026

**Article type:** Empirical article

**Keywords:** heart-rate variability; time irreversibility; surrogate data; cardiac arrest; pre-registration

---

## Take-home message

Testing whether a bodily signal marks transitions a person survives needs concurrent neural and cardiac recordings, a matched recovery/non-recovery contrast and long records. One public corpus has all three. Its first gate failed as executed, but the executed statistic departed from the plan; as planned, the gate passes.

## Abstract

Physiological signals change at transitions such as emergence from anaesthesia or recovery from coma, and some interoceptive signals modulate how the brain responds to external input. Whether any such signal carries information specific to transitions the person survives, rather than to transitions in general, has not been tested. This article states what a test requires and tries to meet those requirements with public data. A test needs, in the same records, a cardiac channel recorded concurrently with EEG; a contrast between transitions followed and not followed by recovery, matchable on severity; and records long enough for a subsampling-robust estimate of distance to criticality, since near-critical dynamics can mimic the effect. A bounded audit of public corpora found one that satisfies all three: the I-CARE post-cardiac-arrest database. The first planned step, a check that the heart-period series carries nonlinear structure beyond linear surrogates in at least 60% of patients, was met in 6 of 21 as executed, and the analysis stopped. An audit found that the executed statistic departed from the written plan. As written, the check is met in 16 of 21 patients (76%); a multiscale version specified before it was run is met in 15 of 21 (71%); and a positive control passes in healthy young adults under both versions (19 and 17 of 20). The stop was an artefact of the deviation. Outcome groups differ markedly in age and arrest rhythm, so matching, not estimability, is the binding constraint. Simulation audits of the planned statistics set further limits.

## Purpose

The aim was to test whether a residual interoceptive signal, left after a strong model of ordinary physiology has absorbed what it can, predicts transitions after which a person recovers differently from transitions after which they do not, when the two are matched on their surface dynamics. The motivation is philosophical: debates about personal persistence contrast a person resuming her life with her not doing so, and it is an open question whether any physiological signal is sensitive to that contrast rather than to transitions as such. Before any such test, three things had to be settled: what data it needs, whether public data provide it, and whether the first precondition, a structured interoceptive signal, holds in those data. The article reports all three. The main test was not run: the analysis stopped at the precondition, and a later audit showed that the stop rested on a statistic that departed from the written plan (§2.4, §3.4). The article claims nothing about identity, consciousness or any mechanism of persistence.

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

**Signal.** R-peaks were detected with an adaptive Pan–Tompkins detector (Pan and Tompkins 1985). The written plan specified that the heart-period (RR) series be resampled evenly at 4 Hz. The executed code instead used the beat-indexed RR series, after removing intervals outside 0.3–2.0 s and beyond four robust standard deviations (median absolute deviation) of the median.

**Statistic.** Time-reversal asymmetry at lag one sample, $T = \langle d^3 \rangle / \langle d^2 \rangle^{3/2}$ with $d_t = x_{t+1} - x_t$, which is zero in expectation for a time-reversible process such as a linear Gaussian one. One sample is one beat in the executed version and 0.25 s in the written plan.

**Null.** 200 iterative amplitude-adjusted Fourier-transform (IAAFT) surrogates per patient, which preserve the power spectrum and the amplitude distribution and destroy nonlinear phase structure (Schreiber and Schmitz 1996). A patient's series counted as structured if the observed statistic fell outside the surrogate distribution at two-sided p < 0.05.

**Decision.** Pass if the fraction of structured patients was at least 0.60.

Three features of the gate should be stated plainly. First, the executed statistic departed from the written plan, as just described; the deviation was not recorded when the gate was run; it was found while the follow-up analyses of §2.6 were being prepared, and recorded before they were run. Second, the gate was applied to the RR series itself, not to a residual left after a model of ordinary physiology. The plan justified this as the cleaner qualification of the observable's own structure. It is a different test: a signal can fail to be structured on its own and still leave a structured residual, or the reverse. Third, the gate as run had no positive control. It had not been shown to pass on a population in which heart-period nonlinearity is expected; §2.6 adds that control.

### 2.5 Simulation audits of the planned statistics

Before the gate was run, the statistics planned for the later stages were audited on synthetic data. Two of them recur below. The *stratified gating differential* is the difference in the success rate of an external perturbation between moments when the interoceptive state is receptive and moments when it is not, contrasted with a placebo perturbation delivered without regard to that state. The *dissociation statistic* is the interaction between the interoceptive residual and the recovery/non-recovery class in predicting the transition. The models are low-dimensional and their units arbitrary; the audits establish properties of the statistics, not of physiology.

- **Common-generator subtraction.** A synthetic common driver acted on both a boundary proxy and an outcome variable, with or without a genuine gating coupling. The planned test regressed out a noisy measurement of the driver and tested the residual interaction against an autocorrelation-preserving block-permutation null.
- **Criticality.** A probabilistic branching network at the critical point, without gating, was compared with a gated counterpart on both statistics, varying read-out noise and the sign of feedback.
- **Branching-ratio estimation.** The naive lag-one estimator and the multistep-regression estimator were compared on short, subsampled, continuous traces.
- **Matching.** False-positive rates of the dissociation statistic were mapped over sample size, effect size and matching quality.
- **Residual-structure tests.** Two tests proposed for qualifying a residual were examined: a variance change-point test and a test for rotation of the eigenvectors of a delay-embedded covariance matrix.

### 2.6 Planned follow-up analyses

Four analyses were specified before they were run, in this manuscript and in pre-registration files committed with it (§2.7), to settle what the gate's failure meant.

- **Positive control.** The gate, in both its executed and its written version, is applied to healthy young and elderly subjects of the Fantasia database (Iyengar et al. 1996), using the database's verified beat annotations. The gate is informative about I-CARE only if it passes in the healthy young group.
- **Beat-indexed, multiscale version.** The asymmetry statistic is recomputed on the beat-indexed RR series, without interpolation, at scales 1 to 10 beats, following the multiscale approach of Costa et al. (2005), with ectopic and artefactual beats removed, and judged against the same 0.60 bar. This addresses two weaknesses of the gate: a single lag, of one beat as executed or 0.25 s as written, captures only the shortest scale, and arrhythmia can inflate the statistic. The written version of the gate is also applied to the same 21 patients.
- **Full pilot by outcome.** The multiscale statistic, computed on the first 30 min of clean beats, is compared between good-outcome and poor-outcome patients in a larger I-CARE sample of 50 patients per group, taken in record order. This is descriptive and does not test the dissociation.
- **Audit re-check.** The classification of the seizure corpora is re-checked against the files themselves, since many recordings in clinical EEG corpora include an ECG channel, and the available EEG signals in VitalDB are re-checked against its track list.

### 2.7 Provenance

The plans for the audit and the gate were written in the author's repository. For both, the plan and the result entered the repository in the same commit, so their order cannot be verified from the record. The follow-up analyses of §2.6 were specified in a version of this manuscript and in pre-registration files committed before they were run (commit `fbe4b6f`); the pre-registration files record the deviation of §2.4 and fix both versions of the gate for the positive control and the multiscale analysis. Results were committed afterwards (commits `46b168f` to `6c27c4d`). No external registry was used, so the order rests on the repository history. The R-peak detector was changed during the analysis. A fixed-threshold detector found 55 peaks in a 118-minute record and was replaced by the adaptive detector. The structured fraction was 0.42 under the fixed-threshold detector and 0.29 under the adaptive one. Both fall below the 0.60 bar in the executed beat-indexed version, so the decision to stop did not depend on the detector.

## 3. Results

### 3.1 Dataset audit

One corpus satisfied all three properties (Table 1).

**Table 1.** Public corpora against the three data requirements, as assessed from documentation and, where marked, from the files (§3.4).

| Corpus | P1 concurrent EEG + cardiac | P2 recovery / non-recovery contrast | P3 length | Notes |
|---|---|---|---|---|
| I-CARE (post-cardiac-arrest) | yes, where ECG available | yes (CPC 1–2 vs 3–5) | yes | between-patient contrast; severity must be matched |
| VitalDB (surgical) | yes: raw EEG (two channels) in 5,871 of 6,388 cases, from the files; ECG per documentation, not counted | no (almost all recover) | partly: long records, but only two EEG channels | supplies only the recovery arm; corrected from documentation-based "no" |
| MIMIC-III/IV Waveform (ICU) | no concurrent raw EEG | yes | yes | |
| Sleep-EDF, SHHS, MASS (sleep) | yes in SHHS and MASS | no (sleep is reversible) | yes | supplies only the recovery arm |
| CHB-MIT (seizure) | no: no ECG in 30 of 30 files checked, from the files | no | yes | files checked come from one patient |
| TUH EEG (seizure) | not checked (access requires an application) | no | yes | |

The contrast in I-CARE is between patients, not within a patient, and patients with good and poor outcomes differ systematically in their post-arrest EEG; that difference is the basis of EEG-based prognosis. Matching on surface dynamics is therefore demanding even where the contrast exists.

### 3.2 Estimability gate as executed

Of 24 patients examined in record order, 3 had no segment long enough to yield 200 R-peaks. Of the remaining 21, 6 showed time-reversal asymmetry outside the IAAFT surrogate distribution (29%; Wilson 95% CI 14–50%), below the 0.60 bar. The analysis stopped, and the dissociation was not run. Section 3.4 shows that this verdict depends on the executed statistic.

### 3.3 Simulation audits

The audits constrain any future test more than the gate does.

**Common-generator subtraction.** Against a linearly acting common driver, the residual test kept a nominal false-positive rate and full power, provided the null preserved autocorrelation. A naive shuffle inflated false positives about threefold. Against a driver that itself carried an interaction term, the test produced false positives at a rate that grew with record length, reaching about 0.9 at the longest records simulated. The rate depended on how well the driver was measured: about 0.1 when the proxy captured 95% of the driver's variance, 0.3 at 89% and 0.6 at 75%. Subtracting the proxy's interaction term did not help. This is the time-series form of a known result: controlling for a confounder measured with error leaves residual confounding, and more data make spurious significance more likely (Westfall and Yarkoni 2016).

**Criticality.** A critical branching network without any gating reproduced the stratified gating differential in 15 of 24 parameter cells (62.5%), with magnitude matching or exceeding that of the gated network as criticality strengthened. A non-critical control returned a differential of about zero. Under a clean read-out with weak homeostatic feedback, the ungated network produced a differential of about −0.25, larger in magnitude than the +0.07 to +0.12 of the gated network, with sign set by what the read-out tracked. Neither a directional criterion nor generalization across network topologies separated the two, which is what critical universality predicts (Kinouchi and Copelli 2006). The dissociation statistic was more robust but not immune: at the strongest cell, the ungated network reached about 73% of the value produced by a signal that was genuinely class-dependent.

**Branching-ratio estimation.** On short subsampled traces, the naive lag-one estimator read a true branching ratio of 0.94 as about 0.79 and certified about 79% of near-critical systems as safely subcritical, reproducing the bias reported by Wilting and Priesemann (2018). The multistep-regression estimator read it as about 0.92, accepted about 90% of genuinely subcritical systems and rejected about 83% of near-critical ones.

**Matching.** Imperfect matching raised the false-positive rate of the dissociation statistic from 0.05 at perfect matching to 0.16 at a standardized mismatch of 0.3 and 0.35 at 0.6, independent of sample size. With matching at or below 0.3, a moderate effect (signal-to-noise ratio 0.8) required about 40 patients per condition for 80% power.

**Residual-structure tests.** Both proposed tests failed as discriminators. A variance change-point test on a residual computed against a model fitted before the transition detects any change of regime, because the model is misspecified afterwards. The eigenvector-rotation test is degenerate for a two-dimensional delay embedding. For a stationary series, the covariance of $(x_t, x_{t-\tau})$ has equal diagonal entries, so its eigenvectors are $(1, 1)/\sqrt{2}$ and $(1, -1)/\sqrt{2}$ whatever the signal. The principal axis sits at 45° when the autocovariance at lag $\tau$ is positive and at 135° when it is negative. The test is blind to amplitude, reports a 90° rotation whenever a change of frequency flips the sign of the lag-$\tau$ autocovariance, and is dominated by noise when that autocovariance is near zero. A simulation confirmed all three behaviours (Appendix A). Both tests were dropped from the protocol.

### 3.4 Follow-up analyses

**Positive control.** In the Fantasia database, the executed version of the gate found structure in 19 of 20 young subjects (95%; 95% CI 76–99%) and 17 of 20 elderly subjects (85%). The written version found structure in 17 of 20 young (85%; 64–95%) and 18 of 20 elderly subjects (90%). Both versions pass the bar in the young, so the gate can pass. The executed version showed the higher structured fraction in the young that the findings of Costa et al. (2005) predict; the written version did not. Values of |T| above 0.5 were common in healthy young subjects under the executed version (10 of 20, up to 1.12), so the magnitude of the statistic does not by itself indicate arrhythmia.

**The gate as written, and a multiscale version.** On the same 21 I-CARE patients, the written version of the gate found structure in 16 (76%; 55–89%), above the bar. The multiscale version found structure in 15 (71%; 50–86%), and in 20 of 20 young and 16 of 20 elderly Fantasia subjects. Five of the six patients structured under the executed version remained structured after ectopic beats were removed. One patient had a multiscale summary of 50.2, far outside the range of the others (0.8–3.9) and probably an artefact; without that patient, 14 of 20 (70%) are structured. The beat series reproduced the pilot's interval counts exactly in all 21 patients. By the plan as written, and by the multiscale version, the estimability precondition is met, and the analysis should not have stopped. With 21 patients, both confidence intervals include values below 0.60.

**By outcome.** In 50 good-outcome and 50 poor-outcome patients, the median multiscale summary was 1.82 (IQR 1.14–3.16) and 2.07 (IQR 1.26–4.71) respectively (two-sided Mann–Whitney p = 0.16), and 74% and 80% of series were structured. The groups differed in covariates that any dissociation test would have to match: median age 55 against 64 years, men 80% against 62%, and a shockable initial rhythm in 70% against 31%. To obtain 50 patients per group, 59 good-outcome and 62 poor-outcome patients were skipped because none of their first three ECG segments gave 30 min of clean beats, so both samples are selected on signal quality. The comparison is descriptive and does not test the dissociation.

**Audit re-check.** None of the first 30 CHB-MIT files, all from one patient, contained an ECG channel; an exploratory check outside the plan found none in the first file of each of 24 patients. VitalDB, classified from its documentation as lacking raw EEG, has raw EEG tracks in 5,871 of its 6,388 cases, and Table 1 is corrected accordingly. TUH EEG was not checked, because access requires an application. None of these corpora has a recovery/non-recovery contrast, so the conclusion of the audit is unchanged.

## 4. Discussion

The main test of this article was not run. The analysis stopped at its first gate, and the stop was a process error: the executed statistic departed from the written plan, the departure was not recorded, and under the plan as written the gate passes. A multiscale version specified before it was run also passes, and a positive control shows that the gate can pass in healthy subjects.

What the three versions agree on is informative. Asymmetry between successive beats was present in 95% of healthy young adults but in only 29% of these patients. That is consistent with the loss of heartbeat time irreversibility with age and heart disease (Costa et al. 2005), and with the sedation, cooling and vasopressors such patients typically receive. Structure across scales of 1 to 10 beats persisted in most patients (71% in the pilot, 74–80% in the larger sample). Whether the interoceptive signal counts as structured therefore depends on the scale the statistic reads, and the plan fixed a version that the code did not use. The written version is itself the least clear of the three. Its lag of 0.25 s is shorter than a beat, so it reads an interpolated series within single intervals, and in Fantasia it did not reproduce the expected age ordering. The conclusion that the precondition is met does not rest on it alone, since the beat-indexed multiscale version also passes. The process lesson is general: a pre-specified stopping rule protects against flexible analysis only if the code is checked against the plan before the rule is applied.

The simulation audits carry the more durable lessons. Any test of whether an interoceptive state gates the efficacy of a perturbation must contend with four facts. State-dependent efficacy is produced by critical dynamics without any gating mechanism (compare Kinouchi and Copelli 2006). Subtracting a common generator measured with error manufactures interactions, increasingly with more data (compare Westfall and Yarkoni 2016). Contrasts defined by outcome manufacture dissociations unless matching is tight. And distance to criticality, which must be controlled, is underestimated by naive estimators on subsampled data (Wilting and Priesemann 2018). None of these is new in isolation; together they set a bar that no analysis of the available public data has yet been shown to meet.

The conceptual limits of the question are as important as the empirical ones. The recovery/non-recovery contrast is between patients and defined by outcome, so it is confounded with severity. In the I-CARE sample the outcome groups differed by nine years in median age and by 39 percentage points in the proportion of shockable rhythms (§3.4), so a dissociation test on this corpus would stand or fall on how well such covariates can be matched. Treating non-recovery as a transition across which a person does not persist is a substantive philosophical position, not a clinical fact. And an interoceptive signal that gates perception is not thereby a signal of anything about the person beyond her physiological state. The next steps licensed by the plan, a subsampling-robust estimate of distance to criticality and the matched dissociation, can be attempted on public data: I-CARE supplies the contrast, and VitalDB, with raw EEG in most of its surgical cases and ECG listed in its documentation, could supply a large recovery-only reference. They were not run here. Whether they are worth running depends on an argument, which this article does not supply, for why an interoceptive signal is the right place to look.

## 5. Conclusion

A test of whether an interoceptive signal is specific to transitions a person survives requires concurrent EEG and cardiac recordings, a matched recovery/non-recovery contrast, and long records. One public corpus, I-CARE, has all three. Its first planned step, a check for nonlinear heart-period structure, failed as executed (6 of 21 patients, against a 60% bar), but the executed statistic departed from the written plan; as written, the check passes (16 of 21), a multiscale version passes (15 of 21), and a positive control passes in healthy young adults. Estimability is not the binding constraint; the imbalance between outcome groups is. Simulation audits show that state-dependent perturbation efficacy is produced by critical dynamics alone, that subtracting a noisily measured common generator manufactures interactions, and that outcome-defined contrasts manufacture dissociations unless matching is tight.

---

## Appendix A. Degeneracy of the Two-Dimensional Eigenvector-Rotation Test

Sinusoids were sampled at 100 Hz with additive Gaussian noise (standard deviation 0.3); AR(1) series had unit innovation variance. All series were embedded as $(x_t, x_{t-5})$. The angle of the leading eigenvector of the embedded covariance was computed before and after an imposed change.

| Change imposed | Angle before → after | Test output |
|---|---|---|
| Amplitude ×4, same frequency | 45.0° → 45.0° | no rotation |
| Sinusoid 3 Hz → 14 Hz | 45.0° → 135.1° | 90° "rotation" |
| AR(1) coefficient 0.5 → −0.5 | 42.9° → 135.1° | 90° "rotation" |
| AR(1) coefficient 0.5 → 0.95 | 59.1° → 45.0° | noise (lag-5 autocovariance near zero before) |

Rows 3 and 4 start from the same process. For an AR(1) coefficient of ±0.5 the lag-5 autocorrelation is only ±0.03, so the "before" angle is noise-sensitive: 42.9° in one run and 59.1° in the other. Row 3 still shows the sign-driven jump to 135°, but from a weak starting signal.

---

## Declarations

**Use of generative AI.** The analyses, code and text of the underlying project were developed with substantial assistance from a large language model (Claude, Anthropic), and this manuscript was drafted by that model on 27 September 2026 from the author's earlier drafts and experimental record. The simulation in Appendix A was run by the model, and the follow-up analyses of §2.6 were coded and run with its assistance. The author reviewed the manuscript and takes full responsibility for its content. [AUTHOR TO CONFIRM OR AMEND BEFORE SUBMISSION.]

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

Iyengar, N., Peng, C.-K., Morin, R., Goldberger, A. L., & Lipsitz, L. A. (1996). Age-related alterations in the fractal scaling of cardiac interbeat interval dynamics. *American Journal of Physiology, 271*, 1078–1084.

Kinouchi, O., & Copelli, M. (2006). Optimal dynamical range of excitable networks at criticality. *Nature Physics, 2*(5), 348–351. https://doi.org/10.1038/nphys289

Pan, J., & Tompkins, W. J. (1985). A real-time QRS detection algorithm. *IEEE Transactions on Biomedical Engineering, 32*(3), 230–236.

Park, H.-D., Correia, S., Ducorps, A., & Tallon-Baudry, C. (2014). Spontaneous fluctuations in neural responses to heartbeats predict visual detection. *Nature Neuroscience, 17*(4), 612–618.

Schreiber, T., & Schmitz, A. (1996). Improved surrogate data for nonlinearity tests. *Physical Review Letters, 77*(4), 635–638.

Westfall, J., & Yarkoni, T. (2016). Statistically controlling for confounding constructs is harder than you think. *PLOS ONE, 11*(3), e0152719. https://doi.org/10.1371/journal.pone.0152719

Wilting, J., & Priesemann, V. (2018). Inferring collective dynamical states from widely unobserved systems. *Nature Communications, 9*, 2325.

Zrenner, C., Desideri, D., Belardinelli, P., & Ziemann, U. (2018). Real-time EEG-defined excitability states determine efficacy of TMS-induced plasticity in human motor cortex. *Brain Stimulation, 11*(2), 374–389.
