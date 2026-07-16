# Phase 0 — Viability Gate for the CBRA Dissociation Test (Paper 2, Trilha B)

**Written before any dataset is inspected.** This gate decides whether the CBRA
identity-linkage dissociation test (§14.1, $M_{\text{diss}}$) is executable on
*existing public data at all*, before a single line of Trilha-B analysis code is
written. The failure mode this guards against is running a suite of experiments
and discovering at the end that none of them tested CBRA — only generic cortical
geometry (which is Paper 3's job, not Paper 2's).

## The single question

Does there exist **≥ 1 openly accessible dataset** with all **three** properties
holding *simultaneously in the same records*?

1. **Right substrate.** A concurrent cardiac / interoceptive channel
   (ECG, HRV, or PPG) recorded *simultaneously* with the neural signal (EEG/MEG).
   Without this the analysis tests cortical shape geometry (Paper 3), not the
   interoceptive *boundary* the CBRA receptivity-proxy hypothesis is about
   (Paper 2, Path C).
2. **$I^{+}/I^{-}$ contrast.** Pairs of transitions of *different* $I$-status —
   at least one $I$-preserving ($I^{+}$: an agent expected to resume the same
   identity-bearing trajectory, e.g. reversible anesthesia, physiological
   sleep-wake) **and** at least one $I$-breaching ($I^{-}$: a transition across
   which the $I$-constitutive invariant is not required/expected to be preserved,
   e.g. non-recovering deep hypothermic circulatory arrest, or a matched
   non-recovering control) — with **pairable surface dynamics** (arousal level,
   metabolic depth, gross macroscopic state matchable to sd $\lesssim 0.3\sigma$,
   the matching tolerance Exp H showed is required before false positives inflate
   3–7×).
3. **Length for a subsampling-robust criticality estimate.** Records long enough
   (and with enough simultaneously observed units/channels) to estimate
   distance-to-criticality on the boundary process with the **MR / multistep-
   regression** estimator (Wilting–Priesemann 2018). The SubCrit experiment
   proved the naive lag-1 slope fails in the dangerous direction on short
   subsampled traces, so "measurable sub-criticality" (§14.1's fourth honesty
   condition) requires an MR-viable record, not merely any record.

## Decision criterion (fixed now, before looking)

- **PASS** — a dataset satisfying **all three** is found and *named*. Trilha B
  (B1 → B2 → B3) is then designed and run on that named dataset. The gate records
  the dataset, its access route, and how each of the three properties is met.
- **FAIL** — no such dataset is found within the bounded search below. This is a
  **publishable result, not a failure to be worked around**: it means the CBRA
  dissociation test "is not executable with available public data," which becomes
  an *added honesty condition* on §14.1 (alongside the ethical and matching
  conditions already there). Trilha B is not run; only Trilha A (Paper-3 extended
  validation) proceeds. The gate records *which* of the three properties each
  candidate fails, so the negative result is specific, not a shrug.
- **PARTIAL / CONDITIONAL** — a dataset meets properties 1 and 3 but the
  $I^{+}/I^{-}$ contrast (property 2) is only *approximable* (e.g. only $I^{+}$
  transitions exist publicly, or $I^{-}$ exists only in animals, or matching is
  not auditable). This is reported as a *near-miss* and treated as FAIL for the
  purpose of running B3 (the dissociation needs a genuine contrast), while noting
  exactly what a future private/animal dataset would need to add.

## Bounded directed search (the whole search, declared in advance)

Named candidates to verify from primary documentation (not memory):

- **Anesthesia banks** with simultaneous neuromonitoring + vitals (VitalDB,
  BIS/EEG + ECG intra-op records) — the most plausible $I^{+}$ substrate
  (reversible = $I^{+}$, depth pairable). Check for any $I^{-}$ arm.
- **ICU waveform banks** (MIMIC-III/IV Waveform, eICU) — ECG abundant; the
  question is whether concurrent EEG exists at all, and whether any
  non-recovering ($I^{-}$) vs recovering ($I^{+}$) transition is annotated.
- **Sleep banks with ECG** (Sleep-EDF, SHHS, MESA, ISRUC, MASS, PhysioNet
  Cyclic-Alternating-Pattern) — many have concurrent ECG; but sleep transitions
  are all $I^{+}$, so the $I^{-}$ arm is the likely failure.
- **Seizure/epilepsy EEG** (CHB-MIT, Temple TUH) — check for concurrent ECG and
  for any $I$-status contrast.
- **Cardiac-arrest / coma / prognostication EEG** (e.g. post-arrest coma
  outcome datasets) — the one place a genuine $I^{-}$ (non-recovery) vs $I^{+}$
  (recovery) contrast could plausibly exist with concurrent ECG; verify access
  and matching feasibility specifically.

Verification standard: for each candidate, record from its *published
documentation* (a) concurrent cardiac+neural yes/no, (b) whether any $I^{+}/I^{-}$
contrast with pairable surface dynamics exists, (c) record length / channel count
for MR feasibility, and (d) open-access status. A candidate counts toward PASS
only if all four are affirmatively documented.

## Budget

One bounded directed pass over the named candidates (documentation-level
verification; no attempt to download every corpus). If nothing satisfies all
three after that pass, the practical answer is "not available," and the gate
returns FAIL/CONDITIONAL with the per-candidate breakdown. No extension: an
open-ended hunt would itself become the CBRA-validation bias the pre-registration
exists to prevent.

## Output

`result.json` recording, per candidate, the four verification facts and the pass
flag; a single overall verdict (PASS with named dataset, or FAIL/CONDITIONAL with
the specific missing property); and, if FAIL/CONDITIONAL, the exact wording of the
added §14.1 honesty condition. The prose verdict claims no more than the recorded
per-candidate facts support.

## Status
Run (2026-07-16). Verdict: **PASS** — I-CARE (PhysioNet i-care/2.1) is the one
public dataset satisfying all three properties (concurrent EEG+ECG; I+/I- via CPC
recovery-vs-non-recovery, Sec 14.1's sanctioned matched non-recovering control;
hours-to-days 22-channel records for MR). PASS is narrow and carries two empirical
gates for Trilha B: (B1) confirm the ECG usable subset on download; (B3) define
the within-record transition and audit surface-dynamics matching to sd<=0.3 sigma.
VitalDB is the pure-I+ substrate (no I- arm); sleep/ICU/seizure banks each fail a
specific property (recorded per-candidate in `_results/dataset_viability_gate/result.json`).
