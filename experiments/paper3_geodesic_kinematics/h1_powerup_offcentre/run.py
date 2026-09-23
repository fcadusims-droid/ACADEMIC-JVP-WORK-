"""H1 power-up, off-centre: manifold vs scalar CUSUM localization on all Sleep-EDF SC records.

See PRE-REGISTRATION.md (and round2_blocked_on_session_egress, Item 1). The detectors, loader,
transition finder, windowing, tolerance and off-centre placement are imported unchanged from
localization_centerbias_control / sleep_stage_localization. Secondary: subject-level McNemar
(one record per subject) and an EEG-only arm (no EOG channel).

Usage:
    python -m experiments.paper3_geodesic_kinematics.h1_powerup_offcentre.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
from scipy.stats import binomtest

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint, _hit,
)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, find_transition, discover_subjects,
    STEP_SEC, TOL_SEC, MIN_SEG_SEC,
)
from experiments.paper3_geodesic_kinematics.scalar_vs_manifold_localization.run import (
    scalar_bandpower, scalar_cusum,
)
from experiments.paper3_geodesic_kinematics.localization_centerbias_control.run import (
    SLEEP_PRE_SEC, SLEEP_POST_SEC, _centre_prior_idx, self_test,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "h1_powerup_offcentre")
N_SC_FILES = 153          # sleep-cassette PSG files on PhysioNet (stopping rule: attempt all)


def detect(sub, fs, seam, tol, min_seg):
    """(manifold hit, scalar hit, centre-prior hit) on one off-centre window."""
    covs, _, cen = sliding_covs_labeled(sub, fs, np.full(sub.shape[1], "", dtype=object))
    E, C = embed_cumsum(covs)
    curve = cusum_changepoint(E, C, min_seg)
    _, _, hit_m, _ = _hit(curve, seam, tol)
    cp_s = scalar_cusum(scalar_bandpower(sub, fs), min_seg)
    return bool(hit_m), bool(abs(cp_s - seam) <= tol), \
        bool(abs(_centre_prior_idx(len(cen)) - seam) <= tol), len(cen)


def records():
    tol = int(round(TOL_SEC / STEP_SEC))
    min_seg = int(round(MIN_SEG_SEC / STEP_SEC))
    rows, skipped = [], []
    for p, h in discover_subjects():
        name = os.path.basename(p)[:7]            # SC4ssN + variant letter
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            skipped.append({"record": name, "why": f"load failed: {type(e).__name__}"})
            continue
        tr = find_transition(stage, fs)
        if tr is None:
            skipped.append({"record": name, "why": "no qualifying transition"})
            continue
        t0, s0, s1 = tr
        lo = max(0, t0 - int(SLEEP_PRE_SEC * fs))
        hi = min(data.shape[1], t0 + int(SLEEP_POST_SEC * fs))
        sub = data[:, lo:hi]
        _, _, cen = sliding_covs_labeled(sub, fs, np.full(sub.shape[1], "", dtype=object))
        if len(cen) < 4:
            skipped.append({"record": name, "why": "window too short"})
            continue
        seam = int(np.argmin(np.abs(cen - (t0 - lo) / fs)))
        m, s, cp, nw = detect(sub, fs, seam, tol, min_seg)
        m2, s2, _, _ = detect(sub[:2], fs, seam, tol, min_seg)     # EEG only (no EOG)
        row = {"record": name, "subject": name[3:5], "night": int(name[5]),
               "from": s0, "to": s1, "seam": seam, "n_windows": nw,
               "manifold_hit": m, "scalar_hit": s, "centre_prior_hit": cp,
               "eeg_only_manifold_hit": m2, "eeg_only_scalar_hit": s2}
        rows.append(row)
        print(f"  {name} {s0}->{s1}: manifold {'HIT' if m else '---'} scalar "
              f"{'HIT' if s else '---'} | EEG-only {'HIT' if m2 else '---'}/"
              f"{'HIT' if s2 else '---'}", flush=True)
    return rows, skipped


def mcnemar(pairs):
    b = sum(1 for m, s in pairs if m and not s)
    c = sum(1 for m, s in pairs if s and not m)
    p = float(binomtest(b, b + c, 0.5).pvalue) if b + c else 1.0
    return b, c, p


def wilson(k, n, z=1.96):
    if n == 0:
        return [float("nan")] * 2
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return [float(c - h), float(c + h)]


def verdict_of(man, sca, b, c, p):
    if p < 0.05 and b > c:
        return "MANIFOLD BEATS SCALAR"
    if p < 0.05 and c > b:
        return "SCALAR BEATS MANIFOLD"
    if abs(man - sca) <= 1:
        return "TIE"
    return "INCONCLUSIVE"


def compare(rows, mkey, skey):
    n = len(rows)
    man = sum(r[mkey] for r in rows)
    sca = sum(r[skey] for r in rows)
    b, c, p = mcnemar([(r[mkey], r[skey]) for r in rows])
    return {"n": n, "manifold_hits": man, "scalar_hits": sca,
            "manifold_rate_ci95": wilson(man, n), "scalar_rate_ci95": wilson(sca, n),
            "manifold_only": b, "scalar_only": c, "mcnemar_p": p,
            "verdict": verdict_of(man, sca, b, c, p)}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("H1 power-up, off-centre (Sleep-EDF SC)")
    if not self_test():
        raise SystemExit("self-test failed -- aborting before reading real data")
    n_files = len(discover_subjects())
    rows, skipped = records()
    if not rows:
        raise SystemExit("no usable records")

    primary = compare(rows, "manifold_hit", "scalar_hit")
    by_subj = {}
    for r in sorted(rows, key=lambda r: (r["subject"], r["night"])):
        by_subj.setdefault(r["subject"], r)
    subj_rows = list(by_subj.values())
    subject = compare(subj_rows, "manifold_hit", "scalar_hit")
    eeg = compare(rows, "eeg_only_manifold_hit", "eeg_only_scalar_hit")
    eeg_subj = compare(subj_rows, "eeg_only_manifold_hit", "eeg_only_scalar_hit")
    cp = sum(r["centre_prior_hit"] for r in rows)

    def line(tag, d):
        return (f"{tag}: {d['verdict']} -- manifold {d['manifold_hits']}/{d['n']} vs scalar "
                f"{d['scalar_hits']}/{d['n']} (manifold-only {d['manifold_only']}, scalar-only "
                f"{d['scalar_only']}, McNemar p = {d['mcnemar_p']:.3g})")
    verdict = (
        f"PRIMARY (pre-registered, record level) {line('', primary)[2:]}. "
        f"{line('Subject level (one record per subject, secondary)', subject)}. "
        f"{line('EEG only, no EOG (secondary)', eeg)}; subject level "
        f"{eeg_subj['manifold_hits']}/{eeg_subj['n']} vs {eeg_subj['scalar_hits']}/{eeg_subj['n']} "
        f"({eeg_subj['verdict']}). "
        f"Off-centre sanity: the centre-prior detector scores {cp}/{len(rows)}. "
        f"Stopping rule: {n_files} of {N_SC_FILES} SC recordings were available and analysed once; "
        f"{len(rows)} had a qualifying transition.")
    print("\n" + verdict)

    summary = {
        "experiment": "h1_powerup_offcentre",
        "data": "PhysioNet Sleep-EDF Expanded, sleep-cassette; channels Fpz-Cz, Pz-Oz, EOG horizontal",
        "question": "With enough records and the transition off-centre, does the geodesic CUSUM "
                    "localize sleep transitions better than a log-total-power CUSUM?",
        "params": {"pre_sec": SLEEP_PRE_SEC, "post_sec": SLEEP_POST_SEC, "tol_sec": TOL_SEC,
                   "step_sec": STEP_SEC, "min_seg_sec": MIN_SEG_SEC},
        "stopping_rule": {"sc_files_on_physionet": N_SC_FILES, "records_available": n_files,
                          "records_with_transition": len(rows), "skipped": skipped},
        "primary_record_level": primary,
        "secondary_subject_level": subject,
        "secondary_eeg_only_record_level": eeg,
        "secondary_eeg_only_subject_level": eeg_subj,
        "centre_prior_hits": cp,
        "verdict": verdict,
        "per_record": rows,
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
