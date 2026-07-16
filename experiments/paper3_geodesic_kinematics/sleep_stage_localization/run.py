"""Trilha A1 -- Sleep-stage structural discrimination + localization (Paper 3).

Generalization test on a SECOND real paradigm: PhysioNet Sleep-EDF. Sleep-stage
transitions are slow, consistent, physiologically structural events (spindles,
delta, REM eye-movements reorganize the spatial correlation between anterior EEG,
posterior EEG and EOG) -- the opposite of the sustained spontaneous alpha bursts
that capped eyes-open/closed localization at 4-5/15. Reuses the appendix detectors
verbatim; only the data loader is new.

Test 1: N2-vs-REM structural discrimination under the committed within-state
        permutation null (>= 12/15 = generalizes).
Test 2: within-trajectory localization of a clean stage transition with the
        geodesic CUSUM (>= 10/15 = generalizes; ~8/15 or below = a METHOD limit,
        since a slow consistent transition is the easiest case localization faces).

Usage:
    python -m experiments.paper3_geodesic_kinematics.sleep_stage_localization.run
"""
from __future__ import annotations

import glob
import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve, _R,
)
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    changepoint_fratio, cusum_changepoint, _hit,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "sleep_stage_localization")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sleep-edfx")

# ---- pre-fixed parameters (see PRE-REGISTRATION.md) --------------------------
N_SUBJECTS = 15
WANT_CH = ["EEG Fpz-Cz", "EEG Pz-Oz", "EOG horizontal"]
BAND = (0.5, 30.0)
WIN_SEC = 2.0
STEP_SEC = 1.0
EIG_FLOOR = 1e-3
EPOCH_SEC = 30.0
LARGE_W = 40            # persistence-sensitive window (windows), ~40 s each side
MIN_SEG_SEC = 20.0
TOL_SEC = 30.0          # +/- one scoring epoch
SEG_SEC = 90.0          # each side of a localization transition
DISC_STAGES = ("N2", "REM")
N_PERM = 500
STAGE_MAP = {"Sleep stage W": "W", "Sleep stage 1": "N1", "Sleep stage 2": "N2",
             "Sleep stage 3": "N3", "Sleep stage 4": "N3", "Sleep stage R": "REM"}


# ======================================================================
#  Sleep-EDF loader (pyedflib) -> (data[3,n], fs, per-sample stage array)
# ======================================================================
def _match_channel(labels, want):
    for i, lab in enumerate(labels):
        if lab.strip() == want:
            return i
    for i, lab in enumerate(labels):        # loose fallback
        if want.lower().replace(" ", "") in lab.lower().replace(" ", ""):
            return i
    raise ValueError(f"channel {want!r} not in {labels}")


def load_subject(psg_path, hyp_path):
    import pyedflib
    r = pyedflib.EdfReader(psg_path)
    labels = [r.getLabel(i) for i in range(r.signals_in_file)]
    idx = [_match_channel(labels, w) for w in WANT_CH]
    fs = float(r.getSampleFrequency(idx[0]))
    data = np.array([r.readSignal(i) for i in idx])          # (3, n)
    r.close()
    n = data.shape[1]
    # hypnogram -> per-sample stage
    hr = pyedflib.EdfReader(hyp_path)
    onsets, durs, descs = hr.readAnnotations()
    hr.close()
    stage = np.full(n, "", dtype=object)
    for o, d, desc in zip(onsets, durs, descs):
        s = STAGE_MAP.get(str(desc).strip())
        if s is None:
            continue
        lo, hi = int(round(o * fs)), int(round((o + d) * fs))
        stage[max(0, lo):min(n, hi)] = s
    # bandpass + per-channel z-score (seam = structure, not power)
    b, a = butter(4, [BAND[0] / (fs / 2), BAND[1] / (fs / 2)], btype="band")
    data = filtfilt(b, a, data, axis=1)
    data = (data - data.mean(1, keepdims=True)) / (data.std(1, keepdims=True) + 1e-12)
    return data, fs, stage


def sliding_covs_labeled(data, fs, stage):
    """Sliding covariances + the majority stage label per window."""
    w, step = int(WIN_SEC * fs), int(STEP_SEC * fs)
    covs, labs, centers = [], [], []
    for start in range(0, data.shape[1] - w + 1, step):
        seg = data[:, start:start + w]
        c = spd.trace_normalize(spd.eigfloor(np.cov(seg), EIG_FLOOR))
        covs.append(c)
        win_stage = stage[start:start + w]
        vals, cnts = np.unique(win_stage[win_stage != ""], return_counts=True)
        labs.append(vals[np.argmax(cnts)] if len(vals) else "")
        centers.append((start + w / 2) / fs)
    return covs, np.array(labs, dtype=object), np.array(centers)


# ======================================================================
#  Test 1 -- structural discrimination with within-state permutation null
# ======================================================================
def _mean_density(covs):
    embs = np.mean([spd.sqrt_embed(c) for c in covs], axis=0)
    nrm = np.sqrt(np.sum(embs * embs))
    return spd.sqrt_unembed(embs * (_R / nrm)) if nrm > 1e-12 else spd.sqrt_unembed(embs)


def _ratio(embA, embB):
    """between/within ratio from two groups of embedded covs (arrays (n,d,d))."""
    def gmean(E):
        m = E.mean(0); nrm = np.sqrt(np.sum(m * m))
        return m * (_R / nrm) if nrm > 1e-12 else m
    def sphere_d(p, q):
        return 2.0 * np.arccos(np.clip(np.sum(p * q) / (_R * _R), -1.0, 1.0))
    mA, mB = gmean(embA), gmean(embB)
    between = sphere_d(mA, mB)
    def within(E):
        h = len(E) // 2
        return sphere_d(gmean(E[:h]), gmean(E[h:]))
    return between / (0.5 * (within(embA) + within(embB)) + 1e-9)


def discrimination(covs, labs, rng):
    A = [spd.sqrt_embed(c) for c, l in zip(covs, labs) if l == DISC_STAGES[0]]
    B = [spd.sqrt_embed(c) for c, l in zip(covs, labs) if l == DISC_STAGES[1]]
    if len(A) < 10 or len(B) < 10:
        return None
    A, B = np.array(A), np.array(B)
    obs = _ratio(A, B)
    pool = np.concatenate([A, B]); nA = len(A)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        perm = rng.permutation(len(pool))
        null[i] = _ratio(pool[perm[:nA]], pool[perm[nA:]])
    p = float((np.sum(null >= obs) + 1) / (N_PERM + 1))
    return {"ratio": float(obs), "p": p, "n_A": int(nA), "n_B": int(len(B)),
            "pass": bool(obs > 1.0 and p < 0.05), "null_median": float(np.median(null))}


# ======================================================================
#  Test 2 -- localization of a clean stage transition
# ======================================================================
def find_transition(stage, fs):
    """First stage boundary of a structural type with >= SEG_SEC contiguous single
    stage on each side. Structural = involves REM or Wake (largest spatial change)."""
    seg = int(SEG_SEC * fs)
    # collapse per-sample stage into runs
    runs = []
    cur, start = stage[0], 0
    for i in range(1, len(stage)):
        if stage[i] != cur:
            runs.append((cur, start, i)); cur, start = stage[i], i
    runs.append((cur, start, len(stage)))
    runs = [(s, a, b) for (s, a, b) in runs if s in ("W", "N1", "N2", "N3", "REM")]
    for k in range(1, len(runs)):
        (s0, a0, b0), (s1, a1, b1) = runs[k - 1], runs[k]
        if s0 == s1:
            continue
        struct = ("REM" in (s0, s1)) or ("W" in (s0, s1))
        if struct and (b0 - a0) >= seg and (b1 - a1) >= seg:
            return b0, s0, s1          # transition sample index, from-stage, to-stage
    return None


def localize(data, fs, stage):
    tr = find_transition(stage, fs)
    if tr is None:
        return None
    t0, s0, s1 = tr
    seg = int(SEG_SEC * fs)
    lo, hi = t0 - seg, t0 + seg
    sub = data[:, lo:hi]
    covs, _, centers = sliding_covs_labeled(sub, fs, np.full(sub.shape[1], "", dtype=object))
    seam = int(np.argmin(np.abs(centers - (t0 - lo) / fs)))
    tol = int(round(TOL_SEC / STEP_SEC))
    min_seg = int(round(MIN_SEG_SEC / STEP_SEC))
    E, C = embed_cumsum(covs)
    win = break_curve(C, LARGE_W)
    fr = changepoint_fratio(E, C, min_seg)
    cu = cusum_changepoint(E, C, min_seg)
    tw, ew, hw, pw = _hit(win, seam, tol)
    tf, ef, hf, pf = _hit(fr, seam, tol)
    tc, ec, hc, pc = _hit(cu, seam, tol)
    return {"from": s0, "to": s1, "seam": int(seam), "n_windows": len(covs),
            "window_mean": {"err_s": ew * STEP_SEC, "hit": hw},
            "fratio": {"err_s": ef * STEP_SEC, "hit": hf},
            "cusum": {"err_s": ec * STEP_SEC, "hit": hc}}


# ======================================================================
def discover_subjects():
    psgs = sorted(glob.glob(os.path.join(DATA_DIR, "SC4*-PSG.edf")))
    out = []
    for p in psgs:
        pref = os.path.basename(p)[:6]
        hyps = glob.glob(os.path.join(DATA_DIR, pref + "*-Hypnogram.edf"))
        if hyps and os.path.getsize(p) > 1_000_000:
            out.append((p, hyps[0]))
    return out


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    subs = discover_subjects()
    print(f"Trilha A1 -- Sleep-EDF ({len(subs)} PSG/Hypnogram pairs on disk)")
    print(f"  channels {WANT_CH}, band {BAND} Hz, win {WIN_SEC}s/step {STEP_SEC}s, "
          f"disc {DISC_STAGES}, tol +/-{TOL_SEC}s")

    disc_rows, loc_rows = [], []
    for p, h in subs:
        pref = os.path.basename(p)[:6]
        if len(disc_rows) >= N_SUBJECTS:
            break
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            print(f"  {pref}: LOAD FAILED {type(e).__name__}: {str(e)[:70]}")
            continue
        covs, labs, centers = sliding_covs_labeled(data, fs, stage)
        d = discrimination(covs, labs, rng)
        l = localize(data, fs, stage)
        if d is None and l is None:
            print(f"  {pref}: no usable N2/REM bank and no qualifying transition -- skipped")
            continue
        row = {"subject": pref}
        if d is not None:
            disc_rows.append({"subject": pref, **d})
        if l is not None:
            loc_rows.append({"subject": pref, **l})
        dtxt = (f"ratio {d['ratio']:.2f} p{d['p']:.3f} {'PASS' if d['pass'] else '   '}"
                if d else "disc: n/a")
        ltxt = (f"{l['from']}->{l['to']} cusum e{l['cusum']['err_s']:.0f}s "
                f"{'HIT' if l['cusum']['hit'] else '   '}" if l else "loc: n/a")
        print(f"  {pref}: {dtxt} | {ltxt}")

    # ---- Test 1 verdict ----
    nd = len(disc_rows)
    disc_pass = int(sum(r["pass"] for r in disc_rows))
    # ---- Test 2 verdict ----
    nl = len(loc_rows)
    cu_hits = int(sum(r["cusum"]["hit"] for r in loc_rows))
    fr_hits = int(sum(r["fratio"]["hit"] for r in loc_rows))
    win_hits = int(sum(r["window_mean"]["hit"] for r in loc_rows))
    med_ratio = float(np.median([r["ratio"] for r in disc_rows])) if nd else float("nan")
    cu_med_err = float(np.median([r["cusum"]["err_s"] for r in loc_rows])) if nl else float("nan")

    disc_ok = nd >= 12 and disc_pass >= 12
    if nd < 12:
        disc_verdict = (f"UNDERPOWERED: only {nd} subjects had a usable N2/REM bank "
                        f"(need 15); of those {disc_pass} discriminate. Re-run with more "
                        f"downloaded subjects before reading the >=12/15 band.")
    elif disc_pass >= 12:
        disc_verdict = (f"GENERALIZES: N2-vs-REM structural discrimination passes the "
                        f"permutation null in {disc_pass}/{nd} subjects (median ratio "
                        f"{med_ratio:.2f}). The trace-normalized geometry discriminates a "
                        f"real structural regime beyond occipital alpha -- a second "
                        f"paradigm, as pre-registered.")
    else:
        disc_verdict = (f"DOES NOT GENERALIZE: only {disc_pass}/{nd} subjects discriminate "
                        f"N2 from REM under the permutation null (median ratio {med_ratio:.2f}) "
                        f"-- below the pre-registered 12/15. Reported as a real negative.")

    if nl < 10:
        loc_verdict = (f"UNDERPOWERED: only {nl} subjects had a qualifying transition "
                       f"(need >=10 to read the band); CUSUM {cu_hits}/{nl} so far.")
    elif cu_hits >= 10:
        loc_verdict = (f"LOCALIZATION GENERALIZES: geodesic CUSUM localizes the sleep-stage "
                       f"transition in {cu_hits}/{nl} subjects (median err {cu_med_err:.0f}s) "
                       f"-- vs 4/15 on eyes-open/closed. A slow consistent structural "
                       f"transition IS localizable within one trajectory; the appendix's "
                       f"5/15 limit was the spontaneous-alpha paradigm, not the method. "
                       f"(F-ratio {fr_hits}/{nl}, window-mean {win_hits}/{nl}.)")
    elif cu_hits >= 8:
        loc_verdict = (f"MATERIALLY BETTER, NOT SOLVED: CUSUM {cu_hits}/{nl} (median err "
                       f"{cu_med_err:.0f}s), above eyes-open/closed (4/15) but short of "
                       f"10/15. On-line localization improves on the easy sleep case but "
                       f"is still imperfect. (F-ratio {fr_hits}/{nl}, window-mean {win_hits}/{nl}.)")
    else:
        loc_verdict = (f"METHOD LIMIT confirmed: even on slow, consistent sleep-stage "
                       f"transitions -- the easiest case on-line localization can face -- "
                       f"the geodesic CUSUM reaches only {cu_hits}/{nl} (median err "
                       f"{cu_med_err:.0f}s). The localization bound is the METHOD's, not the "
                       f"eyes-open/closed paradigm's: a geodesic change-point on "
                       f"trace-normalized covariance does not reliably localize a structural "
                       f"transition within one trajectory. A stronger, publishable negative. "
                       f"(F-ratio {fr_hits}/{nl}, window-mean {win_hits}/{nl}.)")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    if nd:
        ratios = [r["ratio"] for r in disc_rows]
        ax[0].bar(range(nd), ratios, color=["steelblue" if r["pass"] else "gray" for r in disc_rows])
        ax[0].axhline(1.0, ls=":", color="k")
        ax[0].set_xticks(range(nd)); ax[0].set_xticklabels([r["subject"] for r in disc_rows], rotation=90, fontsize=6)
        ax[0].set_ylabel("between/within ratio (N2 vs REM)")
        ax[0].set_title(f"Test 1: structural discrimination {disc_pass}/{nd}")
    labels = ["window-mean", "F-ratio", "CUSUM"]
    vals = [win_hits, fr_hits, cu_hits]
    ax[1].bar([0, 1, 2], [v / max(nl, 1) for v in vals], color=["gray", "crimson", "steelblue"])
    ax[1].axhline(10 / 15, ls="--", color="green", lw=0.8, label=">=10/15 generalizes")
    ax[1].set_xticks([0, 1, 2]); ax[1].set_xticklabels(labels)
    ax[1].set_ylim(0, 1.05); ax[1].set_ylabel(f"localization hit (|err|<= {TOL_SEC}s)")
    ax[1].set_title(f"Test 2: transition localization (n={nl})")
    for i, v in enumerate(vals):
        ax[1].text(i, v / max(nl, 1) + 0.02, f"{v}/{nl}", ha="center")
    ax[1].legend(fontsize=8)
    fig.suptitle("Trilha A1: Sleep-EDF structural discrimination + localization", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "sleep_stage_localization.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "sleep_stage_localization",
        "data": "PhysioNet Sleep-EDF sleep-cassette; channels " + ",".join(WANT_CH),
        "params": {"band": BAND, "win_sec": WIN_SEC, "step_sec": STEP_SEC,
                   "disc_stages": DISC_STAGES, "tol_sec": TOL_SEC, "seg_sec": SEG_SEC,
                   "large_w": LARGE_W, "n_perm": N_PERM},
        "test1_discrimination": {"n": nd, "pass": disc_pass, "median_ratio": med_ratio,
                                 "per_subject": disc_rows, "verdict": disc_verdict},
        "test2_localization": {"n": nl, "cusum_hits": cu_hits, "fratio_hits": fr_hits,
                               "window_mean_hits": win_hits, "cusum_median_err_s": cu_med_err,
                               "per_subject": loc_rows, "verdict": loc_verdict},
        "figures": ["sleep_stage_localization.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print("TEST 1 (discrimination): " + disc_verdict)
    print("\nTEST 2 (localization):   " + loc_verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
