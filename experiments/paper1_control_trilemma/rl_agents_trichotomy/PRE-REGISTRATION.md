# Experiment E — Trichotomy Test with Real Learning/Evolution Agents (Paper 1)

**Run order: 7th.** The experiment that gives teeth to the Sec. 7.5/7.6 defence.
If it fails, that section must be rewritten — better to find out now than for a
referee to.

## Question
The Meta-Optimization Collapse Theorem claims an autonomous preference dynamics
`theta_dot = f(theta)` on a **compact** value space falls into a trichotomy:
Case 1 gradient descent on a meta-potential (integrable), Case 2 unbounded
dispersion, Case 3 bounded recurrence. Do **real** learning/evolution agents obey
it — or does some agent falsify it?

## Method
Implement agents with endogenous preference dynamics (reward/value parameters
`theta` updated by a meta-objective): e.g. meta-learning with a parameterised
reward, and novelty-search / intrinsic-curiosity agents (Lehman & Stanley;
population-based training with meta-optimised hyperparameters). Log the
`theta`-flow over training. Use `shared_lib.helmholtz_hodge` to extract the
gradient / divergence-free split of the flow field and classify each trajectory
into Case 1 / 2 / 3.

## Pre-registered falsification target (the real test)
Search **specifically** for a system exhibiting *positive entropy on the attractor
AND absence of recurrence simultaneously on a compact set* — the object the
theorem says cannot exist. The strongest candidates named in the text are pure
novelty search, intrinsic curiosity, and PBT with meta-optimisation. Run those as
adversarial cases.

## Pre-registered success criterion (for the theorem)
Every tested architecture that genuinely stays on a compact value set classifies
into exactly one of the three cases; no compact-set agent shows positive-entropy-
plus-no-recurrence. Report the empirical classification of ~5–8 architectures.

## Pre-registered failure criterion (falsification of the defence)
If any compact-value-space agent robustly shows positive attractor entropy with no
recurrence, the trichotomy is **falsified** and Sec. 7.5/7.6 must be rewritten.
This outcome is to be reported as prominently as a confirmation.

## Stopping rule
~5–8 architectures including the three adversarial candidates. Do not keep adding
architectures until one confirms; the adversarial cases are the decisive ones.

## Status
Pre-registered. Not yet implemented. (Requires `gymnasium`/`torch`; see
`requirements.txt`.)
