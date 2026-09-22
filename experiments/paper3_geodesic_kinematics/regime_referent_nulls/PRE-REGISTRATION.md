# Pre-registration — Does H2's AASM binding survive a correct null, and is it the geometry?

**Status:** pre-registered before the run. One run, no tuning loop. Written in response to an
external review of `regime_external_referent` (H2), whose three objections are checked against
the code and all three hold:

1. **The null was wrong.** H2 shuffled AASM labels i.i.d. within each record across 563,242
   overlapping sliding windows from 7 records. Hypnograms come in blocks of minutes to hours and
   H2's regime series is a rolling mean, so i.i.d. shuffling destroys the autocorrelation of both
   series and yields an artificially narrow null (95th pct 0.003). The reported p = 0.0005 does
   not show the association survives a null that respects dependence.
2. **The "regime" tested is not the paper's demarcation.** `protocol_regime` is a median split of
   the rolling-mean geodesic step between consecutive windows — a volatility measure. It involves
   no drift/diffusion/jump estimation from the SDE, no Lyapunov exponent and no statistical
   complexity; its docstring calling it a "Lyapunov proxy" overstated it. W and REM being more
   volatile than N2/N3 is expected of any non-stationarity measure.
3. **No baseline.** Nothing checked whether a scalar power-volatility series does as well.

Also recorded: H2 targeted 15 records and used **7**. Only 9 Sleep-EDF PSGs are cached in this
environment (downloads are blocked by the cloud egress; see `round2_blocked_on_session_egress`);
SC4041 has no hypnogram, and SC4012 is truncated and fails to load, leaving 7.

## Data
The same 7 cached Sleep-EDF records, same windows (2 s, 1 s step), same AASM mapping as H2
(N2/N3 → "drift stage", W/REM → "dispersion stage"; N1 and unscored windows excluded).

## Features, each median-split within record exactly as H2 did
- **geo_vol** — H2's `protocol_regime`: rolling mean (10 windows) of the geodesic step between
  consecutive trace-normalised covariances. Named here for what it is: geodesic volatility.
- **scalar_vol** — rolling mean (10 windows) of |Δ log total power|, same windows. The matched
  scalar counterpart: the same volatility construction on the power the manifold discards.
- **scalar_level** — log total power itself (no geometry, no volatility).

## Nulls
- **Circular shift (primary):** for each record, rotate the full AASM label sequence by an offset
  drawn uniformly from [0.1 L, 0.9 L] windows, then re-apply the mapping and pool. Preserves the
  autocorrelation of both series. 2000 shifts. Same shifts reused across the three features.
- **Record level (n = 7):** per-record enrichment d_r = P(N2/N3 | low-volatility half) − P(N2/N3)
  in record r; one-sided Wilcoxon signed-rank on {d_r} (H1: d > 0).

## Pre-registered criteria
- **Association survives a correct null** iff geo_vol's pooled V exceeds the 95th percentile of
  its circular-shift null **and** the record-level Wilcoxon is one-sided p < 0.05.
- **Attributable to the geometry** iff, in addition, geo_vol's pooled V exceeds the pooled V of
  **both** scalar features **and** a one-sided Wilcoxon on per-record V (geo_vol minus the better
  scalar feature) gives p < 0.05.
- Verdicts: (A) survives and attributable; (B) survives, not attributable — the binding is
  non-stationarity tracking sleep stage, not evidence for the geometry; (C) does not survive —
  H2's p = 0.0005 was an artefact of the i.i.d. null and the partial repair is withdrawn.
- Whatever the verdict, the coverage manifest stops crediting the *three-regime demarcation* to
  H2: what was tested is a volatility proxy, not the demarcation.

## Addendum (POST-HOC, written after the primary result and before running it)
The primary run returned verdict (A). But its scalar baselines used *total* power, while the
review named *band* power, and the obvious scalar competitor for N2/N3 versus W/REM is relative
delta power (0.5–4 Hz) — slow-wave activity is part of the AASM definition of N3. A verdict
crediting the geometry only against weak baselines would overclaim. So, labelled post-hoc:
relative delta power (averaged over channels) as a level and as a 10-window rolling volatility
of its log, same windows, same within-record median split, same record-level test.
**Criterion, fixed now:** if either delta feature's pooled V ≥ geodesic-volatility V, or the
per-record one-sided Wilcoxon (geo − best delta feature) is not p < 0.05, the "attributable to
the geometry" clause of verdict (A) is withdrawn and the verdict reads (B). Output:
`posthoc_spectral.json`; it does not replace `result.json`.
