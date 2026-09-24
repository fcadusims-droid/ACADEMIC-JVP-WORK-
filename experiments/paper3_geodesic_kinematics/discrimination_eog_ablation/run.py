"""Is A1's N2-vs-REM structural discrimination carried by the EOG channel? See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.discrimination_eog_ablation.run
"""
from __future__ import annotations
import json, os, warnings
import numpy as np
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects, _ratio, DISC_STAGES, N_PERM, WIN_SEC, STEP_SEC, EIG_FLOOR)
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "discrimination_eog_ablation")


def test(E, labs, rng):
    a, b = labs == DISC_STAGES[0], labs == DISC_STAGES[1]
    obs = _ratio(E[a], E[b]); L = len(labs); null = []
    while len(null) < N_PERM:
        sl = np.roll(labs, int(rng.integers(int(0.1 * L), int(0.9 * L))))
        aa, bb = sl == DISC_STAGES[0], sl == DISC_STAGES[1]
        if aa.sum() >= 10 and bb.sum() >= 10:
            null.append(_ratio(E[aa], E[bb]))
    p = float((np.sum(np.array(null) >= obs) + 1) / (N_PERM + 1))
    return float(obs), p, bool(obs > 1 and p < 0.05)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0); rows = []
    for pth, h in discover_subjects():
        rec = os.path.basename(pth)[:6]
        try:
            data, fs, stage = load_subject(pth, h)
        except Exception:
            continue
        w, step = int(WIN_SEC * fs), int(STEP_SEC * fs)
        E3, E2, labs = [], [], []
        for s in range(0, data.shape[1] - w + 1, step):
            raw = np.cov(data[:, s:s + w])
            E3.append(spd.sqrt_embed(spd.trace_normalize(spd.eigfloor(raw, EIG_FLOOR))))
            E2.append(spd.sqrt_embed(spd.trace_normalize(spd.eigfloor(raw[:2, :2], EIG_FLOOR))))
            ws = stage[s:s + w]; vals, cnts = np.unique(ws[ws != ""], return_counts=True)
            labs.append(vals[np.argmax(cnts)] if len(vals) else "")
        labs = np.asarray(labs, dtype=object); E3, E2 = np.array(E3), np.array(E2)
        if (labs == DISC_STAGES[0]).sum() < 10 or (labs == DISC_STAGES[1]).sum() < 10:
            continue
        r3, p3, ok3 = test(E3, labs, rng); r2, p2, ok2 = test(E2, labs, rng)
        rows.append({"recording": rec, "subject": rec[:5], "ratio_with_eog": r3, "p_with_eog": p3,
                     "pass_with_eog": ok3, "ratio_eeg_only": r2, "p_eeg_only": p2, "pass_eeg_only": ok2})
        print(f"  {rec}: with EOG ratio {r3:.2f} p {p3:.3f} | EEG only ratio {r2:.2f} p {p2:.3f}")
    subs = sorted({r["subject"] for r in rows})
    s3 = sum(all(r["pass_with_eog"] for r in rows if r["subject"] == s) for s in subs)
    s2 = sum(all(r["pass_eeg_only"] for r in rows if r["subject"] == s) for s in subs)
    k3 = sum(r["pass_with_eog"] for r in rows); k2 = sum(r["pass_eeg_only"] for r in rows)
    survives = s2 >= s3 - 1
    med3 = float(np.median([r["ratio_with_eog"] for r in rows]))
    med2 = float(np.median([r["ratio_eeg_only"] for r in rows]))
    verdict = (("THE SLEEP DISCRIMINATION SURVIVES WITHOUT THE EYE. " if survives else
                "THE SLEEP DISCRIMINATION IS CARRIED BY THE EOG CHANNEL. ") +
               f"N2-vs-REM under a circular-shift null: with EOG {k3}/{len(rows)} recordings "
               f"({s3}/{len(subs)} subjects), median ratio {med3:.2f}; EEG only (Fpz-Cz, Pz-Oz) "
               f"{k2}/{len(rows)} recordings ({s2}/{len(subs)} subjects), median ratio {med2:.2f}. " +
               ("The EEG-only geometry still separates the stages, so A1's structural discrimination "
                "is not an eye artefact on these recordings." if survives else
                "Paper 3 may not cite the sleep 14/15 as evidence that the EEG geometry is sensitive to "
                "structural regime.") + f" n = {len(subs)} subjects, descriptive.")
    out = {"experiment": "discrimination_eog_ablation",
           "question": "is A1's N2-vs-REM discrimination carried by the EOG channel?",
           "n_recordings": len(rows), "n_subjects": len(subs),
           "pass_recordings": {"with_eog": k3, "eeg_only": k2},
           "pass_subjects": {"with_eog": s3, "eeg_only": s2},
           "median_ratio": {"with_eog": med3, "eeg_only": med2},
           "preregistered_criterion": "survives iff EEG-only subject passes >= with-EOG subject passes - 1",
           "survives_without_eog": bool(survives), "per_recording": rows,
           "verdict": verdict, "figures": []}
    json.dump(out, open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)
    print("\n" + verdict)


if __name__ == "__main__":
    main()
