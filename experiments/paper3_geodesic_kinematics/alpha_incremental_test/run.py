"""E3.2 -- does the geometry carry information beyond relative alpha power? (Paper 3, §2.6)

See PRE-REGISTRATION.md. EEGMMIDB R01 (open) vs R02 (closed), 15 subjects, 7 occipito-parietal
channels, non-overlapping 2 s epochs. Model A: logistic regression on per-channel relative alpha
power. Model B: A + tangent-space coordinates of the trace-normalized alpha covariance at the
training set's Riemannian mean. Leave one subject out; held-out log-loss. Control: T0 of R03 vs
T0 of R07 (same state).

Usage:
    python -m experiments.paper3_geodesic_kinematics.alpha_incremental_test.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
from scipy.stats import wilcoxon
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, log_loss
from sklearn.preprocessing import StandardScaler

from experiments.paper3_geodesic_kinematics.between_recording_control.run import load_run, rel_alpha
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import EIG_FLOOR
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results", "alpha_incremental_test")
EPOCH = 2.0
N_SUBJ = 15


def epoch_features(z, unfilt, sf, starts):
    n = int(EPOCH * sf)
    A, C = [], []
    for s in starts:
        A.append(rel_alpha(unfilt[:, s:s + n], sf))
        c = spd.trace_normalize(spd.eigfloor(np.cov(z[:, s:s + n]), EIG_FLOOR))
        C.append(c)
    return np.array(A), np.array(C)


def starts_all(nt, sf):
    n = int(EPOCH * sf)
    return list(range(0, nt - n + 1, n))


def starts_t0(t0, sf):
    n = int(EPOCH * sf)
    st = []
    for a, b in t0:
        st += list(range(int(a * sf), int(b * sf) - n + 1, n))
    return st


def build(task):
    data = {}
    for s in range(1, N_SUBJ + 1):
        if task == "open_closed":
            ra, rb = load_run(s, 1), load_run(s, 2)
            sa, sb = starts_all(ra[0].shape[1], ra[3]), starts_all(rb[0].shape[1], rb[3])
        else:
            ra, rb = load_run(s, 3), load_run(s, 7)
            sa, sb = starts_t0(ra[4], ra[3]), starts_t0(rb[4], rb[3])
        Aa, Ca = epoch_features(ra[0], ra[2], ra[3], sa)
        Ab, Cb = epoch_features(rb[0], rb[2], rb[3], sb)
        data[s] = (np.concatenate([Aa, Ab]), np.concatenate([Ca, Cb]),
                   np.array([0] * len(Aa) + [1] * len(Ab)))
    return data


def loso(data):
    from pyriemann.tangentspace import TangentSpace
    rows = []
    for s in sorted(data):
        tr = [t for t in data if t != s]
        Atr = np.concatenate([data[t][0] for t in tr]); Ctr = np.concatenate([data[t][1] for t in tr])
        ytr = np.concatenate([data[t][2] for t in tr])
        Ate, Cte, yte = data[s]
        out = {"subject": f"S{s:03d}", "n_test": int(len(yte))}
        # model A
        sa = StandardScaler().fit(Atr)
        ma = LogisticRegression(C=1.0, max_iter=5000).fit(sa.transform(Atr), ytr)
        pa = ma.predict_proba(sa.transform(Ate))[:, 1]
        # model B
        ts = TangentSpace(metric="riemann").fit(Ctr)
        Btr = np.hstack([Atr, ts.transform(Ctr)]); Bte = np.hstack([Ate, ts.transform(Cte)])
        sb = StandardScaler().fit(Btr)
        mb = LogisticRegression(C=1.0, max_iter=5000).fit(sb.transform(Btr), ytr)
        pb = mb.predict_proba(sb.transform(Bte))[:, 1]
        for key, p in (("A", pa), ("B", pb)):
            out[f"logloss_{key}"] = float(log_loss(yte, p, labels=[0, 1]))
            out[f"balacc_{key}"] = float(balanced_accuracy_score(yte, (p > 0.5).astype(int)))
        rows.append(out)
        print(f"  S{s:03d}: logloss A {out['logloss_A']:.3f}  B {out['logloss_B']:.3f}   "
              f"balacc A {out['balacc_A']:.2f} B {out['balacc_B']:.2f}", flush=True)
    return rows


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("E3.2 incremental test: eyes open vs closed (LOSO)")
    rows = loso(build("open_closed"))
    la = np.array([r["logloss_A"] for r in rows]); lb = np.array([r["logloss_B"] for r in rows])
    n_better = int(np.sum(lb < la))
    p2 = float(wilcoxon(lb, la).pvalue)
    p1 = float(wilcoxon(lb, la, alternative="less").pvalue)
    passed = n_better >= 11 and p2 < 0.05
    print("E3.2 control: T0 R03 vs T0 R07 (same state, LOSO)")
    crow = loso(build("same_state"))
    ca = np.array([r["balacc_A"] for r in crow]); cb = np.array([r["balacc_B"] for r in crow])
    cla = np.array([r["logloss_A"] for r in crow]); clb = np.array([r["logloss_B"] for r in crow])
    verdict = (f"{'GEOMETRY ADDS INFORMATION BEYOND ALPHA POWER' if passed else 'NO EVIDENCE THAT THE GEOMETRY ADDS INFORMATION BEYOND ALPHA POWER'} "
               f"(pre-registered bar: B better in >= 11/15 and two-sided paired Wilcoxon p < 0.05). "
               f"Held-out log-loss lower with the geometry in {n_better}/15 subjects; median log-loss "
               f"A {np.median(la):.3f}, B {np.median(lb):.3f}; Wilcoxon p = {p2:.3g} two-sided "
               f"({p1:.3g} one-sided). Control (two same-state recordings): median held-out balanced "
               f"accuracy A {np.median(ca):.2f}, B {np.median(cb):.2f}; median log-loss A {np.median(cla):.3f}, "
               f"B {np.median(clb):.3f} (chance log-loss ln 2 = 0.693).")
    print("\n" + verdict)
    json.dump({"experiment": "alpha_incremental_test", "plan_id": "E3.2", "fills": "R3.2",
               "question": "Do tangent-space coordinates of the trace-normalized covariance improve held-out "
                           "eyes-open/closed classification beyond per-channel relative alpha power?",
               "params": {"epoch_s": EPOCH, "subjects": N_SUBJ, "model": "StandardScaler + LogisticRegression(C=1)",
                          "tangent_space": "pyriemann TangentSpace(metric='riemann') fitted on training folds"},
               "n_B_better": n_better, "wilcoxon_p_two_sided": p2, "wilcoxon_p_one_sided": p1,
               "median_logloss_A": float(np.median(la)), "median_logloss_B": float(np.median(lb)),
               "criterion_met": bool(passed),
               "control_same_state": {"median_balacc_A": float(np.median(ca)), "median_balacc_B": float(np.median(cb)),
                                      "median_logloss_A": float(np.median(cla)), "median_logloss_B": float(np.median(clb)),
                                      "per_subject": crow},
               "verdict": verdict, "per_subject": rows},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
