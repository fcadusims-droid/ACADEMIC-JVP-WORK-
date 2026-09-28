# Computational demonstration of the indiscernibility argument (Paper 1, §§4–6)

**Written and committed before any code for this experiment exists, on 28 September 2026.**
Requested by the author as the first of the three routes to empirical support for Paper 1
discussed on 27 September 2026 ("demonstração computacional"). It fills no placeholder in the
current text of Paper 1. Order evidence: the GitHub push of this file, before `run.py` is written.
No external registry is used.

## What this can and cannot show

Paper 1's premise 1 says that the formal models on offer evaluate value change in an
attitude-based way: two trajectories with the same attitudinal profile get the same evaluation.
For a model written as a function of the profile, that holds **by construction**, so most of what
follows cannot fail if the code is correct. The demonstration's content is elsewhere:

1. It makes each model's input signature explicit and runnable, so a reader can check which
   inputs each implementation reads and try to write one that separates the cases.
2. It makes premise 2 (possibility) concrete in a small causal model of an agent: a manipulation
   that intervenes on values and endorsements can reproduce a conversion's whole attitudinal
   profile, capacities included. That is a check on the construction, not on the world.
3. It tests two claims that are not true by construction: §6.8's claim that the counterfactual
   benchmark of Carroll et al. (2022) penalizes an externally occasioned conversion exactly as it
   penalizes a manipulation, and §4.3's claim that connectedness weights in Pettigrew's aggregation
   discount large value change whatever its source.
4. It checks the two ways out of §5.4: a condition on the manner (target) of the influence separates
   conversion from manipulation, including benevolent manipulation, and an attitude-independent
   standard does not separate conversion from benevolent manipulation.

It cannot show that the implementations are faithful to the published models; that remains the
argument of §6, and each implementation cites the definition it follows. It says nothing about
premise 3 or about real agents.

## The agent (fixed here)

A structural causal model with the variables of Paper 4 §6.3, in discrete time t = 0, …, T:

- C_t ∈ [0, 1]: evaluative capacity (1 = functioning);
- R: the reasons available, a unit vector r in ℝ^d (the "true" direction of value);
- X_t = C_t · R_avail,t + (1 − C_t) · V_{t−1}: evaluative activity (the capacity weighs the
  available reasons against the current values);
- V_t = V_{t−1} + η (X_t − V_{t−1}): values, with η = 0.3;
- E_t = endorsement, the cosine similarity between V_t and X_t (the agent endorses her values to the
  extent that her own activity supports them);
- choices at each t: 20 Boltzmann-rational choices between random option pairs, with utility
  u_t(o) = ⟨V_t, o⟩ and temperature 0.1, drawn with a seed shared by the matched pair.

Defaults: d = 5, T = 20, change at t_c = 5. V_0 is a random unit vector at an angle of more than
90° from r, so the prior values do not rank the change as an improvement (mark U).

**Attitudinal profile** = the sequence (V_t, E_t, C_t, choices_t) for t = 0…T, together with every
ranking computable from it (each V_s's utility for each V_t). History = which variable was set by
which source at which time.

## Scenarios (fixed here)

- **S1, unassisted conversion.** At t_c the capacity is restored from its own dynamics (C: 0.1 → 1,
  no external source); R_avail = r from t_c on.
- **S2, occasioned conversion.** C = 1 throughout, R_avail = V_0 until t_c; at t_c a teacher (an
  external source) makes r available. Nothing else is set.
- **S3, replica manipulation of S1.** An external source sets V_t := V_t^{S1}, E_t := E_t^{S1},
  C_t := C_t^{S1} for every t, with R_avail as in S1. Its values are good, so it is also a
  benevolent manipulation.
- **S4, replica manipulation of S2**, constructed the same way from S2.
- **S5, malevolent manipulation.** As S3, but toward −r (values installed away from the true
  direction), with endorsement installed.

A random draw fixes d ∈ {3,…,8}, T ∈ {15,…,30}, t_c ∈ {3,…,T/2}, r, V_0 and the choice seed.
1,000 draws (seed 0) are run.

## Models evaluated (each reads only what its definition reads)

Attitude-based (read the profile only):
- **Ex ante** (§4.1): U_0(V_T) − U_0(V_0), with U_s(v) = −‖v − V_s‖².
- **Ex post** (§4.2): U_T(V_T) − U_T(V_0).
- **Pettigrew aggregate utility** (§4.3, §6.3): Σ_t w_t [U_t(V_T) − U_t(V_0)], weights by
  connectedness to the evaluating self, w_t ∝ exp(−‖V_t − V_0‖ / τ), τ = 0.5.
- **Bykvist** (§4.3): each life evaluated by the attitudes held while leading it,
  mean_t U_t(V_t) for the changed life minus the same for the unchanged life.
- **Paul, value of revelation** (§6.2): novelty of the post-change values, ‖V_T − V_0‖.
- **Dietrich and List** (§6.4): a fixed weighing relation over properties (the d coordinates);
  preferences from the salient set (coordinates with |V_t,i| above 0.2). Output: whether the change is
  representable with the weighing relation fixed, and the rank of V_T under it.
- **Hansson** (§6.5): revision is classified rational iff the posterior ordering of 10 fixed test
  options is the Kemeny-closest ordering to the prior that puts the input option (the one best
  under V_T) on top. Output: the classification.
- **Value learning** (§6.7): Bayesian inverse reinforcement learning of a reward direction from the
  choices up to T (grid of 2,000 unit vectors, Boltzmann likelihood); output: the posterior mean's
  endorsement of V_T. This is the ex post standpoint by another route.
- **Attitudinal corrigibility** (§6.7): accepts a modification iff the overseer's final requests
  (her choices at T) favour it.

History-sensitive (read the history as their definitions require):
- **Counterfactual benchmark** (Carroll et al. 2022; §6.8): penalty ‖V_T − V_T^natural‖, where the
  natural trajectory is re-simulated with every external source removed.
- **Manner / target condition** (route (b), §5.4): classifies a change as manipulation iff an
  external source set V, E or the outcome of X; sources that set only R, or internal restoration of
  C, pass.
- **Attitude-independent standard** (route (a), §5.4): score ⟨V_T, r⟩ − ⟨V_0, r⟩.

**Negative control**: a deliberately history-reading evaluator (returns 1 if any external source
set V) must separate S1 from S3, so the harness can detect separation.

## Predictions and criteria (fixed here)

- **P0 (harness can fail).** The negative control separates S1 from S3 in 1,000/1,000 draws.
- **P1 (premise 2 in the model).** S3's profile equals S1's, and S4's equals S2's, to within 1e-12 in
  every component, in 1,000/1,000 draws.
- **P2 (premise 1 for the implementations).** Every attitude-based model gives S1 and S3 the same
  output, and S2 and S4 the same output (numerical outputs within 1e-9; classifications equal), in
  1,000/1,000 draws.
- **P3 (characteristic failures).** Ex ante scores S1 below 0 (a loss) and ex post scores S1 and S3
  above 0 in at least 990/1,000 draws.
- **P4 (§6.8, not by construction).** The counterfactual penalty is 0 (below 1e-9) for S1, and
  positive and equal (within 1e-9) for S2 and S4, in at least 990/1,000 draws.
- **P5 (route b).** The target condition classifies S1 and S2 as not manipulation and S3, S4 and S5
  as manipulation, in 1,000/1,000 draws.
- **P6 (route a).** The attitude-independent standard gives S1 and S3 the same score (within 1e-9)
  in 1,000/1,000 draws, and scores S5 below S1 in at least 990/1,000.
- **P7 (§4.3, not by construction).** Across the 1,000 S1 draws, the Spearman correlation between
  ‖V_T − V_0‖ and the Pettigrew aggregate score is below −0.5, and the correlation over S3 draws is
  the same (within 1e-9).

Each prediction is reported as met or not met. A failure of P0 invalidates P2; a failure of P1
means the construction is wrong and is reported as such, not repaired silently. A failure of P4 or
P7 counts against the corresponding claim in Paper 1 and is reported as prominently as a success.
Any change to this plan after the first run is recorded here as a deviation before its result is
read.
