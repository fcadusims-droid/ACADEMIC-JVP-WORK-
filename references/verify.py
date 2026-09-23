"""Automated first pass of the citation audit.

For every reference in the References section of Paper1.md, Paper2.md and Paper3.md this
queries a primary bibliographic index and compares what the paper says against what the index
returns:

  * journal articles / chapters with a quoted title -> Crossref (DOI, title, authors, year,
    journal, volume, pages);
  * arXiv preprints -> the arXiv API (title, authors, year);
  * books (italic title, no quoted title) -> Open Library (title, author, first-publication year).

It never marks anything verified on its own: it writes `auto_status` = MATCH / PARTIAL / NOMATCH,
with the fields that disagreed. Every entry is then checked by hand and its final `status`
recorded in references/paperN.json (see references/README.md).

Usage:
    python references/verify.py            # writes references/auto_paperN.json
"""
from __future__ import annotations

import difflib
import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "ACADEMIC-JVP-WORK citation audit (https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-)"}


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(2 ** i)
    return None


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()


def sim(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()


def references(paper):
    text = open(os.path.join(ROOT, paper), encoding="utf-8").read()
    sec = text.split("## References", 1)[1]
    sec = re.split(r"\n## ", sec, 1)[0]
    return [l.strip() for l in sec.split("\n") if l.strip()]


def parse(line):
    """Pull first-author surname, year, quoted title, italic title, volume, pages, DOI, arXiv."""
    ref = {"raw": line}
    ref["surname"] = re.split(r"[,.]", line, 1)[0].strip()
    y = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", line)
    ref["year"] = int(y.group(1)) if y else None
    q = re.search(r"[\"“]([^\"”]+)[\"”]", line)
    ref["title"] = q.group(1).rstrip(".") if q else None
    it = re.findall(r"\*([^*]+)\*", line)
    ref["container"] = it[0] if (it and q) else None
    if not q and it:
        ref["title"] = it[0]
        ref["book"] = True
    m = re.search(r"\*\s*(\d+)\s*(?:\((\d+[-–]?\d*)\))?\s*:\s*([\de]+)\s*[-–]?\s*(\d*)", line)
    if m:
        ref["volume"], ref["first_page"] = m.group(1), m.group(3)
    d = re.search(r"DOI:\s*(10\.\S+?)[.)]?(\s|$)", line)
    ref["doi"] = d.group(1) if d else None
    a = re.search(r"arXiv:(\d{4}\.\d{4,5})", line)
    ref["arxiv"] = a.group(1) if a else None
    return ref


def crossref(ref):
    if ref.get("doi"):
        js = fetch("https://api.crossref.org/works/" + urllib.parse.quote(ref["doi"]))
        items = [json.loads(js)["message"]] if js else []
    else:
        q = urllib.parse.quote(re.sub(r"\([^)]*\)\s*$", "", ref["raw"])[:400])
        js = fetch(f"https://api.crossref.org/works?query.bibliographic={q}&rows=5")
        items = json.loads(js)["message"]["items"] if js else []
    best, score = None, 0.0
    for it in items:
        t = (it.get("title") or [""])[0]
        s = sim(ref["title"] or "", t)
        if s > score:
            best, score = it, s
    if not best:
        return {"auto_status": "NOMATCH", "source": "crossref"}
    fam = [a.get("family", "") for a in best.get("author", [])]
    yr = None
    for k in ("published-print", "published-online", "issued"):
        if best.get(k, {}).get("date-parts"):
            yr = best[k]["date-parts"][0][0]
            break
    out = {"source": "crossref", "doi": best.get("DOI"), "url": "https://doi.org/" + best.get("DOI", ""),
           "found_title": (best.get("title") or [""])[0],
           "found_container": (best.get("container-title") or [""])[0],
           "found_authors": fam[:6], "found_year": yr,
           "found_volume": best.get("volume"), "found_page": best.get("page"),
           "title_similarity": round(score, 3)}
    problems = []
    if score < 0.85:
        problems.append("title")
    sn = " ".join(norm(ref["surname"]))
    if fam and not any(sn and sn in " ".join(norm(f)) or " ".join(norm(f)) in sn for f in fam):
        problems.append("author")
    if ref["year"] and yr and abs(ref["year"] - yr) > 1:
        problems.append("year")
    if ref.get("volume") and out["found_volume"] and str(ref["volume"]) != str(out["found_volume"]):
        problems.append("volume")
    if ref.get("first_page") and out["found_page"] and not str(out["found_page"]).startswith(str(ref["first_page"])) \
            and str(ref["first_page"]) not in str(best.get("article-number", "")):
        problems.append("pages")
    out["auto_status"] = "MATCH" if not problems else ("NOMATCH" if "title" in problems else "PARTIAL")
    out["auto_problems"] = problems
    return out


def arxiv(ref):
    """arXiv abstract page -> citation_* meta tags (the export API returns empty bodies from
    this environment)."""
    html = fetch("https://arxiv.org/abs/" + ref["arxiv"])
    if not html:
        return {"auto_status": "NOMATCH", "source": "arxiv"}
    meta = lambda k: re.findall(r'<meta name="%s" content="([^"]*)"' % k, html)
    t = (meta("citation_title") or [""])[0]
    authors = meta("citation_author")
    d = (meta("citation_date") or [""])[0]
    yr = int(d[:4]) if d[:4].isdigit() else None
    if not t:
        return {"auto_status": "NOMATCH", "source": "arxiv"}
    s = sim(ref["title"] or "", t)
    problems = []
    if s < 0.85:
        problems.append("title")
    if not any(" ".join(norm(ref["surname"])) in " ".join(norm(a)) for a in authors):
        problems.append("author")
    if ref["year"] and yr and abs(ref["year"] - yr) > 1:
        problems.append("year")
    return {"source": "arxiv", "url": "https://arxiv.org/abs/" + ref["arxiv"], "found_title": t,
            "found_authors": authors[:6], "found_year": yr, "title_similarity": round(s, 3),
            "auto_problems": problems,
            "auto_status": "MATCH" if not problems else ("NOMATCH" if "title" in problems else "PARTIAL")}


def openlibrary(ref):
    F = "title,author_name,publisher,publish_year,first_publish_year,key"
    q = urllib.parse.urlencode({"title": ref["title"], "author": ref["surname"], "limit": 5, "fields": F})
    js = fetch("https://openlibrary.org/search.json?" + q)
    docs = json.loads(js).get("docs", []) if js else []
    if not docs:
        q = urllib.parse.urlencode({"q": f'{ref["title"]} {ref["surname"]}', "limit": 5, "fields": F})
        js = fetch("https://openlibrary.org/search.json?" + q)
        docs = json.loads(js).get("docs", []) if js else []
    best, score = None, 0.0
    for d in docs:
        s = max(sim(ref["title"], d.get("title", "")),
                sim(ref["title"].split(":")[0], d.get("title", "")))
        if s > score:
            best, score = d, s
    if not best:
        return {"auto_status": "NOMATCH", "source": "openlibrary"}
    authors = best.get("author_name", [])[:6]
    problems = []
    if score < 0.8:
        problems.append("title")
    if not any(" ".join(norm(ref["surname"])) in " ".join(norm(a)) for a in authors):
        problems.append("author")
    return {"source": "openlibrary", "url": "https://openlibrary.org" + best.get("key", ""),
            "found_title": best.get("title"), "found_authors": authors,
            "found_first_year": best.get("first_publish_year"),
            "found_publishers": best.get("publisher", [])[:40],
            "found_publish_years": sorted(set(best.get("publish_year", []))), "title_similarity": round(score, 3),
            "auto_problems": problems,
            "auto_status": "MATCH" if not problems else ("NOMATCH" if "title" in problems else "PARTIAL")}


def main():
    for n in (1, 2, 3):
        rows = []
        for line in references(f"Paper{n}.md"):
            ref = parse(line)
            if ref.get("arxiv"):
                res = arxiv(ref)
            elif ref.get("book"):
                res = openlibrary(ref)
            elif ref.get("title"):
                res = crossref(ref)
            else:
                res = {"auto_status": "NOMATCH", "source": None}
            ref.update(res)
            rows.append(ref)
            print(f"P{n} {ref['auto_status']:8s} {ref['surname'][:18]:18s} {ref['year']} "
                  f"{(ref.get('title') or '')[:50]:50s} {ref.get('auto_problems', '')}", flush=True)
            time.sleep(0.3)
        json.dump(rows, open(os.path.join(OUT, f"auto_paper{n}.json"), "w"), indent=2,
                  ensure_ascii=False)


if __name__ == "__main__":
    main()
