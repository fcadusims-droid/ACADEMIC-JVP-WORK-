# Class G Internal Coherence — Is the Ten-Condition Profile Non-Vacuous? (Paper 1 §8.3)

**The existential-risk check, run before anything else.** Paper 1's entire positive
residue is **Class G**: the admissibility profile the trilemma leaves standing. §8.3
defines it as a **single conjunctive exclusion criterion of ten conditions**, and
says a candidate is G-admissible "only if it survives all ten exclusions at once."
That conjunction has **never been tested for satisfiability**. If the ten conditions
are mutually unsatisfiable — if no mathematical object whatever can meet them
simultaneously — then Class G is *empty by over-specification*, the trilemma's
"residual profile" is a residue of nothing, and Paper 1's §§8–10 must be rewritten.
This is cheap to test and expensive to be wrong about, so it runs first.

**The prior demonstration does not settle this.** Paper 2 §15.2 exhibits a toy
"Class G" regime, but it measures only four diagnostics (correlation power, agency
variance, transverse spread, recurrence) — touching conditions 2, 4, 5, 6, 7 in part
and **never testing conditions 1, 3, 8, 9, or 10 at all**. In particular the two
conditions that carry the anti-reduction weight (9, the receptivity-gate
factorization; 10, non-membership in the endogenous span) have no numerical content
anywhere in the repo.

## The two ways Class G could be vacuous

A conjunctive criterion can fail in *either* direction, and both are reported:

- **Empty (over-specified).** No system satisfies all ten. Class G excludes
  everything, including its own intended instances. Paper 1's positive residue
  collapses.
- **Universal (under-specified).** Every system satisfies all ten, including the
  near-misses §8.3's own table says must be excluded (damping, ungated forcing,
  endogenous feedback, coercion). Then the criterion has no exclusionary content and
  "Class G" does no work — a different, equally serious defect.

A healthy result is therefore **satisfiable *and* discriminating**: an explicit
system passes all ten, and each named near-miss fails the specific condition the
paper predicts it should fail.

Note the distinction from §8.3's own remark that "the conjunction may be *empty* in
many systems — and that is not a defect." That remark concerns *domain* emptiness
(a given physical domain may host no G-transformation), which is compatible with the
profile being coherent. This test is about *logical* satisfiability: whether the
conjunction is non-empty in **some** system. Domain-emptiness is a finding;
logical-emptiness is a refutation.

## Method

An explicit stochastic dynamical system is constructed on
$x = (q, r, \varphi_1, \varphi_2, a, \theta)$ with a declared endogenous field $F_0$
and a declared external field $W_{ext}$, and **all ten conditions are measured on
it**:

- $q$ — regime coordinate on a double well $V_0(q)=(q^2-1)^2/4$: the $M$ (dispersive)
  basin at $q=-1$, the $\Lambda$ (persistent) basin at $q=+1$, barrier at $q=0$.
- $r$ — deviation from the identity manifold, contracted at rate $\kappa$, driven by
  identity-direction diffusion $D_{id}$.
- $\varphi_1,\varphi_2$ — protected phases advancing at **incommensurable**
  frequencies ($\omega_2/\omega_1=$ golden ratio); identity observable
  $f=\cos\varphi_1+\cos\varphi_2$.
- $a$ — agency coordinate, Ornstein–Uhlenbeck with diffusion $D_{ag}$.
- $\theta$ — orientation/receptivity variable driving the gate $\chi(\theta)$.

The **G intervention modifies the landscape rather than commanding a path**:
$V_G(q)=V_0(q)-\chi(\theta)\,B\,h(q)$ with $h$ peaked at the barrier top, so the
applied field is $W_G(x,\theta)=\chi(\theta)\,W_{ext}(q)$, $W_{ext}(q)=B\,h'(q)$.
This is what "lowers the barrier while imposing no commanded trajectory" has to mean
if it means anything.

## Pre-registered per-condition tests and thresholds (fixed before running)

| # | Condition (§8.3) | Operational test | Pass threshold |
|---|---|---|---|
| 1 | $\Delta V^G_{M\to\Lambda}<\Delta V_{M\to\Lambda}$ | barrier height of $V_G$ vs $V_0$ at the receptive gate value; confirmed dynamically by mean first-passage time $M\to\Lambda$ | $\Delta V^G \le 0.9\,\Delta V_0$ **and** $\mathrm{MFPT}_G<\mathrm{MFPT}_0$ |
| 2 | $D_{ag}>0$ | stationary variance of the agency coordinate | $\mathrm{Var}(a)\ge 0.1$ |
| 3 | $D_{id}<D_c$ | $D_c$ := smallest identity diffusion at which invariant preservation through the transition falls below $0.9$ (measured by sweep); compare the system's $D_{id}$ | $D_{id}\le 0.5\,D_c$ |
| 4 | $\lambda_\perp<0$ | transverse Lyapunov/decay exponent | $\lambda_\perp\le-0.05$ |
| 5 | $\lambda_\parallel=0$ (protected tangential spectrum) | tangential Lyapunov exponent | $\lvert\lambda_\parallel\rvert\le0.05$ (and **not** $\le-0.05$) |
| 6 | long-time correlation power nonzero | $P_f=\langle\lvert C_f(t)\rvert^2\rangle$ at long lags | $P_f\ge0.05$ |
| 7 | no $T>0$ with $f(\Phi_{t+T})=f(\Phi_t)$ | **exact-periodicity** test: $\mathrm{err}(T)=\max_t\lvert f(t+T)-f(t)\rvert/(2\,\mathrm{sd}f)$; a signal is periodic iff some $T^\*$ gives $\mathrm{err}\approx0$ **and** the quality persists at $2T^\*,3T^\*$ | not periodic: $\mathrm{err}(T^\*)>10^{-6}$ or quality decays at multiples (acf reported as secondary) |
| 8 | incommensurable / inexhaustible drive | rational approximation of $\omega_2/\omega_1$ | no $p/q$ with $q\le20$ within $10^{-3}$ |
| 9 | $W_G=\chi(\theta)W_{ext}$ | rank-1 structure of the applied-force matrix over a $(\theta\times q)$ grid, **and** the gate is non-trivial | rank-1 relative residual $\le10^{-6}$ **and** $\min\chi\le0.1\max\chi$ |
| 10 | $W_{ext}\notin\langle F_0\rangle$ | relative residual of least-squares projection of $W_{ext}$ onto the span of the endogenous field components over a state grid | relative residual $\ge0.1$ |

**Note on condition 7's operationalization (fixed before any run, no data seen).**
The first draft of this table tested condition 7 by an autocorrelation threshold
($\max\mathrm{acf}\le0.95$). That is mathematically inadequate and was replaced
before running: a quasi-periodic signal is *almost periodic*, so its autocorrelation
returns arbitrarily close to $1$ at near-recurrence lags given enough lag range
(for $\omega_2/\omega_1=$ golden ratio, Fibonacci lags already reach
$\mathrm{acf}\approx0.998$). Such a threshold would measure the length of the
analysis window, not periodicity. Condition 7 as written in §8.3 asserts the absence
of an **exact** period ($f(\Phi_{t+T})=f(\Phi_t)$), so the faithful test is a
sup-norm equality test whose quality must *persist at multiples of* $T^\*$ — exactly
periodic signals repeat perfectly at $2T^\*,3T^\*$, whereas a quasi-periodic
near-recurrence degrades. The acf number is still computed and reported as a
secondary descriptive statistic.

## Pre-registered discrimination controls

Each near-miss from §8.3's own filter table is run through the identical ten-test
battery, with the condition it is *predicted* to fail named in advance:

| Control | Construction | Predicted failure |
|---|---|---|
| Classical damping | strong tangential damping, agency noise off | 2 and 5 |
| Ungated external forcing | same $W_{ext}$, gate removed ($\chi\equiv1$), strong | 9 (and 3 if it drives $D_{id}\ge D_c$) |
| Endogenous feedback | "external" field replaced by a multiple of $F_0$'s own $q$-component | 10 |
| Coercion | gate decoupled from orientation **and** agency collapsed | 2 and 9 |
| Commensurable drive | $\omega_2/\omega_1=3/2$ (rational) | 7 and 8 |

## Decision rule (fixed before running)

- **COHERENT AND DISCRIMINATING** — the G candidate passes all ten **and** every
  control fails at least one condition, each failing (at minimum) a condition the
  table above predicts. Class G is non-vacuous with genuine exclusionary content;
  §8.3 stands as written, now with a satisfiability witness.
- **EMPTY** — the G candidate fails ≥1 condition. Report *which*, and whether the
  failure is a **fundamental tension between conditions** (e.g. 2 vs 3: agency
  diffusion cannot be raised without raising identity diffusion) or an artifact of
  this particular construction. A fundamental tension means Class G is
  over-specified and Paper 1 §§8–10 require rewriting; that is reported as
  prominently as a pass.
- **NON-DISCRIMINATING** — the G candidate passes but one or more controls also pass
  all ten. Then the conjunction fails to exclude what §8.3 claims it excludes, and
  the offending condition(s) must be strengthened or the filter table corrected.

## Scope honesty

A satisfiability witness establishes that the ten conditions are *mutually
consistent* and that the criterion *discriminates* among the paper's own named
candidates. It establishes **nothing** about whether any biological, psychological,
or theological process instantiates Class G — that is exactly the question §8.3 says
it does not answer, and Paper 2's whole architecture exists because it is open. Nor
does a witness make Class G non-trivial in any *particular* domain: domain-emptiness
remains possible and is not tested here.

## Budget

One construction, one battery, one control sweep. If the first construction fails a
condition, **one** targeted repair attempt is permitted (and reported as such); if it
still fails, the finding is EMPTY with the offending tension named. No unlimited
search for a passing system — an unbounded hunt would itself be the bias the
pre-registration exists to prevent.

## Status
Run. Verdict: **COHERENT AND DISCRIMINATING.** An explicit stochastic system
satisfies all ten §8.3 conditions simultaneously (barrier $0.250\to0.107$, MFPT
$386\to187$; agency variance $0.50$; $D_{id}=0.020$ against measured $D_c=0.100$;
$\lambda_\perp=-1.01$, $\lambda_\parallel=+0.000$; $P_f=0.22$; exact-period error
$4\times10^{-2}\gg10^{-6}$; incommensurable drive; rank-1 gate residual
$1.7\times10^{-16}$ with a gate that closes; endogenous-projection residual $0.60$).
So the ten conditions are **mutually consistent** — Class G is not empty by
over-specification. It also **discriminates**: all five near-misses from §8.3's own
filter table are excluded, each failing a predicted condition (damping 2/5/6/7;
ungated forcing 3/9; endogenous feedback 1/10; coercion 2/9; commensurable drive
7/8).

Two instrument defects were found and fixed **before** the result was read, both
recorded in `result.json`: an integer-lag periodicity search could not detect a true
period that falls between samples (the commensurable control was wrongly passing
condition 7), and a coarse fractional-grid refinement left a numerical floor
($\approx10^{-5}$) above the pre-registered $10^{-6}$ threshold, misreading a pure
sine as aperiodic. Both were caught by a detector self-test on signals of known
character, which now runs as a gate on every execution. The pre-registered threshold
was **not** loosened; the numerics were tightened (Brent refinement, floor
$\approx10^{-8}$). Fixing them made the discrimination *stronger*, not the witness's
pass easier. See `_results/class_g_coherence/result.json`.
