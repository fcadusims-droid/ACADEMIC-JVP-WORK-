"""E2.3 -- I-CARE by outcome, descriptive (Paper 2, §2.6). Does NOT test the dissociation.

See PRE-REGISTRATION.md. First 50 good (CPC 1-2) and first 50 poor (CPC 3-5) patients in RECORDS
order with an ECG segment giving >= 1800 s of clean RR (E2.2's 20% local-median rule); at most 3
segments tried per patient. E2.2's multiscale summary on the first 1800 s of retained beats;
Mann-Whitney U between groups; covariates from the metadata.

Usage:
    python -m experiments.paper2_cbra_protocol.icare_outcome_descriptive.run
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request

import numpy as np
from scipy.stats import mannwhitneyu

from experiments.paper2_cbra_protocol.cbra_boundary_residual.run import FS, load_ecg, r_peaks
from experiments.paper2_cbra_protocol.multiscale_asymmetry.run import clean_local_median, multiscale

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "icare_outcome_descriptive")
DATA_DIR = os.path.join(HERE, "..", "..", "data", "icare")
BASE = "https://physionet.org/files/i-care/2.1/"
N_PER_GROUP = 50
MAX_SEGMENTS = 3
CLEAN_SEC = 1800.0


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception:
            time.sleep(2 ** i)
    raise RuntimeError(url)


def cached(rel, fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        data = get(BASE + rel)
        open(path + ".part", "wb").write(data)
        os.replace(path + ".part", path)
    return path


def metadata(pid):
    txt = open(cached(f"training/{pid}/{pid}.txt", f"{pid}.txt")).read()
    meta = dict(line.split(": ", 1) for line in txt.strip().split("\n") if ": " in line)
    return meta


def ecg_segments(pid):
    lp = os.path.join(DATA_DIR, f"{pid}.listing.json")
    if os.path.exists(lp):
        return json.load(open(lp))
    html = get(BASE + f"training/{pid}/").decode()
    segs = sorted(set(re.findall(r'href="(\d{4}_\d{3}_\d{3}_ECG)\.mat"', html)))
    json.dump(segs, open(lp, "w"))
    return segs


def clean_1800(pid, rng):
    tried = []
    for seg in ecg_segments(pid)[:MAX_SEGMENTS]:
        cached(f"training/{pid}/{seg}.hea", f"{seg}.hea")
        mat = cached(f"training/{pid}/{seg}.mat", f"{seg}.mat")
        try:
            beats = r_peaks(load_ecg(mat)) / FS
        except Exception as e:
            tried.append((seg, f"load failed {type(e).__name__}")); continue
        rr, _ = clean_local_median(beats)
        if rr.sum() >= CLEAN_SEC:
            rr = rr[:np.searchsorted(np.cumsum(rr), CLEAN_SEC, side="right") + 1]
            return seg, rr, tried
        tried.append((seg, f"only {rr.sum():.0f} s clean"))
    return None, None, tried


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    recs = [l.strip().strip("/").split("/")[-1] for l in get(BASE + "RECORDS").decode().split("\n") if l.strip()]
    groups = {"good": [], "poor": []}
    skipped = {"good": [], "poor": []}
    for pid in recs:
        if all(len(groups[g]) >= N_PER_GROUP for g in groups):
            break
        meta = metadata(pid)
        try:
            cpc = int(float(meta.get("CPC", "nan")))
        except ValueError:
            continue
        g = "good" if cpc <= 2 else "poor"
        if len(groups[g]) >= N_PER_GROUP:
            continue
        seg, rr, tried = clean_1800(pid, rng)
        if seg is None:
            skipped[g].append({"patient": pid, "tried": tried}); print(f"  {pid} ({g}): skipped {tried}", flush=True)
            continue
        m = multiscale(rr, rng)
        row = {"patient": pid, "segment": seg, "CPC": cpc, "age": meta.get("Age"), "sex": meta.get("Sex"),
               "shockable_rhythm": meta.get("Shockable Rhythm"), "TTM": meta.get("TTM"),
               "OHCA": meta.get("OHCA"), "hospital": meta.get("Hospital"), **m}
        groups[g].append(row)
        print(f"  {pid} ({g} {len(groups[g])}/{N_PER_GROUP}): summary {m['summary_mean_abs_z']:.2f} p {m['p']:.2f}", flush=True)

    a = np.array([r["summary_mean_abs_z"] for r in groups["good"]])
    b = np.array([r["summary_mean_abs_z"] for r in groups["poor"]])
    mw = mannwhitneyu(a, b, alternative="two-sided")

    def cov(rows):
        ages = [float(r["age"]) for r in rows if r["age"] not in (None, "nan")]
        def share(key, val):
            v = [r[key] for r in rows if r[key] not in (None, "nan")]
            return (sum(x == val for x in v) / len(v)) if v else None
        ttm = {}
        for r in rows:
            ttm[r["TTM"]] = ttm.get(r["TTM"], 0) + 1
        return {"n": len(rows), "age_median": float(np.median(ages)) if ages else None,
                "male_share": share("sex", "Male"), "shockable_share": share("shockable_rhythm", "True"),
                "TTM_counts": ttm}

    def dist(v):
        return {"median": float(np.median(v)), "q25": float(np.percentile(v, 25)), "q75": float(np.percentile(v, 75)),
                "min": float(v.min()), "max": float(v.max())}

    frac_g = float(np.mean([r["structured"] for r in groups["good"]]))
    frac_p = float(np.mean([r["structured"] for r in groups["poor"]]))
    verdict = (f"DESCRIPTIVE (not a test of the dissociation). Multiscale asymmetry summary (mean |z|, scales 1-10, "
               f"first 1800 s of clean beats): good outcome median {np.median(a):.2f} (n = {len(a)}), poor outcome "
               f"median {np.median(b):.2f} (n = {len(b)}); two-sided Mann-Whitney p = {mw.pvalue:.3g}. Structured "
               f"fraction (p < 0.05): good {frac_g:.0%}, poor {frac_p:.0%}. Skipped for lack of 30 clean minutes in "
               f"{MAX_SEGMENTS} segments: good {len(skipped['good'])}, poor {len(skipped['poor'])}.")
    print("\n" + verdict)
    json.dump({"experiment": "icare_outcome_descriptive", "plan_id": "E2.3", "fills": "R2.3",
               "question": "Descriptively, how does beat-indexed multiscale heart-period irreversibility compare between "
                           "good- and poor-outcome I-CARE patients?",
               "params": {"n_per_group": N_PER_GROUP, "max_segments": MAX_SEGMENTS, "clean_seconds": CLEAN_SEC, "seed": 0},
               "good": {"summary_distribution": dist(a), "structured_fraction": frac_g, "covariates": cov(groups["good"])},
               "poor": {"summary_distribution": dist(b), "structured_fraction": frac_p, "covariates": cov(groups["poor"])},
               "mann_whitney_U": float(mw.statistic), "mann_whitney_p_two_sided": float(mw.pvalue),
               "skipped": skipped, "verdict": verdict, "per_patient": groups["good"] + groups["poor"]},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
