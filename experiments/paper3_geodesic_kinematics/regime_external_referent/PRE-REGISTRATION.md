# H2 — can the three-regime demarcation be bound to an external referent? (Paper 3)

**Written before the run.** The Phase-0 gate (`regime_groundtruth_gate`) found the demarcation
*not externally falsifiable as defined*: the regimes are fixed by the protocol's own
Lyapunov/complexity criteria, so no independent referent exists. The reviewer proposed a repair:
bind the regimes to a human-scored external referent — **AASM sleep staging** — and test the
binding. This runs that test. Two honest outcomes, both reportable:
- **Repair (at least partial):** a *pre-registered* mapping from the protocol's dynamical regime
  to AASM stage structure agrees with the human scoring above chance on held-out records → the
  demarcation carves something an external scorer recognises, and the Phase-0 verdict is
  superseded for this paradigm.
- **The gate was deep, not surface:** no pre-registered mapping beats chance (or only a post-hoc
  one does) → the tri-partition does not recut anything AASM recognises, and that is reported as
  prominently as a repair would be.

## Pre-registered mapping (fixed now, before any scoring)
Per analysis window the protocol assigns a coarse regime from its own criteria on the
trace-normalised SPD covariance trajectory:
- **drift / persistent** — low local geodesic expansion (a stable, slowly-drifting regime);
- **dispersion** — high local geodesic expansion / high step variance (isotropic wandering);
- **collapse** — an abrupt drop in the smallest raw-covariance eigenvalue (rank collapse).

Mapped to the external AASM referent, fixed in advance:
- drift/persistent ↔ **N2/N3** (consolidated, structured sleep);
- dispersion ↔ **W/REM** (activated, higher-complexity stages);
- collapse ↔ **(no AASM counterpart)** — declared in advance, because AASM has no rank-collapse
  stage; at most **2 of 3** regimes can bind, the same 2-of-3 ceiling the turbulence candidate hit.

## Score and null
Pool all labelled windows across records. Compute the association (Cramér's V, and adjusted
mutual information) between the protocol regime (drift vs dispersion) and the AASM-mapped label,
against a **permutation null** that shuffles the AASM labels within record (destroying any real
association while preserving marginals). Thresholds are fixed in advance, so every record is
effectively held out (nothing is fitted).

## Pre-registered criterion
- **Partial repair:** observed association exceeds the 95th percentile of the permutation null,
  AND the effect is in the mapped direction (drift enriched for N2/N3, dispersion for W/REM).
- **Gate is deep:** association within the null band → the demarcation does not align with AASM;
  the tri-partition is not externally anchored even for 2 of 3 regimes.

## Self-test gating the run
The AASM labels must actually be present and varied (≥ 2 stages, ≥ 100 labelled windows total), or
the association is undefined; abort if not (a data problem, not a result).

## Attempt budget
**One run, no tuning loop.** Mapping, regime rule, statistic and null fixed here.

## Status
Pre-registered. Not yet run.
