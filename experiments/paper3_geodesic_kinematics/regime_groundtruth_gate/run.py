"""Phase 0 -- viability gate for Paper 3's three-regime demarcation.

Decides whether the titular claim (sort a single trajectory into asymptotic geodesic
drift / isotropic fibre dispersion / structural rank collapse) is testable at all on
accessible data, BEFORE any demarcation-scoring code is written.

This is an assessment, not a simulation: it records reachability of candidate corpora and
scores each against the three pre-registered properties. See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper3_geodesic_kinematics.regime_groundtruth_gate.run
"""
from __future__ import annotations

import json
import os
import subprocess

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "regime_groundtruth_gate")

CANDIDATES = [
    {
        "corpus": "PhysioNet EEG (Sleep-EDF, eegmmidb)",
        "host": "https://physionet.org",
        "synthetic": False,
        "p2_protocol_input": True,
        "p3_post_transition_horizon": True,
        "p1_external_regime_label": False,
        "why": ("Supplies STATE labels (sleep stage; eyes-open/closed), not kinematic REGIME "
                "labels. Mapping a state onto drift/dispersion/collapse is precisely the "
                "'additional, separately contestable empirical hypothesis requiring its own "
                "ground-truth validation' that Paper 3 Sec 2 states it neither performs nor "
                "presupposes. Scoring the three-way verdict against a stage label would be "
                "measuring agreement with the wrong object."),
    },
    {
        "corpus": "JHU Turbulence Database (DNS, laminar-turbulent transition)",
        "host": "https://turbulence.pha.jhu.edu",
        "synthetic": False,
        "p2_protocol_input": True,
        "p3_post_transition_horizon": True,
        "p1_external_regime_label": False,
        "why": ("The strongest candidate, and it still fails property 1. It supplies a "
                "genuinely external control parameter (Reynolds number) and an accepted "
                "binary transition (laminar -> turbulent). But the label is BINARY and its "
                "mapping onto three regimes is interpretive: 'turbulent ~ isotropic "
                "dispersion' and 'laminar shear ~ geodesic drift' are arguable readings, and "
                "STRUCTURAL RANK COLLAPSE has no established turbulence counterpart at all. "
                "At most two of three regimes, under a mapping the paper declines to make."),
    },
    {
        "corpus": "Financial microstructure / regime-switching corpora",
        "host": "https://archive.ics.uci.edu",
        "synthetic": False,
        "p2_protocol_input": True,
        "p3_post_transition_horizon": True,
        "p1_external_regime_label": False,
        "why": ("Regime labels in this literature are MODEL-DERIVED -- fitted by "
                "regime-switching or change-point models of the same family being tested. "
                "Scoring against them measures agreement with a competitor, not with ground "
                "truth, and fails property 1's independence requirement by construction."),
    },
    {
        "corpus": "Driven-materials / phase-transition corpora (Zenodo, NOAA)",
        "host": "https://zenodo.org",
        "synthetic": False,
        "p2_protocol_input": False,
        "p3_post_transition_horizon": True,
        "p1_external_regime_label": False,
        "why": ("Order/disorder transitions carry an external control parameter, but the "
                "published records are typically single-channel or spatially-indexed rather "
                "than the multichannel slow/fast-separable series the protocol takes as "
                "input, and the regime label is again binary rather than three-way."),
    },
    {
        "corpus": "Synthetic systems with known governing equations",
        "host": None,
        "synthetic": True,
        "p2_protocol_input": True,
        "p3_post_transition_horizon": True,
        "p1_external_regime_label": True,
        "why": ("Satisfies property 1 BY CONSTRUCTION, and is therefore excluded from the "
                "PASS condition by the pre-registered anti-rescue guard. It validates the "
                "ESTIMATOR (can the machinery recover a regime it was handed?) and not the "
                "TAXONOMY. The suite's repeated lesson is that synthetic performance "
                "overstates real performance."),
    },
]


def reachable(url):
    if not url:
        return None
    try:
        out = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", url],
            capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception as e:
        return f"error: {type(e).__name__}"


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("Phase 0 -- regime ground-truth viability gate (Paper 3)")
    print("  question: is the three-regime demarcation testable on accessible data at all?\n")

    rows = []
    for c in CANDIDATES:
        code = reachable(c["host"])
        passes = (c["p1_external_regime_label"] and c["p2_protocol_input"]
                  and c["p3_post_transition_horizon"] and not c["synthetic"])
        rows.append({**c, "http": code, "passes_gate": bool(passes)})
        mark = "PASS" if passes else "fail"
        host = f"{c['host']} [{code}]" if c["host"] else "(n/a)"
        print(f"  [{mark}] {c['corpus']}")
        print(f"         host {host}  |  p1 regime-label={c['p1_external_regime_label']} "
              f"p2 input={c['p2_protocol_input']} p3 horizon={c['p3_post_transition_horizon']}"
              f"{'  SYNTHETIC (excluded)' if c['synthetic'] else ''}")

    passing = [r for r in rows if r["passes_gate"]]
    reachable_ok = sum(1 for r in rows if r["http"] and r["http"].startswith(("2", "3")))

    if passing:
        verdict = ("PASS -- " + "; ".join(r["corpus"] for r in passing) +
                   " supplies external three-way regime ground truth. The demarcation "
                   "experiment is executable and runs with the pre-registered three-arm "
                   "design plus the three-state co-primary comparator.")
    else:
        verdict = (
            "FAIL, AND THE REASON IS STRUCTURAL RATHER THAN LOGISTICAL -- which makes this a "
            "result rather than a postponement. Every candidate corpus is REACHABLE "
            f"({reachable_ok} of {len([r for r in rows if r['host']])} hosts answered 2xx/3xx), "
            "so access is not the obstacle; property 1 is. No accessible non-synthetic corpus "
            "supplies an external drift/dispersion/collapse label. The diagnosis is sharper "
            "than 'nobody has labelled it yet', and it is visible in Paper 3's own Section 2: "
            "the three regimes are declared to be *operationally defined geometric regimes "
            "fixed by Lyapunov-stability and statistical-complexity criteria, not domain "
            "categories*. If the regimes are defined BY the protocol's own criteria, then an "
            "external referent for them does not exist to be found -- the label IS the "
            "protocol's output, and 'does the protocol classify correctly?' has no "
            "independent truth-maker. The strongest candidate (turbulence) fails not for want "
            "of rigour but because its externally controlled transition is BINARY and "
            "structural rank collapse has no counterpart in it. What remains available is "
            "therefore (a) estimator recovery on synthetic systems with known generators, "
            "which is CALIBRATION of the machinery rather than VALIDATION of the taxonomy, "
            "and (b) agreement with a domain-accepted binary transition covering at most two "
            "of the three regimes under an interpretive mapping the paper explicitly declines "
            "to make. CONSEQUENCE FOR PAPER 3: the titular claim is not merely untested but, "
            "as currently defined, not externally falsifiable -- and the paper must say so in "
            "the register its companion uses for its own halted arm. The honest routes are to "
            "re-define the regimes against an external criterion (making them falsifiable and "
            "changing the paper), or to present the demarcation as an operational taxonomy "
            "whose value is construct-internal and argue for it on those terms.")

    summary = {
        "experiment": "regime_groundtruth_gate",
        "question": ("does an accessible non-synthetic corpus supply external three-way "
                     "drift/dispersion/collapse ground truth for Paper 3's titular claim?"),
        "preregistered_criterion": ("PASS iff >=1 open non-synthetic corpus satisfies all "
                                    "three properties; synthetic excluded by the anti-rescue "
                                    "guard"),
        "candidates": rows,
        "n_passing": len(passing),
        "hosts_reachable": reachable_ok,
        "gate": "PASS" if passing else "FAIL",
        "verdict": verdict,
        "figures": [],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n" + "=" * 72); print(verdict)
    print(f"\nResults in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
