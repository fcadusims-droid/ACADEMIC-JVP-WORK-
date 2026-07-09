"""Shared numerical machinery for the JVP experiment suite.

Papers 1 and 3 share a dynamical-systems core (SPD manifold geometry,
jump-diffusion simulation, Helmholtz-Hodge decomposition), so it lives here
rather than being duplicated per experiment.

Nothing in this package is evidence about any real physical, biological, or
theological system. It is measurement, inference, and verification machinery
for the protocols the three papers define.
"""
from . import spd_manifold, jump_diffusion, stats_utils, helmholtz_hodge  # noqa: F401

__all__ = ["spd_manifold", "jump_diffusion", "stats_utils", "helmholtz_hodge"]
