"""A permanence-aware on-line localizer -- one attempt at the >=10/15 band (Paper 3).

`online_localization_cusum` reached 8/15 on real eyes-open/closed EEG with global
F-ratio and CUSUM detectors, short of its pre-registered SOLVED band of >=10/15,
because spontaneous alpha bursts are sustained-and-recurrent and neither detector
requires the post-transition segment to STAY changed.

This tests one new detector that encodes permanence directly: score each split by
whether its post-segment resembles the state the record actually ENDS in. A burst
returns toward the pre-state (away from the terminal) and is penalised; a permanent
transition's post-segment matches the terminal and is not. Same data, loader,
embedding, sphere, min-segment and tolerance as the sister experiment; only the
statistic is new, and its one parameter (terminal window = last quarter) is fixed in
the pre-registration, not swept.

Usage:
    python -m experiments.paper3_geodesic_kinematics.online_localization_permanence.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, break_curve, _win_mean_emb, _sphere_dist_emb, _R,
)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs,
    N_SUBJECTS, SEG_SEC, STEP_SEC, LARGE_W, TOL_SEC,
)
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    changepoint_fratio, cusum_changepoint, _hit, MIN_SEG_SEC,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "online_localization_permanence")

TERM_FRAC = 0.25         # terminal window = final quarter of the record (pre-registered)


def permanence_changepoint(E, C, min_seg, term_frac=TERM_FRAC):
    """Between-mean distance weighted by how well the post-segment matches the state
    the record ends in. score(tau) = d(pre,post) * max(0, 1 - d(post,term)/d(pre,term)).
    """
    n = C.shape[0] - 1
    term_k = max(min_seg, int(term_frac * n))
    m_term = _win_mean_emb(C, n - term_k, n)
    curve = np.full(n, np.nan)
    for tau in range(min_seg, n - min_seg):
        m_pre = _win_mean_emb(C, 0, tau)
        m_post = _win_mean_emb(C, tau, n)
        between = _sphere_dist_emb(m_pre, m_post)
        d_post_term = _sphere_dist_emb(m_post, m_term)
        d_pre_term = _sphere_dist_emb(m_pre, m_term)
        permanence = max(0.0, 1.0 - d_post_term / (d_pre_term + 1e-9))
        size = tau * (n - tau) / n     # standard change-point size weighting
        curve[tau] = size * between * permanence
    return curve


def analyse(subject):
    data_o, sf = load_state_covs(subject, 1)
    data_c, _ = load_state_covs(subject, 2)
    n = int(SEG_SEC * sf)
    data = np.concatenate([data_o[:, :n], data_c[:, :n]], axis=1)
    covs = sliding_covs(data, sf)
    seam = int(SEG_SEC / STEP_SEC)
    tol = int(TOL_SEC / STEP_SEC)
    min_seg = int(MIN_SEG_SEC / STEP_SEC)
    E, C = embed_cumsum(covs)

    win = break_curve(C, LARGE_W)
    fr = changepoint_fratio(E, C, min_seg)
    cu = cusum_changepoint(E, C, min_seg)
    pm = permanence_changepoint(E, C, min_seg)

    out = {"subject": subject, "seam": seam, "n_windows": len(covs)}
    for key, curve in (("window_mean", win), ("fratio", fr), ("cusum", cu),
                       ("permanence", pm)):
        t, e, h, p = _hit(curve, seam, tol)
        out[key] = {"cp": int(t), "err": int(e), "hit": bool(h), "prom": float(p)}
    return out


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Permanence-aware on-line localization (eegmmidb eyes-open/closed)\n")
    rows = []
    for s in range(1, N_SUBJECTS + 1):
        try:
            rows.append(analyse(s))
        except Exception as exc:            # a subject that fails to load is skipped, recorded
            print(f"  S{s:03d} skipped: {exc!r}")
    n = len(rows)

    def hits(k):
        return int(sum(r[k]["hit"] for r in rows))
    win_h, fr_h, cu_h, pm_h = (hits("window_mean"), hits("fratio"),
                               hits("cusum"), hits("permanence"))
    for r in rows:
        print(f"  S{r['subject']:03d} seam={r['seam']:4d} | "
              f"win {r['window_mean']['err']:3d}{'*' if r['window_mean']['hit'] else ' '} | "
              f"F {r['fratio']['err']:3d}{'*' if r['fratio']['hit'] else ' '} | "
              f"CUSUM {r['cusum']['err']:3d}{'*' if r['cusum']['hit'] else ' '} | "
              f"PERM {r['permanence']['err']:3d}{'*' if r['permanence']['hit'] else ' '}")
    print(f"\n  hits/{n}: window_mean {win_h}, F-ratio {fr_h}, CUSUM {cu_h}, "
          f"PERMANENCE {pm_h}")

    baseline_best = max(win_h, fr_h, cu_h)
    # reproduction check: the sister experiment recorded a best global detector of 8/15
    reproduced = abs(baseline_best - 8) <= 1 or abs(max(fr_h, cu_h) - 8) <= 1
    solved = pm_h >= 10

    if not reproduced:
        outcome = "VOID"
        verdict = (f"VOID: the baselines did not reproduce (best global detector "
                   f"{max(fr_h, cu_h)}/{n} vs the 8/15 on record), so data or loader "
                   f"has drifted and nothing is concluded about the new detector "
                   f"(which scored {pm_h}/{n}).")
    elif solved:
        outcome = "MOVES_THE_BOUND"
        verdict = (f"THE BOUND MOVES: the permanence-aware detector localizes "
                   f"{pm_h}/{n}, reaching the pre-registered SOLVED band (>=10/15) that "
                   f"the F-ratio and CUSUM ({max(fr_h, cu_h)}/{n}) did not. Encoding "
                   f"permanence directly -- scoring a split by whether its post-segment "
                   f"matches the state the record ends in, so a sustained-but-recurrent "
                   f"burst is penalised while a permanent transition is not -- is what "
                   f"the global scatter and tent statistics were missing. Paper 3's "
                   f"on-line localization moves from 'materially better, not solved' to "
                   f"solved on real EEG by this detector. No parameter was tuned: the "
                   f"terminal window was fixed at the final quarter in the "
                   f"pre-registration.")
    else:
        outcome = "BOUND_HOLDS"
        verdict = (f"THE BOUND HOLDS: the permanence-aware detector localizes only "
                   f"{pm_h}/{n}, short of the >=10/15 SOLVED band (baselines "
                   f"{max(fr_h, cu_h)}/{n}, reproduced). Making permanence explicit was "
                   f"a reasonable idea and it is reported as tried-and-insufficient "
                   f"rather than re-parameterised: the on-line localization of a "
                   f"transition that is not the dominant geometric event in its record "
                   f"remains open, and Paper 3's 'materially better, not solved' stands. "
                   f"One attempt, terminal window fixed in advance at the final quarter.")

    fig, ax = plt.subplots(figsize=(8, 5))
    names = ["window_mean", "fratio", "cusum", "permanence"]
    vals = [win_h, fr_h, cu_h, pm_h]
    colors = ["#999", "#b8863b", "#3b6ea8", "#7a2e2e"]
    ax.bar(names, vals, color=colors)
    ax.axhline(10, ls="--", color="green", label="SOLVED band (10/15)")
    ax.axhline(8, ls=":", color="gray", label="prior best (8/15)")
    ax.set_ylabel(f"hits / {n}"); ax.set_ylim(0, N_SUBJECTS)
    ax.set_title("On-line localization on real EEG: permanence vs prior detectors")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "online_localization_permanence.png"), dpi=130)
    plt.close(fig)

    json.dump({
        "experiment": "online_localization_permanence",
        "question": "Does a permanence-aware detector reach the >=10/15 on-line "
                    "localization band that F-ratio/CUSUM (8/15) did not?",
        "data": "eegmmidb eyes-open (R01) vs eyes-closed (R02), occipito-parietal alpha",
        "n_subjects": n, "terminal_fraction": TERM_FRAC,
        "hits": {"window_mean": win_h, "fratio": fr_h, "cusum": cu_h,
                 "permanence": pm_h},
        "solved_band": 10, "baselines_reproduced": bool(reproduced),
        "per_subject": rows, "outcome": outcome, "verdict": verdict,
        "figures": ["online_localization_permanence.png"],
    }, open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
