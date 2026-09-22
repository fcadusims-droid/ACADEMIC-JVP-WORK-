"""POST-HOC addendum: relative delta-power baselines for the H2 re-test (see PRE-REGISTRATION)."""
from __future__ import annotations
import json, os, warnings
import numpy as np
from scipy.stats import wilcoxon
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, discover_subjects, WIN_SEC, STEP_SEC)
from experiments.paper3_geodesic_kinematics.regime_referent_nulls.run import (
    windows, features, low_half, mapped, cramers_v_binary, rolling_mean, EXP_WIN, RESULTS_DIR)
warnings.filterwarnings("ignore")


def rel_delta(data, fs):
    w, step = int(WIN_SEC * fs), int(STEP_SEC * fs)
    starts = np.arange(0, data.shape[1] - w + 1, step)
    idx = starts[:, None] + np.arange(w)[None, :]
    freqs = np.fft.rfftfreq(w, 1 / fs)
    dmask = (freqs >= 0.5) & (freqs < 4.0); tmask = (freqs >= 0.5) & (freqs < 30.0)
    out = np.zeros(len(starts))
    for ch in range(data.shape[0]):
        seg = data[ch][idx]; seg = seg - seg.mean(1, keepdims=True)
        P = np.abs(np.fft.rfft(seg * np.hanning(w), axis=1)) ** 2
        out += P[:, dmask].sum(1) / (P[:, tmask].sum(1) + 1e-12)
    return out / data.shape[0]


def main():
    per, pooled = [], {k: ([], []) for k in ["geo_vol", "delta_level", "delta_vol"]}
    for p, h in discover_subjects():
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception:
            continue
        covs, logp, labs = windows(data, fs, stage)
        rd = rel_delta(data, fs)[:len(covs)]
        lrd = np.log(rd + 1e-12)
        dv = np.abs(np.diff(lrd)); dv = np.concatenate([dv, dv[-1:]])
        feats = {"geo_vol": low_half(features(covs, logp)["geo_vol"]),
                 "delta_level": low_half(-rd),          # high delta -> 'drift' half
                 "delta_vol": low_half(rolling_mean(dv, EXP_WIN))}
        lab = mapped(labs); keep = lab >= 0
        row = {"record": pref}
        for k, v in feats.items():
            row[f"V_{k}"] = cramers_v_binary(v[keep], lab[keep])
            pooled[k][0].append(v[keep]); pooled[k][1].append(lab[keep])
        per.append(row); print(pref, {k: round(v, 3) for k, v in row.items() if k != "record"})
    V = {k: cramers_v_binary(np.concatenate(a), np.concatenate(b)) for k, (a, b) in pooled.items()}
    best = max(["delta_level", "delta_vol"], key=lambda k: V[k])
    diff = np.array([r["V_geo_vol"] - r[f"V_{best}"] for r in per])
    p = float(wilcoxon(diff, alternative="greater").pvalue) if np.any(diff != 0) else 1.0
    holds = V["geo_vol"] > max(V["delta_level"], V["delta_vol"]) and p < 0.05
    verdict = (f"POST-HOC: pooled V geo_vol {V['geo_vol']:.3f}, relative-delta level {V['delta_level']:.3f}, "
               f"relative-delta volatility {V['delta_vol']:.3f}; per-record geo minus best delta ({best}) "
               f"one-sided Wilcoxon p = {p:.4f}. " +
               ("The geometric volatility still binds more strongly than the delta-power baselines: the "
                "attribution clause of verdict (A) stands against the strongest scalar competitor tried."
                if holds else
                "A delta-power scalar binds as strongly or more strongly: the attribution clause of verdict (A) "
                "is WITHDRAWN and the re-test reads (B) -- the association is real but is not evidence for the "
                "geometry."))
    out = {"posthoc": True, "pooled_V": V, "best_delta": best, "wilcoxon_p_geo_minus_delta": p,
           "attribution_holds": bool(holds), "per_record": per, "verdict": verdict}
    json.dump(out, open(os.path.join(RESULTS_DIR, "posthoc_spectral.json"), "w"), indent=2)
    print(verdict)


if __name__ == "__main__":
    main()
