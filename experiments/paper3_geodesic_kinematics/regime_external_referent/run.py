"""H2 -- can the three-regime demarcation be bound to an external referent (AASM staging)?

The Phase-0 gate found the demarcation not externally falsifiable (regimes defined by the
protocol's own criteria). This tests the reviewer's proposed repair: a PRE-REGISTERED mapping
from the protocol's dynamical regime (drift/dispersion; collapse has no AASM counterpart) to
AASM sleep stages, scored against the human hypnogram with a permutation null.

Usage:
    python -m experiments.paper3_geodesic_kinematics.regime_external_referent.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum, _R, _sphere_dist_emb
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, discover_subjects, WIN_SEC, STEP_SEC, EIG_FLOOR,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "regime_external_referent")
N_SUBJECTS = 15
EXP_WIN = 10          # windows over which local geodesic expansion is measured
N_PERM = 2000
DRIFT_STAGES = {"N2", "N3"}
DISP_STAGES = {"W", "REM"}


def protocol_regime(covs):
    """Per-window coarse regime from the protocol's own criteria on the SPD trajectory:
    local geodesic expansion (Lyapunov proxy). Low expansion => drift/persistent;
    high => dispersion. (Collapse is tracked separately and has no AASM counterpart.)"""
    E, C = embed_cumsum(covs)
    n = len(covs)
    step = np.array([_sphere_dist_emb(E[i], E[i + 1]) for i in range(n - 1)])
    step = np.concatenate([step, step[-1:]])
    # local expansion = rolling mean geodesic step (dispersion is large steps sustained)
    expan = np.array([step[max(0, i - EXP_WIN):i + 1].mean() for i in range(n)])
    thr = np.median(expan)
    return np.where(expan > thr, "dispersion", "drift"), expan


def cramers_v(a, b):
    """Cramér's V between two categorical label arrays."""
    cats_a = sorted(set(a)); cats_b = sorted(set(b))
    if len(cats_a) < 2 or len(cats_b) < 2:
        return 0.0
    table = np.zeros((len(cats_a), len(cats_b)))
    ia = {c: i for i, c in enumerate(cats_a)}; ib = {c: i for i, c in enumerate(cats_b)}
    for x, y in zip(a, b):
        table[ia[x], ib[y]] += 1
    n = table.sum()
    row = table.sum(1, keepdims=True); col = table.sum(0, keepdims=True)
    exp = row @ col / n
    chi2 = np.nansum((table - exp) ** 2 / np.where(exp > 0, exp, np.nan))
    k = min(table.shape)
    return float(np.sqrt(chi2 / (n * (k - 1)))) if n > 0 and k > 1 else 0.0


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    print("H2 -- binding the three-regime demarcation to AASM staging (external referent)\n")

    subs = discover_subjects()
    reg_all, aasm_all, rec_ids = [], [], []
    used = 0
    for p, h in subs:
        if used >= N_SUBJECTS:
            break
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception:
            continue
        covs, labs, centers = sliding_covs_labeled(data, fs, stage)
        # keep windows whose AASM label maps to drift or dispersion stages
        reg, _ = protocol_regime(covs)
        for r, l in zip(reg, labs):
            if l in DRIFT_STAGES:
                reg_all.append(r); aasm_all.append("drift_stage"); rec_ids.append(pref)
            elif l in DISP_STAGES:
                reg_all.append(r); aasm_all.append("disp_stage"); rec_ids.append(pref)
        used += 1
        print(f"  {pref}: {len(covs)} windows")

    reg_all = np.array(reg_all); aasm_all = np.array(aasm_all); rec_ids = np.array(rec_ids)
    n_lab = len(reg_all)

    # self-test
    ok = n_lab >= 100 and len(set(aasm_all)) >= 2 and len(set(reg_all)) >= 2
    print(f"\nSelf-test: {n_lab} labelled windows, "
          f"{len(set(aasm_all))} AASM classes, {len(set(reg_all))} regimes -> "
          f"[{'PASS' if ok else 'FAIL'}]")
    if not ok:
        raise SystemExit("SELF-TEST FAILED -- insufficient labelled windows/variety; aborted.")

    obs_v = cramers_v(reg_all, aasm_all)
    # permutation null: shuffle AASM labels within each record
    null = np.empty(N_PERM)
    for k in range(N_PERM):
        perm = aasm_all.copy()
        for rid in set(rec_ids):
            m = rec_ids == rid
            perm[m] = rng.permutation(perm[m])
        null[k] = cramers_v(reg_all, perm)
    p95 = float(np.percentile(null, 95))
    pval = float((np.sum(null >= obs_v) + 1) / (N_PERM + 1))

    # direction: is drift-regime enriched for drift_stage (N2/N3)?
    drift_mask = reg_all == "drift"
    frac_driftstage_in_drift = float(np.mean(aasm_all[drift_mask] == "drift_stage")) if drift_mask.any() else 0.0
    frac_driftstage_overall = float(np.mean(aasm_all == "drift_stage"))
    direction_ok = frac_driftstage_in_drift > frac_driftstage_overall

    repaired = (obs_v > p95) and direction_ok

    if repaired:
        verdict = (
            f"PARTIAL REPAIR -- the demarcation binds to AASM for 2 of 3 regimes. The protocol's "
            f"drift-vs-dispersion regime is associated with AASM stage structure beyond chance "
            f"(Cramér's V = {obs_v:.3f} vs null 95th pct {p95:.3f}, p = {pval:.4f}), in the "
            f"mapped direction (drift regime enriched for N2/N3: {frac_driftstage_in_drift:.2f} "
            f"vs {frac_driftstage_overall:.2f} overall). So an external, human-scored referent "
            f"exists for at least the drift/dispersion contrast, and the Phase-0 'not externally "
            f"falsifiable' verdict is superseded for the sleep paradigm -- with the pre-registered "
            f"ceiling that collapse has no AASM counterpart, so at most 2 of 3 regimes bind.")
    else:
        verdict = (
            f"THE GATE WAS DEEP, NOT SURFACE -- the tri-partition does not recut what AASM scores. "
            f"The protocol's drift-vs-dispersion regime shows association Cramér's V = {obs_v:.3f} "
            f"against a permutation-null 95th percentile of {p95:.3f} (p = {pval:.4f}), "
            f"{'in' if direction_ok else 'not even in'} the mapped direction. On the pre-registered "
            f"mapping the demarcation does not align with human AASM staging beyond chance, so "
            f"binding it to this external referent does not repair falsifiability: the regimes "
            f"remain defined by the protocol's own criteria, exactly as the Phase-0 gate found. "
            f"Reported as prominently as a repair would have been.")

    summary = {
        "experiment": "regime_external_referent",
        "question": ("does a pre-registered mapping from the protocol's dynamical regimes to AASM "
                     "sleep stages bind above chance, repairing the falsifiability gate?"),
        "n_labelled_windows": n_lab, "n_records": used,
        "cramers_v_observed": obs_v, "null_p95": p95, "p_value": pval,
        "direction_ok": bool(direction_ok),
        "frac_N2N3_in_drift_regime": frac_driftstage_in_drift,
        "frac_N2N3_overall": frac_driftstage_overall,
        "preregistered_criterion": "V > null 95th pct AND mapped direction => partial repair (2/3 regimes); collapse has no AASM counterpart by design",
        "repaired": bool(repaired),
        "verdict": verdict,
        "figures": ["regime_external_referent.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(null, bins=40, color="gray", alpha=0.7, label="permutation null")
    ax.axvline(obs_v, color="crimson", lw=2, label=f"observed V={obs_v:.3f}")
    ax.axvline(p95, color="green", ls="--", label=f"null 95th pct={p95:.3f}")
    ax.set_xlabel("Cramér's V (regime vs AASM-mapped label)"); ax.set_ylabel("count")
    ax.set_title(f"H2: demarcation vs AASM staging (p={pval:.3f})"); ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "regime_external_referent.png"), dpi=130)
    plt.close(fig)
    print("\n" + "=" * 72); print(verdict)
    print(f"\nResults in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
