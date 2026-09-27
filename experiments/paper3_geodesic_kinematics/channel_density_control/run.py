"""E3.3 -- channel density: the two between-recording controls with all 64 channels (Paper 3, §2.6).

See PRE-REGISTRATION.md. Runs `between_recording_control` and `detection_between_recording_control`
unchanged except for the channel list (all 64 EEGMMIDB channels instead of seven), writing their
outputs under this experiment's results directory, then applies the pre-registered criterion.

Usage:
    python -m experiments.paper3_geodesic_kinematics.channel_density_control.run
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy.stats import wilcoxon

import experiments.paper3_geodesic_kinematics.between_recording_control.run as brc
import experiments.paper3_geodesic_kinematics.detection_between_recording_control.run as dbrc
import experiments.paper3_geodesic_kinematics.detection_repair_heldout.run as drh

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "channel_density_control")


def all_channels():
    import mne
    from mne.datasets import eegbci
    p = eegbci.load_data(1, [1], path=brc.DATA_DIR, update_path=False)[0]
    raw = mne.io.read_raw_edf(str(p), preload=False, verbose="ERROR")
    eegbci.standardize(raw)
    return list(raw.ch_names)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    chans = all_channels()
    assert len(chans) == 64, len(chans)
    # between-recording control with 64 channels
    brc.CHANNELS = chans
    brc.RESULTS_DIR = os.path.join(RESULTS_DIR, "between_recording_64")
    brc.main()
    # detection control with 64 channels (load_run in detection_repair_heldout selects by WANT)
    drh.WANT = [drh._norm(c) for c in chans]
    dbrc.RESULTS_DIR = os.path.join(RESULTS_DIR, "detection_64")
    dbrc.main()

    b = json.load(open(os.path.join(brc.RESULTS_DIR, "result.json")))
    d = json.load(open(os.path.join(dbrc.RESULTS_DIR, "result.json")))
    ps = b.get("per_subject") or b.get("subjects")
    oc = np.array([r["G_OC"] for r in ps]); ss = np.array([r["G_SS"] for r in ps])
    n_gt = int(np.sum(oc > ss))
    p = float(wilcoxon(oc, ss, alternative="greater").pvalue)
    s_oc = np.array([r["S_OC"] for r in ps]); s_ss = np.array([r["S_SS"] for r in ps])
    auc = float(d["auc_OC_vs_SS"])
    depends = n_gt >= 12 and p < 0.01 and auc >= 0.80
    verdict = (f"{'RESULTS DEPEND ON CHANNEL DENSITY' if depends else 'RESULTS DO NOT DEPEND ON CHANNEL DENSITY (by the pre-registered bar)'}: "
               f"with 64 channels the eyes-open/closed geometric ratio exceeds the same-state control in "
               f"{n_gt}/15 subjects (one-sided Wilcoxon p = {p:.3g}; bar >= 12/15 and p < 0.01; 7 channels: 11/15, "
               f"p = 0.024), and the detection statistic separates a change of state from a same-state change of "
               f"recording at AUC {auc:.3f} (bar 0.80; 7 channels: 0.72). A recording change alone fires it at "
               f"AUC {d['auc_SS_vs_WN']:.3f}. Relative alpha power with 64 channels: median ratio "
               f"{np.median(s_oc):.2f} (eyes open/closed) against {np.median(s_ss):.2f} (same state).")
    print("\n" + verdict)
    json.dump({"experiment": "channel_density_control", "plan_id": "E3.3", "fills": "R3.3",
               "question": "Do the between-recording controls' negative results depend on using only seven channels?",
               "n_channels": 64, "channels": chans,
               "geometry": {"n_OC_gt_SS": n_gt, "wilcoxon_p_one_sided": p,
                            "median_ratio_OC": float(np.median(oc)), "median_ratio_SS": float(np.median(ss))},
               "scalar_rel_alpha_64": {"median_ratio_OC": float(np.median(s_oc)), "median_ratio_SS": float(np.median(s_ss)),
                                       "n_OC_gt_SS": int(np.sum(s_oc > s_ss))},
               "detection": {"auc_OC_vs_SS": auc, "auc_SS_vs_WN": d["auc_SS_vs_WN"], "auc_OC_vs_WN": d["auc_OC_vs_WN"]},
               "criterion_met_depends_on_density": bool(depends), "verdict": verdict,
               "per_subject_ratios": [{"subject": r.get("subject"), "G_OC": r["G_OC"], "G_SS": r["G_SS"],
                                       "S_OC": r["S_OC"], "S_SS": r["S_SS"]} for r in ps]},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
