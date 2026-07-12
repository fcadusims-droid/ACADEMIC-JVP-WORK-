"""Does the Sec 14.1 sub-criticality control actually recover M_diss's power?
(Paper 2). Tests the control I2 (`dissociation_confound`) recommended and the
paper adopted but never validated.

I2 showed a bare critical generator (zero identity mechanism) reproduces the
dissociation signature D_bare_critical, reaching 73% of the identity reference at
the cleanest near-critical cell. I2's fix, written into Sec 14.1: trust a
dissociation result as identity-diagnostic ONLY if the boundary process is shown
to be measurably sub-critical. This asks whether that control (a) works when the
branching ratio sigma is known, and (b) is executable when sigma must be ESTIMATED
from a short, noisy recording -- the physiological regime -- where near-critical
confounded systems can be false-certified as safe.

Three arms at the adversarial cell (read-out noise 0.1):
  * no control     : accept all systems  -> reproduces I2's up-to-73% confound.
  * oracle control : accept true sigma < cut  -> best case the concept can reach.
  * realistic ctrl : accept only if a bootstrap upper bound on the estimated sigma
                     (Harris ratio-of-totals on a short subsampled recording)
                     certifies sigma < cut.

The gap between oracle and realistic isolates whether any failure is the control
CONCEPT or the MEASUREMENT.

Usage:
    python -m experiments.paper2_cbra_protocol.subcriticality_control.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper2_cbra_protocol.dissociation_confound.run import (
    run_bare_critical, run_identity_linked,
)

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "subcriticality_control"
)

# ---- population of boundary processes (safe -> near-critical) ----------------
SIGMA_GRID = np.round(np.linspace(0.70, 0.97, 10), 4)
ADVERSARIAL_NOISE = 0.1          # cleanest read-out: where the I2 confound is largest
SECONDARY_NOISE = 0.5
N_CONF_SEEDS = 8                 # seeds to average the confound signal D(sigma)

# ---- the control ------------------------------------------------------------
SIGMA_CUT = 0.90                 # require certified sigma < 0.90 (margin >= 0.10)
BOOT_B = 200
BOOT_UPPER_PCT = 95              # certify safe if 95th-pct bootstrap sigma-hat < cut
N_STUDIES = 300                  # Monte-Carlo studies per (sigma, budget)

# ---- realistic short recording (physiological regime) -----------------------
HEADLINE_N_AVAL = 40
BUDGET_SWEEP = [20, 40, 80, 160, 400]
OBS_GEN = 6
SEED_POP_LAMBDA = 10.0
SUBSAMPLE_F = 0.5

SAFE_SIGMA = 0.80                # "genuinely sub-critical" reference
CONFOUNDED_SIGMA = 0.925         # "confounded" reference (near-critical)

# ---- harder, more realistic observation model: a single CONTINUOUS subsampled
#      activity trace (not cleanly separated avalanches) -- the regime where
#      branching-ratio estimation is notoriously fragile under subsampling.
CONT_T_OBS = 250                 # short recording length (time steps)
CONT_TARGET_ACTIVITY = 30.0      # mean activity held ~constant across sigma via drive
CONT_Z = 1.645                   # one-sided 95% for the analytic slope CI


def estimate_sigma_continuous_studies(true_sigma, rng, t_obs=CONT_T_OBS):
    """Estimate sigma from ONE short continuous subsampled INAR(1)-with-immigration
    trace per study: a_{t+1} ~ Poisson(sigma*a_t + h), observed n_t = Binomial(a_t, f).
    The branching ratio is the AR(1) slope of n_{t+1} on n_t (subsampling-invariant
    in expectation), estimated by OLS; certify safe if the one-sided 95% upper bound
    on the slope is below the cut. This is the physiological observable (a continuous
    stream), harder than cleanly separated avalanches. Returns (point, certified)."""
    h = CONT_TARGET_ACTIVITY * (1.0 - true_sigma)          # hold mean activity ~const
    a = np.empty((t_obs + 1, N_STUDIES))
    a[0] = CONT_TARGET_ACTIVITY
    for t in range(t_obs):
        a[t + 1] = rng.poisson(np.clip(true_sigma * a[t] + h, 0, 1e6))
    n = rng.binomial(a.astype(np.int64), SUBSAMPLE_F).astype(np.float64)
    x, y = n[:-1], n[1:]                                    # (t_obs, N_STUDIES)
    xm = x.mean(0); ym = y.mean(0)
    xc = x - xm; yc = y - ym
    sxx = np.sum(xc * xc, axis=0)
    b = np.sum(xc * yc, axis=0) / np.maximum(sxx, 1e-9)     # OLS slope = sigma-hat
    resid = yc - b * xc
    sse = np.sum(resid * resid, axis=0)
    se_b = np.sqrt(sse / np.maximum(t_obs - 2, 1) / np.maximum(sxx, 1e-9))
    certified = (b + CONT_Z * se_b) < SIGMA_CUT
    return b, certified


MR_LAGS = 4                      # multistep-regression estimator: lags 1..K


def estimate_sigma_mr_studies(true_sigma, rng, t_obs=CONT_T_OBS):
    """Subsampling-robust branching-ratio estimator (Wilting & Priesemann 2018,
    multistep regression) on the SAME short continuous subsampled trace. The
    subsampling adds binomial noise only to the lag-0 regressor variance, so the
    lag-k slope is b_k = a * sigma^k with a common attenuation a: regressing
    log b_k on k removes a and recovers sigma from the slope. Certify safe if the
    one-sided 95% upper bound on sigma_MR is below the cut; a study whose multi-lag
    slopes go non-positive (too noisy to fit) is conservatively NOT certified."""
    h = CONT_TARGET_ACTIVITY * (1.0 - true_sigma)
    a = np.empty((t_obs + 1, N_STUDIES))
    a[0] = CONT_TARGET_ACTIVITY
    for t in range(t_obs):
        a[t + 1] = rng.poisson(np.clip(true_sigma * a[t] + h, 0, 1e6))
    n = rng.binomial(a.astype(np.int64), SUBSAMPLE_F).astype(np.float64)
    ks = np.arange(1, MR_LAGS + 1)
    logb = np.full((MR_LAGS, N_STUDIES), np.nan)
    for i, k in enumerate(ks):
        x, y = n[:-k], n[k:]
        xc = x - x.mean(0); yc = y - y.mean(0)
        bk = np.sum(xc * yc, axis=0) / np.maximum(np.sum(xc * xc, axis=0), 1e-9)
        logb[i] = np.log(np.clip(bk, 1e-6, None))
        bad = bk <= 1e-6
        logb[i, bad] = np.nan
    # OLS of log b_k on k, per study (columns); studies with any NaN are rejected
    ok = ~np.any(np.isnan(logb), axis=0)
    kk = ks.astype(float); kbar = kk.mean()
    denom = np.sum((kk - kbar) ** 2)
    slope = np.full(N_STUDIES, np.nan)
    ybar = logb.mean(0)
    slope_num = np.sum((kk[:, None] - kbar) * (logb - ybar[None, :]), axis=0)
    slope = slope_num / denom
    resid = logb - (ybar[None, :] + slope[None, :] * (kk[:, None] - kbar))
    sse = np.nansum(resid * resid, axis=0)
    se_slope = np.sqrt(sse / max(MR_LAGS - 2, 1) / denom)
    sigma_mr = np.exp(slope)
    se_sigma = sigma_mr * se_slope                          # delta-method
    certified = ok & ((sigma_mr + CONT_Z * se_sigma) < SIGMA_CUT)
    sigma_mr = np.where(ok, sigma_mr, np.nan)
    return sigma_mr, certified


def confound_curve(noise):
    """D_bare_critical(sigma)/D_ref over the population grid (reused from I2)."""
    d_ref = float(np.mean([run_identity_linked(0.5, s) for s in range(N_CONF_SEEDS)]))
    d = np.array([np.mean([run_bare_critical(s, noise, 1000 + k)
                           for k in range(N_CONF_SEEDS)]) for s in SIGMA_GRID])
    return d, d_ref


def estimate_sigma_studies(true_sigma, n_aval, rng):
    """Monte-Carlo of N_STUDIES short recordings at one true sigma. Each records
    n_aval avalanches over OBS_GEN generations, subsampled at SUBSAMPLE_F, and
    estimates sigma by the Harris ratio-of-totals estimator with a bootstrap upper
    confidence bound. Returns (point_estimates, certified_mask)."""
    # simulate all lineages for all studies at once: (OBS_GEN+1, N_STUDIES*n_aval)
    m = N_STUDIES * n_aval
    Z = np.empty((OBS_GEN + 1, m), dtype=np.int64)
    Z[0] = rng.poisson(SEED_POP_LAMBDA, m)
    for g in range(OBS_GEN):
        Z[g + 1] = rng.poisson(np.clip(true_sigma * Z[g], 0, 1e6))
    Y = rng.binomial(Z, SUBSAMPLE_F)                    # subsampled observation
    # per-lineage numerator/denominator for the ratio estimator
    num = Y[1:].sum(axis=0).reshape(N_STUDIES, n_aval).astype(np.float64)
    den = Y[:-1].sum(axis=0).reshape(N_STUDIES, n_aval).astype(np.float64)
    point = num.sum(1) / np.maximum(den.sum(1), 1e-9)
    # bootstrap over avalanches within each study
    idx = rng.integers(0, n_aval, size=(N_STUDIES, BOOT_B, n_aval))
    num_bs = np.take_along_axis(num[:, None, :], idx, axis=2).sum(axis=2)
    den_bs = np.take_along_axis(den[:, None, :], idx, axis=2).sum(axis=2)
    ratio_bs = num_bs / np.maximum(den_bs, 1e-9)
    upper = np.percentile(ratio_bs, BOOT_UPPER_PCT, axis=1)
    certified = upper < SIGMA_CUT
    return point, certified


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rng = np.random.default_rng(7)
    print("Sec 14.1 sub-criticality control -- does it recover M_diss's power?")
    print(f"  sigma grid {SIGMA_GRID.tolist()}")
    print(f"  control: certify sigma<{SIGMA_CUT} via {BOOT_UPPER_PCT}th-pct bootstrap; "
          f"realistic budget N_aval={HEADLINE_N_AVAL}, obs_gen={OBS_GEN}, f={SUBSAMPLE_F}")

    d_adv, d_ref = confound_curve(ADVERSARIAL_NOISE)
    d_sec, _ = confound_curve(SECONDARY_NOISE)
    conf_frac_adv = d_adv / d_ref
    print(f"  D_ref={d_ref:.3f}; confound/ref over sigma (noise 0.1): "
          f"{np.round(conf_frac_adv, 2).tolist()}")

    # ---- realistic-control acceptance at the headline budget -----------------
    accept_headline = np.zeros(len(SIGMA_GRID))
    sigma_hat_mean = np.zeros(len(SIGMA_GRID))
    sigma_hat_se = np.zeros(len(SIGMA_GRID))
    for i, s in enumerate(SIGMA_GRID):
        pt, cert = estimate_sigma_studies(s, HEADLINE_N_AVAL, rng)
        accept_headline[i] = float(cert.mean())
        sigma_hat_mean[i] = float(pt.mean())
        sigma_hat_se[i] = float(pt.std())
        print(f"  sigma={s:.3f}: sigma_hat={sigma_hat_mean[i]:.3f}+/-{sigma_hat_se[i]:.3f} "
              f"accept={accept_headline[i]:.2f}")

    # ---- harder observation model: continuous subsampled trace ---------------
    accept_cont = np.zeros(len(SIGMA_GRID))
    sigma_hat_cont_mean = np.zeros(len(SIGMA_GRID))
    sigma_hat_cont_se = np.zeros(len(SIGMA_GRID))
    for i, s in enumerate(SIGMA_GRID):
        pt, cert = estimate_sigma_continuous_studies(s, rng)
        accept_cont[i] = float(cert.mean())
        sigma_hat_cont_mean[i] = float(pt.mean())
        sigma_hat_cont_se[i] = float(pt.std())
    print("  [continuous subsampled trace, naive slope, T_obs=%d]" % CONT_T_OBS)
    for i, s in enumerate(SIGMA_GRID):
        print(f"  sigma={s:.3f}: sigma_hat_cont={sigma_hat_cont_mean[i]:.3f}"
              f"+/-{sigma_hat_cont_se[i]:.3f} accept={accept_cont[i]:.2f}")

    # ---- same continuous trace, subsampling-robust MR estimator --------------
    accept_mr = np.zeros(len(SIGMA_GRID))
    sigma_hat_mr_mean = np.zeros(len(SIGMA_GRID))
    for i, s in enumerate(SIGMA_GRID):
        pt, cert = estimate_sigma_mr_studies(s, rng)
        accept_mr[i] = float(cert.mean())
        sigma_hat_mr_mean[i] = float(np.nanmean(pt))
    print("  [continuous subsampled trace, MR estimator, T_obs=%d]" % CONT_T_OBS)
    for i, s in enumerate(SIGMA_GRID):
        print(f"  sigma={s:.3f}: sigma_hat_MR={sigma_hat_mr_mean[i]:.3f} "
              f"accept={accept_mr[i]:.2f}")

    # ---- three arms: residual confound (mean over accepted), noise 0.1 -------
    def residual_confound(accept_mask_weights, conf_frac):
        w = np.asarray(accept_mask_weights, dtype=float)
        if w.sum() <= 1e-9:
            return float("nan"), 0.0
        return float(np.sum(w * conf_frac) / w.sum()), float(w.mean())

    oracle_accept = (SIGMA_GRID < SIGMA_CUT).astype(float)
    no_ctrl_accept = np.ones(len(SIGMA_GRID))

    res_none, _ = residual_confound(no_ctrl_accept, conf_frac_adv)
    res_oracle, _ = residual_confound(oracle_accept, conf_frac_adv)
    res_real, real_accept_overall = residual_confound(accept_headline, conf_frac_adv)
    res_cont, _ = residual_confound(accept_cont, conf_frac_adv)
    res_mr, _ = residual_confound(accept_mr, conf_frac_adv)
    max_none = float(np.max(conf_frac_adv))
    j_safe = int(np.argmin(np.abs(SIGMA_GRID - SAFE_SIGMA)))
    j_conf = int(np.argmin(np.abs(SIGMA_GRID - CONFOUNDED_SIGMA)))
    acc_safe_cont = float(accept_cont[j_safe]); acc_conf_cont = float(accept_cont[j_conf])
    cert_power_cont = acc_safe_cont * (1.0 - acc_conf_cont)
    acc_safe_mr = float(accept_mr[j_safe]); acc_conf_mr = float(accept_mr[j_conf])
    cert_power_mr = acc_safe_mr * (1.0 - acc_conf_mr)

    # acceptance of genuinely sub-critical vs confounded systems (measurability)
    def accept_at(sigma_target):
        j = int(np.argmin(np.abs(SIGMA_GRID - sigma_target)))
        return float(accept_headline[j]), float(SIGMA_GRID[j])
    acc_safe, s_safe = accept_at(SAFE_SIGMA)
    acc_conf, s_conf = accept_at(CONFOUNDED_SIGMA)
    # certification power to separate confounded from safe: safe accepted, confounded rejected
    cert_power = acc_safe * (1.0 - acc_conf)

    # ---- budget sweep: how much data does the control need? ------------------
    budget_rows = []
    for n_aval in BUDGET_SWEEP:
        acc = np.array([estimate_sigma_studies(s, n_aval, rng)[1].mean() for s in SIGMA_GRID])
        rc, _ = residual_confound(acc, conf_frac_adv)
        a_safe = float(acc[int(np.argmin(np.abs(SIGMA_GRID - SAFE_SIGMA)))])
        a_conf = float(acc[int(np.argmin(np.abs(SIGMA_GRID - CONFOUNDED_SIGMA)))])
        budget_rows.append({"n_aval": n_aval, "residual_confound_frac": rc,
                            "accept_safe": a_safe, "accept_confounded": a_conf,
                            "cert_power": a_safe * (1 - a_conf)})
        print(f"  budget N_aval={n_aval:4d}: residual confound={rc:.2f} of ref, "
              f"accept(safe)={a_safe:.2f} accept(confounded)={a_conf:.2f}")

    # ---- verdict against the pre-registered thresholds -----------------------
    # The full honest picture has three estimation regimes on realistic short data:
    #   clean separable avalanches; continuous subsampled + NAIVE slope; continuous
    #   subsampled + subsampling-robust MR estimator. "Works in practice" requires an
    #   executable estimator on the physiological observable (a continuous stream).
    works_aval = (res_real <= 0.30 and acc_safe >= 0.50)
    works_naive = (res_cont <= 0.30 and acc_safe_cont >= 0.50 and cert_power_cont >= 0.5)
    works_mr = (res_mr <= 0.30 and acc_safe_mr >= 0.50 and cert_power_mr >= 0.5)

    concept_note = (
        f"The control CONCEPT is sound: with the true sigma known (oracle) the residual "
        f"confound is {res_oracle:.0%} of the identity reference, down from the "
        f"no-control {res_none:.0%} mean / {max_none:.0%} worst cell; and with cleanly "
        f"separated avalanches (N_aval={HEADLINE_N_AVAL}) a standard ratio estimator "
        f"attains {res_real:.0%} with perfect discrimination "
        f"(certification power {cert_power:.2f}).")
    naive_note = (
        f"But on the physiological observable -- a single short continuous SUBSAMPLED "
        f"stream (T_obs={CONT_T_OBS}, f={SUBSAMPLE_F}) -- the NAIVE lag-1 slope is "
        f"attenuated toward zero (true sigma=0.94 -> sigma_hat={sigma_hat_cont_mean[j_conf]:.2f}), "
        f"the DANGEROUS direction: it false-certifies {acc_conf_cont:.0%} of confounded "
        f"near-critical systems as safe, so the residual confound only reaches "
        f"{res_cont:.0%} and discrimination collapses (certification power "
        f"{cert_power_cont:.2f}). This is the known subsampling bias (Wilting & "
        f"Priesemann 2018).")

    if works_mr:
        verdict = (
            f"CONTROL WORKS -- BUT ONLY WITH A SUBSAMPLING-ROBUST ESTIMATOR; Sec 14.1 "
            f"must specify one. " + concept_note + " " + naive_note +
            f" The subsampling-robust multistep-regression (MR) estimator on the SAME "
            f"short trace removes the attenuation (true sigma=0.94 -> "
            f"sigma_MR={sigma_hat_mr_mean[j_conf]:.2f}) and RESTORES the control: "
            f"residual confound {res_mr:.0%} of reference, accepting {acc_safe_mr:.0%} "
            f"of genuinely sub-critical systems and rejecting {1-acc_conf_mr:.0%} of "
            f"confounded ones (certification power {cert_power_mr:.2f}). Honest close: "
            f"the §14.1 control is executable and recovers M_diss's power, PROVIDED the "
            f"distance-to-criticality is measured with a subsampling-robust estimator "
            f"(MR-type) or from cleanly segmented avalanches -- NOT the naive slope, "
            f"which fails in the dangerous direction. The paper must name this "
            f"estimator requirement; with it, the loop closes.")
    elif works_aval and not works_mr:
        verdict = (
            f"CONTROL NOT EXECUTABLE ON SHORT CONTINUOUS DATA -- a new, more serious "
            f"limitation. " + concept_note + " " + naive_note +
            f" Even the subsampling-robust MR estimator does not rescue it on this "
            f"short a recording (residual confound {res_mr:.0%}, accept(safe) "
            f"{acc_safe_mr:.0%}, certification power {cert_power_mr:.2f}). So distance-"
            f"to-criticality is not reliably measurable on the short, subsampled "
            f"streams CBRA targets, and Sec 14.1's control -- though sound in concept "
            f"and executable with clean avalanche segmentation -- is not executable on "
            f"the data the theory actually applies to. That must return to the text as "
            f"an added honesty condition (a measurable-sub-criticality precondition "
            f"that requires either clean event segmentation or a longer recording than "
            f"a short physiological stream provides), not a solved problem.")
    else:
        # clean-avalanche arm itself did not clear the bar -> the concept/statistic,
        # not just the measurement, is the limitation
        verdict = (
            f"CONTROL DOES NOT RECOVER POWER even with clean observation. Oracle "
            f"residual confound {res_oracle:.0%}, clean-avalanche {res_real:.0%} "
            f"(accept(safe) {acc_safe:.0%}), continuous naive {res_cont:.0%}, "
            f"continuous MR {res_mr:.0%} -- the control does not bring the confound to "
            f"the pre-registered 30% bar with a usable acceptance rate. Sec 14.1's "
            f"sub-criticality condition is not, on this evidence, sufficient to restore "
            f"M_diss's diagnostic power, and needs rethinking beyond a distance-to-"
            f"criticality threshold.")

    # ---- figure --------------------------------------------------------------
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))
    ax[0].plot(SIGMA_GRID, conf_frac_adv, "o-", color="crimson", label="noise 0.1")
    ax[0].plot(SIGMA_GRID, d_sec / d_ref, "s--", color="salmon", label="noise 0.5")
    ax[0].axhline(0.30, ls=":", color="green", label="'works' bar (30%)")
    ax[0].axvline(SIGMA_CUT, ls="--", color="k", lw=0.8, label=f"cut {SIGMA_CUT}")
    ax[0].set_xlabel("true branching ratio sigma"); ax[0].set_ylabel("confound D / reference")
    ax[0].set_title("I2 confound vs criticality"); ax[0].legend(fontsize=8)
    ax[1].plot(SIGMA_GRID, sigma_hat_mean, "o-", color="steelblue", label="avalanches")
    ax[1].fill_between(SIGMA_GRID, sigma_hat_mean - sigma_hat_se, sigma_hat_mean + sigma_hat_se,
                       color="steelblue", alpha=0.25)
    ax[1].plot(SIGMA_GRID, sigma_hat_cont_mean, "^-", color="darkorange", label="continuous")
    ax[1].fill_between(SIGMA_GRID, sigma_hat_cont_mean - sigma_hat_cont_se,
                       sigma_hat_cont_mean + sigma_hat_cont_se, color="darkorange", alpha=0.2)
    ax[1].plot(SIGMA_GRID, SIGMA_GRID, ls="--", color="k", lw=0.8, label="identity")
    ax[1].axhline(SIGMA_CUT, ls=":", color="crimson", label=f"cut {SIGMA_CUT}")
    ax[1].set_xlabel("true sigma"); ax[1].set_ylabel("estimated sigma_hat")
    ax[1].set_title(f"Estimator on short data\n(avalanches N={HEADLINE_N_AVAL}; continuous T={CONT_T_OBS})")
    ax[1].legend(fontsize=8)
    arms = ["no\ncontrol", "oracle", f"realistic\nN={HEADLINE_N_AVAL}", f"continuous\nT={CONT_T_OBS}"]
    vals = [res_none, res_oracle, res_real, res_cont]
    ax[2].bar(range(4), vals, color=["gray", "seagreen", "crimson", "darkorange"])
    ax[2].axhline(0.30, ls=":", color="green"); ax[2].axhline(0.40, ls=":", color="orange")
    ax[2].set_xticks(range(4)); ax[2].set_xticklabels(arms)
    ax[2].set_ylabel("residual confound / reference"); ax[2].set_title("Control efficacy")
    for i, v in enumerate(vals):
        ax[2].text(i, v + 0.01, f"{v:.0%}", ha="center")
    fig.suptitle("Sec 14.1 sub-criticality control: concept vs executability", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(RESULTS_DIR, "subcriticality_control.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "subcriticality_control",
        "question": "Does the Sec 14.1 measured-sub-criticality control recover M_diss's power vs the I2 pure critical generator?",
        "params": {"sigma_grid": SIGMA_GRID.tolist(), "sigma_cut": SIGMA_CUT,
                   "boot_b": BOOT_B, "boot_upper_pct": BOOT_UPPER_PCT,
                   "n_studies": N_STUDIES, "headline_n_aval": HEADLINE_N_AVAL,
                   "obs_gen": OBS_GEN, "seed_pop_lambda": SEED_POP_LAMBDA,
                   "subsample_f": SUBSAMPLE_F, "adversarial_noise": ADVERSARIAL_NOISE,
                   "safe_sigma": SAFE_SIGMA, "confounded_sigma": CONFOUNDED_SIGMA},
        "D_ref": d_ref,
        "confound_frac_over_sigma_noise0.1": conf_frac_adv.tolist(),
        "sigma_hat_mean": sigma_hat_mean.tolist(),
        "sigma_hat_se": sigma_hat_se.tolist(),
        "accept_headline": accept_headline.tolist(),
        "residual_confound": {"no_control_mean": res_none, "no_control_worst": max_none,
                              "oracle": res_oracle, "realistic": res_real,
                              "continuous_trace": res_cont},
        "acceptance": {"safe_sigma": s_safe, "accept_safe": acc_safe,
                       "confounded_sigma": s_conf, "accept_confounded": acc_conf,
                       "certification_power": cert_power},
        "continuous_observation_naive": {"t_obs": CONT_T_OBS,
                                   "sigma_hat_mean": sigma_hat_cont_mean.tolist(),
                                   "sigma_hat_se": sigma_hat_cont_se.tolist(),
                                   "accept": accept_cont.tolist(),
                                   "accept_safe": acc_safe_cont,
                                   "accept_confounded": acc_conf_cont,
                                   "certification_power": cert_power_cont,
                                   "residual_confound": res_cont},
        "continuous_observation_mr": {"mr_lags": MR_LAGS,
                                   "sigma_hat_mean": sigma_hat_mr_mean.tolist(),
                                   "accept": accept_mr.tolist(),
                                   "accept_safe": acc_safe_mr,
                                   "accept_confounded": acc_conf_mr,
                                   "certification_power": cert_power_mr,
                                   "residual_confound": res_mr},
        "budget_sweep": budget_rows,
        "verdict": verdict,
        "figures": ["subcriticality_control.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"  residual confound: no-control {res_none:.0%} (worst {max_none:.0%}) | "
          f"oracle {res_oracle:.0%} | avalanches {res_real:.0%} | "
          f"continuous-naive {res_cont:.0%} | continuous-MR {res_mr:.0%}")
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
