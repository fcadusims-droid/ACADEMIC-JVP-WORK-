# Paper 1, phase 3: formal models of value change, and the exogenous horn in alignment

*Compiled 2026-09-26 for the Paper 1 development plan (phase 3). Each entry was checked against
Crossref or the publisher's record. Where the text was read, the entry says so. "Supports",
"complicates" and "contradicts" are relative to the novelty thesis chosen in phase 1:*

> Formal models that direct, evaluate or explain value change locate a fixed evaluative point.
> When they are used to direct change, they are control in the paper's sense and inherit the
> trilemma. When they only represent change, they represent it either as reabsorption (a moving
> coordinate within a fixed higher-order structure) or as a change of fundamental values about
> whose production they are silent.

## 3.1 Formal models of preference change

### Dietrich and List 2013, "Where do preferences come from?"
- **Record.** *International Journal of Game Theory* 42(3): 613–637, DOI 10.1007/s00182-012-0333-y
  (online 2012). Full text read in the LSE Research Online version.
- **What it says.**
  - Preferences over alternatives are derived from a *weighing relation* over combinations of
    "motivationally salient" properties.
  - Preferences change when the set of salient properties changes. Which properties are salient
    is a primitive of the model, and a "motivation function" maps observable contexts to
    motivational states.
  - The authors are explicit that the deep structure does not change. "The underlying stable
    feature characterizing an agent is not the agent's preference order … but the agent's
    weighing relation over property combinations", and "while the agent's weighing relation is
    stable on this picture, his or her motivational state is variable". In a footnote: "in our
    model preference change goes along with a stable weighing relation."
  - How the agent comes to have a weighing relation "in the first place" is outside the model.
- **Verdict: supports, and forces a correction of wording.**
  - *Supports.* It is the clearest formal instance of the structure the paper calls
    reabsorption. First-order preferences change because a coordinate (salience) moves inside a
    fixed higher-order evaluative structure (the weighing relation). A change of the weighing
    relation itself, which is what conversion would be, is outside the model by construction.
  - *Forces a correction of wording.* It is not a model of *directed* change: nothing in it
    steers salience toward a target. So the thesis cannot say "the formal models are control";
    it has to say "the formal models locate a fixed evaluative point". The model is not a
    counterexample; it is an instance of the fixed point that is not control.
- **What the paper must do.** Add Dietrich and List to §7.8 as the fixed-point case, and word
  the thesis as above. This is the "Dietrich and List faced" item of the plan's freeze
  criterion.

### Bradley 2009, "Becker's thesis and three models of preference change"
- **Record.** *Politics, Philosophy & Economics* 8(2): 223–242, DOI 10.1177/1470594X09102238.
  Full text read in the LSE working-paper version (2007/2008).
- **What it says.**
  - It sets out three models of preference revision:
    1. classical conditioning: information changes, fundamental beliefs and desires held fixed;
    2. Jeffrey conditioning: information and prior beliefs change, fundamental desires held
       fixed;
    3. generalised conditioning: all three may change.
  - The third model is "completely general", in the sense that any change in attitudes can be
    represented within it.
  - On Becker's thesis, that all preference change can be explained against invariant
    fundamental tastes: if the state space may be refined at will, "it seems likely that it will
    always be possible to satisfy Becker's demand for explanations based on invariant tastes".
    But "refining the state space can be as ad hoc from a methodological point of view as
    postulating changes in fundamental desires".
- **Verdict: supports, is prior art, and complicates.**
  - *Supports and prior art.* Becker's invariant-tastes strategy is the paper's "one level up"
    reabsorption. Bradley's observation that it can almost always be carried through by refining
    the state space, at the price of being ad hoc, is the vacuity worry the paper answers in §7.6
    with a stopping rule. The paper should cite this as prior art on reabsorption, not present
    the move as its own discovery.
  - *Complicates.* Generalised conditioning *represents* a change of fundamental desires. So a
    formal representation of what the paper calls conversion exists. It is a kinematics of
    attitude change and says nothing about what produces or directs the change. The thesis
    therefore has to be restricted to models that direct, evaluate or explain change. Otherwise
    Bradley's third model is a counterexample.
- **What the paper must do.**
  - Cite Bradley in §7.6, as prior art on reabsorption and on the charge that it is ad hoc.
  - Cite Bradley in §7.8, as the representation-only model that lets the fundamental point move.

### Hansson 1995, "Changes in preference"
- **Record.** *Theory and Decision* 38(1): 1–28, DOI 10.1007/BF01083166. Publisher abstract
  read; the full text was not accessible.
- **What it says.** A framework in the style of belief revision with four operations: revision
  by "A is better than B", contraction, addition and subtraction of alternatives. The models are
  shown to satisfy "plausible postulates for rational changes in preferences".
- **Verdict: supports, weakly.** Change is driven by an input sentence under a fixed revision
  operator constrained by fixed rationality postulates. The operator and the postulates are the
  fixed evaluative point; the transformation of the standards themselves is not modelled.
- **What the paper must do.** One sentence in §7.8, beside Dietrich and List. The companion
  volume Grüne-Yanoff and Hansson (eds.) 2009, *Preference Change* (Springer,
  DOI 10.1007/978-90-481-2593-7), is the survey to cite for the field. It contains Spohn's "Why
  the received models of considering preference change must fail" (pp. 109–121), which an
  author engaging this literature should read in full; not read here.

### Bykvist 2006, "Prudence for changing selves"
- **Record.** *Utilitas* 18(3): 264–283, DOI 10.1017/S0953820806002032. Publisher abstract read.
- **What it says.** How to act prudently when one's actions will shape one's preferences. Bykvist
  proposes to evaluate each life by how the agent feels about it "when you are actually leading
  it".
- **Verdict: supports.** It is a fixed higher-order rule for adjudicating between the
  evaluations of changing selves, the same structure as Pettigrew's aggregation (§7.8.3), and
  its precursor. Bykvist also reviewed Pettigrew (*Mind* 130 (2021): 1327–1336,
  DOI 10.1093/mind/fzaa094).
- **What the paper must do.** Cite Bykvist in §7.8.3 as the precursor of the aggregation move.

## 3.2 The exogenous horn in the alignment literature

### Carroll, Dragan, Russell and Hadfield-Menell 2022, "Estimating and Penalizing Induced Preference Shifts in Recommender Systems"
- **Record.** ICML 2022 (Spotlight), arXiv:2204.11966. Abstract read on arXiv. An earlier
  workshop version: RecSys 2021, DOI 10.1145/3460231.3478849.
- **What it says.** Systems trained by long-horizon optimization have "direct incentives to
  manipulate users", in particular to shift user preferences so they are easier to satisfy. The
  authors propose to estimate induced shifts and to penalize those outside a trust region of
  "safe shifts", for example the natural shifts users would undergo without interference.
- **Verdict: supports.**
  - It shows that the cost of exogenous forcing on the forced agent's preferences is a problem
    recognized outside the paper. That is what the plan wanted this item for.
  - It also bears on the fixed point. To judge an influence manipulative, the authors need a
    fixed reference: the uninfluenced dynamics. That is the paper's structure again, on the
    evaluator's side.
  - It is not the same claim as the paper's agency cost (`tracking_cost_curve`), which concerns
    the loss of agency-bearing variation under tracking, not preference manipulation. Cite it as
    related, not as confirmation.
- **What the paper must do.** Cite it in §7.3 beside Carroll et al. 2024, which is already
  cited.

## Other sources

### For phase 2 (the boundary section; the author's work)
- **Korsgaard 1996.** *The Sources of Normativity*, Cambridge University Press,
  DOI 10.1017/CBO9780511554476. Practical identity is in lecture 3, "The authority of
  reflection", pp. 90–130.
- **Frankfurt 1988.** "Identification and wholeheartedness". In F. Schoeman (ed.),
  *Responsibility, Character, and the Emotions*, Cambridge University Press, pp. 27–45,
  DOI 10.1017/CBO9780511625411.002. Reprinted in *The Importance of What We Care About*
  (1988), pp. 159–176.
- See `drafts/boundary_section_support.md` §7 for a caveat on using either as the boundary
  criterion.

### For phase 4 (terminology)
- **Stroud 1968.** "Transcendental arguments", *The Journal of Philosophy* 65(9), first page 241,
  DOI 10.2307/2024395. This is the reference against which a philosophy referee will read
  "transcendental". The paper's argument does not have that form (see
  `drafts/paper1_restructure_plan.md`, point 4.1).

## What was not found

No formal model was found that *directs* or *evaluates* a change of fundamental values without a
fixed higher-order reference. The closest thing to a counterexample is a representation-only
model: Bradley's generalised conditioning. The search covered:
- the models above;
- the Grüne-Yanoff and Hansson volume's table of contents;
- the models already engaged in Paper 1: Pettigrew, Paul, Callard, de Blanc, and Carroll et al.
  2024.

It was not a systematic review. A referee in formal epistemology or decision theory might know
another candidate.
