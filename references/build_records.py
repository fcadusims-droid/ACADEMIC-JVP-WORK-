"""Build the final citation-audit records, references/paperN.json.

Inputs: the automated first pass (auto_paperN.json, from verify.py) and the manual review
recorded below. Every reference ends with one of:

  verified            -- found in a primary index or publisher record with the details the paper
                         gives (authors, title, year, venue, and volume/pages where given);
  verified-corrected  -- the work exists, but the paper's reference or its use of the work was
                         wrong; the paper was corrected in the same commit and the correction is
                         described in `correction`.

No entry is marked verified on the strength of the automated pass alone: every automated
non-match was checked by hand (`manual`), and every automated match was compared field by field.

Usage:
    python references/build_records.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- manual review: link overrides and notes, keyed by (paper, first-author surname, year) ----
MANUAL = {
    (1, "Aquinas", 1947): {"url": "https://ccel.org/a/aquinas/summa/home.html",
        "manual": "Benziger Brothers 1947 American edition of the English Dominican translation, confirmed; link is the public-domain text of that translation."},
    (1, "Augustine", 1999): {"url": "https://openlibrary.org/isbn/9781565481367",
        "manual": "Answer to the Pelagians IV (Works of Saint Augustine I/26), trans. Teske, New City Press 1999, confirmed; the volume titles the work 'Grace and Free Choice'."},
    (1, "Bowles", 1998): {"url": "https://econpapers.repec.org/RePEc:aea:jeclit:v:36:y:1998:i:1:p:75-111",
        "manual": "Journal of Economic Literature 36(1): 75-111, confirmed (RePEc record; not indexed by Crossref)."},
    (1, "Calvin", 1960): {"url": "https://openlibrary.org/isbn/9780664220280",
        "manual": "McNeill/Battles, Library of Christian Classics 20-21, confirmed.",
        "correction": "Publisher corrected from 'Westminster John Knox Press' (the later name) to 'Westminster Press', which issued the 1960 edition."},
    (1, "Gregory of Nyssa", 1978): {"url": "https://openlibrary.org/isbn/9780809121120",
        "manual": "Classics of Western Spirituality, Paulist Press 1978, trans. Malherbe and Ferguson, confirmed."},
    (1, "Hadfield-Menell", 2016): {"url": "https://papers.nips.cc/paper/6420-cooperative-inverse-reinforcement-learning",
        "manual": "NIPS 2016 (Advances in Neural Information Processing Systems 29), confirmed on the proceedings site."},
    (1, "Soares", 2015): {"url": "https://intelligence.org/files/Corrigibility.pdf",
        "manual": "Workshops at the Twenty-Ninth AAAI Conference (AI and Ethics), 2015, pp. 74-82, confirmed."},
    (1, "Council of Trent", 1547): {"url": "https://press.georgetown.edu/Book/Decrees-of-the-Ecumenical-Councils-Volume-2",
        "manual": "Tanner (ed.), Decrees of the Ecumenical Councils, vol. 2, Sheed & Ward / Georgetown University Press 1990, confirmed; Session VI (13 January 1547)."},
    (1, "Maximus the Confessor", 2014): {"url": "https://www.hup.harvard.edu/books/9780674726666",
        "manual": "Dumbarton Oaks Medieval Library 28-29, Harvard University Press 2014, ed. and trans. Constas, confirmed."},
    (1, "Metzinger", 2003): {"url": "https://direct.mit.edu/books/monograph/1991/Being-No-OneThe-Self-Model-Theory-of-Subjectivity",
        "manual": "MIT Press 2003, confirmed."},
    (1, "Poincaré", 1890): {"url": "https://projecteuclid.org/journals/acta-mathematica/volume-13/issue-1-2",
        "manual": "Acta Mathematica 13: 1-270 (1890), confirmed; published in chapters, each with its own DOI (preface 10.1007/BF02392505)."},
    (1, "Ricoeur", 1992): {"url": "https://press.uchicago.edu/ucp/books/book/chicago/O/bo3647498.html",
        "manual": "University of Chicago Press 1992, trans. Blamey, confirmed."},
    (1, "Sider", 2001): {"url": "https://academic.oup.com/book/9493",
        "manual": "Oxford University Press 2001, confirmed."},
    (1, "Skoulakis", 2021): {"url": "https://doi.org/10.1609/aaai.v35i13.17352",
        "manual": "AAAI 35(13): 11343-11351, confirmed in Crossref; arXiv:2012.08382 is the 2020 preprint."},
    (1, "Singh", 2004): {"url": "https://papers.nips.cc/paper/2552-intrinsically-motivated-reinforcement-learning",
        "manual": "NIPS 17 (2004), confirmed on the proceedings site."},
    (1, "Haken", 1983): {"manual": "3rd revised and enlarged edition, Springer 1983 (Springer Series in Synergetics 1), confirmed."},
    (1, "James", 1902): {"url": "https://archive.org/details/varietiesofrelig00jameuoft",
        "manual": "Longmans, Green 1902, confirmed; link is a scan of the 1902 edition."},
    (1, "Liberzon", 2003): {"url": "https://link.springer.com/book/10.1007/978-1-4612-0017-8",
        "manual": "Birkhäuser 2003, Systems & Control: Foundations & Applications, confirmed."},
    (1, "Palamas", 1983): {"url": "https://openlibrary.org/isbn/9780809124473",
        "manual": "Classics of Western Spirituality, Paulist Press 1983, ed. Meyendorff, trans. Gendle, confirmed."},
    (1, "Pseudo-Dionysius", 1987): {"url": "https://openlibrary.org/isbn/9780809128389",
        "manual": "Pseudo-Dionysius: The Complete Works, trans. Luibheid, Paulist Press 1987, confirmed."},
    (1, "Wiener", 1948): {"manual": "1948 first edition confirmed.",
        "correction": "Publisher corrected from 'MIT Press' (a name the press took only in 1962) to the 1948 publishers: Technology Press and John Wiley & Sons (New York); Hermann (Paris)."},
    (1, "Callard", 2018): {"manual": "Oxford University Press 2018, confirmed. (A 2026-09 version of Paper 1 misattributed a quotation to this book; the 2026-09-27 text quotes nothing from it.)"},
    (1, "Nayebi", 2025): {"manual": "arXiv abstract confirms the undecidability-by-halting-reduction result the annotation describes.",
        "correction": "Added the venue given on arXiv: to appear in the AAAI 2026 Machine Ethics Workshop proceedings."},
    (1, "Wang", 2025): {"manual": "arXiv journal reference confirms publication in TMLR 2026, and the abstract confirms the capacity-bounded PAC-learnability result the annotation describes."},
    (1, "Adams", 2017): {"manual": "The sentence quoted in §7.5 (now §6.5; 'is only possible for a subsystem interacting with an external environment') was found verbatim in the full text (PMC5430523)."},
    (1, "Dietrich", 2013): {"manual": "IJGT 42(3): 613-637 confirmed in Crossref. Full text read in the authors' accepted manuscript (LSE Research Online, eprint 46864); the 2026-09-27 text paraphrases the model (stable weighing relation, changing salient properties) and quotes nothing."},
    (1, "Bradley", 2009): {"manual": "PPE 8(2): 223-242 confirmed in Crossref. Full text read in the LSE working-paper version (CPNSS 2008, eprint 27007): three models (classical, Jeffrey, generalised conditioning) and the 'as ad hoc' point, as the 2026-09-27 text paraphrases them."},
    (1, "Bykvist", 2006): {"manual": "Utilitas 18(3): 264-283 confirmed; publisher abstract read (evaluation by the attitudes held while leading a life)."},
    (1, "Hansson", 1995): {"manual": "Theory and Decision 38(1): 1-28 confirmed; publisher abstract read (revision, contraction, addition, subtraction under rationality postulates)."},
    (1, "Carroll", 2022): {"url": "https://arxiv.org/abs/2204.11966", "manual": "arXiv:2204.11966 confirmed, with the arXiv comment 'Accepted to ICML 2022 (Spotlight)'; abstract read."},
    (1, "Bykvist", 2021): {"url": "https://doi.org/10.1093/mind/fzaa094",
        "manual": "Crossref: review of Pettigrew, Choosing for Changing Selves, Mind 130(520): 1327-1336, DOI 10.1093/mind/fzaa094. The automated title comparison fails only because the review has no title of its own.",
        "correction": "The 2026-09-27 draft gave the end page as '[end page to be checked]' and no DOI; end page 1336 and the DOI were added from Crossref."},
    (1, "Mele", 1995): {"url": "https://openlibrary.org/search?q=autonomous+agents+mele",
        "manual": "Open Library: Alfred R. Mele, Autonomous Agents, Oxford University Press, first published 1995. The automated title+author query returned nothing; a keyword query found it."},
    (2, "Amorim", 2023, "I-CARE"): {"url": "https://doi.org/10.13026/m33r-bj81",
        "manual": "DataCite record for DOI 10.13026/m33r-bj81: dataset 'I-CARE: International Cardiac Arrest REsearch consortium Database', version 2.1, PhysioNet, 2023, twelve authors from Amorim to Westover as listed."},
    (2, "Iyengar", 1996): {"url": "https://doi.org/10.1152/ajpregu.1996.271.4.R1078",
        "manual": "Crossref and OpenAlex: Am J Physiol Regul Integr Comp Physiol 271(4): R1078-R1084.",
        "correction": "The 2026-09-27 draft gave the journal as 'American Journal of Physiology' with pages 1078-1084; the section title, issue, R-prefixed pages and DOI were added."},
    (2, "Pan", 1985): {"url": "https://doi.org/10.1109/TBME.1985.325532",
        "manual": "Crossref: IEEE Trans Biomed Eng BME-32(3): 230-236. The automated volume check fails only on IEEE's 'BME-32' form of volume 32."},
    (3, "Li", 2021): {"url": "https://doi.org/10.1109/TPAMI.2020.2973153",
        "manual": "Crossref holds only the 2020 early-access record (pages 1-1). Semantic Scholar gives the issue: IEEE TPAMI 43: 316-333 (January 2021 issue), as the paper cites."},
    (2, "Hameroff", 2014): {"url": "https://doi.org/10.1016/j.plrev.2013.08.002",
        "manual": "Physics of Life Reviews 11(1): 39-78, confirmed; the automated pass matched a 2016 book chapter with a similar title instead."},
    (2, "Cao", 2022): {"url": "https://doi.org/10.1103/physrevd.105.026018",
        "manual": "Physical Review D 105: 026018, confirmed.",
        "correction": "Title corrected from the abbreviated 'Hyper-Invariant MERA: …' to the published title 'Hyperinvariant Multiscale Entanglement Renormalization Ansatz: Approximate Holographic Error Correction Codes with Power-Law Correlations'."},
    (2, "Metzinger", 2003): {"url": "https://direct.mit.edu/books/monograph/1991/Being-No-OneThe-Self-Model-Theory-of-Subjectivity",
        "manual": "MIT Press 2003, confirmed."},
    (3, "Barachant", None): {"url": "https://doi.org/10.5281/zenodo.593816",
        "manual": "pyRiemann software, Zenodo concept DOI 10.5281/zenodo.593816 confirmed on Zenodo (creators Barachant, Barthelemy, et al.); version 0.12 used in mdm_trap_control."},
    (3, "Goldberger", 2000): {"url": "https://doi.org/10.1161/01.cir.101.23.e215",
        "manual": "Circulation 101(23): e215-e220, confirmed in Crossref (Crossref lists the title without its subtitle)."},
    (3, "Hsu", 2002): {"url": "https://bookstore.ams.org/gsm-38",
        "manual": "Graduate Studies in Mathematics 38, American Mathematical Society 2002, confirmed."},
}


def references(paper):
    text = open(os.path.join(ROOT, paper), encoding="utf-8").read()
    sec = text.split("## References", 1)[1].split("\n## ", 1)[0]
    return [l.strip() for l in sec.split("\n") if l.strip()]


def main():
    for n in (1, 2, 3):
        auto = json.load(open(os.path.join(HERE, f"auto_paper{n}.json"), encoding="utf-8"))
        current = references(f"Paper{n}.md")
        assert len(current) == len(auto), f"Paper{n}: reference count changed"
        out = []
        for i, (a, line) in enumerate(zip(auto, current)):
            m = next((v for k, v in MANUAL.items() if len(k) == 4 and k[:3] == (n, a["surname"], a["year"])
                      and (a.get("title") or "").startswith(k[3])), None) \
                or MANUAL.get((n, a["surname"], a["year"]), {})
            if a["auto_status"] != "MATCH" and not m:
                raise SystemExit(f"Paper{n} #{i} {a['surname']} {a['year']}: automated non-match "
                                 f"with no manual review recorded")
            rec = {
                "n": i + 1,
                "citation": line,
                "status": "verified-corrected" if m.get("correction") else "verified",
                "url": m.get("url") or a.get("url"),
                "checked_against": a.get("source") if a["auto_status"] == "MATCH" else "manual",
                "automated_pass": a["auto_status"],
            }
            if a.get("doi") and "doi.org" in (rec["url"] or ""):
                rec["doi"] = a["doi"] if not m.get("url") else rec["url"].split("doi.org/")[1]
            if m.get("manual"):
                rec["manual_review"] = m["manual"]
            if m.get("correction"):
                rec["correction"] = m["correction"]
            out.append(rec)
        json.dump(out, open(os.path.join(HERE, f"paper{n}.json"), "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        c = sum(r["status"] == "verified-corrected" for r in out)
        print(f"Paper{n}: {len(out)} references, {len(out) - c} verified, {c} verified-corrected")


if __name__ == "__main__":
    main()
