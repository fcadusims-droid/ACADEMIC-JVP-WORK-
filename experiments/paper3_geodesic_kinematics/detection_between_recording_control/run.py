"""Between-recording control for the held-out detection AUC (Paper 3).

See PRE-REGISTRATION.md. detection_repair_heldout's positives splice two recordings (R01+R02),
its nulls lie within one; this asks whether the scale-normalised CUSUM statistic separates a
STATE change (OC) from a RECORDING change with no state change (SS), on a common chunk structure.

Usage:
    python -m experiments.paper3_geodesic_kinematics.detection_between_recording_control.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

from experiments.paper3_geodesic_kinematics.detection_statistic_repair.run import (
    cusum_curve, stat_scale_normalised,
)
from experiments.paper3_geodesic_kinematics.baseline_benchmark.run import _auc
from experiments.paper3_geodesic_kinematics.detection_repair_heldout.run import (
    load_run, covs_of,
)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import DATA_DIR

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "detection_between_recording_control")
N_SUBJECTS = 15
CHUNK_SEC, SPACING_SEC, N_CHUNKS = 4.2, 8.3, 6
BAR, NOT_SHOWN = 0.70, 0.60


def edf_path(subject, run):
    from mne.datasets import eegbci
    return str(eegbci.load_data(subject, [run], path=DATA_DIR, update_path=False)[0])


def t0_onsets(path):
    import pyedflib
    r = pyedflib.EdfReader(path)
    on, dur, desc = r.readAnnotations()
    r.close()
    return [float(o) for o, d in zip(on, desc) if str(d).strip() == "T0"]


def chunks(data, fs, onsets, k):
    n = int(CHUNK_SEC * fs)
    out = [data[:, int(o * fs):int(o * fs) + n] for o in onsets[:k]]
    assert len(out) == k and all(c.shape[1] == n for c in out), "not enough chunks"
    return out


def stat(chs, fs):
    covs = covs_of(np.concatenate(chs, axis=1), fs)
    return float(stat_scale_normalised(cusum_curve(covs), covs))


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    spaced = [i * SPACING_SEC for i in range(N_CHUNKS)]
    rows = []
    for s in range(1, N_SUBJECTS + 1):
        p = {r: edf_path(s, r) for r in (1, 2, 3, 7)}
        d = {}
        for r in p:
            d[r], fs = load_run(p[r])
        oc = chunks(d[1], fs, spaced, N_CHUNKS) + chunks(d[2], fs, spaced, N_CHUNKS)
        ss = chunks(d[3], fs, t0_onsets(p[3]), N_CHUNKS) + chunks(d[7], fs, t0_onsets(p[7]), N_CHUNKS)
        wn = chunks(d[3], fs, t0_onsets(p[3]), 2 * N_CHUNKS)
        row = {"subject": f"S{s:03d}", "OC": stat(oc, fs), "SS": stat(ss, fs), "WN": stat(wn, fs)}
        rows.append(row)
        print(f"  S{s:03d}: OC {row['OC']:.3f}  SS {row['SS']:.3f}  WN {row['WN']:.3f}", flush=True)

    v = {k: [r[k] for r in rows] for k in ("OC", "SS", "WN")}
    d1 = float(_auc(v["OC"], v["SS"]))
    d2 = float(_auc(v["SS"], v["WN"]))
    d_oc_wn = float(_auc(v["OC"], v["WN"]))
    if d1 >= BAR:
        c1 = "STATE DETECTION SHOWN"
    elif d1 < NOT_SHOWN:
        c1 = "STATE DETECTION NOT SHOWN"
    else:
        c1 = "WEAK / INCONCLUSIVE"
    c2 = ("the statistic fires on a recording change alone" if d2 >= BAR
          else "a recording change alone does not reach the bar")
    verdict = (
        f"{c1}: AUC(eyes-open/closed splice vs same-state between-recording splice) = {d1:.3f} "
        f"(bar {BAR}, not-shown below {NOT_SHOWN}). Secondary: AUC(same-state splice vs "
        f"within-recording) = {d2:.3f} -- {c2}. The held-out design rebuilt on chunks, "
        f"AUC(eyes-open/closed splice vs within-recording) = {d_oc_wn:.3f} (committed held-out "
        f"figure 0.824). n = {len(rows)} subjects, unpaired AUCs over 15 vs 15 (about +/-0.1). "
        + ("Per the pre-registration, detection_repair_heldout's 0.824 is not evidence of state "
           "detection: the statistic does not separate a change of state from a change of "
           "recording." if c1 == "STATE DETECTION NOT SHOWN" else ""))
    print("\n" + verdict)
    json.dump({"experiment": "detection_between_recording_control",
               "question": "Does the held-out detection statistic separate a state change from a recording change?",
               "data": "PhysioNet eegmmidb S001-S015: R01, R02 spaced chunks; T0 chunks of R03, R07",
               "params": {"chunk_sec": CHUNK_SEC, "spacing_sec": SPACING_SEC,
                          "n_chunks_per_side": N_CHUNKS, "bar": BAR, "not_shown_below": NOT_SHOWN},
               "auc_OC_vs_SS": d1, "auc_SS_vs_WN": d2, "auc_OC_vs_WN": d_oc_wn,
               "outcome": c1, "verdict": verdict, "per_subject": rows},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
