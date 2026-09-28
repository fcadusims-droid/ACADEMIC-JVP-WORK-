# The Cybernetic Limits of Conversion: Why Models That Direct Value Change Cannot Tell Conversion from Manipulation

João Vitor Perazzolo

27 September 2026

---

## Abstract

Formal models of value change, including decision theories for changing selves, formal theories of preference change, value-learning agents and schemes for corrigible artificial agents, are increasingly used to direct and evaluate value change, not only to describe it. This paper argues that none of them can evaluate conversion, the undergone reordering of an agent's fundamental values, as distinct from manipulation. Directing change requires a reference standard, and the models on offer, with one exception, take it from the agent's attitudes in one of three ways: from her values before the change, from her values after it, or from a fixed higher-order rule over both. Each standpoint fails in a characteristic way. The ex ante standpoint registers any unanchored change as no improvement, and typically as a loss. The ex post standpoint ratifies whatever change an intervention produces. The higher-order standpoint cannot be revised by the change it evaluates, and when its weights track psychological connectedness it discounts large value change whatever its source. The three share a root: they are attitude-based, and conversion and manipulation can share an attitudinal profile. An attitude-independent standard escapes this argument, but only a condition on the history of the change also excludes benevolent manipulation. The claim is tested against Callard, Paul, Pettigrew, Bykvist, Dietrich and List, Hansson, Bradley and work on value learning and preference influence in artificial intelligence. The exception, the one existing history-sensitive formal proposal, is shown to penalize conversion along with manipulation.

**Keywords:** value change; conversion; manipulation; transformative experience; preference change; personal autonomy

---

## 1. Introduction

Some changes of value are undertaken. A person decides to become a parent, trains her palate, or works her way into a vocation, and her values change along the way. Other changes are undergone. A hostile critic of a movement joins it; a bereaved parent finds that what mattered before no longer does; a boy who believes he is doing wrong by helping a runaway slave keeps helping him. This paper is about the second kind, specifically about undergone changes that the agent comes to endorse, which I call *conversion* (§2.2). Its question is what formal models of value change can say about them.

Such models are no longer only descriptive. Decision theorists ask how an agent should choose when her choices will change what she values (Bykvist 2006; Paul 2014; Pettigrew 2019). Designers of artificial agents ask how a system should act when its actions change the preferences of the people it serves (Carroll et al. 2022, 2024), and how a system can be built to accept changes to its own objectives (Soares et al. 2015; Hadfield-Menell et al. 2016). In each case a model is used to *direct* value change, by selecting actions that bring it about or prevent it, or to *evaluate* it, by ranking some changes above others. To direct or evaluate a change is to hold it to a reference standard. The question of this paper is where that standard comes from, and what a model can then say about conversion.

The thesis is that the models on offer, with one exception discussed in §6.8, take the reference standard from the agent's attitudes, and that attitude-based evaluation cannot distinguish conversion from manipulation. A manipulator can in principle bring about the same sequence of values, rankings and endorsements that a conversion brings about. Any evaluation that depends only on that sequence must then treat the two alike. Yet the distinction between being converted and being brainwashed is one that the concept of conversion, and ordinary practice, both require. A model adequate to conversion must therefore draw on something other than the agent's attitudes: either a standard of value that does not depend on them, or a condition on how the change came about. Only the second also excludes benevolent manipulation (§5.4).

The observation that attitude-based accounts are exposed to manipulation is familiar from the literature on personal autonomy, where it is the standard objection to structural accounts and the motivation for historical ones (Frankfurt 1971; Christman 1991; Mele 1995). The contribution here is to show that the formal models of value change inherit the problem, to say exactly where each one meets it, and to explain why the models' three available standpoints exhaust attitude-based evaluation while failing in different ways.

The three standpoints correspond to the three ways in which the cybernetic tradition directs a system: by its own feedback, by external tracking of a prescribed path, and by optimization of a fixed objective (Wiener 1948; Ashby 1956; Bellman 1957). Evaluating a value change by the agent's prior values is the evaluative counterpart of change generated from within. Evaluating it by the values the change produces is the counterpart of tracking, since a controller that installs a target value structure also installs the standard by which the target is endorsed. Evaluating it by a fixed higher-order rule is the counterpart of optimization. The title of the paper refers to this correspondence. The argument does not depend on it.

Two clarifications of scope. First, the paper makes no claim about whether conversions occur, how they occur, or whether any particular change was one. It concerns what models can evaluate. Second, the thesis is not that directing value change requires a *fixed* standard and conversion changes the standard. That claim is true but definitional: every evaluation uses some standard, and nothing could count against it. The claim defended here is about *where* the standard is anchored. It can fail in identifiable ways, one for each premise of the argument in §5, which §7 states.

Section 2 defines conversion and separates it from refinement, corruption and manipulation. Section 3 says what directing value change requires and distinguishes the standards a model evaluates by from the laws that describe how values move. Section 4 examines the three standpoints. Section 5 states the indiscernibility argument and answers two objections. Section 6 applies the analysis to the models in the literature. Section 7 states what would refute the thesis, and section 8 concludes.

## 2. Conversion, Refinement and Manipulation

### 2.1 Value structures and attitudinal profiles

Let an agent's *value structure* at a time be whatever in her psychology ranks outcomes, options and ways of living for her: her fundamental desires, cares, commitments and the weights among them. Nothing in the argument depends on a particular theory of what value structures are. Where a formal model is in view, the value structure is whatever the model takes to generate the agent's preferences: a utility function, a weighing relation over properties (Dietrich and List 2013), a reward function (Sutton and Barto 2018).

A value change is a change in the value structure between two times, $t_0$ and $t_1$. Call the value structures $V_0$ and $V_1$. The *attitudinal profile* of the change is the sequence of the agent's value structures over the interval, together with every attitude she holds toward them: how $V_0$ ranks the prospect of $V_1$, how $V_1$ ranks the memory of $V_0$, whether she endorses the change when she reflects on it, and so on. The profile includes higher-order attitudes. It also records the agent's standing capacities at each time: whether she deliberates, responds to reasons and answers for her past acts. It excludes facts about the causes of the change, including how those capacities figured in producing it, that are not themselves attitudes or capacities of the agent.

### 2.2 Four marks of conversion

A conversion from $V_0$ to $V_1$ has four marks. The marks are necessary, not sufficient: §2.3 shows that a manipulated change can have all four.

**(F) Fundamental.** The change alters what the agent values non-derivatively, not only her beliefs about how to get what she already values. A change in which an agent learns that a different career would better serve her unchanged ends is not fundamental.

**(U) Unanchored.** $V_0$, applied to the change taken as a prospect, does not rank the post-change state above the pre-change state. The change is not endorsable ex ante by the agent's own prior standards. This excludes the aspirant who works toward a value she already grasps, however defectively (Callard 2018; §6.1).

**(E) Endorsed ex post.** $V_1$ ranks the post-change state above the pre-change state, and the agent, reflecting on the change, endorses it.

**(A) Agency preserved.** After the change the agent is still an agent in the full sense: she deliberates, responds to reasons and answers for what she did under $V_0$. The last clause fixes who the subject of the change is. The converted person still answers for her earlier acts, and that is what distinguishes conversion from the replacement of one person by another. An accountability relation of this kind is formal rather than contentual, which matters here: it can survive a change of every value the person holds.

(U) is the mark that separates conversion from the kinds of value change decision theory already handles well, and it is the mark the literature on transformative choice has in view when it says that some choices cannot be evaluated from the standpoint of the self who makes them (Ullmann-Margalit 2006; Paul 2014). (E) separates conversion from corruption (§2.3), and (A) separates it from breakdown and from the replacement of one person by another. Together, (U) and (E) make conversion a case in which the agent's prior and posterior standards disagree about the change, and the posterior standards are the agent's own.

### 2.3 Refinement, corruption and manipulation

Three neighbouring kinds of change share some or all of these marks.

*Refinement* has (F), (E) and (A) but not (U). The agent's prior standards endorse the change, in the way the aspirant's defective grasp of a value already recommends pursuing it.

*Corruption* has (F), (U) and (A) but not (E). The agent's values change in a way that neither her prior nor, on reflection, her posterior standards endorse.

*Manipulation*, in the sense relevant here, is the case that matters most. Suppose an agent's values are changed by a process that bypasses her capacities for evaluating and controlling her own mental life, as in Mele's (1995) case of an agent whose values are engineered to match those of another person who acquired them in the ordinary way. The result can have all four marks. The change is fundamental. It need not be endorsable by her prior standards. Her new standards endorse it, and she endorses it on reflection, because the manipulation installed the endorsement along with the values. She remains a deliberating agent who answers for her past. What makes the case manipulation is not any of the four marks but the history of the change: the process that produced it.

Most accounts of personal autonomy that take manipulation seriously draw the same conclusion. Structural accounts, which assess an agent's autonomy by the relations among her attitudes at a time, are widely thought to be threatened by such cases, and historical accounts add conditions on how the attitudes came about (Christman 1991; Mele 1995; Fischer and Ravizza 1998). The present paper does not need any particular historical account. It needs only the negative point that the manipulation cases are widely taken to show: the marks (F), (U), (E) and (A), which are properties of the attitudinal profile, do not settle whether a change was manipulation.

The four marks are therefore not sufficient for conversion, and this incompleteness is what the argument of this paper turns on. The ordinary concept of conversion excludes brainwashing: whether the members of new religious movements were converted or brainwashed is a contested empirical question precisely because the two are taken to differ (Barker 1984). The four marks give the attitudinal content of conversion; a full account adds a condition on the process. Section 5 argues that this is exactly what formal models of value change lack.

### 2.4 Is the class of conversions non-empty?

If every real value change were anchored, the paper's subject would be empty and its thesis idle. Callard (2018) makes a strong case that much ordinary value acquisition is anchored, and the paper concedes that case in full (§6.1). But her account is an account of *aspiration*, a form of agency in which the agent works at acquiring a value over time. It therefore does not cover value change that the agent undergoes rather than undertakes, and at least three kinds of undergone change appear to be unanchored.

The first is value change under what happens to one: the reorganization of a parent's values by the death of a child, which she did not aspire to and could not have endorsed in advance. The second is non-deliberative moral change. Arpaly's (2003) reading of Huckleberry Finn describes a boy who helps Jim escape while believing throughout that he is doing wrong, responding to reasons he cannot articulate. He has no proleptic grasp of the value he acts on; his avowed standards condemn it. The third is the conversion of the hostile, the cases James (1902) collected in which a subject actively opposed to a value comes to be governed by it, often abruptly. A modern empirical literature describes sudden transformations of value that people report as having happened to them rather than as something they did (Miller and C'de Baca 2001).

These kinds show that unanchored change occurs. A case of any of them is a conversion only if it also has marks (E) and (A). Many do: James's converts endorse what happened to them and remain agents who answer for their past. Some do not: a bereaved parent may never endorse the change in her values, and Huck's endorsement of what he does is at best ambivalent. Such cases are unanchored change short of conversion, and the argument needs only that some unanchored changes are conversions.

A defender of the anchored view can reply that some prior thread, such as a longing or a misdirected zeal, can always be redescribed as a defective grasp of the value acquired. Where the redescription is true, the case moves to refinement. The paper does not need the redescription to fail in every case, only in some, and the three kinds above make that plausible. The reply also locates the dispute: whether a change was anchored depends on what the agent's prior standards contained, which is a question about the agent and not about the model used to describe her.

## 3. What Directing Value Change Requires

### 3.1 Direction as control

To direct a change is to select among ways of bringing it about, or of preventing it, according to a criterion. The criterion can be explicit, as in a reward function, or implicit, as in a decision rule that selects options by their expected effects on the agent's values. In either case it plays the role that a reference signal plays in control theory: it is what the process is steered toward, and what deviations are measured from (Wiener 1948). To evaluate a change is to rank it against alternatives by such a criterion, whether or not anything then acts on the ranking.

This paper uses "control" in that broad sense, for any selection among trajectories by a criterion. On this usage a decision rule for changing selves is a controller of the agent's own future, and an artificial agent that chooses actions partly for their effects on a user's preferences is a controller of those preferences.

### 3.2 Laws, constraints and standards

The formal models of section 6 contain three different kinds of element, and the argument depends on keeping them apart.

A *law* describes how a value structure changes: an update rule, a dynamical system on a space of value states, a Bayesian or Jeffrey-style kinematics. A law says what will happen, or what would happen under given inputs. It does not rank what happens.

A *constraint* restricts which changes count as rational or admissible. Belief-revision-style postulates for preference change are constraints in this sense (Hansson 1995). A constraint classifies changes as admissible or not; it does not rank the admissible ones.

A *standard* ranks outcomes or trajectories and has a correctness condition: a trajectory can do better or worse by it, and an agent or system can be mistaken about how well a trajectory does. Utility functions, reward functions, weighing relations and aggregation rules over selves are standards when they are used to rank, as they are in the models of section 6.

An element is a standard because of the role it plays, not because of its form. A scalar function over value states is a standard if the model uses it to rank trajectories. It is not a standard merely because it exists.

The distinction matters because a model that contains only laws does not direct or evaluate value change; it describes it, and it can be perfectly adequate to conversion *as description*. Bradley's (2009) generalized conditioning, discussed in §6.6, is an example. A model that contains constraints evaluates change in a thin, classificatory sense, as rational or not, and falls under the thesis in that sense (§6.5). It is the models that direct or evaluate change, and so contain a standard or a constraint, to which the thesis applies.

### 3.3 Why a Lyapunov function is not a standard

One tempting argument blurs this distinction and should be set aside. Suppose an agent revises her values by an autonomous dynamics on a bounded space of value states. By Conley's (1978) fundamental theorem of dynamical systems, every flow on a compact metric space admits a complete Lyapunov function: a scalar function that decreases strictly along trajectories outside the chain-recurrent set and is constant on its components. It is then tempting to say that the revision "optimizes" that function, so that even autonomous value change is directed by a fixed higher-order objective.

The inference fails. A ball rolling downhill has a potential that decreases along its path; it does not value the potential. A Lyapunov function is a law-like invariant of the dynamics, and by Conley's theorem one exists for every such flow. Treating it as a standard would make every dynamical model of value change an optimizer and would make the question of this paper trivial. An autonomous dynamics of values is evaluated by a standard only if something in the model uses a function to rank trajectories: an agent who represents it, or a designer who chose the dynamics because it ranks well.

A related argument about self-revising agents should also be set aside. Poincaré's recurrence theorem (Poincaré 1890) implies that a measure-preserving dynamics on a bounded space returns arbitrarily close to its starting state from almost every initial condition, so that such an agent cannot permanently leave her old values behind. The theorem is correct but settles little here. It holds only for states typical of the invariant measure, which excludes the transients of dissipative dynamics, and the expected return time grows with dimension. By Kac's lemma, in an ergodic measure-preserving system the mean return time of points starting in a set $A$ is $1/\mu(A)$ (Kac 1947). If the invariant measure has a density bounded above, then for a neighbourhood of radius $\varepsilon$ in a $d$-dimensional value space $\mu(A)$ is at most proportional to $\varepsilon^d$, so mean return times grow at least exponentially with $d$ and quickly exceed any timescale over which a person's values are assessed. Recurrence therefore does not show that a high-dimensional self-revising agent cannot undergo a permanent reorganization on any timescale that matters; Appendix A.2 illustrates the scaling. Nor does it bear on evaluation, which is what this paper is about.

## 4. Three Evaluative Standpoints

A model that evaluates a value change by the agent's attitudes must take its standard from some part of the attitudinal profile. There are three options: the attitudes before the change, the attitudes after it, or a fixed rule that combines attitudes from several times or treats them as estimates of some further quantity. The trichotomy is exhaustive for attitude-based standards: a standard either takes the attitudes of a single time as authoritative or it does not, and a standard taken from an intermediate time behaves like one of the first two, depending on which side of the change that time falls. The interest of the classification lies in how each option fails, and the failures differ.

### 4.1 The ex ante standpoint

A model evaluates a change *ex ante* when it ranks trajectories by $V_0$, the values the agent holds when the evaluation is made. This is the default of decision theory: the agent chooses by her present utilities, including her present utilities over futures in which her utilities differ. Its dynamical counterpart is Ashby's (1960) ultrastable system, which changes its parameters whenever an essential variable leaves its viable range and keeps changing them until the variable returns. Such a system changes a great deal, but always in the service of its prior organization. Whatever new behaviour appears was already within its repertoire and is selected by the criterion it had before the disturbance (Ashby 1956).

The ex ante standpoint handles refinement well. By definition the prior standards endorse a refinement, so a model that directs change by $V_0$ can recommend it and can recommend the means to it. Callard's (2018) aspirant, who acts on a defective grasp of a value she is coming to have, is directed by $V_0$ in exactly this sense.

Conversion is another matter. By mark (U), $V_0$ does not rank the post-conversion state above the pre-conversion state. A model that evaluates by $V_0$ therefore ranks conversion as no improvement, and typically as a loss. It ranks corruption the same way, since corruption is also unanchored, and it ranks manipulation the same way when the manipulation is unanchored. The ex ante standpoint thus cannot distinguish conversion from corruption or from manipulation. It can register that all three move the agent away from what she now values, and nothing else. This is the evaluative core of the observation that some choices cannot be evaluated from the standpoint of the person who makes them (Ullmann-Margalit 2006; Paul 2014).

One might reply that an agent can value, at $t_0$, being open to change: she can have a higher-order attitude that favours becoming whoever she will become through certain experiences. Either this attitude makes the particular change endorsable ex ante, in which case the change is anchored and is a refinement at a higher level, or it is a standing rule for evaluating changes, in which case it is the higher-order standpoint of §4.3. A generic openness to change, moreover, endorses manipulation as readily as conversion unless it specifies the processes it is open to, and a specification of processes is a historical condition (§5.4).

### 4.2 The ex post standpoint

A model evaluates a change *ex post* when it ranks trajectories by $V_1$ or by the agent's endorsement after the change. Paul's (2014) example of the choice to become a vampire shows why the standpoint is tempting and why it cannot be trusted: everyone you know who has become a vampire reports that it was the right choice, but that report is produced by the change it evaluates.

The failure of the ex post standpoint is self-ratification. Any process that produces mark (E) passes, and manipulation of the relevant kind produces (E) by installing the endorsement along with the values. The ex post standpoint therefore cannot distinguish conversion from manipulation, and it has a further defect when it is used to direct change rather than only to evaluate it. A system that optimizes the satisfaction of the preferences its users will have has an incentive to change those preferences toward ones that are easier to satisfy. This is the incentive analysed for recommender systems by Carroll et al. (2022) and, in its classical form, the problem of adaptive preferences (Elster 1983). A model that directs change by the ex post standard steers toward whatever values its own interventions can most cheaply make endorsed.

The ex post standpoint is the evaluative counterpart of exogenous tracking control. A controller that prescribes a target value structure and holds the agent to it produces, if it succeeds, an agent who ranks the target above her past. Its success certifies itself.

### 4.3 The higher-order standpoint

A model evaluates a change by a *higher-order* standpoint when it ranks trajectories by a rule that combines the attitudes of the agent at several times, or that refers to some quantity the attitudes are taken to estimate, and holds that rule fixed. Pettigrew's (2019) Aggregate Utility Solution is the most developed example: each self should act on a weighted average of the utilities of all the agent's selves at all times. Bykvist's (2006) proposal, which evaluates each possible life by the attitudes the agent holds while leading it, is an earlier one. In artificial intelligence, value learning directs an agent to maximize a human's reward function, which it does not know and must infer (Hadfield-Menell et al. 2016; Russell 2019).

The higher-order standpoint fails in two ways.

The first is fixity. The rule is not itself revisable by the changes it evaluates. That is what makes it well defined, and it is the evaluative analogue of a requirement of dynamic programming: the Bellman recursion computes the value of a state by backward induction from a single cost structure held fixed over the horizon (Bellman 1957). The more sophisticated control architectures do not escape this; they relocate it. Dual control reshapes the controller's beliefs while serving a fixed cost (Feldbaum 1965). Switched and hybrid systems handle changes of objective only among a family of objectives, and switching conditions, specified in advance (Liberzon 2003). Reward learning, inverse reinforcement learning and meta-learning revise the objective under a fixed higher-order objective. Open-ended search and intrinsic motivation fix a novelty measure or a meta-reward (Lehman and Stanley 2011; Schmidhuber 2010). Fixity matters for conversion when the conversion includes a change in how the agent weighs her own selves. A convert who repudiates her former values plausibly also repudiates the weight her former self deserves in her deliberation. A model that evaluates her change by a fixed aggregation misdescribes her evaluative situation even as it evaluates it.

The second failure is attitude-dependence. If the higher-order rule takes attitudes as its inputs, it is attitude-based, and it treats conversion and an attitudinally identical manipulation alike. There is also a systematic bias. Pettigrew suggests that the weights on selves should reflect psychological connectedness, and among the connections he lists is the sharing of values (as reported in Bykvist's 2021 review). On that proposal the selves whose values differ most from the evaluating self receive the least weight from it, so the aggregate discounts large value change as such, whether it comes from conversion or from manipulation. Value learning shows the same dependence in a different form (§6.7).

The higher-order standpoint could be made history-sensitive by letting the weights on selves, or the credibility of an inferred reward, depend on how the self or the reward came about: less weight for a self produced by manipulation. That would be a good modification, and §5.4 argues that something like it is required. But it is no longer an attitude-based rule.

### 4.4 Exogenous control and the cost to agency

A familiar cybernetic intuition holds that exogenous tracking of a prescribed trajectory destroys the agency of the system tracked: to hold a system on a commanded path, the controller must suppress every degree of freedom along which the system could depart from it. As a general claim about control this is false, and the correction sharpens the present argument.

A controller need not constrain every degree of freedom to hold a specified output on a specified path. The operational-space formulation for redundant robot manipulators tracks a trajectory of the end effector while leaving free the motions that do not affect it, which lie in the null space of the task Jacobian (Khatib 1987). Tracking pays its cost only along the dimensions the target specifies. Appendix A.1 illustrates the point with a two-dimensional system: tracking one coordinate left the variance of the other unchanged when the two were uncoupled and nearly unchanged when they were weakly coupled, while the tracking error was the same as under full-state control.

In value change, the target of a tracking controller is specified in the space of the agent's evaluative attitudes. The cost therefore falls on the agent's capacity to revise those attitudes in response to her own evaluation of reasons. That is her evaluative self-government, the capacity whose bypassing is what makes manipulation manipulation. Her other capacities can be left intact, which is why a manipulated agent can satisfy mark (A): she still deliberates, perceives, plans and answers for her past. The corrected claim is therefore not that exogenous control destroys agency, but that it bypasses exactly the capacity that separates conversion from manipulation, while sparing the capacities that the attitudinal profile records. This is the dynamical form of the point made in §2.3: the marks of conversion do not register the bypassing that makes a change manipulation.

## 5. The Indiscernibility Argument

### 5.1 The argument

Call a model's evaluation of value change *attitude-based* if, for any two value-change trajectories with the same attitudinal profile, the model assigns them the same evaluation: the same rank, the same verdict, or the same classification. The standpoints of section 4 are attitude-based by construction. The argument is then:

1. **(Classification)** Every formal model on offer that directs or evaluates value change, except the one discussed in §6.8, evaluates it in an attitude-based way.
2. **(Possibility)** For any conversion there is a possible manipulation with the same attitudinal profile.
3. **(Adequacy)** A model adequate to conversion must be able to evaluate some conversion differently from some attitudinally identical manipulation.
4. Therefore none of those models is adequate to conversion.

The inference is valid, and trivially so: a function of the attitudinal profile cannot separate trajectories that the profile does not separate. The content of the argument lies in its premises, and each of them can be false. Premise 1 is a claim about particular models, and section 6 argues it case by case. The one model it sets aside is not attitude-based; section 6.8 shows that it fails for a different reason, so the conclusion extends to all the formal models on offer, though not by this argument. Premises 2 and 3 face the two objections that follow.

### 5.2 Objection: the convert grasps reasons that the manipulated agent lacks

It may be said that a genuine convert sees something the manipulated agent does not. The convert comes to value what she values because she has come to grasp a reason for valuing it, while the manipulated agent merely has the attitude. If so, the two differ in attitudinal profile after all, and premise 2 is false.

The objection has two readings. On the first, "grasping a reason" is a psychological state: it seems to the agent that she sees a reason, and she responds accordingly. That state is an attitude, and a manipulator who can install values and endorsements can install it too. Mele's (1995) engineered agent is constructed to have exactly the psychology of an agent who formed her values in the ordinary way, including whatever sense of their rightness that agent has. On this reading premise 2 stands.

On the second reading, grasping a reason is factive: the convert actually sees a reason that is there, as one can know a fact rather than merely believe it. Then the difference between the convert and the manipulated agent lies in whether the reason exists, which is not a fact about the attitudinal profile. On this reading premise 2 is false as stated, but the objection does not rescue attitude-based models. To evaluate the change by whether the agent grasped a real reason, a model needs a standard of what reasons there are that does not depend on the agent's attitudes. The objection does not refute the thesis; it selects one of the two ways out described in §5.4.

### 5.3 Objection: if the attitudes coincide, the difference is idle

It may be said that if a converted agent and a manipulated agent have the same values, the same endorsements and the same capacities going forward, a model has no reason to distinguish them. What matters is how the agent's life goes and what she cares about, and in that respect they are alike.

A reader who accepts this rejects premise 3, and with it the idea that conversion is a distinct kind of change. The position is coherent but revisionary, and there are three reasons not to accept it. The first is that the autonomy literature and ordinary moral practice treat the difference as real: an agent whose values were installed by a process that bypassed her capacities is widely held to lack autonomy with respect to them, even if she endorses them (Christman 1991; Mele 1995), and the dispute over whether converts to new religious movements were brainwashed presupposes that the answer matters (Barker 1984). The second is that research on artificial agents treats the difference as exactly what needs to be captured. Characterizations of manipulation by artificial systems appeal to the incentives, intent, covertness and harm of the influence (Carroll et al. 2023), which are properties of the process and not of the resulting attitudes. The third is practical. A model used to direct value change is a controller, and a controller indifferent between converting and manipulating a person will do whichever is cheaper. A model that cannot distinguish the two is thus a model whose use will select manipulation wherever manipulation is easier.

### 5.4 Two ways out

A model can escape the argument in two ways, which are not exclusive.

**(a) An attitude-independent standard.** The model evaluates $V_1$ by whether it is better than $V_0$, where "better" is fixed by a theory of value that does not depend on the agent's attitudes, such as an objective-list theory of well-being or a realist theory of reasons. On this route there is again a fixed evaluative point, but it is not anchored in the agent. Two costs follow. Decision theory has avoided taking a stand on substantive value by design, and this route gives that up. And an attitude-independent standard does not by itself distinguish conversion from *benevolent* manipulation, in which a manipulator installs values that are in fact better. If benevolent manipulation is still manipulation, as historical accounts of autonomy hold, route (a) is not sufficient.

**(b) A condition on the history of the change.** The model evaluates not only the endpoints and the attitudes but the process that connected them: whether it bypassed the agent's capacities for control over her mental life (Mele 1995), whether she would have resisted it had she attended to it (Christman 1991), whether the mechanism that produced the change was reasons-responsive and her own (Fischer and Ravizza 1998). This route is available to formal models in a way it is not to purely evaluative ones, because the laws that describe value change already represent the process. What they lack is a standard that ranks processes as well as outcomes. Route (b) is necessary if benevolent manipulation is to be excluded, and it is the route the analysis recommends.

The sense in which this is a limit of control can now be stated. The difficulty with using control to direct conversion is not that control requires a fixed reference. Every evaluation does, including route (a). The difficulty is that the references available to the models on offer are anchored in the agent's attitudes, and attitudes do not record the history that separates conversion from manipulation. The one exception (§6.8) uses a historical reference, but conditions on the wrong feature of the history.

## 6. The Models, Case by Case

Premise 1 is a claim about particular models, and it could be false of any of them. This section examines the strongest candidates, including two informal accounts, Callard's and Paul's, on which formal work draws. For each it asks whether the model directs or evaluates value change, which standpoint it evaluates from, and whether that standpoint is attitude-based.

### 6.1 Callard: aspiration as anchored change

Callard (2018) offers the most direct challenge to the idea that value change lies beyond rational direction. The aspirant comes to care about something she does not yet care about by acting on *proleptic* reasons, defective versions of the reasons she expects eventually to grasp. Value acquisition on this account has its own rationality and does not require prior possession of the value acquired.

The account concerns anchored change, and conceding it narrows the present thesis. The aspirant's defective grasp of the value is part of her prior evaluative state, and it recommends the pursuit. Her change therefore lacks mark (U) and is a refinement in the sense of §2.3. The present paper claims nothing about it, and Callard makes a strong case that a large part of ordinary value change is of this kind.

Two further points bear on the argument. First, Callard's account is not a formal model, and it is not purely attitude-based: aspiration is a form of agency, a process in which the aspirant works at acquiring the value, and whether a change was aspiration depends on that process. Her account thus already contains a historical element of the kind §5.4 recommends. Second, and for the same reason, it does not extend to changes the agent undergoes without working at them (§2.4). Where an apparent conversion can be truly redescribed as aspiration, it belongs to her account and not to this one. The dispute is about whether the redescription is always available and true, and that is a dispute about particular agents' prior states.

### 6.2 Paul: an epistemic obstacle and a structural one

Paul (2014) argues that epistemically and personally transformative choices defeat standard decision theory, because the agent cannot know in advance what the transformed outcome is like or how she will then value it. The obstacle she identifies is epistemic: it concerns what the agent can know before the change.

The obstacle identified here survives even if that one is set aside. Grant the agent complete knowledge of her post-change state, including the values she will then have. The ex ante standpoint still ranks an unanchored change as no improvement, by mark (U), and the ex post standpoint still ratifies whatever change occurs. Knowledge of the outcome does not tell the agent which standpoint to evaluate from, and neither standpoint separates conversion from manipulation. The two problems are independent, and the present one concerns Paul's personally transformative class.

Paul's own proposal is that the agent may choose on the basis of the value of *revelation*: of discovering what the new experience and the new self are like. This is a higher-order attitude, and it is attitude-based. It favours a change that reveals something new, and a manipulation that installs novel values reveals as much as a conversion does. As an evaluative standpoint it therefore inherits the indiscernibility of §5.

### 6.3 Pettigrew and Bykvist: aggregation over selves

Pettigrew's (2019) Aggregate Utility Solution, the most developed formal model for choosing when one's values will change, and Bykvist's (2006) earlier account were described in §4.3. Both are higher-order standpoints, and both are attitude-based: their inputs are the utilities or attitudes of the selves, and nothing in them depends on how a self came to have its values.

Section 4.3 identified the consequences: fixity of the aggregation rule, indiscernibility between conversion and manipulation, and, where weights track shared values, a systematic discount on large value change. The last point bears on a question the aggregation framework leaves open. Bykvist (2021) notes that the proposal that weights reflect psychological connectedness is not precise about how the connections are to be measured. The present analysis adds a constraint on any answer: if the weights are to treat conversion differently from manipulation, they must depend on something other than the connections among the selves' attitudes.

Pettigrew can reply that the aggregation rule is a requirement of rationality and not a value, so that conversion, which changes values, is not the kind of thing that could or should revise it. The reply is correct about classification and does not affect the argument. Whatever its status, the rule ranks acts and trajectories, which makes it a standard in the sense of §3.2. The question is only whether its inputs can separate conversion from manipulation, and they cannot.

### 6.4 Dietrich and List: preferences from a weighing relation

Dietrich and List (2013) derive an agent's preferences from a weighing relation over combinations of the properties she finds motivationally salient. Preferences change when the set of salient properties changes, while the weighing relation stays fixed. The model describes a mechanism of preference change and contains a standard, the weighing relation, by which any bundle of properties can be ranked.

If the agent's fundamental values are identified with her weighing relation, as the model's authors suggest when they treat it as the stable feature that characterizes an agent, then the changes the model represents are not fundamental, and conversion as defined in §2.2 lies outside it. A change in the weighing relation itself is not modelled, and the authors leave open how an agent comes to have one. The model is therefore not a counterexample to premise 1. It is the clearest formal instance of a pattern that recurs throughout this section: first-order preferences move while a higher-order structure stays put, and the evaluation of any change is made from that structure.

### 6.5 Hansson: postulates for preference revision

Hansson (1995) models preference change on the pattern of belief revision, with operations of revision, contraction, addition and subtraction of alternatives, each governed by postulates for rational change. The postulates are constraints in the sense of §3.2: they classify a change as rational or not, given the prior preferences and the input, without ranking the admissible outcomes.

The classification is attitude-based. It depends on the relation between the prior preference ordering, the input and the posterior ordering. A change produced by manipulation that satisfies the postulates is, by the model, a rational change, and an otherwise identical change produced by conversion receives the same verdict. Hansson's model is thus an instance of premise 1 among constraint-based models, and its postulates are not a place where conversion and manipulation could be told apart.

### 6.6 Bradley: Becker's thesis and generalized conditioning

Bradley (2009) examines Becker's methodological thesis that all preference change should be explained against fundamental tastes that do not change. He shows that the thesis can almost always be saved by refining the space of fundamental states, and that the refinement can be as ad hoc as postulating a change of fundamental desire. His first model, classical conditioning, changes the agent's information while holding fundamental beliefs and desires fixed; any change it represents is non-fundamental, and so not a conversion. His third model, generalized conditioning, can represent any change in the agent's attitudes, fundamental desires included, and so can represent conversion.

Generalized conditioning is not a counterexample, because it neither directs nor evaluates. It is a kinematics: it relates the attitudes before a change to those after it and says nothing about what produced the change or whether it was good. In the terms of §3.2 it is a law. The case is instructive in the other direction. It shows that representing conversion is not the problem. The problem arises when a model is asked to evaluate what it represents.

### 6.7 Value learning and corrigibility

A value-learning agent maximizes a human's reward function, which it does not know and must infer from the human's behaviour (Hadfield-Menell et al. 2016; Russell 2019). The reference is fixed by construction, and a change in the human's values appears either as a better estimate of the same reward, which is not a change of fundamental value at all, or as a change in the target. For the second case the framework's only resource is the reward the human will have after the change, the ex post standpoint.

The corrigibility problem is the problem of building an agent that accepts modification of its objectives without resisting it (Soares et al. 2015). Two routes are familiar. Building acceptance of modification into the agent's objective makes acceptance a higher-order standard. Overriding the agent from outside is exogenous control. The analysis of section 5 adds a prediction about any notion of corrigibility defined by the attitudes of the overseer, such as her current requests: it cannot distinguish a legitimate correction from one the agent brought about by manipulating the overseer's attitudes. An agent that leads its overseer to request exactly the modification it prefers satisfies a purely attitudinal corrigibility condition.

### 6.8 Influence-aware alignment: the history-sensitive exception

One line of work does not use a purely attitude-based standard. Carroll et al. (2022) observe that recommender systems trained by long-horizon optimization have incentives to shift their users' preferences, and propose to judge a shift by comparing it with the shift the user's preferences would have undergone without the system: an estimate of the "natural" preference dynamics. This is a historical condition of route (b). It asks whether the change would have happened without a particular influence, which is a fact about the process and not about the resulting attitudes. It is the model that premise 1 sets aside, and the most important case in this section.

The condition succeeds against manipulation and fails for conversion, for a reason the cases of §2.4 illustrate. Undergone value change is typically externally occasioned: by a bereavement, an encounter, a friendship, a text. Applied to any influencer, a benchmark defined by what the agent's values would have done without that influencer's action treats every change it occasions as induced, so it penalizes a conversion occasioned by a person as it penalizes a manipulation performed by one. The counterfactual benchmark tracks the source of the change, whereas what separates conversion from manipulation is its manner: whether the influence engaged the agent's capacities or bypassed them.

Carroll et al. (2024) formalize eight notions of alignment for agents whose rewards change and can be influenced, and find that each either permits undesirable influence on the rewards or is overly risk-averse. The present analysis explains why this pattern should be expected, to the extent that the notions fall into two kinds. Notions that evaluate by the rewards a person holds at some time are attitude-based, and when they evaluate by later rewards they inherit the self-ratification of §4.2. Notions that evaluate against a benchmark of uninfluenced change are history-sensitive in the wrong way and penalize legitimate externally occasioned change. A notion that avoided both would need a condition on the manner of influence, not on its presence.

### 6.9 Self-modifying agents described dynamically

Finally, a family of models describes agents that revise their own preferences by an autonomous dynamics on a space of value states. These models contain laws and not standards (§3.2), so they describe value change without directing or evaluating it, and they fall outside premise 1. The two conclusions sometimes drawn from them, that a Lyapunov function makes the agent an optimizer and that recurrence rules out permanent reorganization, were set aside in §3.3.

## 7. What Would Count Against the Thesis

Because the indiscernibility argument is valid, the thesis can fail only through its premises. Each failure is identifiable.

The thesis would fail through premise 1 if a formal model that directs or evaluates value change used an attitude-independent standard or a historical condition and thereby ranked some conversion above an attitudinally identical manipulation. Such a model would refute the thesis as stated and confirm its diagnosis, since it would take one of the two ways out of §5.4. The influence-aware alignment of §6.8 is the closest existing case. It is history-sensitive, but it does not separate conversion from manipulation, because its historical condition concerns the presence of external influence rather than its manner.

Premise 2 would fail if some mark of conversion could not be produced by any process that bypasses the agent's capacities. The factive reading of §5.2 is the most promising way to argue this, and it leads to route (a).

Premise 3 would fail if the difference between conversion and manipulation were normatively idle. Section 5.3 gave reasons to reject this, but a reader who accepts it rejects conversion as a distinct kind of change, not merely this paper.

Finally, the thesis would be idle, though not false, if every value change were anchored, so that every apparent conversion could be truly redescribed as refinement. Section 2.4 argued that at least three kinds of undergone change resist the redescription.

## 8. Conclusion

Formal models of value change can describe conversion. Bradley's generalized conditioning represents any change in an agent's attitudes, and dynamical models of self-revising agents represent changes that no prior standard anticipated. The difficulty begins when such models are used to direct or evaluate change. A directing model needs a reference, and the models on offer, with one exception, take it from the agent's attitudes: from her values before the change, from her values after it, or from a fixed rule over both. The first registers every unanchored change as no improvement, the second ratifies whatever change is produced, and the third cannot be revised by what it evaluates and, when it weighs selves by shared values, discounts large change as such. Beneath these three failures lies one: the attitudinal profile of a conversion can be produced by manipulation, and a standard anchored in attitudes cannot tell the two apart.

What an adequate model needs is a condition on the history of the change, one that distinguishes influence that engages an agent's capacities from influence that bypasses them. The one existing history-sensitive formal proposal conditions on whether a change was externally influenced at all, and so penalizes conversion together with manipulation. Stating a condition on the manner of influence precisely enough to be built into a formal model is the open problem this analysis leaves. It is a problem shared by the philosophy of personal autonomy, which has long had historical accounts but few formal ones, and by the design of artificial agents, which has formal models but, so far, not the right history.

---

## Appendix A. Two Illustrative Computations

Neither computation supports the argument of the paper, which is conceptual. Each illustrates a technical claim made in passing. The predictions were committed to the accompanying repository before the computations were run, and code and results were committed afterwards; no external registry was used.

### A.1 Tracking constrains only the dimensions the target specifies (§4.4)

**Model.** A two-dimensional linear stochastic system with a target coordinate $x$ and a second coordinate $y$ coupled with strength $c$:

$$dx = (-x + c\,y + u)\,dt + \sigma\,dW_x, \qquad dy = (-y + c\,x + v)\,dt + \sigma\,dW_y .$$

A reference $r(t)$, which steps from 0 to 1 halfway through the run (a new target), is tracked with gain $k \in \{0, 0.5, 1, 2, 5, 10, 20, 50\}$, for $c \in \{0, 0.3\}$, $\sigma = 1$, ten seeds. Under *output tracking*, $u = -k(x - r)$ and $v = 0$. Under *full-state tracking*, $u = -k(x - r)$ and $v = -k\,y$.

**Pre-specified prediction.** Variances are measured after the step, once transients have decayed. Under full-state tracking the variance of $y$ falls monotonically and is below 5% of $\sigma^2/2$ at $k = 50$. Under output tracking it stays within 10% of $\sigma^2/2$ at every $k$ when $c = 0$, and is at least 90% of $\sigma^2/2$ at $k = 50$ when $c = 0.3$.

**Result.** The prediction was met. Under full-state tracking the variance of $y$ fell monotonically with $k$ and reached 2.0% of $\sigma^2/2$ at $k = 50$ for both values of $c$. Under output tracking it was 98.6% of $\sigma^2/2$ at every $k$ when $c = 0$; when $c = 0.3$ it fell from 107.8% at $k = 0$ to 98.8% at $k = 50$. The tracking error, the variance of $x - r$, was the same under both controllers (0.0101 at $k = 50$). Values are means over ten seeds, with variances computed over $t \in [1200, 2000]$.

### A.2 Recurrence times grow exponentially with dimension (§3.3)

**Model.** An ergodic rotation of the $d$-dimensional torus, $\theta \mapsto \theta + \alpha \pmod 1$, with $\alpha_i$ the fractional parts of the square roots of the first five primes (rationally independent together with 1), for $d = 1, \dots, 5$. The return set $A$ is a box of side $\varepsilon = 0.1$ centred at $(0.5, \dots, 0.5)$, so $\mu(A) = 10^{-d}$; 200 initial points are drawn uniformly in $A$.

**Pre-specified prediction.** The mean return time, averaged over initial points in the return set, matches Kac's value $1/\mu(A) = 10^{d}$ within 15%, and the slope of $\log_{10}$ of the mean return time against $d$ lies between 0.9 and 1.1.

**Result.** The prediction was met. For $d = 1, \dots, 5$ the mean return time divided by $10^{d}$ was 1.022, 0.884, 0.965, 1.036 and 1.011, and the slope of $\log_{10}$ of the mean against $d$ was 1.006. The return times were widely dispersed (for $d = 5$, mean 101,052 and standard deviation 100,061 steps), and none of the 1,000 starts reached the cap of $10^{7}$ steps.

---

## Statements and Declarations

**Use of generative AI.** This manuscript was drafted by Claude (Anthropic), a large language model, on 27 September 2026, from the author's earlier drafts, notes and experimental repository and according to the author's decisions about thesis and scope. The author reviewed each argument, revised the text, and takes full responsibility for the content. [AUTHOR TO CONFIRM OR AMEND BEFORE SUBMISSION.]

**Competing interests.** The author declares no competing interests.

**Funding.** No funding was received for this work.

**Data and code availability.** Code for the computations in Appendix A is available in the author's public repository. [LINK AND COMMIT HASH TO BE ADDED; REMOVE FROM THE ANONYMIZED MANUSCRIPT.]

---

## References

Arpaly, N. (2003). *Unprincipled virtue: An inquiry into moral agency*. Oxford University Press.

Ashby, W. R. (1956). *An introduction to cybernetics*. Chapman and Hall.

Ashby, W. R. (1960). *Design for a brain: The origin of adaptive behaviour* (2nd ed.). Chapman and Hall.

Barker, E. (1984). *The making of a Moonie: Choice or brainwashing?* Blackwell.

Bellman, R. (1957). *Dynamic programming*. Princeton University Press.

Bradley, R. (2009). Becker's thesis and three models of preference change. *Politics, Philosophy & Economics, 8*(2), 223–242. https://doi.org/10.1177/1470594X09102238

Bykvist, K. (2006). Prudence for changing selves. *Utilitas, 18*(3), 264–283. https://doi.org/10.1017/S0953820806002032

Bykvist, K. (2021). [Review of the book *Choosing for changing selves*, by R. Pettigrew]. *Mind, 130*(520), 1327–1336. https://doi.org/10.1093/mind/fzaa094

Callard, A. (2018). *Aspiration: The agency of becoming*. Oxford University Press.

Carroll, M., Chan, A., Ashton, H., & Krueger, D. (2023). Characterizing manipulation from AI systems. In *Proceedings of the 3rd ACM Conference on Equity and Access in Algorithms, Mechanisms, and Optimization (EAAMO '23)*. https://doi.org/10.1145/3617694.3623226

Carroll, M., Dragan, A., Russell, S., & Hadfield-Menell, D. (2022). Estimating and penalizing induced preference shifts in recommender systems. In *Proceedings of the 39th International Conference on Machine Learning (ICML 2022)*. arXiv:2204.11966

Carroll, M., Foote, D., Siththaranjan, A., Russell, S., & Dragan, A. (2024). AI alignment with changing and influenceable reward functions. In *Proceedings of the 41st International Conference on Machine Learning (ICML 2024)*. arXiv:2405.17713

Christman, J. (1991). Autonomy and personal history. *Canadian Journal of Philosophy, 21*(1), 1–24.

Conley, C. (1978). *Isolated invariant sets and the Morse index* (CBMS Regional Conference Series in Mathematics, No. 38). American Mathematical Society.

Dietrich, F., & List, C. (2013). Where do preferences come from? *International Journal of Game Theory, 42*(3), 613–637. https://doi.org/10.1007/s00182-012-0333-y

Elster, J. (1983). *Sour grapes: Studies in the subversion of rationality*. Cambridge University Press.

Feldbaum, A. A. (1965). *Optimal control systems*. Academic Press.

Fischer, J. M., & Ravizza, M. (1998). *Responsibility and control: A theory of moral responsibility*. Cambridge University Press.

Frankfurt, H. G. (1971). Freedom of the will and the concept of a person. *The Journal of Philosophy, 68*(1), 5–20.

Hadfield-Menell, D., Russell, S. J., Abbeel, P., & Dragan, A. (2016). Cooperative inverse reinforcement learning. In *Advances in Neural Information Processing Systems 29*.

Hansson, S. O. (1995). Changes in preference. *Theory and Decision, 38*(1), 1–28. https://doi.org/10.1007/BF01083166

James, W. (1902). *The varieties of religious experience: A study in human nature*. Longmans, Green.

Kac, M. (1947). On the notion of recurrence in discrete stochastic processes. *Bulletin of the American Mathematical Society, 53*(10), 1002–1010.

Khatib, O. (1987). A unified approach for motion and force control of robot manipulators: The operational space formulation. *IEEE Journal on Robotics and Automation, 3*(1), 43–53. https://doi.org/10.1109/JRA.1987.1087068

Lehman, J., & Stanley, K. O. (2011). Abandoning objectives: Evolution through the search for novelty alone. *Evolutionary Computation, 19*(2), 189–223. https://doi.org/10.1162/EVCO_a_00025

Liberzon, D. (2003). *Switching in systems and control*. Birkhäuser.

Mele, A. R. (1995). *Autonomous agents: From self-control to autonomy*. Oxford University Press.

Miller, W. R., & C'de Baca, J. (2001). *Quantum change: When epiphanies and sudden insights transform ordinary lives*. Guilford Press.

Paul, L. A. (2014). *Transformative experience*. Oxford University Press.

Pettigrew, R. (2019). *Choosing for changing selves*. Oxford University Press.

Poincaré, H. (1890). Sur le problème des trois corps et les équations de la dynamique. *Acta Mathematica, 13*, 1–270.

Russell, S. (2019). *Human compatible: Artificial intelligence and the problem of control*. Viking.

Schmidhuber, J. (2010). Formal theory of creativity, fun, and intrinsic motivation (1990–2010). *IEEE Transactions on Autonomous Mental Development, 2*(3), 230–247.

Soares, N., Fallenstein, B., Yudkowsky, E., & Armstrong, S. (2015). Corrigibility. In *AAAI Workshop on AI and Ethics* (pp. 74–82).

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press.

Ullmann-Margalit, E. (2006). Big decisions: Opting, converting, drifting. *Royal Institute of Philosophy Supplement, 58*, 157–172. https://doi.org/10.1017/S1358246100009358

Wiener, N. (1948). *Cybernetics: Or control and communication in the animal and the machine*. Technology Press; John Wiley & Sons.
