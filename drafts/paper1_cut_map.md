# Paper 1: cut map (round 1 applied; round 2 and the appendix map await approval)

## Status (2026-09-26)

**Target, corrected by the author.** Synthese's guideline of 15–30 printed pages covers the whole
article. The target is therefore:
- body plus notes: at most **13,500** words;
- appendix: at most **2,500** words;
- references: no target, but any reference that loses its citation leaves the list.

That is roughly 17,500 words in all, about 33 pages. It replaces the earlier rule (15,000 words
excluding the appendix and references), under which the article would have run to about 45 pages.

**Round 1 is applied.** The author approved it with the changes listed below. The pre-cut text is
`drafts/paper1_precut_2026-09-26.md`, which already includes the author's corrections to §6.6 and §8.4.

| | Words (body + notes) |
|---|---|
| Before the author's corrections to §6.6 and §8.4 | 25,107 |
| After those corrections (the pre-cut text) | 25,428 |
| After round 1 | **14,256** |
| Target | ≤ 13,500 |
| Still to cut | **≥ 756** |
| Appendix now / target | 5,070 / ≤ 2,500 |

*Counting method.* The count is whitespace-separated tokens from `## Abstract` up to the appendix,
plus the footnote. The earlier figure, 25,129, came from a slightly different tokenization of the
same text.

**How round 1 was applied, and where it differs from the table below.**
- **Rows applied as approved:** F1–F7, F9–F11, T1–T4, T6, T7, T9–T11, T13–T18, L1, L3, L4, L6, L7,
  G1–G3, U1 and C1. **Reserve applied:** R1, R2 and R3. **R4 was rejected**, so the deflationary
  alternative (§6.4) keeps about 190 words.
- **F8.** "Limitative theorems" appeared nowhere else in the body, so the whole paragraph was removed.
  The qualification rule that guarded the phrase was withdrawn from `experiments/qualifications.json`.
  The Nayebi reference annotation no longer cites §2.1.
- **T5.** Condensed to about 510 words, with one paragraph per architecture.
- **T8.** Removed. A 59-word pointer stays in the body and carries the second `[^lean]` anchor.
- **T12.** Condensed to about 280 words, with its content updated:
  - what §6.6 settles: which system a contract may be about, namely the bearer of the
    responsibility-bearing history;
  - what stays open: which readings of that bearer's value state are admissible, and so whether
    every admissible contract factors through a bounded reading.

  Both qualification phrases are kept.
- **L2.** One clause each for Frankfurt, Korsgaard, Parfit and Bratman. Taylor, Kuhn and MacIntyre
  were removed, together with their four reference entries (Taylor has two).
- **L5 and R1.** §7.7 is now 153 words. Omohundro, Hubinger and Everitt left the list.
- **U1 and R3.** §9 keeps the definition, the post-jump criterion and the reason §7.6 needs the
  profile (120 words). Subsections 9.1–9.3 are gone from the text and the table of contents; the
  conditions remain in A.6.
- **L7.** One clause added to §7.4 on Bradley's first model, classical conditioning. §8.4 already
  cited "§7.4, Bradley's first model", but §7.4 did not mention it. The clause is taken from the
  verified notes (`references/paper1_phase3_literature.md`).
- **Cross-references repaired:**
  - §7.3 cited "§2.1" for the premise; it is now §2;
  - the A.6 heading now points to §9, not §9.3;
  - the table of contents no longer lists the glossary.

**Reference classification (item 4 of the decision).** Apart from the references the author named,
the map had flagged these:

| Reference | Rule applied | Result |
|---|---|---|
| Adams et al. 2017 | priority (same recurrence argument for externality) | kept, one clause in §6.5 |
| Conley 1978 | priority | kept, §6.5 |
| Carroll et al. 2024 | priority (alignment under changing preferences) | kept, §7.5 |
| Aubin 1991, Ames et al. 2019 | the viability-theory counterpart of conditions 1–5 | kept, §8.3 |
| Haken 1983, Carr 1981 | the dynamical rationale for the decomposition | kept, §8.1 |
| Soares 2015, Hadfield-Menell 2016, Russell 2019, Nayebi 2025, Wang 2025 | the corrigibility claims that §7.7 keeps | kept |

Five references were cited without a year (Lehman and Stanley, Schmidhuber, Singh et al., Bowles
and James), so the citation check could not match them. The years were added. Paper 1 now has
57 references (64 before). The audit record was rebuilt, with the removed entries taken out of
`references/auto_paper1.json`.

## Round 2: proposals to reach 13,500 (nothing applied)

Protected, as instructed:
- the abstract;
- §3, §4.1 and §4.2;
- §6.6 and §8.4;
- the §7 introduction, §7.3 and §8.2;
- the two §8.3 tables.

"Now" is measured; "saves" is an estimate. The core rows (S1–S8) sum to 791, which gives about
13,465.

| # | Where | Now | Action | Saves | What the argument loses | Gates / references |
|---|---|---|---|---|---|---|
| S1 | §6.5 "The closure of the trichotomy" | 236 | Condense to ~120. Drop the parenthesis about the withdrawn "confirmed directly" sentence (its history is in the repository) | 116 | The in-text record of a withdrawn claim. The measure-preserving/dissipative distinction stays | — |
| S2 | §6.5 summary table of the three horns | 107 | Remove | 107 | A table restating §6.2–6.4. The "conjunction is the result" paragraph stays | — |
| S3 | §6.7 "costing" paragraph | 254 | Condense to ~130 | 124 | The funnel-control detail (in §6.3) and the "600 lines of dynamics" sentence | Ilchmann and Bechlioulis stay cited in §6.3 |
| S4 | §6.7 opening paragraph | 191 | Condense to ~100 | 91 | The bachelor analogy and part of the statement of the vacuity worry | — |
| S5 | §8.1 four-way table, its lead-in and the closing sentence | 138 | Remove | 138 | A contrast the §8.3 candidate table already draws (damping, forcing, feedback, coercion) | — |
| S6 | §8.1 forcing/Class G bullets and "Both can pass…" | 162 | Merge into ~80 | 82 | Some wording. The dimensionality contrast stays; the formal version is in A.2 | — |
| S7 | §7.5 Arpaly paragraph | 135 | Condense to ~60 and update it | 75 | The paragraph still says Huck's case is "not obviously externally occasioned" and "the clearest test the framework has not passed". After the author's correction, §8.4 treats Huck as a candidate if the occasion is external (Jim) and §6.6 puts purely internal change inside the boundary. The condensed text would point to §8.4 | Arpaly stays |
| S8 | §2 "Failure conditions of the critique" | 108 | Condense to ~50 | 58 | The three failure conditions become one sentence | — |

Reserve:

| # | Where | Now | Action | Saves | What the argument loses |
|---|---|---|---|---|---|
| S9 | §2.1 first two paragraphs | 187 | Condense to ~100 | 87 | The perpetual-motion analogy and the "dominant paradigm" paragraph |
| S10 | §5 closing paragraph | 134 | Condense to ~70 | 64 | Part of the P/Lambda contrast and the bridge to §6 |
| S11 | §6.2 two argument paragraphs | 294 | Condense to ~180 | 114 | Detail on requisite variety; the "self-salvation" gloss, which belongs to the companion paper |
| S12 | §8 opening two paragraphs | 153 | Condense to ~80 | 73 | "Admissibility predicate, not mechanism" is said twice; once remains |
| S13 | §7.1 concession paragraph | 170 | Condense to ~120 | 50 | Wording |

## Appendix map to 2,500 (nothing applied)

To keep, as instructed:
- the theorem's statement (A.3, first paragraph, 250 words);
- the Class G conditions in symbols (A.5 table);
- the satisfiability witness, including the measured $D_c$ checked by `claims.json` (A.5,
  satisfiability paragraph, 310 words).

The core rows sum to 2,629, which gives about 2,441.

| # | Where | Now | Action | Saves | What is lost | Gates |
|---|---|---|---|---|---|---|
| AP1 | A.1 taxonomy | 749 | Keep only the correlation-power definition (~150). The class descriptions and the comparison table go; §5 already defines the classes | 599 | The Lambda comparison table (quasi-periodicity, metastability, long memory) | — |
| AP2 | A.2 decomposition | 444 | Keep the formal decomposition (~120). Drop the 277-word "distinction is technical" paragraph, which restates §8.1 | 324 | A second statement of the forcing/reconfiguration contrast | — |
| AP3 | A.3 "Two limitations" | 654 | Condense to ~200. Keep the bounded-reading closure and the conditional wording | 454 | The long discussion of unbounded drift and the three sampled contracts | **Qualification rule:** "closed by the *same* argument as the bounded cell" must keep "bounded reading" or "conditional" in its paragraph |
| AP4 | A.5 independence paragraph | 378 | Condense to ~120 | 258 | The per-condition breakdown of which conditions are entailed; "about six independent constraints" stays | — |
| AP5 | A.6 U-limit predicate | 1,244 | Keep the displayed predicate and its definitions (~250). The $\Omega_I$ discussion and the continuity floor go to one sentence each | 994 | The full argument that $\Omega_I$ is a product of the transformation, not an input, and the continuity floor | — |

Appendix reserve: A.3 Case 3, 434 → ~200 (saves 234; loses the attractor-by-attractor
discussion).

## What the author needs to decide

1. Approve, change or strike each of S1–S8, and pick reserve rows if needed.
2. Approve, change or strike AP1–AP5.
3. S7 is also a consistency fix. Its current text contradicts the corrected §8.4. If S7 is struck,
   that paragraph should still be updated.

---

## Round 1 map (as prepared; applied with the changes above)

*Original introduction, kept for the record:*


*Prepared 2026-09-26, after §6.6 and §8.4 were inserted. The count follows the author's rule:*
*body plus notes; excluding the references, the appendix and the table of contents, which is not
part of a submitted manuscript. Counts are whitespace-separated tokens, so a formula counts as
one word per space-separated piece.*

| | Words |
|---|---|
| Current count | **25,129** |
| Target | **≤ 15,000** |
| Cut needed | **≥ 10,129** |

"Now" is the measured length of the passage. For a condensation, "saves" is the measured length
minus a target length. The target is my estimate of what the passage needs, so the real saving
is known only after rewriting. The core rows (1–41) sum to exactly 10,129, which leaves no
margin. The reserve (R1–R4) exists for that reason.

**Gates.** No cut touches a number checked by `experiments/claims.json`. The only Paper 1 claim
is the measured $D_c$ in Appendix A.5, which is not in the count. Rows where a qualification
rule or the citation audit is involved say so:
- two qualification rules must stay satisfied (F8, T12);
- some references would lose their only citation. References are not in the count, but an
  uncited reference has to leave the list and the audit record.

**A caveat on moving material to the appendix.** The author's count excludes the appendix, so
moving text there shortens the counted body. But Synthese's guideline, "typically between 15 and
30 printed journal pages", covers the whole article, appendix and references included.
- The appendix is about 5,000 words now; the references are about 1,700.
- With the three moves marked **M** (1,470 words), the article would be roughly 15,000 + 6,500 +
  1,700 ≈ 23,000 words, or about 45 printed pages. That is above the typical range.
- For that reason each move below also has a "remove" alternative, and the appendix itself may
  need trimming later.

## Core map

### Front matter, §1, §2

| # | Where | Now | Action | Saves | What the argument loses | Gates / references |
|---|---|---|---|---|---|---|
| F1 | Glossary | 675 | Remove (**M** alternative: move to appendix) | 675 | A quick-reference table; every term is defined where it is introduced | — |
| F2 | §1 "The argument in condensed form" (7 short paragraphs) | 312 | Remove | 312 | A one-page summary that duplicates the abstract and the roadmap paragraph | — |
| F3 | §1 first four paragraphs | 492 | Condense to ~300 | 192 | The "three errors about identity" framing, reduced to one sentence | — |
| F4 | §2 opening cluster: genre, "What kind of paper this is", "Scope and non-claims", five-step outline, notation paragraph, levels table | 529 | Condense to ~200 | 329 | What the paper does and does not claim is now stated three times; once remains | — |
| F5 | §2 "Two delimitations" | 426 | Condense to ~150 | 276 | The restated theorem outline (it is in §6.5); both conditions stay | — |
| F6 | §2 "Scope, summed" + *Domain* + *Status of the formalism* | 414 | Condense to ~180 | 234 | The three-tier discussion of the formalism's status becomes one sentence per tier | The `[^lean]` footnote is anchored here and in T8; keep one anchor |
| F7 | §2 objection table | 716 | Keep 6 rows (~300): tautology, "rediscovers", modern control, open-ended methods, ordinary influence, U-limit | 416 | Signposting for 8 objections that the text still answers | — |
| F8 | §2.1 limitative-theorems disclaimer | 387 | Condense to ~100 | 287 | The Gödel/Tarski/Rice detail and the Nayebi contrast (Nayebi stays in §7.7) | **Qualification rule:** a paragraph saying "limitative theorems" must also say "analogy of form" or "formal kinship" |
| F9 | §2.1 objection about notation | 271 | Condense to ~80 | 191 | The "a priori syntactic limitation tool" defence, reduced to its conclusion | — |
| F10 | §2.2 identity functional | 452 | Condense to ~300 | 152 | Repetition of the circularity worry (§4.1 has the locks) | — |
| F11 | §4.3 failure cases | 127 | Condense to ~70 | 57 | One sentence of each worked failure | — |

### §6

| # | Where | Now | Action | Saves | What the argument loses | Gates / references |
|---|---|---|---|---|---|---|
| T1 | §6.3 "A critical qualification" (trigger vs tracking) | 230 | Condense to ~100 | 130 | The anaesthesia/locus-coeruleus example and the companion-paper link. The trigger/tracking distinction stays: §6.5 depends on it | — |
| T2 | §6.4 circularity paragraph | 320 | Condense to ~120 | 200 | The survey of literatures that attest the axiological discontinuity | — |
| T3 | §6.4 dynamic-programming paragraphs | 315 | Condense to ~180 | 135 | Part of the explanation of why the value function is singular | — |
| T4 | §6.4 deflationary alternative | 456 | Condense to ~180 | 276 | Detail of the "latent coordinates" reply; the conditional conclusion stays | — |
| T5 | §6.5 "Does modern control escape?" (dual control, switched/hybrid, adaptive/RL, common structure) | 906 | Condense to ~350 | 556 | Per-architecture detail; the common-structure conclusion stays | Feldbaum 1965 and Liberzon 2003 are cited only here: keep a clause each, or remove them from the list |
| T6 | §6.5 "The negative force of this result…" | 102 | Remove | 102 | A restatement of the preceding paragraph | — |
| T7 | §6.5 status of the exhaustiveness premise | 366 | Condense to ~150 | 216 | Overlap with §6.7; the concession and the three named families stay | Lehman, Schmidhuber, Singh and Bowles are cited only here: keep the names |
| T8 | §6.5 "What the theorem excludes" | 348 | **M**: move to A.3 with a ~60-word pointer (or remove; the appendix already has the corrected forms) | 288 | The four measure-theoretic qualifications leave the body; the pointer keeps "typical states only, interpretive for dissipative transients" | Carries the second `[^lean]` anchor |
| T9 | §6.5 relation to prior art | 356 | Condense to ~100 | 256 | Detail; the attribution to Conley and Skoulakis et al. stays | Keep the Skoulakis citation |
| T10 | §6.5 non-autonomous ≠ coercion | 341 | Condense to ~170 | 171 | A restatement of §6.3's distinction; the bold thesis sentence stays | — |
| T11 | §6.5 bounded-region bullets | 140 | Condense to ~40 | 100 | Detail already in A.3 | — |
| T12 | §6.5 open problem ("What remains open…") | 970 | Condense to ~300 | 670 | The extended discussion of whether the problem is well posed under §2.2 | **Qualification rule:** the paragraph must keep "first open problem this argument leaves" together with "pragmatic-indexing metamodel" |
| T13 | §6.7 "What an analytic frame still buys: sorting" | 193 | Condense to ~100 | 93 | The periodic-table and type-system analogies | — |
| T14 | §6.7 stopping rule | 412 | Condense to ~220 | 192 | Repetition; the criterion and the Bradley precedent stay | — |
| T15 | §6.7 "The division of labor…" (theology) | 255 | Condense to ~40 | 215 | The theology/formalism settlement, which now belongs to the companion paper | — |
| T16 | §6.8 simulations | 190 | Condense to ~60 | 130 | The three bullet summaries; the pointer to the repository stays | — |
| T17 | §6.1 | 373 | Condense to ~250 | 123 | Some of the setup of the three strategies | Wiener and Sutton & Barto are cited only here: keep them |
| T18 | §6.3 other four paragraphs | 720 | Condense to ~550 | 170 | Restatements of the agency cost | Ilchmann and Bechlioulis must stay cited (here or in §6.7) |

### §7

| # | Where | Now | Action | Saves | What the argument loses | Gates / references |
|---|---|---|---|---|---|---|
| L1 | §7.2 Paul | 314 | Condense to ~220 | 94 | Part of the epistemic-versus-structural comparison | — |
| L2 | §7.5 one-line engagements (Frankfurt, Taylor, Korsgaard, Parfit, MacIntyre, Kuhn, Bratman) | 288 | Condense to ~120 | 168 | Each thinker's specific contribution is reduced to a clause | Taylor ×2, Kuhn, MacIntyre, Bratman ×2, Korsgaard 2009 and Frankfurt are cited only here: keep a clause for each, or remove them from the list |
| L3 | §7.5 priority paragraph | 256 | Condense to ~150 | 106 | Detail on Ullmann-Margalit, de Blanc, Carroll 2024 and Villiger | de Blanc and Villiger are cited only here |
| L4 | §7.6 non-vacuity check | 698 | Condense to ~500 | 198 | Some exposition of the three members of the class | — |
| L5 | §7.7 corrigibility | 719 | Condense to ~300 | 419 | Omohundro, mesa-optimization and reward tampering reduced to a sentence; Soares, value learning, Nayebi and Wang stay briefly | Omohundro, Hubinger and Everitt are cited only here |
| L6 | §7.1 "convergence" paragraph and closing paragraph | 279 | Condense to ~160 | 119 | Part of the account of how Callard's aspirant might occupy the residual space | — |
| L7 | §7.4 | 447 | Trim to ~400 | 47 | Wording only | — |

### §8, §9, §10

| # | Where | Now | Action | Saves | What the argument loses | Gates / references |
|---|---|---|---|---|---|---|
| G1 | §8.1 "repair loop" cluster (six paragraphs, from "A reasonable objection…" to "This also fixes the precise sense…") | 1,383 | Condense to ~450 | 933 | The extended objection-and-reply sequence on maintenance versus establishment. The distinction and the "generator, not set-point" point stay. The paragraph on the tension with Paper 2 goes, because it is Paper 2's concern | — |
| G2 | §8.3 "The conjunction may nonetheless be empty…" | 129 | Condense to ~60 | 69 | Part of the discussion of empty cases | Aubin and Ames are cited in §8.3: check they stay |
| G3 | §8.1 remaining paragraphs | ~580 | Condense to ~480 | 100 | Wording | Haken and Carr (knife-edge paragraph) stay |
| U1 | §9 U-limit | 757 | **M**: keep a ~250-word statement and the four conditions; move the isomorphism and topology argument to A.6 (or remove it; the full text is preserved in `drafts/paper1_full_2026-09-26.md`) | 507 | The body keeps what the U-limit is and why §7.6 needs it, but not the argument that distinguishes it from coercion | — |
| C1 | §10 conclusion | 475 | Condense to ~250 | 225 | Restatement | — |

**Core total: 10,129 words, which gives a projected count of 15,000.** There is no margin, so
some reserve items will be needed.

**Untouched by choice:**
- the abstract;
- §3, §4.1, §4.2, §5, §6.2;
- **§6.6 and §8.4**, just written;
- the §7 introduction, §7.3 and §8.2;
- the §8.3 condition table and the §8.3 candidate table.

## Reserve (pick as needed for margin)

| # | Where | Action | Saves | What the argument loses |
|---|---|---|---|---|
| R1 | §7.7 corrigibility | Reduce to one ~150-word paragraph instead of L5's ~300 | +150 | The AI-safety audience mostly loses its section |
| R2 | §2 objection table | Remove entirely instead of F7's six rows | +300 | All signposting; §6.7 and §8.4 still answer the main objections |
| R3 | §9 U-limit | Keep only its definition and the "why §7.6 needs it" sentence (~100) instead of U1's ~250 | +150 | The four conditions move to the appendix too |
| R4 | §6.4 deflationary alternative | Reduce to two sentences instead of T4's ~180 | +130 | The one reply that could remove the optimization horn, reduced to its statement |

## What the author needed to decide (round 1, done)

1. Approve, change or strike each row. Where the author approves fewer rows, the reserve fills
   the gap.
2. Choose, for T8, U1 and F1, between **move** and **remove**, bearing in mind Synthese's page
   guideline.
3. For each reference at risk, choose between keeping a clause that cites it and removing it from
   the list. The audit record is rebuilt either way.

After approval the cuts will be applied in one pass, with the full pre-cut text preserved, and
the gates, PDF and count re-run.
