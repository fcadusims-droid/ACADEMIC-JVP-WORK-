# Submission readiness

## Paper 3 — *Kinematics of Geodesic Flow* — ready first

The most conventional and most complete of the three. Target: a methods venue in
signal processing or neuroinformatics.

**What a methods reviewer will check, and where it now stands.**

| Expected challenge | Status |
|---|---|
| "Why not an HMM / BOCPD / PELT?" | Answered with numbers: benchmarked against BOCPD, `ruptures` (PELT/BinSeg/Window), a 2-state Gaussian HMM and sliding-window *k*-means, on the same data and features. Localisation 10/15 vs the best baseline's 8/15 — reported as inside binomial noise, not as a demonstrated advantage. |
| "Your detector can't tell whether a transition exists." | Was true, and is fixed: detection AUC 0.23 → **0.81** by specifying the detection statistic (scale-normalised peak). At 0.81 the detector ranks 4th of 19 (itself against six baseline algorithms × three feature sets) — competitive, not superior; stated that way. |
| "You chose that repair on the same records that exposed the problem." | Correct, and answered rather than deferred: the committed statistic was applied **unchanged** to a paradigm not used to select it (eegmmidb eyes-open/closed, 16 subjects), bar fixed in advance at the same 0.70 → **AUC 0.82**. On the identical segments the old statistic scores **0.43**, sub-chance a second time, so the *failure* mechanism generalises alongside the fix — which is what the mechanistic diagnosis predicted and what single-corpus selection could not have shown. |
| "What does the geometry buy?" | The structural-vs-power dissociation: on a structural transition with power held constant it localises perfectly against the best power baseline's 0.75, and it is blind to a pure power change *by construction*. Both directions reported. |
| "Does it generalise?" | Two real paradigms (eyes-open/closed; Sleep-EDF), with the localisation limit characterised as paradigm-bounded rather than absolute. |
| "Sensitivity to hyperparameters / cost?" | Runtime per record reported alongside every baseline; the metric-choice trade-off (log-Euclidean vs square-root) is quantified including its weak-collapse cost (0.85 → 0.22). |
| "Is the code available?" | Installable package, CI on two Python versions, `CITATION.cff`, and `RELEASING.md` for a Zenodo DOI. |

**Remaining before submission** (author actions, not code): mint the Zenodo DOI
(`RELEASING.md`), and post a preprint to establish priority.

## Paper 1 — after Paper 3

Two viable framings, and the choice is strategic rather than scientific: philosophy of
action / analytic theology, or an alignment venue on the strength of §7.8.6 (the
trichotomy as a corrigibility result). The literature engagement (§7.8) and the Class G
satisfiability and independence results are the parts that were missing; both are now
in place, including the concessions (the thesis is narrowed to *unanchored* value
change, and the ten-condition count is discounted to an effective six).

## Paper 2 — Registered Report format

The natural home given what it now establishes: a data-requirements specification plus
a pre-registered executability negative. It should be submitted as a protocol/negative
result rather than as a findings paper, which is what the retitling already reflects.
