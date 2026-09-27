Three interlinked papers and an in-silico validation suite that tests their formal
and statistical claims. The papers argue a negative thesis about control theory, a
conditional protocol for testing it in biology, and an independent geometric method
for demarcating state transitions in single time series. The suite exists to find
out which of their claims survive contact with a computer.

Everything on this site is generated from the repository itself. The papers are
rendered from their source; every experiment page is built from the pre-registration
written *before* the run and the `result.json` committed *after* it. When the
repository changes, this site rebuilds.

## The three papers

The papers were rewritten on 27 September 2026, and in their current versions they are
logically independent. Paper 1 is a philosophical argument: formal models used to direct or
evaluate value change take their standard from the agent's attitudes, and so cannot tell
conversion from manipulation. Paper 2 says what data a test of a physiological version of the
persistence question would need, and reports that the one public corpus with the right contrast
failed the first pre-specified step. Paper 3 is the validation record of one EEG method: five
traps that made it look validated, and the controls that overturned it. Each paper's remaining
analyses are specified in its text before they are run; their results are marked as pending.

The earlier versions are kept, marked as superseded, in `archive/papers_2026-09-26_superseded/`.

## What the experiment suite is for

Every computational experiment is pre-registered. Each has a
`PRE-REGISTRATION.md` fixing the question, the method, the thresholds and a stopping
rule *before* the run; a machine-readable `result.json` committed after; and a
verdict issued strictly against the pre-registered criterion. Bands are fixed in
advance so that a middling result cannot be narrated upward.

The scope of what this establishes is narrow and worth stating plainly. Synthetic
results are about *instruments*, not about biology. Single-corpus results are about
that corpus. The logical results — Class G's satisfiability, for instance — say
nothing about whether anything instantiates the profile. The discipline guards
against one specific failure mode, running until something works and reporting only
that, and against nothing else.

What makes the protocol more than decoration is the list of occasions on which it
cost something: a pre-registered halt that stopped Paper 2's positive arm dead, a
detector fix that made the paper's own negative *stronger*, a headline figure
corrected downward from ≈12× to ≈3.3× and then to ≈1.3×, a rescue arm labelled post-hoc rather than
swapped in as though it had been the plan, and a process lapse recorded rather than
back-dated. Those are set out in full on the [methodology](methodology.html) page.
