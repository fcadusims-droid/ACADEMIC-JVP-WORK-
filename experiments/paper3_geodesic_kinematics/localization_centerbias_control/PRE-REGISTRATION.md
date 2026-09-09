# Pre-registration — Centre-bias control for the localization comparisons (Paper 3)

**Status:** pre-registered before the run. One run, no tuning loop.

## Why this exists
A read of the repo (Round-2 data note, §2b) points out a confound shared by every
within-trajectory localization run to date, including `scalar_vs_manifold_localization`
(H1), `sleep_stage_localization` (A1) and `baseline_benchmark`: the analysis window is
built **symmetric about the true transition** — sleep-onset uses `[t0-90 s, t0+90 s]`, and
the eyes-open/closed splice joins two equal-length segments — so the true change point
falls at the **centre of the window by construction**. With a tolerance band around that
centre, *any* detector with a central prior (or a fallback that returns the midpoint) scores
a hit for free. This inflates the **absolute** hit rates of all methods and could, in
principle, distort the **paired** manifold-vs-scalar comparison if the two detectors lean on
the centre prior to different degrees.

This is a confound-robustness check, **not** a power increase: PhysioNet is unreachable this
session (expired TLS certificate), so no new records can be downloaded and n is unchanged
from H1. The H1 power-up to ~74 records is documented separately as blocked.

## Data (local only)
- Sleep-EDF sleep-onset (W->N1), the same cached records H1/A1 use (`discover_subjects`).
- eegmmidb eyes-open (R01) / eyes-closed (R02), the same cached records (`load_state_covs`).

## Design — two things measured
**(1) Centre-prior baseline (quantifies the inflation).** A trivial "detector" that always
predicts the window centre. Scored under BOTH window constructions:
- **Centred** (the existing design): transition at the window midpoint.
- **Off-centre** (this control): the transition is placed away from the midpoint —
  sleep-onset window `[t0-45 s, t0+135 s]` (same 180 s duration, transition at 1/4), and the
  eyes-open/closed splice uses unequal segments (open 1/2 length, closed full length; seam at
  1/3). Detectors, windows, step, tolerance and min-segment are otherwise identical to H1.

**(2) Manifold vs scalar, re-run in the off-centre design.** The identical geodesic-manifold
CUSUM and scalar log-band-power CUSUM as H1, on the off-centre windows, with the same McNemar
paired test.

## Pre-registered criteria
- **Inflation is real** iff the centre-prior baseline scores materially higher under the
  centred construction than under the off-centre one (drop of >= 0.30 in hit rate). This
  confirms §2b: the absolute localization numbers were inflated by the centred design.
- **The H1 relative conclusion is robust** iff, in the off-centre design, the manifold-vs-scalar
  McNemar verdict is unchanged from H1 — i.e. the manifold is still **not** certified superior
  at p<0.05 (and not certified inferior). If instead the paired verdict flips (manifold now
  beats, or now loses to, scalar at p<0.05), the centred comparison was confounded and H1 must
  be re-read.
- Reported honestly whichever way each lands; the absolute off-centre hit rates are recorded
  but not narrated upward.

## Self-test (gates the run)
On a synthetic SPD trajectory with a single injected change point placed off-centre, the
manifold CUSUM must localize it within tolerance while the centre-prior baseline must miss it.
If the self-test fails, the run aborts and the defect is fixed on the instrument before any
real-data result is read.
