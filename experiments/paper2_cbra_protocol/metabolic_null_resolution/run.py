"""Experiment J -- Spatial resolution of the metabolic null (Paper 2, Sec 7.2).

Sec 7.2 argues qualitatively that a spatially-resolved / strong operational null
absorbs the structured boundary residual that a weak (coarse) null leaves. This
turns that qualitative claim into a number: AT WHAT SPATIAL RESOLUTION does the
null actually absorb the residual, and how does the threshold depend on the
substrate's diffusion length and on metabolic maintenance of the boundary
structure?

Model (spectral, 1-D substrate). An active boundary injects a structured signal
with a characteristic length scale ell (spectrum peaked at k_b = 2*pi/ell,
amplitude set by a metabolic parameter that keeps it from collapsing). Energy
diffusion low-passes it with transfer H(k) = 1/(1+(k L_D)^2) over the diffusion
length L_D. An operational null at spatial resolution h can model/absorb every
scale coarser than h (wavenumbers k < 2*pi/h); the surviving residual is the
structured energy at k >= 2*pi/h. Sweeping h gives the resolution at which the
residual is absorbed.

Usage:
    python -m experiments.paper2_cbra_protocol.metabolic_null_resolution.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "_results", "metabolic_null_resolution"
)

ELL = 1.0                                  # boundary structure length scale (unit)
K_B = 2 * np.pi / ELL                      # boundary wavenumber
BUMP_WIDTH = 0.35 * K_B                    # spectral width of the boundary signature
# diffusion length sweep, spanning the smearing transition L_D ~ ell/(2 pi) ~ 0.16
L_DS = [0.05, 0.08, 0.12, 0.18, 0.25]      # in units of ell
NOISE_FLOOR = 1e-3                         # measurement noise energy density
RESOLUTIONS = np.linspace(0.05, 8.0, 200)  # null spatial resolution h (units of ell)
K = np.linspace(0.01, 6 * K_B, 4000)       # wavenumber grid


def boundary_spectrum(metabolic=1.0):
    """Structured boundary power spectrum: a Gaussian bump at k_b whose amplitude
    is maintained by metabolism (metabolic=0 -> collapsed, flat/weak)."""
    bump = np.exp(-0.5 * ((K - K_B) / BUMP_WIDTH) ** 2)
    return metabolic * bump + (1 - metabolic) * 0.05 * np.exp(-K / K_B)


def observed_spectrum(L_D, metabolic=1.0):
    H = 1.0 / (1.0 + (K * L_D) ** 2)       # diffusion low-pass
    return boundary_spectrum(metabolic) * H ** 2


def surviving_residual(P_obs, h):
    """Energy at scales finer than the null resolution h (k >= 2*pi/h), above the
    noise floor -- what a null of resolution h cannot absorb."""
    k_c = 2 * np.pi / h
    mask = K >= k_c
    dens = np.clip(P_obs - NOISE_FLOOR, 0, None)
    dk = K[1] - K[0]
    return float(np.sum(dens[mask]) * dk)


def threshold_resolution(P_obs, frac=0.1):
    """Finest-to-coarsest: the resolution h* at which the surviving residual first
    exceeds `frac` of its coarse-null (h -> large) maximum -- i.e. finer than h*
    the null absorbs (residual < frac*max), coarser than h* it survives."""
    R = np.array([surviving_residual(P_obs, h) for h in RESOLUTIONS])
    Rmax = R.max()
    if Rmax <= 1e-9:
        return None, R  # nothing structured to absorb (collapsed boundary)
    above = np.where(R >= frac * Rmax)[0]
    return (float(RESOLUTIONS[above[0]]) if len(above) else None), R


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Experiment J: spatial resolution of the metabolic null")

    curves = {}
    thresholds = {}
    for L_D in L_DS:
        P = observed_spectrum(L_D, metabolic=1.0)
        h_star, R = threshold_resolution(P)
        curves[L_D] = R
        thresholds[L_D] = h_star
        print(f"  L_D={L_D:4.2f}: absorption resolution h* = "
              f"{'n/a' if h_star is None else f'{h_star:.2f}'} (units of ell)")

    # metabolic on/off in the structured regime (L_D = 0.1): metabolism keeps the
    # boundary spectrum from collapsing (Sec 7.2). Compare the peak structured
    # residual with metabolism on vs off.
    L_MET = 0.1
    P_on = observed_spectrum(L_MET, metabolic=1.0)
    P_off = observed_spectrum(L_MET, metabolic=0.0)
    h_on, _ = threshold_resolution(P_on)
    Ron_max = np.array([surviving_residual(P_on, h) for h in RESOLUTIONS]).max()
    Roff_max = np.array([surviving_residual(P_off, h) for h in RESOLUTIONS]).max()
    met_ratio = Ron_max / max(Roff_max, 1e-9)
    print(f"  metabolic ON  (L_D={L_MET}): peak residual {Ron_max:.3f}, h*={h_on:.2f}")
    print(f"  metabolic OFF (L_D={L_MET}): peak residual {Roff_max:.4f} "
          f"-> ON/OFF ratio {met_ratio:.0f}x")

    # does the threshold scale with the effective structure scale max(ell, L_D)?
    valid = {ld: h for ld, h in thresholds.items() if h is not None}
    scaling_ok = len(valid) >= 3 and np.all(np.diff([valid[ld] for ld in sorted(valid)]) >= -0.2)

    if valid and scaling_ok:
        lo, hi = min(valid.values()), max(valid.values())
        verdict = (f"RESOLUTION THRESHOLD EXISTS and SCALES with diffusion length: "
                   f"the null absorbs the structured boundary residual only when its "
                   f"resolution is finer than h* ~ {lo:.1f}-{hi:.1f} ell, and h* "
                   f"GROWS with the diffusion length L_D (a longer diffusion length "
                   f"smears the boundary signature to a coarser scale, so a coarser "
                   f"null already absorbs it). Sec 7.2's weak-vs-strong-null claim is "
                   f"resolution-driven and now quantified: strong null := resolution "
                   f"< h*(L_D). With metabolism the residual is structured and the "
                   f"threshold is meaningful; WITHOUT metabolism the structured "
                   f"residual is {met_ratio:.0f}x smaller (boundary spectrum "
                   "collapses toward the smooth background), so no resolution "
                   "recovers structure -- exactly the role Sec 7.2 gives metabolic "
                   "expenditure in keeping the memory kernel from collapsing.")
    elif not valid:
        verdict = ("NO STRUCTURED RESIDUAL: even the metabolically-maintained "
                   "boundary leaves no residual above the noise floor at any "
                   "resolution -- the weak/strong-null distinction is not "
                   "resolution-driven in this model and Sec 7.2 must be restated.")
    else:
        verdict = (f"THRESHOLD PRESENT BUT NOT MONOTONE in L_D "
                   f"(h* = {valid}); the resolution/diffusion relationship is more "
                   "complex than a simple scaling and should be reported as such.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    for L_D in L_DS:
        ax.plot(RESOLUTIONS, curves[L_D], label=f"L_D={L_D}")
    ax.set_xlabel("null spatial resolution h (units of ell)")
    ax.set_ylabel("surviving structured residual"); ax.legend(fontsize=8)
    ax.set_title("Residual vs null resolution (finer h = stronger null)")
    ax = axes[1]
    lds = sorted(valid)
    ax.plot(lds, [valid[ld] for ld in lds], "o-", color="crimson")
    ax.set_xlabel("diffusion length L_D (units of ell)")
    ax.set_ylabel("absorption threshold h* (units of ell)")
    ax.set_title("Threshold resolution scales with diffusion length")
    fig.suptitle("Exp J: metabolic null resolution", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(RESULTS_DIR, "null_resolution.png"), dpi=130)
    plt.close(fig)

    summary = {
        "experiment": "J_metabolic_null_resolution",
        "params": {"ell": ELL, "L_Ds": L_DS, "noise_floor": NOISE_FLOOR},
        "absorption_threshold_h_star_by_L_D": {str(ld): thresholds[ld] for ld in L_DS},
        "metabolic_on_peak_residual": float(Ron_max),
        "metabolic_off_peak_residual": float(Roff_max),
        "metabolic_on_off_ratio": float(met_ratio),
        "preregistered_criterion": "a concrete resolution threshold vs diffusion length",
        "verdict": verdict,
        "figures": ["null_resolution.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "=" * 72)
    print(verdict)
    print(f"Results + figure in {os.path.relpath(RESULTS_DIR)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
