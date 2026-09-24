# Data specification for a collaborating laboratory (Paper 2, CBRA)

**DRAFT for the author to review, revise and sign. It has not been sent to anyone.** Whoever sends
it commits, under their own name, to the design below. The author should read it as if they had
written it and change anything they would not defend in a conversation with the group receiving
it.

*Prepared 2026-09-23. Partnership window: until 2026-12-23. If no group has agreed to discuss a
collaboration by then, Paper 2 moves to the reduced version: a short data-requirements paper with
the I-CARE negative (see `OPEN_ISSUES.md`).*

## What we are asking for, in one paragraph

We have a pre-registered eliminative protocol with a strict go/no-go gate. It asks whether a
brain-state transition preserves a structured "boundary residual": interoceptive (cardiac)
structure that survives a linear-Gaussian null and an ordinary-criticality null. The protocol has
been built, simulated and run once on public data. It halted at its own stopping rule, because
the only public corpus with the right structure (I-CARE, post-cardiac arrest) failed the gate:
6 of 21 patients, against a 60 % bar fixed in advance.

We are looking for a group that records, or could record, the three things no public repository
holds together. The analysis would be registered **before** any data are seen.

## The three properties the data must have together

1. **Raw multichannel EEG with a concurrent cardiac channel.**
   - EEG: at least 19 channels, as raw signal, not a processed index such as BIS.
   - ECG: sampled fast enough for reliable R-peak timing (≥ 250 Hz).
   - The two must be time-locked.
2. **A contrast between transitions that preserve the person and transitions that do not.** The
   protocol calls these I⁺ and I⁻.
   - I⁺: a transition after which the person demonstrably returns, such as emergence from
     anaesthesia.
   - I⁻: a matched transition after which they do not, such as non-recovery after cardiac arrest.
   - The matching must be on the surface dynamics.
   - The I⁻ arm is the hard part. It is why reversible-anaesthesia datasets alone cannot run the
     test.
3. **Records long enough for a subsampling-robust criticality estimate.** In practice this means
   hours, not minutes, of stable recording around each transition.

## Design numbers (from the committed simulations)

| Requirement | Value | Source in the repository |
|---|---|---|
| Matching of the two arms on surface dynamics | standard deviation ≲ 0.3 σ; beyond that, unmatched contrasts manufacture dissociations at a rate independent of n | `dissociation_power_analysis` (Paper 2 §14.1) |
| Sample size | about 40 per condition for 80 % power at a moderate effect (SNR 0.8) | same |
| Criticality estimator | multistep regression (Wilting and Priesemann 2018), never the naive lag-1 slope, which false-certifies 79 % of confounded near-critical systems | `subcriticality_control` |
| Metabolic null resolution | finer than about 0.7–0.9 diffusion lengths | `metabolic_null_resolution` |
| Go/no-go gate (B1) | interoceptive nonlinearity versus IAAFT surrogates in at least 60 % of participants; I-CARE reached 29 % | `cbra_boundary_residual` |

## What happens, in order

1. **Before any data are shared:** the design, the analysis code and the decision rules are
   registered publicly. A Registered Report is possible only in this order.
2. **Gate B1 is run first.** If it fails, the study stops and the negative is reported. This is
   what happened on I-CARE.
3. **If B1 passes:** the pre-registered dissociation test runs once, with no tuning loop.
4. **All code is open.** The existing pipeline is in `experiments/paper2_cbra_protocol/`.

## What the collaborating group would get

- Co-authorship on any resulting paper.
- A fully specified, pre-registered analysis.
- A negative result reported as prominently as a positive one.

Data governance, consent and ethics approval remain the group's. The protocol needs derived
features, not identifiable data. Whether raw data can leave the institution is the group's
decision.

## What we are not claiming

The protocol tests a conditional. *If* an identity-linked boundary channel existed, this is what
it would have to leave measurable. Nothing in the repository is evidence that such a channel
exists. The one public attempt was negative.

## For the author before sending

- Check every number above against the cited `result.json`.
- Decide which groups to write to. A reviewer offered to help identify three to five named
  groups, for example anaesthesiology EEG labs or neurointensive care units with concurrent
  EEG/ECG monitoring. A direct e-mail to named groups is what brings collaborators; a web page
  does not.
- Sign it.
