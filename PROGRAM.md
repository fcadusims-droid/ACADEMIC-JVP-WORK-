# The Conditional Program — how the three papers relate, and why they are kept apart

This document exists because a review of the trilogy found the connective tissue nowhere
written down: each paper states its own scope, but the *program* that motivates all three —
and the precise sense in which they do and do not depend on one another — lived only in the
author's head. Putting it in its own file, rather than inside any of the three papers, is
deliberate: the papers are logically independent and must remain so, and a unifying preface
embedded in one of them would manufacture a dependency the work does not have. This is the
optional reading that connects them; it is not load-bearing for any of them.

## The one conditional that ties them together

The program is a single conditional, and every paper occupies one clause of it:

> **IF** there is such a thing as an agency-preserving transformation of an agent's own
> top-level evaluative structure — conversion, metanoia, a genuine reordering of what the
> agent values, undergone without the agent being overwritten — **THEN** (i) it must have a
> particular formal *type signature*, which classical control theory cannot render (Paper 1);
> (ii) if such a thing were realized in living tissue, a specific *eliminative statistical
> protocol* would be required to distinguish it from cheaper explanations (Paper 2); and
> (iii) demarcating the geometric *regimes* of any such transition from a single trajectory
> would require a specific *inference method* on a curved state space (Paper 3).

The antecedent is supplied by philosophy and theology and is contested there; the program
makes no claim that the antecedent is true. Each paper discharges one clause of the
consequent, and each is written so that it survives the antecedent being false.

- **Paper 1** argues the *negative* half of clause (i): an autonomous, bounded value dynamics
  read through a bounded identity contract cannot realize the transformation (by Poincaré recurrence
  only for states typical of an invariant measure; for dissipative dynamics the transients are
  excluded by an interpretive argument, not a theorem), so if it occurs
  it is externally occasioned — relative to where the observer draws the system boundary, a
  pragmatic choice of the same kind as the identity contract; and it names **Class G** as the residual admissibility profile
  — the type signature the transformation would have to satisfy. This is a conceptual
  contribution: it licenses *sorting* (which cell an account of transformation occupies) and
  *costing* (the agency price of exogenous forcing), and one conditional dynamical result. It
  licenses no claim that any such transformation occurs.
- **Paper 2** builds clause (ii): the CBRA eliminative protocol, borrowing Class G and the
  contract *I* from Paper 1 as *definitions* only. It is a pre-registered negative — its
  positive arm halted at its own stopping rule on the one viable public corpus — so what it
  contributes is the protocol, the gate it failed, and the conditions under which it could
  run.
- **Paper 3** was meant to build clause (iii): a single-trajectory demarcation method on the
  covariance manifold. That method did not survive testing, and Paper 3 is now the
  methodological record of how it looked validated and was not (five traps), with the
  original proposal kept as a draft. It is a methods paper, and a Phase-0 gate found its titular three-regime claim is
  not, as currently defined, externally falsifiable. It borrows *nothing* from the other two
  and is offered on its own terms as time-series methodology.

## The dependency runs one way, and only through definitions

```
        Paper 1  (Class G, contract I)  ──used-as-definitions-by──▶  Paper 2
        Paper 1 ──── no dependency ────────────────────────────────  Paper 3
        Paper 2 ──── no dependency ────────────────────────────────  Paper 3
```

Paper 2 borrows Class G and *I* from Paper 1 as a vocabulary, not as a premise: its empirical
fate does not feed back to Paper 1, and if Paper 1's trilemma were rejected, Paper 2's
eliminative statistics would still be a well-posed protocol for whether a biological
transition preserves a hidden boundary organization. Paper 3 is fully independent — it takes a
multichannel time series and returns a regime demarcation, and a reader who rejects both
companions can adopt, test, or reject it on its own terms. **The regime labels in Paper 3
(geodesic drift / fibre dispersion / rank collapse) are geometric names for geometric
objects, and the program supplies no warrant to map them onto Paper 1's cells or Paper 2's
boundary** — such a mapping would be a further, separately contestable hypothesis that none of
the three papers makes.

## Why kept apart, not submitted as a unit

Three reasons, all of which survived four rounds of adversarial review:

1. **Different genres.** Paper 1 is conceptual, Paper 2 is a pre-registered negative, Paper 3
   is methodology. Their reviewer pools are disjoint (philosophy of action; computational
   neuroscience methods; statistics / signal processing).
2. **Different readiness.** Their central claims are in different states (see below), and
   binding them would hold the more finished ones hostage to the least finished.
3. **Independence is a feature, not a limitation.** Tying them into one submission would let
   the failure of a *conceptual* result invalidate a *method*, which is worse epistemics, not
   better. The cost — that the motivating program is not visible from any single paper — is
   what this document pays down.

## Honest current state of each clause

This is the same summary that heads `RESULTS.md`, restated here so the program is not read as
stronger than its parts:

- **Clause (i) / Paper 1.** The trilemma's exhaustivity is stated for *bounded-reading
  contracts*; the synthetic residue is one load-bearing site (the exogenous costing); the
  first open problem — characterising the admissible contract class — may be ill-posed under
  §2.2's pragmatic reading of *I*; and the Lean formalization first rested on two axioms that
  were false as stated (pointwise Poincaré and Conley), now replaced by their true forms — so
  the forbidden object is excluded only for states typical of the flow's invariant measure — almost every initial condition for conservative dynamics, but nothing about the transients of dissipative dynamics, where the exclusion rests on an interpretive argument.
- **Clause (ii) / Paper 2.** The positive arm halted at 29% against a 60% bar and is not
  executable on public data; the eliminative arm survives, needs *n* ≈ 40 per condition and a
  subsampling-robust estimator, and one of its three residual filters (Test Two) was
  unexercised until recently.
- **Clause (iii) / Paper 3.** The three-regime demarcation has never been run end-to-end and,
  as defined, is not externally falsifiable; the bundle apparatus is net negative where tested;
  on real data the method does nothing better than a scalar baseline. Paper 3 now reports how it
  came to look validated (five traps). The field's standard pipeline does not fall into those
  traps on the same data, but published studies often do not report the checks that would
  expose them.

The program, in short, is a well-posed conditional whose consequent is built out in three
independent pieces, each of which reports honestly that its central empirical claim is
unconfirmed, untested, or not-yet-falsifiable. That is the state of the work, and it is the
reason the three are offered as a program of method and honest negatives rather than as a
trilogy of discoveries.

## Why three limits and negatives are the contribution

A reviewer of the trilogy observed that each paper reads as if it makes a strong claim, then
spends most of its length withdrawing it. The observation is fair, and the remedy is to state
at the outset what the papers are, not to remove the qualifications. The titles now do this.
Paper 1 is about the *limits* of control, Paper 2 about the data a test would need, and Paper 3
is a *proposed* protocol reported with its benchmarks and failure modes.

What the three offer, read that way:

1. **A map of where the question cannot be answered, and why.** Paper 1 shows which cells a
   control-theoretic account of transformation must fall into, given a stated definition of
   control. That is a sorting device, and it is useful whether or not any transformation
   occurs.
2. **A statement of what evidence would be needed, and a check of whether it exists.** Paper 2
   specifies an eliminative protocol and reports, under a stopping rule fixed in advance, that
   the only open corpus able to run it fails the protocol's own estimability gate. That is a
   result about the evidence base, and it tells the next person where not to look.
3. **A method with its failure modes measured, not assumed.** Paper 3 reports which parts of a
   geometric method were tested on real data, which failed, and against which baselines. A
   negative methods result saves the next group from building the same apparatus.
4. **A record of how the claims were corrected.** Every downgrade — the Lean axioms, the
   exchangeable-window p-values, the centred windows, the EOG channel, the between-recording
   ratio — is recorded with the control that forced it (`METHODOLOGY.md`, `STATUS.md`). The
   record lets a reader check that what remains was not selected after the fact.

None of this is a discovery about conversion, biology or EEG, and the program does not claim
one. It claims that the question has been made precise enough to fail cleanly in three
places.

## Freeze criterion

Adopted 2026-09-23, after a reviewer observed that the three papers were caught in a loop of audit, correction and re-audit. Each round made the text more honest, and none brought a paper closer to finished. From now on:

- only factual-error corrections enter the papers;
- no new experiment is run unless a stated decision point depends on its result;
- each paper has one decision that fixes its scope:
  - Paper 3: the MDM control and the literature survey decide whether it is about this method's traps or the field's;
  - Paper 1: the author's section on the system boundary;
  - Paper 2: whether a laboratory partnership is under discussion by 2026-12-23.

