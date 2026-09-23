"""Between-recording negative control and scalar baseline for the eyes-open/closed ratio.

See PRE-REGISTRATION.md. The eyes-open/closed temporal-half ratio (eeg_reconciliation)
compares two separate recordings in its numerator and two halves of one recording in its
denominator. This run computes the same statistic on two separate recordings of the SAME
state (T0 rest of two task runs), and a per-channel relative-alpha-power scalar baseline.

Usage:
    python -m experiments.paper3_geodesic_kinematics.between_recording_control.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
from scipy.stats import wilcoxon

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    sliding_covs, mean_density, DATA_DIR,
    N_SUBJECTS, CHANNELS, ALPHA_BAND, SEG_SEC, WIN_SEC, STEP_SEC,
)

warnings.filterwarnings("ignore")
HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "between_recording_control")
RECON = os.path.join(HERE, "..", "..", "_results", "eeg_reconciliation", "result.json")
BROAD = (1.0, 40.0)
W_SECOND_START = 34.0     # secondary arm W: R01[0,26) vs R01[34,60)


def load_run(subject, run):
    """(z-scored alpha data, raw alpha data, unfiltered data, sfreq, T0 intervals)."""
    import mne
    from mne.datasets import eegbci
    paths = eegbci.load_data(subject, [run], path=DATA_DIR, update_path=False)
    raw = mne.io.read_raw_edf(str(paths[0]), preload=True, verbose="ERROR")
    eegbci.standardize(raw)
    raw.pick(CHANNELS)
    sf = raw.info["sfreq"]
    unfilt = raw.get_data().copy()
    ann = raw.annotations
    t0 = [(o, o + d) for desc, o, d in zip(ann.description, ann.onset, ann.duration)
          if desc == "T0"]
    raw.filter(*ALPHA_BAND, verbose="ERROR")
    alpha = raw.get_data()
    z = (alpha - alpha.mean(axis=1, keepdims=True)) / (alpha.std(axis=1, keepdims=True) + 1e-12)
    return z, alpha, unfilt, sf, t0


def window_starts(n_times, sf):
    w, step = int(WIN_SEC * sf), int(STEP_SEC * sf)
    return list(range(0, n_times - w + 1, step)), w


def rel_alpha(seg, sf):
    """Per-channel relative alpha power of one window (Hann periodogram)."""
    x = seg - seg.mean(axis=1, keepdims=True)
    x = x * np.hanning(x.shape[1])[None, :]
    p = np.abs(np.fft.rfft(x, axis=1)) ** 2
    f = np.fft.rfftfreq(x.shape[1], 1.0 / sf)
    a = p[:, (f >= ALPHA_BAND[0]) & (f <= ALPHA_BAND[1])].sum(axis=1)
    b = p[:, (f >= BROAD[0]) & (f <= BROAD[1])].sum(axis=1)
    return a / (b + 1e-30)


def windows_from(z, alpha, unfilt, sf, starts, w):
    """For given window starts: geometry covs, scalar vectors, absolute alpha power."""
    covs = []
    for s in starts:
        covs += sliding_covs(z[:, s:s + w], sf)          # exactly one window each
    scal = np.array([rel_alpha(unfilt[:, s:s + w], sf) for s in starts])
    power = float(np.mean([alpha[:, s:s + w].var(axis=1).mean() for s in starts]))
    return {"covs": covs, "scal": scal, "power": power}


def baseline_set(run_data, t_from, n_win):
    z, alpha, unfilt, sf, _ = run_data
    all_starts, w = window_starts(z.shape[1], sf)
    s0 = int(round(t_from * sf))
    starts = [s for s in all_starts if s >= s0][:n_win]
    assert len(starts) == n_win, "baseline too short"
    return windows_from(z, alpha, unfilt, sf, starts, w)


def t0_set(run_data, n_win):
    z, alpha, unfilt, sf, t0 = run_data
    all_starts, w = window_starts(z.shape[1], sf)
    inside = [s for s in all_starts
              if any(a * sf <= s and s + w <= b * sf for a, b in t0)]
    starts = inside[:n_win]
    assert len(starts) == n_win, f"only {len(inside)} T0 windows"
    span = (starts[-1] + w - starts[0]) / sf
    out = windows_from(z, alpha, unfilt, sf, starts, w)
    out["span_s"] = float(span)
    return out


def th_geo(covs):
    h = len(covs) // 2
    return spd.sqrt_distance(mean_density(covs[:h]), mean_density(covs[h:]))


def th_scal(v):
    h = len(v) // 2
    return float(np.linalg.norm(v[:h].mean(0) - v[h:].mean(0)))


def ratio_geo(A, B):
    num = spd.sqrt_distance(mean_density(A["covs"]), mean_density(B["covs"]))
    return float(num / (0.5 * (th_geo(A["covs"]) + th_geo(B["covs"])) + 1e-9))


def ratio_scal(A, B):
    num = np.linalg.norm(A["scal"].mean(0) - B["scal"].mean(0))
    return float(num / (0.5 * (th_scal(A["scal"]) + th_scal(B["scal"])) + 1e-12))


def analyse_subject(s):
    r1, r2, r3, r7 = (load_run(s, r) for r in (1, 2, 3, 7))
    sf = r1[3]
    n_win = len(window_starts(int(SEG_SEC * sf), sf)[0])
    o = baseline_set(r1, 0.0, n_win)
    c = baseline_set(r2, 0.0, n_win)
    o_late = baseline_set(r1, W_SECOND_START, n_win)
    t3 = t0_set(r3, n_win)
    t7 = t0_set(r7, n_win)
    arms = {"OC": (o, c), "SS": (t3, t7), "OT": (o, t3), "W": (o, o_late)}
    row = {"subject": s, "n_windows": n_win, "t0_span_s": [t3["span_s"], t7["span_s"]]}
    for k, (A, B) in arms.items():
        row[f"G_{k}"] = ratio_geo(A, B)
        row[f"S_{k}"] = ratio_scal(A, B)
    row["alpha_power"] = {"R01": o["power"], "R02": c["power"], "T0_R03": t3["power"]}
    row["t0_closer_to_open"] = bool(abs(np.log(t3["power"] / o["power"]))
                                    < abs(np.log(c["power"] / o["power"])))
    return row


def wx(x, alternative):
    try:
        return float(wilcoxon(x, alternative=alternative).pvalue)
    except Exception:
        return float("nan")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = []
    for s in range(1, N_SUBJECTS + 1):
        r = analyse_subject(s)
        rows.append(r)
        print(f"S{s:03d} " + " ".join(f"{k}={r[k]:.2f}" for k in
              ("G_OC", "G_SS", "G_OT", "G_W", "S_OC", "S_SS", "S_OT", "S_W"))
              + f" T0~open={r['t0_closer_to_open']}")
    a = lambda k: np.array([r[k] for r in rows])
    n = len(rows)
    med = {k: float(np.median(a(k))) for k in
           ("G_OC", "G_SS", "G_OT", "G_W", "S_OC", "S_SS", "S_OT", "S_W")}

    # sanity gate
    recon = json.load(open(RECON))["temporal_half"]["median_ratio"]
    sanity_ok = abs(med["G_OC"] - recon) <= 0.01

    # C1
    d1 = a("G_OC") - a("G_SS")
    p1 = wx(d1, "greater")
    n_oc_gt_ss = int(np.sum(d1 > 0))
    if p1 < 0.05 and n_oc_gt_ss >= 11:
        c1 = "EXCEEDS the same-state between-recording control"
    elif med["G_SS"] >= med["G_OC"] or p1 >= 0.2:
        c1 = "NOT DISTINGUISHABLE from a between-recording difference"
    else:
        c1 = "DIRECTION ONLY (not significant)"
    p1_ot = wx(a("G_OC") - a("G_OT"), "greater")

    # C2
    p2 = wx(a("G_OC") - a("S_OC"), "two-sided")
    if p2 < 0.05 and med["G_OC"] > med["S_OC"]:
        c2 = "GEOMETRY EXCEEDS scalar"
    elif p2 < 0.05 and med["S_OC"] > med["G_OC"]:
        c2 = "SCALAR EXCEEDS geometry"
    else:
        c2 = "TIE"
    cg, cs = a("G_OC") / a("G_SS"), a("S_OC") / a("S_SS")
    p2b = wx(cg - cs, "two-sided")

    # C3
    n_open = int(sum(r["t0_closer_to_open"] for r in rows))
    c3 = ("CONSISTENT with eyes open" if n_open >= 12
          else "NOT consistent with eyes open")

    may_say_structural = c1.startswith("EXCEEDS") and not c2.startswith("SCALAR")
    # Lead with the pre-registered consequence: the site index compresses verdicts, and a
    # string opening "C1: EXCEEDS" would read as a win when C2 says the scalar beats it.
    lead = ("MAY BE CALLED STRUCTURAL DISCRIMINATION (C1 exceeds, C2 not scalar-dominated). "
            if may_say_structural else
            "NOT STRUCTURAL DISCRIMINATION: a between-recording difference that per-channel "
            "alpha power separates more strongly. ")
    verdict = (
        lead
        + (f"INSTRUMENT DEFECT: sanity gate failed (G_OC median {med['G_OC']:.3f} vs committed "
         f"{recon:.3f}); no verdict. " if not sanity_ok else "")
        + f"C1: {c1}. Geometry ratio R01-vs-R02 median {med['G_OC']:.2f}; same-state control "
        f"T0(R03)-vs-T0(R07) median {med['G_SS']:.2f}; OC > SS in {n_oc_gt_ss}/{n} subjects, "
        f"one-sided Wilcoxon p = {p1:.3g}. The review's control R01-vs-T0(R03) median "
        f"{med['G_OT']:.2f} (OC > OT p = {p1_ot:.3g}); within-R01 separate segments median "
        f"{med['G_W']:.2f}. "
        f"C2: {c2}. Scalar relative-alpha ratio R01-vs-R02 median {med['S_OC']:.2f} vs geometry "
        f"{med['G_OC']:.2f}, two-sided Wilcoxon p = {p2:.3g}; scalar same-state control median "
        f"{med['S_SS']:.2f}; control-normalised contrast geometry median {np.median(cg):.2f} vs "
        f"scalar {np.median(cs):.2f}, p = {p2b:.3g}. "
        f"C3: {c3} ({n_open}/{n} subjects have T0 occipital alpha power closer to R01 than R02 is). "
        + ("Paper 3 may call the result structural discrimination only as pre-registered."
           if may_say_structural else
           "Paper 3 must describe the eyes-open/closed result as a difference between two "
           "recordings that exceeds each one's internal drift, not as structural discrimination.")
    )
    print(verdict)

    summary = {
        "experiment": "between_recording_control",
        "data": "PhysioNet eegmmidb S001-S015: R01, R02 baselines; T0 rest of R03, R07",
        "params": {"channels": CHANNELS, "alpha_band": ALPHA_BAND, "broad_band": BROAD,
                   "seg_sec": SEG_SEC, "win_sec": WIN_SEC, "step_sec": STEP_SEC,
                   "w_second_start": W_SECOND_START},
        "sanity": {"committed_temporal_half_median": recon, "reproduced": med["G_OC"],
                   "ok": bool(sanity_ok)},
        "medians": med,
        "C1": {"verdict": c1, "wilcoxon_p_OC_gt_SS": p1, "n_OC_gt_SS": n_oc_gt_ss, "n": n,
               "wilcoxon_p_OC_gt_OT": p1_ot},
        "C2": {"verdict": c2, "wilcoxon_p_G_vs_S": p2,
               "contrast_geo_median": float(np.median(cg)),
               "contrast_scalar_median": float(np.median(cs)), "wilcoxon_p_contrast": p2b},
        "C3": {"verdict": c3, "n_t0_closer_to_open": n_open, "n": n},
        "may_call_structural_discrimination": bool(may_say_structural),
        "verdict": verdict,
        "per_subject": rows,
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
