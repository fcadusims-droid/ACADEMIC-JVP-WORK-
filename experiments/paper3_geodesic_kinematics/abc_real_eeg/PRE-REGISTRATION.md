# Do Experiments A and B Replicate on Real EEG? (Paper 3, appendix)

**Written before the run.**

## What is outstanding

Experiments **A** (`localization_multiscale`), **B** (`localization_priors`) and
**C** (`cross_dataset`) were all run **synthetically**, because PhysioNet was
unreachable from the execution environment at the time. Their conclusions are
load-bearing for Paper 3's appendix:

- **A** — the 5/15 localization failure is a *window-size* artifact. A single large
  window already reaches 15/15, matching a multiscale bank, so **the operative fix is
  window size and the multiscale machinery adds nothing.**
- **B** — causal smoothing of the predictability covariate *monotonically degrades*
  localization (0.36 → 0.07); the discriminator that works is persistence, not
  smoothing.

`sleep_stage_localization` (A1) later ran on real Sleep-EDF and reached 10/15 — but
it used a **single fixed large window** (`large_w = 40`) and never compared it
against a short window or against the multiscale bank. So A's actual claim — that
window size and not multiscale is what matters — has **never been tested on real
data**, and the STATUS entry saying real-EEG confirmation is no longer outstanding
overstates what A1 did. This experiment tests it.

## Question

On the same 15 real Sleep-EDF recordings and the same sleep-onset transitions A1
used, does A's conclusion replicate?

1. Does a **short** window localize materially worse than a **large** one?
2. Does a **multiscale bank** beat the single large window by a material margin, or
   does it merely match it?

And, as a real-data analogue of B:

3. Does **smoothing** the break curve before taking its maximum help?

## Method

Identical loading, filtering, windowing and transition selection to
`sleep_stage_localization` — the code is imported rather than reimplemented, so the
comparison is against A1's own numbers on A1's own recordings. Only the detector's
scale changes.

Arms, all scored by the same ±30 s tolerance A1 uses:

| arm | detector |
|---|---|
| `short_w5` | window-mean break curve, window 5 |
| `short_w10` | window-mean break curve, window 10 |
| `large_w40` | window-mean break curve, window 40 — **A1's setting, the reference** |
| `multiscale` | maximum of the normalized break curves over windows {5, 10, 20, 40} |
| `smoothed_w40` | window 40, break curve smoothed with a 5-window moving average before the maximum |

## Pre-registered criteria

- **A replicates** if (i) `large_w40` beats the better short window by **≥ 3 hits**
  out of 15, *and* (ii) `multiscale` is within **±1 hit** of `large_w40`. That is
  precisely A's claim: window size matters, multiscale does not add.
- **A partially replicates** if (i) holds but (ii) fails — i.e. multiscale beats the
  large window by ≥ 2 hits. Then the appendix's dismissal of the multiscale bank is
  wrong on real data and must be corrected.
- **A fails** if (i) fails — window size is not what drives the difference on real
  EEG, and the synthetic conclusion does not transfer.
- **B's analogue replicates** if `smoothed_w40` does **not** exceed `large_w40`
  (≤ 0 hits gained). A gain of ≥ 2 hits refutes the analogue.

Reported regardless of outcome: per-arm hit counts and median absolute errors.

## Scope limit, stated in advance

This tests A's window-size claim and a real-data **analogue** of B. It is **not** a
replication of B proper: B concerns smoothing the *predictability covariate* inside
the jump-anchoring pipeline, and smoothing the break curve is a different operation
on a different object. Whatever this arm shows, B itself remains synthetic-only, and
the result will say so rather than claiming more.

Experiment **C** is not tested here. Its content — robustness across paradigm
strength and fluctuation persistence — needs corpora varying along those axes, not a
second analysis of one corpus.

## Stopping rule

One run, five arms, on whatever subset of the 15 recordings yields a usable
transition under A1's existing criteria. No arm added after seeing results; no
tolerance or window changed after the fact.

## Status
Run on 16 recordings. Outcome: **A_REPLICATES — in direction, not in magnitude.**

| arm | hits | median error |
|---|---|---|
| `short_w5` | 2/16 | 63.5 s |
| `short_w10` | 4/16 | 50.5 s |
| **`large_w40`** | **7/16** | 33.5 s |
| `multiscale` | 6/16 | 36.0 s |
| `smoothed_w40` | 7/16 | 31.0 s |

Both halves of A's claim hold: the large window clears the pre-registered 3-hit margin
over the best short window, and the multiscale bank is within one hit rather than
beating it. **But the magnitude does not transfer** — synthetic A moved 2/15 → 15/15,
real data moves 4/16 → 7/16. The recommendation stands; the perfect synthetic score
gave an impression of a solved problem that real EEG does not support, and Paper 3 now
quotes the real number.

B's analogue is consistent with B (smoothing gains nothing, 7/16 either way), but it
remains an **analogue**: B smooths the predictability covariate inside the
jump-anchoring pipeline, a different object, so **B itself is still synthetic-only**.
**C is untested** and its STATUS row has been corrected — an earlier note claiming C's
real-EEG confirmation was no longer outstanding conflated C with A1/A3/Bench, which
test different things. See `_results/abc_real_eeg/result.json`.
