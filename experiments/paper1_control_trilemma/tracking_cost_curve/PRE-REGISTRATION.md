# Experiment F — Cost Curve of the Exogenous (Coercion) Horn (Paper 1)

**Run order: 6th.**

## Question
Paper 1's "costing" of the exogenous-annihilation horn (Sec. 7.3, as edited)
claims that finite-gain trajectory-tracking control pays a **graded, monotone**
agency cost: as tracking gain rises, the agency diffusion `D_ag → 0` and the
agency eigenvalue `lambda_parallel → -∞`. Is the claimed curve actually monotone
and graded, or is that assertion false?

## Method
Run trajectory-tracking control (funnel control / prescribed-performance control)
on a reference dynamical system across a sweep of increasing gain. At each gain,
numerically estimate the effective agency diffusion `D_ag` (residual exploratory
variance) and the parallel agency eigenvalue `lambda_parallel` (contraction rate
toward the prescribed trajectory). Plot both vs gain.

## Pre-registered success criterion
Both curves are **monotone** in gain and consistent with the text: `D_ag`
decreasing toward 0 and `lambda_parallel` decreasing (more negative) without
bound, with the perfect-tracking limit recovering the annihilation claim and
finite gain paying a *graded* (not all-or-nothing) cost.

## Pre-registered failure criterion
If either curve is **non-monotone**, saturates away from the claimed limit, or the
cost is discontinuous rather than graded, this is a real defect and Sec. 7.3 must
be corrected to match what control actually does.

## Stopping rule
One gain sweep on a defensible reference system, with the estimators for `D_ag`
and `lambda_parallel` fixed in advance.

## Status
Pre-registered. Not yet implemented.
