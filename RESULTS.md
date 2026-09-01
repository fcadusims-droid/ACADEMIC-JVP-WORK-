# Results — What the 33 Experiments Found

A reader-facing synthesis of the validation suite. Every number here is read from a
committed `result.json`; `experiments/STATUS.md` is the authoritative per-experiment
record, and this document is the summary of it.

**What this suite establishes, and what it does not.** It tests the papers' *methods
and numeric claims*. Synthetic results are evidence about instruments, not about
biology. Single-corpus results are about that corpus. Logical results — Class G's
satisfiability, the trichotomy — say nothing about whether anything instantiates the
profile. Nothing here is evidence about any real physical, biological or theological
system.

---

## Paper 1 — The Cybernetic Impossibility of Conversion

**The trichotomy survives its strongest adversarial candidates.** No candidate
dynamics is the forbidden object — positive entropy together with absence of
recurrence on a compact set. Gradient flow and curiosity land in Case 1; a Hamiltonian
flow in Case 3; novelty search on a compact torus is bounded-recurrent (1.000); Lorenz
chaos is the one positive-entropy case ($\lambda = +0.88$) and remains recurrent
(0.995). *(`rl_agents_trichotomy`, `poincare_recurrence_check`)*

**The one regime left open was closed against expectation.** The high-dimensional
stress test reported its strong-recession cells as *numerically unresolved* rather
than claiming them either way. The follow-up showed the apparent falsifier was a
coordinate artifact: under E2's own renormalization scheme $\lambda$ climbs
$217 \to 1360$ as $dt$ falls — a $1/dt$ blow-up, the signature of an artifact — while a
controlled full-state scheme converges. *(`high_dim_trichotomy`,
`value_base_discontinuity_probe`)*

**The finite-gain agency cost is graded, not a step.** $D_{ag}$ falls
$0.85 \to 0.012$ and $\lambda_\parallel$ drops $-0.09 \to -11.5$, both monotone; the
perfect-tracking limit is approached continuously. *(`tracking_cost_curve`)*

**Class G is satisfiable and it discriminates.** An explicit stochastic witness meets
all ten conditions against thresholds fixed in advance, and every near-miss in the
paper's own filter table is excluded, each failing a condition the table predicts.
This is logical non-emptiness, not instantiation. *(`class_g_coherence`; formalized
in `formal/ClassG.lean`, where the satisfiability proofs consume **zero** axioms)*

**But "ten conditions" overstates the content.** Only **six** of the ten can be
violated in isolation (1, 2, 3, 4, 6, 9); the rest are entailed by others, two of them
as a matter of logic rather than of this construction. Effective dimensionality is
about six, and the paper now says so. Counted by distinct failure signature the answer
is nine; the defended claim is the lower bound. *(`class_g_independence`)*

**The escape horn closes — but the paper's reason for it was wrong.** Two claims were
travelling together in §7.5:

| claim | verdict |
|---|---|
| escape requires an external occasion | **false** — $\dot\theta = \theta\lVert\theta\rVert$ is autonomous and leaves every compact set in finite time |
| escape forfeits persistence (Λ → Class M) | **false as stated**, though the conclusion survives |

Persistence *survives* escape: quasi-periodic escapers with incommensurable
frequencies retain $P_f = 0.17$–$0.21$ against a $0.05$ bar while running to
$\log r = 25$. What fails universally is **non-recurrence** ($0.81$–$1.00$). The escape
happens in the *radius*; an identity contract reads the *direction*; the direction
lives on a compact quotient where the recurrence theorem applies unchanged. So the
escaping cell closes by the *same* argument as the bounded cell — stronger and more
general. A follow-up then removed the one caveat this had carried: the closure was
thought to depend on a scale-free contract, but a family of **cardinal**
(magnitude-reading) contracts — bounded, linear and exponential — all leave the
observable recurrent too ($0.81$–$0.93$), so the horn closes under every contract
tested and §7.5's persistence argument is vindicated by none of them. The one
apparent persistence collapse (under an $e^{25}$ observable) is a numerical
artefact, since bounded and linear readings of the identical system retain
$P_f = 0.15$–$0.21$. *(`escape_endogeneity`, `escape_persistence_decider`,
`escape_cardinal_contract`)*

---

## Paper 2 — The Conditional Biological Requirements Architecture

**The positive arm halted at a pre-registered gate, and that is the paper's title.**

A dataset search found exactly one public corpus with the three properties the
protocol needs — concurrent cardiac and neural recording, a recovery-versus-non-recovery
contrast, and adequate record length: **I-CARE**. VitalDB is purely I+; the sleep banks
are all I+; ICU-scale data lacks concurrent EEG; seizure banks lack both.
*(`dataset_viability_gate`)*

The gating experiment on that corpus then asked whether the interoceptive boundary
residual beats a linear-Gaussian null. The pre-registration said the track halts below
60%. **It reached 29%** (6 of 21 patients). The downstream experiments were **not
run**. *(`cbra_boundary_residual`)*

**The eliminative arm is what survives, and it is demanding.** Imperfect matching
inflates the false-positive rate three- to sevenfold *independently of sample size*;
even with tight matching a moderate effect needs $n \approx 40$ per condition
*(`dissociation_power_analysis`)*. A genuinely critical generator with no identity
mechanism reproduces the gating differential near criticality, reaching 73% of the
identity-linked reference at the strongest cell *(`criticality_sweep`,
`dissociation_confound`)* — which is why the defensible claim is eliminative rather
than detective.

**A control was added because the confound analysis demanded one, and it comes with a
condition.** Requiring *measured* sub-criticality recovers the test's power — but only
with a **subsampling-robust estimator**. The naive branching-ratio slope is attenuated
($\sigma = 0.94 \to \hat\sigma = 0.79$) and false-certifies 79% of confounded
near-critical systems as safe. The MR estimator removes the attenuation
($\sigma_{MR} = 0.92$). That estimator requirement is now a stated condition in §14.1.
*(`subcriticality_control`)*

**The metabolic null has a quantified resolution threshold**: it absorbs the structured
residual only when finer than $h^* \approx 0.7$–$0.9\,\ell$, and $h^*$ grows with the
diffusion length. *(`metabolic_null_resolution`)*

---

## Paper 3 — The Kinematics of Geodesic Flow

**Structural discrimination replicates on real data, across two paradigms.** N2-versus-REM
discrimination passes **14/15** under a permutation null (median ratio 2.79), and
within-trajectory sleep-onset localization reaches **10/15** — against 4/15 on
eyes-open/closed. The earlier limit was the *paradigm*, not the method.
*(`sleep_stage_localization`, `real_eeg_localization`)*

**Benchmarked against standard methods, with the defeat criterion fixed in advance.**
Against BOCPD, `ruptures` (PELT, binary segmentation, windowed), a Gaussian HMM and
sliding-window $k$-means, on the same data and features. The outcome is genuinely mixed
and is reported on three axes:

| axis | result |
|---|---|
| localization | **10/15** vs best baseline 8/15 — clears the rule, but inside binomial noise |
| detection | initially the **worst** method compared (AUC 0.23), later repaired to 0.81 — competitive, not superior (best baseline 0.88) |
| structure-vs-power | **1.00** vs 0.75 where power is held constant; **0.55** vs 1.00 on the mirror case, losing exactly as its construction requires |

Reporting the mirror case is what makes the pair evidence rather than advocacy.
*(`baseline_benchmark`)*

**A sub-chance result, diagnosed and repaired — then validated out of sample.** The
AUC 0.23 was traced to the confidence statistic, not the geometry: peak-to-median
rewards the null by construction. The diagnosis was stated as a falsifiable prediction
and both halves verified *before* any repair was scored. Four repairs were
pre-registered against a fixed bar; the cheapest passed, lifting detection to **0.813**
with localization unchanged. Applied unchanged to a paradigm not used to select it, it
holds at **AUC 0.824**, while the old statistic fails sub-chance a second time
(**0.434**) — so the *failure* mechanism generalises alongside the fix.
*(`detection_statistic_repair`, `detection_repair_heldout`)*

**A headline figure corrected downward.** The appendix's ≈12× structural effect was
traced to an estimator choice and corrected to **≈3.3×** under the null the paper
commits to. Direction and significance replicated; magnitude did not.
*(`eeg_reconciliation`)*

**Window size, not multiscale — confirmed on real EEG, at a smaller effect.** The large
window reaches **7/16** against the best short window's 4/16, and the multiscale bank
**6/16**, so window size is the operative variable and the bank adds nothing. But the
synthetic $2/15 \to 15/15$ becomes $4/16 \to 7/16$ on real recordings — under half.
*(`localization_multiscale`, `abc_real_eeg`)*

**Declared failure modes.** A structural region where a weak jump is not separable from
drift at any threshold, worsening with longer windows as holonomy accumulates
*(`drift_jump_confusion_sweep`)*. A flat log-Euclidean base metric resolves that corner
(AUC $0.65 \to 0.96$) but costs weak-collapse jump power ($0.85 \to 0.22$), so the
recommendation is square-root primary with a log-Euclidean cross-check
*(`base_metric_corner`, `log_euclidean_real_eeg`)*. A hybrid metric does **not** help
($0.65 \to 0.61$) *(`hybrid_metric`)*. Causal localization is recoverable but pays a
real reporting lag *(`causal_vs_offline_localization`)*. On-line localization is
**materially better, not solved** — a global CUSUM doubles it (4/15 → 8/15), short of
the pre-registered ≥10/15 band *(`online_localization_cusum`)*.

**One replication came back qualified, and the qualification is the finding.** The
pre-registered natural-power arm was *not* silent, so by the registered criterion the
clean structure/power dissociation did not replicate; a pure-amplitude control that
*is* silent was added and marked **post-hoc**. The appendix's clean claim is
paradigm-specific. *(`sleep_structure_power_dissociation`)*

---

## What it cost to run it this way

The protocol is only worth something where it changed an outcome.
`METHODOLOGY.md` lists every such case in full. The load-bearing ones:

- **A halt obeyed** where continuing was most tempting — Paper 2's positive arm stopped
  at 29% against a 60% bar, and B2/B3 were never run.
- **A bug fix that made the paper's own negative stronger** — replacing a broken R-peak
  detector moved the result from a spuriously higher 42% to a clearer 29%.
- **A headline corrected downward** — ≈12× to ≈3.3×.
- **A rescue arm labelled post-hoc** rather than swapped in as though it had been the
  plan.
- **A published claim withdrawn** — an escape finding that had already been merged into
  Paper 1 turned out to rest on a measurement-bound defect, and was reversed in the
  paper.
- **The most exciting result was the one discarded.** A run returned `REFUTES_E2` — a
  genuine hole in Paper 1 — and was rejected because it depended on that same defect.
  A protocol that only ever discards results unfavourable to the author is not a
  protocol.
- **A process lapse recorded rather than back-dated** — one pre-registration was written
  after its run, and says so.

---

## What remains open

- **Paper 1** — the escape-horn closure is now confirmed for cardinal as well as
  scale-free contracts (`escape_cardinal_contract`), so that gap is closed. What
  remains: the Poincaré and Conley axioms in the Lean development are still axioms;
  discharging them from Mathlib is blocked by the environment's egress policy, not by
  the mathematics.
- **Paper 2** — the positive arm is not currently executable on public data. Reviving it
  needs a new mechanism idea or a corpus that does not yet exist, not another run.
- **Paper 3** — on-line localization of transitions that are not the dominant geometric
  event in their record remains open: a permanence-explicit detector, scoring each
  split by whether its post-segment matches the state the record ends in, was tried
  (`online_localization_permanence`) and reached only 3/15, below CUSUM's 8/15 and the
  10/15 band. Experiment **B** remains synthetic-only (its real-data arm here is an
  *analogue*, not a replication), and experiment **C** is untested on real data
  entirely.
