"""E1.2 -- recurrence time against dimension on an ergodic torus rotation (Paper 1, Appendix A.2).

See PRE-REGISTRATION.md. theta -> theta + alpha (mod 1), alpha_i = frac(sqrt(p_i)) for the first
five primes; return set A = box of side 0.1 centred at (0.5, ..., 0.5); 200 initial points in A;
steps to first return, capped at 1e7. Kac: mean return time = 1/mu(A) = 10^d.

Usage:
    python -m experiments.paper1_control_trilemma.kac_recurrence_dimension.run
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "kac_recurrence_dimension")
PRIMES = [2, 3, 5, 7, 11]
SIDE = 0.1
N_POINTS = 200
CAP = 10_000_000
SEED = 0
BLOCK = 20_000


def return_times(d, rng):
    alpha = np.array([math.sqrt(p) % 1.0 for p in PRIMES[:d]])
    lo, hi = 0.5 - SIDE / 2, 0.5 + SIDE / 2
    theta0 = rng.uniform(lo, hi, size=(N_POINTS, d))
    times = np.full(N_POINTS, -1, dtype=np.int64)
    pending = np.arange(N_POINTS)
    n0 = 1
    while len(pending) and n0 <= CAP:
        n = np.arange(n0, min(n0 + BLOCK, CAP + 1))
        # theta_n = theta_0 + n * alpha (mod 1), computed directly (no accumulated rounding)
        pos = (theta0[pending][:, None, :] + n[None, :, None] * alpha[None, None, :]) % 1.0
        inside = np.all((pos >= lo) & (pos < hi), axis=2)
        hit = inside.any(axis=1)
        first = inside.argmax(axis=1)
        times[pending[hit]] = n[first[hit]]
        pending = pending[~hit]
        n0 = n[-1] + 1
    return times, len(pending)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    rows = []
    for d in range(1, 6):
        t, n_capped = return_times(d, rng)
        ok = t[t > 0].astype(float)
        kac = 10.0 ** d
        rows.append({"d": d, "kac_expected": kac, "mean": float(ok.mean()), "sd": float(ok.std(ddof=1)),
                     "median": float(np.median(ok)), "min": int(ok.min()), "max": int(ok.max()),
                     "n_distinct_return_times": int(len(np.unique(ok))),
                     "ratio_to_kac": float(ok.mean() / kac), "within_15pct": bool(abs(ok.mean() / kac - 1) <= 0.15),
                     "n_capped": int(n_capped)})
        print(f"d={d}: mean {ok.mean():.1f}  (Kac {kac:.0f}, ratio {ok.mean()/kac:.3f})  sd {ok.std(ddof=1):.1f}  capped {n_capped}")
    ds = np.array([r["d"] for r in rows], float)
    lm = np.log10([r["mean"] for r in rows])
    slope, intercept = np.polyfit(ds, lm, 1)
    all15 = all(r["within_15pct"] for r in rows)
    slope_ok = 0.9 <= slope <= 1.1
    passed = all15 and slope_ok
    verdict = (f"{'PREDICTION MET' if passed else 'PREDICTION NOT MET'}. Mean return time / Kac value "
               f"(10^d) for d = 1..5: " + ", ".join(f"{r['ratio_to_kac']:.3f}" for r in rows) +
               f" (bar within +/-15% each: {'yes' if all15 else 'no'}); slope of log10(mean) on d = "
               f"{slope:.3f} (bar 0.9-1.1). {sum(r['n_capped'] for r in rows)} of {5 * N_POINTS} starts hit the cap.")
    print(verdict)
    json.dump({"experiment": "kac_recurrence_dimension", "plan_id": "E1.2", "fills": "R-A2",
               "question": "Does the mean return time to a box of side 0.1 grow as 10^d (Kac's lemma) "
                           "for an ergodic rotation of the d-torus, d = 1..5?",
               "params": {"alpha_primes": PRIMES, "side": SIDE, "n_points": N_POINTS, "cap": CAP, "seed": SEED},
               "rows": rows, "slope_log10_mean_vs_d": float(slope), "intercept": float(intercept),
               "prediction_met": passed, "verdict": verdict},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
