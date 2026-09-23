# Pre-registration: H1 power-up, off-centre (Round-2 Item 1, now runnable)

**Status:** pre-registered before the run. One run, no tuning loop.

The design and primary criterion were fixed in
`round2_blocked_on_session_egress/PRE-REGISTRATION.md` (Item 1) while the data was unreachable.
They are restated here unchanged. The **stopping rule** and **two secondary analyses** are added
now. They were written before any record was downloaded or analysed, and the reasons for them come
from results obtained after Item 1 was written.

## Why
`scalar_vs_manifold_localization` (H1) was INCONCLUSIVE at n = 22: manifold 14/22 vs scalar 9/22,
McNemar p = 0.227. Off-centre, `localization_centerbias_control` found a dead tie, 10/22 vs 10/22.
The Round-2 power note puts ~74 records at 80 % power for the observed discordance ratio.
PhysioNet became reachable from the cloud session on 2026-09-23.

## Design (unchanged from Item 1)
- **Corpus:** PhysioNet Sleep-EDF Expanded, sleep-cassette (SC) recordings.
- **Code:** the identical matched-detector comparison, imported unchanged from
  `localization_centerbias_control` / `sleep_stage_localization`. The loader is `load_subject`,
  with channels Fpz-Cz, Pz-Oz and horizontal EOG, 0.5–30 Hz, per-channel z-score.
  The transition is `find_transition`. There is 2 s / 1 s windowing, and the tolerance is
  ±30 s.
- **Detectors:**
  - manifold: geodesic CUSUM (`embed_cumsum` + `cusum_changepoint`);
  - scalar: log Tr(cov) CUSUM (`scalar_bandpower` + `scalar_cusum`).
- **Placement: off-centre.** The window is [t0 − 45 s, t0 + 135 s], so the transition sits at
  1/4 of the window.
- **No re-tuning** of either detector.

## Primary criterion (unchanged from Item 1)
Record-level paired McNemar (exact binomial on discordant pairs).
- **Manifold beats scalar** iff p < 0.05 **and** b > c, where b = manifold-only hits and
  c = scalar-only hits.
- **Tie** iff |manifold hits − scalar hits| ≤ 1 and p ≥ 0.05.
- **Scalar beats manifold** iff p < 0.05 and c > b.
- Anything else is **inconclusive**, reported with n.

## Stopping rule (added now, before any download)
Attempt to download **every** SC recording: 153 PSG/hypnogram pairs, in file-list order. Analyse
**once**, on every record that downloads and has a qualifying transition. n is whatever that
yields, and it is reported. There is no interim analysis. If the download cannot finish in this
session, the run happens once on what has downloaded, and the shortfall is reported. It is not
topped up later to a more favourable n.

## Secondary analyses (added now; neither can change the primary verdict)
1. **Subject level.** SC records are two nights of one subject (`SC4ssN`), so record-level
   McNemar pseudo-replicates, the defect found in `regime_referent_nulls`. The same McNemar is
   rerun on one record per subject: the lowest night number with a qualifying transition. If
   primary and subject-level verdicts differ, both are reported and the subject-level one is
   treated as the more trustworthy.
2. **EEG only.** `regime_referent_eog_control` and `discrimination_eog_ablation` found the
   geometry's sleep effects carried by the horizontal-EOG channel. Both detectors are rerun on
   Fpz-Cz and Pz-Oz only (SPD(2) for the manifold, Tr of the 2×2 covariance for the scalar), same
   everything else. This asks whether any manifold advantage survives without the eye.

## Also reported
- The centre-prior hit rate in the off-centre window, as a sanity check. It should be near 0.
- Absolute hit rates, with a Wilson 95 % interval.
