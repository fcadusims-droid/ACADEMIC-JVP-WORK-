"""Held-out validation of the detection-statistic repair (Paper 3).

The repair (scale-normalised CUSUM peak) was SELECTED on the same 15 Sleep-EDF records
it was evaluated on. This applies it unchanged to a paradigm not used to choose it --
eegmmidb eyes-open vs eyes-closed -- and scores the old and new statistics on identical
segments. Criterion (pre-registered): AUC >= 0.70 off Sleep-EDF.

Usage:
    python -m experiments.paper3_geodesic_kinematics.detection_repair_heldout.run
"""
from __future__ import annotations

import glob, json, os, warnings
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

from experiments.shared_lib import spd_manifold as spd
from experiments.paper3_geodesic_kinematics.detection_statistic_repair.run import (
    cusum_curve, stat_peak_over_median, stat_scale_normalised, localise, AUC_BAR,
)
from experiments.paper3_geodesic_kinematics.baseline_benchmark.run import _auc

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "detection_repair_heldout")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "eegmmidb")

WANT = ["O1", "OZ", "O2", "PO3", "POZ", "PO4", "PZ"]   # occipito-parietal
BAND = (8.0, 13.0)          # alpha
WIN_SEC, STEP_SEC = 1.0, 0.25
SEG_SEC = 26.0
EIG_FLOOR = 1e-3
TOL_SEC = 2.0


def _norm(lbl):
    return lbl.strip().upper().replace(".", "").replace(" ", "")


def load_run(path):
    import pyedflib
    r = pyedflib.EdfReader(path)
    labels = [_norm(r.getLabel(i)) for i in range(r.signals_in_file)]
    idx = [labels.index(w) for w in WANT if w in labels]
    if len(idx) < 4:
        r.close(); return None, None
    fs = float(r.getSampleFrequency(idx[0]))
    data = np.array([r.readSignal(i) for i in idx]); r.close()
    b, a = butter(4, [BAND[0]/(fs/2), BAND[1]/(fs/2)], btype="band")
    data = filtfilt(b, a, data, axis=1)
    return (data - data.mean(1, keepdims=True)) / (data.std(1, keepdims=True) + 1e-12), fs


def covs_of(data, fs):
    w, st = int(WIN_SEC*fs), int(STEP_SEC*fs)
    return [spd.trace_normalize(spd.eigfloor(np.cov(data[:, s:s+w]), EIG_FLOOR))
            for s in range(0, data.shape[1]-w+1, st)]


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Held-out validation of the detection repair (eegmmidb eyes-open/closed)")
    subs = sorted({os.path.basename(p)[:4] for p in glob.glob(os.path.join(DATA_DIR, "S*R01.edf"))})
    pos_new, neg_new, pos_old, neg_old, hits, used = [], [], [], [], [], []
    for s in subs:
        p1 = os.path.join(DATA_DIR, f"{s}R01.edf"); p2 = os.path.join(DATA_DIR, f"{s}R02.edf")
        if not (os.path.exists(p1) and os.path.exists(p2)): continue
        d1, fs = load_run(p1); d2, _ = load_run(p2)
        if d1 is None or d2 is None: continue
        n = int(SEG_SEC*fs)
        if d1.shape[1] < 2*n or d2.shape[1] < n: continue
        real = covs_of(np.concatenate([d1[:, :n], d2[:, :n]], axis=1), fs)   # seam at centre
        null = covs_of(d1[:, :2*n], fs)                                      # within one state
        seam = int(SEG_SEC/STEP_SEC)
        cr, cn = cusum_curve(real), cusum_curve(null)
        pos_new.append(stat_scale_normalised(cr, real)); neg_new.append(stat_scale_normalised(cn, null))
        pos_old.append(stat_peak_over_median(cr));       neg_old.append(stat_peak_over_median(cn))
        hits.append(abs(localise(cr)-seam)*STEP_SEC <= TOL_SEC); used.append(s)
    n = len(used)
    auc_new, auc_old = _auc(pos_new, neg_new), _auc(pos_old, neg_old)
    passes = bool(auc_new >= AUC_BAR)
    print(f"  {n} subjects | NEW (scale-normalised) AUC {auc_new:.3f} | OLD (peak/median) AUC {auc_old:.3f}")
    print(f"  localisation (|err|<={TOL_SEC}s): {int(np.sum(hits))}/{n}")

    if n < 8:
        outcome, verdict = "UNDERPOWERED", f"Only {n} usable subjects; need >= 8 to read the bar."
    elif passes:
        outcome = "GENERALISES"
        verdict = (f"THE REPAIR GENERALISES OFF THE DATA IT WAS CHOSEN ON. Applied unchanged "
                   f"to eyes-open/closed EEG ({n} subjects) -- a paradigm not used to select it "
                   f"-- the scale-normalised statistic reaches AUC {auc_new:.3f}, clearing the "
                   f"pre-registered {AUC_BAR} bar. The old peak-to-median statistic scores "
                   f"{auc_old:.3f} on the same segments"
                   + (", again at or below chance, so the FAILURE mechanism generalises too: "
                      "a driftless random walk inflates a ratio whose denominator is the median, "
                      "whatever the paradigm." if auc_old <= 0.55 else ".") +
                   f" The repair is therefore a fix to the STATISTIC rather than a tuning to the "
                   f"sleep paradigm, which is what the mechanistic diagnosis predicted and what "
                   f"selection on a single dataset could not establish. Localisation is "
                   f"{int(np.sum(hits))}/{n} here, but THAT NUMBER SHOULD NOT BE QUOTED: this "
                   f"design splices two runs so the seam always falls at the segment centre, "
                   f"which flatters any localiser with a central prior, and it is not the "
                   f"appendix's eyes-open/closed protocol. Only DETECTION is under test here, "
                   f"and the appendix's negative localisation result stands unrevised.")
    else:
        outcome = "PARADIGM_TUNED"
        verdict = (f"THE REPAIR DOES NOT GENERALISE. On held-out eyes-open/closed EEG ({n} "
                   f"subjects) the scale-normalised statistic reaches only AUC {auc_new:.3f}, "
                   f"below the pre-registered {AUC_BAR} bar (old statistic {auc_old:.3f}). Per "
                   f"the pre-registration, Paper 3 must state that the detection fix is "
                   f"demonstrated on SLEEP ONLY and restrict the detection claim accordingly. "
                   f"Selecting among four repairs on the same 15 records that exposed the "
                   f"problem was the methodological gap this test exists to expose, and it "
                   f"found something.")

    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.bar([0, 1], [auc_old, auc_new], color=["crimson", "steelblue"])
    ax.axhline(AUC_BAR, ls="--", color="green", label=f"bar {AUC_BAR}")
    ax.axhline(0.5, ls=":", color="k", label="chance")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["old\npeak/median", "repaired\nscale-normalised"])
    ax.set_ylabel("detection AUC (held-out: eyes-open/closed)")
    ax.set_title(f"Held-out validation, n={n} subjects"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "detection_repair_heldout.png"), dpi=130)
    plt.close(fig)

    json.dump({"experiment": "detection_repair_heldout",
               "question": "Does the scale-normalised repair, chosen on Sleep-EDF, generalise to a paradigm not used to select it?",
               "data": "PhysioNet eegmmidb R01 (eyes open) vs R02 (eyes closed), occipito-parietal alpha",
               "n_subjects": n, "subjects": used, "bar": AUC_BAR,
               "auc_repaired": auc_new, "auc_old_statistic": auc_old,
               "localisation_hits": int(np.sum(hits)),
               "outcome": outcome, "verdict": verdict,
               "figures": ["detection_repair_heldout.png"]},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2, default=float)
    print("\n" + "="*72); print(verdict); print("="*72)


if __name__ == "__main__":
    main()
