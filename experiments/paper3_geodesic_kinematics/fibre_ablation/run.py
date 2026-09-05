"""Fibre ablation -- does the bundle apparatus earn its place? (Paper 3)

An audit found the fibre (Sec 3.2), the Sasaki-type metric and the Ehresmann
connection (Sec 3.3) are not merely un-isolated by the experiment suite but
UNEXERCISED: `stats_utils.t_eff_product` is never called, no experiment builds a
bundle point, and every validated result is a property of the trace-normalized SPD
base alone. This runs the ablation the paper never ran.

Arms (identical data, windows, detectors, tolerance):
  A  base only                 -- the committed method
  B  base + fibre (Sasaki)     -- the paper's full construction, two scalings
  C  fibre only                -- control: does the coupling carry anything?

See PRE-REGISTRATION.md. One run, no tuning loop.

Usage:
    python -m experiments.paper3_geodesic_kinematics.fibre_ablation.run
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, hilbert

from experiments.shared_lib import spd_manifold as spd

warnings.filterwarnings("ignore")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "fibre_ablation")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "mne_eegbci")

# ---- pre-fixed parameters ----------------------------------------------------
N_SUBJECTS = 15
CHANNELS = ["O1", "Oz", "O2", "PO3", "POz", "PO4", "Pz"]
LOW_BAND = (8.0, 13.0)      # slow carrier: phase
HIGH_BAND = (20.0, 45.0)    # fast component: envelope
SEG_SEC = 26.0
WIN_SEC = 2.0               # longer than the committed 1.0 s: PAC needs cycles
STEP_SEC = 0.25
EIG_FLOOR = 1e-3
TOL_SEC = 2.0
N_PERM = 300
_R = 2.0


# ======================================================================
#  representations
# ======================================================================
def _bp(data, sf, band):
    b, a = butter(4, [band[0] / (sf / 2), band[1] / (sf / 2)], btype="band")
    return filtfilt(b, a, data, axis=1)


def base_fibre_windows(data, sf):
    """Per window: base embedding (flattened 2*sqrt(rho)) and normalized PAC matrix.

    Fibre (Sec 3.2): C_xs[i,j] = < exp(i phi_L^(i)) * E_H^(j) >, normalized by the
    GEOMETRIC mean of the two block traces -- the normalization that makes it
    invariant under independent rescaling of the two bands.
    """
    lo = _bp(data, sf, LOW_BAND)
    hi = _bp(data, sf, HIGH_BAND)
    phi = np.angle(hilbert(lo, axis=1))          # slow-carrier phase
    env = np.abs(hilbert(hi, axis=1))            # fast envelope
    w, step = int(WIN_SEC * sf), int(STEP_SEC * sf)
    bases, fibres = [], []
    for s in range(0, data.shape[1] - w + 1, step):
        L = lo[:, s:s + w]
        P = phi[:, s:s + w]
        E = env[:, s:s + w]
        # base: trace-normalized SPD covariance of the slow band
        c = spd.trace_normalize(spd.eigfloor(np.cov(L), EIG_FLOOR))
        bases.append(spd.sqrt_embed(c).reshape(-1))
        # fibre: cross-channel PAC matrix
        z = np.exp(1j * P)                        # (n_ch, w)
        C = (z @ E.T) / w                         # (n_ch, n_ch) complex
        tr_L = float(np.trace(np.cov(L)))
        tr_E = float(np.trace(np.cov(E)))
        denom = np.sqrt(max(tr_L, 1e-24) * max(tr_E, 1e-24))
        Ct = C / denom
        fibres.append(np.concatenate([Ct.real.reshape(-1), Ct.imag.reshape(-1)]))
    return np.array(bases), np.array(fibres)


def _median_step(X):
    if len(X) < 2:
        return 0.0
    return float(np.median(np.linalg.norm(np.diff(X, axis=0), axis=1)))


def build_arms(bases, fibres):
    """A = base, B_lit = [base, fibre], B_eq = [base, scaled fibre], C = fibre."""
    sb, sf_ = _median_step(bases), _median_step(fibres)
    k = (sb / sf_) if sf_ > 1e-18 else 0.0
    return {
        "A_base": bases,
        "B_sasaki_literal": np.hstack([bases, fibres]),
        "B_sasaki_equal": np.hstack([bases, fibres * k]),
        "C_fibre": fibres,
    }, {"median_base_step": sb, "median_fibre_step": sf_, "equalizing_factor": k}


# ======================================================================
#  detectors (identical across arms)
# ======================================================================
def cusum_cp(X, min_seg):
    """Generic geodesic-CUSUM analogue on feature vectors: project each point's
    deviation from the global mean onto the first-quarter -> last-quarter direction
    and take argmax |cumsum|."""
    n = len(X)
    m0 = X.mean(0)
    q = max(min_seg, n // 4)
    u = X[n - q:].mean(0) - X[:q].mean(0)
    nu = np.linalg.norm(u)
    u = u / nu if nu > 1e-18 else u
    s = (X - m0) @ u
    s = s - s.mean()
    S = np.abs(np.cumsum(s))
    curve = np.full(n, -np.inf)
    curve[min_seg:n - min_seg] = S[min_seg:n - min_seg]
    return int(np.argmax(curve))


def discrimination(Xa, Xb, rng):
    """Between/within ratio with a within-state permutation null, same for all arms."""
    def gmean(Z):
        return Z.mean(0)
    def ratio(A, B):
        between = np.linalg.norm(gmean(A) - gmean(B))
        def within(Z):
            h = len(Z) // 2
            return np.linalg.norm(gmean(Z[:h]) - gmean(Z[h:]))
        return between / (0.5 * (within(A) + within(B)) + 1e-12)
    obs = ratio(Xa, Xb)
    pool = np.vstack([Xa, Xb]); na = len(Xa)
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        p = rng.permutation(len(pool))
        null[i] = ratio(pool[p[:na]], pool[p[na:]])
    pv = float((np.sum(null >= obs) + 1) / (N_PERM + 1))
    return float(obs), pv, bool(obs > 1.0 and pv < 0.05)


# ======================================================================
#  self-test: injected PAC change the base cannot see
# ======================================================================
def _synthetic_pac(seed=0, sf=160.0, dur=52.0, seam=26.0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(dur * sf)) / sf
    n = len(t)
    carrier = np.sin(2 * np.pi * 10.0 * t)
    phase = 2 * np.pi * 10.0 * t
    fast = np.sin(2 * np.pi * 30.0 * t)
    # modulation present before the seam, absent after; base mixing held FIXED
    mod = np.where(t < seam, 0.5 * (1 + np.cos(phase)), 1.0)
    ch0 = carrier + 0.6 * mod * fast + 0.05 * rng.standard_normal(n)
    ch1 = 0.8 * carrier + 0.6 * mod * fast + 0.05 * rng.standard_normal(n)
    ch2 = 0.5 * carrier + 0.3 * mod * fast + 0.05 * rng.standard_normal(n)
    return np.vstack([ch0, ch1, ch2]), sf, seam


def self_test():
    data, sf, seam_s = _synthetic_pac()
    bases, fibres = base_fibre_windows(data, sf)
    arms, _ = build_arms(bases, fibres)
    seam = int(seam_s / STEP_SEC)
    tol = int(TOL_SEC / STEP_SEC)
    min_seg = int(5.0 / STEP_SEC)
    err_fib = abs(cusum_cp(arms["C_fibre"], min_seg) - seam)
    err_base = abs(cusum_cp(arms["A_base"], min_seg) - seam)
    ok = err_fib <= tol
    print("Self-test (injected PAC change, base shape held fixed):")
    print(f"  fibre arm err {err_fib * STEP_SEC:5.2f}s  -> [{'PASS' if ok else 'FAIL'}]")
    print(f"  base  arm err {err_base * STEP_SEC:5.2f}s  (expected to miss: base is fixed)")
    if not ok:
        raise SystemExit("SELF-TEST FAILED -- coupling estimator cannot see an injected "
                         "PAC change; run aborted (instrument failure, not evidence).")
    return {"fibre_err_s": err_fib * STEP_SEC, "base_err_s": err_base * STEP_SEC,
            "passed": bool(ok)}


# ======================================================================
def load_broadband(subject, run):
    import mne
    from mne.datasets import eegbci
    paths = eegbci.load_data(subject, [run], path=DATA_DIR, update_path=False)
    raw = mne.io.read_raw_edf(str(paths[0]), preload=True, verbose="ERROR")
    eegbci.standardize(raw)
    raw.pick(CHANNELS)
    raw.filter(1.0, 50.0, verbose="ERROR")
    d = raw.get_data()
    d = (d - d.mean(1, keepdims=True)) / (d.std(1, keepdims=True) + 1e-12)
    return d, raw.info["sfreq"]


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(0)
    tol = int(TOL_SEC / STEP_SEC)
    min_seg = int(5.0 / STEP_SEC)
    print("Fibre ablation: does the bundle apparatus earn its place?")
    print(f"  low {LOW_BAND} (phase) x high {HIGH_BAND} (envelope), win {WIN_SEC}s, "
          f"tol +/-{TOL_SEC}s")
    st = self_test()

    arm_names = ["A_base", "B_sasaki_literal", "B_sasaki_equal", "C_fibre"]
    loc = {a: 0 for a in arm_names}
    disc = {a: [] for a in arm_names}
    scales, n_ok = [], 0

    for s in range(1, N_SUBJECTS + 1):
        try:
            do, sf = load_broadband(s, 1)
            dc, _ = load_broadband(s, 2)
            nn = int(SEG_SEC * sf)
            cat = np.concatenate([do[:, :nn], dc[:, :nn]], axis=1)
            bases, fibres = base_fibre_windows(cat, sf)
            arms, sc = build_arms(bases, fibres)
            scales.append(sc)
            seam = int(SEG_SEC / STEP_SEC)
            # discrimination uses the two pure states separately
            bo, fo = base_fibre_windows(do[:, :nn], sf)
            bc, fc = base_fibre_windows(dc[:, :nn], sf)
            arms_o, _ = build_arms(bo, fo)
            arms_c, _ = build_arms(bc, fc)
            row = []
            for a in arm_names:
                e = abs(cusum_cp(arms[a], min_seg) - seam)
                hit = e <= tol
                loc[a] += hit
                r, pv, ok = discrimination(arms_o[a], arms_c[a], rng)
                disc[a].append((r, ok))
                row.append(f"{a.split('_')[0]}:{'H' if hit else '.'}{r:4.1f}")
            n_ok += 1
            print(f"  S{s:03d}  " + "  ".join(row))
        except Exception as e:
            print(f"  S{s:03d}: FAILED {type(e).__name__}: {str(e)[:60]}")

    summary = {}
    for a in arm_names:
        rs = [r for r, _ in disc[a]]
        summary[a] = {
            "localization_hits": int(loc[a]), "n": n_ok,
            "discrimination_pass": int(sum(ok for _, ok in disc[a])),
            "median_ratio": float(np.median(rs)) if rs else float("nan"),
        }
        print(f"  {a:20s} loc {loc[a]:2d}/{n_ok}  disc {summary[a]['discrimination_pass']:2d}/{n_ok}"
              f"  median ratio {summary[a]['median_ratio']:.2f}")

    A = summary["A_base"]
    best_B = max(summary["B_sasaki_literal"], summary["B_sasaki_equal"],
                 key=lambda d: (d["localization_hits"], d["discrimination_pass"]))
    d_loc = best_B["localization_hits"] - A["localization_hits"]
    d_disc = best_B["discrimination_pass"] - A["discrimination_pass"]
    fibre_signal = summary["C_fibre"]["discrimination_pass"] >= max(2, 0.2 * n_ok)
    earns = (d_loc >= 3) or (d_disc >= 3 and best_B["median_ratio"] > A["median_ratio"])

    if earns:
        verdict = (
            f"FIBRE EARNS ITS PLACE. Adding the cross-scale coupling in the Sasaki-type "
            f"metric materially improves demarcation over the trace-normalized SPD base: "
            f"localization {A['localization_hits']}/{n_ok} -> {best_B['localization_hits']}/{n_ok} "
            f"(delta {d_loc:+d}), discrimination {A['discrimination_pass']}/{n_ok} -> "
            f"{best_B['discrimination_pass']}/{n_ok} (delta {d_disc:+d}). The bundle apparatus "
            f"is doing measurable work on this signal.")
    elif not fibre_signal and st["passed"]:
        verdict = (
            f"NO MATERIAL GAIN, and the fibre carries little on this signal. Base "
            f"{A['localization_hits']}/{n_ok} localization and {A['discrimination_pass']}/{n_ok} "
            f"discrimination; the best fibre-augmented arm reaches "
            f"{best_B['localization_hits']}/{n_ok} and {best_B['discrimination_pass']}/{n_ok} "
            f"(deltas {d_loc:+d}, {d_disc:+d}), both short of the pre-registered +3. The "
            f"fibre-only control passes discrimination in only "
            f"{summary['C_fibre']['discrimination_pass']}/{n_ok}, while the self-test confirms "
            f"the estimator DOES see an injected PAC change (err {st['fibre_err_s']:.2f}s) -- so "
            f"this is a real negative about the fibre's added value on eyes-open/closed EEG, "
            f"not a broken instrument. On what is measured, Paper 3's validated content is the "
            f"trace-normalized SPD base; the bundle apparatus is unearned on this signal.")
    else:
        verdict = (
            f"NO MATERIAL GAIN (deltas {d_loc:+d} localization, {d_disc:+d} discrimination, "
            f"against a pre-registered +3), though the fibre-only control does carry signal "
            f"({summary['C_fibre']['discrimination_pass']}/{n_ok} discrimination). The coupling "
            f"is measurable but redundant with the base for these tasks: it adds no demarcation "
            f"power the base does not already supply. Paper 3's bundle apparatus is not earning "
            f"its place on this signal, though it is not inert either.")

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    xs = np.arange(len(arm_names))
    ax[0].bar(xs, [summary[a]["localization_hits"] / max(n_ok, 1) for a in arm_names],
              color=["steelblue", "seagreen", "darkseagreen", "crimson"])
    ax[0].set_xticks(xs); ax[0].set_xticklabels([a.replace("_", "\n") for a in arm_names], fontsize=8)
    ax[0].set_ylabel(f"localization hit rate (|err|<={TOL_SEC}s)"); ax[0].set_ylim(0, 1.05)
    ax[0].set_title(f"Localization ({n_ok} real subjects)")
    for i, a in enumerate(arm_names):
        ax[0].text(i, summary[a]["localization_hits"] / max(n_ok, 1) + 0.02,
                   f"{summary[a]['localization_hits']}/{n_ok}", ha="center", fontsize=9)
    ax[1].bar(xs, [summary[a]["discrimination_pass"] / max(n_ok, 1) for a in arm_names],
              color=["steelblue", "seagreen", "darkseagreen", "crimson"])
    ax[1].set_xticks(xs); ax[1].set_xticklabels([a.replace("_", "\n") for a in arm_names], fontsize=8)
    ax[1].set_ylabel("discrimination pass rate"); ax[1].set_ylim(0, 1.05)
    ax[1].set_title("Structural discrimination")
    fig.suptitle("Fibre ablation: base vs base+fibre (Sasaki) vs fibre only", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "fibre_ablation.png"), dpi=130)
    plt.close(fig)

    out = {
        "experiment": "fibre_ablation",
        "question": ("does the fibre (cross-scale coupling in the Sasaki-type metric) "
                     "materially improve demarcation over the trace-normalized SPD base?"),
        "audit_finding": ("the fibre was UNEXERCISED before this run: stats_utils.t_eff_product "
                          "is never called by any experiment and no experiment builds a bundle "
                          "point; every prior validated result is a property of the base alone"),
        "data": "PhysioNet eegbci eyes-open (R01) / eyes-closed (R02), real EEG",
        "params": {"low_band": LOW_BAND, "high_band": HIGH_BAND, "win_sec": WIN_SEC,
                   "step_sec": STEP_SEC, "seg_sec": SEG_SEC, "tol_sec": TOL_SEC,
                   "n_perm": N_PERM},
        "self_test": st,
        "arms": summary,
        "deltas_best_B_minus_A": {"localization": int(d_loc), "discrimination": int(d_disc)},
        "preregistered_criterion": "fibre earns its place iff +3 localization hits or +3 discrimination passes with higher median ratio",
        "fibre_carries_signal": bool(fibre_signal),
        "scaling": scales[0] if scales else {},
        "verdict": verdict,
        "figures": ["fibre_ablation.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n" + "=" * 72); print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
