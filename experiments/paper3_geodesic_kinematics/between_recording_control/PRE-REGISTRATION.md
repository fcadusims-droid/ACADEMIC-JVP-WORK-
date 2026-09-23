# Pre-registration: is the eyes-open/closed ratio more than a between-recording difference?

**Status:** pre-registered before the run. One run, no tuning loop. Post-hoc analyses, if any,
are labelled post-hoc in the result.

## Why this exists
The last positive number in Paper 3 is the eyes-open/closed ratio of `eeg_reconciliation`
(temporal-half estimator): median ≈ 1.3, 12/15 subjects > 1, Wilcoxon p ≈ 0.008. An external
review noted an asymmetry in that statistic:

- the **numerator** compares **two separate recordings** (R01, eyes open; R02, eyes closed);
- the **denominator** compares two halves of **one** 26 s recording.

Two recordings differ for reasons that have nothing to do with the state: electrode impedance
drift, a re-seated subject, headset shift, and time elapsed. So a ratio > 1 may mean only
"two recordings differ more than one recording drifts". That needs a negative control: the same
statistic on **two separate recordings of the same state**. The review also asked for a
**scalar baseline** on the same channels, to check whether the SPD geometry adds anything over
per-channel alpha power.

## Data availability (checked before writing this)
eegmmidb (PhysioNet) R01/R02 are 1-minute baselines (eyes open / eyes closed). R03–R14 are
2-minute task runs. Their annotations (checked on S001 R03/R04) alternate **T0 (rest) intervals
of 4.2 s** with T1/T2 task intervals of 4.1 s, 15 T0 intervals per run. The PhysioNet
documentation says "T0 corresponds to rest". It does **not** say whether the eyes are open
during task runs. The paradigm shows targets on a screen, which implies eyes open, but the
documentation does not state it. So T0 is a short, cue-paced inter-trial rest, not a
contiguous baseline. Caveat C3 below checks eyes-open status empirically, but a consistency
check is not a confirmation.

## Statistic (unchanged from `eeg_reconciliation`, temporal-half)
For two window sets A, B, in time order:
`R(A,B) = d(mean A, mean B) / (0.5 * (th(A) + th(B)))`, where `th(X) = d(mean X[:h], mean X[h:])`.

- **Geometry (G):** the same pipeline as `real_eeg_localization`. Channels O1, Oz, O2, PO3, POz,
  PO4, Pz. Alpha 8–13 Hz band-pass, then per-channel z-score over the whole run. 1 s windows,
  0.25 s step, eigen-floored, trace-normalised covariances. Square-root metric,
  `mean_density`. Imported, not re-implemented.
- **Scalar baseline (S):** for each window, the 7-vector of per-channel relative alpha power,
  computed from the unfiltered data. Relative alpha is 8–13 Hz power over 1–40 Hz power, from a
  Hann-windowed periodogram of the 1 s window. Mean = arithmetic mean, d = Euclidean.

## Window sets
- Baselines: the first 26 s of R01 / R02, giving N windows, as before.
- T0 sets: every 1 s window lying entirely inside a T0 interval of the run, in time order,
  truncated to the **same N** windows.

## Arms (per subject, 15 subjects: S001–S015)
- **OC** — R01 vs R02: the claim under test. *Sanity gate:* the median of G_OC must reproduce the
  committed `eeg_reconciliation` temporal-half median within 0.01. Otherwise the result is an
  instrument defect and no verdict is issued.
- **SS** — T0(R03) vs T0(R07). Primary negative control: two separate recordings of the same
  state, from the same task type (real open/close fist).
- **OT** — R01 vs T0(R03). The control the review proposed: baseline eyes-open vs task rest.
- **W** — R01[0, 26 s) vs R01[34 s, 60 s). Secondary: separate segments of one recording.
  It does not capture between-recording differences.

## Pre-registered criteria
**C1 — between-recording control (geometry).** Paired, one-sided Wilcoxon, G_OC > G_SS, across
the 15 subjects.
- **Exceeds the same-state between-recording control** iff p < 0.05 **and** G_OC > G_SS in
  ≥ 11/15 subjects.
- **Not distinguishable from a between-recording difference** iff median G_SS ≥ median G_OC, or
  p ≥ 0.2.
- Otherwise **direction only**, not significant.

**C2 — scalar baseline.** Paired, two-sided Wilcoxon, G_OC vs S_OC.
- **Geometry exceeds scalar** iff p < 0.05 and median G_OC > median S_OC.
- **Scalar exceeds geometry** iff p < 0.05 and median S_OC > median G_OC.
- Otherwise a **tie**.
- *Secondary:* the control-normalised contrasts G_OC/G_SS vs S_OC/S_SS, same test.

**C3 — T0 eyes-open consistency.** Measure absolute occipital alpha power: the mean over the 7
channels of the alpha-band-passed variance, before z-scoring, over the selected windows. T0 is
**consistent with eyes open** iff |log(P_T0(R03)/P_R01)| < |log(P_R02/P_R01)| in ≥ 12/15
subjects. This is a consistency check, not a confirmation: eyes closed raises occipital alpha,
but other things change it too.

## Known biases, declared in advance
- **Span.** T0 windows span ~66 s of wall time, against 26 s for a baseline. So the temporal-half
  denominator of a T0 set spans more drift, which pushes the SS/OT ratios *down*. That makes the
  control easier to beat. An "exceeds" verdict in C1 is therefore weaker than it looks. A
  "not distinguishable" verdict is robust to this bias.
- **Task context.** T0 sits between motor trials: post-movement beta rebound and visual cueing
  may change occipital alpha. So SS compares two same-*kind* states, not a pure resting state.
- **Sample.** n = 15 subjects, one pair of task runs each.

Whatever the outcome, Paper 3 calls the eyes-open/closed result "a difference between two
recordings that exceeds each one's internal drift", not "structural discrimination", unless C1
returns *exceeds* **and** C2 does not return *scalar exceeds geometry*.
