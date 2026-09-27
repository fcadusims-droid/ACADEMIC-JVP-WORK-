"""E2.2 -- beat-indexed, multiscale time irreversibility (Paper 2, §2.6).

See PRE-REGISTRATION.md. Fantasia (annotated beats) and the 21 I-CARE pilot patients (first ECG
segment, the pilot's adaptive detector). RR indexed by beat; intervals >20% from the median of the
centred 5-beat window removed; scales 1..10 (non-overlapping block means); T at lag 1; 100 IAAFT
surrogates per scale; summary = mean |z|; p from the leave-one-out surrogate summaries.
Secondary: the gate as described (4 Hz interpolation) on the same I-CARE segments.

Usage:
    python -m experiments.paper2_cbra_protocol.multiscale_asymmetry.run
"""
from __future__ import annotations

import glob
import json
import os
import warnings

import numpy as np

from experiments.paper2_cbra_protocol.cbra_boundary_residual.run import (
    FS, load_ecg, r_peaks, rr_tachogram, time_reversal_asymmetry, iaaft, boundary_structure,
)
from experiments.paper2_cbra_protocol.fantasia_positive_control.run import (
    YOUNG, OLD, fantasia_beats, clean_rr_as_applied, interp_4hz,
)

warnings.filterwarnings("ignore")
HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "multiscale_asymmetry")
ICARE_DIR = os.path.join(HERE, "..", "..", "data", "icare")
PILOT = os.path.join(HERE, "..", "..", "_results", "cbra_boundary_residual", "result.json")
SCALES = range(1, 11)
N_SURR = 100
BAR = 0.60


def clean_local_median(beat_t):
    """RR by beat; drop intervals differing >20% from the median of the centred 5-beat window."""
    rr = np.diff(beat_t)
    rr = rr[rr > 0]
    n = len(rr)
    med = np.array([np.median(rr[max(0, i - 2):min(n, i + 3)]) for i in range(n)])
    keep = np.abs(rr - med) <= 0.20 * med
    return rr[keep], int((~keep).sum())


def coarse(x, tau):
    m = len(x) // tau
    return x[:m * tau].reshape(m, tau).mean(axis=1)


def multiscale(rr, rng):
    obs, surr = [], []
    for tau in SCALES:
        c = coarse(rr, tau)
        obs.append(time_reversal_asymmetry(c))
        surr.append([time_reversal_asymmetry(iaaft(c, rng=rng)) for _ in range(N_SURR)])
    obs, surr = np.array(obs), np.array(surr)              # (10,), (10, 100)
    mu, sd = surr.mean(1), surr.std(1, ddof=1)
    z = (obs - mu) / sd
    summary = float(np.mean(np.abs(z)))
    # each surrogate treated as the real series: z against the other 99, per scale
    s_sum = np.empty(N_SURR)
    for j in range(N_SURR):
        others = np.delete(surr, j, axis=1)
        zj = (surr[:, j] - others.mean(1)) / others.std(1, ddof=1)
        s_sum[j] = np.mean(np.abs(zj))
    count = int(np.sum(s_sum >= summary))
    return {"summary_mean_abs_z": summary, "z_by_scale": [float(v) for v in z],
            "T_by_scale": [float(v) for v in obs], "p": count / N_SURR, "p_plus1": (count + 1) / (N_SURR + 1),
            "structured": bool(count / N_SURR < 0.05), "n_rr": int(len(rr))}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    pilot = {r["patient"]: r for r in json.load(open(PILOT))["per_patient"]}
    groups = {"fantasia_young": [], "fantasia_elderly": [], "icare": []}
    repro, secondary = [], []

    for group, recs in (("fantasia_young", YOUNG), ("fantasia_elderly", OLD)):
        for rec in recs:
            rr, n_removed = clean_local_median(fantasia_beats(rec))
            r = {"subject": rec, "n_removed": n_removed, **multiscale(rr, rng)}
            groups[group].append(r)
            print(f"  {group} {rec}: summary {r['summary_mean_abs_z']:.2f} p {r['p']:.2f} {'STRUCTURED' if r['structured'] else ''}", flush=True)

    rng_gate = np.random.default_rng(0)
    for pid in sorted(pilot):
        files = sorted(glob.glob(os.path.join(ICARE_DIR, f"pilot_{pid}_*_ECG.mat")))
        if not files:
            print(f"  icare {pid}: segment not downloaded"); continue
        ecg = load_ecg(files[0])
        # reproduction check against the pilot
        rr_orig = rr_tachogram(ecg)
        n_orig = None if rr_orig is None else int(len(rr_orig))
        t_orig = None if rr_orig is None else float(time_reversal_asymmetry(rr_orig))
        repro.append({"patient": pid, "segment": os.path.basename(files[0]), "n_rr_now": n_orig,
                      "n_rr_pilot": pilot[pid]["n_rr"], "T_now": t_orig, "T_pilot": pilot[pid]["t_rev"],
                      "same_segment": n_orig == pilot[pid]["n_rr"]})
        beats = r_peaks(ecg) / FS
        rr, n_removed = clean_local_median(beats)
        r = {"subject": pid, "n_removed": n_removed, "pilot_structured": pilot[pid]["significant"], **multiscale(rr, rng)}
        groups["icare"].append(r)
        # secondary: the gate as described (4 Hz)
        rr2, t2 = clean_rr_as_applied(beats)
        if rr2 is not None:
            g = boundary_structure(interp_4hz(rr2, t2), rng_gate)
            secondary.append({"patient": pid, **g})
        print(f"  icare {pid}: summary {r['summary_mean_abs_z']:.2f} p {r['p']:.2f} {'STRUCTURED' if r['structured'] else ''} "
              f"(pilot {'structured' if r['pilot_structured'] else '-'}; repro n {n_orig} vs {pilot[pid]['n_rr']})", flush=True)

    def summ(rows):
        n = len(rows); k = sum(r["structured"] for r in rows)
        return {"n": n, "n_structured": int(k), "fraction": (k / n) if n else None, "passes_0.60": bool(n and k / n >= BAR)}

    res = {g: {**summ(v), "per_subject": v} for g, v in groups.items()}
    orig6 = [r for r in groups["icare"] if r["pilot_structured"]]
    still = int(sum(r["structured"] for r in orig6))
    sec_frac = (sum(r["significant"] for r in secondary) / len(secondary)) if secondary else None
    n_same = sum(r["same_segment"] for r in repro)
    verdict = (f"Structured fraction (multiscale, beat-indexed, p < 0.05; bar 0.60): Fantasia young "
               f"{res['fantasia_young']['n_structured']}/{res['fantasia_young']['n']}, elderly "
               f"{res['fantasia_elderly']['n_structured']}/{res['fantasia_elderly']['n']}, I-CARE "
               f"{res['icare']['n_structured']}/{res['icare']['n']}. Of the {len(orig6)} I-CARE patients the pilot "
               f"called structured, {still} remain structured after cleaning. Reproduction check: {n_same}/{len(repro)} "
               f"segments give the pilot's exact RR count. Secondary (gate as described, 4 Hz) on I-CARE: "
               f"{sum(r['significant'] for r in secondary)}/{len(secondary)}"
               + (f" ({sec_frac:.0%})." if sec_frac is not None else "."))
    print("\n" + verdict)
    json.dump({"experiment": "multiscale_asymmetry", "plan_id": "E2.2", "fills": "R2.2",
               "question": "With beat-indexed, cleaned RR series and a multiscale asymmetry summary, what fraction of "
                           "Fantasia young, Fantasia elderly and I-CARE pilot subjects is structured?",
               "params": {"scales": list(SCALES), "n_surrogates_per_scale": N_SURR, "ectopic_rule": ">20% from centred 5-beat median",
                          "bar": BAR, "seed": 0},
               "results": res, "icare_original_structured": len(orig6), "icare_original_still_structured": still,
               "reproduction_check": repro, "secondary_icare_gate_as_described_4hz": {"n": len(secondary),
                   "n_structured": int(sum(r['significant'] for r in secondary)), "fraction": sec_frac, "per_patient": secondary},
               "verdict": verdict},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
