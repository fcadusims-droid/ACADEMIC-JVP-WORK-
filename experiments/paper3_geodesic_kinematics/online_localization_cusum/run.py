"""Global permanence-aware on-line localization on REAL EEG (Paper 3 headline claim).

The window-mean persistence detector solved the synthetic localization
(2/15 -> 15/15) but stalls on real EEG (large window 4/15), because spontaneous
alpha bursts are *sustained* and a local window-mean cannot tell
"sustained-and-recurrent" (a burst that passes, pre-state returns) from
"sustained-and-permanent" (the true transition). This tests two GLOBAL,
permanence-aware change-point detectors that see the whole trajectory -- the tool
the local window-mean lacks -- directly on the same 15 real subjects, with no
synthetic tuning.

  (1) Geodesic change-point F-ratio (duration-penalized LR):
        F(tau) = d(mean_pre, mean_post) / (scatter_pre + scatter_post)
      A permanent shift maximizes between-mean distance at low within-scatter; a
      burst inflates the scatter of the segment holding the burst-and-return.
  (2) Geodesic CUSUM: classical argmax_t |S_t| of the tangent deviation projected
      onto the first->last change direction; a permanent step's tent scales with
      the remaining record length, a transient burst's bump with its short duration.

Baseline: the window-mean large-window break-curve, re-run head-to-head.

Usage:
    python -m experiments.paper3_geodesic_kinematics.online_localization_cusum.run
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
    N_SUBJECTS, CHANNELS, ALPHA_BAND, SEG_SEC, STEP_SEC, LARGE_W, TOL_SEC,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "online_localization_cusum"
)

MIN_SEG_SEC = 5.0        # minimum-duration penalty: each regime >= 5 s


def _seg_dists(E_flat, m_emb):
    """Geodesic distances (on the radius-2 sphere) of every embedded window to a
    segment mean embedding m (norm _R), vectorised."""
    cos = np.clip(E_flat @ m_emb.reshape(-1) / (_R * _R), -1.0, 1.0)
    return 2.0 * np.arccos(cos)


def changepoint_fratio(E, C, min_seg):
    """Global single-change-point likelihood-ratio with a minimum segment length,
    in the textbook size-weighted form. The (n_pre*n_post/N) factor is the standard
    change-point weighting: it is zero at the record ends and maximal at the centre,
    which removes the boundary spike a raw between/within ratio suffers (a tiny end
    segment has spuriously low scatter). Returns F(tau) over valid tau (NaN outside)."""
    n = C.shape[0] - 1
    E_flat = E.reshape(n, -1)
    F = np.full(n, np.nan)
    for tau in range(min_seg, n - min_seg):
        m_pre = _win_mean_emb(C, 0, tau)
        m_post = _win_mean_emb(C, tau, n)
        between = _sphere_dist_emb(m_pre, m_post)
        scat_pre = float(np.mean(_seg_dists(E_flat[:tau], m_pre)))
        scat_post = float(np.mean(_seg_dists(E_flat[tau:], m_post)))
        pooled = (tau * scat_pre + (n - tau) * scat_post) / n
        size = tau * (n - tau) / n          # 0 at the ends, max at the centre
        F[tau] = size * between * between / (pooled + 1e-9)
    return F


def cusum_changepoint(E, C, min_seg):
    """Geodesic CUSUM: project each window's deviation from the global Fréchet mean
    onto the first-quarter -> last-quarter change direction and take the classical
    cumulative-sum change-point curve |S_t|."""
    n = C.shape[0] - 1
    E_flat = E.reshape(n, -1)
    m0 = _win_mean_emb(C, 0, n).reshape(-1)
    q = max(min_seg, n // 4)
    u = (_win_mean_emb(C, n - q, n) - _win_mean_emb(C, 0, q)).reshape(-1)
    un = np.linalg.norm(u)
    u = u / un if un > 1e-12 else u
    s = (E_flat - m0) @ u
    s = s - s.mean()
    S = np.cumsum(s)
    curve = np.full(n, np.nan)
    curve[min_seg:n - min_seg] = np.abs(S[min_seg:n - min_seg])
    return curve


def _hit(curve, seam, tol):
    v = np.where(np.isnan(curve), -np.inf, curve)
    t = int(np.argmax(v))
    finite = curve[np.isfinite(curve)]
    prom = float(np.max(finite) / (np.median(finite) + 1e-12)) if finite.size else 0.0
    return t, abs(t - seam), (abs(t - seam) <= tol), prom


def analyse_subject(subject):
    data_o, sf = load_state_covs(subject, 1)
    data_c, _ = load_state_covs(subject, 2)
    n = int(SEG_SEC * sf)
    data = np.concatenate([data_o[:, :n], data_c[:, :n]], axis=1)
    covs = sliding_covs(data, sf)
    seam = int(SEG_SEC / STEP_SEC)
    tol = int(TOL_SEC / STEP_SEC)
    min_seg = int(MIN_SEG_SEC / STEP_SEC)
    E, C = embed_cumsum(covs)

    # baseline: window-mean large window
    win = break_curve(C, LARGE_W)
    fr = changepoint_fratio(E, C, min_seg)
    cu = cusum_changepoint(E, C, min_seg)

    tw, ew, hw, pw = _hit(win, seam, tol)
    tf, ef, hf, pf = _hit(fr, seam, tol)
    tc, ec, hc, pc = _hit(cu, seam, tol)
    return {"subject": subject, "seam": seam, "n_windows": len(covs),
            "window_mean": {"cp": tw, "err": ew, "hit": hw, "prom": pw},
            "fratio":      {"cp": tf, "err": ef, "hit": hf, "prom": pf},
            "cusum":       {"cp": tc, "err": ec, "hit": hc, "prom": pc}}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tol = int(TOL_SEC / STEP_SEC)
    print("Global permanence-aware on-line localization on REAL EEG")
    print(f"  {N_SUBJECTS} subjects, channels {CHANNELS}, alpha {ALPHA_BAND} Hz, "
          f"seg {SEG_SEC}s, tol +/-{TOL_SEC}s ({tol} windows), min-seg {MIN_SEG_SEC}s")
    print(f"  {'subj':>5} {'seam':>5} | {'winmean':>18} | {'fratio':>18} | {'cusum':>18}")

    rows = []
    for s in range(1, N_SUBJECTS + 1):
        try:
            r = analyse_subject(s)
            rows.append(r)
            def fmt(d):
                return f"cp{d['cp']:3d} e{d['err']*STEP_SEC:4.1f}s {'HIT' if d['hit'] else '   '}"
            print(f"  S{s:03d} {r['seam']:5d} | {fmt(r['window_mean'])} | "
                  f"{fmt(r['fratio'])} | {fmt(r['cusum'])}")
        except Exception as e:
            print(f"  S{s:03d}: FAILED {type(e).__name__}: {str(e)[:80]}")

    n = len(rows)
    def hits(key):  return int(sum(r[key]["hit"] for r in rows))
    def med_err(key): return float(np.median([r[key]["err"] for r in rows]) * STEP_SEC)
    def med_prom(key): return float(np.median([r[key]["prom"] for r in rows]))

    win_h, fr_h, cu_h = hits("window_mean"), hits("fratio"), hits("cusum")
    best_h = max(fr_h, cu_h)
    best_name = "fratio" if fr_h >= cu_h else "cusum"

    # ---- verdict against pre-registered bands ----
    if best_h >= 10:
        verdict = (
            f"SOLVED on real EEG. The global {best_name} detector localizes the "
            f"transition in {best_h}/{n} subjects (median err {med_err(best_name):.1f}s) "
            f"-- vs the local window-mean's {win_h}/{n}. Seeing the whole trajectory "
            f"and penalizing non-permanent regimes (the transient-vs-permanent "
            f"distinction the window-mean lacked) turns Paper 3's headline on-line "
            f"localization claim from OPEN to SUPPORTED on real EEG. (F-ratio "
            f"{fr_h}/{n}, CUSUM {cu_h}/{n}.)")
    elif best_h >= 8:
        verdict = (
            f"MATERIALLY BETTER, not solved. The global {best_name} reaches "
            f"{best_h}/{n} (median err {med_err(best_name):.1f}s) vs the window-mean's "
            f"{win_h}/{n} -- a real, substantial improvement from a permanence-aware "
            f"global view, but short of a full solution. Honest status: on-line "
            f"localization on real EEG is IMPROVED but still imperfect. (F-ratio "
            f"{fr_h}/{n}, CUSUM {cu_h}/{n}.)")
    elif best_h >= 6:
        verdict = (
            f"MARGINAL -- and the budget is spent. The best global detector "
            f"({best_name}) reaches {best_h}/{n} (median err {med_err(best_name):.1f}s), "
            f"better than the window-mean's {win_h}/{n} but inside the zone the "
            f"review flagged. Per the pre-registered rule, the honest conclusion is "
            f"now the METHOD LIMITATION reading: the trace-normalised geometry "
            f"DISCRIMINATES a structural regime (validated in eeg_reconciliation) but "
            f"does NOT reliably localize the transition on-line within a single "
            f"trajectory of this signal type. That is a genuine, publishable bound on "
            f"Paper 3's operational claim, not a bug to chase further. (F-ratio "
            f"{fr_h}/{n}, CUSUM {cu_h}/{n}.)")
    else:
        verdict = (
            f"REAL METHOD LIMITATION (not a bug). Even the global, permanence-aware "
            f"detectors do not beat the local window-mean: F-ratio {fr_h}/{n}, CUSUM "
            f"{cu_h}/{n}, window-mean {win_h}/{n}. The right tool for the "
            f"transient-vs-permanent distinction does not rescue on-line "
            f"localization on this signal. Honest, publishable conclusion: the "
            f"trace-normalised geometry discriminates a structural regime "
            f"(validated) but CANNOT localize the transition on-line within a single "
            f"trajectory of real eyes-open/eyes-closed EEG -- a genuine limitation "
            f"bounding Paper 3's headline claim, not a detector still to be found. "
            f"The synthetic 15/15 was solving the model of the problem, not the "
            f"problem: real spontaneous alpha is both sustained AND geometrically "
            f"larger than the transition, defeating permanence too.")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    labels = ["window-mean\n(local)", "F-ratio\n(global LR)", "CUSUM\n(global)"]
    vals = [win_h / n, fr_h / n, cu_h / n]
    ax[0].bar([0, 1, 2], vals, color=["gray", "crimson", "steelblue"])
    ax[0].axhline(10 / n, ls="--", color="green", lw=0.8, label="SOLVED band (>=10/15)")
    ax[0].axhline(6 / n, ls=":", color="orange", lw=0.8, label="marginal (>=6/15)")
    ax[0].set_xticks([0, 1, 2]); ax[0].set_xticklabels(labels)
    ax[0].set_ylabel(f"localization hit rate (|err| <= {TOL_SEC}s)"); ax[0].set_ylim(0, 1.05)
    ax[0].set_title(f"On-line localization on {n} real subjects")
    for i, h in enumerate([win_h, fr_h, cu_h]):
        ax[0].text(i, h / n + 0.02, f"{h}/{n}", ha="center")
    ax[0].legend(fontsize=8)
    # example curves for one subject (the first that ran)
    r0 = rows[0]
    s0 = r0["subject"]
    data_o, sf = load_state_covs(s0, 1); data_c, _ = load_state_covs(s0, 2)
    nn = int(SEG_SEC * sf)
    covs = sliding_covs(np.concatenate([data_o[:, :nn], data_c[:, :nn]], axis=1), sf)
    E, C = embed_cumsum(covs); ms = int(MIN_SEG_SEC / STEP_SEC)
    def z(c):
        v = c[np.isfinite(c)]; return (c - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v) + 1e-12)
    tt = np.arange(len(covs)) * STEP_SEC
    ax[1].plot(tt, z(break_curve(C, LARGE_W)), color="gray", label="window-mean")
    ax[1].plot(tt, z(changepoint_fratio(E, C, ms)), color="crimson", label="F-ratio")
    ax[1].plot(tt, z(cusum_changepoint(E, C, ms)), color="steelblue", label="CUSUM")
    ax[1].axvline(r0["seam"] * STEP_SEC, ls="--", color="k", label="true seam")
    ax[1].set_xlabel("time (s)"); ax[1].set_ylabel("normalised detector response")
    ax[1].set_title(f"Detector curves (S{s0:03d})"); ax[1].legend(fontsize=8)
    fig.suptitle("Global permanence-aware on-line localization, real EEG", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(RESULTS_DIR, "online_localization_cusum.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "online_localization_cusum",
        "data": "PhysioNet eegbci, eyes-open (run 1) + eyes-closed (run 2) concatenated, same cache",
        "question": "Does a GLOBAL permanence-aware change-point detector localize the real transition where the local window-mean failed (4/15)?",
        "params": {"n_subjects": n, "channels": CHANNELS, "alpha_band": ALPHA_BAND,
                   "seg_sec": SEG_SEC, "step_sec": STEP_SEC, "large_w": LARGE_W,
                   "tol_sec": TOL_SEC, "min_seg_sec": MIN_SEG_SEC},
        "hits": {"window_mean": win_h, "fratio": fr_h, "cusum": cu_h, "n": n},
        "median_err_sec": {"window_mean": med_err("window_mean"),
                           "fratio": med_err("fratio"), "cusum": med_err("cusum")},
        "median_prominence": {"window_mean": med_prom("window_mean"),
                              "fratio": med_prom("fratio"), "cusum": med_prom("cusum")},
        "best_detector": best_name, "best_hits": best_h,
        "verdict": verdict,
        "per_subject": rows,
        "figures": ["online_localization_cusum.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  window-mean {win_h}/{n} | F-ratio {fr_h}/{n} | CUSUM {cu_h}/{n}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
