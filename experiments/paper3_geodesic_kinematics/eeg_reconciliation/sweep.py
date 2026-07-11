"""Secondary sweep: does ANY reasonable segment/window choice reach the appendix's
median ratio ~=12 under the permutation null?

run.py established that on the pre-registered parameters (26 s, 1 s covariance
window) the appendix's own within-state permutation null gives median ratio ~=3.3,
not ~=12 -- the significance replicates but the magnitude does not. Before
concluding the appendix figure is optimistic, this maps the full achievable
surface over the two levers that change the within-state denominator: segment
length (more windows -> tighter mean -> smaller within -> bigger ratio) and
covariance-window length (conditioning of each covariance).

This is reported as a full grid, not a best-cell cherry-pick: the point is the
whole surface and its maximum, so we can say honestly whether ~=12 is reachable
under any reasonable choice or is simply not reproduced on this data.

Usage:
    python -m experiments.paper3_geodesic_kinematics.eeg_reconciliation.sweep
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, mean_density, N_SUBJECTS, EIG_FLOOR, STEP_SEC,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "eeg_reconciliation"
)

SEG_SECS = [20.0, 30.0, 45.0, 58.0]     # up to ~record length (61 s)
WIN_SECS = [0.5, 1.0, 2.0]
N_PERM = 120
SEED = 20240711


def sliding_covs_param(data, sf, win_sec, step_sec):
    w = int(win_sec * sf)
    step = int(step_sec * sf)
    covs = []
    for start in range(0, data.shape[1] - w + 1, step):
        seg = data[:, start:start + w]
        c = np.cov(seg)
        c = spd.eigfloor(c, EIG_FLOOR)
        covs.append(spd.trace_normalize(c))
    return covs


def temporal_half_within(covs):
    h = len(covs) // 2
    return spd.sqrt_distance(mean_density(covs[:h]), mean_density(covs[h:]))


def permutation_within_median(covs, rng, n_perm):
    m = len(covs); h = m // 2
    d = np.empty(n_perm)
    for k in range(n_perm):
        perm = rng.permutation(m)
        g1 = [covs[i] for i in perm[:h]]
        g2 = [covs[i] for i in perm[h:2 * h]]
        d[k] = spd.sqrt_distance(mean_density(g1), mean_density(g2))
    return float(np.median(d))


def cell_ratios(seg_sec, win_sec, rng):
    r_perm, r_temp, nwins = [], [], []
    for s in range(1, N_SUBJECTS + 1):
        try:
            data_o, sf = load_state_covs(s, 1)
            data_c, _ = load_state_covs(s, 2)
            n = int(seg_sec * sf)
            co = sliding_covs_param(data_o[:, :n], sf, win_sec, STEP_SEC)
            cc = sliding_covs_param(data_c[:, :n], sf, win_sec, STEP_SEC)
            db = spd.sqrt_distance(mean_density(co), mean_density(cc))
            wt = 0.5 * (temporal_half_within(co) + temporal_half_within(cc)) + 1e-9
            wp = 0.5 * (permutation_within_median(co, rng, N_PERM)
                        + permutation_within_median(cc, rng, N_PERM)) + 1e-9
            r_perm.append(db / wp); r_temp.append(db / wt); nwins.append(len(co))
        except Exception:
            pass
    return {"n_subjects": len(r_perm), "n_windows": int(np.median(nwins)) if nwins else 0,
            "median_ratio_perm": float(np.median(r_perm)),
            "median_ratio_temporal": float(np.median(r_temp)),
            "n_above_1_perm": int(np.sum(np.array(r_perm) > 1.0)),
            "max_ratio_perm": float(np.max(r_perm)) if r_perm else 0.0}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    print("EEG reconciliation SWEEP: median permutation ratio over seg x win")
    print(f"  segments {SEG_SECS}s  x  windows {WIN_SECS}s  (step {STEP_SEC}s, N_perm {N_PERM})\n")
    print(f"  {'seg':>5} {'win':>5} {'nwin':>5} {'r_perm':>7} {'r_temp':>7} {'>1':>5} {'max':>6}")

    grid = []
    best = {"median_ratio_perm": -1}
    for seg in SEG_SECS:
        for win in WIN_SECS:
            c = cell_ratios(seg, win, rng)
            c["seg_sec"] = seg; c["win_sec"] = win
            grid.append(c)
            if c["median_ratio_perm"] > best["median_ratio_perm"]:
                best = c
            print(f"  {seg:5.0f} {win:5.1f} {c['n_windows']:5d} "
                  f"{c['median_ratio_perm']:7.2f} {c['median_ratio_temporal']:7.2f} "
                  f"{c['n_above_1_perm']:3d}/{c['n_subjects']:<2d} {c['max_ratio_perm']:6.1f}")

    reaches_12 = best["median_ratio_perm"] >= 8.0
    if reaches_12:
        verdict = (
            f"REACHABLE: the appendix's median ~=12 is recoverable under the "
            f"permutation null at seg={best['seg_sec']:.0f}s win={best['win_sec']:.1f}s "
            f"(median {best['median_ratio_perm']:.1f}, {best['n_above_1_perm']}/"
            f"{best['n_subjects']} > 1). The appendix figure is reproducible but only "
            f"with a longer segment / different window than real_eeg_localization's "
            f"26 s / 1 s choice -- so the honest number depends on BOTH the "
            f"within-state null AND the segment/window, which the appendix did not "
            f"pin down.")
    else:
        verdict = (
            f"NOT REACHABLE on this data. Across the full seg x win grid the maximum "
            f"median permutation ratio is {best['median_ratio_perm']:.1f} "
            f"(seg={best['seg_sec']:.0f}s win={best['win_sec']:.1f}s) -- it never "
            f"approaches the appendix's ~=12. Combined with run.py, the honest "
            f"reconciled status is: the permutation null reproduces the appendix's "
            f"SIGNIFICANCE and direction (14/15 > 1, p~=0.002) but NOT its MAGNITUDE; "
            f"median ~=12 is optimistic and is not reproduced under any reasonable "
            f"segment/window/within-state choice on the 15 cached subjects. The "
            f"defensible reported ratio is ~3-4 (permutation) or ~1.3 (temporal-half), "
            f"not 12.")

    out = {
        "experiment": "eeg_reconciliation_sweep",
        "question": "Does any reasonable seg x win reach the appendix median ratio ~=12 under the permutation null?",
        "params": {"seg_secs": SEG_SECS, "win_secs": WIN_SECS, "step_sec": STEP_SEC,
                   "n_perm": N_PERM, "seed": SEED, "n_subjects": N_SUBJECTS},
        "grid": grid,
        "best_cell": best,
        "appendix_median_ratio": 12,
        "verdict": verdict,
    }
    with open(os.path.join(RESULTS_DIR, "sweep.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results in {os.path.relpath(RESULTS_DIR)}/sweep.json")
    print("=" * 72)


if __name__ == "__main__":
    main()
