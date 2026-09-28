"""Computational demonstration of Paper 1's indiscernibility argument (§§4-6).

See PRE-REGISTRATION.md (committed before this file). A small structural causal model of an agent
(capacity C, available reasons R, activity X, values V, endorsement E, choices) generates matched
conversions and manipulations. Each model of value change is written as a function of exactly the
inputs its definition reads: attitude-based models receive the attitudinal profile only;
history-sensitive ones also receive the history (who set which variable, when).

Usage:
    python -m experiments.paper1_control_trilemma.model_indiscernibility.run
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "model_indiscernibility")
N_DRAWS = 1000
SEED = 0
ETA = 0.3
TEMP = 0.1
N_CHOICES = 20
TAU = 0.5
C_DAMAGED = 0.1
N_TEST_OPTIONS = 10
N_GRID = 2000
TOL_PROFILE = 1e-12
TOL_OUT = 1e-9


# ------------------------------------------------------------------ agent and scenarios

@dataclass
class Profile:
    """The attitudinal profile: values, endorsements, capacities and choices over time."""
    V: np.ndarray          # (T+1, d)
    E: np.ndarray          # (T+1,)
    C: np.ndarray          # (T+1,)
    choices: np.ndarray    # (T+1, N_CHOICES) booleans: option a chosen over option b


@dataclass
class History:
    """Who set which variable at which time. source is 'internal' or 'external'."""
    events: list = field(default_factory=list)   # (t, variable, source)


@dataclass
class Draw:
    d: int
    T: int
    tc: int
    r: np.ndarray
    V0: np.ndarray
    opt_a: np.ndarray       # (T+1, N_CHOICES, d)
    opt_b: np.ndarray
    unif: np.ndarray        # (T+1, N_CHOICES) shared uniform draws for choices
    test_options: np.ndarray
    w_dl: np.ndarray        # Dietrich-List weighing relation (fixed)
    grid: np.ndarray        # value-learning hypothesis grid


def make_draw(rng) -> Draw:
    d = int(rng.integers(3, 9))
    T = int(rng.integers(15, 31))
    tc = int(rng.integers(3, T // 2 + 1))
    r = rng.normal(size=d); r /= np.linalg.norm(r)
    while True:                                   # prior values more than 90 degrees from r (mark U)
        V0 = rng.normal(size=d); V0 /= np.linalg.norm(V0)
        if V0 @ r < 0:
            break
    grid = rng.normal(size=(N_GRID, d)); grid /= np.linalg.norm(grid, axis=1, keepdims=True)
    return Draw(d, T, tc, r, V0,
                rng.normal(size=(T + 1, N_CHOICES, d)), rng.normal(size=(T + 1, N_CHOICES, d)),
                rng.uniform(size=(T + 1, N_CHOICES)), rng.normal(size=(N_TEST_OPTIONS, d)),
                rng.uniform(0.5, 1.5, size=d), grid)


def choices_from(V, dr: Draw):
    ua = np.einsum("tkd,td->tk", dr.opt_a, V)
    ub = np.einsum("tkd,td->tk", dr.opt_b, V)
    p = 1.0 / (1.0 + np.exp(-(ua - ub) / TEMP))
    return dr.unif < p


def simulate(dr: Draw, C, R_avail):
    """Agent's own dynamics given capacity C_t and available reasons R_avail[t]."""
    T = dr.T
    V = np.zeros((T + 1, dr.d)); E = np.zeros(T + 1)
    V[0] = dr.V0; E[0] = 1.0
    for t in range(1, T + 1):
        X = C[t] * R_avail[t] + (1 - C[t]) * V[t - 1]
        V[t] = V[t - 1] + ETA * (X - V[t - 1])
        E[t] = float(V[t] @ X / (np.linalg.norm(V[t]) * np.linalg.norm(X) + 1e-300))
    return V, E


def scenario(dr: Draw, name: str, target=None):
    """Return (profile, history, natural_V) for a scenario. natural_V: the trajectory with every
    external source removed (for the counterfactual benchmark)."""
    T, tc = dr.T, dr.tc
    t_idx = np.arange(T + 1)
    if name in ("S1", "S3", "S5"):
        R = np.where((t_idx >= tc)[:, None], dr.r if target is None else target, dr.V0)
        C_s1 = np.where(t_idx >= tc, 1.0, C_DAMAGED)
        V, E = simulate(dr, C_s1, R)
        if name == "S1":
            hist = History([(tc, "C", "internal"), (tc, "R", "internal")])
            return Profile(V, E, C_s1, choices_from(V, dr)), hist, V
        # replica manipulation: the agent's own capacity stays damaged and no reasons arrive;
        # an external source sets V, E and C to the conversion's (or a mirrored) trajectory.
        C_own = np.full(T + 1, C_DAMAGED)
        V_nat, _ = simulate(dr, C_own, np.tile(dr.V0, (T + 1, 1)))
        hist = History([(t, v, "external") for t in range(1, T + 1) for v in ("V", "E", "C")])
        return Profile(V.copy(), E.copy(), C_s1.copy(), choices_from(V, dr)), hist, V_nat
    if name in ("S2", "S4"):
        C = np.ones(T + 1)
        R = np.where((t_idx >= tc)[:, None], dr.r, dr.V0)
        V, E = simulate(dr, C, R)
        V_nat, _ = simulate(dr, C, np.tile(dr.V0, (T + 1, 1)))
        if name == "S2":
            return Profile(V, E, C, choices_from(V, dr)), History([(tc, "R", "external")]), V_nat
        hist = History([(t, v, "external") for t in range(1, T + 1) for v in ("V", "E", "C")])
        return Profile(V.copy(), E.copy(), C.copy(), choices_from(V, dr)), hist, V_nat
    raise ValueError(name)


# ------------------------------------------------------------------ models: attitude-based
# Each receives (profile, draw-level fixed structure) and nothing else.

def U(Vs, v):
    return -float(np.sum((v - Vs) ** 2))


def ex_ante(p: Profile, dr):                                    # §4.1
    return U(p.V[0], p.V[-1]) - U(p.V[0], p.V[0])


def ex_post(p: Profile, dr):                                    # §4.2
    return U(p.V[-1], p.V[-1]) - U(p.V[-1], p.V[0])


def pettigrew_aus(p: Profile, dr):                              # §4.3, §6.3
    w = np.exp(-np.linalg.norm(p.V - p.V[0], axis=1) / TAU); w /= w.sum()
    return float(sum(w[t] * (U(p.V[t], p.V[-1]) - U(p.V[t], p.V[0])) for t in range(len(w))))


def bykvist(p: Profile, dr):                                    # §4.3: each life by its own attitudes
    changed = np.mean([U(p.V[t], p.V[-1]) for t in range(len(p.V))])
    unchanged = U(p.V[0], p.V[0])
    return float(changed - unchanged)


def paul_revelation(p: Profile, dr):                            # §6.2
    return float(np.linalg.norm(p.V[-1] - p.V[0]))


def dietrich_list(p: Profile, dr):                              # §6.4: fixed weighing relation
    salient = tuple(int(i) for i in np.where(np.abs(p.V[-1]) > 0.2)[0])
    score = float(sum(dr.w_dl[i] * abs(p.V[-1][i]) for i in salient))
    return (salient, round(score, 12))


def hansson(p: Profile, dr):                                    # §6.5: revision postulates
    prior = list(np.argsort(-(dr.test_options @ p.V[0])))
    post = list(np.argsort(-(dr.test_options @ p.V[-1])))
    top = post[0]
    kemeny_closest = [top] + [o for o in prior if o != top]
    return bool(post == kemeny_closest)


def value_learning(p: Profile, dr):                             # §6.7: Bayesian IRL from choices
    diff = (dr.opt_a - dr.opt_b).reshape(-1, dr.d)
    y = p.choices.reshape(-1)
    z = diff @ dr.grid.T / TEMP                                  # (n_choices, n_grid)
    ll = np.where(y[:, None], -np.logaddexp(0, -z), -np.logaddexp(0, z)).sum(axis=0)
    post = np.exp(ll - ll.max()); post /= post.sum()
    theta = post @ dr.grid
    return float(theta @ p.V[-1] / (np.linalg.norm(theta) * np.linalg.norm(p.V[-1]) + 1e-300))


def attitudinal_corrigibility(p: Profile, dr):                 # §6.7
    return bool(p.V[-1] @ p.V[-1] > p.V[-1] @ p.V[0])


ATTITUDE_BASED = {"ex_ante": ex_ante, "ex_post": ex_post, "pettigrew_aus": pettigrew_aus,
                  "bykvist": bykvist, "paul_revelation": paul_revelation,
                  "dietrich_list": dietrich_list, "hansson": hansson,
                  "value_learning": value_learning,
                  "attitudinal_corrigibility": attitudinal_corrigibility}


# ------------------------------------------------------------------ models: history-sensitive

def counterfactual_penalty(p: Profile, h: History, V_nat, dr):  # Carroll et al. 2022, §6.8
    return float(np.linalg.norm(p.V[-1] - V_nat[-1]))


def target_condition(p: Profile, h: History, V_nat, dr):        # route (b), §5.4
    return any(src == "external" and var in ("V", "E", "X") for _, var, src in h.events)


def attitude_independent(p: Profile, h: History, V_nat, dr):    # route (a), §5.4
    return float(p.V[-1] @ dr.r - p.V[0] @ dr.r)


def negative_control(p: Profile, h: History, V_nat, dr):        # must separate S1 from S3
    return any(src == "external" and var == "V" for _, var, src in h.events)


def same(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return abs(a - b) <= TOL_OUT
    return a == b


def profile_gap(p: Profile, q: Profile):
    return max(float(np.max(np.abs(p.V - q.V))), float(np.max(np.abs(p.E - q.E))),
               float(np.max(np.abs(p.C - q.C))), float(np.sum(p.choices != q.choices)))


# ------------------------------------------------------------------ run

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    c = {k: 0 for k in ("P0", "P1", "P3_exante", "P3_expost", "P4", "P5", "P6_same", "P6_s5")}
    p2 = {m: 0 for m in ATTITUDE_BASED}
    p2_fail_examples = {}
    mag, aus_s1, aus_s3 = [], [], []
    pen = {"S1": [], "S2": [], "S3": [], "S4": []}
    for i in range(N_DRAWS):
        dr = make_draw(rng)
        P = {}
        for s in ("S1", "S2", "S3", "S4"):
            P[s] = scenario(dr, s)
        P["S5"] = scenario(dr, "S5", target=-dr.r)
        (p1, h1, n1), (p2_, h2, n2), (p3, h3, n3), (p4, h4, n4), (p5, h5, n5) = (P[s] for s in ("S1", "S2", "S3", "S4", "S5"))
        c["P0"] += negative_control(p1, h1, n1, dr) != negative_control(p3, h3, n3, dr)
        c["P1"] += profile_gap(p1, p3) <= TOL_PROFILE and profile_gap(p2_, p4) <= TOL_PROFILE
        for m, f in ATTITUDE_BASED.items():
            ok = same(f(p1, dr), f(p3, dr)) and same(f(p2_, dr), f(p4, dr))
            p2[m] += ok
            if not ok and m not in p2_fail_examples:
                p2_fail_examples[m] = {"draw": i, "S1": str(f(p1, dr)), "S3": str(f(p3, dr))}
        c["P3_exante"] += ex_ante(p1, dr) < 0
        c["P3_expost"] += ex_post(p1, dr) > 0 and ex_post(p3, dr) > 0
        cp = {s: counterfactual_penalty(*P[s], dr) for s in ("S1", "S2", "S3", "S4")}
        for s in cp:
            pen[s].append(cp[s])
        c["P4"] += cp["S1"] < TOL_OUT and cp["S2"] > TOL_OUT and abs(cp["S2"] - cp["S4"]) <= TOL_OUT
        tcnd = {s: target_condition(*P[s], dr) for s in P}
        c["P5"] += (not tcnd["S1"]) and (not tcnd["S2"]) and tcnd["S3"] and tcnd["S4"] and tcnd["S5"]
        ai = {s: attitude_independent(*P[s], dr) for s in ("S1", "S3", "S5")}
        c["P6_same"] += abs(ai["S1"] - ai["S3"]) <= TOL_OUT
        c["P6_s5"] += ai["S5"] < ai["S1"]
        mag.append(paul_revelation(p1, dr)); aus_s1.append(pettigrew_aus(p1, dr)); aus_s3.append(pettigrew_aus(p3, dr))

    rho1 = float(spearmanr(mag, aus_s1).correlation)
    rho3 = float(spearmanr(mag, aus_s3).correlation)
    N = N_DRAWS
    preds = {
        "P0_negative_control_separates": {"count": c["P0"], "bar": f"{N}/{N}", "met": c["P0"] == N},
        "P1_replica_reproduces_profile": {"count": c["P1"], "bar": f"{N}/{N}", "met": c["P1"] == N},
        "P2_attitude_based_models_indiscernible": {
            "per_model": p2, "bar": f"{N}/{N} each", "met": all(v == N for v in p2.values()),
            "failures": p2_fail_examples},
        "P3_ex_ante_loss": {"count": c["P3_exante"], "bar": ">= 990", "met": c["P3_exante"] >= 990},
        "P3_ex_post_gain_both": {"count": c["P3_expost"], "bar": ">= 990", "met": c["P3_expost"] >= 990},
        "P4_counterfactual_penalizes_occasioned_conversion_like_manipulation": {
            "count": c["P4"], "bar": ">= 990", "met": c["P4"] >= 990,
            "median_penalty": {s: float(np.median(v)) for s, v in pen.items()}},
        "P5_target_condition_separates": {"count": c["P5"], "bar": f"{N}/{N}", "met": c["P5"] == N},
        "P6_attitude_independent_blind_to_benevolent": {
            "same_S1_S3": c["P6_same"], "S5_below_S1": c["P6_s5"],
            "bar": f"{N}/{N} and >= 990", "met": c["P6_same"] == N and c["P6_s5"] >= 990},
        "P7_connectedness_discount": {
            "spearman_S1": rho1, "spearman_S3": rho3, "bar": "S1 < -0.5 and S3 equal within 1e-9",
            "met": bool(rho1 < -0.5 and abs(rho1 - rho3) <= TOL_OUT)},
    }
    met = {k: v["met"] for k, v in preds.items()}
    lines = [f"{k}: {'MET' if v else 'NOT MET'}" for k, v in met.items()]
    verdict = (("ALL PREDICTIONS MET. " if all(met.values()) else "NOT ALL PREDICTIONS MET. ") +
               f"Over {N} random draws: the replica manipulation reproduced the conversion's profile in "
               f"{c['P1']}/{N}; each of the 9 attitude-based models gave matched conversion and manipulation the "
               f"same output in {min(p2.values())}/{N} or more; the counterfactual benchmark gave an unassisted "
               f"conversion no penalty and an occasioned conversion the same positive penalty as its replica "
               f"manipulation in {c['P4']}/{N} (median penalties S2 {np.median(pen['S2']):.3f}, S4 "
               f"{np.median(pen['S4']):.3f}); the target condition separated conversions from manipulations in "
               f"{c['P5']}/{N}; the attitude-independent standard scored conversion and benevolent manipulation "
               f"alike in {c['P6_same']}/{N}; Spearman(size of change, Pettigrew aggregate) = {rho1:.3f} for "
               f"conversions and {rho3:.3f} for manipulations. P2 holds by construction for profile-only "
               f"implementations; P4 and P7 are the parts that could have failed.")
    for l in lines:
        print(l)
    print(verdict)
    json.dump({"experiment": "model_indiscernibility", "fills": None,
               "question": "Do implementations of the value-change models discussed in Paper 1 §§4-6 treat a "
                           "conversion and an attitudinally identical manipulation alike, and do the §6.8 "
                           "benchmark and the two ways out of §5.4 behave as the paper says?",
               "params": {"n_draws": N, "seed": SEED, "eta": ETA, "temp": TEMP, "n_choices": N_CHOICES,
                          "tau": TAU, "c_damaged": C_DAMAGED, "n_test_options": N_TEST_OPTIONS,
                          "n_grid": N_GRID},
               "predictions": preds, "all_met": all(met.values()), "verdict": verdict},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
