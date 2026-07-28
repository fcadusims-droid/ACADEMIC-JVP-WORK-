# Escape With Class G's Own Openness: The Deciding Case for E2 (Paper 1 §7.5)

**Written before the run.** No candidate has been simulated at the time of writing.
This experiment was registered *in the verdict of* `escape_endogeneity`, which named
it as the missing case, and it is run now rather than folded into that experiment
because adding a construction after seeing a result is fitting the test to the
outcome.

## What `escape_endogeneity` established, and what it could not

That experiment separated two claims carrying §7.5's escape horn:

- **E1** escape requires an external occasion — **refuted**. An autonomous
  $\dot\theta = \theta\lVert\theta\rVert$ leaves every compact set in finite time.
- **E2** escape forfeits persistence (Λ → Class M) — **inconclusive**.

E2 came back inconclusive for a specific, diagnosable reason. Every escaping
candidate did fail persistence — but so did the *bounded* control, because the only
openness those constructions possessed was **chaos**, and chaos destroys correlation
power whether or not the trajectory escapes. The failure could not be charged to
escape.

## The equivocation this experiment targets

Running that battery exposed something sharper than the original question: **Paper 1
uses "openness" in two incompatible senses**, and the escape horn is argued in one
while Class G is defined in the other.

| | §7.5, Case 3 (strange attractor) | §8.3, Class G conditions 5–8 |
|---|---|---|
| openness means | **positive entropy**, $\lambda > 0$ | **protected tangential spectrum**, $\lvert\lambda_\parallel\rvert \approx 0$ |
| aperiodicity from | chaos | **incommensurable** frequencies |
| correlation power | destroyed (Riemann–Lebesgue) | **required** to be retained, $P_f \ge 0.05$ |

These are not two descriptions of one property; they are near-opposites. A chaotic
system is open in the first sense and *cannot* satisfy the second, because chaos is
exactly what kills $P_f$. `escape_endogeneity` measured openness in the **first**
sense, which is why its escaping candidates could not possibly have persisted.

Class G — the profile the whole positive residue of Paper 1 rests on — demands the
**second**. So the question that actually matters for the paper's own architecture is
the one that battery never asked.

## Question

Does there exist a **purely autonomous** dynamics that simultaneously

1. **escapes** — leaves every compact set;
2. is **open in Class G's sense** — aperiodic, driven by incommensurable
   frequencies, with $\lvert\lambda\rvert \approx 0$ (no chaos) and a
   non-collapsed identity observable;
3. is **non-recurrent** — never returns to a previously occupied neighbourhood;
4. **persists** — $P_f \ge 0.05$ on the contract-designated observable and
   separated from phase-randomized surrogates at $p < 0.05$?

## Why this may well succeed where the chaotic battery failed

A quasi-periodic oscillation with an exponentially growing amplitude,
$\theta_1(t) = e^{at}\cos(\omega_1 t)$ with $\omega_1/\omega_2$ irrational, is a
serious candidate for all four at once: its amplitude diverges (escape), its
frequency content is aperiodic but not chaotic ($\lambda = 0$, openness in Class G's
sense), its spiral never revisits a previous neighbourhood in the raw observable
(non-recurrence), and its autocorrelation retains power at the driving frequencies
(persistence).

If that holds, **E2 is false** and §7.5's disposal of the escape horn fails on the
paper's *own* definition of openness — the strongest available form of the objection,
since it cannot be answered by saying the test used the wrong notion.

There is a real counter-argument, which is why this is worth running rather than
asserting. Persistence is judged on the **contract-designated** observable, and under
a scale-free (ordinal) contract the growing amplitude is divided out, leaving a
bounded quasi-periodic direction which *is* recurrent by Weyl equidistribution. The
result may therefore split by contract — and §5.4 says a persistence verdict is
meaningless except relative to a declared contract, so a split is a legitimate
finding, not a hedge.

## Candidates

All autonomous, checked structurally (AST-parsed, rejected if they read a clock or
RNG) using the same checker as `escape_endogeneity`.

| # | candidate | role |
|---|---|---|
| 1 | `quasiperiodic_bounded` | **control** — incommensurable, no escape. Must pass openness + persistence and FAIL escape. Validates that the criteria are jointly satisfiable at all. |
| 2 | `quasiperiodic_escape` | the deciding candidate: incommensurable frequencies, exponentially growing amplitude |
| 3 | `quasiperiodic_escape_slow` | the same at a slower growth rate, to check the verdict is not an artifact of one escape speed |
| 4 | `commensurable_escape` | rational frequency ratio — **periodic**, so it must FAIL aperiodicity while passing the rest. Isolates incommensurability as the load-bearing property. |
| 5 | `chaotic_escape` | the `escape_endogeneity` construction, re-run here as a cross-experiment consistency check. Must reproduce: open in the entropy sense, failing persistence. |

Candidate 1 is the control that matters most: if *nothing* passes openness and
persistence together, the criteria are unsatisfiable and no conclusion about escape
can be drawn — the failure mode that made the previous experiment inconclusive.

## Measurement

Reuses `escape_endogeneity`'s estimators unchanged, including its seven-check
self-test, so the two experiments are directly comparable:

- **escape** — log-radius exceeding a fixed bound, honouring log-coded scales;
- **non-recurrence** — departure-and-return estimator (mere spatial proximity does
  not count as a return);
- **persistence** — $P_f$ against 200 phase-randomized surrogates.

Added here, because Class G's openness needs them and the previous battery had no
such measurement:

- **$\lambda \approx 0$** — angular Lyapunov exponent within $\pm 0.01$, i.e.
  *absence* of chaos, the opposite of the previous criterion;
- **aperiodicity** — the exact-period test from `class_g_coherence` (Brent-refined
  fractional-lag search), at the same $10^{-6}$ bar;
- **incommensurability** — the frequency ratio's distance to the nearest rational
  with denominator $\le 20$, which is the bar `class_g_coherence` uses (`THR_RATIONAL_Q`, imported rather than restated).

Both contracts from §5.4 are evaluated: $I_{\text{dir}}$ (scale-free, ordinal) and
$I_{\text{raw}}$ (true scale, cardinal).

## Pre-registered decision rule

- **REFUTES E2** — some escaping candidate passes Class-G openness, non-recurrence
  and persistence under **at least one** declared contract, *and* the control
  (candidate 1) confirms the criteria are jointly satisfiable. Then §7.5's escape
  clause is false on the paper's own definition of openness, and Paper 1 must be
  reformulated rather than annotated.
- **SUPPORTS E2** — every escaping candidate fails at least one property under both
  contracts, *while the control passes openness and persistence*. Only with that
  control passing is the result attributable to escape — the check whose absence
  made `escape_endogeneity` inconclusive.
- **INCONCLUSIVE** — the control fails openness or persistence, so the criteria are
  not jointly satisfiable even without escape and nothing may be concluded about
  escape.

The attribution check is pre-registered **this time**, having been added post hoc
last time.

## Stopping rule and budget

Five candidates, one attempt each at the parameters fixed here. No candidate added
after seeing results. Frequencies, growth rates and window lengths are fixed in this
document and may be changed only if a numerical sanity check fails (e.g. the
integrator loses the oscillation), with any such change recorded in the result.

## Status
Run. Outcome: **SUPPORTS_E2, and attributably** — the control passes Class-G openness
and persistence together ($P_f = 0.157$, $p = 0.005$), so the criteria are jointly
achievable and a failure under escape is charged to escape. This is the attribution the
pre-registration required and that `escape_endogeneity` could not supply.

**The mechanism is not the one §7.5 gives, and is better.** Persistence *survives*
escape: the quasi-periodic escapers reach $P_f = 0.17$–$0.21$ under the ordinal
contract while running to $\log r = 25$. What fails, for every escaping candidate under
both contracts, is **non-recurrence** (return fractions $0.81$–$1.00$). The escape
happens in the radius; the contract reads the direction; the direction is confined to a
sphere, where the recurrence theorem applies unchanged. So the escaping cell closes by
the *same* argument as the bounded cell, not by a separate appeal to divergence.

`commensurable_escape` behaved as designed, failing aperiodicity while the
incommensurable pair passed — which isolates incommensurability as load-bearing rather
than assumed. `chaotic_escape` reproduced `escape_endogeneity` exactly, confirming the
two experiments are measuring the same things.

**Two sanity-check adjustments**, both recorded: the value vector was kept at full
dimension (a 2-D sub-vector passes near zero, putting a spurious $\lambda = -0.019$ on
a rotation whose exponent is analytically zero), and the contract observable was
declared as a mixture of channels (coordinate 0 alone is a pure sine in which the
second frequency never appears). Neither changed a threshold. See
`_results/escape_persistence_decider/result.json`.
