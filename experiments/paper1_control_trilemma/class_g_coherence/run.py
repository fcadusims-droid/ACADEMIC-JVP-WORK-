"""Class G internal coherence -- is the ten-condition profile non-vacuous? (Paper 1 §8.3)

Paper 1's entire positive residue is Class G, defined in §8.3 as a SINGLE CONJUNCTIVE
exclusion criterion of TEN conditions ("G-admissible only if it survives all ten
exclusions at once"). That conjunction has never been tested for satisfiability. If
the ten conditions are mutually unsatisfiable, Class G is empty by over-specification
and §§8-10 must be rewritten. The Paper 2 §15.2 toy demo does NOT settle this: it
measures four diagnostics and never tests conditions 1, 3, 8, 9 or 10 at all.

A conjunctive criterion can be vacuous in EITHER direction, and both are tested:
  * EMPTY      -- nothing satisfies all ten (Class G excludes even its own instances);
  * UNIVERSAL  -- everything satisfies all ten (the criterion excludes nothing).
Healthy = SATISFIABLE and DISCRIMINATING: an explicit system passes all ten, and each
near-miss from §8.3's own filter table fails the condition the paper predicts.

The witness system, on x = (q, r, phi1, phi2, a, theta):
  q      -- regime coordinate on a double well V0(q)=(q^2-1)^2/4; M basin at q=-1
            (dispersive), Lambda basin at q=+1, barrier at q=0
  r      -- deviation from the identity manifold, contracted at rate kappa
  phi1,2 -- protected phases at INCOMMENSURABLE frequencies (golden ratio);
            identity observable f = cos(phi1) + cos(phi2)
  a      -- agency coordinate (Ornstein-Uhlenbeck, diffusion D_ag)
  theta  -- orientation driving the receptivity gate chi(theta)

The G intervention MODIFIES THE LANDSCAPE rather than commanding a path:
  V_G(q) = V0(q) - chi(theta) * B * h(q),  h peaked at the barrier top,
so the applied field is W_G(x,theta) = chi(theta) * W_ext(q), W_ext(q) = B * h'(q).

Usage:
    python -m experiments.paper1_control_trilemma.class_g_coherence.run
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "class_g_coherence")

PHI_GOLDEN = (1.0 + np.sqrt(5.0)) / 2.0

# ---- pre-registered thresholds (see PRE-REGISTRATION.md; fixed before running) ----
THR_BARRIER_FRAC = 0.9      # cond 1: dV_G <= 0.9 * dV_0
THR_VAR_AG = 0.1            # cond 2: Var(a) >= 0.1
THR_DID_FRAC = 0.5          # cond 3: D_id <= 0.5 * D_c
THR_LAM_PERP = -0.05        # cond 4: lambda_perp <= -0.05
THR_LAM_PAR = 0.05          # cond 5: |lambda_par| <= 0.05
THR_PF = 0.05               # cond 6: correlation power >= 0.05
THR_PERIODIC_ERR = 1e-6     # cond 7: exact-periodicity sup-norm tolerance
THR_RATIONAL_Q = 20         # cond 8: no p/q with q <= 20 ...
THR_RATIONAL_TOL = 1e-3     #         ... within this tolerance
THR_RANK1_RESID = 1e-6      # cond 9: rank-1 relative residual <= 1e-6
THR_GATE_TRIVIAL = 0.1      #         and min(chi) <= 0.1 * max(chi)
THR_ENDO_RESID = 0.1        # cond 10: projection residual >= 0.1

DT = 0.01
T_SIM = 2000.0
T_MFPT = 500.0
N_MFPT_SEEDS = 60
SIGMA_H = 0.4               # width of the barrier-lowering bump
Q_TARGET = 0.5              # crossing criterion for MFPT (into the Lambda basin)
R_MAX = 1.0                 # identity-invariant preservation bound on |r|


@dataclass
class Spec:
    """A candidate transformation. `kind` selects the G witness or a near-miss."""
    kind: str
    B: float = 0.15             # external barrier-lowering amplitude
    D_id: float = 0.02          # identity-direction diffusion
    D_ag: float = 0.5           # agency diffusion
    D_q: float = 0.05           # regime-coordinate diffusion
    kappa: float = 1.0          # transverse contraction rate
    gamma_a: float = 1.0        # agency mean reversion
    omega1: float = 1.0
    omega_ratio: float = PHI_GOLDEN
    omega_theta: float = 0.05   # slow orientation drift
    gamma_par: float = 0.0      # tangential damping (damping control only)
    coerce_A: float = 0.0       # state-imposing tracking gain (coercion control)
    endogenous_feedback: bool = False   # W_ext replaced by a multiple of F0's q-field
    ungated: bool = False       # chi == 1 (no receptivity gate)

    @property
    def omega2(self) -> float:
        return self.omega1 * self.omega_ratio


# ======================================================================
#  Landscape, endogenous field, external field, gate
# ======================================================================
def V0(q):
    return (q ** 2 - 1.0) ** 2 / 4.0


def dV0(q):
    """V0'(q) = q^3 - q  (the endogenous regime drift is -dV0)."""
    return q ** 3 - q


def h_bump(q):
    """Bump peaked at the barrier top q=0."""
    return np.exp(-q ** 2 / (2.0 * SIGMA_H ** 2))


def dh_bump(q):
    return -(q / SIGMA_H ** 2) * h_bump(q)


def chi_gate(theta, spec: Spec):
    """Receptivity gate chi(theta) in [0,1]: open at theta=0, closed at theta=pi."""
    if spec.ungated or spec.kind == "coercion":
        return np.ones_like(np.asarray(theta, dtype=float))
    return (1.0 + np.cos(theta)) / 2.0


def W_ext(q, spec: Spec):
    """The external field. For the endogenous-feedback control it is deliberately a
    multiple of the system's OWN q-drift, i.e. inside <F_0>."""
    if spec.endogenous_feedback:
        return spec.B * (-dV0(q))
    return spec.B * dh_bump(q)


def applied_force_q(q, theta, spec: Spec):
    """Total externally-applied force on q (excludes the endogenous -dV0)."""
    if spec.kind == "coercion":
        # state-imposing tracking toward a commanded target, no receptivity gate
        return spec.coerce_A * (Q_TARGET - q)
    return chi_gate(theta, spec) * W_ext(q, spec)


# ======================================================================
#  Simulation
# ======================================================================
def simulate(spec: Spec, seed=0, t_total=T_SIM, q0=-1.0, gate_open=False):
    """Euler-Maruyama on the full state. Returns dict of trajectories."""
    rng = np.random.default_rng(seed)
    n = int(t_total / DT)
    q, r, p1, p2, a = q0, 0.0, 0.0, 0.0, 0.0
    theta = 0.0 if gate_open else rng.uniform(0, 2 * np.pi)
    Q = np.empty(n); R = np.empty(n); F = np.empty(n); A = np.empty(n); TH = np.empty(n)
    sq, sr, sa = np.sqrt(2 * spec.D_q * DT), np.sqrt(2 * spec.D_id * DT), np.sqrt(2 * spec.D_ag * DT)
    for i in range(n):
        # --- endogenous field F_0 + external applied force ---
        dq = -dV0(q) + applied_force_q(q, theta, spec)
        dr = -spec.kappa * r
        if spec.gamma_par > 0.0:     # damping control: tangential collapse to a fixed phase
            dp1 = -spec.gamma_par * np.sin(p1)
            dp2 = -spec.gamma_par * np.sin(p2)
        else:
            dp1, dp2 = spec.omega1, spec.omega2
        da = -spec.gamma_a * a
        dth = 0.0 if gate_open else spec.omega_theta
        q = q + dq * DT + sq * rng.standard_normal()
        r = r + dr * DT + sr * rng.standard_normal()
        p1 = p1 + dp1 * DT
        p2 = p2 + dp2 * DT
        a = a + da * DT + sa * rng.standard_normal()
        theta = theta + dth * DT
        Q[i], R[i], A[i], TH[i] = q, r, a, theta
        F[i] = np.cos(p1) + np.cos(p2)
    return {"q": Q, "r": R, "f": F, "a": A, "theta": TH}


# ======================================================================
#  The ten condition tests
# ======================================================================
def cond1_barrier(spec: Spec):
    """dV^G_{M->Lambda} < dV_{M->Lambda}, plus a dynamical MFPT confirmation."""
    qs = np.linspace(-2.0, 2.0, 4001)
    # barrier under the intervention at maximal receptivity (gate fully open)
    theta_open = 0.0
    Vg = V0(qs) - np.array([np.trapezoid(applied_force_q(qs[:k + 1], theta_open, spec), qs[:k + 1])
                            for k in range(len(qs))])
    left = qs < 0.0
    dV0_barrier = float(V0(0.0) - np.min(V0(qs[left])))
    dVg_barrier = float(Vg[np.argmin(np.abs(qs))] - np.min(Vg[left]))
    # dynamical check: mean first passage M -> Lambda, gated vs no intervention
    def mfpt(sp):
        times = []
        for s in range(N_MFPT_SEEDS):
            tr = simulate(sp, seed=5000 + s, t_total=T_MFPT, q0=-1.0)
            idx = np.argmax(tr["q"] > Q_TARGET)
            crossed = bool(tr["q"][idx] > Q_TARGET) if idx > 0 or tr["q"][0] > Q_TARGET else False
            times.append(idx * DT if crossed else T_MFPT)   # censored at T_MFPT
        return float(np.mean(times)), float(np.mean(np.array(times) < T_MFPT))
    none_spec = Spec(kind="none", B=0.0, D_ag=spec.D_ag, D_id=spec.D_id, D_q=spec.D_q)
    mfpt_g, frac_g = mfpt(spec)
    mfpt_0, frac_0 = mfpt(none_spec)
    passed = (dVg_barrier <= THR_BARRIER_FRAC * dV0_barrier) and (mfpt_g < mfpt_0)
    return {"pass": bool(passed), "barrier_no_intervention": dV0_barrier,
            "barrier_under_G": dVg_barrier, "mfpt_G": mfpt_g, "mfpt_none": mfpt_0,
            "cross_frac_G": frac_g, "cross_frac_none": frac_0}


def cond2_agency(tr):
    v = float(np.var(tr["a"]))
    return {"pass": bool(v >= THR_VAR_AG), "var_agency": v}


def cond3_identity_diffusion(spec: Spec, D_c: float):
    ok = spec.D_id <= THR_DID_FRAC * D_c
    return {"pass": bool(ok), "D_id": spec.D_id, "D_c": D_c,
            "ratio": spec.D_id / D_c if D_c > 0 else float("inf")}


def measure_D_c(base: Spec, grid=(0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0), n_seeds=40):
    """D_c := smallest identity diffusion at which invariant preservation (|r| stays
    within R_MAX through the window) falls below 0.9."""
    out = []
    for d in grid:
        sp = Spec(kind="probe", B=base.B, D_id=d, D_ag=base.D_ag, D_q=base.D_q)
        keep = 0
        for s in range(n_seeds):
            tr = simulate(sp, seed=9000 + s, t_total=200.0)
            if np.max(np.abs(tr["r"])) < R_MAX:
                keep += 1
        out.append((d, keep / n_seeds))
    for d, p in out:
        if p < 0.9:
            return float(d), out
    return float(grid[-1] * 2), out          # never broke within the grid


def _lyap_numeric(spec: Spec, mode: str, t_total=50.0, delta=1e-6):
    """Numerically measured exponent of the DETERMINISTIC flow, in the transverse
    (r) or tangential (phase) subspace -- measured from the implemented dynamics, so
    an implementation bug shows up here rather than being assumed away."""
    n = int(t_total / DT)
    if mode == "perp":
        x, xp = 1.0, 1.0 + delta
        for _ in range(n):
            x += (-spec.kappa * x) * DT
            xp += (-spec.kappa * xp) * DT
        sep = abs(xp - x)
    else:
        p, pp = 0.0, delta
        for _ in range(n):
            if spec.gamma_par > 0.0:
                p += (-spec.gamma_par * np.sin(p)) * DT
                pp += (-spec.gamma_par * np.sin(pp)) * DT
            else:
                p += spec.omega1 * DT
                pp += spec.omega1 * DT
        sep = abs(pp - p)
    return float(np.log(max(sep, 1e-300) / delta) / t_total)


def cond4_transverse(spec: Spec):
    lam = _lyap_numeric(spec, "perp")
    return {"pass": bool(lam <= THR_LAM_PERP), "lambda_perp": lam}


def cond5_tangential(spec: Spec):
    lam = _lyap_numeric(spec, "par")
    return {"pass": bool(abs(lam) <= THR_LAM_PAR), "lambda_par": lam}


def _acf(x, max_lag):
    x = x - x.mean()
    denom = np.sum(x * x)
    if denom <= 0:
        return np.zeros(max_lag)
    return np.array([np.sum(x[:len(x) - k] * x[k:]) / denom for k in range(1, max_lag + 1)])


def cond6_correlation_power(tr):
    f = tr["f"][::10]                       # decimate: lags in units of 0.1 t
    max_lag = min(len(f) // 4, 2000)
    ac = _acf(f, max_lag)
    long_lags = ac[max_lag // 2:]           # long-lag half
    pf = float(np.mean(long_lags ** 2))
    return {"pass": bool(pf >= THR_PF), "P_f": pf}


def periodicity_report(f, dt, win_t=20.0, max_lag_t=200.0):
    """Exact-periodicity test with FRACTIONAL lags.

    A signal is periodic iff some shift tau makes f(t+tau)=f(t) identically, and the
    quality persists at 2*tau, 3*tau. Two subtleties make the naive version useless
    and are handled here:

      * an autocorrelation threshold cannot work at all -- quasi-periodic signals are
        *almost periodic*, so acf -> 1 at near-recurrences given enough lag range
        (see PRE-REGISTRATION.md);
      * an INTEGER-lag sup-norm search cannot work either -- a true period generally
        does not land on the sampling grid (for omega2/omega1 = 3/2 the period 4*pi
        falls between samples), so a genuinely periodic signal shows the same small
        residual as a quasi-periodic one. This was a real false-negative found by the
        commensurable control failing to be flagged; the fix is a fractional-lag
        search by cubic spline, so grid resolution stops being the limiting factor.
    """
    from scipy.interpolate import CubicSpline
    n = len(f)
    t = np.arange(n) * dt
    W = int(win_t / dt)
    max_lag = min(int(max_lag_t / dt), n - W - 1)
    if max_lag <= 10 or W <= 10:
        return {"sup_err_at_T": float("nan"), "T_star": float("nan"),
                "sup_err_at_2T": float("nan"), "sup_err_at_3T": float("nan"),
                "declared_periodic": False}
    scale = 2.0 * np.std(f) + 1e-12
    ref = f[:W]
    # ---- stage 1: coarse integer-lag scan (vectorised) ----
    lags = np.arange(int(1.0 / dt), max_lag)
    errs = np.array([np.max(np.abs(f[k:k + W] - ref)) for k in lags]) / scale
    order = np.argsort(errs)[:20]                       # top candidates
    # ---- stage 2: fractional refinement by cubic spline ----
    cs = CubicSpline(t, f)
    def err_at(tau):
        if tau <= 0 or tau + win_t >= t[-1]:
            return float("nan")
        return float(np.max(np.abs(cs(t[:W] + tau) - ref)) / scale)
    # Brent minimisation around each candidate, so the limiting accuracy is the
    # spline's (~1e-10 here) rather than a refinement-grid spacing. Without this the
    # numerical floor (~1e-5) sits ABOVE the periodicity threshold and a pure sine is
    # misread as aperiodic -- caught by selftest_periodicity_detector().
    from scipy.optimize import minimize_scalar
    best_tau, best_err = float(lags[order[0]] * dt), np.inf
    for idx in order:
        tau0 = lags[idx] * dt
        try:
            r = minimize_scalar(lambda tau: err_at(tau) if not np.isnan(err_at(tau)) else np.inf,
                                bracket=None, bounds=(max(tau0 - 2 * dt, dt), tau0 + 2 * dt),
                                method="bounded", options={"xatol": 1e-10})
            e, tau = float(r.fun), float(r.x)
        except Exception:
            e, tau = err_at(tau0), tau0
        if not np.isnan(e) and e < best_err:
            best_err, best_tau = e, tau
    e2, e3 = err_at(2 * best_tau), err_at(3 * best_tau)
    periodic = (best_err < THR_PERIODIC_ERR
                and (np.isnan(e2) or e2 < THR_PERIODIC_ERR)
                and (np.isnan(e3) or e3 < THR_PERIODIC_ERR))
    return {"sup_err_at_T": float(best_err), "T_star": float(best_tau),
            "sup_err_at_2T": e2, "sup_err_at_3T": e3,
            "declared_periodic": bool(periodic)}


def selftest_periodicity_detector():
    """Validate the instrument on signals of KNOWN character before trusting it:
    a pure sine and a commensurable sum must read periodic; a golden-ratio
    (quasi-periodic) sum must not; a constant is trivially periodic."""
    dt = DT
    t = np.arange(int(T_SIM / dt)) * dt
    cases = {
        "pure_sine (periodic)": (np.cos(t), True),
        "commensurable_3_2 (periodic)": (np.cos(t) + np.cos(1.5 * t), True),
        "golden_ratio (quasi-periodic)": (np.cos(t) + np.cos(PHI_GOLDEN * t), False),
        "constant (periodic)": (np.zeros_like(t), True),
    }
    rows = []
    for name, (sig, want_periodic) in cases.items():
        rep = periodicity_report(sig, dt)
        ok = bool(rep["declared_periodic"]) == want_periodic
        rows.append({"case": name, "expected_periodic": want_periodic,
                     "declared_periodic": rep["declared_periodic"],
                     "sup_err_at_T": rep["sup_err_at_T"], "correct": ok})
    return rows, all(r["correct"] for r in rows)


def cond7_aperiodic(tr):
    rep = periodicity_report(tr["f"], DT)
    fdec = tr["f"][::10]
    ac = _acf(fdec, min(len(fdec) // 4, 2000))
    return {"pass": bool(not rep["declared_periodic"]),
            "sup_err_at_T": rep["sup_err_at_T"], "T_star": rep["T_star"],
            "sup_err_at_2T": rep["sup_err_at_2T"], "sup_err_at_3T": rep["sup_err_at_3T"],
            "declared_periodic": rep["declared_periodic"],
            "max_acf_secondary": float(np.max(ac)) if len(ac) else float("nan")}


def cond8_incommensurable(spec: Spec):
    ratio = spec.omega_ratio
    best = None
    for qd in range(1, THR_RATIONAL_Q + 1):
        p = round(ratio * qd)
        err = abs(ratio - p / qd)
        if best is None or err < best[2]:
            best = (int(p), int(qd), float(err))
    rational = best[2] < THR_RATIONAL_TOL
    return {"pass": bool(not rational), "ratio": float(ratio),
            "best_rational": f"{best[0]}/{best[1]}", "best_err": best[2]}


def cond9_gate_factorization(spec: Spec):
    """W_G = chi(theta) * W_ext(q): the applied-force matrix over a (theta x q) grid
    must be rank 1, AND the gate must be a genuine gate (it must actually close)."""
    thetas = np.linspace(0, 2 * np.pi, 64)
    qs = np.linspace(-1.5, 1.5, 128)
    M = np.array([[applied_force_q(q, th, spec) for q in qs] for th in thetas])
    if np.allclose(M, 0.0):
        return {"pass": False, "rank1_residual": float("nan"), "gate_min": 0.0,
                "gate_max": 0.0, "reason": "no applied field"}
    s = np.linalg.svd(M, compute_uv=False)
    resid = float(np.sqrt(np.sum(s[1:] ** 2)) / np.sqrt(np.sum(s ** 2)))
    ch = chi_gate(thetas, spec) if spec.kind != "coercion" else np.ones_like(thetas)
    # effective gate profile = row norms (captures a gate that is constant in theta)
    row = np.linalg.norm(M, axis=1)
    gmin, gmax = float(np.min(row)), float(np.max(row))
    nontrivial = gmin <= THR_GATE_TRIVIAL * gmax
    passed = (resid <= THR_RANK1_RESID) and nontrivial
    return {"pass": bool(passed), "rank1_residual": resid, "gate_min": gmin,
            "gate_max": gmax, "gate_nontrivial": bool(nontrivial),
            "chi_min": float(np.min(ch)), "chi_max": float(np.max(ch))}


def cond10_not_endogenous(spec: Spec):
    """W_ext not in <F_0>. Projected onto a DELIBERATELY GENEROUS endogenous basis
    {1, q, -dV0(q)} -- making the condition harder to pass, which is the honest
    direction."""
    qs = np.linspace(-1.5, 1.5, 601)
    w = W_ext(qs, spec)
    if np.allclose(w, 0.0):
        return {"pass": False, "residual": 0.0, "reason": "no external field"}
    basis = np.vstack([np.ones_like(qs), qs, -dV0(qs)]).T
    coef, *_ = np.linalg.lstsq(basis, w, rcond=None)
    resid = float(np.linalg.norm(w - basis @ coef) / np.linalg.norm(w))
    return {"pass": bool(resid >= THR_ENDO_RESID), "residual": resid}


# ======================================================================
#  Battery
# ======================================================================
def run_battery(spec: Spec, D_c: float):
    tr = simulate(spec, seed=1, t_total=T_SIM)
    res = {
        "1_barrier_lowered": cond1_barrier(spec),
        "2_agency_positive": cond2_agency(tr),
        "3_identity_subcritical": cond3_identity_diffusion(spec, D_c),
        "4_transverse_contract": cond4_transverse(spec),
        "5_tangential_protected": cond5_tangential(spec),
        "6_long_correlation": cond6_correlation_power(tr),
        "7_aperiodic": cond7_aperiodic(tr),
        "8_incommensurable": cond8_incommensurable(spec),
        "9_gate_factorization": cond9_gate_factorization(spec),
        "10_not_endogenous": cond10_not_endogenous(spec),
    }
    failed = [k for k, v in res.items() if not v["pass"]]
    return {"conditions": res, "n_pass": 10 - len(failed), "failed": failed,
            "G_admissible": len(failed) == 0}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Class G internal coherence -- ten-condition non-vacuity test (Paper 1 §8.3)")

    # validate the periodicity instrument on signals of known character first
    st_rows, st_ok = selftest_periodicity_detector()
    print("  periodicity-detector self-test:")
    for r in st_rows:
        print(f"    {r['case']:34s} expected={str(r['expected_periodic']):5s} "
              f"got={str(r['declared_periodic']):5s} err={r['sup_err_at_T']:.1e} "
              f"{'OK' if r['correct'] else 'WRONG'}")
    if not st_ok:
        print("  !! detector self-test FAILED -- condition 7 results are not trustworthy")

    g_spec = Spec(kind="G")
    D_c, dc_curve = measure_D_c(g_spec)
    print(f"  measured critical identity diffusion D_c = {D_c:.3f} "
          f"(preservation curve: {[(d, round(p,2)) for d, p in dc_curve]})")

    # the G witness, plus the near-misses from §8.3's own filter table
    controls = {
        "G_witness": g_spec,
        "classical_damping": Spec(kind="damping", gamma_par=1.0, D_ag=0.0),
        "ungated_forcing": Spec(kind="ungated", ungated=True, B=0.45, D_id=0.30),
        "endogenous_feedback": Spec(kind="endogenous", endogenous_feedback=True),
        "coercion": Spec(kind="coercion", coerce_A=2.0, D_ag=0.0),
        "commensurable_drive": Spec(kind="commensurable", omega_ratio=1.5),
    }
    predicted = {"classical_damping": [2, 5], "ungated_forcing": [9],
                 "endogenous_feedback": [10], "coercion": [2, 9],
                 "commensurable_drive": [7, 8]}

    out = {}
    for name, sp in controls.items():
        r = run_battery(sp, D_c)
        out[name] = r
        tag = "G-ADMISSIBLE" if r["G_admissible"] else f"fails {[int(f.split('_')[0]) for f in r['failed']]}"
        print(f"  {name:22s}: {r['n_pass']:2d}/10  {tag}")

    g = out["G_witness"]
    witness_ok = g["G_admissible"]
    # discrimination: every control must fail >=1, and must include a predicted one
    disc_rows = []
    for name, preds in predicted.items():
        got = [int(f.split("_")[0]) for f in out[name]["failed"]]
        disc_rows.append({"control": name, "predicted_failures": preds,
                          "actual_failures": got,
                          "fails_something": len(got) > 0,
                          "includes_predicted": any(p in got for p in preds)})
    all_fail = all(d["fails_something"] for d in disc_rows)
    all_pred = all(d["includes_predicted"] for d in disc_rows)

    if witness_ok and all_fail and all_pred:
        outcome = "COHERENT_AND_DISCRIMINATING"
        verdict = (
            f"CLASS G IS NON-VACUOUS AND DISCRIMINATING. An explicit stochastic system "
            f"satisfies ALL TEN §8.3 conditions simultaneously (barrier lowered "
            f"{g['conditions']['1_barrier_lowered']['barrier_no_intervention']:.3f} -> "
            f"{g['conditions']['1_barrier_lowered']['barrier_under_G']:.3f} with mean "
            f"first-passage {g['conditions']['1_barrier_lowered']['mfpt_none']:.0f} -> "
            f"{g['conditions']['1_barrier_lowered']['mfpt_G']:.0f}; agency variance "
            f"{g['conditions']['2_agency_positive']['var_agency']:.2f}; identity diffusion "
            f"{g['conditions']['3_identity_subcritical']['D_id']:.3f} against a measured "
            f"critical {D_c:.3f}; lambda_perp "
            f"{g['conditions']['4_transverse_contract']['lambda_perp']:+.2f}, lambda_par "
            f"{g['conditions']['5_tangential_protected']['lambda_par']:+.3f}; correlation "
            f"power {g['conditions']['6_long_correlation']['P_f']:.2f}; aperiodic "
            f"(sup-norm exact-period error {g['conditions']['7_aperiodic']['sup_err_at_T']:.3f} "
            f">> {THR_PERIODIC_ERR:g}); incommensurable drive; gate factorization exact "
            f"(rank-1 residual {g['conditions']['9_gate_factorization']['rank1_residual']:.1e}) "
            f"with a gate that genuinely closes; and the external field is NOT in the "
            f"endogenous span (projection residual "
            f"{g['conditions']['10_not_endogenous']['residual']:.2f} against a deliberately "
            f"generous basis). So the ten conditions are MUTUALLY CONSISTENT: Class G is not "
            f"empty by over-specification, and §§8-10 stand as written, now with a "
            f"satisfiability witness. The criterion also DISCRIMINATES: every near-miss in "
            f"§8.3's own filter table fails, and each fails a condition the table predicts "
            f"-- damping fails {out['classical_damping']['failed']}, ungated forcing fails "
            f"{out['ungated_forcing']['failed']}, endogenous feedback fails "
            f"{out['endogenous_feedback']['failed']}, coercion fails {out['coercion']['failed']}, "
            f"a commensurable drive fails {out['commensurable_drive']['failed']}. The "
            f"conjunction therefore has real exclusionary content rather than being "
            f"satisfied by everything. SCOPE: this establishes logical consistency and "
            f"discrimination ONLY. It says nothing about whether any biological, "
            f"psychological or theological process instantiates Class G -- precisely the "
            f"question §8.3 declines to answer -- and domain-emptiness in any particular "
            f"substrate remains possible and untested here.")
    elif not witness_ok:
        outcome = "EMPTY"
        verdict = (
            f"CLASS G MAY BE EMPTY -- the witness construction FAILS conditions "
            f"{g['failed']} ({g['n_pass']}/10). Per the pre-registration this is reported as "
            f"prominently as a pass: if the failure reflects a FUNDAMENTAL TENSION between "
            f"conditions rather than an artifact of this construction, Class G is "
            f"over-specified and Paper 1 §§8-10 require rewriting. The specific failing "
            f"condition(s) and their measured values are in the per-condition record.")
    else:
        universal = [n for n in predicted if out[n]["G_admissible"]]
        outcome = "NON_DISCRIMINATING"
        verdict = (
            f"CLASS G IS SATISFIABLE BUT NOT DISCRIMINATING. The witness passes all ten, but "
            f"{universal} also pass — near-misses §8.3's own filter table says must be "
            f"excluded. The conjunction therefore fails to exclude what the paper claims it "
            f"excludes, and the offending condition(s) must be strengthened or the filter "
            f"table corrected. Controls that failed nothing: {universal}.")

    # ---- figure ----
    names = list(controls.keys())
    cond_labels = [f"{i}" for i in range(1, 11)]
    M = np.array([[1 if out[n]["conditions"][k]["pass"] else 0
                   for k in out[n]["conditions"]] for n in names])
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.imshow(M, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(10)); ax.set_xticklabels(cond_labels)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Class G condition (§8.3)")
    for i in range(len(names)):
        for j in range(10):
            ax.text(j, i, "P" if M[i, j] else "F", ha="center", va="center", fontsize=7)
    ax.set_title(f"Class G ten-condition battery — witness {'PASSES' if witness_ok else 'FAILS'}; "
                 f"near-misses excluded: {sum(1 for d in disc_rows if d['fails_something'])}/5")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "class_g_coherence.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "class_g_coherence",
        "question": "Are Paper 1 §8.3's ten Class G conditions jointly satisfiable (non-vacuous), "
                    "and do they discriminate against the paper's own named near-misses?",
        "thresholds": {"barrier_frac": THR_BARRIER_FRAC, "var_agency": THR_VAR_AG,
                       "D_id_frac": THR_DID_FRAC, "lambda_perp": THR_LAM_PERP,
                       "lambda_par_abs": THR_LAM_PAR, "P_f": THR_PF,
                       "periodic_sup_err": THR_PERIODIC_ERR, "rational_q": THR_RATIONAL_Q,
                       "rank1_residual": THR_RANK1_RESID, "gate_trivial_frac": THR_GATE_TRIVIAL,
                       "endogenous_residual": THR_ENDO_RESID},
        "periodicity_detector_selftest": {"cases": st_rows, "valid": bool(st_ok),
            "note": "instrument validated on known-character signals before use; an "
                    "integer-lag search and a coarse fractional grid were both found "
                    "to misclassify genuinely periodic signals and were fixed"},
        "measured_D_c": D_c, "D_c_preservation_curve": dc_curve,
        "batteries": out,
        "discrimination": disc_rows,
        "witness_G_admissible": bool(witness_ok),
        "all_controls_excluded": bool(all_fail),
        "all_controls_fail_a_predicted_condition": bool(all_pred),
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["class_g_coherence.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
