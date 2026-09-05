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

The trilogy is deliberately asymmetric in what it claims. Paper 1 is a negative
result and its argument is transcendental — it does not propose a mechanism, it
argues that a dominant family of mechanisms cannot state the question. Paper 2 is
conditional throughout and its secure contribution is *eliminative*: it says what
would have to be measurable, and reports a pre-registered negative on whether it
presently can be. Paper 3 is logically independent of both and stands or falls as a
time-series method.

That asymmetry matters for reading them. A reader who accepts Paper 3 incurs no
commitment to Paper 1; a reader who rejects Paper 2's empirical arm leaves Paper 1
untouched. The dependency runs one way — Paper 2 borrows Paper 1's Class G and the
consistency contract *I* — and no result flows back.

## What the experiment suite is for

Thirty-nine pre-registered computational experiments. Each has a
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
corrected downward from ≈12× to ≈3.3×, a rescue arm labelled post-hoc rather than
swapped in as though it had been the plan, and a process lapse recorded rather than
back-dated. Those are set out in full on the [methodology](methodology.html) page.

## Reading paths

If you want the argument, read the paper summaries and then the papers themselves —
each is available as navigable HTML with a section index, as a PDF you can read in
the browser, and as a PDF you can download.

If you want the evidence, go to the [experiments](experiments/index.html): every run
is there with its pre-registration, its verdict, its figures, and its raw JSON.

If you want to check the work, the [reproduction](reproduce.html) page gives the
commands. Results, code and pre-registrations are committed; only the datasets are
not, and they are all public.
