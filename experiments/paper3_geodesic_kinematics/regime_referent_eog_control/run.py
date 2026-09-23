"""Is the geometry's advantage over scalars really the eye? Subject-level EOG control for the
H2 re-test. See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.regime_referent_eog_control.run
"""
from __future__ import annotations
import json, os, warnings
import numpy as np
from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum, _R
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects, WIN_SEC, STEP_SEC, EIG_FLOOR)
from experiments.paper3_geodesic_kinematics.regime_referent_nulls.run import (
    low_half, mapped, cramers_v_binary, rolling_mean, EXP_WIN)
from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "regime_referent_eog_control")
FPZ, PZ, EOG = 0, 1, 2   # order of WANT_CH in sleep_stage_localization
EOG_FEATS = ["fpz_eog_corr_vol", "fpz_eog_corr_level", "eog_pow_vol", "eog_pow_level"]
FEATS = ["geo_vol", "geo_vol_eeg"] + EOG_FEATS


def geo_vol(covs):
    E, _ = embed_cumsum(covs)
    En = E.reshape(len(covs), -1)
    step = 2.0 * np.arccos(np.clip(np.sum(En[:-1] * En[1:], 1) / (_R * _R), -1, 1))
    return rolling_mean(np.concatenate([step, step[-1:]]), EXP_WIN)


def vol(x):
    d = np.abs(np.diff(x)); return rolling_mean(np.concatenate([d, d[-1:]]), EXP_WIN)


def features(data, fs, stage):
    w, step = int(WIN_SEC * fs), int(STEP_SEC * fs)
    starts = np.arange(0, data.shape[1] - w + 1, step)
    idx = starts[:, None] + np.arange(w)[None, :]
    covs3, covs2, labs = [], [], []
    for s in starts:
        seg = data[:, s:s + w]
        raw = np.cov(seg)
        covs3.append(spd.trace_normalize(spd.eigfloor(raw, EIG_FLOOR)))
        covs2.append(spd.trace_normalize(spd.eigfloor(raw[:2, :2], EIG_FLOOR)))
        ws = stage[s:s + w]
        vals, cnts = np.unique(ws[ws != ""], return_counts=True)
        labs.append(vals[np.argmax(cnts)] if len(vals) else "")
    f = data[FPZ][idx]; e = data[EOG][idx]
    f = f - f.mean(1, keepdims=True); e = e - e.mean(1, keepdims=True)
    corr = np.abs((f * e).sum(1) / np.sqrt((f * f).sum(1) * (e * e).sum(1) + 1e-12))
    logeog = np.log((e * e).mean(1) + 1e-12)
    return {"geo_vol": geo_vol(covs3), "geo_vol_eeg": geo_vol(covs2),
            "fpz_eog_corr_vol": vol(corr), "fpz_eog_corr_level": corr,
            "eog_pow_vol": vol(logeog), "eog_pow_level": logeog}, np.array(labs, dtype=object)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    per_rec, pooled = [], {k: ([], []) for k in FEATS}
    for p, h in discover_subjects():
        rec = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception:
            continue
        feats, labs = features(data, fs, stage)
        lab = mapped(labs); keep = lab >= 0
        row = {"record": rec, "subject": rec[:5]}
        for k in FEATS:
            reg = low_half(feats[k])       # V is symmetric in the split's direction
            row[f"V_{k}"] = cramers_v_binary(reg[keep], lab[keep])
            pooled[k][0].append(reg[keep]); pooled[k][1].append(lab[keep])
        per_rec.append(row)
        print(rec, {k: round(row[f"V_{k}"], 3) for k in FEATS})

    V = {k: cramers_v_binary(np.concatenate(a), np.concatenate(b)) for k, (a, b) in pooled.items()}
    subjects = sorted({r["subject"] for r in per_rec})
    per_subj = []
    for s in subjects:
        rs = [r for r in per_rec if r["subject"] == s]
        per_subj.append({"subject": s, "n_nights": len(rs),
                         **{f"V_{k}": float(np.mean([r[f'V_{k}'] for r in rs])) for k in FEATS}})
    n_s = len(per_subj)
    estar = max(EOG_FEATS, key=lambda k: V[k])
    geo_wins = sum(r["V_geo_vol"] > r[f"V_{estar}"] for r in per_subj)
    eeg_wins = sum(r["V_geo_vol_eeg"] > r[f"V_{estar}"] for r in per_subj)
    min_p = 1.0 / 2 ** n_s

    eye = V[estar] >= V["geo_vol"] or (n_s - geo_wins) >= 2
    survives = (not eye) and V["geo_vol"] > V[estar] and geo_wins == n_s
    cat = "EYE" if eye else ("SURVIVES" if survives else "NOT_ESTABLISHED")
    ratio = V["geo_vol_eeg"] / V["geo_vol"] if V["geo_vol"] > 0 else 0.0
    if eeg_wins == n_s:
        eeg_read = (f"the EEG-only geometry also beats it in {eeg_wins}/{n_s} subjects, so the signal "
                    f"is not carried by the EOG channel alone")
    elif ratio < 0.2:
        eeg_read = (f"with the EOG channel removed the geometry's pooled V falls from "
                    f"{V['geo_vol']:.3f} to {V['geo_vol_eeg']:.3f} and it beats {estar} in "
                    f"{eeg_wins}/{n_s} subjects, so the EOG channel carries essentially all of the signal")
    else:
        eeg_read = (f"the EEG-only geometry beats it in only {eeg_wins}/{n_s} subjects (pooled V "
                    f"{V['geo_vol_eeg']:.3f}), so the EOG channel carries part of the signal")
    head = {"EYE": "ATTRIBUTABLE TO THE EYE, NOT THE GEOMETRY",
            "SURVIVES": "THE GEOMETRY SURVIVES THE EOG CONTROL -- CONSISTENT IN EVERY SUBJECT, NOT SIGNIFICANT",
            "NOT_ESTABLISHED": "GEOMETRY OVER EOG NOT ESTABLISHED"}[cat]
    verdict = (f"{head}. Unit = subject (n = {n_s}; 7 recordings are {n_s} people), so the smallest "
               f"attainable one-sided p is {min_p:.4f} and no significance claim is possible. Pooled V: "
               f"geometry with EOG {V['geo_vol']:.3f}, geometry without EOG {V['geo_vol_eeg']:.3f}; best "
               f"EOG-carrying scalar ({estar}) {V[estar]:.3f} (others: " +
               ", ".join(f"{k} {V[k]:.3f}" for k in EOG_FEATS if k != estar) +
               f"). Geometry beats {estar} in {geo_wins}/{n_s} subjects; {eeg_read}.")
    out = {"experiment": "regime_referent_eog_control",
           "question": "is geodesic volatility's advantage over scalars attributable to EOG coupling?",
           "n_recordings": len(per_rec), "n_subjects": n_s, "min_attainable_p_one_sided": min_p,
           "pooled_V": V, "best_eog_scalar": estar, "geo_wins_subjects": geo_wins,
           "geo_eeg_only_wins_subjects": eeg_wins,
           "preregistered_criterion": ("eye iff best EOG scalar pooled V >= geo V or wins >= 2/4 "
                                       "subjects; survives iff geo beats it pooled and 4/4 subjects "
                                       "(reported as not significant)"),
           "category": cat, "per_subject": per_subj, "per_record": per_rec,
           "verdict": verdict, "figures": []}
    json.dump(out, open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)
    print("\n" + verdict)


if __name__ == "__main__":
    main()
