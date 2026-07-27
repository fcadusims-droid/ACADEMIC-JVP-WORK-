#!/usr/bin/env python3
"""Static-site generator for the ACADEMIC-JVP-WORK- repository.

Everything the site shows is derived from the repository at build time -- the papers
from their Markdown sources, the experiment pages from the pre-registrations and the
committed `result.json` files, the status table from `experiments/STATUS.md`. Nothing
is hand-maintained in HTML, so adding an experiment or editing a paper propagates to
the site on the next build with no changes here.

Outputs into `_site/`:

    index.html                 programme overview
    papers/index.html          the three papers
    papers/paper-N.html        full text, navigable, with a section index
    papers/paper-N-pdf.html    the PDF read in the browser
    papers/paper-N.pdf         the PDF, downloadable
    experiments/index.html     every run, with verdicts
    experiments/<slug>.html    pre-registration, verdict, figures, raw JSON
    methodology.html  data.html  reproduce.html  formal.html

Usage:
    python site/build.py [--no-pdf]

`--no-pdf` skips the LaTeX pass, which is the slow part; the PDF pages then link to
files that do not exist, so it is for previewing HTML only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "_site")
RESULTS = os.path.join(ROOT, "experiments", "_results")
REPO_URL = "https://github.com/fcadusims-droid/ACADEMIC-JVP-WORK-"

PAPERS = [
    {
        "n": 1, "src": "Paper1.md", "slug": "paper-1",
        "short": "The Cybernetic Impossibility of Conversion",
        "sub": "A Transcendental Negative Critique of Control-Theoretic Models of "
               "Existential Transformation",
        "blurb": "A negative result. Given control as directed change relative to a "
                 "held-fixed evaluative structure, agency-preserving conversion cannot "
                 "be formulated as control without collapsing into tautology, "
                 "annihilation, or incommensurability.",
        "content": "paper1.md", "dir": "paper1_control_trilemma",
    },
    {
        "n": 2, "src": "Paper2.md", "slug": "paper-2",
        "short": "The Conditional Biological Requirements Architecture",
        "sub": "Data Requirements for Testing Hidden Boundary Organization in "
               "Biological State Transitions, and a Pre-Registered Negative on Their "
               "Present Availability",
        "blurb": "A strict eliminative protocol, conditional throughout, built so that "
                 "a clean negative is expected unless a structured boundary residual "
                 "survives an adversarial sequence of controls. Its positive arm halted "
                 "at a pre-registered gate.",
        "content": "paper2.md", "dir": "paper2_cbra_protocol",
    },
    {
        "n": 3, "src": "Paper3.md", "slug": "paper-3",
        "short": "The Kinematics of Geodesic Flow on Riemannian Vector Bundles",
        "sub": "A Non-Equilibrium Jump-Diffusion Protocol for the Asymptotic "
               "Demarcation of Systemic State Transitions",
        "blurb": "A single-trajectory method for deciding whether dynamics after an "
                 "abrupt transition is directed drift, undirected diffusion, or "
                 "structural collapse -- from one record, with no ensemble. "
                 "Independent of its two companions.",
        "content": "paper3.md", "dir": "paper3_geodesic_kinematics",
    },
]

NAV = [
    ("index.html", "Overview"),
    ("papers/index.html", "Papers"),
    ("experiments/index.html", "Experiments"),
    ("data.html", "Data"),
    ("methodology.html", "Methodology"),
    ("formal.html", "Formal"),
    ("reproduce.html", "Reproduce"),
]


# --------------------------------------------------------------------------
# markdown / pdf
# --------------------------------------------------------------------------

def _pandoc(args, stdin=None):
    return subprocess.run(["pandoc"] + args, input=stdin, capture_output=True,
                          text=True, check=True).stdout


def md_to_html(text: str) -> str:
    """Markdown fragment -> HTML fragment, math converted to MathML.

    MathML rather than a client-side TeX renderer, deliberately. A CDN script that
    fails to load does not degrade gracefully -- the reader is shown raw source,
    `\\(D_{ag}\\to 0\\)`, in what is supposed to be a published paper. MathML is
    produced here at build time and rendered natively by every current browser, so
    the mathematics does not depend on a third party being reachable.
    """
    return _pandoc(["-f", "markdown+tex_math_dollars+pipe_tables+raw_tex-raw_html",
                    "-t", "html5", "--mathml", "--wrap=none"], stdin=text)


def md_file_to_html(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return md_to_html(fh.read())


def md_to_html_with_toc(text: str) -> tuple[str, str]:
    """Returns (toc_html, body_html) for a long document."""
    tpl = os.path.join(SITE, "templates", "split.html")
    out = _pandoc(["-f", "markdown+tex_math_dollars+pipe_tables+raw_tex-raw_html",
                   "-t", "html5", "--mathml", "--wrap=none", "--standalone",
                   "--toc", "--toc-depth=2", "--section-divs",
                   f"--template={tpl}"], stdin=text)
    toc, _, body = out.partition("<!--PANDOC-SPLIT-->")
    return toc.strip(), body.strip()


PDF_HEADER = r"""
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}
"""


def verify_pdf(path: str, min_pages: int = 5) -> list:
    """Check a freshly-built PDF is a publishable document, not a broken one.

    The PDFs are regenerated from the Markdown on every push, so each build is a fresh
    opportunity for LaTeX to produce something wrong-but-not-empty: a truncated file
    after a mid-document error, or a page rendering `$x = $` literally because a
    delimiter was malformed. Both look like success to a build script that only checks
    the exit status. These are the checks that catch them.
    """
    problems = []
    if not os.path.exists(path):
        return [f"{os.path.basename(path)} was not produced"]
    size = os.path.getsize(path)
    if size < 20_000:
        problems.append(f"{os.path.basename(path)} is only {size} bytes — truncated")
    with open(path, "rb") as fh:
        if not fh.read(5).startswith(b"%PDF-"):
            problems.append(f"{os.path.basename(path)} is not a PDF")

    try:
        info = subprocess.run(["pdfinfo", path], capture_output=True, text=True,
                              check=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", info, re.M)
        pages = int(m.group(1)) if m else 0
        if pages < min_pages:
            problems.append(f"{os.path.basename(path)} has only {pages} pages — "
                            f"the LaTeX pass probably stopped early")
        text = subprocess.run(["pdftotext", path, "-"], capture_output=True,
                              text=True, check=True).stdout
        # A '$' in the *output* means a delimiter was never parsed as math.
        for m in re.finditer(r".{0,50}\$.{0,50}", text):
            problems.append(f"{os.path.basename(path)}: a literal '$' reached the "
                            f"page — …{' '.join(m.group(0).split())}…")
        for marker in ("??", "[MISSING]"):
            if text.count(marker) > 3:
                problems.append(f"{os.path.basename(path)}: {text.count(marker)} "
                                f"'{marker}' markers — unresolved references")
    except FileNotFoundError:
        print("  ~ poppler-utils absent; PDF content not inspected", file=sys.stderr)
    except subprocess.CalledProcessError:
        problems.append(f"{os.path.basename(path)} could not be read back")
    return problems


def build_pdf(src: str, dest: str, title: str, subtitle: str) -> bool:
    """Render a paper to PDF via XeLaTeX. Returns False if the toolchain fails."""
    hdr = os.path.join(OUT, "_header.tex")
    with open(hdr, "w", encoding="utf-8") as fh:
        fh.write(PDF_HEADER)
    # The papers carry their own H1 title line; strip it so it is not duplicated
    # under the LaTeX title block.
    with open(src, encoding="utf-8") as fh:
        body = fh.read()
    body = re.sub(r"\A#\s+.*?\n", "", body, count=1)
    body = re.sub(r"\A\s*Jo[a-zA-ZÀ-ſ]* Vitor Perazzolo\s*\n", "", body)
    meta = (f"---\ntitle: |\n  {title}\nsubtitle: |\n  {subtitle}\n"
            f"author: João Vitor Perazzolo\ndate: July 2026\n---\n\n")
    try:
        subprocess.run(
            ["pandoc", "-f", "markdown+tex_math_dollars+pipe_tables+raw_tex-raw_html",
             "-o", dest, "--pdf-engine=xelatex", "--toc", "--toc-depth=2",
             "-V", "documentclass=article", "-V", "papersize=a4",
             "-V", "geometry:margin=2.6cm", "-V", "fontsize=11pt",
             "-V", "linkcolor=RoyalBlue", "-V", "urlcolor=RoyalBlue",
             "-V", "colorlinks=true", "-V", "linestretch=1.08",
             f"--include-in-header={hdr}"],
            input=meta + body, capture_output=True, text=True, check=True)
        return True
    except FileNotFoundError:
        print("  ! pandoc not found; skipping PDF", file=sys.stderr)
    except subprocess.CalledProcessError as exc:
        print(f"  ! PDF build failed for {os.path.basename(dest)}", file=sys.stderr)
        print((exc.stderr or "")[-2500:], file=sys.stderr)
    return False


# --------------------------------------------------------------------------
# page shell
# --------------------------------------------------------------------------

# No client-side maths renderer: the formulas are already MathML in the markup, so
# the page needs no JavaScript and no third-party host to display them correctly.
MATH_STYLE = """
<style>
math { font-size: 1.02em; }
mrow, mi, mn, mo { font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", serif; }
math[display="block"] { display: block; margin: 1.1rem 0; overflow-x: auto; overflow-y: hidden; }
</style>
"""


def page(title: str, body: str, depth: int = 0, current: str = "",
         wide: bool = False, desc: str = "", math: bool = True) -> str:
    up = "../" * depth
    nav = "\n".join(
        '      <a href="{}{}"{}>{}</a>'.format(
            up, href, ' class="current"' if href == current else "", label)
        for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or title)}">
<meta name="author" content="João Vitor Perazzolo">
<link rel="stylesheet" href="{up}assets/style.css">
{MATH_STYLE if math else ""}
</head>
<body>
<header class="masthead">
  <div class="masthead-inner">
    <a class="wordmark" href="{up}index.html">João Vitor Perazzolo &middot; Research Programme</a>
    <nav class="site">
{nav}
    </nav>
  </div>
</header>
<main{' class="wide"' if wide else ''}>
{body}
</main>
<footer class="site">
  <div class="inner">
    <p>Generated from the repository at commit <code>{COMMIT}</code> on {BUILD_DATE}.
       Every figure, number and verdict on this site is read from a committed
       <code>result.json</code>; the papers are rendered from their Markdown sources.</p>
    <p><a href="{REPO_URL}">Source repository</a> &middot;
       <a href="{REPO_URL}/blob/main/CITATION.cff">Citation metadata</a> &middot;
       <a href="{REPO_URL}/blob/main/METHODOLOGY.md">Methodology</a></p>
  </div>
</footer>
</body>
</html>
"""


def write(relpath: str, content: str):
    dest = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(content)


def wrap_tables(h: str) -> str:
    """Tables must scroll inside their own box rather than widen the page."""
    return h.replace("<table>", '<div class="table-scroll"><table>') \
            .replace("</table>", "</table></div>")


# --------------------------------------------------------------------------
# repository facts
# --------------------------------------------------------------------------

def git(*args, default=""):
    try:
        return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return default


COMMIT = git("rev-parse", "--short", "HEAD", default="unknown")
BUILD_DATE = _dt.datetime.now(_dt.timezone.utc).strftime("%d %B %Y, %H:%M UTC")

ROW_SPLIT = re.compile(r"(?<!\\)\|")


def parse_status() -> dict:
    """`experiments/STATUS.md` -> {slug: {label, paper, state, summary}}."""
    path = os.path.join(ROOT, "experiments", "STATUS.md")
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in ROW_SPLIT.split(line)[1:-1]]
            if len(cells) < 5:
                continue
            slug = cells[1].strip("`*_ ")
            if cells[0].strip("*| ").lower() in {"#", ""}:
                continue
            out[slug] = {
                "label": cells[0].strip("*` "),
                "paper": cells[2].strip(),
                "state": cells[3].strip(),
                "summary": cells[4].strip(),
            }
    return out


STATUS = parse_status()


def experiment_dirs() -> dict:
    """slug -> source directory relative to the repository root."""
    out = {}
    exp = os.path.join(ROOT, "experiments")
    for paper in sorted(os.listdir(exp)):
        pdir = os.path.join(exp, paper)
        if not os.path.isdir(pdir) or not paper.startswith("paper"):
            continue
        for slug in sorted(os.listdir(pdir)):
            if os.path.isdir(os.path.join(pdir, slug)):
                out[slug] = f"experiments/{paper}/{slug}"
    return out


SRC_DIRS = experiment_dirs()


def paper_of(slug: str) -> str:
    d = SRC_DIRS.get(slug, "")
    m = re.search(r"paper(\d)_", d)
    if m:
        return m.group(1)
    return (STATUS.get(slug, {}).get("paper") or "?").strip()


VERDICT_KEYS = ["verdict", "outcome", "preregistered_criterion",
                "preregistered_question", "question", "motivation"]


def load_results() -> list:
    """One record per experiment with a committed result.json."""
    recs = []
    if not os.path.isdir(RESULTS):
        return recs
    for slug in sorted(os.listdir(RESULTS)):
        rj = os.path.join(RESULTS, slug, "result.json")
        if not os.path.exists(rj):
            continue
        try:
            with open(rj, encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError:
            print(f"  ! {slug}/result.json is not valid JSON; skipped",
                  file=sys.stderr)
            continue
        figs = sorted(f for f in os.listdir(os.path.join(RESULTS, slug))
                      if f.lower().endswith((".png", ".svg", ".jpg")))
        src = SRC_DIRS.get(slug)
        prereg = None
        if src and os.path.exists(os.path.join(ROOT, src, "PRE-REGISTRATION.md")):
            prereg = os.path.join(src, "PRE-REGISTRATION.md")
        recs.append({"slug": slug, "data": data, "figures": figs, "src": src,
                     "prereg": prereg, "paper": paper_of(slug),
                     "status": STATUS.get(slug)})
    return recs


def headline(rec) -> str:
    """The shortest honest one-liner available for an experiment."""
    d = rec["data"]
    for k in ("verdict", "outcome"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            first = re.split(r"(?<=[.!?])\s+", v.strip())[0]
            return first if len(first) < 400 else first[:397] + "…"
    st = rec.get("status")
    if st:
        txt = re.sub(r"\*\*|`", "", st["summary"])
        return re.split(r"(?<=[.!?])\s+", txt)[0]
    return "See the raw result."


def json_block(data) -> str:
    return ('<details><summary>Raw <code>result.json</code></summary>'
            f'<pre><code>{html.escape(json.dumps(data, indent=2))}</code></pre>'
            '</details>')


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------

def build_papers(with_pdf: bool):
    cards = []
    for p in PAPERS:
        src = os.path.join(ROOT, p["src"])
        with open(src, encoding="utf-8") as fh:
            raw = fh.read()
        title = f"Paper {p['n']} — {p['short']}"

        pdf_name = f"{p['slug']}.pdf"
        pdf_path = os.path.join(OUT, "papers", pdf_name)
        pdf_ok = False
        if with_pdf:
            print(f"  PDF: {p['src']} → papers/{pdf_name}")
            os.makedirs(os.path.join(OUT, "papers"), exist_ok=True)
            pdf_ok = build_pdf(src, pdf_path, p["short"], p["sub"])
            if pdf_ok:
                bad = verify_pdf(pdf_path)
                for b in bad:
                    print(f"  ! {b}", file=sys.stderr)
                    FAILURES.append(b)
                if not bad:
                    print(f"    verified: {os.path.getsize(pdf_path)//1024} KB")
            else:
                FAILURES.append(f"{pdf_name} failed to build")

        # --- full text, navigable ---------------------------------------
        toc, body = md_to_html_with_toc(raw)
        body = wrap_tables(body)
        summary = wrap_tables(md_file_to_html(os.path.join(SITE, "content", p["content"])))

        related = [r for r in RECORDS if r["paper"] == str(p["n"])]
        rel_html = ""
        if related:
            items = "\n".join(
                f'<li><a href="../experiments/{r["slug"]}.html">'
                f'<code>{r["slug"]}</code></a> &mdash; {html.escape(headline(r))}</li>'
                for r in related)
            rel_html = (f'<h2>Experiments testing this paper</h2>'
                        f'<ul class="plain">{items}</ul>')

        actions = (
            f'<div class="btn-row">'
            f'<a class="btn primary" href="{p["slug"]}-pdf.html">Read the PDF in browser</a>'
            f'<a class="btn" href="{pdf_name}" download>Download PDF</a>'
            f'<a class="btn" href="{REPO_URL}/blob/main/{p["src"]}">Markdown source</a>'
            f'</div>')

        overview = f"""
<p class="kicker">Paper {p['n']}</p>
<h1>{html.escape(p['short'])}</h1>
<p class="lede">{html.escape(p['sub'])}</p>
<p class="meta">João Vitor Perazzolo &middot; July 2026</p>
{actions}
<div class="prose">
{summary}
{rel_html}
</div>
<h2 id="full-text">Full text</h2>
<p class="prose">The complete paper follows, rendered from its source with a section
index. It is the same text as the PDF.</p>
"""
        full = f"""{overview}
<div class="paper-layout">
  <aside class="paper-toc">
    <div class="toc-title">Contents</div>
    {toc}
  </aside>
  <article class="paper-body">
{body}
  </article>
</div>
"""
        write(f"papers/{p['slug']}.html",
              page(title, full, depth=1, current="papers/index.html", wide=True,
                   desc=p["blurb"]))

        # --- in-browser PDF reader --------------------------------------
        reader = f"""
<p class="kicker">Paper {p['n']} &middot; PDF</p>
<h1>{html.escape(p['short'])}</h1>
<p class="meta">João Vitor Perazzolo &middot; July 2026 &middot;
   <a href="{p['slug']}.html">back to the annotated version</a></p>
<div class="btn-row">
  <a class="btn primary" href="{pdf_name}" download>Download PDF</a>
  <a class="btn" href="{pdf_name}">Open PDF in a new tab</a>
  <a class="btn" href="{p['slug']}.html">Read as web page</a>
</div>
<p class="note">The viewer below is your browser's own. If it does not appear —
some mobile browsers decline to embed PDFs — use <em>Download</em> or
<em>Open in a new tab</em>, or read the
<a href="{p['slug']}.html">web version</a>, which carries identical text.</p>
<object class="pdf-frame" data="{pdf_name}" type="application/pdf">
  <div class="pdf-fallback">
    <p>Your browser cannot display the PDF inline.</p>
    <p><a class="btn primary" href="{pdf_name}" download>Download the PDF</a></p>
  </div>
</object>
"""
        write(f"papers/{p['slug']}-pdf.html",
              page(f"{title} (PDF)", reader, depth=1, current="papers/index.html",
                   wide=True, desc=p["blurb"], math=False))

        size = ""
        if os.path.exists(pdf_path):
            size = f" &middot; {os.path.getsize(pdf_path) / 1_048_576:.1f} MB"
        cards.append(f"""
<div class="card">
  <span class="num">Paper {p['n']}</span>
  <h3>{html.escape(p['short'])}</h3>
  <p>{html.escape(p['blurb'])}</p>
  <div class="spacer"></div>
  <div class="btn-row">
    <a class="btn primary" href="{p['slug']}.html">Read</a>
    <a class="btn" href="{p['slug']}-pdf.html">PDF</a>
    <a class="btn" href="{pdf_name}" download>Download{size}</a>
  </div>
</div>""")

    idx = f"""
<h1>The papers</h1>
<p class="lede prose">Three interlinked papers. Each is available as a navigable web
page with a section index, as a PDF you can read here in the browser, and as a PDF you
can download.</p>
<div class="cards">{''.join(cards)}</div>
<div class="prose">
<h2>How they depend on one another</h2>
<p>The dependency runs one way. Paper&nbsp;2 borrows Paper&nbsp;1's Class&nbsp;G and
its consistency contract <em>I</em>; nothing flows back, so Paper&nbsp;2's empirical
fate leaves Paper&nbsp;1 untouched. Paper&nbsp;3 is logically independent of both and
stands or falls as a time-series method, which is why a reader who accepts it incurs
no commitment to the other two.</p>
<p>They also differ in kind. Paper&nbsp;1 is transcendental and negative: it argues
that a family of models cannot pose a question, not that some particular model is
wrong. Paper&nbsp;2 is conditional and eliminative, and its title now carries the
pre-registered negative that halted its positive arm. Paper&nbsp;3 is an ordinary
methods paper making an ordinary methods claim, tested against ordinary baselines.</p>
</div>
"""
    write("papers/index.html",
          page("Papers", idx, depth=1, current="papers/index.html",
               desc="Three interlinked papers, readable in the browser or downloadable "
                    "as PDFs."))


def build_experiments():
    os.makedirs(os.path.join(OUT, "experiments"), exist_ok=True)

    by_paper = {}
    for r in RECORDS:
        by_paper.setdefault(r["paper"], []).append(r)

    sections = []
    for pnum in sorted(by_paper, key=lambda x: (not x.isdigit(), x)):
        rows = []
        for r in sorted(by_paper[pnum], key=lambda x: x["slug"]):
            label = (r["status"] or {}).get("label", "")
            chip = ('<br><span class="tag">%s</span>' % html.escape(label)) if label else ""
            rows.append(
                '<tr><td><a href="{slug}.html"><code>{slug}</code></a>{chip}</td>'
                '<td>{hl}</td><td>{nf}</td></tr>'.format(
                    slug=r["slug"], chip=chip,
                    hl=html.escape(headline(r)), nf=len(r["figures"])))
        title = f"Paper {pnum}" if pnum.isdigit() else "Shared"
        sections.append(f"""
<h2 id="paper-{pnum}">{title} &mdash; {len(by_paper[pnum])} experiments</h2>
<div class="table-scroll"><table>
<thead><tr><th>Experiment</th><th>Finding</th><th>Figures</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>""")

    n_fig = sum(len(r["figures"]) for r in RECORDS)
    idx = f"""
<h1>Experiments</h1>
<p class="lede prose">Every computational run in the repository, with the question it
was pre-registered to answer, the verdict issued against that criterion, the figures,
and the raw <code>result.json</code>. This index is generated from the committed
results, so a new experiment appears here without anyone editing the site.</p>
<div class="stat-grid">
  <div class="stat"><span class="k">Experiments</span><span class="v">{len(RECORDS)}</span></div>
  <div class="stat"><span class="k">Figures</span><span class="v">{n_fig}</span></div>
  <div class="stat"><span class="k">Pre-registered</span>
    <span class="v">{sum(1 for r in RECORDS if r['prereg'])}</span></div>
  <div class="stat"><span class="k">Papers covered</span><span class="v">{len(by_paper)}</span></div>
</div>
<div class="note prose">A verdict here is bounded by the scope stated in its own
<code>result.json</code>. Synthetic results are about instruments rather than biology;
single-corpus results are about that corpus; and the logical results say nothing about
instantiation. Negative and qualified results are listed exactly as they came out.</div>
{''.join(sections)}
"""
    write("experiments/index.html",
          page("Experiments", idx, depth=1, current="experiments/index.html", wide=True,
               desc="Every pre-registered run, with verdicts, figures and raw results."))

    for r in RECORDS:
        build_experiment_page(r)


SKIP_IN_TABLE = {"experiment", "verdict", "figures", "question", "motivation",
                 "outcome", "condition_names", "per_subject", "subjects"}


def build_experiment_page(r):
    slug, d = r["slug"], r["data"]
    figdir = os.path.join(OUT, "experiments", "figures", slug)
    os.makedirs(figdir, exist_ok=True)
    for f in r["figures"]:
        shutil.copy2(os.path.join(RESULTS, slug, f), os.path.join(figdir, f))

    paper = r["paper"]
    parts = [f'<p class="kicker">Paper {paper} &middot; experiment</p>'
             f'<h1><code>{slug}</code></h1>']

    q = d.get("question") or d.get("preregistered_question")
    if isinstance(q, str) and q.strip():
        parts.append(f'<p class="lede prose">{html.escape(q.strip())}</p>')

    links = [f'<a class="btn" href="index.html">All experiments</a>']
    if r["src"]:
        links.append(f'<a class="btn" href="{REPO_URL}/blob/main/{r["src"]}/run.py">'
                     f'Source code</a>')
    if r["prereg"]:
        links.append(f'<a class="btn" href="{REPO_URL}/blob/main/{r["prereg"]}">'
                     f'Pre-registration</a>')
    links.append(f'<a class="btn" href="{REPO_URL}/blob/main/experiments/_results/'
                 f'{slug}/result.json">result.json</a>')
    parts.append(f'<div class="btn-row">{"".join(links)}</div>')

    if isinstance(d.get("motivation"), str):
        parts.append(f'<div class="prose"><p>{html.escape(d["motivation"])}</p></div>')

    for key, label in (("verdict", "Verdict"), ("outcome", "Outcome"),
                       ("preregistered_criterion", "Pre-registered criterion")):
        v = d.get(key)
        if isinstance(v, str) and v.strip():
            parts.append(
                f'<div class="verdict"><span class="label">{label}</span>'
                f'<p>{html.escape(v.strip())}</p></div>')

    # key scalars, in the order the runner wrote them
    scalars = [(k, v) for k, v in d.items()
               if k not in SKIP_IN_TABLE and isinstance(v, (int, float, bool, str))
               and not (isinstance(v, str) and len(v) > 120)]
    if scalars:
        cells = "".join(
            f'<div class="stat"><span class="k">{html.escape(k.replace("_", " "))}</span>'
            f'<span class="v">{html.escape(_fmt(v))}</span></div>'
            for k, v in scalars[:18])
        parts.append(f'<h2>Key quantities</h2><div class="stat-grid">{cells}</div>')

    if r["figures"]:
        parts.append("<h2>Figures</h2>")
        for f in r["figures"]:
            parts.append(
                f'<figure><img src="figures/{slug}/{html.escape(f)}" '
                f'alt="{html.escape(slug)} figure" loading="lazy">'
                f'<figcaption><code>{html.escape(f)}</code> &middot; '
                f'<a href="figures/{slug}/{html.escape(f)}">full size</a>'
                f'</figcaption></figure>')

    if r["prereg"]:
        pre = wrap_tables(md_file_to_html(os.path.join(ROOT, r["prereg"])))
        parts.append('<h2>Pre-registration</h2>'
                     '<p class="note">Written before the run, and reproduced here '
                     'unedited — including, where it applies, its own record of a '
                     'departure from the protocol.</p>'
                     f'<div class="prose">{pre}</div>')

    if r["status"]:
        st = wrap_tables(md_to_html(r["status"]["summary"]))
        parts.append(f'<h2>Status-table entry</h2><div class="prose">{st}</div>')

    parts.append("<h2>Raw result</h2>")
    parts.append(json_block(d))

    write(f"experiments/{slug}.html",
          page(f"{slug} — experiment", "\n".join(parts), depth=1,
               current="experiments/index.html",
               desc=headline(r)[:180]))


def _fmt(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def build_static_pages():
    # methodology
    meth = wrap_tables(md_file_to_html(os.path.join(ROOT, "METHODOLOGY.md")))
    write("methodology.html",
          page("Methodology", f'<div class="prose-wide">{meth}</div>', depth=0,
               current="methodology.html", wide=True,
               desc="The pre-registration protocol, and the occasions on which it cost "
                    "something."))

    # data
    body = ('<h1>Data</h1>'
            '<p class="lede prose">What was used, where it came from, and what it can '
            'and cannot support.</p>'
            f'<div class="prose">{md_file_to_html(os.path.join(SITE, "content", "data.md"))}</div>')
    extra = os.path.join(ROOT, "experiments", "paper3_geodesic_kinematics", "DATA.md")
    if os.path.exists(extra):
        body += ('<h2>Acquisition notes</h2><div class="prose">'
                 + wrap_tables(md_file_to_html(extra)) + "</div>")
    write("data.html", page("Data", body, depth=0, current="data.html",
                            desc="Public datasets used by the experiment suite."))

    # reproduce
    body = ('<h1>Reproducing this work</h1>'
            '<p class="lede prose">Results, code and pre-registrations are committed. '
            'Only the datasets are not, and all of them are public.</p>'
            f'<div class="prose">{md_file_to_html(os.path.join(SITE, "content", "reproduce.md"))}</div>')
    write("reproduce.html", page("Reproduce", body, depth=0, current="reproduce.html",
                                 desc="How to run the experiment suite."))

    # formal
    fr = os.path.join(ROOT, "formal", "README.md")
    inner = md_file_to_html(fr) if os.path.exists(fr) else (
        "<p>No formalization is present in this build.</p>")
    body = ('<h1>Formal artefacts</h1>'
            '<p class="lede prose">A Lean&nbsp;4 formalization of the trichotomy. It '
            'compiles with no <code>sorry</code> — but a formalization is only as '
            'strong as what it assumes, so the axioms are audited and listed rather '
            'than left implicit.</p>'
            f'<div class="prose">{wrap_tables(inner)}</div>'
            f'<div class="btn-row"><a class="btn" href="{REPO_URL}/tree/main/formal">'
            f'Browse <code>formal/</code></a></div>')
    write("formal.html", page("Formal artefacts", body, depth=0, current="formal.html",
                              desc="Lean 4 formalization and its audited axioms."))


def build_index():
    overview = wrap_tables(md_file_to_html(os.path.join(SITE, "content", "overview.md")))

    cards = "".join(f"""
<div class="card">
  <span class="num">Paper {p['n']}</span>
  <h3>{html.escape(p['short'])}</h3>
  <p>{html.escape(p['blurb'])}</p>
  <div class="spacer"></div>
  <div class="btn-row">
    <a class="btn primary" href="papers/{p['slug']}.html">Read</a>
    <a class="btn" href="papers/{p['slug']}-pdf.html">PDF</a>
    <a class="btn" href="papers/{p['slug']}.pdf" download>Download</a>
  </div>
</div>""" for p in PAPERS)

    n_fig = sum(len(r["figures"]) for r in RECORDS)
    body = f"""
<p class="kicker">Research programme</p>
<h1>Conversion, boundary organization, and the geometry of transitions</h1>
<p class="lede prose">Three papers by João Vitor Perazzolo, and the
pre-registered computational suite that tests them.</p>

<div class="cards">{cards}</div>

<div class="stat-grid">
  <div class="stat"><span class="k">Papers</span><span class="v">3</span></div>
  <div class="stat"><span class="k">Experiments</span><span class="v">{len(RECORDS)}</span></div>
  <div class="stat"><span class="k">Figures</span><span class="v">{n_fig}</span></div>
  <div class="stat"><span class="k">Pre-registrations</span>
    <span class="v">{sum(1 for r in RECORDS if r['prereg'])}</span></div>
</div>

<div class="prose">
{overview}
</div>
"""
    write("index.html", page("Perazzolo — Research Programme", body, depth=0,
                             current="index.html",
                             desc="Three papers on conversion, boundary organization and "
                                  "the geometry of state transitions, with a "
                                  "pre-registered validation suite."))


# --------------------------------------------------------------------------

LINK_RE = re.compile(r'(?:href|src|data)="([^"#][^"]*)"')


def check_links(skip_pdf: bool = False):
    """Every internal link must resolve to a file that exists.

    Cheap to run and catches the failure that matters most here: a PDF that did not
    build leaves a download button pointing at nothing, and a renamed experiment
    leaves the index pointing at a page that is gone. Both look fine in the build log.
    """
    seen = 0
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".html"):
                continue
            page_path = os.path.join(dirpath, name)
            with open(page_path, encoding="utf-8") as fh:
                body = fh.read()
            for target in LINK_RE.findall(body):
                if target.startswith(("http://", "https://", "mailto:", "data:", "//")):
                    continue
                if skip_pdf and target.endswith(".pdf"):
                    continue          # --no-pdf preview: the PDFs were not built
                seen += 1
                resolved = os.path.normpath(
                    os.path.join(dirpath, target.split("#")[0].split("?")[0]))
                if not os.path.exists(resolved):
                    rel = os.path.relpath(page_path, OUT)
                    FAILURES.append(f"broken link in {rel}: {target}")
    print(f"  links: {seen} internal references checked")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true",
                    help="skip the LaTeX pass (HTML preview only)")
    args = ap.parse_args()

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    global RECORDS
    RECORDS = load_results()
    print(f"Building site: {len(RECORDS)} experiments, {len(PAPERS)} papers")

    shutil.copytree(os.path.join(SITE, "assets"), os.path.join(OUT, "assets"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    build_papers(with_pdf=not args.no_pdf)
    build_experiments()
    build_static_pages()
    build_index()

    hdr = os.path.join(OUT, "_header.tex")
    if os.path.exists(hdr):
        os.remove(hdr)

    check_links(skip_pdf=args.no_pdf)

    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"Wrote {n} files to {os.path.relpath(OUT, ROOT)}/")

    if FAILURES:
        print(f"\nBUILD FAILED — {len(FAILURES)} problem(s):", file=sys.stderr)
        for f in FAILURES:
            print(f"  - {f}", file=sys.stderr)
        print("\nThe site was not published. Fix these and re-run; the previously "
              "deployed site stays live in the meantime.", file=sys.stderr)
        return 1
    return 0


RECORDS: list = []
FAILURES: list = []

if __name__ == "__main__":
    sys.exit(main() or 0)
