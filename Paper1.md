# The Cybernetic Limits of Conversion: Formal Models of Value Change and the Fixed Evaluative Point

João Vitor Perazzolo

September 26, 2026

## Table of Contents

**Abstract**

1. General Introduction
2. Scope, Method, and Formal Status
   - 2.1 What a Negative Critique Claims and Does Not Claim
   - 2.2 The Identity Functional as a Pragmatic-Indexing Metamodel
3. Identity as Trajectory, Not State
4. The Identity-Relevant Functional *I* as a Consistency Contract
   - 4.1 The Three Locks Against Circularity
   - 4.2 Constitutive and Indicative Invariants as a Heuristic Partition
   - 4.3 Worked Applications and Adversarial Failure Cases
5. Four Diagnostic Regimes, and Why Persistence Is Not Stasis
6. The Control Trilemma
   - 6.1 The Central Problem: Why Control Theory Cannot Formulate Conversion
   - 6.2 The Endogenous Horn: Change Generated from Within (Ashby's Closure)
   - 6.3 The Exogenous Horn: Tracking and Its Cost to Agency
   - 6.4 The Optimization Horn: Incommensurable Objectives
   - 6.5 The Joint Result: A Limit on What Control Can Formulate
   - 6.6 The System Boundary: Why Relativity to It Does Not Trivialize the Thesis
   - 6.7 Is the Trilemma Vacuous? A Demarcation Criterion and the Division of Labor
   - 6.8 What the Simulations Checked, and What They Cannot Show
7. The Fixed Evaluative Point in Formal Models of Value Change
   - 7.1 Callard: Proleptic Rationality and the Anchored/Unanchored Distinction
   - 7.2 Paul: An Epistemic Obstacle and a Structural One
   - 7.3 Pettigrew and Bykvist: Aggregation as Reabsorption
   - 7.4 Formal Models of Preference Change: Dietrich and List, Hansson, and Becker's Invariant Tastes
   - 7.5 The Wider Literature, and Priority
   - 7.6 Is the Unanchored Class Non-Empty? The Concession's Own Non-Vacuity Check
   - 7.7 The Trichotomy as a Corrigibility Result
8. Class G as the Residual Admissibility Profile
   - 8.1 Mode-Selective Transformation, Not Totalizing Control
   - 8.2 Externality and Orientation-Gated Receptivity
   - 8.3 Definition of Class G as a Type Signature
   - 8.4 Is Class G Just Ordinary Interpersonal Influence?
9. The U-Limit: Identical Signature, Divergent Post-Jump Topology
10. Conclusion: The Insufficiency of the Control Paradigm

**Appendix A. Formal Apparatus**
   - A.1 The Diagnostic Taxonomy and the Correlation-Power Condition
   - A.2 The Identity/Agency Decomposition
   - A.3 The Meta-Optimization Collapse Theorem
   - A.4 Externality and Orientation-Gated Receptivity
   - A.5 The Class G Conditions in Symbols, and the Satisfiability Tests
   - A.6 The U-Limit Admissibility Predicate

**References**

---

## Abstract

Formal models of value change — decision theories for changing selves, formal theories of preference change, learning agents that revise their own objectives, schemes for corrigible artificial agents — are offered as accounts of how an agent's values can be transformed. This paper argues that each of them locates a fixed evaluative point: an aggregation rule, a weighing relation, invariant tastes, revision postulates, or a higher-order objective held constant while first-order values move. Used to direct change, such a model is control relative to that point, and control meets a trilemma. Change generated from within executes the agent's existing organization; change imposed by tracking a prescribed path costs the agent its agency, gradedly and in the limit completely; and optimization is undefined across a change of the objective itself. The trilemma is conceded to be definitional at its top level. The substantive claim is the case-by-case one, examined against Callard, Paul, Pettigrew, Dietrich and List, Hansson, Bradley and work on corrigibility. A dynamical theorem covers agents that revise their own preferences, and the agency cost of tracking is made quantitative. What remains is an admissibility profile, not a mechanism: an externally occasioned, receptivity-gated, mode-selective transformation, shown to be satisfiable and discriminating, with a unilateral limiting case distinguished from coercion by what it leaves open. The claim is conditioned on a definition of control, on the high-dimensional self-organizing regime, and on identity contracts that factor through a bounded reading.

**Keywords:** value change; transformative choice; preference change; control theory; corrigibility; personal identity.

---

## 1. General Introduction

A recurring problem across metaphysics, psychology and theology is persistence under transformation: how something can remain recognizably itself while undergoing real change. Identity is not perfect invariance, not unrestricted flux and not copyable information. This paper is about the constructive half of the problem, *transition*: how a subject moves toward a regime of healthy persistence. The default modern answer is *control*: specify the desired state, an error signal or a cost, and drive the system toward it. The paper argues that this answer, and the formal models of value change that make it precise, share a structure that disqualifies them for one case: conversion, the radical reordering of a person's values. Each holds some evaluative point fixed, and conversion is the transformation of such a point.

The claim concerns what a framework can formulate, not what can happen. It does not say that conversion is impossible. It says that, given its definition of control, *the control-theoretic framework cannot formulate conversion as conversion*. Section 6 argues this and concedes that at the top level it follows from the definitions. The claim that does not follow from them is the one section 7 argues case by case: that the formal models of value change on offer are, under analysis, control in this sense, or represent value change as movement within a fixed structure.

Sections 3 to 5 treat the identity functional *I* not as a property measurable in a flow but as a *pragmatic-indexing metamodel*, a consistency contract, and build the diagnostic vocabulary on it. Section 6 states the control trilemma. Section 7, the core of the paper, examines the formal models of value change one by one. Section 8 identifies Class G as the residual profile the trilemma leaves empty, and section 9 distinguishes it from a unilateral, integrity-bounded transition (the U-limit) by post-jump topology. Section 10 concludes. The theological applications are left to a companion paper (in preparation).

---

## 2. Scope, Method, and Formal Status

This is a conceptual paper addressed to the philosophy of action. It offers a *negative result about formulation*: an argument that a dominant family of models cannot formulate a certain problem, with the vocabulary needed to see why. It does not show how conversion happens, and it makes no theological or empirical claim. What its formal apparatus licenses is **sorting** (which cell a candidate account of transformation occupies), **costing** (the agency price of a given degree of exogenous forcing), and one conditional dynamical result (§6.5). Class G is an admissibility predicate, not a causal mechanism, and the notation states exclusions rather than new theorems in dynamical systems.

**Two delimitations.** First, the result is *conditional on a definition of control*: to be a control account at all is to define directed change relative to a held-fixed evaluative structure (a cost, a reward, an enumerated family of these, or a fixed higher-order objective). A reader who counts open-ended or value-base-mutating optimization as control will read the result as a claim about a narrower family. The thesis is therefore: *given that control is evaluation relative to a fixed evaluative point, conversion, the transformation of that point, cannot be formulated as control.* Second, the claim is *exact only in the high-dimensional, self-organizing regime*. A low-dimensional system whose identity/agency decomposition a designer supplies in advance is trackable by a multi-objective controller. Wherever the paper says that control "cannot" formulate conversion, it means this conditioned claim.

**Scope, summed.** The negative claim covers value change that is **unanchored** (§7.1 cedes proleptically anchored change to Callard; §7.6 checks that the residual class is non-empty), **autonomous**, and read through an identity contract that **factors through a bounded reading** (§6.5). Compactness has moved from the state space to the observable, and whether every admissible contract factors that way is an open problem (§6.5). The dimensional delimitation stands: the hardest case tested is six-dimensional, with a constructed decomposition. The formalism has three tiers. **One site is load-bearing:** the costing of the exogenous horn (§6.3, §6.7), which turns a binary intuition into a monotone cost curve. **One is conditional:** the closure of the escape horn by recurrence on the quotient (§6.5), a short step from Poincaré recurrence in its almost-everywhere form[^lean] whose premise, the bounded reading, is a hypothesis. **The rest is disambiguation**, stated in words in the body and formally in Appendix A.

**Failure conditions of the critique.** The argument would fail if a control strategy were exhibited that moves a subject toward Lambda-like persistence while preserving both $D_{id} < D_c$ and $D_{ag} > 0$ across a change of cost function; if the constitutive/indicative distinction collapsed, leaving "preserving agency" without content; or if the three horns were not jointly exhaustive.

### 2.1 What a Negative Critique Claims and Does Not Claim

A negative critique of this kind establishes a limit, not a positive theory. The analogy is to impossibility results elsewhere in science: a proof that perpetual motion violates thermodynamics does not tell you how to build an engine, but it permanently rules out a class of attempts and redirects inquiry. This paper's result is meant to work the same way, although at its top level it rests on a definition (§6.7), not on a law of nature. It does not tell anyone how conversion occurs. It rules out, with structural rather than empirical force, the attempt to model conversion as control. What remains after the ruling-out is not a mechanism but a *constraint on any adequate mechanism* — the admissibility profile of section 8.

The critique is therefore valuable in proportion to the dominance of the paradigm it limits. Cybernetics, optimal control, reinforcement learning, and predictive-processing-as-control are the default scientific languages for directed change in the twenty-first century. To show that this entire family cannot so much as state the problem of non-coercive transformation is to clear the ground on which any positive account must be built.

A reader may object that the paper imports heavy notation while disclaiming theorems. The notation is neither theorem-proving nor metaphor. It states, exactly, the boundary conditions a control model would have to meet to formulate agency-preserving transformation: $\lambda_\parallel \to -\infty$, for instance, is what exact tracking must impose, stated sharply enough that its conflict with $D_{ag} > 0$ can be shown rather than asserted.

### 2.2 The Identity Functional as a Pragmatic-Indexing Metamodel

The most important methodological commitment of this paper is the demotion of the identity-relevant functional *I* from a putative physical property to a *pragmatic-indexing metamodel*. Naive dynamical accounts treat persistence as something one could read off a trajectory. This paper rejects that, because it is the source of the circularity that makes such accounts vacuous.

On the present account *I* is a contract entered into by an observer (a clinician, an analyst, a theologian) who proposes to make a persistence claim: *if you assert that this system persisted as the same X, you are committed to indexing these constraints as the ones whose violation would refute your claim.* The constitutive/indicative partition is the observer's choice of which features the claim treats as load-bearing, not a fact about the system. This places the framework in the sortal-dependence tradition: "same?" is shorthand for "same *what*?", and *I* formalizes the *what* (Wiggins 2001). It departs from a purely sortalist account in that *I* may index a practice or a memory-bearing process rather than a substance-kind, and in carrying a dynamical vocabulary the bare sortal leaves unspecified.

The demotion is the precondition for non-circularity. If *I* were chosen after inspecting the trajectory, any pattern could be made persistent by selecting the contract that preserves it. Fixed in advance, under the three locks of section 4.1, the contract can be violated and can be contested by observers who propose a rival one. "This system is Lambda-like" therefore never means that the system intrinsically instantiates Lambda. It means that, relative to a pre-specified, externally contestable contract, the system retains the relevant correlation power over the declared timescale.

---

## 3. Identity as Trajectory, Not State

Throughout this article, remaining the same self does not mean retaining every property, memory, or psychological disposition. It means preserving a historically indexed *trajectory* through admissible change. A copied pattern, even if structurally identical, is not by that fact the same trajectory. This non-branching requirement is essential because fission, teletransportation, and uploading cases show that psychological or informational continuity can ramify (Parfit 1984; Lewis 1976; Williams 1970; Agar 2016).

A living organism persists while exchanging matter and energy. A person persists through memory revision, moral transformation, trauma, sleep, illness, and social re-description. The state of the system at any instant is not the carrier of its identity; the carrier is the continuity of the path, indexed by the contract *I*. Two consequences follow. First, identity is a four-dimensional notion: it concerns the shape of a history, not the contents of a moment. Second — and this is what the trilemma will exploit — any intervention that moves the system must be evaluated by what it does to the *trajectory and its openness*, not merely by what end-state it produces. A controller that reaches the target state by collapsing the path's future openness has not transformed the subject; it has replaced a trajectory with a terminus.

---

## 4. The Identity-Relevant Functional *I* as a Consistency Contract

The functional *I* is specified by a domain, an observable $f$, a tolerance $\epsilon$, and a timescale $\tau$. The quadruple $(I, f, \epsilon, \tau)$ is the content of the contract. It does not describe the flow; it commits the observer.

### 4.1 The Three Locks Against Circularity

A valid use of *I* requires three locks. First, **domain justification**: the contract must be motivated by the persistence question before any trajectory is inspected. Second, **adversarial failure cases**: the observer must specify, in advance, the transformations that would count as identity-destroying. Third, **independent contestability**: domain experts not committed to the target verdict must be able to challenge the contract. A contract that cannot be challenged is not a contract; it is a tautology.

### 4.2 Constitutive and Indicative Invariants as a Heuristic Partition

The contract partitions features into constitutive and indicative. A *constitutive* invariant is one whose destruction the contract treats as breaking the trajectory: its loss is replacement, not change. An *indicative* invariant tracks identity but may change without, on the contract, destroying the subject. The partition is heuristic and observer-relative: it expresses which features the persistence claim treats as load-bearing. It is also externally contestable — a critic can argue that a proposed constitutive invariant is in fact merely indicative, or vice versa. The partition does no work as a discovery about the system; it does all its work as a structuring of the claim.

### 4.3 Worked Applications and Adversarial Failure Cases

The discriminating power of *I* is shown by cases it handles and, crucially, by attempted contracts that *fail*.

**Moral conversion** preserves constitutive invariants — non-branching trajectory, responsibility-bearing history, practical agency — while reorganizing indicative ones — habits, desires, self-description. On a well-formed contract for personhood, this is transformation, not replacement.

**Teletransportation/fission** preserves copyable structure but breaks the non-branching trajectory. A contract for singular numerical personhood must, by its adversarial cases, classify this as identity failure despite pattern-continuity.

**Two failed contracts.** $I_{profile}$, similarity of memory reports, personality and dispositions, fails in the fission case: two successors could each satisfy it, violating non-branching. It mistakes indicative invariants for constitutive ones. $I_{exact}$, preservation of everything, classifies conversion and maturation as destruction. It mistakes constitutive for indicative.

These failures clarify the contract's role: it must be strict enough to reject branching copies and permissive enough to allow genuine transformation. A contract that cannot satisfy both under adversarial testing is not admissible for the domain. This is the substance of external contestability.

---

## 5. Four Diagnostic Regimes, and Why Persistence Is Not Stasis

Relative to a contract $(I, f, \epsilon, \tau)$, the paper names four regimes of persistence-relevant behaviour. They are not boxes into which whole systems fall; a system behaves as one of them only relative to the question of which features must remain identifiable, over which timescale.

- **Class R (random disorder).** Order is overwhelmed by stochastic disorder. The failure mode is dissolution.
- **Class P (mechanical periodicity).** Structure is preserved by strict repetition, $x(t+T) = x(t)$. The failure mode is closure: a loop contains no new history.
- **Class M (mixing chaos).** The dynamics are deterministic, bounded and aperiodic, but identity-relevant correlations decay. The failure mode is dispersal: motion without retention.
- **Lambda (aperiodic, memory-preserving persistence).** The dynamics are bounded and aperiodic, and the observable the contract designates keeps a non-vanishing share of its correlation with its own past (the correlation-power condition, Appendix A.1). Lambda is not a new mathematical class; it is the regime in which the subject neither dissolves, freezes nor forgets, relative to the contract.

The contrast between P and Lambda is why persistence must not be confused with stasis: a person incapable of growth or new understanding has not achieved perfected identity, but closure. The taxonomy is purely diagnostic. It classifies what is happening to a system; it does not say how a system moves from one regime to another without losing what matters. The intuitive answer to that question is *control*: specify the target and drive the system there. Section 6 argues that control, in each of its three forms, either is no transformation at all, or achieves the transition at the cost of the agent, or cannot be defined across the change of evaluative standard that conversion involves. Fuller definitions of the four regimes, and a comparison of Lambda with neighbouring notions, are in Appendix A.1.

## 6. The Control Trilemma

### 6.1 The Central Problem: Why Control Theory Cannot Formulate Conversion

The diagnostic taxonomy poses a transition problem: move a subject from a dispersive (M), rigid (P) or disordered (R) regime toward Lambda-like persistence. The default framework for directed transition is control theory in its broad sense: cybernetics, optimal control, dynamic programming and their descendants. This section argues that the framework cannot formulate the transition conversion names, because conversion must honor two constraints jointly: the identity-bearing trajectory is preserved ($D_{id} < D_c$) *and* agency-bearing openness is preserved ($D_{ag} > 0$), across a change that reorders the subject rather than relocating it within a fixed value structure.

The framework offers three strategies for producing transition: generate the change from within the system's own dynamics (feedback), impose it from outside by force on the state (forcing), or compute it as the solution to an optimization over a cost or value function (optimal control). These are the directed-change repertoire of the cybernetic tradition, from Wiener (1948) to its reinforcement-learning descendants (Sutton and Barto 2018). Each fails, and what remains, the conjunction of properties no control strategy delivers, is the admissibility profile of section 8.

The two constraints need a working vocabulary. Near the region where the subject's identity is preserved, its possible changes split into two kinds of direction:
- *identity-bearing* directions, along which uncontrolled spread destroys identity;
- *agency-bearing* directions, along which variation *is* the subject's adaptive openness.

Conversion requires three things together. Deviation along the identity-bearing directions must contract. Openness along the agency-bearing directions must be *protected*: the rate at which agency-bearing excursions are pulled back, written $\lambda_\parallel$, must be held near zero, so that agency is neither frozen nor dispersed. And the two spreads must satisfy the constraints the paper writes as $D_{id} < D_c$ (identity-bearing spread below a critical value) and $D_{ag} > 0$ (agency-bearing openness preserved). The formal decomposition is in Appendix A.2. The trilemma is that no control strategy can establish this profile.

### 6.2 The Endogenous Horn: Change Generated from Within (Ashby's Closure)

The first strategy generates the change from within: the system's own feedback reorganizes it toward the target. Call the internal vector field $F_0$, so that the transformative term lies in $\langle F_0 \rangle$, the span of the system's own dynamics.

The difficulty is that endogenously generated change is the execution of a latent subroutine, not conversion. An ultrastable system changes its own parameters whenever an essential variable leaves its viable bounds, until the variable returns (Ashby 1960), and a regulator absorbs disturbance only to the extent of its own variety (Ashby 1956). Such a system *changes state in order to preserve its organization*: whatever new behaviour appears was already reachable in its own variety, selected by the disturbance to restore the prior organization.

This is the negation of conversion, which is the change of the organization itself, the replacement of one cost structure by another (§6.4). If the transformative field lies in $\langle F_0 \rangle$, the "new" trajectory is one the system's own dynamics already admitted. Endogenous control is excluded not because it produces no change, but because the change it produces preserves the organization.

### 6.3 The Exogenous Horn: Tracking and Its Cost to Agency

The second strategy imposes the change from outside, by force on the state. "External input" is far too broad, so the case must be specified: the horn concerns *coercive trajectory-tracking control*, in which an input $u_t$ drives the system along a prescribed path and penalizes deviation from it, overriding the system's own dynamics wherever they would depart from the commanded route. Only this class is excluded. Inputs that merely trigger a transition toward an attractor already latent in the system's dynamics, without then penalizing departures from a commanded path, are a different category, treated below.

The difficulty is that tracking achieves the target trajectory only at the cost of agency, and in the limit of exact tracking by collapsing it. To hold a system on a prescribed path against its own dynamics and noise, the controller must suppress the tangential degrees of freedom that would carry it away. In the linearized picture this drives the agency eigenvalues strongly negative, $\lambda_\parallel \to -\infty$ in the limit, so that any agentive excursion is contracted back at once, and the agency-bearing diffusion is suppressed, $D_{ag} \to 0$. It is the penalty on departure that forces the contraction.

The subject then reaches the target *state*, but as a contracted point with no tangential freedom: a Class P closure imposed from outside, a trajectory turned into a terminus. One cannot hold an agent on a prescribed trajectory by force and leave it free to depart from it, since the freedom to depart is what the tracking penalty must suppress. Tracking is excluded not because it fails to produce the target state, but because producing it by deviation-penalizing force requires $D_{ag} \to 0$.

One refinement keeps this horn from overclaiming. The collapse $D_{ag}\to 0$ is the *perfect-tracking limit* (zero asymptotic error, infinite gain). Real forcing is finite-gain. Funnel control and prescribed-performance control guarantee a prescribed error bound with finite, state-dependent gain (Ilchmann, Ryan, and Sangwin 2002; Bechlioulis and Rovithakis 2008), and leave $\lambda_\parallel$ finite and $D_{ag}>0$. The horn is therefore graded: deviation-penalizing forcing reduces agency-bearing diffusion *monotonically* with the tightness of the bound, collapsing it only in the limit. What the horn asserts is that monotone *agency cost*, strictly positive and increasing in the control authority exerted, not a binary kill. The cost of exogenous influence on an agent's preferences is recognized outside this paper: systems trained by long-horizon optimization have incentives to shift the preferences of the people they serve, and judging such a shift acceptable or manipulative requires a fixed reference, such as the shifts the people would have undergone without interference (Carroll et al. 2022).

The collapse result does *not* hold for exogenous *trigger* inputs: signals that push a system through a bifurcation toward an attractor already latent in its own dynamics, and then release. Such an input imposes no path and penalizes no deviation, so it does not drive $\lambda_\parallel \to -\infty$, and it can *expand* the repertoire. The horn excludes deviation-penalizing tracking, not exogenous causation as such. The difference between a trigger toward a latent attractor and a Class G reconfiguration, which opens an attractor the prior dynamics did not contain, is taken up in section 8.

### 6.4 The Optimization Horn: Incommensurable Objectives

The third strategy computes the change as the solution to an optimization: define a cost or value function $J$, and let the optimal policy be the one that minimizes expected cost (or maximizes expected value) over the trajectory. This is the apparatus of optimal control and dynamic programming, and it is the most sophisticated of the three, because it appears to honor both constraints — it can preserve identity by penalizing destructive excursions and preserve agency by leaving the policy free within the value landscape.

The difficulty is that optimization is *undefined* across the kind of transformation conversion essentially is. Conversion is not a movement to the optimum of a fixed value function. It is a change in *what counts as value* — a reordering of the cost function itself, $J \to J'$. The convert does not get better at satisfying their old preferences; their preferences are transformed. The thing that was salient as a good ceases to be a good, and what was invisible becomes the organizing end. This is an axiological discontinuity.

A charge of circularity is due here: the paper has *defined* conversion as a change no fixed value structure can represent, and then observed that methods fixing a value structure cannot represent it. The charge is partly right, and §6.7 concedes that the top-level thesis is definitional. It does not reach the axiological discontinuity itself, which is attested independently, in the literature on transformative experience, where the agent cannot evaluate the post-transformation state by pre-transformation preferences (Paul 2014). The failure of backward induction across $J \to J'$ is then a step that could have failed. It does fail for genuinely novel $J'$, and does not fail for parametric change within a fixed family, which optimization handles.

At such a discontinuity dynamic programming has nothing to compute. The Bellman equation defines the value of a state recursively, by backward induction from terminal costs: the immediate cost plus the discounted optimal value of the successors (Bellman 1957). The recursion presupposes a *single, fixed* cost function across the horizon. If the cost ceases to be $J$ and becomes $J'$ mid-trajectory, earlier values would have to be computed against a terminal structure that does not yet exist and is incommensurable with the one that did. "Optimal" has no fixed referent across the change, and the value function is singular there.

This is a category failure, not a numerical instability. Optimization describes *improvement within a value structure*. It cannot describe *the transformation of the value structure*, because that is what it holds fixed in order to be well-posed. It can model a saint getting better at being the person they already were, not the becoming of a person whose metric of the good has changed.

**A deflationary alternative.** The strongest reply to this horn is that *there is no genuine $J\to J'$*. What the phenomenology reports as a categorical reordering is parametric change within a higher-dimensional value function $J^{*}$ whose relevant coordinates were latent, not absent; the felt discontinuity reflects limited introspective access. If this holds, the third horn fails, and the novel/parametric distinction does not exclude it, since the deflationist can classify every apparent novelty as latent after the fact. What the paper can do is state the cost of the move. It requires that the post-conversion preferences be representable in coordinates the pre-conversion agent already possessed. The transformative-experience literature claims exactly that this fails, because the content needed to fix those coordinates is available only from inside the transformed state (Paul 2014); on that view $J^{*}$ is a post-hoc reconstruction. The formalism cannot settle the dispute. The horn holds *if* axiological discontinuity is real and reduces to the deflationary reading if it is not. The deflationist escapes only at the price of holding that no one ever undergoes a change of values they could not have anticipated, a strong and contestable thesis.

### 6.5 The Joint Result: A Limit on What Control Can Formulate

The three horns are jointly exhaustive of the control paradigm. Any control-theoretic account of transition must generate the change endogenously, impose it exogenously, or compute it by optimization; there is no fourth source of directed change within the paradigm, and each fails on a constraint conversion requires.

The conjunction is the result. The control paradigm *cannot formulate* a transformation that (i) genuinely reorders the subject's value structure rather than redeploying its latent variety, (ii) preserves the subject's agency rather than collapsing it to execute a command, and (iii) is well-defined across the reordering rather than singular at it. But these three are exactly the marks of conversion. Therefore conversion is not a control problem that is merely hard; it is a transformation the control paradigm lacks the conceptual resources to state.

**Does modern control escape the trilemma?** The horns as stated engage classical feedback, brute forcing and deterministic dynamic programming. Three modern families appear to evade them, and if any formulates conversion the negative claim fails: dual control, switched and hybrid systems, and adaptive or reinforcement-learning control. Each, on inspection, falls under a horn for the same structural reason: it presupposes in advance the value structure that conversion transforms.

*Dual control* gives the input a double role, probing to reduce uncertainty and regulating the state (Feldbaum 1965). It escapes the static reading of the endogenous horn, because the controller reshapes its own beliefs. But the probing and regulating serve a cost functional given in advance and held fixed. Dual control changes what the agent believes, not what it values, and it is an instance of the optimization horn: against an incommensurable $J'$, the exploration-exploitation trade-off it computes relative to $J$ is undefined.

*Switched and hybrid systems* are the most serious objection. For them a transition $J \to J'$ is not a singularity but a documented structural change, handled by switching among controllers or modes (Liberzon 2003). But they handle it only when the *family* $\{J, J', \dots\}$ and the switching surfaces are specified in advance. Conversion is the arrival of a $J'$ that was not in the family, governed by no antecedent switching surface. A switched system can model a person changing which of several known goods they pursue, not a person coming to be governed by a good that was not among the options; against a novel $J'$ it is back in the optimization horn.

*Adaptive and reinforcement-learning control* revise their policies online and seem to need no fixed model. But learning a policy is not transforming a value structure. Standard RL holds the reward, which is the agent's value structure, fixed by construction. Where the reward is itself learned (inverse RL, reward learning, meta-learning), the change is governed by a fixed higher-order objective, which moves the fixed point up a level and reproduces the horn there. If no level is ultimately fixed, the scheme has no defined notion of "better" and computes nothing.

The common structure is the real content of the exhaustiveness claim. Every variant presupposes a fixed point of evaluation: dual control fixes the cost, switched systems the family and the switching surfaces, adaptive control the terminal objective. Exhaustiveness is not a claim about named techniques, which will multiply, but about the *form* of a control account: any technique recognizable as control inherits a fixed evaluative point, and with it one of the three failures.

**The status of the exhaustiveness premise.** That form is a premise, not a theorem: *to be a control account at all is to define directedness relative to a held-fixed evaluative structure.* Three families press on it: open-ended and novelty-search algorithms (Lehman and Stanley 2011), theories of artificial curiosity and intrinsic motivation (Schmidhuber 2010; Singh, Barto, and Chentanez 2004), and endogenous-preference models in economics (Bowles 1998). A reader who counts these as control will read the trilemma as bounded to the narrower family and the result as conditional on a definition they reject. The paper's reply is that each, at the level where "better" is ultimately defined, still fixes some criterion: the novelty measure and behavioural space, the meta-objective of compression progress, the higher-order dynamics of preference updating. For the endogenous case the regress can be stated as a theorem about the dynamics of the value state, a theorem for states typical of an invariant measure, with the dissipative case resting on interpretation.

**The Meta-Optimization Collapse Theorem (endogenous-preference case), in outline.** Suppose the agent revises its own preferences by an autonomous dynamics of its value state, and suppose the value state stays within a bounded region, as it must if the agent is to persist rather than have its values diverge. Every such dynamics falls into exactly one of three cases, and none of the three is conversion:
- *Case 1, the integrable case (Bellman returns).* The revision is descent on a single higher-level potential. The "new" values are a moving coordinate within one fixed objective, and the Bellman horn of §6.4 applies to that objective exactly as it applied to a fixed cost.
- *Case 2, the dispersive case (Class M).* The value state wanders without settling. Preferences cycle, and there is no directed, permanent reordering.
- *Case 3, the recurrent case.* The value state settles onto a bounded attractor. What excludes conversion depends on the attractor:
  - at a fixed point, openness collapses;
  - on a limit cycle, the change is rigid repetition;
  - on a strange attractor, the system is open but keeps returning arbitrarily close to where it has been, which is the negation of permanent reorganization into a new regime.

The formal statement is in Appendix A.3. It includes the Helmholtz–Hodge decomposition that makes the three cases exhaustive, and the measure-theoretic form of the recurrence argument: recurrence holds with respect to the attractor's invariant measure, not the ambient one.

*The closure of the trichotomy.* Conversion requires *both* permanent directed reorganization into a new regime (escaping Cases 2 and 3) *and* preserved aperiodic openness (escaping Case 1's frozen descent and Case 3's fixed point and cycle). By Helmholtz–Hodge the three cases are exhaustive for an autonomous $\dot\theta=f(\theta)$ on a compact set, and conversion is excluded from each. For *measure-preserving* value dynamics, satisfying both properties at once requires a **non-autonomous** drive, $\dot\theta = f(\theta, t)$, which breaks the measure preservation recurrence rests on. For *dissipative* dynamics it does not: an autonomous flow can settle permanently onto a new attractor, and what excludes that as conversion is the interpretive argument that the attractor was latent in the flow.

**What the theorem excludes.** Recurrence excludes the forbidden object only for states typical of the flow's invariant measure: almost every initial condition for conservative dynamics, but not the transients of dissipative dynamics, where the exclusion rests on the interpretation of settling as reabsorption, not on a theorem. The corrected forms of Poincaré's and Conley's theorems are in Appendix A.3.[^lean]

**Relation to prior art.** The dynamical content is not new. The split of a flow on a compact space into a gradient-like and a chain-recurrent part is Conley's fundamental theorem (Conley 1978). That a system whose objective co-evolves with it is Poincaré recurrent has been shown for agents and the zero-sum game they play (Skoulakis et al. 2021). That non-repeating novelty requires coupling to an external environment was argued via the same recurrence mechanism by Adams et al. (2017). What is new is only the transfer to an agent's own top-level value function, and the reading of conversion that follows.

"Non-autonomous" is not synonymous with "coercion". A time-dependent input takes one of the two forms §6.3 distinguished. Deviation-penalizing tracking is the exogenous horn and is excluded. A *non-tracking trigger*, an exogenous occasion that releases the value dynamics toward a regime not latent in the prior autonomous flow while commanding no path and penalizing no deviation, does not drive $\lambda_\parallel\to-\infty$ and is the admissible profile of section 8. So the theorem does not close into "conversion is impossible". **Relative to a declared system boundary, an autonomous preference dynamics does not realize conversion (by recurrence for invariant-measure-typical states, a theorem; and by the openness argument for dissipative transients, an interpretation, not a theorem), so conversion is externally occasioned — necessarily in the measure-preserving case, and in the dissipative case only as far as that interpretation is accepted; and the external occasion is coercion (excluded) if and only if it is deviation-penalizing tracking, and is otherwise the non-coercive Class-G trigger the rest of the paper characterizes.** Why relativity to the declared boundary does not make this verdict arbitrary is the subject of §6.6.

The theorem assumes a bounded value state. Unbounded drift is closed by *recurrence on the quotient*, for any identity contract that factors through a bounded reading, such as one that reads only the direction of the value state. Contracts that grow exponentially with magnitude are **not testable by this instrument** (Appendix A.3).

**What remains open.** The closure is a disjunction: *either* the identity contract factors through a bounded reading, and recurrence excludes conversion, *or* it does not, and the only witnesses available here purchase non-return by freezing the direction, failing openness instead (§6.8). The disjunction closes the horn only if it is exhaustive over *admissible* contracts. §6.6 settles part of what admissibility means. It fixes which system a contract may be about: the bearer of the responsibility-bearing history, a constitutive invariant every personhood contract already carries. It does not say which readings of that bearer's value state a contract may take, and so not whether every admissible contract factors through a bounded reading. **Characterizing the admissible identity contracts beyond the boundary, and settling whether every member factors through a bounded reading, is the first open problem this argument leaves.** It may not be well-posed. §2.2 makes $I$ a *pragmatic-indexing metamodel*, stipulated by an observer. Taken strictly, that leaves no fact of the matter about admissibility beyond what the contract itself declares: a substantive constraint on readings would reopen the circularity §2.2 guards against, and declaring exhaustivity would close the horn by definition. The paper takes neither route. It reports the closure for the class on which it was established: three horns exhaust control *for bounded-reading contracts*. Exhaustivity over all admissible contracts is a declared open problem, not a carried conjecture. On a compact, measure-preserving space, Case 2 then collapses into Case 3's recurrence, and genuine escape is closed by recurrence on the quotient; neither supplies an autonomous flow that achieves conversion. A counterexample would be an *autonomous*, compact, measure-preserving preference dynamics that is positive-entropy and non-recurrent toward a permanent regime, which Poincaré recurrence rules out.

### 6.6 The System Boundary: Why Relativity to It Does Not Trivialize the Thesis

The result of §6.5 holds relative to a declared system boundary. That invites an objection which, if it succeeded, would empty the thesis. Take any event the paper classifies as a Class-G occasion and enlarge the boundary to include the occasion's source. The enlarged flow is autonomous. Its new regime is then an attractor latent in that flow, and by §6.5 the change is reabsorption. Since every occasion has a source, every Class-G verdict can be undone by redrawing the line. A verdict that depends only on where the observer draws it says nothing about the agent.

The paper accepts the premise and rejects the conclusion. The verdict is boundary-relative, as the identity verdict is contract-relative (§2.2). What fails is the step from relativity to arbitrariness, and it fails for two reasons: not every boundary is admissible, and the enlarged boundary changes the subject of the claim.

**Which boundaries are admissible.** Declaring the boundary in advance, under the locks of §4.1, blocks redrawing it after the event is seen. It does not block a tendentious choice made before, such as a boundary drawn narrowly so that the event will come out as Class G. The paper therefore needs a restriction on *which* boundaries individuate an agent, not only on *when* they are declared.

The restriction it adopts is already part of the contract. Among the constitutive invariants of any well-formed personhood contract is a responsibility-bearing, non-branching history (§4.3). The admissible boundary for assessing a conversion is accordingly the boundary of whatever bears that history: the bearer who can be held to answer, both before and after the event, for what was done under the old values.

This criterion is chosen over the more familiar ones in the philosophy of action for a reason specific to conversion. Practical identity and identification are *contents*, and conversion may change exactly those contents. A boundary drawn by what the agent identifies with would move with the event it is meant to classify. The accountability relation is formal rather than contentual. By the paper's own classification it survives conversion. That the converted person still answers for what she did before is precisely what distinguishes conversion from replacement (§4.3).

Applied to the objection, the criterion decides the case. The enlarged system, agent plus source, does not bear the agent's responsibility-bearing history. The source does not answer for what the agent did under her old values, whether that source is a friend, a text, a community or, on a theological reading, God. Nor is agent-plus-source a bearer of that history at all. The enlarged system is a well-defined dynamical system. It is not an admissible individuation of the agent whose conversion is in question. The objection's move is available to the dynamics; it is not available under the contract.

The criterion blocks narrowing as well as enlargement. The tendentious case that motivated it was a boundary drawn narrowly in advance, so that some of the agent's own processes would count as an external occasion. A sub-personal part, such as a value module, a perceptual system or a neuromodulatory process taken alone, does not bear the agent's responsibility-bearing history either, so it is not an admissible individuation. Whatever changes the agent through her own processes, deliberative or not, lies inside the admissible boundary and falls under the endogenous horn. A Class-G candidate therefore needs an occasion outside the bearer of that history, not merely outside some part of her.

**Redrawing the boundary changes the subject.** Suppose a critic insists on the enlarged boundary anyway. The verdict she obtains is "the agent-plus-occasion did not convert". That verdict is compatible with "the agent was converted", which is the only claim the Class-G classification makes. The objection establishes the first and mistakes it for the negation of the second.

The comparison with frame-relativity in physics shows what does and does not vary. Velocity depends on the frame, but acceleration is invariant across inertial frames, so "this body is accelerating" is a substantive claim despite the relativity of velocity. The corresponding invariant here is the verdict *given* an admissible individuation of the agent. Holding that individuation fixed, the verdict does not change under redescriptions of the environment, such as modelling the occasion as noise, as an input, or as another agent. What changes the verdict is a change in *which agent* is assessed, and that is governed by admissibility, not by the observer's convenience.

**A hard case: joint agents.** The criterion leaves one case open, and the paper states it rather than closing it by stipulation. If the source and the agent form a genuine joint agent, one that bears a shared responsibility-bearing history and answers as a whole for the agent's prior acts, then the enlarged boundary may be admissible, and the verdict for that joint agent may be reabsorption. This is a verdict about a different subject and can coexist with a Class-G verdict for the individual. Whether a given community is such a joint agent is a question for the theory of group agency, which the paper does not settle.

**What would count against the thesis.** A declared admissible boundary, fixed in advance, inside which an autonomous flow shows directed, permanent, agency-preserving reorganization of the agent's top-level evaluative structure. For measure-preserving dynamics, such a case would contradict a theorem (§6.5). For dissipative dynamics, where the exclusion rests on the reabsorption interpretation, it would have to defeat that interpretation, by showing that the new regime was not latent in the declared flow.

**What this section concedes.** The thesis is individuation-relative. A reader whose theory of agent individuation does not take the bearer of responsibility as the boundary may reject its application to a given case. The criterion also presupposes that responsibility attributions are well-defined across the event. Where they are contested, as in severe dementia or radical dissociation, the admissible boundary is contested too, and the framework returns no verdict. Theological readings, developed in the companion paper, are one declared boundary among others; the argument here does not establish them.

### 6.7 Is the Trilemma Vacuous? A Demarcation Criterion and the Division of Labor

The most damaging objection is that the *whole result is analytic*. If "control" is defined as directed change relative to a held-fixed evaluative point, and "conversion" as the change of that point, then "control cannot formulate conversion" restates the definitions; and if every counterexample can be reabsorbed by moving the fixed point "one level up", nothing could count against it. This subsection concedes the analytic core and argues that an analytic frame can still do two kinds of non-trivial work, *sorting* and *costing*.

**The reabsorption move needs a stopping rule, or the charge of vacuity is fair.** Bradley (2009) presses the same worry against Becker's programme of explaining all preference change by invariant tastes (§7.4). Answering every counterexample with "there is always a fixed point one level up" would be unfalsifiable. What disciplines the move is a criterion that can be failed: a candidate escapes the trilemma if and only if it exhibits a *directed, permanent, agency-preserving reorganization of its top-level evaluative structure, generated by no antecedently fixed criterion at any level and not merely externally triggered*. The "one level up" reply is licensed only for architectures that install a genuine higher-order objective (inverse RL's matching target, curiosity's meta-reward, novelty search's novelty measure), where the relocation is a checkable fact. Where an architecture installs none and is autonomous and bounded, the Meta-Optimization Collapse Theorem (§6.5) forecloses conversion for states typical of an invariant measure; for dissipative transients the foreclosure rests on reading settling as reabsorption, an interpretation. The vacuity charge holds against the slogan and fails against the theorem, and only in the endogenous-autonomous case does the paper claim a theorem rather than a definition.

**What an analytic frame still buys: sorting.** A definitional frame that carves a space cleanly is not thereby empty. The trilemma sorts any proposed account of transformation into four cells (endogenous, exogenous, optimization, and the residual Class G) and so says which failure it inherits or which conditions it must meet. The sorting is non-obvious where practitioners believe an adaptive scheme has escaped the fixed evaluative point when it has only relocated it.

**What the formalism buys beyond sorting: costing.** The one place the apparatus is not merely analytic is the exogenous horn. That agency is destroyed in the perfect-tracking limit is not a definition; it is a *quantitative* claim about a rate — the agency-bearing diffusion $D_{ag}$ and the tangential eigenvalue $\lambda_\parallel$ as functions of the control gain — and it is *graded*: finite-gain forcing pays a *monotone, computable* agency cost. It turns a binary intuition into a cost curve on which an intervention sits at a definite point, and it places Class G at the $\lambda_\parallel\to 0$, $D_{ag}>0$ corner, which must be actively held (§8.1). What the dynamics buys over the definitional thesis is this costing, not a theorem that conversion is impossible.

**What the definitions do not settle: whether the models on offer are control.** Grant that "control cannot formulate conversion" is definitional. It does not follow from the definitions that any particular model of value change *is* control in this sense, or that it represents change only as movement within a fixed structure. That is a claim about the models, and it can be false of any of them. Section 7 argues it case by case, and it is where the paper's substantive content lies.

**The division of labor.** The formalism licenses sorting, costing and the conditional endogenous result, and nothing about whether any transformation it describes occurs. Theological uses are conditional and are left to the companion paper.

### 6.8 What the Simulations Checked, and What They Cannot Show

Simulations cannot validate a thesis that is definitional at its top level. A pre-registered suite checked three formal claims this section relies on: the agency cost of tracking is graded and monotone in the gain; the standard counterexamples each fell into one of the theorem's three cases; and an apparent falsifier in a value-mutating agent turned out to be an artefact of coordinates.

The runs and numbers are in the accompanying repository (`experiments/paper1_control_trilemma/`, `IN_SILICO_RECORD.md`).

## 7. The Fixed Evaluative Point in Formal Models of Value Change

§6.7 concedes that the trilemma is definitional at its top level. The claim that is not definitional, and that this section argues case by case, is this. The formal models on offer for directing or evaluating value change each locate a fixed evaluative point. When such a model is used to direct change, it is control in the paper's sense and inherits the trilemma. When it only represents change, it represents it either as reabsorption — a moving coordinate within a fixed higher-order structure — or as a change of fundamental values whose production it does not model. The claim is contestable, and a single counterexample would refute it: a model that directs or evaluates a change of fundamental values without a fixed higher-order reference. The cases below are the strongest candidates the paper knows of: from the philosophy of rational value change (Callard, Paul, Pettigrew), from the formal theory of preference change (Dietrich and List, Hansson, Bradley), and from work on self-modifying artificial agents (§7.7). On the way, the thesis is narrowed in one place (§7.1), and its remaining domain is checked for emptiness (§7.6).

### 7.1 Callard: Proleptic Rationality and the Anchored/Unanchored Distinction

Callard (2018) is the most direct challenge in print, and if she is right in the strong form, the trilemma is false. Her subject is *aspiration*: the process by which an agent comes to care about something she does not yet care about — becoming a parent, acquiring a taste for music, entering a vocation. The puzzle she takes up is exactly the paper's: how can such a process be rational, when the reason to engage in it is available only to the person one will become? Her answer is that the aspirant acts on **proleptic reasons** — acknowledged-*defective* versions of the reasons she expects eventually to grasp — so that what rationalizes her action is a value she grasps only imperfectly. Value acquisition, on this account, has its own distinctive rationality, and needs no prior full possession of the value acquired.

Two things must be said, and the first is a concession that narrows this paper's thesis.

*The concession.* The trilemma is a claim about **unanchored** value change. Callard's aspirant is anchored: she has a defective but genuine grasp of the value she is acquiring, and that grasp is what guides her. Under that description the aspirant's trajectory is endogenous refinement of an evaluative structure already present *in nuce* — Case 1 of the trichotomy, gradient-like motion on a meta-potential whose potential is fidelity to the imperfectly grasped value. So the aspirant is no falsifier of the theorem; but neither does the theorem tell against her, because what she describes is not what this paper means by conversion. The honest consequence is that the thesis must be stated more narrowly than §6.5 alone suggests: the trilemma bites against value change that is *not proleptically anchored*, and Callard makes a powerful case that a large and important class of ordinary value change is anchored. This paper does not claim that all value change is unformulable; it claims that value change without an anchor cannot be formulated as control.

*The convergence.* On Callard's account aspiration is not decision-making: the aspirant does not adjudicate between old and new values but works to see the world in a new way. That is this paper's negative thesis in another vocabulary. The disagreement is about what follows: this paper concludes that conversion is externally occasioned (§6.5), Callard that there is a distinct rationality internal to the aspirant.

Whether proleptic rationality occupies the space the trilemma leaves empty is open, and condition 10 of Class G makes it precise. If the proleptic grasp is the agent's own, aspiration is Case 1, not Class G. If it is externally occasioned (someone showed her the value), it may be G-admissible, and the accounts nearly converge. Callard would likely resist the dichotomy, and the disagreement is left standing.

### 7.2 Paul: An Epistemic Obstacle and a Structural One

Paul (2014) supplies the vocabulary the analytic literature expects. Her transformative experiences are *epistemically* transformative (one cannot know what the outcome is like without undergoing it) and *personally* transformative (undergoing it changes one's core preferences), so standard decision theory fails: the agent cannot assign values to outcomes she cannot access.

The obstacles differ. Paul's is **epistemic** and would be removed by information. The trilemma's survives that removal: grant the agent complete knowledge of the post-transformation state, including the values she would then have, and she still cannot formulate the transition as control, because "improvement" needs an evaluative point and that point is what is at issue. Paul's problem is that one does not know the value of the outcome; this paper's is that no standpoint makes "the value of the outcome" well-defined *across* the transition. The claims are independent, and this paper's target is Paul's *personally transformative* class.

Paul's own proposal, to decide on the value of *revelation*, installs a higher-order criterion relative to which the first-order transformation is evaluated. That is §6.7's reabsorption, reached independently.

### 7.3 Pettigrew and Bykvist: Aggregation as Reabsorption

Pettigrew (2020) is the most direct *formal* competitor, because he constructs exactly the object the trichotomy says collapses: a decision theory for agents whose utilities change. His metaphysical starting point is that a person is a corporate entity composed of person-like parts, "selves"; his **Aggregate Utility Solution** holds that each self should act not on its own values but on a *weighted average of the values of all the selves at all times*. Its precursor is Bykvist's (2006) account of prudence for agents whose actions will shape their preferences, which evaluates each possible life by the attitudes the agent holds while leading it: again a fixed higher-order rule for adjudicating between the evaluations of changing selves.

On this paper's reading Pettigrew is not a falsifier but the best worked-out *example* of §6.7's reabsorption. The aggregation rule is a fixed higher-order evaluative structure: the weights, and the prior decision to aggregate at all, are not themselves up for revision by the selves whose values they combine. Relative to that structure the changing first-order values are *data*, not transformations of the evaluative point — and the trilemma reapplies one level up exactly as §6.7 predicts. Either the weights are fixed, in which case the fixed evaluative point has merely moved upward and conversion has not been formulated but relocated; or the weights change too, and require weights on weights, terminating in a regress or an arbitrary stopping point.

Pettigrew has a reply, and it should be stated because it is the strongest objection the paper faces. The aggregation, he can say, is not a *value* but a *constraint of rationality*, and constraints of rationality are not the kind of thing conversion transforms; to treat them as an evaluative point is to equivocate. This paper's premise (§2) denies exactly that distinction for its own purposes: any structure that determines choice, and relative to which outcomes are ranked, functions as an evaluative point for the argument, whatever its philosophical classification. That is a substantive disagreement rather than a definitional one, and it marks the single clearest place where a reader who rejects the paper's founding premise will part company with it. Naming that is more useful than pretending the premise is neutral.

### 7.4 Formal Models of Preference Change: Dietrich and List, Hansson, and Becker's Invariant Tastes

The formal theory of preference change is the most direct place to look for a counterexample. It supplies three cases.

Dietrich and List (2013) derive an agent's preferences from a *weighing relation* over combinations of motivationally salient properties; preferences change when different properties become salient. They are explicit about what does not change: "the underlying stable feature characterizing an agent is not the agent's preference order … but the agent's weighing relation over property combinations", and in their model "preference change goes along with a stable weighing relation". Nothing in the model steers salience toward a target, so it is not control. But it is the clearest formal instance of reabsorption (§6.7): first-order preferences move because a coordinate moves within a fixed higher-order structure. A change of the weighing relation itself, which conversion would be, lies outside the model, and its authors leave open how an agent comes to have one.

Hansson's (1995) models of preference change follow belief revision (revision, contraction, addition and subtraction of alternatives, under postulates for rational change). The operator and its postulates are held fixed while first-order preferences move.

Becker's methodological thesis, that all preference change should be explained against invariant fundamental tastes, is the reabsorption move adopted as a research programme. Bradley (2009) shows its reach and its price. If the space of fundamental states may be refined at will, Becker's demand can seemingly always be met; but refining the state space "can be as ad hoc from a methodological point of view as postulating changes in fundamental desires". That is the vacuity worry of §6.7, stated in decision theory first. Of Bradley's three models, the first, classical conditioning, changes information and holds fundamental beliefs and desires fixed, so it is reabsorption by construction. The third, generalised conditioning, can represent any change in an agent's attitudes, fundamental desires included, and so represents what this paper calls conversion. It is not a counterexample, because it is a kinematics: it relates attitudes before and after and says nothing about what produces or directs the change.

None of the three, then, directs or evaluates a change of fundamental values without a fixed higher-order reference. Each either holds such a reference fixed (Dietrich and List, Hansson, Becker) or represents the change without saying what brings it about (generalised conditioning). The paper's claim is accordingly about models that direct or evaluate value change, not about the possibility of representing it.

### 7.5 The Wider Literature, and Priority

Several further positions bear on the argument and are recorded here with the specific work each does.

**Frankfurt** (1971) supplies the hierarchy of higher-order desires that the "one level up" move of §6.7 presupposes; the paper's claim is only that a control formulation forces the regress. **Korsgaard** (2009) presses the sharpest internal challenge after Callard: if agency constitutes itself through action, the fixed evaluative point may be an artefact of the control framing, and the trilemma a result about controllers rather than agents. **Parfit** (1984) supplies the identity-through-change background of the contract $I$ (§4). **Bratman** (1987, 2007) offers the nearest positive mechanism for the endogenous horn: planning agency and the standing policies that keep intentions stable.

**Priority.** That transformative choices lie outside ordinary decision theory is not new. **Ullmann-Margalit** (2006) argued that decision theory holds for "middle-sized" decisions and that "big" ones (opting, converting, drifting) may need separate treatment; Paul and Callard develop the epistemic and agential versions, and **Villiger** (2024) surveys the literature since. **de Blanc** (2011) posed the *ontological crisis* of an agent whose goal is defined over an ontology it replaces. **Carroll et al.** (2024) show that eight formal notions of alignment under changing preferences each either permit influence on those preferences or are overly risk-averse. This paper adds the case-by-case claim of this section, a dynamical reading of why a controller cannot generate the change of its own evaluative point (§6.5), and the costing of the exogenous alternative (§6.3). It does not claim the observation that optimization cannot choose its own criterion.

**Arpaly** (2003) is the hard case. Her Huckleberry Finn changes morally *without deliberation* and *against his avowed principles*, responding to reasons he cannot articulate. The change is plainly not a control process. It is a Class-G candidate only if his companionship with Jim is declared as the external occasion (§6.6, §8.4); change produced by his own processes alone would fall under the endogenous horn. No empirical test of the case has been made.

### 7.6 Is the Unanchored Class Non-Empty? The Concession's Own Non-Vacuity Check

The concession to Callard in §7.1 narrowed the thesis to value change that is not proleptically anchored. **If nearly all real value change is anchored, the theorem is technically true and substantively empty.** So: what is in the unanchored class?

Callard supplies the decisive fact herself. Aspiration is a form of **agency**: the aspirant works at acquiring the value, over time, for reasons she can partly articulate. So **all non-agential value change lies outside her account by construction**, and that class is not empty. Three kinds of member survive.

*Value change under what happens to one.* A parent whose evaluative structure is reorganised by the death of a child has not aspired to the new structure or held a defective grasp of it in advance. Such change is unanchored and common. It is not automatically Class G: where it destroys agency it belongs to the exogenous horn or the U-limit (§9).

*Non-deliberative moral change.* Arpaly's Huckleberry Finn (§7.5) changes against his avowed principles, responding to reasons he cannot articulate, without working at it. He has no proleptic grasp of the value he arrives at, since he believes throughout that he is doing wrong. It is the strongest case: neither traumatic nor agential, and uncontroversially a change in what he values.

*Conversion of the hostile.* James's (1902) abrupt cases, and the paradigm cases of the theological tradition, involve subjects actively opposed to the value acquired. Callard can reply that the convert often had some prior thread (a longing, a misdirected zeal) that can be redescribed as the proleptic grasp. Where that succeeds, the case is hers. But the reply reinterprets the transformation as continuous with what preceded it, which turns conversion into refinement, Case 1. The disagreement is about whether that redescription is always available and true.

The class is **non-empty**, so the theorem is not vacuous, and its members share a recognisable phenomenology (suddenness, passivity, prior resistance) that James documented long before this apparatus. The cost is that the domain is smaller than the paper first implied, and its boundary is drawn by someone else's distinction.

The trilemma does not touch the ordinary, worked-at, proleptically guided value acquisition that makes up most of a life, and which Callard describes better than this framework could. What remains is the class of transformations one *undergoes* rather than *undertakes*: what "conversion" was supposed to name, now said explicitly.

### 7.7 The Trichotomy as a Corrigibility Result

The trilemma also bears on **corrigibility**, the problem of building an agent that permits its objectives to be modified without resisting (Soares et al. 2015). It predicts that corrigibility cannot be secured by building acceptance of modification into the objective, which is still a fixed evaluative point optimized against (Case 1), nor by external override, the exogenous horn. **Value learning** (Hadfield-Menell et al. 2016; Russell 2019) is reabsorption: "maximize the unknown true reward" is a fixed higher-order objective, and the agent refines an estimate while its evaluative point stays put. Two recent limits are distinct from this one: Nayebi (2025) shows that verifying corrigibility after arbitrary modification is undecidable, a claim about predicates over programs, and Wang et al. (2025) give a capacity condition for learnability under self-improvement. The trilemma's claim is dynamical, and it is falsifiable: a corrigible agent whose corrigibility is neither an optimized objective nor an override would refute it.

---

## 8. Class G as the Residual Admissibility Profile

Class G is not a fifth class alongside R, P, M and Lambda, and it is not a discovered mechanism. It is the *shape of the space the trilemma leaves empty*: the type signature any non-coercive, identity-preserving, value-reordering transformation must satisfy, given that the three control strategies are excluded. It is an admissibility predicate: its conditions are necessary constraints that exclude inadmissible transformations, not causal laws, and they do not say what causes transformation.

### 8.1 Mode-Selective Transformation, Not Totalizing Control

The exogenous horn fails because brute control is *totalizing*: to guarantee a trajectory it collapses all tangential freedom. The escape is *mode-selectivity*: contracting only the destructive transverse directions while protecting the agency-bearing ones.

In words, mode-selective transformation has four requirements:
- destructive deviation along the identity-bearing directions contracts;
- identity-bearing spread stays below its critical value ($D_{id} < D_c$);
- agency-bearing openness is preserved ($D_{ag} > 0$);
- the rate at which agency-bearing excursions are pulled back is held near zero, neither contracting (which freezes agency) nor expanding (which disperses it).

The pair of spread constraints negates the exogenous horn's signature. Totalizing control collapses agency to guarantee identity; mode-selective transformation protects both (Appendix A.2).

The neutrality condition $\lambda_\parallel = 0$ is a knife-edge, the measure-zero boundary between contraction (which freezes agency) and expansion (which disperses it), so protected openness is a *maintained* condition, not an accident. The decomposition has a dynamical rationale: in dissipative systems far from equilibrium, a few slow modes (order parameters) enslave the fast ones (Haken 1983; Carr 1981). The identity-bearing directions are the slow subspace carrying the constitutive invariants; the agency-bearing directions are the faster subspace where exploration occurs.

A reasonable objection: under external noise no real system can hold a Lyapunov exponent at exactly zero; fluctuations in the coupling would push $\lambda_\parallel$ off the knife-edge and accumulate into drift on the identity-bearing modes. Class G does not demand exact neutrality. It demands that the effective exponent stay within a band, $|\lambda_\parallel^{eff}| < \eta$, and that deviations be corrected faster than they leak into the constitutive subspace: a *rate inequality*, $r_{repair} > r_{leak}$.

A more serious objection follows. If repair is an active feedback loop that restores a set-point, it is the ultrastability of the endogenous horn (§6.2), and Class G has smuggled endogenous control back in. The reply separates two things the word "repair" conflates: the *maintenance* of an established viable corridor, and its *establishment*. Ashbyan feedback is fully adequate to maintenance, and a converted system maintains approximate neutrality by ordinary regulation. That is no embarrassment, because *maintenance is not conversion*: the first horn excludes endogenous dynamics as the source of the reordering, not of subsequent stability. The division of labour is strict. Establishing the corridor is the work of a Class G transformation and cannot be endogenous. Maintaining it must be endogenous, because externally maintained neutrality would be continuous coercion. A process that is only the maintaining loop is homeostasis, not Class G.

A sharper form of the objection: how can an externally established corridor couple to a pre-existing maintaining loop unless the corridor was already in the system's latent variety? The tempting reply, that the external transformation supplies a new *set-point* to a generic loop, would destroy the thesis, since set-point tracking is the elementary operation of control. A set-point is a target within a fixed space of accessible states. What a Class G transformation alters is *the transition structure itself*, the generator that fixes which states are accessible from which. It changes the wiring, not the dial. What pre-exists is not the corridor but the capacity to stabilize whatever generator obtains, within the system's viability constraints (thermodynamic admissibility, the gradients and flux the structure requires). That capacity is neither target-specific nor omnipotent, and the external transformation is admissible only if the corridor it opens is viable. Nothing in the coupling is a set-point.

A dense nonlinear model can in principle describe such a restructured substrate, and a controller furnished with the description could force a system along the same trajectory. The paper does not claim the trajectory is unreachable by exogenous means. It claims that forcing reaches it only by the second horn, and so cannot reproduce *conversion*, whose mark is that agency survives.

Forcing a prescribed trajectory is **coercive dimensionality reduction**: to hold the commanded path the controller contracts the agency-bearing directions, and the system arrives as a contracted point. A Class G transformation is **geometric reconfiguration**: a change of the generator that changes which states are accessible, after which the system reorganizes with its repertoire preserved or enlarged (Appendix A.2). Both can pass through the same point in state space. The only control that reproduces the trajectory does so by the collapse the second horn names, so the negative claim is exact over the conjunction that defines conversion: reaching the new corridor *while* keeping agency-bearing openness intact.

### 8.2 Externality and Orientation-Gated Receptivity

The endogenous horn fails because change from $\langle F_0 \rangle$ is organization-preserving. The escape is *externality*: the transformative field must not lie in the span of the system's own dynamics. But pure externality, imposed without regard to the subject, is the exogenous horn. The escape from *that* is *receptivity*: the subject's orientation must modulate the coupling without generating the field.

In words, the transformative field is the product of two factors:
- an **external field**, not generated by the system's own dynamics;
- a **receptivity gate**, set by the subject's orientation.

The orientation does not create the field; it modulates receptivity to it. Each factor carries an exclusion:
- a field inside the span of the system's own dynamics returns the endogenous horn;
- a gate that does not vary with orientation returns coercion, because the outcome is then fixed whatever the subject's orientation.

A candidate transformation that fails either exclusion is not Class G. The formal statement is in Appendix A.4.

### 8.3 Definition of Class G as a Type Signature

A Class G intervention is an external, orientation-gated transformation of the effective landscape that lowers the transition barrier from dispersive dynamics toward Lambda-like persistence, while preserving agency, protecting identity-bearing modes, and preventing collapse into periodic closure. It is a type signature for admissible transformation, not a controllability theorem; it establishes no existence result and no constructive protocol.

| No. | Condition | Function | Horn it escapes |
|---|---|---|---|
| 1 | The barrier toward Lambda-like persistence is lower under the intervention than without it | Lowers the barrier toward transformation | — |
| 2 | Agency-bearing openness stays above zero | Preserves agency and exploration | Exogenous |
| 3 | Identity-bearing spread stays below its critical value | Protects identity-bearing invariants | — |
| 4 | Destructive transverse deviation contracts | Contracts destructive transverse deviation | — |
| 5 | The tangential rate is held near zero, or the tangential spectrum is otherwise protected | Prevents collapse into a point or loop | Exogenous |
| 6 | Long-time correlation power is nonzero | Preserves long-time memory | — |
| 7 | The identity-relevant observable has no exact period | Avoids mechanical periodicity | — |
| 8 | The drive is incommensurable or inexhaustible | Sustains aperiodicity (no fixed optimum target) | Optimization |
| 9 | The field factors into an external field and a receptivity gate that varies with orientation | Separates the external field from the receptivity gate | Exogenous |
| 10 | The external field is not in the span of the system's own dynamics | Prevents reduction to endogenous feedback | Endogenous |

The conditions in symbols are in Appendix A.5.

The conditions are read as a single conjunctive exclusion criterion: each line rejects a class of near-miss transformations, and a candidate is G-admissible only if it survives all ten exclusions at once.

**The conjunction is satisfiable, and it discriminates. Both were checked, not assumed.**
- *Satisfiable.* A pre-registered test built an explicit stochastic system that meets all ten conditions at once, each against a threshold fixed in advance.
- *Discriminating.* Every near-miss in the filter table below fails the conditions the table predicts it should.
- *Not ten independent hurdles.* A second test found that about six of the ten can be broken in isolation, and the rest are entailed by others. The criterion is therefore a filter of roughly six independent constraints with several entailed consequences, and the count of ten should be discounted accordingly.

What this establishes is logical non-emptiness and exclusionary content, nothing more. Whether any biological, psychological or theological process instantiates the profile remains open. The measured values and the entailments are in Appendix A.5.

The conjunction may be *empty* in a given domain, and then the grammar has done its work by identifying the absence. Conditions 1, 3 and 4 make the identity-bearing region controlled-invariant in the sense of viability theory, and conditions 2 and 5 forbid achieving that by collapse to a point (Aubin 1991; Ames et al. 2019).

The G-admissibility filter applied to the candidate transformations considered here is consistent with Class G being the residue of the trilemma:

| Candidate | What it satisfies | Where it fails | Diagnosis |
|---|---|---|---|
| Classical damping | Contracts destructive transverse deviation | Collapses agency-bearing openness | Totalizing stabilization (exogenous horn) |
| External forcing | External source | No receptivity gate; risks identity-bearing spread above its critical value | State imposition (exogenous horn) |
| Endogenous feedback | Continuity, adaptation | Field inside the endogenous span $\langle F_0\rangle$ | Self-optimization (endogenous horn) |
| Coercion | Reduces a barrier or imposes a state | Decouples the receptivity gate; collapses agency-bearing openness | Coercive transition (exogenous horn) |
| Conversion / sanctification | Trajectory preserved, reorientation allowed | G-admissible *only if* external, receptive, non-coercive, identity- and agency-preserving | G-admissible (conditional) |

### 8.4 Is Class G Just Ordinary Interpersonal Influence?

As defined in §8.3, Class G is external, gated by the agent's receptivity, selective about which modes it changes, and driven towards no fixed optimum target (condition 8); the occasion it involves commands no path (§6.3, §6.5). A reader may ask whether that is simply what a friend, a mentor, a book or an encounter does when it gives reasons. If so, the paper's conclusion would reduce to "control does not model conversion, but encounter and persuasion do". That is plausible, but not new.

Class G is narrower than ordinary influence, and this follows from commitments the paper has already made rather than from a new stipulation. The paper cedes the anchored case of value change to Callard (§7.1), and it reads Bradley's first model, change by new information with fundamental desires held fixed, as reabsorption (§7.4). Persuasion by reasons the agent can assess by her present lights is exactly that model. The input is external, but the standard that evaluates it is fixed. The efficacy of such persuasion is computed inside the agent's pre-existing evaluative structure, so it belongs to the endogenous horn (§6.2).

Externality of the *input* is not externality of the *reorganizing field* in the sense of §8.2. That section requires that the field not lie in the span of the system's own dynamics. An agent's response to reasons she already has the standards to weigh lies in that span.

**The criterion.** An influence is *anchored* if the agent's pre-change standards, applied to the input taken as a reason, would rank the post-change evaluative state above the pre-change one. The change is then endorsable ex ante, and the influence falls under the endogenous horn, however external its source. Class-G candidates are the remaining cases. In them, the post-change structure is not endorsable by the agent's pre-change lights. Yet the change is endorsed afterwards, the accountability relation of §6.6 is intact, and the agent's receptivity gated the coupling.

The criterion does not beg the question. It refers only to the pre-change standards and to the input, and it says nothing about whether the change "was a conversion". It uses the same asymmetry between the ex-ante and the ex-post standpoint on which Paul's account of transformative experience and Ullmann-Margalit's notion of converting already rely.

**What the criterion classifies.** It classifies descriptions, not events. Whether a historical change was anchored depends on what the agent's pre-change standards contained. The observer must declare that content as part of the contract, and it is contestable under §4.1.

Callard's reply belongs here. For any apparent Class-G case, she can redescribe some prior thread of the agent's valuing as a proleptic grasp of the new value. In the terms of this section, that is a rival contract: it attributes to the pre-change standards a content that makes the change endorsable ex ante. The paper does not adjudicate between the two contracts. It locates the dispute precisely, in the content of the pre-change contract, and that is where any evidence would have to bear.

What the paper claims, then, is conditional. If unanchored changes occur, their admissible form is Class G. Whether they occur is the non-vacuity question of §7.6, and it remains open.

**Manipulation.** The anchored criterion does not by itself exclude manipulation. A manipulated change is not endorsable by the agent's pre-change standards, may be endorsed afterwards, and leaves the accountability relation intact. What excludes it is a condition Class G already carries: its drive has no fixed optimum target (§8.3, condition 8). A manipulator selects the content of the values the agent is to end with and steers towards it, so the change is driven towards a fixed evaluative point, the manipulator's. Reading condition 8 this way is an interpretation of a formal condition about the drive, not a consequence of it, and the paper offers it as such. That is control in the paper's sense, with the fixed point relocated from the agent to the manipulator, and it inherits the trilemma: tracking returns the exogenous horn, and a one-shot implantation of chosen values is directed change towards a point fixed outside the agent. A Class-G occasion constrains the regime the agent moves towards, persistence without dissolution, freezing or dispersal, and not the content of the values she arrives at. Whether every real case can be sorted by this distinction is contestable; the paper claims only that the distinction is the one Class G's conditions draw.

**What this leaves of encounter.** Encounter is wider than Class G and includes it. The mentor who gives reasons the agent can already weigh is anchored influence. The mentor whose example changes what the agent can see as a reason at all is a Class-G candidate. So is non-deliberative moral change of the kind Arpaly describes in Huck Finn, provided the occasion lies outside the agent, as Huck's companionship with Jim does. What changes him is not reached by his explicit standards, and it is endorsed, if at all, only afterwards. A non-deliberative change produced by the agent's own processes alone would fall inside the admissible boundary of §6.6 and under the endogenous horn. The contribution of the formal apparatus over "encounter and persuasion" is to say which part of encounter the formal models of section 7 cannot represent, and why: those models hold the evaluating standard fixed, and the unanchored part of encounter is exactly the part in which that standard is what changes.

---

## 9. The U-Limit: Identical Signature, Divergent Post-Jump Topology

The profiles above sort continuous, receptively mediated transformations. One externally occasioned case is not a flow: a discrete unilateral jump that the subject's antecedent orientation does not gate, and that nonetheless leaves the subject an agent. Call it the U-limit. At the instant of the jump its signature is the same as coercion's; the two differ in post-jump topology. Coercion deposits the subject in a rigid basin with its future closed, and the U-limit on an open, aperiodic manifold with subsequent agency preserved, $D_{ag}^{post} > 0$. The paper needs the profile because §7.6 counts the conversion of the actively hostile as unanchored, and for a hostile subject Class G's receptivity gate is closed. The admissibility conditions are in Appendix A.6.

## 10. Conclusion: The Insufficiency of the Control Paradigm

This paper has defended a negative thesis. The control trilemma argues that the three control-theoretic strategies for directed transition each fail for a subject whose identity and agency must both survive: endogenous change preserves organization and so is not conversion; tracking reaches the target only at a cost to agency that becomes total in the limit; and optimization is undefined across a change of the evaluative standard. Given the paper's definition of control, the framework cannot *formulate* conversion, and §6.7 concedes that at this level the result follows from the definitions. The claim that does not follow from them is that of section 7: the formal models that direct or evaluate value change each hold an evaluative point fixed.

What survives is an admissibility profile, Class G (externally occasioned, receptivity-gated, mode-selective, value-reordering), stated as a type signature rather than a mechanism, and conditional: if unanchored changes occur, this is their admissible form (§8.4).

The framework makes no theological claim and explains no conversion. Its result is definitional at its top level (§6.7), quantitative at the exogenous horn, and part measure-theoretic, part interpretive in the endogenous case: recurrence for invariant-measure-typical states, an interpretive argument for dissipative transients. The most developed scientific account of directed change cannot deliver agentive, value-reordering, non-coercive transformation without holding fixed what that transformation changes.

> Persistence under transformation is neither frozen sameness nor unrestricted flux. The control paradigm can damp it, force it, or optimize within it; it cannot transform it without erasing it. What transformation without erasure requires is exactly what the paradigm leaves empty.

---

## Appendix A. Formal Apparatus

The body states the argument in prose. This appendix collects the formal statements the body relies on, in the order the body uses them. It adds no claim the body does not make, and where a passage below says "this section" or "above", it refers to the body section named in its heading.

### A.1 The Diagnostic Taxonomy and the Correlation-Power Condition (§5)

The four regimes are defined in words in §5, always relative to a contract $(I, f, \epsilon, \tau)$. The one formal condition is the correlation-power condition. For a mean-zero observable $f$, define the autocorrelation under the flow $C_f(t) = \langle f, U_t f \rangle$, with $U_t$ the Koopman evolution, and the correlation-power average $P_f(T) = \frac{1}{T}\int_0^T |C_f(t)|^2\,dt$. A system preserves the relevant pattern if $\liminf_{T\to\infty} P_f(T) > 0$; in finite applications this is a pre-specified finite-window estimate, validated against phase-randomized surrogates. The condition separates Lambda from Class M: an observable with non-trivial projection onto the point spectrum of $U_t$ retains correlation power, whereas one in the absolutely continuous spectrum has $C_f(t)\to 0$ by Riemann–Lebesgue (Walters 1982; Halmos 1956). In computational mechanics the same separation appears as substantial excess entropy on an aperiodic observable (Crutchfield and Young 1989; Crutchfield 2012). The condition is necessary, not sufficient: long-memory processes also retain correlation power, and Lambda requires retention on the specific observable the contract designates as carrying a constitutive invariant.

### A.2 The Identity/Agency Decomposition (§6.1, §8.1)

Near the identity manifold $M_\Lambda$, decompose the tangential space into a transverse identity-bearing subspace and a tangential agency-bearing subspace, $TM_\Lambda = E_{id}\oplus E_{ag}$. Mode-selective transformation requires $\lambda_\perp < 0$ (destructive transverse deviation contracted), $\lambda_\parallel = 0$ or a protected non-mixing tangential spectrum (agency neither frozen nor dispersed), $D_{id} < D_c$ (identity-bearing diffusion below threshold) and $D_{ag} > 0$ (agency-bearing diffusion preserved). The pair $D_{id} < D_c$, $D_{ag} > 0$ negates the exogenous horn's signature $D_{ag}\to 0$. Forcing a trajectory drives $\lambda_\parallel \to -\infty$ and collapses the policy repertoire $H(\pi)$; a Class G reconfiguration of the generator keeps $D_{ag} > 0$ and $H(\pi)$ intact under the new geometry (§8.1).

### A.3 The Meta-Optimization Collapse Theorem (§6.5)

**The Meta-Optimization Collapse Theorem (endogenous-preference case).** Let the cost be parametrized by a value state $\theta$ that evolves under an endogenous dynamics $\dot\theta = f(\theta)$ (the agent revises its own preferences), and suppose the value state remains confined to a compact set $K$ — a necessary condition for the agent to be a persisting system rather than one whose values diverge to infinity. Decompose $f$ by Helmholtz–Hodge into a gradient part and a divergence-free part, $f = -\nabla V + g$ with $\nabla\!\cdot g = 0$ (Bhatia et al. 2013; Glötzl & Richters 2023). One technical caveat must be stated for the decomposition to be well-posed on a *compact* set $K$: on a bounded domain with boundary the Hodge decomposition acquires a third, harmonic component, $f = -\nabla V + g + h$ with $h$ both curl-free and divergence-free, and the decomposition is unique only once boundary conditions are fixed. The harmonic term does not open a fourth dynamical category: being curl-free it is locally the gradient of a harmonic potential and groups with Case 1 wherever it is exact, while any non-exact (cohomologically nontrivial) circulation it carries behaves dynamically like the divergence-free part and groups with Cases 2–3. The trichotomy below should therefore be read as a partition by *asymptotic behavior* (descent to a potential minimum; unbounded non-attracting drift; bounded attractor), which is exhaustive regardless of how the boundary-dependent harmonic remainder is apportioned. With that understood, exactly one of three cases holds, and *none* of the three is conversion.

*Case 1 — the integrable case (Bellman returns).* If $g\equiv 0$, or more generally if $f$ admits a global scalar potential (equivalently, an integrating factor rendering it a gradient flow), then $\dot\theta = -\nabla V$ is descent on a fixed meta-potential $V$. The "new" cost $J_{\theta(t)}$ is then not an axiological rupture but a moving coordinate within the single invariant objective $V$: the system is performing optimization in the extended space $(x,\theta)$, and the third horn of the trilemma — the Bellman incommensurability of §6.4 — applies to $V$ exactly as it applied to a fixed $J$. The meta-objective has simply absorbed the preference change. Conversion, which requires that there be *no* fixed evaluative point even at the meta-level, is excluded by hypothesis.

*Case 2 — the dispersive case (Class M).* If the divergence-free part dominates and the flow has no attracting invariant set within $K$ — equivalently, the value state wanders without settling — then preferences cycle: the divergence-free component of a value field generically induces intransitive preference loops ($A\succ B\succ C\succ A$, the classical "value pump"), and the agent suffers chronic temporal inconsistency. It never reaches a directed, permanent reordering; it fluctuates. This is precisely Class M dispersion in the companion vocabulary — motion without retention — and it fails conversion's first constitutive property, *permanent stabilization in a new regime*.

*Case 3 — the recurrent case.* A flow with non-zero curl ($g\not\equiv0$, escaping Case 1) that possesses a bounded attracting invariant set in $K$ (escaping Case 2). Conversion is excluded from each attractor type, by two different arguments. (i) A *fixed point* is a permanent terminus with zero asymptotic entropy: $D_{ag}$ collapses, so it fails openness, not by recurrence. (ii) A *limit cycle* is rigidly periodic, closed recurrence rather than a new regime. (iii) A *strange attractor* (e.g. Lorenz; Strogatz 2015) is bounded and aperiodic with positive Lyapunov exponent, so it is open, but it fails permanence. A dissipative attractor does not preserve the ambient measure, so Poincaré recurrence applies to the flow restricted to the attractor with its finite invariant (SRB) measure (Poincaré 1890; Walters 1982): almost every point of the attractor returns arbitrarily close to itself. Numerically the Lorenz attractor's recurrence fraction is $0.98$–$0.995$ for return radii $\varepsilon \gtrsim 0.05\cdot\text{span}$, falling to $\approx 0.51$ at $\varepsilon = 0.01\cdot\text{span}$. Openness is purchased at the cost of recurrence on the attractor.

**The compactness assumption.** The theorem assumes the value state stays in a compact set. An earlier version excluded unbounded drift as a failure of persistence; that is **false**. A quasi-periodic dynamics with incommensurable frequencies and exponentially growing amplitude escapes every compact set while retaining correlation power ($P_f \approx 0.17$–$0.21$ against a $0.05$ bar, $p = 0.005$ against phase-randomized surrogates). What excludes it is **recurrence on the quotient**: a scale-indifferent contract reads the direction, the direction lives on a sphere, and recurrence applies there. The escaping cell is therefore closed by the *same* argument as the bounded cell, but only conditionally: for contracts that factor through a *bounded reading*. Saturating and linear cardinal contracts leave the observable recurrent (return fractions $0.81$–$0.93$). Exponential contracts are **not testable by this instrument**: they are the only ones that could break recurrence and the only ones that overflow the estimator ($P_f = 0.0006$ against $0.15$–$0.21$ for the other readings), so the exclusion is systematic and correlated with the property under test. Whether every admissible contract factors through a bounded reading is the open problem of §6.5.

### A.4 Externality and Orientation-Gated Receptivity (§8.2)

Let $W_G(x, t; \Xi, \theta) = \chi(\theta)\, W_{ext}(x, t; \Xi)$, where $W_{ext}$ is not generated by $F_0$, $\Xi$ is the external source, $\theta$ is orientation/receptivity, and $\chi(\theta)$ modulates coupling strength. The orientation does not create the field; it modulates receptivity to it. Each factor carries an exclusion. The requirement $W_{ext}\notin\langle F_0\rangle$ excludes endogenous optimization (the first horn). The requirement that $\chi(\theta)$ genuinely vary with $\theta$ excludes coercion (the second horn): if $\chi$ is constant in $\theta$, the outcome is fixed regardless of orientation, which is mechanical imposition. A candidate transformation failing either exclusion is not Class G — the first failure returns self-optimization, the second returns coercive control.

### A.5 The Class G Conditions in Symbols, and the Satisfiability Tests (§8.3)

| No. | Condition | Function | Horn it escapes |
|---|---|---|---|
| 1 | $\Delta V^G_{M\to\Lambda} < \Delta V_{M\to\Lambda}$ | Lowers the barrier toward transformation | — |
| 2 | $D_{ag} > 0$ | Preserves agency and exploration | Exogenous |
| 3 | $D_{id} < D_c$ | Protects identity-bearing invariants | — |
| 4 | $\lambda_\perp < 0$ | Contracts destructive transverse deviation | — |
| 5 | $\lambda_\parallel = 0$ or protected tangential spectrum | Prevents collapse into a point or loop | Exogenous |
| 6 | Long-time correlation power nonzero | Preserves long-time memory | — |
| 7 | No $T>0$ with $f(\Phi_{t+T})=f(\Phi_t)$ for identity-relevant $f$ | Avoids mechanical periodicity | — |
| 8 | Incommensurable or inexhaustible drive | Sustains aperiodicity (no fixed optimum target) | Optimization |
| 9 | $W_G = \chi(\theta)W_{ext}$ | Separates the external field from the receptivity gate | Exogenous |
| 10 | $W_{ext}\notin\langle F_0\rangle$ | Prevents reduction to endogenous feedback | Endogenous |

**The conjunction is satisfiable, and it discriminates — both were checked rather than assumed.** A conjunctive criterion of ten conditions invites two opposite and equally fatal objections: that it is *empty by over-specification* (no object whatever meets all ten, so the "residual profile" is a residue of nothing), or *vacuous by under-specification* (everything meets all ten, so the filter excludes nothing). A pre-registered test settles both. An explicit stochastic system — a regime coordinate on a double well, a contracted transverse deviation from an identity manifold, two protected phases advancing at incommensurable frequencies, an Ornstein–Uhlenbeck agency coordinate, and an orientation variable driving a receptivity gate, with the intervention *lowering the landscape barrier* rather than commanding a path — satisfies all ten conditions simultaneously, each measured against a threshold fixed in advance: the barrier falls $0.250\to0.107$ (mean first-passage $386\to187$), agency variance is $0.50$, identity diffusion $0.020$ sits below a *measured* critical value $D_c=0.100$, $\lambda_\perp=-1.01$ while $\lambda_\parallel=0.000$, long-time correlation power is $0.22$, the identity observable admits no exact period (sup-norm period error $4\times10^{-2}$ against a $10^{-6}$ bar, on an instrument separately validated to flag genuinely periodic signals at $\approx10^{-8}$), the drive is incommensurable, the applied field factors exactly as $\chi(\theta)W_{ext}$ (rank-one to $10^{-16}$) through a gate that genuinely closes, and $W_{ext}$ resists projection onto a deliberately generous endogenous basis (residual $0.60$). So the ten conditions are mutually consistent. They also do real work: every near-miss in the §8.3 filter table is excluded, and each fails a condition the table predicts it should — classical damping on 2 and 5, ungated forcing on 9, endogenous feedback on 10, coercion on 2 and 9, a commensurable drive on 7 and 8. What this establishes is *logical* non-emptiness and exclusionary content, nothing more: whether any biological, psychological, or theological process instantiates the profile is exactly the question this section declines to answer, and remains open.

**The ten conditions are not ten independent hurdles.** A second test perturbed the witness to violate each condition in turn. Six of the ten (conditions 1, 2, 3, 4, 6 and 9) can be broken in isolation; the measured entailments are $5\Rightarrow6$, $5\Rightarrow7$, $8\Rightarrow7$ and $10\Rightarrow1$. Two are matters of logic and hold for any system: an incommensurable drive is aperiodic by definition, so 8 entails 7; and collapsing the tangential spectrum (5) destroys long-time correlation power (6) and makes the identity observable trivially periodic (7). The third may be specific to this construction. The criterion is therefore a filter of **about six** independent constraints. Counted by distinct failure signature the figure is nine; six is the conservative lower bound, and it is the one defended here.

### A.6 The U-Limit Admissibility Predicate (§9)

The U-limit bounds the magnitude of the unilateral intervention and requires agency to open after the transition:

$$U\text{-limit:}\qquad |W_U| < \Delta_c(Q_I, E), \qquad D_{ag}^{post} > 0,$$

where $W_U$ is the unilateral transformation, $\Delta_c(Q_I, E)$ the integrity threshold set by the support capacity of the projected invariant (so that the jump transforms rather than shatters it, against Class R), and $D_{ag}^{post}$ the agency-bearing diffusion available after the transition. $D_{ag}^{post} > 0$ is the post-jump topology: the U-limit opens a field of agency, where coercion closes one and dissolution leaves no "post" at all. The full predicate is a conjunction of exclusions:

$$\begin{aligned} \text{U-Adm}(x) \iff{} &\big[W_U \text{ functionally independent of } \mathcal{F}_{endo}\big] \;\land\; \big[\tfrac{\partial W_U}{\partial\theta}=0\big] \\ &\land\; \big[|W_U| < \Delta_c(Q_I, E)\big] \;\land\; \big[\mathbf{T}_U(x^-) \in \Omega_I\big], \end{aligned}$$

where $\mathcal{F}_{endo}$ is the set of transformations the system can actuate from its own resources, functional independence means $W_U$ is not derivable from or composable out of them (the endogenous horn applied to jumps), $\partial W_U/\partial\theta=0$ says orientation does not gate the jump, and $\Omega_I$ is the viable region in which the trajectory class is preserved.

**Why this is not coercion under another name.** If $\Omega_I$ were a viability set given in advance, the U-limit would be state-constrained optimization: a barrier functional penalizing departure from $\Omega_I$, with survival in the envelope as a fixed higher-order criterion, and the jump would be directed change towards a pre-given target. It is not. Only the thinnest layer, bare non-dissolution, is antecedent, and it is far too weak to pick out a corridor. *Which* corridor is viable for this identity is fixed by the reconfigured generator, because the generator determines which states are mutually accessible. $\Omega_I$ is a product of the transformation, not an input to it, so there is no target to steer towards before the jump.

**The continuity floor.** During the crisis that precedes reconfiguration, the projection that reads the identity-relevant macro-variable off the dynamics does not collapse to the empty set, which would sever the trajectory and make the result a replacement (Class R). It contracts to a minimal continuity kernel $P_\epsilon$ with $\epsilon > 0$: the identity-bearing variety thins without rupturing, while the orthogonal subspace expands to admit the reconfiguration. The floor is a property of the projection, not a global collapse of precision, which would disperse the system into Class M. $P_\epsilon$ is the projection-side counterpart of $\Delta_c$: one forbids a jump that shatters the invariant, the other a thinning that severs its history.

[^lean]: A Lean 4 formalization of the trichotomy and of the escape-horn step is kept in the repository (`formal/`), not in this paper. With the dynamical notions as opaque predicates and Poincaré recurrence and Conley's theorem stated as axioms in their true forms (almost everywhere with respect to the invariant measure; the ω-limit set in the chain-recurrent set), it checks only that the conclusions follow from those premises by propositional reasoning. It is not a mechanical verification of the dynamics. Its first version stated both theorems pointwise, which is false; `formal/Counterexamples.lean` refutes those forms in concrete models.

## References

Agar, Nicholas. 2016. "Enhancement, Mind-Uploading, and Personal Identity." In Steve Clarke, Julian Savulescu, C. A. J. Coady, Alberto Giubilini, and Sagar Sanyal, eds., *The Ethics of Human Enhancement: Understanding the Debate*. Oxford University Press.
Ames, Aaron D., Coogan, Samuel, Egerstedt, Magnus, Notomista, Gennaro, Sreenath, Koushil, and Tabuada, Paulo. 2019. "Control Barrier Functions: Theory and Applications." *2019 18th European Control Conference (ECC)*: 3420-3431. DOI: 10.23919/ECC.2019.8796030.
Adams, Alyssa, Hector Zenil, Paul C. W. Davies, and Sara Imari Walker. 2017. "Formal Definitions of Unbounded Evolution and Innovation Reveal Universal Mechanisms for Open-Ended Evolution in Dynamical Systems." *Scientific Reports* 7: 997. DOI: 10.1038/s41598-017-00810-8. (Closed finite systems are Poincaré-recurrent within their recurrence time; unbounded novelty requires coupling to an external environment.)
Arpaly, Nomy. 2003. *Unprincipled Virtue: An Inquiry Into Moral Agency*. Oxford University Press. (Moral change without deliberation; the Huckleberry Finn case.)
Ashby, W. Ross. 1956. *An Introduction to Cybernetics*. Chapman and Hall.
Ashby, W. Ross. 1960. *Design for a Brain: The Origin of Adaptive Behaviour*. 2nd ed. Chapman and Hall.
Aubin, Jean-Pierre. 1991. *Viability Theory*. Birkhäuser.
Bratman, Michael E. 1987. *Intention, Plans, and Practical Reason*. Harvard University Press.
Bratman, Michael E. 2007. *Structures of Agency: Essays*. Oxford University Press. (Planning agency and self-governance; standing policies as a mechanism for stability of intention.)
Callard, Agnes. 2018. *Aspiration: The Agency of Becoming*. Oxford University Press. (Proleptic reasons: acknowledged-defective versions of reasons one expects eventually to grasp; the most direct challenge to this paper's thesis.)
Bellman, Richard. 1957. *Dynamic Programming*. Princeton University Press.
Bowles, Samuel. 1998. "Endogenous Preferences: The Cultural Consequences of Markets and Other Economic Institutions." *Journal of Economic Literature* 36(1): 75-111.
Carr, Jack. 1981. *Applications of Centre Manifold Theory*. Springer.
Crutchfield, James P., and Young, Karl. 1989. "Inferring Statistical Complexity." *Physical Review Letters* 63(2): 105-108.
Feldbaum, A. A. 1965. *Optimal Control Systems*. Academic Press.
Crutchfield, James P. 2012. "Between Order and Chaos." *Nature Physics* 8(1): 17-24.
Frankfurt, Harry G. 1971. "Freedom of the Will and the Concept of a Person." *The Journal of Philosophy* 68(1): 5-20. (Second-order desires; the hierarchy the §6.7 "one level up" move presupposes.)
Hadfield-Menell, Dylan, Stuart J. Russell, Pieter Abbeel, and Anca Dragan. 2016. "Cooperative Inverse Reinforcement Learning." *Advances in Neural Information Processing Systems* 29. (Value learning as a fixed higher-order objective; §7.6 reads it as reabsorption.)
Haken, Hermann. 1983. *Synergetics: An Introduction*. 3rd ed. Springer.
James, William. 1902. *The Varieties of Religious Experience: A Study in Human Nature*. Longmans, Green. (Classical phenomenology of conversion: abruptness, passivity, retained identity.)
Halmos, Paul R. 1956. *Lectures on Ergodic Theory*. Chelsea Publishing.
Bechlioulis, Charalampos P., and George A. Rovithakis. 2008. "Robust Adaptive Control of Feedback Linearizable MIMO Nonlinear Systems with Prescribed Performance." *IEEE Transactions on Automatic Control* 53(9): 2090-2099. (Bounded tracking error with finite control authority.)
Ilchmann, Achim, Eugene P. Ryan, and Christopher J. Sangwin. 2002. "Tracking with Prescribed Transient Behaviour." *ESAIM: Control, Optimisation and Calculus of Variations* 7: 471-493. (Funnel control: prescribed error bound with finite, state-dependent gain.)
Korsgaard, Christine M. 2009. *Self-Constitution: Agency, Identity, and Integrity*. Oxford University Press. (Agency constituting itself through action; the sharpest internal challenge to a given evaluative point.)
Lewis, David. 1976. "Survival and Identity." In Amelie Oksenberg Rorty, ed., *The Identities of Persons*. University of California Press.
Paul, L. A. 2014. *Transformative Experience*. Oxford University Press. (Epistemically and personally transformative experience; the epistemic obstacle this paper's structural obstacle survives.)
Pettigrew, Richard. 2020. *Choosing for Changing Selves*. Oxford University Press. (The Aggregate Utility Solution: each self acts on a weighted average of the values of all selves; §7.3 reads it as the best worked-out instance of reabsorption.)
Bhatia, Harsh, et al. 2013. "The Helmholtz–Hodge Decomposition — A Survey." *IEEE Transactions on Visualization and Computer Graphics* 19(8): 1386-1404. (Helmholtz–Hodge decomposition of vector fields; uniqueness and boundary conditions on bounded domains.)
Conley, Charles. 1978. *Isolated Invariant Sets and the Morse Index*. CBMS Regional Conference Series in Mathematics 38. American Mathematical Society, Providence, RI. (The Fundamental Theorem of Dynamical Systems: every flow on a compact metric space admits a complete Lyapunov function, decreasing off the chain-recurrent set and constant on its transitive components — the gradient-like/chain-recurrent dichotomy.)
Glötzl, Erhard, and Oliver Richters. 2023. "Helmholtz Decomposition and Potential Functions for n-Dimensional Analytic Vector Fields." *Journal of Mathematical Analysis and Applications* 525(2): 127138. (Existence and structure of the gradient/divergence-free/harmonic parts in $\mathbb{R}^n$.)
Russell, Stuart. 2019. *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking. (Value learning and the assistance framing of alignment.)
Soares, Nate, Benja Fallenstein, Eliezer Yudkowsky, and Stuart Armstrong. 2015. "Corrigibility." In *AAAI Workshop on AI and Ethics*: 74-82. (The corrigibility problem; §7.6 gives the trilemma's structural prediction about its solution space.)
Nayebi, Aran. 2025. "Core Safety Values for Provably Corrigible Agents." arXiv:2507.20964. To appear in the AAAI 2026 Machine Ethics Workshop proceedings. (Deciding whether an arbitrarily modified agent ever violates corrigibility is undecidable by reduction to the halting problem; §7.7 places this neighbouring result and distinguishes its object — a predicate over programs — from the trilemma's dynamical claim.)
Wang, Charles L., Keir Dorchen, and Peter Jin. 2025. "On the Statistical Limits of Self-Improving Agents." arXiv:2510.04399 (TMLR 2026). (Distribution-free PAC-learnability is preserved iff the policy-reachable family stays uniformly capacity-bounded, a VC-dimension condition; §7.7 contrasts this static capacity limit with the trilemma's dynamical mechanism.)
Strogatz, Steven H. 2015. *Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering*. 2nd ed. Westview Press. (Limit cycles, strange attractors, and Lyapunov exponents.)
Lehman, Joel, and Stanley, Kenneth O. 2011. "Abandoning Objectives: Evolution Through the Search for Novelty Alone." *Evolutionary Computation* 19(2): 189-223. DOI: 10.1162/EVCO_a_00025.
Liberzon, Daniel. 2003. *Switching in Systems and Control*. Birkhäuser.
Parfit, Derek. 1984. *Reasons and Persons*. Oxford University Press.
Poincaré, Henri. 1890. "Sur le problème des trois corps et les équations de la dynamique." *Acta Mathematica* 13: 1-270. (Poincaré recurrence theorem.)
Schmidhuber, Jürgen. 2010. "Formal Theory of Creativity, Fun, and Intrinsic Motivation (1990-2010)." *IEEE Transactions on Autonomous Mental Development* 2(3): 230-247.
Singh, Satinder, Barto, Andrew G., and Chentanez, Nuttapong. 2004. "Intrinsically Motivated Reinforcement Learning." *Advances in Neural Information Processing Systems* 17 (NIPS 2004): 1281-1288.
Skoulakis, Stratis, Tanner Fiez, Ryann Sim, Georgios Piliouras, and Lillian Ratliff. 2021. "Evolutionary Game Theory Squared: Evolving Agents in Endogenously Evolving Zero-Sum Games." *Proceedings of the AAAI Conference on Artificial Intelligence* 35: 11343-11351. arXiv:2012.08382. (When agents and the game they play co-evolve endogenously, the coupled replicator dynamics is Poincaré recurrent.)
Sutton, Richard S., and Barto, Andrew G. 2018. *Reinforcement Learning: An Introduction*. 2nd ed. MIT Press.
Walters, Peter. 1982. *An Introduction to Ergodic Theory*. Springer.
Wiener, Norbert. 1948. *Cybernetics: Or Control and Communication in the Animal and the Machine*. Technology Press and John Wiley & Sons (New York); Hermann (Paris).
Wiggins, David. 2001. *Sameness and Substance Renewed*. Cambridge University Press.
Williams, Bernard. 1970. "The Self and the Future." *The Philosophical Review* 79(2): 161-180.
Ullmann-Margalit, Edna. 2006. "Big Decisions: Opting, Converting, Drifting." *Royal Institute of Philosophy Supplement* 58: 157-172. DOI: 10.1017/S1358246100009358. (Big, transformative decisions as a limit of decision theory; the prior statement of the observation this paper extends.)
de Blanc, Peter. 2011. "Ontological Crises in Artificial Agents' Value Systems." arXiv:1105.3821. (A goal defined over one ontology is ill-defined after the agent replaces that ontology.)
Carroll, Micah, Davis Foote, Anand Siththaranjan, Stuart Russell, and Anca Dragan. 2024. "AI Alignment with Changing and Influenceable Reward Functions." arXiv:2405.17713. (Dynamic-reward MDPs; alignment notions under changing preferences either permit undesirable influence or are overly risk-averse.)
Villiger, Daniel. 2024. "Transformative Experience." *Philosophy Compass* 19(6): e13000. DOI: 10.1111/phc3.13000. (Survey of the literature on transformative experience after Paul 2014.)
Bradley, Richard. 2009. "Becker's Thesis and Three Models of Preference Change." *Politics, Philosophy & Economics* 8(2): 223-242. DOI: 10.1177/1470594X09102238. (Becker's invariant tastes can almost always be saved by refining the state space, at a price "as ad hoc" as postulating taste change; generalised conditioning represents any change of attitudes, fundamental desires included. Quotations in §7.4 follow the working-paper version, CPNSS, LSE, 2008, and should be checked against the published text.)
Bykvist, Krister. 2006. "Prudence for Changing Selves." *Utilitas* 18(3): 264-283. DOI: 10.1017/S0953820806002032. (Prudence when actions shape preferences, evaluated by the attitudes held while leading a life; a fixed higher-order rule, precursor of Pettigrew's aggregation.)
Carroll, Micah, Anca Dragan, Stuart Russell, and Dylan Hadfield-Menell. 2022. "Estimating and Penalizing Induced Preference Shifts in Recommender Systems." ICML 2022. arXiv:2204.11966. (Optimizing systems have incentives to shift users' preferences; judging shifts requires a reference such as the uninfluenced dynamics.)
Dietrich, Franz, and Christian List. 2013. "Where Do Preferences Come From?" *International Journal of Game Theory* 42(3): 613-637. DOI: 10.1007/s00182-012-0333-y. (Preferences derived from a stable weighing relation over motivationally salient properties; preference change as a change of salience. Quotations in §7.4 follow the authors' accepted manuscript, LSE Research Online.)
Hansson, Sven Ove. 1995. "Changes in Preference." *Theory and Decision* 38(1): 1-28. DOI: 10.1007/BF01083166. (Preference revision, contraction, addition and subtraction under postulates for rational change.)
