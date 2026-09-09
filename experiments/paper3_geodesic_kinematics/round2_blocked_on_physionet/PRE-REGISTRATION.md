# Pre-registration — Round-2 data items blocked on the PhysioNet outage

**Status:** pre-registered, NOT run. Blocked by an external outage. No `result.json`, so none
of these is counted as a completed experiment. The designs are fixed here *before* data access
precisely so that, when the data becomes reachable, they cannot be retro-fitted to a result.

## The blocker (recorded, outcome-independent)
On 2026-09-09 `physionet.org` presents an **expired TLS certificate**: every download fails
with `certificate verify failed: certificate has expired`, through the session's egress proxy,
which correctly refuses it. This is host-specific — arXiv, Google and the general web resolve
`200` through the same proxy, and the proxy reports no relay failures — and it is not something
to route around (disabling TLS verification is prohibited and would be wrong). So no *new*
PhysioNet record (Sleep-EDF beyond the 9 cached, I-CARE EEG, SHHS) can be fetched this session.
Only the locally cached data is available. The items below wait for PhysioNet's certificate to
be renewed; each is a straightforward run once it is.

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
