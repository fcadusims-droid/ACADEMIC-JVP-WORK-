# Does the Escape Horn Close Under a Cardinal Contract? (Paper 1 §7.5)

**Written before the run.** No cardinal contract has been evaluated at the time of
writing. This experiment was named as an open question in `RESULTS.md` after
`escape_persistence_decider` closed the scale-free case, and it is run as its own
pre-registered study rather than folded in, because adding a contract after seeing a
result is fitting the test to the outcome.

## The gap this closes

`escape_persistence_decider` established that §7.5's escape horn does close for a
**scale-free** identity contract — but not by the argument §7.5 gives. Persistence
*survives* escape under a scale-free contract (P_f = 0.17–0.21 against a 0.05 bar);
what fails is **non-recurrence**, because the escape lives in the radius while a
scale-free contract reads the direction, and the direction lives on a compact quotient
where Poincaré recurrence applies unchanged.

That closure has a stated price: **it depends on the contract being scale-free.** §5.4
makes a persistence verdict meaningless except relative to a declared contract, and a
reader entitled to a *cardinal* contract — one treating absolute value magnitude as
constitutive, not just the ordering — is owed an answer. §7.5's own words ("unbounded
value drift is *itself* a failure of persistence … a more extreme Class M") are a claim
about magnitude, so the cardinal case is exactly the one those words describe.

## What the decider already shows, and why it is not enough

The decider evaluated a second observable, `I_raw` = direction × e^{log r}, which is
cardinal in spirit. Under it the escaping candidates failed persistence hard
(P_f = 0.0006, 0.0001) while the bounded control passed (0.157) — pointing at a clean
two-mechanism resolution: scale-free contracts close the horn by recurrence, cardinal
contracts by persistence-failure, so §7.5's argument is *correct precisely for the
contract its words fit*.

But `I_raw` multiplies by e^{25}, concentrating all variance in a handful of final
samples, so its P_f collapse may be a **numerical artefact of an unbounded observable**
rather than a genuine loss of the identity pattern. A cardinal contract that reads
magnitude without blowing up numerically is needed before the two-mechanism resolution
can be asserted.

## Question

Take the deciding candidate from `escape_persistence_decider` — `quasiperiodic_escape`,
incommensurable frequencies with an exponentially growing amplitude, which passes all
four properties under a scale-free contract. Under a **cardinal** identity contract,
does it still pass escape + Class-G openness + non-recurrence + persistence?

## Cardinal contracts evaluated

Four principled cardinal observables, because "reads absolute magnitude" admits more
than one honest formalisation and §5.4 makes the observable a declared choice; a result
that differs between them is the finding, not a hedge. Each is declared here in advance.

| contract | observable | why it is cardinal, and what it guards against |
|---|---|---|
| `raw_coord` | direction × e^{log r} | the decider's `I_raw`, carried for continuity; expected degenerate (exponential) |
| `magnitude` | ‖θ‖ | raw magnitude; also unbounded, a second degeneracy check |
| `log_magnitude` | log‖θ‖ | **the non-degenerate cardinal reading** — grows linearly, no numerical blow-up, so a P_f verdict here is genuine rather than an artefact |
| `saturating` | tanh(log‖θ‖ / 10) | reads magnitude but is bounded, isolating whether any P_f collapse is about the *pattern* or about the observable's dynamic range |

The scale-free contract `I_dir` is carried as a reference column, so the split (if any)
is visible in one table.

## Control (attribution, pre-registered)

The **bounded** quasi-periodic system is evaluated under every cardinal contract. If a
cardinal contract cannot certify openness + persistence even for a bounded system, then
that contract is not a usable identity contract at all and a failure under escape says
nothing about escape — the attribution failure that ended `escape_endogeneity`. Only
cardinal contracts whose bounded control passes can carry a verdict about escape.

## Measurement

Every estimator is imported unchanged from `escape_endogeneity` /
`escape_persistence_decider`, including the seven-check instrument self-test, so this
is directly comparable to both:

- **escape** — log-radius past a fixed bound, honouring log-coded scales;
- **openness** (Class G's sense) — |angular λ| ≤ 0.01 (absence of chaos), aperiodic by
  the Brent-refined period test at the 1e-6 bar, non-collapsed variance;
- **non-recurrence** — departure-and-return estimator (proximity alone is not a return);
- **persistence** — P_f ≥ 0.05 on the contract observable AND separated from 200
  phase-randomized surrogates at p < 0.05, both required, as §5.4 demands.

## Pre-registered decision rule

- **HORN OPEN FOR CARDINAL CONTRACTS** — some cardinal contract whose bounded control
  passes lets the escaping candidate pass all four. Then §7.5 cannot close the horn for
  that contract, and Paper 1 must explicitly restrict its exclusion to the contracts
  where it does close, naming the escaping witness as a live cardinal counterexample.
- **HORN CLOSES FOR CARDINAL CONTRACTS** — under every cardinal contract whose control
  passes, the escaping candidate fails at least one property. Then the two-mechanism
  resolution stands, and the *mechanism* of failure per contract is the reportable
  content: if it is persistence, §7.5's original "more extreme Class M" argument is
  vindicated precisely for cardinal contracts.
- **CONTRACT-DEPENDENT / INCONCLUSIVE** — the usable cardinal contracts disagree, or
  none has a passing control. Reported as such; §5.4 already says the verdict is
  contract-relative, so a genuine disagreement between principled cardinal contracts is
  itself a substantive finding about how much the exclusion can claim.

## Stopping rule and budget

One escaping candidate, one bounded control, four cardinal contracts plus the scale-free
reference, one attempt at the parameters inherited from the decider. No contract added
after seeing results; a contract may be dropped only if its bounded control fails
(making it unusable), and that is recorded rather than hidden.

## Status
Run. Outcome: **HORN_CLOSES_FOR_CARDINAL**. The escape horn closes under cardinal
contracts too, by the *same* recurrence argument as the scale-free case, not by the
persistence-failure §7.5 asserts. All three cardinal contracts whose bounded control
passes (`saturating`, `log_scaled`, `raw_coord`) leave the escaping candidate
**recurrent** (0.81–0.93), so it fails non-recurrence under every one. Persistence
collapses **only** under the exponential `raw_coord` (P_f = 0.0006) while the bounded
and linear readings of the identical system retain it (P_f = 0.21, 0.15) — so that
collapse is the numerical artefact of an $e^{25}$ observable, the concern this
pre-registration named, not §7.5's mechanism. The two-mechanism split the design
anticipated did not materialise; the answer is one mechanism (recurrence) everywhere.
Paper 1 §7.5 updated accordingly; the scale-free-dependency caveat is withdrawn. See
`_results/escape_cardinal_contract/result.json`.
