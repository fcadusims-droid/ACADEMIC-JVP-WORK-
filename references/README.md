# Citation audit

Every reference in the three papers was checked one by one: 77 in Paper 1, 43 in Paper 2 and
24 in Paper 3. The check asks two questions: does the work exist, and do the paper's details
for it match the source? The details compared are authors, title, year, venue, volume and
pages. The papers' reference lists were corrected where they did not match.

## How each reference was checked

1. **Automated first pass** (`verify.py`). Each reference is sent to one primary index:
   - journal articles and chapters go to Crossref (DOI, title, authors, year, journal, volume,
     pages);
   - preprints go to the arXiv abstract page;
   - books go to Open Library (title, author, publisher, edition years).

   The script compares each field and marks the entry MATCH, PARTIAL or NOMATCH. It never marks
   anything verified on its own. Output: `auto_paperN.json`.
2. **Manual review.**
   - Every automated MATCH was compared field by field with the paper's reference.
   - Every PARTIAL or NOMATCH was looked up by hand in the publisher's or proceedings' own
     record, or in a library catalogue. Examples: the NeurIPS proceedings, RePEc,
     Project Euclid, the university-press pages.
   - Books were checked for the edition and publisher the paper names, not just the title.
   - Direct quotations attributed to a cited author were checked against the source text.
   - Annotations that make a specific claim about a recent paper were checked against its
     abstract.
3. **Final record** (`build_records.py`). The script writes `paperN.json` from the two steps
   above. For each reference, the record holds:
   - the citation as it now stands in the paper;
   - a link to the work;
   - the index it was checked against;
   - any correction made.

   The build fails if an automated non-match has no recorded manual review.

`site/check_claims.py` (run in CI) fails if a paper's reference list and its `paperN.json`
disagree. So a citation cannot be added or edited without being checked again.

## Result

| Paper | References | Verified as cited | Corrected |
|---|---|---|---|
| 1 | 77 | 73 | 4 |
| 2 | 43 | 42 | 1 |
| 3 | 24 | 24 | 0 |

**No cited work was found to be fabricated.** The five corrections:

- **Paper 1, Callard 2018 (misattributed quotation).** §7.8.1 put "is not a matter of
  decision-making at all" in quotation marks as Callard's. The phrase is from L. A. Paul's
  endorsement of the book on the publisher's page, not from Callard's text. The sentence now
  paraphrases Callard's position, without quotation marks.
- **Paper 1, Calvin 1960.** The publisher was given as Westminster John Knox Press, a later
  name. The 1960 McNeill/Battles edition was published by Westminster Press (Library of
  Christian Classics 20–21).
- **Paper 1, Wiener 1948.** The publisher was given as MIT Press, a name the press took only in
  1962. The 1948 edition was published by Technology Press and John Wiley & Sons, and by
  Hermann in Paris.
- **Paper 1, Nayebi 2025.** Added the venue that arXiv records: to appear in the AAAI 2026
  Machine Ethics Workshop proceedings.
- **Paper 2, Cao, Pollack and Wang 2022.** The title was an abbreviation, "Hyper-Invariant
  MERA: …". It now gives the published title.

## What this does and does not establish

A verified citation means that the work exists with the details given. For quotations and for
the specific claims in annotations, it also means that what the paper attributes to the work
was found in it.

It does **not** mean that every use the papers make of every cited work was checked against
that work's argument. That is a reading task, and it is not complete. Summaries of long books,
such as "Callard is best read as …", remain the author's interpretation and are open to
dispute.
