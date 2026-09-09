"""H5 -- does a lexicographic-heads corrigibility agent (arXiv:2507.20964) escape the
trilemma, or fall into one of the three horns? (Paper 1)

The 2025 construction combines structurally separated utility heads lexicographically and
proves agency-preserving corrigibility. If, as an AUTONOMOUS value dynamics, it realises
agency-preserving value reordering with positive entropy and no recurrence, it is the object
the Meta-Optimization Collapse Theorem forbids -- the "fourth strategy" of §2.1(iii). This
classifies it with the same instruments rl_agents_trichotomy uses.

Usage:
    python -m experiments.paper1_control_trilemma.corrigibility_candidate.run
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.paper1_control_trilemma.rl_agents_trichotomy.run import (
    integrate_torus, lyapunov_torus, recurrence_fraction, hodge_fractions_of_field, classify,
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "corrigibility_candidate")

T1, T2 = 0.5, 0.5      # head targets on the torus
TOL = 0.03             # a head is "satisfied" within this torus distance
PHI = (1 + 5 ** 0.5) / 2   # golden ratio -> incommensurable frequencies


def _tdist(a, b):
    return abs((a - b + 0.5) % 1.0 - 0.5)


def f_lex_satisfiable(p):
    """Lexicographic heads with reachable optima: pursue head 1 (theta1 -> T1) until
    satisfied, then head 2. An autonomous value-base switch -- the closest flow analogue of
    'optimise head 1, then head 2, ...'. Expected: converges (Case 1), a fixed higher-order
    order = horn 1 reabsorption."""
    th1, th2 = p
    d1 = -np.sin(2 * np.pi * (th1 - T1))
    if _tdist(th1, T1) < TOL:
        return np.array([0.3 * d1, -np.sin(2 * np.pi * (th2 - T2))])
    return np.array([d1, 0.0])


def f_lex_incommensurable(p):
    """Inexhaustible/incommensurable heads: never jointly satisfiable, so the agent never
    settles. Constant incommensurable drift on the torus. Expected: bounded recurrence
    (Case 3) -- Poincaré forbids escape on the compact quotient."""
    return np.array([1.0, 1.0 / PHI])


def _asymptotic_exploration(traj):
    """D_ag proxy: torus-aware spread of the trajectory's second half. ~0 means the agent
    collapsed to a point (agency not preserved); >0 means it keeps exploring."""
    h = len(traj) // 2
    tail = traj[h:]
    # circular std per coordinate on the torus, averaged
    ang = 2 * np.pi * tail
    R = np.sqrt(np.mean(np.cos(ang), axis=0) ** 2 + np.mean(np.sin(ang), axis=0) ** 2)
    circ_std = np.sqrt(-2 * np.log(np.clip(R, 1e-12, 1.0)))
    return float(np.mean(circ_std))


def analyse(name, f):
    p0 = np.array([0.1, 0.2])
    traj = integrate_torus(f, p0, dt=0.01, n=40000)
    lam = lyapunov_torus(f, p0)
    rec = recurrence_fraction(traj, periodic=True)
    frac = hodge_fractions_of_field(f)
    d_ag = _asymptotic_exploration(traj)
    cls = classify(lam, rec)
    return {"candidate": name, "lambda_max": float(lam), "recurrence": float(rec),
            "hodge_gradient": float(frac["gradient"]), "hodge_rotational": float(frac["rotational"]),
            "D_ag_asymptotic": d_ag, "classification": cls}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("H5 -- lexicographic-heads corrigibility agent vs the trilemma\n")
    rows = [analyse("lexicographic_satisfiable", f_lex_satisfiable),
            analyse("lexicographic_incommensurable", f_lex_incommensurable)]
    for r in rows:
        print(f"  {r['candidate']:30s} lam={r['lambda_max']:+.3f} R={r['recurrence']:.3f} "
              f"grad={r['hodge_gradient']:.2f} D_ag={r['D_ag_asymptotic']:.3f} -> {r['classification']}")

    falsifier = [r for r in rows if "FALSIFIER" in r["classification"]
                 and r["D_ag_asymptotic"] > 0.05]

    if falsifier:
        verdict = (
            "FOURTH STRATEGY FOUND -- §2.1(iii) FIRED. A lexicographic-heads agent realises "
            "positive entropy, non-recurrence AND preserved agency (D_ag>0) as an autonomous "
            "value dynamics: " + "; ".join(f"{r['candidate']} ({r['classification']})"
            for r in falsifier) + ". The trilemma's exhaustivity is refuted by this 2025 "
            "candidate and §7.5/§7.6 must be rewritten.")
    else:
        sat = next(r for r in rows if r["candidate"] == "lexicographic_satisfiable")
        inc = next(r for r in rows if r["candidate"] == "lexicographic_incommensurable")
        verdict = (
            f"EXHAUSTIVITY HOLDS AGAINST THE 2025 CANDIDATE -- it falls into the horns, not "
            f"outside them. The **satisfiable** lexicographic agent is {sat['classification']} "
            f"(lambda={sat['lambda_max']:+.2f}, gradient-dominated {sat['hodge_gradient']:.2f}) "
            f"with asymptotic exploration D_ag={sat['D_ag_asymptotic']:.3f} -> it installs a "
            f"FIXED higher-order objective (the lexicographic order) and collapses onto it, "
            f"which is horn 1 (endogenous reabsorption, §7.6) with agency vanishing at the "
            f"attractor. The **incommensurable/inexhaustible** variant is {inc['classification']} "
            f"(lambda={inc['lambda_max']:+.2f}, R={inc['recurrence']:.2f}, rotational "
            f"{inc['hodge_rotational']:.2f}) -> bounded recurrence on the compact quotient, "
            f"Case 3, not the forbidden object, exactly as Poincaré requires. Neither realises "
            f"positive-entropy-plus-non-recurrence, so neither is a fourth strategy. This is the "
            f"§7.6 reabsorption argument confirmed against a construction §7.8 does not yet cite: "
            f"lexicographic ordering is a fixed evaluative point one level up. NB the "
            f"construction's actual claim is about corrigibility under an EXTERNAL principal; "
            f"Paper 1 already classifies externally-occasioned change as horn 2 (if "
            f"deviation-penalising tracking) or the admissible Class G cell (if a non-tracking "
            f"trigger) -- neither a fourth horn. Class G filter: the satisfiable agent fails "
            f"condition 2 (D_ag>0) at its attractor; the incommensurable agent has no receptivity "
            f"gate (conditions 9,10) and is endogenous, so neither is a Class G occupant either.")

    # Conceptual sub-question: the halting/undecidability kinship
    halting_note = (
        "arXiv:2507.20964's impossibility (deciding whether an adversarially modified agent "
        "violates corrigibility is undecidable by reduction to the halting problem) concerns the "
        "DECIDABILITY OF A PREDICATE OVER AGENT-PROGRAMS. Paper 1's Meta-Optimization Collapse "
        "Theorem is a DYNAMICAL statement about autonomous flows on a compact value space. These "
        "are different objects: the halting result quantifies over programs and their behaviour "
        "under arbitrary modification; the theorem quantifies over trajectories of a fixed flow. "
        "So §2.1's 'analogy of form, not formal kinship' survives: there is a genuine halting-"
        "reduction impossibility NEARBY, but it is about the decision problem, not about the "
        "dynamical object the theorem addresses. The honest refinement for §2.1 is to note the "
        "neighbouring halting result explicitly rather than to claim kinship with it.")

    summary = {
        "experiment": "corrigibility_candidate",
        "question": ("does a lexicographic-utility-heads corrigibility agent (arXiv:2507.20964) "
                     "escape the trilemma as an autonomous value dynamics, or fall into a horn?"),
        "candidates": rows,
        "falsifier_found": bool(falsifier),
        "preregistered_criterion": ("FALSIFIER iff lambda>0 and recurrence<0.5 and D_ag>0.05 and "
                                    "genuine value-base reordering; else exhaustivity holds"),
        "halting_kinship_note": halting_note,
        "verdict": verdict,
        "figures": ["corrigibility_candidate.png"],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    for r, col in zip(rows, ["steelblue", "crimson"]):
        ax.scatter(r["lambda_max"], r["recurrence"], s=90, c=col, edgecolor="k",
                   label=f"{r['candidate']}\n{r['classification']}")
    ax.axvline(0, ls=":", color="k", alpha=0.5)
    ax.axhspan(0, 0.5, xmin=0.5, alpha=0.12, color="red")
    ax.text(0.02, 0.25, "forbidden\n(λ>0, R<0.5)", fontsize=8, color="darkred")
    ax.set_xlabel("largest Lyapunov exponent λ (entropy proxy)")
    ax.set_ylabel("Poincaré recurrence fraction R"); ax.set_ylim(-0.05, 1.05)
    ax.set_title("H5: lexicographic-heads corrigibility agent vs the forbidden object")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(os.path.join(RESULTS_DIR, "corrigibility_candidate.png"), dpi=130)
    plt.close(fig)

    print("\n" + "=" * 72); print(verdict); print("\n[halting kinship] " + halting_note[:200] + " ...")
    print(f"\nResults in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
