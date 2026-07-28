# Methodology: How Results in This Repository Were Produced

Every experimental claim in the three papers is backed by a run in `experiments/`
that followed the same protocol. This document states the protocol, and then — more
usefully — lists the occasions on which it **cost something**, because a
pre-registration that never changes an outcome is decoration.

## The protocol

1. **Pre-registration before execution.** Each experiment has a
   `PRE-REGISTRATION.md` written *before* the run, fixing the question, the method,
   the success/failure thresholds, and a stopping rule. Where a threshold was later
   found to be mathematically inadequate, it was corrected *before* the run and the
   reason recorded in the same file.
2. **Verdicts issued against the pre-registered criterion**, never renegotiated after
   seeing results. Bands (e.g. "solved ≥ 10/15", "materially better ≥ 8/15") are
   fixed in advance so a middling result cannot be narrated upward.
3. **Raw `result.json` committed** for every run, alongside the figure. The prose
   verdict is written to claim no more than that JSON supports, and the JSON is the
   authority when the two are compared.
4. **Declared attempt budget.** Each experiment states in advance how many attempts
   it gets. When the budget is spent, the limit becomes the result rather than an
   invitation to keep tuning.
5. **Independent audit of the raw output before any paper edit.** Numbers are read
   out of `result.json` and checked against the text; papers are edited only after
   that check.

`experiments/STATUS.md` is the live per-experiment record. Data (`experiments/data/`)
is gitignored; results, code, and pre-registrations are committed.

## Where the protocol cost something

These are the cases that make the protocol more than decoration. Each is a place
where following the rule produced a worse-looking result, a discarded piece of work,
or a correction against interest.

| Case | What the discipline cost |
|---|---|
| **B1 — the stop was obeyed** (`cbra_boundary_residual`) | The pre-registration said Trilha B halts if the boundary residual fails to beat a linear-Gaussian null in ≥ 60% of a pilot. It reached 29%. **B2 and B3 were not run**, and Paper 2's positive arm was declared not currently executable on public data — at the point where continuing would have been most tempting and least defensible. |
| **Pan-Tompkins — a fix that strengthened a negative** (`cbra_boundary_residual`) | A fixed-threshold R-peak detector was found inadequate on I-CARE's heterogeneous ECG (55 peaks on a 118-minute record). Replacing it with an adaptive detector moved the result from a spuriously *higher* 42% to a clearer 29% — i.e. the correction made the paper's own negative *stronger*, and was applied anyway because the detector was broken. |
| **A2 — a pre-registered arm failed, and the rescue was labelled post-hoc** (`sleep_structure_power_dissociation`) | The pre-registered power arm (within-stage high-vs-low natural power) was **not** silent, so by the registered criterion the clean dissociation did not replicate. A pure-amplitude control that *is* silent was added — and marked **post-hoc** in both the pre-registration addendum and the verdict, rather than swapped in as though it had been the plan. |
| **Benchmark — a correction that favoured this project, quarantined** (`baseline_benchmark`) | A first run said the geodesic detector **lost** to baselines. A centre-bias leak was then found (fallbacks returning the record midpoint, which was the true answer) and fixed, reversing the result to a win. Because the correction favoured the project's own method, the verdict records the provenance in full and justifies the fix by an *outcome-independent* impossibility — power-based baselines were scoring 1.00 on a scenario where total power is constant and they cannot beat chance. |
| **Class G — instrument defects found by self-test** (`class_g_coherence`) | Two defects in the periodicity detector (an integer-lag search blind to periods falling between samples; a refinement floor above the pre-registered threshold, misreading a pure sine as aperiodic) were caught by a self-test on signals of known character. The pre-registered threshold was **not** loosened; the numerics were tightened. |
| **E2 → E2-Res — an open regime left open, then closed against expectation** (`high_dim_trichotomy`, `value_base_discontinuity_probe`) | E2's strong-recession cells were reported as *numerically unresolved* rather than claimed either way, and the paper said so. The follow-up then showed the apparent falsifier was a coordinate artifact — a result that helped the thesis, and which was only credible because the earlier run had declined to guess. |
| **EEG-Recon — a headline figure corrected downward** (`eeg_reconciliation`) | The appendix's ≈12× structural effect was traced to an estimator choice and corrected to ≈3.3× under the null the paper commits to. The direction and significance replicated; the magnitude did not, and the paper now reports the smaller number. |
| **Detection repair — a second correction favouring this project** (`detection_statistic_repair`) | The benchmark's sub-chance detection AUC (0.23) was traced to the confidence statistic and repaired to 0.81. Because this again moved an unfavourable finding in the project's favour, the mechanism was **stated as a falsifiable diagnosis and verified before any repair was scored** (real curves more tent-like, 0.83 vs 0.70; nulls higher on peak-to-median, 1.80 vs 1.53), the bar was fixed in advance, the three repairs that *failed* it are reported with their numbers, and the original 0.23 is retained unaltered in the benchmark record. The repair was then re-exposed to failure on data that could not have influenced it (`detection_repair_heldout`): applied unchanged to a paradigm not used to select it, with the bar fixed in advance, it held at AUC 0.82 — and the *old* statistic failed sub-chance a second time, which is the outcome the diagnosis predicted and single-corpus selection could not have shown. |
| **Exp E — a wrong metric found in review, fixed against a favourable direction** (`rl_agents_trichotomy`) | An end-to-end review found the recurrence test measuring **Euclidean** distance on coordinates the integrator had explicitly wrapped to the torus $[0,1)^2$, so every recurrence crossing the wrap boundary was missed — while the companion experiment `high_dim_trichotomy`, on the same kind of torus, used the toroidal metric correctly. The fix can only *raise* recurrence, and the falsifier the experiment hunts is a candidate with positive entropy and **no** recurrence, so the correction runs in the direction that favours the paper. It was applied anyway, on the outcome-independent ground that the distance was simply wrong, and the before/after is on record: recurrence rose 0.9976 → 0.9994 for the gradient candidate and was unchanged elsewhere, with **every classification identical** and the Lorenz value correctly untouched. A verdict string that rounded 0.9954 to "1.00" was tightened at the same time, since the rounded figure read as exact recurrence. |
| **Escape endogeneity — a verdict downgraded to inconclusive by a check nobody required** (`escape_endogeneity`) | The pre-registered rule returned "E2 survives" — every escaping candidate failed a property, exactly as §7.5 asserts. An attribution check run *after* the fact showed the **bounded control failed the same property**, so the failure could not be charged to escape at all. The rule was not rewritten and the computed verdict is still reported; what changed is what may be concluded from it, and the result is recorded as **inconclusive** rather than as the confirmation the letter of the rule allowed. The same run found that the paper's two senses of "openness" (positive entropy in §7.5, protected tangential spectrum in §8.3) come apart, and that the candidate which would decide the question was missing — registered as a follow-up rather than added post hoc, since adding it after seeing the result would be fitting a construction to an outcome. |
| **Escape endogeneity — a published claim withdrawn** (`escape_endogeneity`, `escape_persistence_decider`) | The experiment reported that escaping systems achieve escape, openness *and* non-recurrence at once, concluding that recurrence was not what excluded conversion in that regime. That conclusion **reached Paper 1 and was merged** before the defect was found: crossing the log-radius *measurement* bound was being treated as a finite-time blow-up, which overrode a **measured** recurrence of 0.98 to "non-recurrent". The fix reverses the finding — escaping systems are recurrent in the identity observable — and the paper text was reversed with it. The episode is kept here because the correction ran *against* the direction the previous fix in this table ran, which is the point: the same override was first too narrow (flattering the paper) and then too wide (flattering its critics), and only measuring without overrides at all was right. |
| **Escape decider — the exciting result was the one that got killed** (`escape_persistence_decider`) | A run of this experiment returned **REFUTES_E2** — the headline outcome, a genuine hole in Paper 1's argument. It was rejected, because it depended on the same measurement-bound defect above: the "non-recurrent" candidate had a measured recurrence of 1.000. Against the corrected instrument the verdict is the opposite, and the final result *supports* the paper. A protocol that only ever discards results unfavourable to the author is not a protocol; this is the case where the discarded result was the one an author would most want to keep. |
| **Escape endogeneity — a rigged test caught by its own self-test** (`escape_endogeneity`) | Four instrument defects were found before any result was read, **two of them flattering the paper**: openness was read from a full-state Lyapunov exponent, which is positive under pure uniform expansion, so a frozen-direction blow-up scored as "open"; and a finite-time blow-up was scored as *failing* non-recurrence because the estimator returned NaN on too few samples, when such a trajectory is non-recurrent by construction. A fifth and worse problem was a **design** flaw rather than a coding one: the escaping candidates' directions had been modelled as autonomous flows on the 2-sphere, where Poincaré–Bendixson forbids chaos outright — so "escape kills openness" was unfalsifiable by construction. Corrected, and the self-test now includes a check that an escaping candidate *can* be open, so that this class of rigging fails the build rather than producing a result. |
| **Class G independence — a lapse, recorded** (`class_g_independence`) | The pre-registration for this experiment was written **after** the run, contrary to rule 1. It is recorded in the file itself, in `STATUS.md`, and here, rather than back-dated. The mitigation is that the experiment carries no success/failure threshold — it reports a co-failure matrix and a count, with no bar that could have been moved after the fact — but the lapse is a lapse, and a protocol that hides its own violations is worth nothing. |

## What this does not establish

The protocol constrains how results were produced; it does not make them true. Every
verdict is bounded by the scope stated in its own `result.json` — synthetic results
are about instruments rather than biology, single-corpus results are about that
corpus, and the logical results (e.g. Class G's satisfiability) say nothing about
instantiation. The discipline is a guard against one specific failure mode — running
until something works and reporting only that — and against nothing else.
