# Reading the result (written after the run, 28 September 2026)

All nine pre-registered predictions were met (`experiments/_results/model_indiscernibility/result.json`).
What that does and does not show:

- **P1 and P2 hold by construction.** A replica manipulation that sets values, endorsements and
  capacities to a conversion's trajectory has the same profile, and a function of the profile gives
  the same output on both. The run confirms that the nine implementations read only the profile; the
  negative control (P0) shows the harness would have detected an implementation that read the history.
  Whether each implementation is faithful to the published model is not tested here; that is the
  argument of Paper 1 §6.
- **P4 is less independent than the pre-registration claimed.** The pre-registration listed P4 among
  the predictions that could fail. After the run it is clear that, in this agent model, the equality of
  the penalties for the occasioned conversion (S2) and its replica manipulation (S4) also follows from
  the construction: both have the same endpoint, and removing the external source leaves both at the
  prior values. What the run does show is the §6.8 point in runnable form: the counterfactual benchmark
  penalizes S2, a conversion whose only external input was reasons (median penalty 1.631), exactly as
  it penalizes a manipulation, and does not penalize S1, a conversion with no external source. Its
  verdict tracks the presence of an external source, not the manner of the influence.
- **P7 is the one result that depends on a modelling choice.** With connectedness weights that decay
  with distance in value space (τ = 0.5), the Pettigrew aggregate falls with the size of the change
  (Spearman −0.850), identically for conversions and manipulations. The size of the correlation depends
  on τ and on the weight form, which were fixed in advance but not varied.
- **P5 and P6** show the two ways out of §5.4 behaving as the paper says: a condition on the target of
  the influence separates every conversion from every manipulation, benevolent ones included; an
  attitude-independent standard scores a conversion and a benevolent manipulation alike.

This is a demonstration about models, in a toy agent. It is not evidence about real agents, and it does
not bear on premise 3.
