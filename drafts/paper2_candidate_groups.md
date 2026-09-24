# Candidate groups for the Paper 2 data partnership

**Working list for the author. Nobody on it has been contacted.** It goes with
`drafts/paper2_data_specification.md`. The author decides whom to write to.

*Compiled 2026-09-24 from Europe PMC searches. Every study below was read in full text (one
from its abstract only, marked) and its DOI checked against Crossref.*

## The filter

A group is listed only if it has published, since 2019, at least one study in which it
recorded all of the following itself:
- raw multichannel EEG, not a processed index such as BIS;
- simultaneous ECG or haemodynamic signals;
- in anaesthesia or in neurological intensive care (coma, disorders of consciousness).

Working on "anaesthesia and EEG" in general is not enough. A group that only re-analyses a
public dataset is excluded, because it holds no data beyond what is already public. That rule
excludes anyone working only on I-CARE, which already failed the gate.

Each entry is then checked against the three properties the specification asks for together:
1. **Channels and ECG.** At least 19 EEG channels, with ECG fast enough for R-peak timing
   (≥ 250 Hz).
2. **Contrast.** A person-preserving versus non-preserving contrast (I⁺/I⁻), ideally in the
   same cohort.
3. **Length.** Hours of stable recording around the transition.

## Meets the filter

The ranking puts first the groups whose own cohort contains both arms of the contrast
(survivors versus non-survivors, or recovery versus non-recovery). The specification needs
that and no public corpus other than I-CARE has it.

### 1. Lausanne / Bern — De Lucia (Lausanne University Hospital), with the Bern University Hospital ICU
- **Verified study:** Pelentritou, …, De Lucia 2025. "Cardiac signals inform auditory
  regularity processing in the absence of consciousness." *PNAS*.
  DOI: 10.1073/pnas.2505454122.
- **Recorded:**
  - high-density EEG, 63 active electrodes at 1,200 Hz, with simultaneous ECG;
  - 64 comatose patients in the first day after cardiac arrest, at the Bern University
    Hospital ICU, 2017–2022.
- **Contrast:** survivors versus non-survivors in the same cohort. **This is the I⁺/I⁻
  structure the protocol needs.**
- **Properties:**
  - (1) yes;
  - (2) yes;
  - (3) probably not as published: a 20-minute baseline plus stimulation blocks of about
    10 minutes. Ask whether longer continuous EEG/ECG exists for the same patients.
- **Data:** analysis code on GitHub; data availability to be asked.

### 2. Paris — Hermann, Benghanem, Sharshar, Cariou (Université Paris Cité / Inserm UMR-S 1266; Cochin Hospital medical ICU)
- **Verified studies:**
  - Hermann, Candia-Rivera, Sharshar, …, Benghanem 2024. "Aberrant brain–heart coupling is
    associated with the severity of post cardiac arrest brain injury." *Annals of Clinical
    and Translational Neurology*. DOI: 10.1002/acn3.52000.
  - Hermann, Benghanem, …, Candia-Rivera 2025. "Brain-heart interactions are associated with
    mortality and acute encephalopathy in ICU patients with severe COVID-19." *Clinical
    Neurophysiology*. DOI: 10.1016/j.clinph.2025.2110745 (abstract checked).
  - Benghanem, …, Hermann 2024. "Heart rate variability for neuro-prognostication after CA:
    Insight from the Parisian registry." *Resuscitation*.
    DOI: 10.1016/j.resuscitation.2024.110294.
- **Recorded:**
  - EEG with 2 precordial ECG leads at 256 Hz on a Natus Deltamed system, in consecutive
    patients admitted to the Cochin ICU after cardiac arrest;
  - the EEG montage is reduced: Fp1, Fp2, C3, Cz, C4, O1, O2 and a reference.
- **Contrast:** good versus poor outcome (CPC) in the same prospective registry.
- **Properties:**
  - (1) **no**: about 7 EEG channels, against the 19 the specification asks for;
  - (2) yes;
  - (3) to be asked.
- **Data:** "available from the corresponding author upon reasonable request".
- **Note:** the ECG-coupling methods and outcome registry fit well. The montage does not meet
  the specification as written. Either the specification is relaxed for this group, which
  would have to be decided and pre-registered before any data are seen, or the group is asked
  whether full-montage recordings exist.

### 3. Paris — Sitt, Naccache, Candia-Rivera (Paris Brain Institute – ICM; Pitié-Salpêtrière), with Tallon-Baudry (ENS)
- **Verified studies:**
  - Candia-Rivera, Raimondo, Pérez, Naccache, Tallon-Baudry, Sitt 2023. "Conscious processing
    of global and local auditory irregularities causes differentiated heartbeat-evoked
    responses." *eLife*. DOI: 10.7554/eLife.75352.
  - Candia-Rivera, Annen, Gosseries, Martial, Thibaut, Laureys, Tallon-Baudry 2021. "Neural
    Responses to Heartbeats Detect Residual Signs of Consciousness during Resting State in
    Postcomatose Patients." *J Neurosci*. DOI: 10.1523/JNEUROSCI.1740-20.2021. Abstract only;
    the full text could not be retrieved. This one is joint with the Liège Coma Science Group.
- **Recorded:** high-density EEG, analysed on a 64-channel subset, with ECG, in patients with
  disorders of consciousness.
- **Contrast:** minimally conscious state versus unresponsive wakefulness. That is a
  diagnostic contrast, not transition versus non-transition; ask whether outcome follow-up
  exists.
- **Properties:**
  - (1) yes;
  - (2) partial;
  - (3) to be asked.
- **Data:** "available upon reasonable request"; code and pre-processed data on GitHub.

### 4. Milan — Sattin and colleagues (Fondazione IRCCS Istituto Neurologico Carlo Besta)
- **Verified study:** Sattin, Duran, Visintini, …, 2021. "Analyzing the Loss and the Recovery
  of Consciousness: Functional Connectivity Patterns and Changes in Heart Rate Variability
  During Propofol-Induced Anesthesia." *Frontiers in Systems Neuroscience*.
  DOI: 10.3389/fnsys.2021.652080.
- **Recorded:** 19-channel 10–20 EEG at 256 Hz with simultaneous ECG (HRV), through propofol
  induction, loss of consciousness and recovery of consciousness in neurosurgical patients.
- **Contrast:** anaesthesia only, so the I⁺ arm without an I⁻ arm.
- **Properties:**
  - (1) yes for EEG; the ECG sampling rate is to be checked;
  - (2) I⁺ only;
  - (3) short peri-induction and peri-emergence windows.
- **Data:** deposited on Zenodo, according to the paper's data statement. It is the one
  candidate with data already public. Useful for piloting the I⁺ arm, not for the test.

### 5. Florence — Mannini, Hakiki, Grippo (IRCCS Fondazione Don Carlo Gnocchi; Sant'Anna School of Advanced Studies)
- **Verified study:** Liuzzi, Hakiki, Scarpino, …, Mannini 2023. "Neural coding of autonomic
  functions in different states of consciousness." *Journal of NeuroEngineering and
  Rehabilitation*. DOI: 10.1186/s12984-023-01216-6.
- **Recorded:** a 19-electrode 10–20 cap with chest ECG, both at 128 Hz, in patients with
  prolonged disorders of consciousness.
- **Contrast:** levels of consciousness, in intensive rehabilitation rather than acute
  neuro-ICU.
- **Properties:**
  - (1) EEG yes; the ECG at 128 Hz is below the ≥ 250 Hz asked for;
  - (2) partial;
  - (3) to be asked.
- **Data:** no statement found.

## Borderline (one criterion missing)

| Group | Study (verified) | Why borderline |
|---|---|---|
| Chengdu: Southwest Jiaotong University with clinical partners | Li et al. 2026, "Cross-modal synchronization of EEG and ECG reveals hidden signatures of recovery in traumatic brain injury", *JNER*, DOI 10.1186/s12984-025-01869-5 | EEG + ECG at 500 Hz in traumatic brain injury, good versus poor outcome, but n = 11 and the channel count is not stated in the text; ask |
| Seoul: Korea University (S.-W. Lee) | Won et al. 2019, "Alteration of coupling between brain and heart induced by sedation with propofol and midazolam", *PLOS ONE*, DOI 10.1371/journal.pone.0219238 | Over 60-channel EEG with ECG through loss and recovery of consciousness under sedation, but the ECG was sampled at 74 Hz, the study is from 2019, and it is healthy volunteers (I⁺ only) |

## Excluded, with the reason

| Group | Study | Reason |
|---|---|---|
| Tianjin University (Fan H) | Niu et al. 2025 *Sci Rep* (10.1038/s41598-025-93579-0); Niu et al. 2026 *JNER* (10.1186/s12984-026-01971-2) | Re-analysis of the public I-CARE database; no data of their own ("no datasets were generated") |
| University of Michigan (Mashour) | Mashour et al. 2021 *eLife* (10.7554/eLife.59525) | ECG was a standard clinical monitor only; it is not described as recorded for analysis |
| Shanghai Sixth People's Hospital | Li et al. 2026 *Cell Rep Med* (10.1016/j.xcrm.2025.102581) | 128-channel EEG under propofol, but the ECG and blood pressure recordings described are of the awake baseline only |

## What this list does and does not establish

- It establishes that each listed group has **recorded** the right kind of signal together in
  a relevant population at least once. It does not establish that the group still holds those
  data, that the data can be shared, or that the group would be interested.
- No group was found that meets all three properties as written. The closest is Lausanne/Bern
  (1), which fails only on recording length as published. The honest opening question to
  each group is therefore a specific one: whether they hold longer continuous EEG/ECG around
  the transition for the patients in the cited study.
- The searches were of open-access full text in Europe PMC. Groups that publish mainly in
  closed-access venues may be missing. A second pass in PubMed, or through the reviewer who
  offered help, would widen the list.
