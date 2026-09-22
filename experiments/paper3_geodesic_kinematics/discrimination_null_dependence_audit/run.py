"""Do A1's window-permutation discrimination p-values survive a dependence-preserving null?
See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.discrimination_null_dependence_audit.run
"""
from __future__ import annotations
import json, os, warnings
import numpy as np
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, discover_subjects, _ratio, DISC_STAGES, N_PERM)
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "discrimination_null_dependence_audit")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    rows = []
    for p, h in discover_subjects():
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception:
            continue
        covs, labs, _ = sliding_covs_labeled(data, fs, stage)
        E = np.array([spd.sqrt_embed(c) for c in covs])
        labs = np.asarray(labs)
        a, b = labs == DISC_STAGES[0], labs == DISC_STAGES[1]
        if a.sum() < 10 or b.sum() < 10:
            continue
        obs = _ratio(E[a], E[b])
        pool = np.concatenate([E[a], E[b]]); nA = int(a.sum())
        null_iid = np.array([_ratio(pool[q[:nA]], pool[q[nA:]])
                             for q in (rng.permutation(len(pool)) for _ in range(N_PERM))])
        L = len(labs); null_shift = []
        while len(null_shift) < N_PERM:
            s = int(rng.integers(int(0.1 * L), int(0.9 * L)))
            sl = np.roll(labs, s)
            aa, bb = sl == DISC_STAGES[0], sl == DISC_STAGES[1]
            if aa.sum() < 10 or bb.sum() < 10:
                continue
            null_shift.append(_ratio(E[aa], E[bb]))
        null_shift = np.array(null_shift)
        p_iid = float((np.sum(null_iid >= obs) + 1) / (N_PERM + 1))
        p_shift = float((np.sum(null_shift >= obs) + 1) / (N_PERM + 1))
        row = {"recording": pref, "ratio": float(obs), "p_iid": p_iid, "p_shift": p_shift,
               "null_iid_p95": float(np.percentile(null_iid, 95)),
               "null_shift_p95": float(np.percentile(null_shift, 95)),
               "pass_iid": bool(obs > 1 and p_iid < 0.05),
               "pass_shift": bool(obs > 1 and p_shift < 0.05)}
        rows.append(row)
        print(f"  {pref}: ratio {obs:.2f} | iid p {p_iid:.3f} (95th {row['null_iid_p95']:.2f}) "
              f"| shift p {p_shift:.3f} (95th {row['null_shift_p95']:.2f})")
    n = len(rows)
    k_iid = sum(r["pass_iid"] for r in rows); k_shift = sum(r["pass_shift"] for r in rows)
    survives = k_shift >= k_iid - 1
    verdict = (
        f"{'A1 DISCRIMINATION SURVIVES A DEPENDENCE-PRESERVING NULL' if survives else 'A1 DISCRIMINATION RESTS PARTLY ON AN ANTI-CONSERVATIVE NULL'}. "
        f"On the {n} cached recordings, A1's statistic passes in {k_iid}/{n} under its original "
        f"window-permutation null and {k_shift}/{n} under a circular-shift null that preserves the "
        f"autocorrelation of both series. Median null 95th percentile: window-permutation "
        f"{np.median([r['null_iid_p95'] for r in rows]):.2f}, circular shift "
        f"{np.median([r['null_shift_p95'] for r in rows]):.2f}. "
        + ("The 14/15 is not an artefact of the i.i.d. null on these recordings."
           if survives else
           "The i.i.d. null inflates the pass count; A1's 14/15 and the four other window-permutation "
           "results (A2, A3, fibre-ablation discrimination, eeg_reconciliation) must be read as resting "
           "on a null that ignores dependence.")
        + " A check on 7 of A1's 15 recordings, not a replacement for them.")
    out = {"experiment": "discrimination_null_dependence_audit",
           "question": "do A1's window-permutation discrimination p-values survive a dependence-preserving null?",
           "n_recordings": n, "pass_iid": k_iid, "pass_shift": k_shift,
           "preregistered_criterion": "survives iff circular-shift passes >= iid passes - 1",
           "survives": bool(survives), "per_recording": rows, "verdict": verdict, "figures": []}
    json.dump(out, open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)
    print("\n" + verdict)


if __name__ == "__main__":
    main()
