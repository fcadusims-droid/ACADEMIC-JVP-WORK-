# Experiment J — Spatial Resolution of the Metabolic Null (Paper 2)

**Run order: 10th (last).**

## Question
Paper 2, Sec. 7.2 argues qualitatively that a spatially-resolved / strong
operational null absorbs the residual that a weak null leaves. **At what spatial
resolution** does the null actually absorb the boundary residual? Turn the
qualitative claim into a number.

## Method
Simulate the Sec. 7.2 argument with a simplified energy-diffusion model of the
substrate: an active-boundary source term plus a null model that observes the
substrate at a controllable spatial resolution. Sweep the null's resolution and
measure how much of the structured boundary residual survives after the null has
absorbed everything it can, as a function of resolution.

## Pre-registered success criterion
A concrete resolution threshold (a number, with its dependence on the diffusion
length and source geometry) above which the strong null absorbs the residual and
below which structured residual survives — replacing the qualitative claim with a
quantitative one.

## Pre-registered failure criterion
If the residual either always survives or always vanishes regardless of resolution
(no threshold), the Sec. 7.2 weak-vs-strong-null distinction is not
resolution-driven in this model and the argument must be restated.

## Stopping rule
One diffusion-model sweep with pre-fixed source geometry and diffusion length.

## Status
Pre-registered. Not yet implemented.
