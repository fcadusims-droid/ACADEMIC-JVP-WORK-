# Pre-registration — Round-2 data items blocked on this session's egress TLS path

**Status:** pre-registered, NOT run. Blocked by this session's egress TLS path (see corrected diagnosis below), not by a global PhysioNet outage. No `result.json`, so none
of these is counted as a completed experiment. The designs are fixed here *before* data access
precisely so that, when the data becomes reachable, they cannot be retro-fitted to a result.

## The blocker (recorded, outcome-independent) — corrected diagnosis
Every download from `physionet.org` in **this session** fails with `certificate verify failed:
certificate has expired`, deterministically, through the session's egress proxy. The first
write-up of this attributed it to PhysioNet serving an expired certificate to the world and
said to wait for a renewal. **That was wrong, and is corrected here.** The repository maintainer
independently confirmed that `physionet.org` serves normally from other networks (all 197
Sleep-EDF Expanded records, 8.1 GB, reachable), and `sleepdata.org` (NSRR) fails the same way
here while arXiv and Google resolve `200` through the same proxy. So the fault is **environment-
/session-local** — this egress path's TLS view of a class of research-data hosts, not a global
PhysioNet outage — consistent with the repo having previously downloaded its 9 cached Sleep-EDF
records from the same site. It is still not something to route around from inside this session
(disabling TLS verification is prohibited, and the egress proxy's upstream view is not under this
session's control), so the downloads remain unavailable **here**. The correct remedy is **not**
to wait for PhysioNet: it is to run these items from an environment that reaches these hosts —
the maintainer's own machine, or a fresh session whose egress path validates them. Each item
below is a straightforward run there; only the local sandbox blocks it.

## Item 1 — H1 power-up (Paper 3, extends `scalar_vs_manifold_localization`)
`scalar_vs_manifold_localization` returned INCONCLUSIVE at n=22 (manifold 14/22 vs scalar 9/22,
McNemar p=0.227); the discordant pairs were too few to resolve. The same open corpus
(Sleep-EDF Expanded, 197 records) supplies the n. **Pre-registered:** re-run the *identical*
matched-detector comparison — geodesic CUSUM vs `log Tr(cov)` CUSUM, same windows/tolerance —
on as many Sleep-EDF sleep-onset records as download allows, targeting the power computed in the
Round-2 note: **~74 records for 80% power** at the observed discordance ratio (8/11), rising to
~180 at a conservative π=0.65. Criterion unchanged: manifold beats scalar iff McNemar p<0.05 and
b>c; tie iff |man−sca|≤1 and p≥0.05. **Run this off-centre** (per `localization_centerbias_control`):
place the transition at 1/4 of the window, not the midpoint, so the centre prior cannot inflate
the absolute rates. No re-tuning of the detector.

## Item 2 — H2 collapse → burst-suppression, closing the demarcation at 3/3 (Paper 3, extends `regime_external_referent`)
`regime_external_referent` bound 2 of 3 regimes (drift/dispersion) to AASM staging; the
**collapse** regime (abrupt drop in the smallest covariance eigenvalue = rank collapse) has no
AASM counterpart, which is why it bound only 2/3. **Pre-registered external referent for
collapse: burst-suppression**, an EEG state clinically and quantitatively scored by the Burst
Suppression Ratio (BSR = fraction of time with |EEG| < ~5 µV for ≥ 0.5 s; BJA 2026, Frontiers
2020). **Design:** on I-CARE post-cardiac-arrest EEG (already used by `cbra_boundary_residual`,
so no new corpus is needed — only its `*_EEG.mat` segments, which the outage currently blocks),
compute the protocol's collapse-regime indicator per epoch and score its association with a
BSR-derived burst-suppression label against a within-record label-shuffle permutation null
(Cramér's V, same machinery as `regime_external_referent`). **Criterion:** collapse binds iff
V exceeds the null 95th percentile in the mapped direction (collapse enriched for high BSR).
Success would move the demarcation from 2/3 to **3/3** externally-referenced regimes; failure is
reported as a collapse regime that is real dynamically but lacks an external referent even in
burst-suppression. One run, no tuning loop.

## Item 3 — SHHS EEG+ECG pipeline calibration (Paper 2, context for `cbra_dataset_inventory`)
`cbra_dataset_inventory` (H4) established that no public corpus carries raw EEG + concurrent ECG
+ an I⁺/I⁻ contrast except I-CARE (which fails estimability at B1=29%). SHHS (9,736 PSG, C3/C4 +
ECG, open) has raw EEG + ECG but **no I⁺/I⁻ contrast**, so it cannot carry the positive arm —
this does not change H4's conclusion. Its only pre-registered use is *calibrational*: confirm the
EEG+ECG boundary-residual pipeline runs end-to-end and estimates the residual stably on a large,
healthy, non-post-arrest cohort, isolating whether B1's 29% is driven by the estimator or by the
post-arrest confounds (sedation/TTM/pressors suppressing cardiac time-irreversibility; Costa–
Goldberger–Peng, PRL 95 198102 2005). **This is a pipeline check, not a test of the CBRA positive
arm**, and it too is blocked by the outage (SHHS is hosted on PhysioNet/NSRR).
