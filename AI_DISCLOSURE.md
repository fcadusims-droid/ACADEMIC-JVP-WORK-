# AI assistance disclosure — read this before relying on anything here

**All of the research in this repository and on its website — the three papers, the
experiment code, the analyses, the formal (Lean) development, the verdicts, and the website
itself — is the work of João Vitor Perazzolo and is being developed with substantial
assistance from Claude, a generative AI model made by Anthropic.**

The author asks every reader to treat that fact as a reason for caution: **no statement,
number, proof or verdict here should be trusted at 100% simply because it is written down.**
Check it yourself.

## What the AI assistance covers

Claude has been used, under the author's direction, to:

- draft and revise the text of the papers and of the documentation;
- design, write and run the experiment code, and write the pre-registrations;
- analyse the results and write the verdicts;
- write the Lean formalization and the automated checks (the numeric-claims, qualifications
  and coverage gates);
- review the work, including its own earlier output.

The author directs the work and is responsible for it. The AI assistance is disclosed here,
not offered as a source of authority.

## Why this matters

Generative AI produces text and code that read as fluent and confident whether or not they are
correct. It can introduce subtle programming bugs, mis-specified statistical tests, overstated
conclusions, citations that do not say what is claimed, and formal statements that are stronger
than the theorems they are named after. These errors are easy to miss precisely because the
surrounding text looks careful.

This is not hypothetical. Errors of exactly this kind have already been found in this
repository — some by the author, some by external reviewers, some by the checks themselves —
and are recorded rather than hidden in [`METHODOLOGY.md`](https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-/blob/main/METHODOLOGY.md). Among them:

- the Lean formalization of Paper 1's central theorem rested on two axioms that were **false as
  stated** (pointwise versions of Poincaré recurrence and of Conley's theorem), and it was
  presented for a long time as mechanical verification;
- a statistical test used a permutation null that **ignored the autocorrelation** of its data,
  making a p-value look far stronger than it was;
- every localization experiment placed the true transition at the **centre of its analysis
  window**, so a detector that simply guessed the middle would have scored perfectly, and a
  conclusion in a paper abstract rested on the inflated numbers;
- the one positive empirical result left in a paper — that a geometric measure tracked sleep
  stages better than simpler measures — turned out to be driven by an **eye-movement (EOG)
  channel** included in the data, and rested on 4 people counted as 7;
- a paper sentence claimed an experiment had **"confirmed directly"** a mechanism that no
  experiment in the repository ever tested;
- a phrase was put in **quotation marks as an author's own words** when it came from someone
  else's endorsement of her book (found by a one-by-one audit of all 144 citations, which found
  no fabricated reference but corrected five);
- the work was described as **ready for submission** when it was not;
- a local network fault in the AI's own sandbox was misreported as an outage of a public
  data server.

Each of these was caught and corrected. **Others may remain.** The safeguards used here —
pre-registration before each run, verdicts against thresholds fixed in advance, self-tests,
automated gates in continuous integration — reduce errors but do not eliminate them, and many
of those safeguards were themselves written with the same AI assistance, so they can share its
blind spots.

## The author's request to readers

Please do not depend only on what is said here. Instead:

1. **Re-run the experiments on your own computer.** Every experiment has a
   `PRE-REGISTRATION.md` (what was to be tested and how it would be judged), a `run.py`, and a
   committed `result.json`. Clone the repository, install it, download the public datasets, run
   the experiments, and check whether your numbers match the committed ones. The
   [reproduction page](https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-/blob/main/site/content/reproduce.md) gives the commands.
2. **Read the code, not just the verdicts.** Check that each test measures what its
   pre-registration says it measures, and that its null hypothesis is appropriate for the data.
3. **Check the mathematics and the formal development yourself.** Compile the Lean files, read
   their axioms, and ask whether each axiom is actually a true statement of the theorem it is
   named after.
4. **Check every citation against its source.**
5. **Report anything that does not match** by opening an issue on the
   [GitHub repository](https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-/issues). A failed
   reproduction is a useful result, and it will be recorded.

## Status

This is **work in progress**. None of the three papers is ready for submission, and any
result, framing or conclusion here may still change. See [`OPEN_ISSUES.md`](https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-/blob/main/OPEN_ISSUES.md) for
what is currently known to be open.
