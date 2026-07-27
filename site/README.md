# The published site

The site at **https://fcadusims-droid.github.io/academic-jvp-work-/** is generated
from this repository. Nothing in it is hand-maintained HTML, and no build output is
committed — editing a paper or adding an experiment is all that is required to change
what the site shows.

## What generates what

| Site page | Generated from |
|---|---|
| `index.html` | `site/content/overview.md` + counts read from the results |
| `papers/paper-N.html` | `PaperN.md`, rendered with a section index |
| `papers/paper-N.pdf` | `PaperN.md`, typeset with XeLaTeX |
| `papers/paper-N-pdf.html` | a browser PDF viewer around the same file |
| the "at a glance" panel on each paper | `site/content/paperN.md` |
| `experiments/index.html` | every `experiments/_results/*/result.json` |
| `experiments/<slug>.html` | that experiment's `PRE-REGISTRATION.md`, its `result.json`, its figures, and its row in `experiments/STATUS.md` |
| `methodology.html` | `METHODOLOGY.md` |
| `data.html` | `site/content/data.md` + `experiments/paper3_geodesic_kinematics/DATA.md` |
| `formal.html` | `formal/README.md` |
| `reproduce.html` | `site/content/reproduce.md` |

A new experiment appears on the site as soon as its `result.json` is committed. No
list anywhere needs updating.

## How the mathematics is rendered

**MathML, generated at build time — not a client-side TeX renderer.** The obvious
choice is MathJax from a CDN, and it was the first thing tried. It fails badly: when
the CDN is unreachable, MathJax does not degrade, it simply never runs, and the
reader is shown the raw source — `\(D_{ag}\to 0\)` — in what is presented as a
published paper. That was verified, not assumed: with the CDN blocked, every formula
on the paper pages appeared as literal TeX.

Pandoc's `--mathml` converts the formulas during the build instead. Current browsers
render MathML natively, so the mathematics needs no JavaScript, no third-party host,
and no network at all. It is also selectable, searchable and accessible to screen
readers, which client-side rendering makes harder.

The one cosmetic cost: Chromium spaces fence characters more loosely than TeX does,
so `C_f(t)` reads slightly airier than it would in a journal. The markup is
semantically exact and there is no CSS fix — the spacing comes from the browser's
operator dictionary — so it is accepted rather than papered over.

## Why the build is gated

The PDFs are **regenerated on every push**, not stored. That is what keeps them in
step with the Markdown, and it is also why each push is a fresh opportunity for LaTeX
to produce something wrong. The failure is quiet: a malformed delimiter does not
raise an error, it prints the source verbatim, so `$x = $` reaches the reader as
literal dollar signs in a published paper.

Three gates run before anything is deployed, and a failure at any of them leaves the
previously published site live rather than replacing it with a damaged one.

**1. `site/check_math.py`, before the build.** Tokenizes each paper the way pandoc's
`tex_math_dollars` extension does — `$` opens math only if the next character is not
whitespace; the closing `$` must not be preceded by whitespace or followed by a
digit — and reports every `$` that will reach the reader as a literal. It also checks
brace balance, `\begin`/`\end` pairing and `\left`/`\right` pairing inside every
formula, and flags macros outside a known list as advisory.

Crucially it then **verifies itself against pandoc**: if its own span count disagrees
with what pandoc actually produced, it fails, because a checker that has drifted from
the renderer reports confidence it has not earned. It also greps the rendered output
directly for surviving `$`, which catches defects the tokenizer alone would miss.

**2. PDF verification, after typesetting.** Each PDF is checked for size, for a
plausible page count (a truncated LaTeX run produces a short but valid PDF), for any
literal `$` reaching the page, and for unresolved reference markers.

**3. Link checking, before publish.** Every internal `href`, `src` and `data`
attribute in the generated HTML must resolve to a file that exists — which is what
catches a PDF that failed to build leaving a download button pointing at nothing.

## Building locally

```bash
sudo apt-get install -y pandoc texlive-xetex texlive-latex-recommended \
                        texlive-fonts-recommended lmodern poppler-utils
python site/check_math.py
python site/build.py            # writes _site/
python -m http.server -d _site  # then open http://localhost:8000
```

`python site/build.py --no-pdf` skips the LaTeX pass for a fast HTML preview; the PDF
links are then not checked, because the files were not built.

## Deployment

`.github/workflows/pages.yml` runs on every push to `main` and on manual dispatch.
`site/check_math.py` additionally runs on pull requests via `tests.yml`, so a broken
formula is caught before it can reach `main` at all.
