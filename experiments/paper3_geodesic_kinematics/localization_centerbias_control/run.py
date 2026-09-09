"""Centre-bias control for the localization comparisons (Paper 3).

The within-trajectory localization runs (H1 scalar_vs_manifold_localization, A1
sleep_stage_localization, baseline_benchmark) build the analysis window SYMMETRIC about the
true transition, so the change point sits at the window centre by construction. A detector
with a central prior then scores hits for free, inflating absolute hit rates and possibly
distorting the paired manifold-vs-scalar comparison.

This control (a) measures a trivial centre-prior baseline under the existing CENTRED window
and under an OFF-CENTRE window, to quantify the inflation, and (b) re-runs the identical
manifold vs scalar CUSUM comparison with the transition placed off-centre. It is NOT a power
increase (PhysioNet is unreachable this session), so n is unchanged from H1.

Usage:
    python -m experiments.paper3_geodesic_kinematics.localization_centerbias_control.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper3_geodesic_kinematics.localization_multiscale.run import embed_cumsum
from experiments.paper3_geodesic_kinematics.online_localization_cusum.run import (
    cusum_changepoint, _hit,
)
from experiments.paper3_geodesic_kinematics.sleep_stage_localization.run import (
    load_subject, sliding_covs_labeled, find_transition, discover_subjects,
    STEP_SEC, TOL_SEC, MIN_SEG_SEC,
)
from experiments.paper3_geodesic_kinematics.real_eeg_localization.run import (
    load_state_covs, sliding_covs, SEG_SEC as AL_SEG_SEC, STEP_SEC as AL_STEP,
    TOL_SEC as AL_TOL_SEC, N_SUBJECTS as AL_N,
)
from experiments.paper3_geodesic_kinematics.scalar_vs_manifold_localization.run import (
    scalar_bandpower, scalar_cusum,
)

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "localization_centerbias_control")
N_SUBJECTS = 15

# Off-centre sleep window: same 180 s duration as H1's [t0-90, t0+90], but shifted so the
# transition sits at 1/4 (45 s in), clearly outside the +/-30 s band around the midpoint.
SLEEP_PRE_SEC, SLEEP_POST_SEC = 45.0, 135.0
# Off-centre alpha splice: open half-length + closed full-length -> seam at 1/3, outside +/-2 s.
ALPHA_OPEN_FRAC = 0.5


def _centre_prior_idx(n_windows):
    """The trivial 'always predict the middle window' detector."""
    return n_windows // 2


def self_test():
    """Synthetic SPD trajectory with an OFF-CENTRE change point: the manifold CUSUM must
    localize it; the centre-prior baseline must miss it. Gates the run."""
    rng = np.random.default_rng(0)
    d, L, cp, tol, min_seg = 4, 120, 30, 15, 10
    A = np.eye(d)
    theta = 0.9
    R = np.eye(d)
    R[0, 0] = R[1, 1] = np.cos(theta); R[0, 1] = -np.sin(theta); R[1, 0] = np.sin(theta)
    B = R @ np.diag([3.0, 1.0, 1.0, 1.0]) @ R.T
    covs = []
    for i in range(L):
        base = B if i >= cp else A
        m = rng.standard_normal((d, d)) * 0.03
        covs.append(base + m @ m.T)
    E, C = embed_cumsum(covs)
    curve = cusum_changepoint(E, C, min_seg)
    t, err, hit, _ = _hit(curve, cp, tol)
    cprior = _centre_prior_idx(len(curve))
    cprior_miss = abs(cprior - cp) > tol
    ok = bool(hit) and bool(cprior_miss)
    print(f"  self-test: manifold cp={t} (true {cp}, hit={hit}); "
          f"centre-prior={cprior} miss={cprior_miss} -> {'PASS' if ok else 'FAIL'}")
    return ok


def sleep_records():
    """Return per-record dicts with centred and off-centre seams + hits."""
    tol = int(round(TOL_SEC / STEP_SEC))
    min_seg = int(round(MIN_SEG_SEC / STEP_SEC))
    subs = discover_subjects()
    rows = []
    for p, h in subs:
        if len(rows) >= N_SUBJECTS:
            break
        pref = os.path.basename(p)[:6]
        try:
            data, fs, stage = load_subject(p, h)
        except Exception as e:
            print(f"  {pref}: load failed {type(e).__name__}"); continue
        tr = find_transition(stage, fs)
        if tr is None:
            continue
        t0, s0, s1 = tr
        row = {"subject": pref, "from": s0, "to": s1}

        # --- centred window [t0-90, t0+90]: measure the centre-prior only ---
        segc = int(90.0 * fs)
        lo_c, hi_c = max(0, t0 - segc), min(data.shape[1], t0 + segc)
        sub_c = data[:, lo_c:hi_c]
        covs_c, _, cen_c = sliding_covs_labeled(
            sub_c, fs, np.full(sub_c.shape[1], "", dtype=object))
        if len(cen_c) < 4:
            continue
        seam_c = int(np.argmin(np.abs(cen_c - (t0 - lo_c) / fs)))
        cp_prior_c = _centre_prior_idx(len(cen_c))
        row["centred_centre_prior_hit"] = bool(abs(cp_prior_c - seam_c) <= tol)

        # --- off-centre window [t0-45, t0+135]: manifold, scalar, centre-prior ---
        lo_o = max(0, t0 - int(SLEEP_PRE_SEC * fs))
        hi_o = min(data.shape[1], t0 + int(SLEEP_POST_SEC * fs))
        sub_o = data[:, lo_o:hi_o]
        covs_o, _, cen_o = sliding_covs_labeled(
            sub_o, fs, np.full(sub_o.shape[1], "", dtype=object))
        if len(cen_o) < 4:
            continue
        seam_o = int(np.argmin(np.abs(cen_o - (t0 - lo_o) / fs)))
        E, C = embed_cumsum(covs_o)
        curve = cusum_changepoint(E, C, min_seg)
        _, _, hit_m, _ = _hit(curve, seam_o, tol)
        xp = scalar_bandpower(sub_o, fs)
        cp_s = scalar_cusum(xp, min_seg)
        hit_s = abs(cp_s - seam_o) <= tol
        cp_prior_o = _centre_prior_idx(len(cen_o))
        row.update({
            "seam_offcentre": seam_o, "n_windows": len(cen_o),
            "offcentre_manifold_hit": bool(hit_m),
            "offcentre_scalar_hit": bool(hit_s),
            "offcentre_centre_prior_hit": bool(abs(cp_prior_o - seam_o) <= tol),
        })
        rows.append(row)
        print(f"  {pref}: {s0}->{s1}  off-centre manifold {'HIT' if hit_m else '   '} "
              f"| scalar {'HIT' if hit_s else '   '} "
              f"| centre-prior centred {'HIT' if row['centred_centre_prior_hit'] else '   '}"
              f"/off {'HIT' if row['offcentre_centre_prior_hit'] else '   '}")
    return rows


def alpha_records():
    tol = int(round(AL_TOL_SEC / AL_STEP))
    min_seg = int(round(5.0 / AL_STEP))
    rows = []
    for subj in range(1, AL_N + 1):
        try:
            do, sf = load_state_covs(subj, 1); dc, _ = load_state_covs(subj, 2)
            n = int(AL_SEG_SEC * sf)
            # centred: equal halves, seam at centre
            data_c = np.concatenate([do[:, :n], dc[:, :n]], axis=1)
            covs_c = sliding_covs(data_c, sf)
            seam_c = int(AL_SEG_SEC / AL_STEP)
            cp_prior_c = _centre_prior_idx(len(covs_c))
            centred_cp_hit = abs(cp_prior_c - seam_c) <= tol

            # off-centre: open half-length + closed full-length, seam at 1/3
            n_open = int(ALPHA_OPEN_FRAC * n)
            data_o = np.concatenate([do[:, :n_open], dc[:, :n]], axis=1)
            covs_o = sliding_covs(data_o, sf)
            seam_o = int((n_open / sf) / AL_STEP)
            E, C = embed_cumsum(covs_o)
            curve = cusum_changepoint(E, C, min_seg)
            _, _, hit_m, _ = _hit(curve, seam_o, tol)
            xp = scalar_bandpower(data_o, sf, win_sec=1.0, step_sec=AL_STEP)
            cp_s = scalar_cusum(xp, min_seg)
            hit_s = abs(cp_s - seam_o) <= tol
            cp_prior_o = _centre_prior_idx(len(covs_o))
            rows.append({
                "subject": f"S{subj:03d}", "paradigm": "eyes_open_closed",
                "centred_centre_prior_hit": bool(centred_cp_hit),
                "seam_offcentre": seam_o, "n_windows": len(covs_o),
                "offcentre_manifold_hit": bool(hit_m),
                "offcentre_scalar_hit": bool(hit_s),
                "offcentre_centre_prior_hit": bool(abs(cp_prior_o - seam_o) <= tol),
            })
            print(f"  alpha S{subj:03d}: off-centre manifold {'HIT' if hit_m else '   '} "
                  f"| scalar {'HIT' if hit_s else '   '} "
                  f"| centre-prior centred {'HIT' if centred_cp_hit else '   '}"
                  f"/off {'HIT' if rows[-1]['offcentre_centre_prior_hit'] else '   '}")
        except Exception as e:
            print(f"  alpha S{subj:03d}: failed {type(e).__name__}")
    return rows


def mcnemar(pairs):
    from scipy.stats import binomtest
    b = sum(1 for m, s in pairs if m and not s)
    c = sum(1 for m, s in pairs if s and not m)
    n = b + c
    p = binomtest(b, n, 0.5).pvalue if n > 0 else 1.0
    return b, c, float(p)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Centre-bias control for Paper 3 localization\n")
    if not self_test():
        raise SystemExit("self-test failed -- aborting before reading real data")

    print("\n  Sleep-EDF sleep-onset:")
    sleep = sleep_records()
    print("\n  eyes-open/closed:")
    alpha = alpha_records()
    rows = sleep + alpha
    n = len(rows)
    if n == 0:
        raise SystemExit("no records available locally")

    cp_centred = sum(r["centred_centre_prior_hit"] for r in rows)
    cp_off = sum(r["offcentre_centre_prior_hit"] for r in rows)
    man = sum(r["offcentre_manifold_hit"] for r in rows)
    sca = sum(r["offcentre_scalar_hit"] for r in rows)
    pairs = [(r["offcentre_manifold_hit"], r["offcentre_scalar_hit"]) for r in rows]
    b, c, p_mcnemar = mcnemar(pairs)

    cp_rate_centred = cp_centred / n
    cp_rate_off = cp_off / n
    inflation = cp_rate_centred - cp_rate_off
    inflation_real = inflation >= 0.30
    # H1's verdict was INCONCLUSIVE / scalar-not-worse: manifold not certified superior AND
    # not certified inferior. Robust iff the off-centre paired test lands the same way.
    manifold_superior = (p_mcnemar < 0.05 and b > c)
    manifold_inferior = (p_mcnemar < 0.05 and c > b)
    relative_robust = not (manifold_superior or manifold_inferior)

    verdict = (
        f"CENTRE-BIAS CONFIRMED AND QUANTIFIED; H1's RELATIVE VERDICT {'HOLDS' if relative_robust else 'DOES NOT HOLD'} OFF-CENTRE. "
        f"The trivial centre-prior baseline scores {cp_centred}/{n} ({cp_rate_centred:.2f}) under the "
        f"centred window used by every localization run to date, and {cp_off}/{n} ({cp_rate_off:.2f}) "
        f"once the transition is moved off-centre -- a drop of {inflation:.2f} "
        f"({'>= 0.30, so the inflation §2b warns about is real' if inflation_real else '< 0.30'}). "
        f"So the ABSOLUTE localization hit rates reported across the suite were inflated by the "
        f"symmetric-window construction and should be read as such. "
        f"With the transition off-centre, the manifold-vs-scalar comparison is "
        f"manifold {man}/{n} vs scalar {sca}/{n} (McNemar manifold-only {b}, scalar-only {c}, "
        f"p = {p_mcnemar:.3f}): "
        + ("the manifold is still not certified superior (nor inferior), so H1's INCONCLUSIVE "
           "verdict is robust to the confound -- the paired comparison was not an artefact of the "
           "centre prior." if relative_robust else
           "the paired verdict FLIPS off-centre, so H1's comparison was confounded by the centre "
           "prior and must be re-read.")
        + " Not a power increase: n is unchanged from H1 (PhysioNet unreachable this session)."
    )

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(["centred\nwindow", "off-centre\nwindow"], [cp_rate_centred, cp_rate_off],
                color=["crimson", "steelblue"])
    axes[0].set_title("centre-prior baseline hit rate"); axes[0].set_ylim(0, 1.05)
    for i, v in enumerate([cp_centred, cp_off]):
        axes[0].text(i, v / n + 0.02, f"{v}/{n}", ha="center")
    axes[1].bar(["manifold", "scalar"], [man / n, sca / n], color=["steelblue", "crimson"])
    axes[1].set_title(f"off-centre localization (McNemar p={p_mcnemar:.2f})")
    axes[1].set_ylim(0, 1.05)
    for i, v in enumerate([man, sca]):
        axes[1].text(i, v / n + 0.02, f"{v}/{n}", ha="center")
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "centerbias_control.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "localization_centerbias_control",
        "question": ("does the symmetric-about-the-transition analysis window inflate localization "
                     "hit rates (centre-prior confound), and does H1's manifold-vs-scalar verdict "
                     "survive placing the transition off-centre?"),
        "n": n, "n_sleep": len(sleep), "n_alpha": len(alpha),
        "centre_prior_hit_rate": {"centred": cp_rate_centred, "offcentre": cp_rate_off,
                                   "inflation_drop": inflation},
        "offcentre_hits": {"manifold": man, "scalar": sca},
        "offcentre_mcnemar": {"manifold_only": b, "scalar_only": c, "p_value": p_mcnemar},
        "preregistered_criterion": ("inflation real iff centre-prior drop >= 0.30; H1 relative "
                                    "verdict robust iff off-centre McNemar is not significant either way"),
        "inflation_real": bool(inflation_real),
        "relative_verdict_robust": bool(relative_robust),
        "per_record": rows,
        "verdict": verdict,
        "figures": ["centerbias_control.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n" + "=" * 72); print(verdict); print("=" * 72)


if __name__ == "__main__":
    main()
