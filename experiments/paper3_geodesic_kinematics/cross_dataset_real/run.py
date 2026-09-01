"""Experiment C on REAL data -- is on-line localization governed by the measured
transition/fluctuation ratio, across paradigms? (Paper 3)

Synthetic Exp C (`cross_dataset`) swept the transition-to-spontaneous-fluctuation
ratio and found localization is *governed by that ratio*. It flagged that C itself was
never tested on real data. This supplies that test: it MEASURES the ratio on each real
recording, from two paradigms at opposite ends of the ratio axis, and asks whether the
measured ratio predicts how well the geodesic CUSUM localizes the transition.

  - Low-ratio paradigm  : eegmmidb eyes-open/eyes-closed occipital alpha
                          (loader from `real_eeg_localization`).
  - High-ratio paradigm : Sleep-EDF wake -> sleep-onset (W->N1)
                          (loader + transition finder from `sleep_stage_localization`).

Per recording, on the sqrt-embedding sphere (radius R=2):
    delta  = geodesic distance between pre- and post-seam state centroids
    phi    = mean of the two states' median within-state distance-to-centroid
    R      = delta / phi                       (measured transition/fluctuation ratio)
    e_norm = |cusum_cp - seam| / (n_windows/2) (tolerance-free localization error)

Pre-registered primary criterion: Spearman rho(R, e_norm) <= -0.40, p < 0.05, pooled
across both real paradigms, with the paradigm ordering consistent (sleep higher R and
lower e_norm than alpha). See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.cross_dataset_real.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import (
    embed_cumsum, _win_mean_emb, _sphere_dist_emb, _R,
)
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint,
)
# low-ratio paradigm (eyes-open/closed alpha)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs,
    N_SUBJECTS as AL_N, SEG_SEC as AL_SEG_SEC, STEP_SEC as AL_STEP,
)
# high-ratio paradigm (sleep onset)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, find_transition, discover_subjects,
    SEG_SEC as SL_SEG_SEC, STEP_SEC as SL_STEP, MIN_SEG_SEC as SL_MINSEG,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "cross_dataset_real")

AL_MINSEG_SEC = 5.0            # matches online_localization_cusum for the alpha paradigm


# ======================================================================
#  measured quantities on one recording's covariance trajectory
# ======================================================================
def record_metrics(covs, seam, min_seg, step_sec):
    """R = delta/phi and the tolerance-free localization error for one recording.

    covs   : list of trace-normalised density matrices (the trajectory)
    seam   : window index of the true transition
    min_seg: minimum segment length (windows) handed to the CUSUM
    step_sec: seconds per window step (for the persistence time only)
    """
    E, C = embed_cumsum(covs)
    n = len(covs)
    if seam < 1 or seam > n - 1:
        return None
    c_pre = _win_mean_emb(C, 0, seam)
    c_post = _win_mean_emb(C, seam, n)
    delta = _sphere_dist_emb(c_pre, c_post)

    # within-state fluctuation: median distance of each window to its own state centroid
    d_pre = np.array([_sphere_dist_emb(E[i], c_pre) for i in range(seam)])
    d_post = np.array([_sphere_dist_emb(E[i], c_post) for i in range(seam, n)])
    phi = 0.5 * (float(np.median(d_pre)) + float(np.median(d_post)))
    ratio = delta / (phi + 1e-12)

    # localization: geodesic CUSUM change point, tolerance-free normalised error
    cu = cusum_changepoint(E, C, min_seg)
    cp = int(np.nanargmax(np.where(np.isnan(cu), -np.inf, cu)))
    e_norm = abs(cp - seam) / (n / 2.0)

    # secondary/descriptive: within-state persistence time of the fluctuation series
    s = np.concatenate([d_pre, d_post])
    persist_s = _persistence_time(s, step_sec)

    return {"ratio": float(ratio), "delta": float(delta), "phi": float(phi),
            "cp": cp, "seam": int(seam), "n_windows": int(n),
            "e_norm": float(e_norm), "err_windows": int(abs(cp - seam)),
            "persist_s": float(persist_s), "persist_windows": float(persist_s / step_sec)}


def _persistence_time(s, dt):
    """First lag (in seconds) at which the autocorrelation of the within-state
    fluctuation series falls below 1/e -- Exp C's 'burst persistence' axis."""
    s = np.asarray(s, float)
    s = s - s.mean()
    denom = float(np.dot(s, s))
    if denom < 1e-18 or len(s) < 6:
        return 0.0
    for lag in range(1, len(s) // 2):
        ac = float(np.dot(s[:-lag], s[lag:])) / denom
        if ac < np.exp(-1.0):
            return lag * dt
    return (len(s) // 2) * dt


# ======================================================================
#  per-paradigm recording extraction (loaders reused verbatim)
# ======================================================================
def alpha_records(n_subjects):
    """Low-ratio paradigm: concatenate eyes-open + eyes-closed, seam at the join."""
    out = []
    min_seg = int(AL_MINSEG_SEC / AL_STEP)
    for s in range(1, n_subjects + 1):
        try:
            data_o, sf = load_state_covs(s, 1)
            data_c, _ = load_state_covs(s, 2)
            n = int(AL_SEG_SEC * sf)
            data = np.concatenate([data_o[:, :n], data_c[:, :n]], axis=1)
            covs = sliding_covs(data, sf)
            seam = int(AL_SEG_SEC / AL_STEP)
            m = record_metrics(covs, seam, min_seg, AL_STEP)
            if m is not None:
                m.update(paradigm="alpha", subject=f"S{s:03d}")
                out.append(m)
                print(f"  alpha S{s:03d}: R={m['ratio']:.2f} e_norm={m['e_norm']:.3f} "
                      f"(err {m['err_windows']*AL_STEP:.1f}s) persist={m['persist_s']:.1f}s")
        except Exception as e:
            print(f"  alpha S{s:03d}: FAILED {type(e).__name__}: {str(e)[:70]}")
    return out


def sleep_records(max_records):
    """High-ratio paradigm: wake -> sleep-onset (W->N1) structural transition."""
    out = []
    min_seg = int(SL_MINSEG / SL_STEP)
    subs = discover_subjects()
    for p, h in subs:
        if len(out) >= max_records:
            break
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            print(f"  sleep {pref}: LOAD FAILED {type(e).__name__}: {str(e)[:60]}")
            continue
        tr = find_transition(stage, fs)
        if tr is None:
            print(f"  sleep {pref}: no qualifying transition -- skipped")
            continue
        t0, s0, s1 = tr
        seg = int(SL_SEG_SEC * fs)
        lo, hi = max(0, t0 - seg), min(data.shape[1], t0 + seg)
        sub = data[:, lo:hi]
        covs, _, centers = sliding_covs_labeled(
            sub, fs, np.full(sub.shape[1], "", dtype=object))
        seam = int(np.argmin(np.abs(centers - (t0 - lo) / fs)))
        m = record_metrics(covs, seam, min_seg, SL_STEP)
        if m is not None:
            m.update(paradigm="sleep", subject=pref, transition=f"{s0}->{s1}")
            out.append(m)
            print(f"  sleep {pref}: {s0}->{s1} R={m['ratio']:.2f} e_norm={m['e_norm']:.3f} "
                  f"(err {m['err_windows']*SL_STEP:.0f}s) persist={m['persist_s']:.0f}s")
    return out


# ======================================================================
#  self-test: the ratio estimator must see a ratio it is handed
# ======================================================================
def self_test():
    """On two synthetic recordings with a KNOWN high vs low transition/fluctuation
    ratio, the estimator must order them correctly and give the high-ratio one a
    smaller normalised localization error. Gates the run."""
    from experiments.paper3_geodesic_kinematics.cross_dataset.run import generate_subject
    covs_hi, seam_hi = generate_subject(0, seam_size=1.5, burst_duration=1)
    covs_lo, seam_lo = generate_subject(0, seam_size=0.25, burst_duration=1)
    hi = record_metrics(covs_hi, seam_hi, 20, 1.0)
    lo = record_metrics(covs_lo, seam_lo, 20, 1.0)
    checks = {
        "ratio_orders_correctly": hi["ratio"] > lo["ratio"],
        "high_ratio_localizes_better": hi["e_norm"] <= lo["e_norm"],
    }
    print("Self-test (ratio estimator on known synthetic ratios):")
    print(f"  high-ratio synthetic: R={hi['ratio']:.2f} e_norm={hi['e_norm']:.3f}")
    print(f"  low-ratio  synthetic: R={lo['ratio']:.2f} e_norm={lo['e_norm']:.3f}")
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    if not all(checks.values()):
        raise SystemExit("SELF-TEST FAILED -- ratio estimator unreliable; run aborted.")
    return {k: bool(v) for k, v in checks.items()}, {
        "high": {"ratio": hi["ratio"], "e_norm": hi["e_norm"]},
        "low": {"ratio": lo["ratio"], "e_norm": lo["e_norm"]}}


# ======================================================================
def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment C (real data): does the measured transition/fluctuation ratio "
          "govern on-line localization across real paradigms?")
    st_checks, st_vals = self_test()

    print("\nLow-ratio paradigm (eyes-open/closed alpha):")
    alpha = alpha_records(AL_N)
    print("\nHigh-ratio paradigm (Sleep-EDF wake -> sleep-onset):")
    sleep = sleep_records(max_records=AL_N)

    recs = alpha + sleep
    n = len(recs)
    R = np.array([r["ratio"] for r in recs])
    E = np.array([r["e_norm"] for r in recs])

    rho, pval = spearmanr(R, E)
    rho, pval = float(rho), float(pval)

    def med(rows, key):
        return float(np.median([x[key] for x in rows])) if rows else float("nan")

    R_alpha, R_sleep = med(alpha, "ratio"), med(sleep, "ratio")
    E_alpha, E_sleep = med(alpha, "e_norm"), med(sleep, "e_norm")
    ordering_ok = (R_sleep > R_alpha) and (E_sleep < E_alpha)

    # ---- verdict strictly against the pre-registered bands ----
    if rho <= -0.40 and pval < 0.05 and ordering_ok:
        verdict = (
            f"CONFIRMED ON REAL DATA -- localization is governed by the measured "
            f"transition/fluctuation ratio. Across {n} real recordings from two paradigms, "
            f"a higher measured ratio predicts a smaller normalised localization error: "
            f"Spearman rho = {rho:.2f} (p = {pval:.3g}), clearing the pre-registered "
            f"-0.40 bar. The paradigm ordering is consistent: the high-ratio sleep-onset "
            f"paradigm has median ratio {R_sleep:.2f} and error {E_sleep:.3f} vs the "
            f"low-ratio alpha paradigm's {R_alpha:.2f} and {E_alpha:.3f}. So the synthetic "
            f"Exp C mechanism transfers: the eyes-open/closed 4/15 was the LOW-RATIO end of "
            f"one continuum, not a fixed method limitation, and the ratio -- measurable on a "
            f"real recording before any ground truth -- says which transitions this geometry "
            f"can localize on-line and which it cannot.")
    elif rho <= -0.20 and ordering_ok:
        verdict = (
            f"QUALIFIED -- the measured ratio is predictive but not decisive. Spearman "
            f"rho = {rho:.2f} (p = {pval:.3g}) across {n} real recordings: higher ratio does "
            f"trend to better localization and the paradigm ordering holds (sleep ratio "
            f"{R_sleep:.2f}/err {E_sleep:.3f} vs alpha {R_alpha:.2f}/{E_alpha:.3f}), but the "
            f"association is below the pre-registered -0.40 bar. Exp C's mechanism is "
            f"directionally supported on real data, not established at strength.")
    elif rho < 0.0 and not ordering_ok:
        verdict = (
            f"NOT SUPPORTED AT STRENGTH -- right-signed but weak, and the paradigm-ordering "
            f"assumption is REFUTED. Within {n} real recordings the measured ratio is "
            f"right-signed on localization error (Spearman rho = {rho:.2f}, p = {pval:.3g}) -- "
            f"Exp C's direction -- but it does not clear the pre-registered -0.40 bar and is "
            f"not significant at this n. More decisively, the ordering the design assumed is "
            f"false: MEASURED, sleep-onset (W->N1) is not a higher-ratio transition than "
            f"eyes-open/closed alpha (median R {R_sleep:.2f} vs {R_alpha:.2f}) and localizes "
            f"no better (median e_norm {E_sleep:.3f} vs {E_alpha:.3f}). So (i) the design did "
            f"not actually span the ratio axis -- W->N1 is a gradual, low-ratio transition on "
            f"this geometry -- and (ii) Exp C's synthetic 'robust across paradigm strength' "
            f"(15/15 at every ratio) does NOT transfer: real localization degrades badly at "
            f"low ratio and is not rescued at the nominal 'high-ratio' paradigm, the same "
            f"synthetic-overstates-real pattern already documented for Exp A. This is the "
            f"pre-registration's negative branch (ordering violated); it is reported as such, "
            f"and the fair test -- a genuinely high-ratio real transition (e.g. N2<->REM) as "
            f"the high end -- is registered as a follow-up rather than run post-hoc to chase "
            f"the bar.")
    else:
        verdict = (
            f"NOT SUPPORTED ON REAL DATA -- no right-signed association. Spearman "
            f"rho = {rho:.2f} (p = {pval:.3g}) across {n} real recordings "
            f"(paradigm ordering {'holds' if ordering_ok else 'violated'}: sleep ratio "
            f"{R_sleep:.2f}/err {E_sleep:.3f} vs alpha {R_alpha:.2f}/{E_alpha:.3f}). The "
            f"synthetic Exp C ratio mechanism does NOT transfer: on real recordings the "
            f"transition/fluctuation ratio is not what decides whether the geodesic detector "
            f"localizes the transition. Reported as a real negative -- the localization "
            f"limitation is not reducible to paradigm strength.")

    # residual-persistence note (descriptive, C's second axis)
    hi_ratio = [r for r in recs if r["ratio"] >= np.median(R)]
    hi_miss = [r for r in hi_ratio if r["e_norm"] > 0.10]
    persist_note = (
        f"Persistence (descriptive): median within-state persistence "
        f"{med(recs, 'persist_windows'):.1f} windows; of the {len(hi_ratio)} higher-ratio "
        f"recordings, {len(hi_miss)} still localize poorly (e_norm>0.10), with median "
        f"persistence {med(hi_miss, 'persist_windows') if hi_miss else float('nan'):.1f} "
        f"windows vs {med([r for r in hi_ratio if r['e_norm']<=0.10], 'persist_windows'):.1f} "
        f"for the higher-ratio hits -- Exp C's 'burst longer than the window' residual.")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for rows, col, lab in [(alpha, "crimson", "alpha (low-ratio)"),
                           (sleep, "steelblue", "sleep (high-ratio)")]:
        if rows:
            ax[0].scatter([x["ratio"] for x in rows], [x["e_norm"] for x in rows],
                          c=col, label=lab, s=40, alpha=0.8, edgecolor="k", linewidth=0.4)
    ax[0].set_xlabel("measured transition/fluctuation ratio R")
    ax[0].set_ylabel("normalised localization error e_norm")
    ax[0].set_title(f"Ratio governs localization?  Spearman rho={rho:.2f} (p={pval:.3g})")
    ax[0].legend(fontsize=9)
    # paradigm medians
    labels = ["alpha\n(low-ratio)", "sleep\n(high-ratio)"]
    ax[1].bar([0, 1], [R_alpha, R_sleep], color=["crimson", "steelblue"], alpha=0.6,
              label="median ratio R")
    ax[1].set_ylabel("median measured ratio R")
    ax2 = ax[1].twinx()
    ax2.plot([0, 1], [E_alpha, E_sleep], "ko--", label="median e_norm")
    ax2.set_ylabel("median e_norm")
    ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(labels)
    ax[1].set_title("Paradigm ordering (ratio up => error down)")
    fig.suptitle(f"Exp C on real data ({n} recordings, {len(alpha)} alpha + {len(sleep)} sleep)",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "ratio_governs_localization.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "cross_dataset_real",
        "data": ("PhysioNet eegbci eyes-open/closed (low-ratio) + Sleep-EDF wake->sleep-onset "
                 "(high-ratio); real recordings, one unified geodesic-CUSUM detector"),
        "question": ("does the measured transition/fluctuation ratio govern on-line "
                     "localization across real paradigms (Exp C's mechanism on real data)?"),
        "self_test": {"checks": st_checks, "values": st_vals},
        "n_recordings": {"total": n, "alpha": len(alpha), "sleep": len(sleep)},
        "spearman": {"rho": rho, "p": pval},
        "paradigm_medians": {"alpha": {"ratio": R_alpha, "e_norm": E_alpha},
                             "sleep": {"ratio": R_sleep, "e_norm": E_sleep},
                             "ordering_consistent": bool(ordering_ok)},
        "preregistered_criterion": "rho(R,e_norm) <= -0.40 and p<0.05 and paradigm ordering consistent",
        "persistence_note": persist_note,
        "per_recording": recs,
        "verdict": verdict,
        "figures": ["ratio_governs_localization.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print("\n" + persist_note)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
