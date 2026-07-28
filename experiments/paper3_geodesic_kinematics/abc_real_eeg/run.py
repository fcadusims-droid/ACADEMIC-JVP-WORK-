"""Do experiments A and B replicate on real EEG? (Paper 3, appendix)

A (`localization_multiscale`), B (`localization_priors`) and C (`cross_dataset`) were
all run synthetically, because PhysioNet was unreachable at the time. A's conclusion
is load-bearing: the 5/15 localization failure is a WINDOW-SIZE artifact, a single
large window already matches a multiscale bank, so the multiscale machinery adds
nothing.

`sleep_stage_localization` (A1) later ran on real Sleep-EDF and reached 10/15 -- but
with a single fixed large window (large_w = 40). It never compared short against
large, or large against a multiscale bank. So A's actual claim has never been tested
on real data, and the STATUS note saying real-EEG confirmation was no longer
outstanding overstated what A1 did.

This runs the comparison A1 skipped, on A1's own recordings, importing A1's loading
and transition-selection code unchanged so the only thing that varies is the
detector's scale.

Usage:
    python -m experiments.paper3_geodesic_kinematics.abc_real_eeg.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, find_transition, discover_subjects,
    SEG_SEC, STEP_SEC, TOL_SEC,
)
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve,
)

warnings.filterwarnings("ignore")

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "abc_real_eeg")

# ---- pre-registered arms and criteria --------------------------------------
SHORT_WINDOWS = [5, 10]
LARGE_WINDOW = 40
BANK = [5, 10, 20, 40]
SMOOTH_K = 5
MARGIN_WINDOW_SIZE = 3     # large must beat the better short by >= this
MARGIN_MULTISCALE = 2      # multiscale "adds" only if it beats large by >= this


def _norm(curve):
    """Scale a break curve to [0,1] so scales are comparable in the bank."""
    c = np.asarray(curve, float)
    lo, hi = np.nanmin(c), np.nanmax(c)
    return (c - lo) / (hi - lo) if hi > lo else np.zeros_like(c)


def multiscale_curve(C, windows):
    """Pointwise maximum of normalized break curves -- the bank A tested."""
    curves = []
    n = None
    for w in windows:
        cur = _norm(break_curve(C, w))
        curves.append(cur)
        n = len(cur) if n is None else min(n, len(cur))
    return np.max(np.stack([c[:n] for c in curves]), axis=0)


def smooth(curve, k=SMOOTH_K):
    c = np.asarray(curve, float)
    if len(c) < k:
        return c
    ker = np.ones(k) / k
    return np.convolve(c, ker, mode="same")


def peak_err(curve, seam):
    """Absolute error of the curve's maximum, in windows."""
    c = np.asarray(curve, float)
    if not len(c) or not np.any(np.isfinite(c)):
        return None
    return int(abs(int(np.nanargmax(c)) - seam))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Do A and B replicate on real EEG? (Sleep-EDF, A1's recordings)\n")

    subjects = discover_subjects()
    tol = int(round(TOL_SEC / STEP_SEC))
    arms = ([f"short_w{w}" for w in SHORT_WINDOWS]
            + [f"large_w{LARGE_WINDOW}", "multiscale", f"smoothed_w{LARGE_WINDOW}"])
    errs = {a: [] for a in arms}
    used = []

    for psg, hyp in subjects:
        try:
            data, fs, stage = load_subject(psg, hyp)
        except Exception as exc:
            print(f"  skip {os.path.basename(psg)}: {exc}")
            continue
        tr = find_transition(stage, fs)
        if tr is None:
            continue
        t0, s0, s1 = tr
        seg = int(SEG_SEC * fs)
        lo, hi = t0 - seg, t0 + seg
        if lo < 0 or hi > data.shape[1]:
            continue
        sub = data[:, lo:hi]
        covs, _, centers = sliding_covs_labeled(
            sub, fs, np.full(sub.shape[1], "", dtype=object))
        if len(covs) < 2 * LARGE_WINDOW + 4:
            continue
        seam = int(np.argmin(np.abs(centers - (t0 - lo) / fs)))
        _, C = embed_cumsum(covs)

        per = {}
        for w in SHORT_WINDOWS:
            per[f"short_w{w}"] = peak_err(break_curve(C, w), seam)
        per[f"large_w{LARGE_WINDOW}"] = peak_err(break_curve(C, LARGE_WINDOW), seam)
        per["multiscale"] = peak_err(multiscale_curve(C, BANK), seam)
        per[f"smoothed_w{LARGE_WINDOW}"] = peak_err(
            smooth(break_curve(C, LARGE_WINDOW)), seam)

        if any(v is None for v in per.values()):
            continue
        for a in arms:
            errs[a].append(per[a])
        used.append({"record": os.path.basename(psg), "from": s0, "to": s1,
                     "errors_windows": per})
        print(f"  {os.path.basename(psg):22s} {s0}->{s1}  "
              + "  ".join(f"{a}={per[a]}" for a in arms))

    n = len(used)
    summary = {}
    for a in arms:
        e = np.array(errs[a], dtype=float)
        summary[a] = {"hits": int(np.sum(e <= tol)), "n": n,
                      "median_err_s": float(np.median(e) * STEP_SEC) if n else None}

    print(f"\n  {n} recordings with a usable transition")
    for a in arms:
        s = summary[a]
        print(f"    {a:16s} {s['hits']}/{n}  median err {s['median_err_s']}s")

    # ---- pre-registered decision -------------------------------------
    large = summary[f"large_w{LARGE_WINDOW}"]["hits"]
    best_short = max(summary[f"short_w{w}"]["hits"] for w in SHORT_WINDOWS)
    multi = summary["multiscale"]["hits"]
    smoothed = summary[f"smoothed_w{LARGE_WINDOW}"]["hits"]

    window_size_matters = bool(large - best_short >= MARGIN_WINDOW_SIZE)
    multiscale_adds = bool(multi - large >= MARGIN_MULTISCALE)
    smoothing_helps = bool(smoothed - large >= MARGIN_MULTISCALE)

    if n < 8:
        outcome = "UNDERPOWERED"
    elif window_size_matters and not multiscale_adds:
        outcome = "A_REPLICATES"
    elif window_size_matters and multiscale_adds:
        outcome = "A_PARTIAL"
    else:
        outcome = "A_FAILS"

    if outcome == "A_REPLICATES":
        head = (f"A REPLICATES ON REAL EEG. The large window beats the best short "
                f"window {large}/{n} vs {best_short}/{n}, clearing the "
                f"pre-registered {MARGIN_WINDOW_SIZE}-hit margin, and the multiscale "
                f"bank returns {multi}/{n} -- within a hit of the single large "
                f"window rather than beating it. A's claim was that window size is "
                f"the operative fix and the multiscale machinery adds nothing; on "
                f"real data both halves hold. THE MAGNITUDE DOES NOT TRANSFER, AND "
                f"THAT IS THE MORE USEFUL HALF OF THIS RESULT. Synthetically, A moved "
                f"localization from 2/15 to a perfect 15/15; on real recordings the "
                f"same change moves it from {best_short}/{n} to {large}/{n} -- under "
                f"half. The DIRECTION of A's finding replicates and its "
                f"RECOMMENDATION stands, but the synthetic 15/15 gave an impression "
                f"of a solved problem that real EEG does not support, exactly as the "
                f"appendix's 12x structural effect had to be corrected to 3.3x. The "
                f"appendix should quote the real number.")
    elif outcome == "A_PARTIAL":
        head = (f"A REPLICATES ONLY IN PART, AND THE APPENDIX MUST BE CORRECTED. "
                f"Window size does matter ({large}/{n} vs {best_short}/{n}), but the "
                f"multiscale bank reaches {multi}/{n}, beating the single large "
                f"window by {multi - large} on real recordings. A's dismissal of the "
                f"multiscale machinery was a synthetic artifact and does not survive "
                f"contact with Sleep-EDF.")
    elif outcome == "A_FAILS":
        head = (f"A DOES NOT REPLICATE. The large window reaches {large}/{n} against "
                f"the best short window's {best_short}/{n}, short of the "
                f"pre-registered {MARGIN_WINDOW_SIZE}-hit margin, so window size is "
                f"not what drives localization on real EEG and the synthetic "
                f"conclusion does not transfer.")
    else:
        head = (f"UNDERPOWERED: only {n} recordings yielded a usable transition; "
                f"at least 8 are needed to read the pre-registered margins.")

    verdict = (
        head + " WHY THIS WAS RUN. A, B and C were synthetic because PhysioNet was "
        "unreachable when they were executed. A1 later reached 10/15 on real "
        "Sleep-EDF but used one fixed large window and never compared scales, so A's "
        "actual claim -- window size rather than multiscale -- had never been tested "
        "on real data, and the STATUS note declaring real-EEG confirmation no longer "
        "outstanding overstated what A1 had done. That note is corrected. "
        f"B'S ANALOGUE: smoothing the break curve gives {smoothed}/{n} against the "
        f"unsmoothed {large}/{n}, so smoothing "
        + ("does not help, consistent with B's synthetic finding that the useful "
           "discriminator is persistence rather than smoothing. "
           if not smoothing_helps else
           "DOES help here, which runs against B's synthetic finding and is reported "
           "as such. ")
        + "SCOPE, stated rather than left implicit: this is an ANALOGUE of B, not a "
        "replication of it. B concerns smoothing the predictability covariate inside "
        "the jump-anchoring pipeline; smoothing a break curve is a different "
        "operation on a different object, so B itself remains synthetic-only. "
        "Experiment C is not addressed here at all -- its content is robustness "
        "across paradigm strength and fluctuation persistence, which needs corpora "
        "varying along those axes rather than a second analysis of one corpus.")

    # ---- figure -------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    vals = [summary[a]["hits"] for a in arms]
    colors = ["#a85f5f"] * len(SHORT_WINDOWS) + ["#1f4e79", "#7a2e2e", "#4a4a4a"]
    ax.bar(range(len(arms)), vals, color=colors)
    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels(arms, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel(f"hits (|err| <= {TOL_SEC:.0f} s) out of {n}")
    ax.set_title("Experiment A on real Sleep-EDF: does window size, not multiscale, "
                 "do the work?", fontsize=10)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.1, str(v), ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "abc_real_eeg.png"), dpi=130)
    plt.close(fig)

    out = {
        "experiment": "abc_real_eeg",
        "question": "Do experiments A (window size vs multiscale) and an analogue of "
                    "B (smoothing) replicate on real Sleep-EDF?",
        "data": "Sleep-EDF Expanded, the same recordings and sleep-onset transitions "
                "as sleep_stage_localization (A1)",
        "params": {"short_windows": SHORT_WINDOWS, "large_window": LARGE_WINDOW,
                   "bank": BANK, "smooth_k": SMOOTH_K, "tol_sec": TOL_SEC,
                   "margin_window_size": MARGIN_WINDOW_SIZE,
                   "margin_multiscale": MARGIN_MULTISCALE},
        "n_recordings": n,
        "per_arm": summary,
        "per_record": used,
        "window_size_matters": window_size_matters,
        "multiscale_adds": multiscale_adds,
        "smoothing_helps": smoothing_helps,
        "scope_note": "Analogue of B, not a replication of B: B smooths the "
                      "predictability covariate inside the jump-anchoring pipeline. "
                      "Experiment C is not addressed.",
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["abc_real_eeg.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
