# Paper 2 — CBRA Protocol (Phase 3)

Scope is deliberately narrow: **simulation cannot confirm CBRA.** It can only say
whether the statistical design is feasible before spending on real subjects. No
in-silico result here is evidence that tissue implements anything.

| Exp | Folder | Tests |
|---|---|---|
| **H** | `dissociation_power_analysis/` | Statistical power of the `M_diss` dissociation test — feasible at realistic sample sizes? |
| **I** | `criticality_sweep/` | Is the critical-generator confound (Sec. 15.5) robust or fragile across parameters? |
| **J** | `metabolic_null_resolution/` | At what spatial resolution does the strong null actually absorb the residual? |

Each folder has a `PRE-REGISTRATION.md`. The deliverable of this phase is a
**feasibility verdict** — "is this protocol executable with realistic resources, or
does it demand unattainable statistical power?" — not a biological result.
