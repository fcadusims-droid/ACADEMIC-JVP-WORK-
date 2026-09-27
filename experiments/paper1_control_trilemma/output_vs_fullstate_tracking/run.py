"""E1.1 -- output tracking versus full-state tracking (Paper 1, Appendix A.1).

See PRE-REGISTRATION.md. Two coupled Ornstein-Uhlenbeck coordinates; a reference that steps
from 0 to 1 at t = 1000 is tracked on x only (output) or on x and y (full state).
Euler-Maruyama, dt = 0.001, T = 2000, 10 seeds, common random numbers across conditions.

Usage:
    python -m experiments.paper1_control_trilemma.output_vs_fullstate_tracking.run
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "output_vs_fullstate_tracking")

SIGMA = 1.0
DT = 1e-3
T_END = 2000.0
T_STEP = 1000.0
T_MEASURE = 1200.0          # 200 time units after the step are discarded
KS = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
CS = [0.0, 0.3]
SEEDS = list(range(10))
CHUNK = 100_000


def simulate():
    """Integrate all conditions at once. Axis order: (condition, k, c, seed)."""
    nk, nc, ns = len(KS), len(CS), len(SEEDS)
    k = np.array(KS)[None, :, None, None]
    c = np.array(CS)[None, None, :, None]
    full = np.array([0.0, 1.0])[:, None, None, None]        # 0 = output only, 1 = full state
    shape = (2, nk, nc, ns)
    x = np.zeros(shape)
    y = np.zeros(shape)
    acc = {name: np.zeros(shape) for name in ("sy", "syy", "se", "see")}
    n_meas = 0
    rngs = [np.random.default_rng(s) for s in SEEDS]
    n_steps = int(round(T_END / DT))
    i_step = int(round(T_STEP / DT))
    i_meas = int(round(T_MEASURE / DT))
    sq = SIGMA * np.sqrt(DT)
    for start in range(0, n_steps, CHUNK):
        m = min(CHUNK, n_steps - start)
        # per-seed streams, identical across conditions (common random numbers)
        noise = np.stack([g.standard_normal((m, 2)) for g in rngs], axis=1) * sq  # (m, seed, 2)
        for j in range(m):
            i = start + j
            r = 1.0 if i >= i_step else 0.0
            u = -k * (x - r)
            v = -k * y * full
            dw = noise[j]
            x_new = x + (-x + c * y + u) * DT + dw[:, 0]
            y = y + (-y + c * x + v) * DT + dw[:, 1]
            x = x_new
            if i + 1 >= i_meas:
                e = x - (1.0 if i + 1 >= i_step else 0.0)
                acc["sy"] += y
                acc["syy"] += y * y
                acc["se"] += e
                acc["see"] += e * e
                n_meas += 1
    var_y = acc["syy"] / n_meas - (acc["sy"] / n_meas) ** 2
    var_e = acc["see"] / n_meas - (acc["se"] / n_meas) ** 2
    return var_y, var_e, n_meas


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    var_y, var_e, n_meas = simulate()
    ref = SIGMA ** 2 / 2
    table = []
    for ci, cname in enumerate(("output", "full_state")):
        for kc, cval in enumerate(CS):
            for ki, kval in enumerate(KS):
                vy = var_y[ci, ki, kc]
                ve = var_e[ci, ki, kc]
                table.append({"condition": cname, "c": cval, "k": kval,
                              "var_y_mean": float(vy.mean()), "var_y_sd": float(vy.std(ddof=1)),
                              "var_y_min": float(vy.min()), "var_y_max": float(vy.max()),
                              "var_y_over_ref": float(vy.mean() / ref),
                              "var_x_minus_r_mean": float(ve.mean()),
                              "var_x_minus_r_sd": float(ve.std(ddof=1)),
                              "var_y_per_seed": [float(v) for v in vy]})

    def rows(cond, cval):
        return [t for t in table if t["condition"] == cond and t["c"] == cval]

    full_checks = {}
    for cval in CS:
        m = [t["var_y_mean"] for t in rows("full_state", cval)]
        full_checks[str(cval)] = {"monotone_strictly_decreasing": bool(all(a > b for a, b in zip(m, m[1:]))),
                                  "var_y_at_k50_over_ref": m[-1] / ref,
                                  "below_5pct_at_k50": bool(m[-1] < 0.05 * ref)}
    out0 = [t["var_y_over_ref"] for t in rows("output", 0.0)]
    out3 = rows("output", 0.3)[-1]["var_y_over_ref"]
    output_checks = {"c0_all_within_10pct": bool(all(abs(v - 1) <= 0.10 for v in out0)),
                     "c0_ratios": out0,
                     "c03_k50_ratio": out3,
                     "c03_k50_at_least_90pct": bool(out3 >= 0.90)}
    full_pass = all(v["monotone_strictly_decreasing"] and v["below_5pct_at_k50"] for v in full_checks.values())
    output_pass = output_checks["c0_all_within_10pct"] and output_checks["c03_k50_at_least_90pct"]
    passed = full_pass and output_pass
    verdict = (
        f"{'PREDICTION MET' if passed else 'PREDICTION NOT MET'}. Full-state tracking: var(y) falls "
        f"monotonically with k for c = 0 and 0.3 "
        f"({'yes' if all(v['monotone_strictly_decreasing'] for v in full_checks.values()) else 'no'}) "
        f"and at k = 50 is {full_checks['0.0']['var_y_at_k50_over_ref']:.1%} (c = 0) and "
        f"{full_checks['0.3']['var_y_at_k50_over_ref']:.1%} (c = 0.3) of sigma^2/2 (bar < 5%). "
        f"Output tracking: with c = 0, var(y)/(sigma^2/2) ranges {min(out0):.3f}-{max(out0):.3f} over k "
        f"(bar within +/-10%); with c = 0.3 it is {out3:.3f} at k = 50 (bar >= 0.90). Seed means of 10 "
        f"seeds; variances over t in [1200, 2000].")
    print(verdict)
    json.dump({"experiment": "output_vs_fullstate_tracking", "plan_id": "E1.1", "fills": "R-A1",
               "question": "Does tracking one coordinate leave the variance of an uncoupled (or weakly "
                           "coupled) coordinate unchanged, while full-state tracking suppresses it?",
               "params": {"sigma": SIGMA, "dt": DT, "T": T_END, "t_step": T_STEP,
                          "measure_window": [T_MEASURE, T_END], "k": KS, "c": CS, "seeds": SEEDS,
                          "samples_per_run": n_meas, "reference_var": ref},
               "full_state_checks": full_checks, "output_checks": output_checks,
               "prediction_met": passed, "verdict": verdict, "table": table},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
