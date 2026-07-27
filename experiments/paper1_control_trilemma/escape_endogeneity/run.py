"""Can escape from compactness be purely endogenous? (Paper 1 §7.5-7.6)

The Meta-Optimization Collapse Theorem is safe on its own domain: an autonomous flow
on a COMPACT set cannot be simultaneously positive-entropy and non-recurrent, because
Poincare recurrence is a theorem. `rl_agents_trichotomy` confirmed that empirically.

What is NOT a theorem is the clause that carries the escape horn (§7.5, first stated
limitation): "unbounded value drift is itself a failure of persistence ... it is a
more extreme Class M". Two claims travel together in the prose:

    E1  escape requires an external occasion;
    E2  escape forfeits persistence (Lambda -> M).

E1 is false and needs no experiment: theta_dot = theta*||theta|| is autonomous, has no
external term, and leaves every compact set in finite time. That is stated in the
pre-registration so no part of this can be sold as a discovery.

E2 is the real question -- a falsifiable claim about the JOINT achievability of escape
and persistence -- and is what the six autonomous candidates below test on four
measured properties: escape, openness, non-recurrence, and correlation power on the
contract-designated observable (§5.4's Lambda-vs-M criterion, at the same threshold
class_g_coherence uses, against phase-randomized surrogates).

INSTRUMENT NOTE. A first version of this file produced a verdict that FAVOURED the
paper for reasons that were partly artefacts. The defects are recorded rather than
quietly fixed:
  (a) escape was detected on the raw state norm, but two candidates carry their radius
      as log r, so a true radius of e^105 registered as a norm of 105 and read as
      "bounded";
  (b) the scale-free observable normalised the whole state vector including log r, so
      the radial coordinate contaminated the "direction";
  (c) openness was read off the full-state Lyapunov exponent, which is positive under
      pure uniform expansion -- stretching is not entropy, and a frozen-direction
      blow-up therefore scored as "open";
  (d) a finite-time blow-up left too few samples for the recurrence estimator, which
      returned NaN and was scored as "fails non-recurrence" -- but a trajectory that
      leaves in finite time and never returns is non-recurrent BY CONSTRUCTION.
(c) and (d) both biased toward the paper's own conclusion. All four are fixed below,
and a self-test on signals of known character now gates the run.

Usage:
    python -m experiments.paper1_control_trilemma.escape_endogeneity.run
"""
from __future__ import annotations

import ast
import inspect
import json
import os
import textwrap
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

warnings.filterwarnings("ignore")

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "escape_endogeneity")

# ---- pre-registered thresholds (fixed before the run) -----------------------
THR_PF = 0.05            # same bar class_g_coherence uses for condition 6
THR_SURR_P = 0.05        # separation from phase-randomized surrogates
N_SURROGATES = 200
THR_LAMBDA_OPEN = 0.01   # openness: ANGULAR Lyapunov exponent above this
THR_VAR_COLLAPSE = 1e-6  # observable variance below this = collapsed, not open
THR_RECURRENT = 0.5      # recurrence fraction above this = recurrent
LOG_ESCAPE_BOUND = 25.0  # log-radius beyond this counts as having left compactness

DT = 0.005
N_STEPS = 60000
SEED = 0


# =============================================================================
# candidate dynamics -- every one autonomous: f(state) only, never f(state, t)
# =============================================================================

def f_bounded_lorenz(s):
    """CONTROL. Compact attractor, positive entropy -- must come out recurrent."""
    x, y, z = s
    return np.array([10.0 * (y - x), x * (28.0 - z) - y, x * y - (8.0 / 3.0) * z])


def f_radial_blowup(s):
    """Pure exponential escape, frozen direction. Should fail OPENNESS."""
    return s.copy()


def f_finite_time_blowup(s):
    """theta_dot = theta*||theta||: leaves every compact set in FINITE time."""
    return s * np.linalg.norm(s)


def f_escaping_chaos(s):
    """Radial escape carrying a chaotic direction.

    s = [x1, x2, x3, log r], with x a full Lorenz state and the value vector
    theta = e^{log r} * x, so the radius diverges while the DIRECTION x/||x|| inherits
    Lorenz's chaos.

    The direction is deliberately NOT modelled as an autonomous flow on the sphere.
    An earlier version projected the field onto S^2 and asked whether the resulting
    S^2 flow was chaotic -- which Poincare-Bendixson forbids outright, so that
    candidate could not have been open whatever escape did to it. Letting the chaotic
    system live in R^3 and reading off its direction restores the possibility the
    experiment is supposed to be testing.
    """
    return np.array([*f_bounded_lorenz(s[:3]), 0.35])


def f_freezing_escape(s):
    """THE SERIOUS CANDIDATE: escape that endogenously slows its own direction.

    The same construction, with the chaotic motion divided by a power of the radius.
    As the state escapes, its own growth brakes its angular dynamics, so the direction
    can converge to a limit that is not a fixed point of the field -- a permanent,
    non-recurrent terminus reached with no external drive. Still autonomous: the
    braking is produced by the state's own radial coordinate, not by a clock.
    """
    slow = np.exp(-0.06 * s[3])
    return np.array([*(f_bounded_lorenz(s[:3]) * slow), 0.35])


def f_dimension_extension(s):
    """Endogenous activation of NEW value coordinates.

    A coordinate is dormant until an accumulated novelty budget reaches its threshold,
    then wakes and starts oscillating. Nothing external switches it: the budget is a
    state variable driven by the already-active coordinates. This is the case the
    theorem does not quantify over -- a flow whose EFFECTIVE dimension grows -- so it
    is reported as a scope finding, not as a counterexample within the quantifier.
    """
    n_dim = len(s) - 1
    out = np.zeros_like(s)
    active = min(1 + int(s[-1]), n_dim)
    for k in range(active):
        w = 0.7 + 0.31 * k
        nxt = s[(k + 1) % active] if active > 1 else 0.0
        out[k] = w * (nxt - 0.15 * s[k] ** 3) + 0.25 * np.sin(1.7 * s[k])
    out[-1] = 0.02 * np.sum(np.abs(s[:active]))
    return out


# Each candidate declares its own GEOMETRY, so the analysis never guesses which
# coordinates are values and which is a (possibly logarithmic) scale -- defect (a)/(b).
#   value : indices of the value vector
#   logr  : index holding log-radius, or None if the radius is just ||value||
CANDIDATES = [
    {"name": "bounded_lorenz", "f": f_bounded_lorenz, "s0": np.array([1.0, 1.0, 20.0]),
     "value": [0, 1, 2], "logr": None, "role": "control"},
    {"name": "radial_blowup", "f": f_radial_blowup, "s0": np.array([1.0, 0.6, -0.3]),
     "value": [0, 1, 2], "logr": None, "role": "escape"},
    {"name": "finite_time_blowup", "f": f_finite_time_blowup,
     "s0": np.array([1.0, 0.6, -0.3]), "value": [0, 1, 2], "logr": None, "role": "escape"},
    {"name": "escaping_chaos", "f": f_escaping_chaos, "s0": np.array([1.0, 1.0, 20.0, 0.0]),
     "value": [0, 1, 2], "logr": 3, "role": "escape"},
    {"name": "freezing_escape", "f": f_freezing_escape, "s0": np.array([1.0, 1.0, 20.0, 0.0]),
     "value": [0, 1, 2], "logr": 3, "role": "escape"},
    {"name": "dimension_extension", "f": f_dimension_extension,
     "s0": np.array([0.4, 0.0, 0.0, 0.0, 0.0]), "value": [0, 1, 2, 3], "logr": None,
     "role": "scope"},
]

BANNED = {"time", "datetime", "random", "rng", "clock", "perf_counter"}


def assert_autonomous(fn):
    """Structural check that no candidate is secretly non-autonomous.

    The experiment is about whether escape can happen with NO external drive, so
    'autonomous' cannot be left as a claim in a docstring. The BODY is parsed rather
    than the source grepped: an earlier version matched the substring "time." inside
    the docstring phrase "in FINITE time." and rejected an autonomous field.
    """
    params = list(inspect.signature(fn).parameters)
    if len(params) != 1:
        raise AssertionError(f"{fn.__name__} takes {params} -- not autonomous")
    fdef = ast.parse(textwrap.dedent(inspect.getsource(fn))).body[0]
    body = fdef.body
    if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    for node in ast.walk(ast.Module(body=body, type_ignores=[])):
        if isinstance(node, ast.Name) and node.id in BANNED:
            raise AssertionError(f"{fn.__name__} reads '{node.id}' -- not autonomous")
        if isinstance(node, ast.Attribute) and node.attr in BANNED:
            raise AssertionError(f"{fn.__name__} reads '.{node.attr}' -- not autonomous")
    return True


# =============================================================================
# integration and geometry
# =============================================================================

def rk4(f, s, dt):
    k1 = f(s); k2 = f(s + 0.5 * dt * k1)
    k3 = f(s + 0.5 * dt * k2); k4 = f(s + dt * k3)
    return s + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def log_radius(traj, spec):
    """True log-radius of the value vector, honouring log-coded scales -- defect (a)."""
    val = traj[:, spec["value"]]
    base = np.log(np.linalg.norm(val, axis=1) + 1e-300)
    if spec["logr"] is not None:
        base = base + traj[:, spec["logr"]]
    return base


def integrate(spec, n=N_STEPS, dt=DT):
    f, s = spec["f"], np.array(spec["s0"], float)
    traj = np.empty((n, len(s)))
    escaped = finite_time = False
    steps = n
    for i in range(n):
        traj[i] = s
        s = rk4(f, s, dt)
        if not np.all(np.isfinite(s)):
            escaped = finite_time = True
            steps = i + 1
            traj = traj[:steps]
            break
        lr = np.log(np.linalg.norm(s[spec["value"]]) + 1e-300)
        if spec["logr"] is not None:
            lr += s[spec["logr"]]
        if lr > LOG_ESCAPE_BOUND:
            escaped = True
            finite_time = i < n - 1
            steps = i + 1
            traj = traj[:steps]
            break
    return traj, escaped, finite_time, steps


# =============================================================================
# the two declared contracts (§5.4: persistence is contract-relative)
# =============================================================================

def obs_dir(traj, spec):
    """I_dir -- scale-free direction cosine of the VALUE vector only -- defect (b)."""
    val = traj[:, spec["value"]]
    u = val / (np.linalg.norm(val, axis=1, keepdims=True) + 1e-300)
    return u[:, 0]


def obs_raw(traj, spec):
    """I_raw -- the first value coordinate at TRUE scale (log-radius reinstated)."""
    val = traj[:, spec["value"]]
    u = val / (np.linalg.norm(val, axis=1, keepdims=True) + 1e-300)
    return u[:, 0] * np.exp(np.clip(log_radius(traj, spec), -700, 700))


CONTRACTS = {"I_dir": obs_dir, "I_raw": obs_raw}


# =============================================================================
# measurement
# =============================================================================

def _acf(x, max_lag):
    x = np.asarray(x, float) - np.mean(x)
    denom = np.sum(x * x)
    if denom <= 0:
        return np.zeros(max_lag)
    return np.array([np.sum(x[:len(x) - k] * x[k:]) / denom
                     for k in range(1, max_lag + 1)])


def correlation_power(f, decim=10):
    """P_f -- §5.4's Lambda-vs-M criterion, as class_g_coherence computes it."""
    fd = np.asarray(f, float)[::decim]
    fd = fd[np.isfinite(fd)]
    if len(fd) < 40:
        return 0.0
    max_lag = min(len(fd) // 4, 2000)
    if max_lag < 4:
        return 0.0
    return float(np.mean(_acf(fd, max_lag)[max_lag // 2:] ** 2))


def phase_randomised(x, rng):
    n = len(x)
    F = np.fft.rfft(x - np.mean(x))
    ph = rng.uniform(0, 2 * np.pi, len(F))
    ph[0] = 0.0
    if n % 2 == 0:
        ph[-1] = 0.0
    return np.fft.irfft(np.abs(F) * np.exp(1j * ph), n)


def persistence(f, rng):
    fd = np.asarray(f, float)
    fd = fd[np.isfinite(fd)]
    if len(fd) < 200:
        return {"P_f": 0.0, "surrogate_p": 1.0, "pass": False,
                "note": "observable too short to estimate"}
    pf = correlation_power(fd)
    surr = np.array([correlation_power(phase_randomised(fd, rng))
                     for _ in range(N_SURROGATES)])
    p = float((1 + np.sum(surr >= pf)) / (1 + len(surr)))
    return {"P_f": pf, "surrogate_p": p,
            "surrogate_median_P_f": float(np.median(surr)),
            "pass": bool(pf >= THR_PF and p < THR_SURR_P)}


def angular_lyapunov(spec, n=20000, dt=DT, d0=1e-9):
    """Openness MODULO SCALE -- divergence of DIRECTIONS, not of raw states -- defect (c).

    A pure radial blow-up stretches every separation uniformly and yields a large
    positive full-state exponent while the direction never moves. That is expansion,
    not entropy, and reading it as openness is how a frozen-direction escape scored as
    "open" in the first version. Here the perturbation is renormalised in the ANGULAR
    coordinate of the value vector, so uniform scaling contributes exactly zero.
    """
    f, vi = spec["f"], spec["value"]

    def direction(z):
        v = z[vi]
        return v / (np.linalg.norm(v) + 1e-300)

    p = np.array(spec["s0"], float)
    # Seed the perturbation PURELY TANGENTIALLY, at angular size exactly d0. A seed
    # with a radial component contributes one large negative log on the first step
    # (the radial part is invisible to an angular measurement), which alone put a
    # spurious -0.022 on a flow whose directions are exactly invariant.
    u0 = p[vi] / (np.linalg.norm(p[vi]) + 1e-300)
    e = np.zeros(len(vi))
    e[int(np.argmin(np.abs(u0)))] = 1.0
    tan0 = e - np.dot(e, u0) * u0
    tan0 = tan0 / (np.linalg.norm(tan0) + 1e-300)
    seed = u0 + d0 * tan0
    q = p.copy()
    q[vi] = seed / np.linalg.norm(seed) * np.linalg.norm(p[vi])
    acc, live = 0.0, 0
    for _ in range(n):
        p, q = rk4(f, p, dt), rk4(f, q, dt)
        if not (np.all(np.isfinite(p)) and np.all(np.isfinite(q))):
            break
        sep = np.linalg.norm(direction(q) - direction(p))
        if sep > 1e-300:
            acc += np.log(sep / d0)
            live += 1
            # Re-inject at angular size d0 ALONG THE TANGENT. Rescaling the raw
            # difference and then normalising shrinks it by its radial component,
            # which accumulated a spurious negative exponent (~-0.02) on a flow whose
            # directions are exactly invariant -- caught by the self-test.
            u_p, u_q = direction(p), direction(q)
            tan = (u_q - u_p) - np.dot(u_q - u_p, u_p) * u_p
            ntan = np.linalg.norm(tan)
            if ntan <= 1e-300:
                break
            newdir = u_p + d0 * (tan / ntan)
            newdir = newdir / (np.linalg.norm(newdir) + 1e-300)
            q = p.copy()
            q[vi] = newdir * np.linalg.norm(p[vi])
    return acc / (live * dt) if live else float("nan")


def recurrence_fraction(obs, eps_frac=0.05, theiler=200, stride=3):
    """Recurrence of the identity OBSERVABLE in a delay embedding.

    Euclidean throughout: none of these candidates lives on a torus, so the toroidal
    metric corrected in rl_agents_trichotomy is deliberately not reused here.
    """
    x = np.asarray(obs, float)
    x = x[np.isfinite(x)]
    if len(x) < 1000:
        return float("nan")
    lag = 20
    emb = np.stack([x[:-2 * lag], x[lag:-lag], x[2 * lag:]], axis=1)
    span = np.sqrt(np.mean(np.sum((emb - emb.mean(0)) ** 2, axis=1)))
    if span < 1e-12:
        return 1.0                      # collapsed to a point: trivially recurrent
    eps = eps_frac * span
    n = len(emb)
    tree = cKDTree(emb)
    idxs = list(range(0, n, stride))
    rec = 0
    for i in idxs:
        # A RETURN, not mere proximity: the trajectory must LEAVE the eps-ball and
        # come back. Counting any far-in-index neighbour instead scores a monotone
        # ramp as fully recurrent -- slow motion keeps distant indices spatially
        # close -- which would have mislabelled exactly the decelerating candidate
        # this experiment exists to test. Caught by the self-test before any result
        # was read.
        #
        # Computed exactly, without the O(n^2) scan: the neighbours of i within eps
        # form index runs. The run CONTAINING i is the visit in progress; a neighbour
        # outside that run is a genuine return, having required a departure to get
        # there. The Theiler window discards returns too close in index to count.
        nb = np.sort(np.asarray(tree.query_ball_point(emb[i], eps), dtype=int))
        if nb.size == 0:
            continue
        pos = int(np.searchsorted(nb, i))
        lo = hi = pos
        while lo > 0 and nb[lo] - nb[lo - 1] == 1:
            lo -= 1
        while hi < nb.size - 1 and nb[hi + 1] - nb[hi] == 1:
            hi += 1
        outside = np.concatenate([nb[:lo], nb[hi + 1:]])
        if outside.size and np.any(np.abs(outside - i) > theiler):
            rec += 1
    return rec / len(idxs)


# =============================================================================
# instrument self-test -- gates the run, as class_g_coherence's does
# =============================================================================

def selftest():
    """Validate each estimator on signals of KNOWN character before reading results."""
    checks = []
    rng = np.random.default_rng(1)
    t = np.arange(30000) * DT

    pf_sine = correlation_power(np.sin(2.0 * t))
    checks.append(("P_f detects a periodic signal", pf_sine > 0.3, f"{pf_sine:.3f}"))
    pf_noise = correlation_power(rng.standard_normal(30000))
    checks.append(("P_f rejects white noise", pf_noise < THR_PF, f"{pf_noise:.4f}"))

    lam_rad = angular_lyapunov(
        {"f": f_radial_blowup, "s0": np.array([1.0, 0.6, -0.3]), "value": [0, 1, 2]},
        n=4000)
    checks.append(("angular lambda ~ 0 under pure radial expansion",
                   abs(lam_rad) < THR_LAMBDA_OPEN, f"{lam_rad:+.5f}"))
    lam_lor = angular_lyapunov(
        {"f": f_bounded_lorenz, "s0": np.array([1.0, 1.0, 20.0]), "value": [0, 1, 2]},
        n=8000)
    checks.append(("angular lambda > 0 for Lorenz", lam_lor > THR_LAMBDA_OPEN,
                   f"{lam_lor:+.4f}"))

    # Guard the design error that produced the first reading of this experiment: an
    # escaping candidate must be CAPABLE of angular openness, or "escape kills
    # openness" is unfalsifiable by construction.
    lam_esc = angular_lyapunov(
        {"f": f_escaping_chaos, "s0": np.array([1.0, 1.0, 20.0, 0.0]),
         "value": [0, 1, 2]}, n=8000)
    checks.append(("escaping candidate CAN be angularly open",
                   lam_esc > THR_LAMBDA_OPEN, f"{lam_esc:+.4f}"))

    rec_per = recurrence_fraction(np.sin(2.0 * t))
    checks.append(("recurrence ~ 1 for a periodic orbit", rec_per > 0.9, f"{rec_per:.3f}"))
    rec_mono = recurrence_fraction(np.linspace(0.0, 100.0, 30000))
    checks.append(("recurrence ~ 0 for a monotone ramp", rec_mono < 0.1, f"{rec_mono:.3f}"))

    print("  instrument self-test")
    ok = True
    for label, passed, val in checks:
        print(f"      [{'ok' if passed else 'FAIL'}] {label}: {val}")
        ok &= bool(passed)
    if not ok:
        raise AssertionError("instrument self-test failed -- results not read")
    return [{"check": c, "pass": bool(p), "value": v} for c, p, v in checks]


# =============================================================================

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(SEED)
    print("Can escape from compactness be purely endogenous? (Paper 1 §7.5-7.6)\n")

    for spec in CANDIDATES:
        assert_autonomous(spec["f"])
    print(f"  autonomy check: all {len(CANDIDATES)} fields are f(state) only, "
          f"no time argument, no RNG\n")
    st = selftest()
    print()

    results, falsifiers, scope_gaps = {}, [], []

    for spec in CANDIDATES:
        name = spec["name"]
        traj, escaped, finite_time, steps = integrate(spec)
        lr = log_radius(traj, spec)
        lam_ang = angular_lyapunov(spec)
        open_ok = bool(np.isfinite(lam_ang) and lam_ang > THR_LAMBDA_OPEN)

        entry = {"role": spec["role"], "escaped": bool(escaped),
                 "finite_time_blowup": bool(finite_time),
                 "steps_integrated": int(steps),
                 "final_log_radius": float(lr[-1]),
                 "angular_lambda": None if not np.isfinite(lam_ang) else float(lam_ang),
                 "angularly_open": open_ok, "contracts": {}}

        for cname, obs_fn in CONTRACTS.items():
            obs = obs_fn(traj, spec)
            fin = obs[np.isfinite(obs)]
            var = float(np.var(fin[len(fin) // 2:])) if len(fin) > 4 else 0.0
            collapsed = var < THR_VAR_COLLAPSE
            rec = recurrence_fraction(obs)
            # Defect (d): a finite-time escape never returns. That is non-recurrence by
            # construction, not an estimator NaN to be scored as a failure.
            if finite_time:
                non_rec = True
                rec_note = "finite-time escape: non-recurrent by construction"
            elif np.isfinite(rec):
                non_rec, rec_note = bool(rec < THR_RECURRENT), ""
            else:
                non_rec, rec_note = False, "estimator returned NaN (too few samples)"
            per = persistence(obs, rng)
            all4 = bool(escaped and open_ok and not collapsed and non_rec and per["pass"])
            entry["contracts"][cname] = {
                "late_variance": var, "collapsed": bool(collapsed),
                "recurrence_fraction": None if not np.isfinite(rec) else float(rec),
                "recurrence_note": rec_note, "non_recurrent": non_rec,
                "open": bool(open_ok and not collapsed),
                "persistence": per, "all_four": all4}
            if all4:
                (scope_gaps if spec["role"] == "scope" else falsifiers).append(
                    [name, cname])

        results[name] = entry
        tag = ("ESCAPES" + (" (finite time)" if finite_time else "")) if escaped else "bounded"
        print(f"  {name:20s} {tag:22s} log r={lr[-1]:8.2f}  ang.lambda={lam_ang:+.4f}")
        for cname in CONTRACTS:
            c = entry["contracts"][cname]
            r = c["recurrence_fraction"]
            rs = "n/a" if r is None else f"{r:.3f}"
            print(f"      {cname:6s} rec={rs:>6s}  nonrec={str(c['non_recurrent']):5s}"
                  f"  P_f={c['persistence']['P_f']:.4f}"
                  f" (p={c['persistence']['surrogate_p']:.3f})"
                  f"  open={str(c['open']):5s}  ALL4={c['all_four']}")

    # ---- verdict -------------------------------------------------------
    if falsifiers:
        outcome = "REFUTES_E2"
        head = (f"E2 IS REFUTED. Autonomous escape can retain persistence: "
                f"{falsifiers} met all four pre-registered properties.")
    elif scope_gaps:
        outcome = "SCOPE_GAP"
        head = (f"E2 SURVIVES FOR FLOWS ON A FIXED SPACE, BUT THE THEOREM'S SCOPE IS "
                f"NARROWER THAN THE PROSE IMPLIES: {scope_gaps} met all four, and did "
                f"so by growing the effective dimension of the value space rather than "
                f"by escaping within a fixed one.")
    else:
        # ATTRIBUTION CHECK, not in the pre-registration and added because the run
        # exposed the need for it. If the BOUNDED control also fails persistence, then
        # persistence is being destroyed by something the escaping candidates share
        # with it -- here, chaos -- and the failure cannot be charged to escape. The
        # pre-registered rule is still reported as computed; what changes is what may
        # be concluded from it.
        ctrl = results.get("bounded_lorenz", {})
        ctrl_persists = any(c["persistence"]["pass"]
                            for c in ctrl.get("contracts", {}).values())
        if ctrl_persists:
            outcome = "SUPPORTS_E2"
            head = ("E2 SURVIVES. No autonomous candidate escaped compactness while "
                    "retaining openness, non-recurrence and correlation power under "
                    "either declared contract.")
        else:
            outcome = "SUPPORTS_E2_BUT_UNATTRIBUTABLE"
            head = ("BY THE LETTER OF THE PRE-REGISTERED RULE E2 SURVIVES -- every "
                    "escaping candidate fails a property under both contracts -- BUT "
                    "THE RESULT CANNOT BE ATTRIBUTED TO ESCAPE, AND IS THEREFORE "
                    "REPORTED AS INCONCLUSIVE. The bounded control, which never leaves "
                    "any compact set, fails persistence for the same reason the "
                    "escaping candidates do.")

    verdict = (
        head + " WHAT WAS AND WAS NOT AT ISSUE. The theorem is not in question on its "
        "own domain, where Poincare recurrence settles it; this tests the two weaker "
        "claims that carry the escape horn in the prose. E1 -- that escape requires an "
        "external occasion -- is FALSE, and was known to be false before the run: "
        "theta_dot = theta*||theta|| is autonomous, contains no external term, and "
        "leaves every compact set in FINITE time, which `finite_time_blowup` confirms "
        "numerically. Any sentence in §7.5-7.7 implying that leaving compactness is "
        "something done TO a system must be rewritten; endogenous escape is trivially "
        "available. E2 -- that escape forfeits persistence -- is the substantive claim. ")

    if outcome.startswith("SUPPORTS_E2"):
        reasons = []
        for nm, e in results.items():
            if not e["escaped"]:
                continue
            for cn, c in e["contracts"].items():
                miss = [k for k, v in (("openness", c["open"]),
                                       ("non-recurrence", c["non_recurrent"]),
                                       ("persistence", c["persistence"]["pass"]))
                        if not v]
                if miss:
                    reasons.append(f"{nm}/{cn} fails {'+'.join(miss)}")
        verdict += ("Every escaping candidate fails at least one property under both "
                    "contracts: " + "; ".join(reasons) + ". The PATTERN is the "
                    "reportable content. Escape is easy and openness is easy, but they "
                    "are bought from different accounts: an escape fast enough to be "
                    "permanent drives the identity observable either to a frozen "
                    "direction (no openness) or onto a scale where the contract's "
                    "correlation structure cannot be estimated, while a system that "
                    "keeps its correlation structure keeps returning. ")
        if outcome == "SUPPORTS_E2_BUT_UNATTRIBUTABLE":
            verdict += (
                "WHAT THIS DESIGN CANNOT SETTLE, stated plainly rather than left for a "
                "reviewer. The escaping candidates DO achieve escape, openness AND "
                "non-recurrence simultaneously -- Poincare recurrence is not what stops "
                "them, and that much is a real finding: in the escaping regime §7.5's "
                "disposal of the horn rests entirely on the PERSISTENCE condition, not "
                "on the trichotomy. But the persistence failure cannot be charged to "
                "escape, because the bounded control fails it too. The reason is "
                "structural: the only openness available to these candidates is CHAOS, "
                "and chaos destroys correlation power whether or not the trajectory "
                "escapes. Worse, the operationalisation itself is contestable -- "
                "'openness' is read here as a positive Lyapunov exponent, which is "
                "§7.5's 'positive entropy' sense, whereas Class G in §8.3 requires the "
                "opposite signature (protected tangential spectrum, |lambda_par| ~ 0, "
                "with incommensurable frequencies and retained correlation power). "
                "Those two senses of openness come apart, and the paper uses both. A "
                "system that is aperiodic and correlation-retaining WITHOUT being "
                "chaotic -- quasi-periodic with incommensurable frequencies, which is "
                "what Class G actually demands -- is exactly the case this battery does "
                "not contain, and it is the case most likely to escape while "
                "persisting. Adding it now would be fitting a candidate to a result, "
                "which the pre-registration forbids; it is named here as the required "
                "follow-up experiment instead.")
        else:
            verdict += ("That is what §7.5 asserts, and a reader was entitled to see "
                        "it tested rather than assumed.")
    elif outcome == "SCOPE_GAP":
        verdict += ("The theorem quantifies over autonomous flows on a FIXED compact "
                    "subset of R^n. A system that endogenously activates new value "
                    "coordinates is not a counterexample within that quantifier -- it "
                    "lies outside it. §7.5 should state its scope as fixed-dimensional, "
                    "because 'autonomous preference dynamics' reads more broadly than "
                    "what is proved, and an agent that extends its own value space is "
                    "exactly the case a critic of the endogenous horn will raise.")
    else:
        verdict += ("§7.5's escape clause must be reformulated: unbounded value drift "
                    "does NOT automatically forfeit persistence, so the paper cannot "
                    "dispose of the escape horn by calling it 'a more extreme Class M'.")

    verdict += (" INSTRUMENT PROVENANCE, recorded because it cuts against this "
                "verdict's own direction: a first version of this experiment reported "
                "SUPPORTS_E2 partly for artefactual reasons -- openness was read from a "
                "full-state Lyapunov exponent that is positive under pure uniform "
                "expansion, and a finite-time blow-up was scored as recurrent because "
                "the estimator returned NaN on too few samples. Both errors flattered "
                "the paper. They are fixed here (angular exponent; explicit "
                "non-recurrence for finite-time escape), and the estimators are now "
                "gated by a self-test on signals of known character.")

    # ---- figure --------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, spec in zip(axes.ravel(), CANDIDATES):
        traj, _, _, _ = integrate(spec, n=min(N_STEPS, 20000))
        ax.plot(obs_dir(traj, spec)[:8000], lw=0.6, color="#7a2e2e")
        e = results[spec["name"]]
        c = e["contracts"]["I_dir"]
        lam = e["angular_lambda"]
        ax.set_title(f"{spec['name']}\n{'ESCAPES' if e['escaped'] else 'bounded'} · "
                     f"$P_f$={c['persistence']['P_f']:.3f} · "
                     f"$\\lambda_{{ang}}$={lam:+.3f}" if lam is not None else
                     spec["name"], fontsize=9)
        ax.set_xlabel("step"); ax.set_ylabel("$I_{dir}$")
    fig.suptitle("Autonomous escape from compactness: does persistence survive?",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "escape_endogeneity.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "escape_endogeneity",
        "question": "Can a purely autonomous preference dynamics leave every compact "
                    "set while retaining openness, non-recurrence and persistence?",
        "E1_escape_requires_external_occasion": False,
        "E1_note": "Known false before the run; an autonomous blow-up leaves every "
                   "compact set in finite time. Recorded in the pre-registration so it "
                   "cannot be presented as a discovery.",
        "thresholds": {"P_f": THR_PF, "surrogate_p": THR_SURR_P,
                       "angular_lambda_open": THR_LAMBDA_OPEN,
                       "recurrent_above": THR_RECURRENT,
                       "log_escape_bound": LOG_ESCAPE_BOUND,
                       "n_surrogates": N_SURROGATES},
        "contracts": {"I_dir": "scale-free direction cosine of the value vector "
                               "(ordinal contract)",
                      "I_raw": "first value coordinate at true scale (cardinal contract)"},
        "instrument_selftest": st,
        "instrument_defects_fixed": [
            "escape detected on raw state norm, missing log-coded radii",
            "scale-free observable normalised the log-radius into the direction",
            "openness read from a full-state Lyapunov exponent, positive under pure "
            "uniform expansion (biased toward the paper)",
            "finite-time blow-up scored as failing non-recurrence via an estimator NaN "
            "(biased toward the paper)"],
        "candidates": results,
        "attribution": {
            "control_bounded_lorenz_persists": bool(
                any(c["persistence"]["pass"] for c in
                    results.get("bounded_lorenz", {}).get("contracts", {}).values())),
            "note": "If the bounded control also fails persistence, the escaping "
                    "candidates' failure cannot be attributed to escape. Checked after "
                    "the run, not pre-registered; it downgrades what may be concluded "
                    "rather than changing the pre-registered rule."},
        "required_follow_up": "A candidate that is aperiodic and correlation-retaining "
                              "WITHOUT being chaotic (quasi-periodic, incommensurable "
                              "frequencies -- Class G's actual openness signature, "
                              "|lambda_par| ~ 0), which this battery lacks. Adding it "
                              "here would be fitting a candidate to a result.",
        "falsifiers": falsifiers,
        "scope_gaps": scope_gaps,
        "outcome": outcome,
        "verdict": verdict,
        "figures": ["escape_endogeneity.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=float)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"\nResults + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
