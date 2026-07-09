# Experiment B — Informative Prior on the Predictability Covariate (Paper 3)

**Run order: 3rd.**

## Question
The jump is currently anchored to the raw peak of the conditional residual
variance `gamma_t`, with no smoothing. Does **adaptive causal smoothing** of
`gamma_t` before taking the argmax reduce sensitivity to spontaneous local
fluctuations and improve localization?

## Method
Insert a causal smoothing kernel (adaptive bandwidth) on the predictability
covariate produced by `shared_lib.jump_diffusion.conditional_residual_variance`
before the argmax anchor in `stats_utils.glr_jump_test`. Sweep the bandwidth.
Evaluate on the same 15-subject concatenated records as Exp A, same ±2 s scoring.
Must not blur out a genuine sharp transition (guardrail: check jump-detection
power on synthetic collapses does not drop below the appendix baseline).

## Pre-registered success criterion
A bandwidth range in which localization improves over the 5/15 baseline (ideally
combined with Exp A) **while** synthetic-collapse jump power stays ≥ its
pre-smoothing value — i.e. smoothing buys robustness without costing sharpness.

## Pre-registered failure criterion
If every bandwidth that improves real-data localization also drops synthetic jump
power materially (a strict trade-off), smoothing is reported as **not a free
improvement** and not adopted.

## Stopping rule
Shared with Exp A: the A+B+C stopping rule governs whether localization is
declared fixed or a confirmed limitation.

## Status
Pre-registered. Not yet implemented.
