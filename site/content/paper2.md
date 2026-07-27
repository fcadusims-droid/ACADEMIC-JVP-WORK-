## The claim in one paragraph

CBRA is a strict *eliminative* statistical protocol for asking whether a complex
biological state transition — emergence from anaesthesia, say — requires
organizational variables that live on the active boundary of the system and are not
absorbed by a strong operational model of its measured dynamics. It is conditional
and falsifiable throughout. It is never offered as evidence that living tissue
implements anything, and it is built so that a clean negative is not merely possible
but expected unless a structured boundary residual survives an adversarial sequence
of controls.

## The conditional question

*If* an identity-indexed persistence channel were materially instantiated in living
tissue, what would the tissue have to implement, and what residual structure would
have to be measurable after the strongest available operational null had already
absorbed everything it could?

The paper depends conceptually on Paper 1 — it borrows Class G and the consistency
contract *I* — but not on the success of any biological mechanism, and nothing flows
back the other way.

## Four corrections to the naive programme

**The Mori–Zwanzig category error.** The physical boundary does not interact with the
mathematical projection operator. It is folded into the classical microphysical
substrate, and its biological role is to alter the Liouville generator of that
substrate *before* projection, so that metabolic expenditure keeps the memory kernel
from collapsing.

**Cardio-interoceptive variables are proxies, not constitutive invariants.** The
heart-transplant case forces the reclassification — and the reclassification turns
the transplant from a refutation into a confirmation. The self survives organ
replacement, but the thermodynamic cost of re-anchoring and the texture of
homeostasis change radically.

**The computational demonstration is demoted** from a false claim of spontaneous
emergence to a low-dimensional syntactic-consistency proof: the mode separation and
geometric constraints were injected by hand, and the demonstration shows only that
the grammar is algorithmically executable.

**The estimator requirement is named.** Subsampled branching estimators are biased,
and §14.1 now states which family of estimator the protocol requires rather than
leaving the choice to the implementer.

## The pre-registered negative

The paper's title carries it: *and a Pre-Registered Negative on Their Present
Availability*. The positive arm was not abandoned for lack of interest; it was halted
by a gate written before the run.

A dataset-viability search (`dataset_viability_gate`) found exactly one public corpus
with the three properties the protocol needs — concurrent cardiac and neural
recording, a recovery-versus-non-recovery contrast, and records long enough to
estimate on. The gating experiment on that corpus (`cbra_boundary_residual`) then
asked whether the interoceptive boundary residual beats a linear-Gaussian null. The
pre-registration said the track halts below 60% of a pilot. It reached 29%. The
downstream experiments were **not run**, and the paper declares its positive arm not
currently executable on public data.

En route, a fixed-threshold R-peak detector was found inadequate on heterogeneous
ICU ECG — 55 peaks on a 118-minute record. Replacing it with an adaptive detector
moved the result from a spuriously higher 42% to a clearer 29%. The correction made
the paper's own negative *stronger*, and was applied anyway, because the detector was
broken.

## What survives

The eliminative arm. Simulation studies show the protocol is executable but demanding
— imperfect matching inflates the false-positive rate three- to sevenfold
independently of sample size (`dissociation_power_analysis`), and a genuinely
critical generator with no identity mechanism reproduces the gating differential near
criticality (`criticality_sweep`, `dissociation_confound`), which is why the paper's
defensible claim is eliminative rather than detective. A sub-criticality control was
added because the confound analysis demanded one (`subcriticality_control`).
