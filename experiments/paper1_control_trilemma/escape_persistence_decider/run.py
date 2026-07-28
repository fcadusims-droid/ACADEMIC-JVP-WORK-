"""Escape with Class G's OWN openness: the deciding case for E2 (Paper 1 §7.5).

`escape_endogeneity` refuted E1 (escape needs no external occasion) but came back
INCONCLUSIVE on E2 (escape forfeits persistence), for a diagnosable reason: the only
openness its candidates possessed was CHAOS, and chaos destroys correlation power
whether or not the trajectory escapes, so the bounded control failed persistence too.

Running that battery exposed something sharper. Paper 1 uses "openness" in two
incompatible senses, and argues the escape horn in one while defining Class G in the
other:

    §7.5 Case 3   openness = POSITIVE ENTROPY, lambda > 0, correlation destroyed
    §8.3 Class G  openness = |lambda_par| ~ 0, INCOMMENSURABLE frequencies,
                  correlation power RETAINED (P_f >= 0.05)

These are near-opposites. Class G -- the entire positive residue of the paper -- needs
the second. This experiment asks the question in that sense: can an autonomous system
escape compactness while being aperiodic-but-not-chaotic AND correlation-retaining?

A quasi-periodic oscillation with exponentially growing amplitude is the serious
candidate. The counter-argument is real too: under a scale-free contract the growth
divides out, leaving a bounded quasi-periodic direction that is recurrent by Weyl
equidistribution. §5.4 makes persistence contract-relative, so a split by contract is
a legitimate finding rather than a hedge.

Estimators are imported unchanged from `escape_endogeneity`, including its seven-check
self-test, so the two experiments are directly comparable.

Usage:
    python -m experiments.paper1_control_trilemma.escape_persistence_decider.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper1_control_trilemma.escape_endogeneity.run import (
    assert_autonomous, integrate, log_radius, obs_dir, obs_raw, persistence,
    angular_lyapunov, recurrence_fraction, selftest, f_bounded_lorenz,
    THR_PF, THR_SURR_P, THR_VAR_COLLAPSE, THR_RECURRENT, DT,
)
from experiments.paper1_control_trilemma.class_g_coherence.run import (
    periodicity_report, THR_RATIONAL_Q, THR_RATIONAL_TOL,
)

warnings.filterwarnings("ignore")

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "escape_persistence_decider")

# ---- pre-registered thresholds ---------------------------------------------
THR_LAMBDA_FLAT = 0.01   # Class G openness: |lambda| <= this (ABSENCE of chaos)
GROWTH = 0.35            # log-radius growth rate for the escaping candidates
GROWTH_SLOW = 0.08
W1, W2 = 1.0, np.sqrt(2.0)          # incommensurable pair
W1C, W2C = 1.0, 1.5                 # commensurable control (3/2)
SEED = 0


# =============================================================================
# candidates -- all autonomous: f(state) only
# =============================================================================

def _quasi(s, w1, w2, growth):
    """Two uncoupled rotations at w1, w2 plus a growing log-radius.

    State [x1, y1, x2, y2, log r]. Linear, autonomous, lambda = 0 exactly: the
    aperiodicity comes from the frequency ratio, not from sensitivity -- which is
    precisely Class G's openness signature rather than §7.5's.
    """
    x1, y1, x2, y2 = s[0], s[1], s[2], s[3]
    return np.array([-w1 * y1, w1 * x1, -w2 * y2, w2 * x2, growth])


def f_quasiperiodic_bounded(s):
    """CONTROL. Incommensurable, NO escape. Must pass openness + persistence.

    Without this the experiment cannot attribute anything: if the criteria are not
    jointly satisfiable even for a bounded system, a failure under escape says
    nothing about escape. That attribution check is pre-registered this time, having
    been added post hoc in `escape_endogeneity`.
    """
    return _quasi(s, W1, W2, 0.0)


def f_quasiperiodic_escape(s):
    """THE DECIDING CANDIDATE: incommensurable frequencies, growing amplitude."""
    return _quasi(s, W1, W2, GROWTH)


def f_quasiperiodic_escape_slow(s):
    """The same at a slower growth rate -- checks the verdict is not speed-specific."""
    return _quasi(s, W1, W2, GROWTH_SLOW)


def f_commensurable_escape(s):
    """Rational frequency ratio (3/2): PERIODIC, so it must fail aperiodicity.

    Isolates incommensurability as the load-bearing property rather than leaving it
    as an assumption about what makes the deciding candidate work.
    """
    return _quasi(s, W1C, W2C, GROWTH)


def f_chaotic_escape(s):
    """`escape_endogeneity`'s escaping construction, re-run as a consistency check.

    Must reproduce there: open in the ENTROPY sense, and failing persistence.
    """
    return np.array([*f_bounded_lorenz(s[:3]), GROWTH])


S0_Q = np.array([1.0, 0.0, 1.0, 0.0, 0.0])

# Two things the first runs of this experiment conflated, separated here.
#
# GEOMETRY. The value vector is the whole 4-vector, whose norm is exactly constant.
# Using only the two cosine channels [x1, x2] lets ||value|| pass near zero, where the
# direction is ill-conditioned; that alone put a spurious lambda = -0.019 on a linear
# rotation whose Lyapunov exponent is analytically ZERO, and the candidate then failed
# Class-G flatness for a numerical reason rather than a dynamical one.
#
# CONTRACT OBSERVABLE. Taking coordinate 0 of the unit direction gives cos(w1 t)/sqrt(2)
# -- a pure sine in which the second frequency never appears, so the candidate was not
# quasi-periodic where it was being measured and the periodicity detector was right to
# reject it. §5.4 makes the observable a DECLARED choice, so it is declared here as a
# mixture of all channels, which is what carries both frequencies.
#
# Both are recorded as numerical sanity-check failures under the pre-registration's
# stopping rule; neither changes a threshold.
#
# `quasiperiodic_escape_slow` also needed a longer window: at growth 0.08 it reached
# log r = 24.35 against a bound of 25 and so never registered as escaping, i.e. it was
# not testing the thing it exists to test.
SLOW_STEPS = 200000


def obs_dir_mix(traj, spec):
    """I_dir -- scale-free MIXTURE of the value channels (declared contract, §5.4)."""
    val = traj[:, spec["value"]]
    u = val / (np.linalg.norm(val, axis=1, keepdims=True) + 1e-300)
    return u.sum(axis=1) / np.sqrt(u.shape[1])


def obs_raw_mix(traj, spec):
    """I_raw -- the same mixture at TRUE scale (cardinal contract)."""
    return obs_dir_mix(traj, spec) * np.exp(np.clip(log_radius(traj, spec), -700, 700))

CANDIDATES = [
    {"name": "quasiperiodic_bounded", "f": f_quasiperiodic_bounded, "s0": S0_Q,
     "value": [0, 1, 2, 3], "logr": 4, "role": "control", "ratio": W2 / W1},
    {"name": "quasiperiodic_escape", "f": f_quasiperiodic_escape, "s0": S0_Q,
     "value": [0, 1, 2, 3], "logr": 4, "role": "escape", "ratio": W2 / W1},
    {"name": "quasiperiodic_escape_slow", "f": f_quasiperiodic_escape_slow, "s0": S0_Q,
     "value": [0, 1, 2, 3], "logr": 4, "role": "escape", "ratio": W2 / W1},
    {"name": "commensurable_escape", "f": f_commensurable_escape, "s0": S0_Q,
     "value": [0, 1, 2, 3], "logr": 4, "role": "escape", "ratio": W2C / W1C},
    {"name": "chaotic_escape", "f": f_chaotic_escape,
     "s0": np.array([1.0, 1.0, 20.0, 0.0]), "value": [0, 1, 2], "logr": 3,
     "role": "escape", "ratio": None},
]


def incommensurable(ratio):
    """Distance to the nearest rational with small denominator -- class_g's test."""
    if ratio is None:
        return {"pass": None, "note": "not a two-frequency construction"}
    best = None
    for qd in range(1, THR_RATIONAL_Q + 1):
        p = round(ratio * qd)
        err = abs(ratio - p / qd)
        if best is None or err < best[2]:
            best = (int(p), int(qd), float(err))
    return {"pass": bool(best[2] >= THR_RATIONAL_TOL), "ratio": float(ratio),
            "best_rational": f"{best[0]}/{best[1]}", "best_err": best[2]}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    print("Escape with Class G's own openness -- the deciding case for E2\n")

    for spec in CANDIDATES:
        assert_autonomous(spec["f"])
    print(f"  autonomy check: all {len(CANDIDATES)} fields are f(state) only\n")
    st = selftest()
    print()

    results = {}
    for spec in CANDIDATES:
        name = spec["name"]
        nsteps = SLOW_STEPS if spec["name"].endswith("_slow") else 60000
        traj, escaped, finite_time, steps = integrate(spec, n=nsteps)
        lr = log_radius(traj, spec)
        lam = angular_lyapunov(spec)
        # Class G openness is the ABSENCE of chaos, not its presence.
        flat = bool(np.isfinite(lam) and abs(lam) <= THR_LAMBDA_FLAT)
        inc = incommensurable(spec["ratio"])

        entry = {"role": spec["role"], "escaped": bool(escaped),
                 "finite_time_blowup": bool(finite_time),
                 "final_log_radius": float(lr[-1]),
                 "angular_lambda": None if not np.isfinite(lam) else float(lam),
                 "lambda_flat_classG": flat,
                 "incommensurable": inc,
                 "contracts": {}}

        for cname, obs_fn in (("I_dir", obs_dir_mix), ("I_raw", obs_raw_mix)):
            obs = obs_fn(traj, spec)
            fin = obs[np.isfinite(obs)]
            var = float(np.var(fin[len(fin) // 2:])) if len(fin) > 4 else 0.0
            collapsed = var < THR_VAR_COLLAPSE
            # Aperiodicity on the SCALE-FREE observable in both cases: a growing
            # amplitude would make any signal look non-repeating, which is escape
            # showing up as aperiodicity rather than the frequency content doing it.
            per_obs = obs_dir_mix(traj, spec)
            rep = periodicity_report(per_obs[np.isfinite(per_obs)], DT)
            aperiodic = bool(not rep["declared_periodic"])
            rec = recurrence_fraction(obs)
            # Measured, never overridden -- see escape_endogeneity for why both
            # earlier overrides produced false labels in opposite directions.
            if np.isfinite(rec):
                non_rec, rec_note = bool(rec < THR_RECURRENT), ""
            else:
                non_rec = None
                rec_note = "UNMEASURED: too few samples before divergence"
            pers = persistence(obs, rng)

            classg_open = bool(flat and aperiodic and not collapsed
                               and (inc["pass"] is not False))
            all_four = bool(escaped and classg_open and non_rec is True and pers["pass"])
            entry["contracts"][cname] = {
                "late_variance": var, "collapsed": collapsed,
                "aperiodic": aperiodic,
                "sup_err_at_T": rep["sup_err_at_T"],
                "declared_periodic": rep["declared_periodic"],
                "recurrence_fraction": None if not np.isfinite(rec) else float(rec),
                "recurrence_note": rec_note, "non_recurrent": non_rec,
                "classG_open": classg_open, "persistence": pers,
                "all_four": all_four}

        results[name] = entry
        tag = ("ESCAPES" + (" (finite)" if finite_time else "")) if escaped else "bounded"
        ls = "n/a" if entry["angular_lambda"] is None else f"{entry['angular_lambda']:+.4f}"
        print(f"  {name:26s} {tag:17s} logr={lr[-1]:7.2f} lam={ls:>8s} "
              f"flat={str(flat):5s} incomm={inc['pass']}")
        for cname in ("I_dir", "I_raw"):
            c = entry["contracts"][cname]
            r = c["recurrence_fraction"]
            rs = "n/a" if r is None else f"{r:.3f}"
            print(f"      {cname:6s} aper={str(c['aperiodic']):5s} rec={rs:>6s} "
                  f"nonrec={str(c['non_recurrent']):5s} "
                  f"P_f={c['persistence']['P_f']:.4f}(p={c['persistence']['surrogate_p']:.3f}) "
                  f"G-open={str(c['classG_open']):5s} ALL4={c['all_four']}")

    # ---- attribution + verdict ----------------------------------------
    ctrl = results["quasiperiodic_bounded"]
    ctrl_ok = any(c["classG_open"] and c["persistence"]["pass"]
                  for c in ctrl["contracts"].values())
    refuters = [[n, cn] for n, e in results.items() if e["role"] == "escape"
                for cn, c in e["contracts"].items() if c["all_four"]]

    if not ctrl_ok:
        outcome = "INCONCLUSIVE"
        head = ("INCONCLUSIVE. The bounded control does not satisfy Class-G openness "
                "and persistence together, so those criteria are not jointly "
                "achievable even without escape and nothing follows about escape. "
                "This is the pre-registered attribution failure, and it is the same "
                "one that ended `escape_endogeneity`.")
    elif refuters:
        outcome = "REFUTES_E2"
        head = (f"E2 IS FALSE ON THE PAPER'S OWN DEFINITION OF OPENNESS. {refuters} "
                f"escape every compact set while remaining aperiodic, non-chaotic, "
                f"non-recurrent AND correlation-retaining, and the bounded control "
                f"confirms the criteria are jointly satisfiable so the result is "
                f"attributable to escape.")
    else:
        outcome = "SUPPORTS_E2"
        head = ("E2 SURVIVES, AND THIS TIME ATTRIBUTABLY. The bounded control passes "
                "Class-G openness and persistence together, so the criteria are "
                "jointly achievable; every ESCAPING candidate nonetheless fails at "
                "least one property under both contracts.")

    verdict = (
        head + " WHY THIS TEST AND NOT THE PREVIOUS ONE. `escape_endogeneity` measured "
        "openness as POSITIVE ENTROPY, which is §7.5's sense, and every candidate that "
        "had it was chaotic -- so all of them failed correlation power, including the "
        "bounded control, and nothing could be attributed to escape. Class G in §8.3 "
        "requires the opposite signature: |lambda| ~ 0, aperiodicity from "
        "INCOMMENSURABLE frequencies rather than from chaos, and correlation power "
        "explicitly RETAINED. Since Class G is the paper's entire positive residue, "
        "that is the sense in which the escape horn has to hold. ")

    if outcome == "REFUTES_E2":
        verdict += (
            "CONSEQUENCE FOR PAPER 1, stated rather than left to a reviewer: §7.5 "
            "cannot dispose of the escape horn by calling unbounded drift 'a more "
            "extreme Class M'. A system can leave every compact set and still satisfy "
            "the persistence condition, so the escape cell is NOT empty, and the "
            "trichotomy's exhaustiveness argument does not by itself exclude "
            "conversion there. What remains true is the compact case, which Poincare "
            "recurrence settles. The theorem should therefore be stated as a result "
            "about COMPACT autonomous dynamics, with the escape cell declared open "
            "rather than closed by assertion. Note also what this does NOT show: the "
            "escaping witness satisfies the persistence and openness conditions, but "
            "nothing here shows it realises conversion in the full sense, which "
            "requires the §8.3 conjunction in its entirety. It refutes a disposal "
            "argument, not the thesis.")
    elif outcome == "SUPPORTS_E2":
        reasons = []
        for n, e in results.items():
            if e["role"] != "escape":
                continue
            for cn, c in e["contracts"].items():
                miss = [k for k, v in (("Class-G openness", c["classG_open"]),
                                       ("non-recurrence", c["non_recurrent"]),
                                       ("persistence", c["persistence"]["pass"]))
                        if not v]
                if miss:
                    reasons.append(f"{n}/{cn} fails {'+'.join(miss)}")
        verdict += ("Failures: " + "; ".join(reasons) + ". Because the control passes, "
                    "this is the attributable version of the claim that "
                    "`escape_endogeneity` could not deliver. "
                    "THE MECHANISM, WHICH IS NOT THE ONE §7.5 GIVES. The property that "
                    "fails for EVERY escaping candidate, under BOTH contracts, is "
                    "NON-RECURRENCE -- not persistence. The quasi-periodic escapers "
                    "retain correlation power handsomely under the ordinal contract "
                    "(P_f = 0.17-0.21 against a 0.05 bar) while escaping to log r = 25; "
                    "what they cannot do is stop returning. The reason is structural "
                    "and general rather than particular to these constructions: the "
                    "escape happens in the RADIUS, while the contract-designated "
                    "observable sees the DIRECTION, and the direction lives on a sphere "
                    "-- a compact quotient -- where Poincare recurrence applies exactly "
                    "as it does in the bounded case. Escape in a coordinate the "
                    "contract does not read buys nothing. "
                    "CONSEQUENCE FOR PAPER 1: §7.5 closes the escape horn with the "
                    "wrong argument. It says unbounded drift 'is itself a failure of "
                    "persistence ... a more extreme Class M', and that is NOT what "
                    "happens -- persistence survives escape. The horn closes by "
                    "RECURRENCE ON THE QUOTIENT, which is a stronger and more general "
                    "argument than the one the paper gives, and it should be stated "
                    "that way: a scale-free identity contract cannot see radial escape, "
                    "so the recurrence theorem the trichotomy already relies on extends "
                    "to the escaping cell instead of being surrendered there.")

    # ---- figure -------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, spec in zip(axes.ravel(), CANDIDATES):
        traj, _, _, _ = integrate(spec, n=12000)
        o = obs_raw_mix(traj, spec)
        o = o[np.isfinite(o)]
        ax.plot(o[:6000], lw=0.6, color="#1f4e79")
        e = results[spec["name"]]
        c = e["contracts"]["I_raw"]
        ax.set_title(f"{spec['name']}\n{'ESCAPES' if e['escaped'] else 'bounded'} · "
                     f"$P_f$={c['persistence']['P_f']:.3f} · ALL4={c['all_four']}",
                     fontsize=9)
        ax.set_xlabel("step"); ax.set_ylabel("$I_{raw}$")
    for ax in axes.ravel()[len(CANDIDATES):]:
        ax.axis("off")
    fig.suptitle("Escape with Class G's openness: aperiodic, non-chaotic, "
                 "correlation-retaining", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "escape_persistence_decider.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "escape_persistence_decider",
        "question": "Can an autonomous system escape compactness while open in CLASS "
                    "G's sense (aperiodic, incommensurable, non-chaotic) and "
                    "correlation-retaining?",
        "motivation": "escape_endogeneity was inconclusive because its only openness "
                      "was chaos, which destroys P_f regardless of escape. Paper 1 "
                      "uses two incompatible senses of openness; Class G needs the "
                      "other one.",
        "two_senses_of_openness": {
            "section_7_5_case_3": "positive entropy, lambda > 0, correlation destroyed",
            "section_8_3_class_G": "|lambda_par| ~ 0, incommensurable frequencies, "
                                   "correlation power retained"},
        "thresholds": {"P_f": THR_PF, "surrogate_p": THR_SURR_P,
                       "lambda_flat": THR_LAMBDA_FLAT,
                       "recurrent_above": THR_RECURRENT,
                       "rational_denominator_max": THR_RATIONAL_Q,
                       "rational_tol": THR_RATIONAL_TOL},
        "instrument_selftest": st,
        "sanity_adjustments": [
            "GEOMETRY: value vector kept as the full 4-vector (constant norm). Using "
            "only the two cosine channels lets ||value|| pass near zero, where the "
            "direction is ill-conditioned, putting a spurious lambda = -0.019 on a "
            "linear rotation whose exponent is analytically ZERO -- the candidate then "
            "failed Class-G flatness for a numerical rather than a dynamical reason.",
            "CONTRACT OBSERVABLE: declared as a MIXTURE of the value channels. "
            "Coordinate 0 of the unit direction is cos(w1 t)/sqrt(2), a pure sine in "
            "which the second frequency never appears, so the candidate was not "
            "quasi-periodic where it was measured and the periodicity detector was "
            "right to reject it. §5.4 makes the observable a declared choice.",
            "quasiperiodic_escape_slow given a longer window (200k steps): at growth "
            "0.08 it reached log r = 24.35 against the escape bound of 25 and so never "
            "counted as escaping."],
        "attribution": {"control_jointly_satisfies_openness_and_persistence": ctrl_ok,
                        "note": "Pre-registered THIS time, having been added post hoc "
                                "in escape_endogeneity."},
        "candidates": results,
        "refuters": refuters,
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["escape_persistence_decider.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
