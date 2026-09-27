"""E2.1 -- positive control for the estimability gate on Fantasia (Paper 2, §2.6).

See PRE-REGISTRATION.md. Beats from Fantasia's reviewed annotations. Two versions of the gate:
  primary   -- the gate AS APPLIED to I-CARE (beat-indexed RR, 0.3-2.0 s, 4-MAD trim, mean removed);
  secondary -- the gate AS DESCRIBED in Paper 2 §2.4 (the same RR, linearly interpolated at 4 Hz).
Both: time-reversal asymmetry at lag 1, 200 IAAFT surrogates, structured if two-sided p < 0.05.
Sensitive if the young structured fraction >= 0.60 (primary decides).

Usage:
    python -m experiments.paper2_cbra_protocol.fantasia_positive_control.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

from experiments.paper2_cbra_protocol.cbra_boundary_residual.run import (
    boundary_structure, MIN_RPEAKS, N_SURR, PASS_FRACTION,
)

warnings.filterwarnings("ignore")
HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "fantasia_positive_control")
DATA_DIR = os.path.join(HERE, "..", "..", "data", "fantasia")
YOUNG = [f"f1y{i:02d}" for i in range(1, 11)] + [f"f2y{i:02d}" for i in range(1, 11)]
OLD = [f"f1o{i:02d}" for i in range(1, 11)] + [f"f2o{i:02d}" for i in range(1, 11)]
BEATS = set("NLRBAaJSVrFejnE/fQ?")
FS_INTERP = 4.0


def fantasia_beats(rec):
    """Beat times (s) from the reviewed annotations (annotator 'ecg')."""
    import wfdb
    ann = wfdb.rdann(os.path.join(DATA_DIR, rec), "ecg")
    keep = np.array([s in BEATS for s in ann.symbol])
    return ann.sample[keep] / float(ann.fs)


def clean_rr_as_applied(beat_t):
    """`rr_tachogram`'s cleaning, applied to beat times: returns (rr, time of each kept rr)."""
    rr = np.diff(beat_t)
    t = beat_t[1:]
    ok = (rr > 0.3) & (rr < 2.0)
    rr, t = rr[ok], t[ok]
    if len(rr) < MIN_RPEAKS:
        return None, None
    med = np.median(rr); mad = np.median(np.abs(rr - med)) + 1e-9
    keep = np.abs(rr - med) < 4 * 1.4826 * mad
    rr, t = rr[keep], t[keep]
    if len(rr) < MIN_RPEAKS:
        return None, None
    return rr - rr.mean(), t


def interp_4hz(rr, t):
    grid = np.arange(t[0], t[-1], 1.0 / FS_INTERP)
    x = np.interp(grid, t, rr)
    return x - x.mean()


def gate(series_by_subject, rng):
    rows = []
    for rec, x in series_by_subject:
        r = boundary_structure(x, rng)
        rows.append({"record": rec, **r})
        print(f"    {rec}: n {r['n_rr']:6d}  T {r['t_rev']:+.4f}  surr {r['surr_mean']:+.4f}+/-{r['surr_std']:.4f}  "
              f"p {r['p']:.3f}  {'STRUCTURED' if r['significant'] else ''}", flush=True)
    return rows


def frac(rows):
    return (sum(r["significant"] for r in rows) / len(rows)) if rows else float("nan")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    series = {}
    for rec in YOUNG + OLD:
        rr, t = clean_rr_as_applied(fantasia_beats(rec))
        series[rec] = (rr, t)
    out = {}
    for version in ("as_applied_beat_indexed", "as_described_4hz"):
        print(f"E2.1 Fantasia -- gate {version}")
        rng = np.random.default_rng(0)
        res = {}
        for group, recs in (("young", YOUNG), ("elderly", OLD)):
            items = []
            for rec in recs:
                rr, t = series[rec]
                if rr is None:
                    continue
                items.append((rec, rr if version.startswith("as_applied") else interp_4hz(rr, t)))
            res[group] = gate(items, rng)
        out[version] = {"young": {"fraction_structured": frac(res["young"]), "n": len(res["young"]),
                                  "n_structured": int(sum(r["significant"] for r in res["young"])),
                                  "per_subject": res["young"]},
                        "elderly": {"fraction_structured": frac(res["elderly"]), "n": len(res["elderly"]),
                                    "n_structured": int(sum(r["significant"] for r in res["elderly"])),
                                    "per_subject": res["elderly"]},
                        "sensitive": bool(frac(res["young"]) >= PASS_FRACTION)}
    p, s = out["as_applied_beat_indexed"], out["as_described_4hz"]
    verdict = (f"PRIMARY (gate as applied to I-CARE, beat-indexed): {'SENSITIVE' if p['sensitive'] else 'NOT SENSITIVE'} -- "
               f"young {p['young']['n_structured']}/{p['young']['n']} ({p['young']['fraction_structured']:.0%}), "
               f"elderly {p['elderly']['n_structured']}/{p['elderly']['n']} ({p['elderly']['fraction_structured']:.0%}); "
               f"bar 60% in the young. SECONDARY (gate as described, 4 Hz): "
               f"{'SENSITIVE' if s['sensitive'] else 'NOT SENSITIVE'} -- young {s['young']['n_structured']}/{s['young']['n']} "
               f"({s['young']['fraction_structured']:.0%}), elderly {s['elderly']['n_structured']}/{s['elderly']['n']} "
               f"({s['elderly']['fraction_structured']:.0%}). Prediction young > elderly: "
               f"{'met' if p['young']['fraction_structured'] > p['elderly']['fraction_structured'] else 'not met'} (primary), "
               f"{'met' if s['young']['fraction_structured'] > s['elderly']['fraction_structured'] else 'not met'} (secondary).")
    print("\n" + verdict)
    json.dump({"experiment": "fantasia_positive_control", "plan_id": "E2.1", "fills": "R2.1",
               "question": "Does the I-CARE estimability gate pass (>= 60% structured) in healthy young subjects, "
                           "where heartbeat time irreversibility is expected?",
               "data": "PhysioNet Fantasia 1.0.0, reviewed beat annotations (annotator 'ecg')",
               "params": {"n_surrogates": N_SURR, "min_rr": MIN_RPEAKS, "pass_fraction": PASS_FRACTION,
                          "interp_hz_secondary": FS_INTERP, "seed": 0},
               "primary_decides": "as_applied_beat_indexed", "results": out, "verdict": verdict},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
