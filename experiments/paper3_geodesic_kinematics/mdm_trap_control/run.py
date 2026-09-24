"""MDM trap control: the field's standard Riemannian pipeline through this suite's traps.

See PRE-REGISTRATION.md. Covariances(oas) -> MDM(riemann) (pyRiemann), balanced accuracy.
T1 EOG, T2 recording confound, T3 subject leakage, T4 window dependence.

Usage:
    python -m experiments.paper3_geodesic_kinematics.mdm_trap_control.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
from scipy.stats import wilcoxon
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GroupKFold, KFold

from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects,
)
from experiments.paper3_geodesic_kinematics.between_recording_control.run import load_run

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results", "mdm_trap_control")
EPOCH_SLEEP = 30.0
EPOCH_EEG = 2.0
MIN_PER_CLASS = 20
N_FOLDS = 5
N_EEG = 15


def pipeline():
    from pyriemann.classification import MDM
    return MDM(metric="riemann")


def covs(epochs):
    from pyriemann.estimation import Covariances
    return Covariances(estimator="oas").fit_transform(epochs)


def blocked_folds(y, k=N_FOLDS):
    """k contiguous-in-time folds within each class (epochs are in time order)."""
    fold = np.empty(len(y), dtype=int)
    for c in np.unique(y):
        idx = np.where(y == c)[0]
        for f, part in enumerate(np.array_split(idx, k)):
            fold[part] = f
    return [(np.where(fold != f)[0], np.where(fold == f)[0]) for f in range(k)]


def cv_score(C, y, splits):
    pred = np.empty(len(y), dtype=y.dtype)
    for tr, te in splits:
        m = pipeline().fit(C[tr], y[tr])
        pred[te] = m.predict(C[te])
    return float(balanced_accuracy_score(y, pred))


def sleep_epochs(path, hyp):
    data, fs, stage = load_subject(path, hyp)
    n = int(EPOCH_SLEEP * fs)
    X, y = [], []
    for s in range(0, data.shape[1] - n + 1, n):
        lab = stage[s:s + n]
        if lab[0] in ("N2", "REM") and np.all(lab == lab[0]):
            X.append(data[:, s:s + n])
            y.append(lab[0])
    return np.array(X), np.array(y)


def sleep_part():
    rows, pooled = [], {"C3": [], "y": [], "rec": [], "subj": []}
    for p, h in discover_subjects():
        name = os.path.basename(p)[:7]
        try:
            X, y = sleep_epochs(p, h)
        except Exception as e:
            print(f"  {name}: load failed {type(e).__name__}")
            continue
        if min((y == "N2").sum(), (y == "REM").sum()) < MIN_PER_CLASS:
            continue
        C3, C2 = covs(X), covs(X[:, :2])
        bf = blocked_folds(y)
        shuf = list(KFold(N_FOLDS, shuffle=True, random_state=0).split(C3))
        r = {"record": name, "subject": name[3:5],
             "n_N2": int((y == "N2").sum()), "n_REM": int((y == "REM").sum()),
             "acc_eog_blocked": cv_score(C3, y, bf),
             "acc_noeog_blocked": cv_score(C2, y, bf),
             "acc_eog_shuffled": cv_score(C3, y, shuf)}
        rows.append(r)
        pooled["C3"].append(C3); pooled["y"].append(y)
        pooled["rec"] += [name] * len(y); pooled["subj"] += [name[3:5]] * len(y)
        print(f"  {name}: EOG {r['acc_eog_blocked']:.2f} noEOG {r['acc_noeog_blocked']:.2f} "
              f"shuffled {r['acc_eog_shuffled']:.2f}", flush=True)
    C = np.concatenate(pooled["C3"]); y = np.concatenate(pooled["y"])
    rec, subj = np.array(pooled["rec"]), np.array(pooled["subj"])
    t3 = {}
    for key, g in (("grouped_by_recording", rec), ("grouped_by_subject", subj)):
        t3[key] = cv_score(C, y, list(GroupKFold(N_FOLDS).split(C, y, g)))
    return rows, t3


def eeg_epochs(x, sf, starts):
    n = int(EPOCH_EEG * sf)
    return np.array([x[:, s:s + n] for s in starts])


def eeg_part():
    rows = []
    for s in range(1, N_EEG + 1):
        runs = {r: load_run(s, r) for r in (1, 2, 3, 7)}
        sf = runs[1][3]
        n = int(EPOCH_EEG * sf)

        def base(r):
            x = runs[r][1]
            return eeg_epochs(x, sf, range(0, x.shape[1] - n + 1, n))

        def t0(r):
            x, iv = runs[r][1], runs[r][4]
            st = []
            for a, b in iv:
                st += list(range(int(a * sf), int(b * sf) - n + 1, n))
            return eeg_epochs(x, sf, st)

        def score(A, B):
            k = min(len(A), len(B))
            X = np.concatenate([A[:k], B[:k]])
            y = np.array(["a"] * k + ["b"] * k)
            return cv_score(covs(X), y, blocked_folds(y)), k

        oc, k_oc = score(base(1), base(2))
        ss, k_ss = score(t0(3), t0(7))
        rows.append({"subject": f"S{s:03d}", "acc_open_vs_closed": oc, "n_per_class_oc": k_oc,
                     "acc_same_state_T0_R03_vs_R07": ss, "n_per_class_ss": k_ss})
        print(f"  S{s:03d}: open/closed {oc:.2f} (n={k_oc})  same-state T0 {ss:.2f} (n={k_ss})",
              flush=True)
    return rows


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("MDM trap control")
    sleep_rows, t3 = sleep_part()
    eeg_rows = eeg_part()

    # T1 (subject level)
    subj = {}
    for r in sleep_rows:
        subj.setdefault(r["subject"], []).append(r)
    drops = np.array([np.mean([x["acc_eog_blocked"] - x["acc_noeog_blocked"] for x in v])
                      for v in subj.values()])
    t1_p = float(wilcoxon(drops, alternative="greater").pvalue)
    t1_med = float(np.median(drops))
    t1 = t1_med >= 0.05 and t1_p < 0.05
    # T2
    ss = np.array([r["acc_same_state_T0_R03_vs_R07"] for r in eeg_rows])
    oc = np.array([r["acc_open_vs_closed"] for r in eeg_rows])
    t2_med = float(np.median(ss))
    t2 = t2_med >= 0.70
    # T3
    t3_gap = t3["grouped_by_recording"] - t3["grouped_by_subject"]
    t3_applies = t3_gap >= 0.03
    # T4
    d4 = np.array([r["acc_eog_shuffled"] - r["acc_eog_blocked"] for r in sleep_rows])
    t4_med = float(np.median(d4))
    t4 = t4_med >= 0.05

    applies = {"T1_eog": bool(t1), "T2_recording": bool(t2), "T3_leakage": bool(t3_applies),
               "T4_dependence": bool(t4)}
    k = sum(applies.values())
    framing = ("TRAPS OF THE FIELD" if k >= 2 else
               "TRAPS OF THIS METHOD" if k == 0 else "MIXED")
    verdict = (
        f"{framing}: {k} of 4 traps apply to the standard covariance->MDM pipeline. "
        f"T1 EOG: median subject-level accuracy drop without EOG {t1_med:+.3f} "
        f"(one-sided Wilcoxon p = {t1_p:.2g}, {len(drops)} subjects) -> "
        f"{'applies' if t1 else 'does not apply'}. "
        f"T2 recording confound: two recordings of the SAME state (T0 of R03 vs R07) classified at "
        f"median balanced accuracy {t2_med:.2f} (eyes open vs closed: {np.median(oc):.2f}; "
        f"{len(ss)} subjects) -> {'applies' if t2 else 'does not apply'}. "
        f"T3 leakage: pooled accuracy grouped by recording {t3['grouped_by_recording']:.3f} vs by "
        f"subject {t3['grouped_by_subject']:.3f} (gap {t3_gap:+.3f}) -> "
        f"{'applies' if t3_applies else 'does not apply'}. "
        f"T4 dependence: shuffled minus blocked CV, median {t4_med:+.3f} over {len(d4)} records -> "
        f"{'applies' if t4 else 'does not apply'}.")
    print("\n" + verdict)
    json.dump({"experiment": "mdm_trap_control",
               "question": "Do this suite's traps affect the field's standard covariance->MDM pipeline?",
               "pipeline": "pyriemann 0.12 Covariances(oas) -> MDM(riemann); balanced accuracy",
               "applies": applies, "n_applies": k, "framing": framing,
               "T1": {"median_drop": t1_med, "wilcoxon_p": t1_p, "n_subjects": len(drops),
                      "n_records": len(sleep_rows)},
               "T2": {"median_same_state_acc": t2_med, "median_open_closed_acc": float(np.median(oc)),
                      "n_subjects": len(ss)},
               "T3": {**t3, "gap": t3_gap},
               "T4": {"median_shuffled_minus_blocked": t4_med, "n_records": len(d4)},
               "verdict": verdict, "per_record_sleep": sleep_rows, "per_subject_eeg": eeg_rows},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
