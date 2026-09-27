"""E3.1 -- matched control: the standard pipeline given this method's design (Paper 3, §2.6).

See PRE-REGISTRATION.md. `mdm_trap_control` with exactly two changes:
  1. each OAS covariance is divided by its trace;
  2. overlapping windows: 1 s / 0.25 s step (EEGMMIDB), 2 s / 1 s step (sleep; a window is kept
     only if every sample lies in one scored N2 or REM stage).
Everything else (classifier, channels, filtering, folds, subjects, records) is unchanged.

Usage:
    python -m experiments.paper3_geodesic_kinematics.mdm_matched_control.run
"""
from __future__ import annotations

import json
import os
import warnings
from multiprocessing import Pool

import numpy as np
from scipy.stats import wilcoxon
from sklearn.model_selection import GroupKFold, KFold

from experiments.paper3_geodesic_kinematics.mdm_trap_control.run import (
    blocked_folds, cv_score, MIN_PER_CLASS, N_FOLDS, N_EEG,
)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects,
)
from experiments.paper3_geodesic_kinematics.between_recording_control.run import load_run

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results", "mdm_matched_control")
SLEEP_WIN, SLEEP_STEP = 2.0, 1.0
EEG_WIN, EEG_STEP = 1.0, 0.25


def covs(epochs):
    """Change 1: OAS covariance, then divided by its trace."""
    from pyriemann.estimation import Covariances
    C = Covariances(estimator="oas").fit_transform(epochs)
    return C / np.trace(C, axis1=1, axis2=2)[:, None, None]


def sleep_windows(path, hyp):
    """Change 2 (sleep): 2 s windows, 1 s step, entirely inside one N2 or REM stage."""
    data, fs, stage = load_subject(path, hyp)
    n, step = int(SLEEP_WIN * fs), int(SLEEP_STEP * fs)
    X, y = [], []
    for s in range(0, data.shape[1] - n + 1, step):
        lab = stage[s:s + n]
        if lab[0] in ("N2", "REM") and np.all(lab == lab[0]):
            X.append(data[:, s:s + n])
            y.append(lab[0])
    return np.array(X), np.array(y)


def one_record(args):
    p, h = args
    name = os.path.basename(p)[:7]
    try:
        X, y = sleep_windows(p, h)
    except Exception as e:
        return name, None, f"load failed {type(e).__name__}"
    if len(y) == 0 or min((y == "N2").sum(), (y == "REM").sum()) < MIN_PER_CLASS:
        return name, None, "too few windows per class"
    C3, C2 = covs(X), covs(X[:, :2])
    bf = blocked_folds(y)
    shuf = list(KFold(N_FOLDS, shuffle=True, random_state=0).split(C3))
    r = {"record": name, "subject": name[3:5],
         "n_N2": int((y == "N2").sum()), "n_REM": int((y == "REM").sum()),
         "acc_eog_blocked": cv_score(C3, y, bf),
         "acc_noeog_blocked": cv_score(C2, y, bf),
         "acc_eog_shuffled": cv_score(C3, y, shuf)}
    return name, (r, C3.astype(np.float32), y), None


def sleep_part():
    rows, pooled = [], {"C3": [], "y": [], "rec": [], "subj": []}
    with Pool(4) as pool:
        for name, out, err in pool.imap(one_record, discover_subjects()):
            if out is None:
                print(f"  {name}: skipped ({err})", flush=True)
                continue
            r, C3, y = out
            rows.append(r)
            pooled["C3"].append(C3); pooled["y"].append(y)
            pooled["rec"] += [name] * len(y); pooled["subj"] += [name[3:5]] * len(y)
            print(f"  {name}: n={len(y)} EOG {r['acc_eog_blocked']:.2f} noEOG {r['acc_noeog_blocked']:.2f} "
                  f"shuffled {r['acc_eog_shuffled']:.2f}", flush=True)
    C = np.concatenate(pooled["C3"]).astype(float); y = np.concatenate(pooled["y"])
    rec, subj = np.array(pooled["rec"]), np.array(pooled["subj"])
    t3 = {}
    for key, g in (("grouped_by_recording", rec), ("grouped_by_subject", subj)):
        t3[key] = cv_score(C, y, list(GroupKFold(N_FOLDS).split(C, y, g)))
        print(f"  T3 {key}: {t3[key]:.4f}", flush=True)
    t3["n_windows_pooled"] = int(len(y))
    return rows, t3


def eeg_part():
    rows = []
    for s in range(1, N_EEG + 1):
        runs = {r: load_run(s, r) for r in (1, 2, 3, 7)}
        sf = runs[1][3]
        n, step = int(EEG_WIN * sf), int(EEG_STEP * sf)

        def base(r):
            x = runs[r][1]
            return np.array([x[:, a:a + n] for a in range(0, x.shape[1] - n + 1, step)])

        def t0(r):
            x, iv = runs[r][1], runs[r][4]
            st = []
            for a, b in iv:
                st += list(range(int(a * sf), int(b * sf) - n + 1, step))
            return np.array([x[:, a:a + n] for a in st])

        def score(A, B):
            k = min(len(A), len(B))
            X = np.concatenate([A[:k], B[:k]])
            yy = np.array(["a"] * k + ["b"] * k)
            return cv_score(covs(X), yy, blocked_folds(yy)), k

        oc, k_oc = score(base(1), base(2))
        ss, k_ss = score(t0(3), t0(7))
        rows.append({"subject": f"S{s:03d}", "acc_open_vs_closed": oc, "n_per_class_oc": k_oc,
                     "acc_same_state_T0_R03_vs_R07": ss, "n_per_class_ss": k_ss})
        print(f"  S{s:03d}: open/closed {oc:.2f} (n={k_oc})  same-state T0 {ss:.2f} (n={k_ss})", flush=True)
    return rows


def spread(v):
    v = np.asarray(v, float)
    return {"median": float(np.median(v)), "q25": float(np.percentile(v, 25)),
            "q75": float(np.percentile(v, 75)), "min": float(v.min()), "max": float(v.max()), "n": int(len(v))}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("E3.1 matched control (trace-normalized OAS covariances, overlapping windows) -> MDM")
    eeg_rows = eeg_part()
    sleep_rows, t3 = sleep_part()

    subj = {}
    for r in sleep_rows:
        subj.setdefault(r["subject"], []).append(r)
    drops = np.array([np.mean([x["acc_eog_blocked"] - x["acc_noeog_blocked"] for x in v]) for v in subj.values()])
    t1_p = float(wilcoxon(drops, alternative="greater").pvalue)
    t1_med = float(np.median(drops))
    ss = np.array([r["acc_same_state_T0_R03_vs_R07"] for r in eeg_rows])
    oc = np.array([r["acc_open_vs_closed"] for r in eeg_rows])
    d4 = np.array([r["acc_eog_shuffled"] - r["acc_eog_blocked"] for r in sleep_rows])
    t3_gap = t3["grouped_by_recording"] - t3["grouped_by_subject"]

    crosses = {"T4_dependence": bool(np.median(d4) >= 0.05),
               "T3_pseudoreplication": bool(t3_gap >= 0.05),
               "T1_ocular": bool(t1_med >= 0.05),
               "T2_recording": bool(np.median(ss) >= 0.70)}
    t1_strict = bool(t1_med >= 0.05 and t1_p < 0.05)
    rule = crosses["T4_dependence"] or crosses["T1_ocular"] or crosses["T2_recording"]
    reading = ("TRAPS OF THE DESIGN (trace normalization + overlap): Paper 3 §4.1 stands" if rule else
               "TRAPS OF THE GEODESIC CUSUM ITSELF: Paper 3 §4.1's interpretation must be withdrawn")
    verdict = (f"{reading}. Dependence (shuffled - blocked): median {np.median(d4):+.3f} over {len(d4)} "
               f"recordings (bar 0.05) -> {'crosses' if crosses['T4_dependence'] else 'below'}. "
               f"Ocular (drop without EOG): median {t1_med:+.3f} over {len(drops)} subjects, one-sided "
               f"Wilcoxon p = {t1_p:.2g} (bar 0.05) -> {'crosses' if crosses['T1_ocular'] else 'below'}. "
               f"Recording (two same-state recordings): median balanced accuracy {np.median(ss):.3f} over "
               f"{len(ss)} subjects (bar 0.70; eyes open vs closed {np.median(oc):.3f}) -> "
               f"{'crosses' if crosses['T2_recording'] else 'below'}. Pseudo-replication (grouped by "
               f"recording - by subject): {t3_gap:+.4f} (bar 0.05; not part of the reading rule) -> "
               f"{'crosses' if crosses['T3_pseudoreplication'] else 'below'}.")
    print("\n" + verdict)
    json.dump({"experiment": "mdm_matched_control", "plan_id": "E3.1", "fills": "R3.1",
               "question": "Does the standard OAS->MDM pipeline fall into the dependence, ocular or recording "
                           "trap when given this method's design (trace normalization, overlapping windows)?",
               "pipeline": "pyriemann 0.12 Covariances(oas) / trace -> MDM(riemann); balanced accuracy",
               "windows": {"eegmmidb": [EEG_WIN, EEG_STEP], "sleep": [SLEEP_WIN, SLEEP_STEP]},
               "crosses_bar": crosses, "reading_rule_met": bool(rule), "reading": reading,
               "T1_ocular": {"per_subject_drop": spread(drops), "wilcoxon_p_one_sided": t1_p,
                             "strict_original_conjunction_met": t1_strict},
               "T2_recording": {"same_state_acc": spread(ss), "open_closed_acc": spread(oc)},
               "T3_pseudoreplication": {**t3, "gap": t3_gap},
               "T4_dependence": {"shuffled_minus_blocked": spread(d4)},
               "verdict": verdict, "per_record_sleep": sleep_rows, "per_subject_eeg": eeg_rows},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
