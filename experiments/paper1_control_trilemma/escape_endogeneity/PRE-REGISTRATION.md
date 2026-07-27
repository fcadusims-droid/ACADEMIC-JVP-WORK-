# Can Escape from Compactness Be Purely Endogenous? (Paper 1 §7.5–7.6)

**Written before the run.** No candidate has been simulated at the time of writing.

## What is actually at issue

The Meta-Optimization Collapse Theorem is stated for an autonomous flow
$\dot\theta = f(\theta)$ **on a compact set**, and on that domain it is not in
doubt: Poincaré recurrence is a theorem, and §7.5's refutation condition — exhibit
an autonomous, compact, finite-measure-preserving dynamics that is simultaneously
positive-entropy and non-recurrent — cannot be met. `rl_agents_trichotomy` already
confirmed this empirically on the standard adversarial candidates.

So the compact case is closed. The exposed surface is the **escape horn**, and the
claim carrying it is not a theorem but a single clause in §7.5's first stated
limitation:

> a preference dynamics permitted to grow without bound evades the recurrence
> argument, **but unbounded value drift is itself a failure of persistence** (the
> agent's values diverge), so it does not rescue conversion either — it is a more
> extreme Class M.

Two distinct claims travel together in the surrounding prose and must be separated,
because only the second is defensible as stated:

- **(E1) Escape requires an external occasion.** §7.5 concludes that conversion is
  "necessarily externally occasioned", and §7.7 reports that sustained novelty
  "required, in every case, leaving compactness (the escape horn)". Read informally,
  this suggests leaving compactness is something done *to* a system.
- **(E2) Escape forfeits persistence.** Whatever leaves every compact set thereby
  loses the correlation power that separates Λ from Class M.

**E1 is false and this experiment does not need to be run to know it**:
$\dot\theta = \theta^2$ is autonomous, contains no external or time-dependent term,
and leaves every compact set in finite time. That is stated here, in advance, so that
no part of the verdict can be presented as a discovery. If the paper anywhere asserts
E1 rather than E2, it is wrong and must be reformulated.

The real question is therefore **E2**, which is a falsifiable dynamical claim about
the *joint* achievability of escape and persistence.

## Question

Does there exist a **purely autonomous** preference dynamics $\dot\theta = f(\theta)$
— no exogenous input, no explicit time dependence — that simultaneously

1. **escapes**: leaves every compact set;
2. is **open**: retains positive entropy / non-collapsed agency on the
   identity-relevant observable;
3. is **directed**: reaches a permanent new regime and does not return (low
   recurrence on the identity observable);
4. **persists**: retains correlation power on the contract-designated observable,
   $P_f$ above the same threshold `class_g_coherence` uses, and separably above
   phase-randomized surrogates — i.e. is **Λ, not Class M**?

A system meeting all four is a counterexample to E2, and §7.5's escape clause would
have to be rewritten.

## Why this is not obviously answerable either way

There is a real argument on each side, which is why it is worth running.

**For the paper.** If the identity observable is scale-invariant — if only the
*ordering* of values matters, not their magnitude — then the contract-relevant state
lives on the projective quotient (a sphere), which is compact. Escape in the radial
coordinate is then invisible to the contract, Poincaré recurrence applies to the
angular dynamics, and the counterexample collapses back into Case 3. If that is what
happens, the theorem's reach is *larger* than its statement, and this experiment
supplies the argument for saying so.

**Against the paper.** The radial escape can *couple back* into the angular
dynamics — for instance $\dot\varphi = g(\varphi)/r$ with $r$ growing — so the
angular motion slows as the state escapes. That is still autonomous in $(r,\varphi)$,
but the direction can converge to a limit that is not a fixed point of $g$, giving a
permanent, non-recurrent terminus while the observable retains correlation power at
every finite time. Whether openness survives that freezing is exactly what has to be
measured rather than argued.

## Candidates

Each is autonomous by construction, and this is **checked structurally** rather than
asserted: every field is a function of the state alone, and the runner rejects any
field whose signature accepts a time argument.

| # | candidate | escapes? | purpose |
|---|---|---|---|
| 1 | `bounded_lorenz` (control) | no | instrument check — must reproduce recurrence |
| 2 | `radial_blowup` $\dot\theta=\theta$ | yes | escape with frozen direction; expected to fail openness |
| 3 | `finite_time_blowup` $\dot\theta=\theta\lVert\theta\rVert$ | yes | escape in finite time |
| 4 | `escaping_chaos` | yes | radial escape + chaotic direction: open, but recurrent in direction? |
| 5 | `freezing_escape` | yes | the serious candidate: escape that endogenously slows its own angular motion |
| 6 | `dimension_extension` | yes | endogenous activation of new value coordinates |

Candidate 6 is included because it is the case the theorem does not cover at all: the
theorem quantifies over flows on a *fixed* $\mathbb{R}^n$, and an agent that
endogenously extends its own value space is outside that quantifier rather than a
counterexample within it. Its result will be reported as a scope finding, not as a
refutation.

## Measurement

- **Escape** — $\lVert\theta(t)\rVert$ exceeds every fixed bound and is increasing at
  the end of the window; finite-time blow-up recorded separately.
- **Openness** — largest Lyapunov exponent of the identity observable (Benettin, full
  state renormalization, the corrected scheme from `value_base_discontinuity_probe`),
  plus the observable's late-window variance as a non-collapse check.
- **Directedness / non-recurrence** — recurrence fraction of the identity observable
  under the same estimator as `rl_agents_trichotomy`, with the **toroidal-vs-Euclidean
  metric chosen to match each candidate's geometry** (the defect that experiment was
  corrected for).
- **Persistence** — $P_f$ = mean squared long-lag autocorrelation of the
  contract-designated observable, threshold **$P_f \ge 0.05$**, the same bar
  `class_g_coherence` uses for condition 6, plus separation from **200 phase-randomized
  surrogates** at $p < 0.05$, as §5.4 requires.

Two contracts are evaluated for every candidate, because §5.4 makes persistence
contract-relative and the answer may differ between them:

- $I_{\text{dir}}$ — a scale-free direction observable (what a purely ordinal
  preference contract designates);
- $I_{\text{raw}}$ — a raw coordinate observable (what a cardinal contract
  designates).

Reporting both is not hedging: §5.4 states that a persistence verdict is meaningless
except relative to a declared contract, so a result that holds under one and fails
under the other is the honest finding and will be reported as such.

## Pre-registered decision rule

- **REFUTES E2** — some autonomous candidate escapes *and* passes openness,
  non-recurrence and persistence under **at least one** declared contract. Then
  §7.5's escape clause is wrong as written and Paper 1 must be reformulated.
- **SUPPORTS E2** — every escaping candidate fails at least one of openness,
  non-recurrence or persistence, under **both** contracts. Then the clause stands,
  and the *reason* it stands (which property fails, and whether the failure is
  structural or particular to the construction) is the reportable content.
- **SCOPE GAP** — a candidate escapes and passes all four, but only by leaving the
  theorem's quantifier (e.g. by changing the dimension of the value space). Then the
  theorem is not refuted but its scope is narrower than the prose implies, and the
  prose must say so.

E1 is reported as **false regardless of outcome**, since a single autonomous
blow-up settles it and that is known before the run.

## Stopping rule and budget

Six candidates, one attempt each at the parameters fixed here. Integrator tolerances
and window lengths may be tightened *only* if a candidate fails a numerical sanity
check (blow-up detected as integration failure rather than escape), and any such
change is recorded in the result. No candidate is added after seeing results; if an
outcome suggests a further construction, that is a *new* pre-registered experiment,
not an extension of this one.

## Status
Run. Outcome: **SUPPORTS_E2_BUT_UNATTRIBUTABLE** — the pre-registered rule returns
"E2 survives", and that verdict is reported as **inconclusive** because the design
cannot attribute the result to escape.

**E1 is refuted, as anticipated in advance.** `finite_time_blowup` is autonomous and
leaves every compact set in finite time. Escape needs no external occasion, and any
sentence implying otherwise must be rewritten.

**On E2 the informative finding is a negative one about the argument's structure.**
The escaping candidates achieve escape, openness *and* non-recurrence
simultaneously — `escaping_chaos` reaches angular λ = +0.33 with recurrence 0.98 under
a return-based estimator, `freezing_escape` λ = +0.20. So in the escaping regime
Poincaré recurrence is **not** what stops them, and §7.5's disposal of the horn rests
entirely on the persistence condition rather than on the trichotomy.

**But persistence cannot be charged to escape.** The bounded control fails it too
($P_f = 0.0011$), because the only openness these candidates have is chaos, and chaos
destroys correlation power whether or not the trajectory escapes. This attribution
check was **not** pre-registered; it was added after the run and is recorded as such.
It downgrades what may be concluded rather than altering the rule.

**A deeper problem with the operationalisation, found by running it.** "Openness" is
read here as a positive Lyapunov exponent — §7.5's *positive entropy* sense — whereas
Class G in §8.3 demands the opposite signature: protected tangential spectrum
($|\lambda_\parallel| \approx 0$), incommensurable frequencies, retained correlation
power. The paper uses both senses and they come apart. The case most likely to escape
*and* persist — aperiodic and correlation-retaining without being chaotic — is exactly
what this battery lacks.

Adding that candidate now would be fitting a construction to a result, which the
stopping rule above forbids. It is registered as the required follow-up instead. See
`_results/escape_endogeneity/result.json`.
