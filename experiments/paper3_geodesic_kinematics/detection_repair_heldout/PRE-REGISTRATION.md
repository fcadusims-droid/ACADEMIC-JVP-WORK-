# Held-Out Validation of the Detection-Statistic Repair (Paper 3)

`detection_statistic_repair` lifted the geodesic CUSUM's detection AUC from 0.227 to
0.813 by scale-normalising the peak. But **four candidate repairs were compared on the
same 15 Sleep-EDF recordings that exposed the problem**, so the winner was selected on
the data it is evaluated on. That is a genuine methodological gap: the repair may be a
real fix to the *statistic*, as its mechanistic diagnosis suggests, or it may be tuned
to the sleep paradigm.

## Test

Apply the **already-chosen** repair — `max|S| / (σ̂√n)`, no further variants, no
re-selection — to a paradigm **not used to choose it**: PhysioNet eegmmidb
eyes-open (R01) versus eyes-closed (R02), occipito-parietal channels in the alpha band.
Real segments concatenate an eyes-open and an eyes-closed run (the seam is the
transition); null segments lie entirely within one state. Both statistics are scored on
the identical segments:

- the **old** peak-to-median ratio (expected to be near or below chance if the
  diagnosis generalises), and
- the **new** scale-normalised peak.

## Pre-registered criterion

- **Repair generalises** if the scale-normalised statistic reaches **AUC ≥ 0.70** on
  this held-out paradigm.
- **Repair is paradigm-tuned** if it falls below 0.70. Then the Paper 3 text must say
  that the fix is demonstrated on sleep only, and the detection claim is restricted
  accordingly.

Secondary (descriptive, not a criterion): whether the old statistic is again
sub-chance here, which would show the *failure* mechanism generalises even if the
repair did not.

Nothing is re-tuned. The repair is applied exactly as committed; only the data are new.

## Status
Run. Verdict: **the repair generalises.** On 16 eegmmidb subjects the scale-normalised
statistic reaches **AUC 0.824**, clearing the 0.70 bar; the old peak-to-median statistic
scores **0.434** on the identical segments — sub-chance again, so the *failure* mechanism
generalises as well as the fix. Nothing was re-tuned: the statistic is the one committed
in `detection_statistic_repair`.

The secondary localisation count (9/16) is **deliberately not quoted** as a result: this
design splices two runs, so the seam always falls at the segment centre and any localiser
with a central prior is flattered. It is not the appendix's eyes-open/closed protocol,
and the appendix's negative localisation finding stands unrevised. Only detection was
under test. See `_results/detection_repair_heldout/result.json`.
