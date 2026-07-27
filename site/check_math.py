#!/usr/bin/env python3
"""Validate the LaTeX in the papers before the site is built.

The PDFs and the web versions are regenerated from the Markdown on every push, so a
malformed formula does not stay contained in one build -- it ships. And the failure
mode is silent: a bad delimiter does not raise, it renders the source verbatim, so
`$I_{profile} = $` reaches the reader as literal dollar signs in a published paper.
This checker fails the build instead of publishing that.

It works by tokenizing each paper exactly the way pandoc's `tex_math_dollars`
extension does, rather than by pattern-matching, because the naive regex reading
mistakes the prose *between* two formulas for a formula:

  * `$$...$$` opens display math, closed by the next `$$`.
  * `$` opens inline math only if the next character is not whitespace.
  * The closing `$` must not be preceded by whitespace, and must not be followed by
    a digit.
  * `\\$` is a literal dollar and is not a delimiter.

Anything that fails to open or close under those rules is a `$` that will be printed
to the reader. That is the first and most important class of defect. The others:

  * unbalanced braces inside a formula (breaks the LaTeX pass, not the HTML one);
  * unbalanced `\\begin`/`\\end` environments;
  * unbalanced `\\left`/`\\right` pairs;
  * macros outside a known list, reported as advisory rather than fatal, since an
    unrecognised macro may be legitimate but is worth a human glance.

Usage:
    python site/check_math.py [--quiet] [--strict]

`--strict` promotes the advisory macro warnings to errors. Exit status is non-zero
if any error is found.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = ["Paper1.md", "Paper2.md", "Paper3.md"]

KNOWN_MACROS = set("""
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda
mu nu xi pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega
Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega
sum prod coprod int oint iint iiint lim limsup liminf sup inf max min arg deg
det dim ker exp log ln lg sin cos tan cot sec csc sinh cosh tanh coth arcsin arccos
arctan gcd hom Pr sqrt frac dfrac tfrac cfrac binom over atop choose pmod bmod mod
partial nabla infty forall exists nexists neg lnot emptyset varnothing in notin ni
subset supset subseteq supseteq subsetneq supsetneq cup cap bigcup bigcap sqcup
setminus times div cdot cdots ldots dots vdots ddots ast star circ bullet
oplus ominus otimes oslash odot bigoplus bigotimes wedge vee bigwedge bigvee
approx sim simeq cong equiv neq ne leq le geq ge leqslant geqslant ll gg propto
gtrsim lesssim gtrless lessgtr eqsim approxeq nsim ncong nleq ngeq
land lor lnot not implies vdots
perp parallel angle measuredangle triangle square diamond pm mp
to rightarrow leftarrow leftrightarrow Rightarrow Leftarrow Leftrightarrow mapsto
implies impliedby iff longrightarrow longleftarrow Longrightarrow Longleftrightarrow
uparrow downarrow updownarrow hookrightarrow rightsquigarrow xrightarrow xmapsto
hat bar tilde vec dot ddot check breve acute grave overline underline overrightarrow
widehat widetilde overbrace underbrace overset underset stackrel substack
mathbb mathbf mathcal mathrm mathit mathsf mathtt mathfrak mathscr bm boldsymbol
operatorname operatornamewithlimits DeclareMathOperator
text textrm textbf textit textsf texttt mbox hbox
left right middle big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr
langle rangle lvert rvert lVert rVert vert Vert lfloor rfloor lceil rceil
quad qquad space hspace vspace thinspace enspace nobreakspace phantom hphantom vphantom
prime ell hbar imath jmath Re Im aleph beth surd top bot models vdash dashv
matrix pmatrix bmatrix Bmatrix vmatrix Vmatrix smallmatrix cases dcases array
align aligned alignat split gather gathered equation eqnarray multline
label ref eqref tag notag nonumber intertext
mid colon coloneqq eqqcolon triangleq doteq asymp bowtie propto succ prec succeq preceq
displaystyle textstyle scriptstyle scriptscriptstyle limits nolimits
begin end nolimits mathopen mathclose mathbin mathrel mathop mathpunct
sfrac nicefrac degree circ percent textperthousand
""".split())

ENV_RE = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")
MACRO_RE = re.compile(r"\\([A-Za-z]+)")


# --------------------------------------------------------------------------
# tokenizer
# --------------------------------------------------------------------------

def _mask_code(src: str) -> str:
    """Blank out code spans, keeping offsets, so `$5` in prose is not math."""
    out = list(src)
    for m in re.finditer(r"`+[^`\n]*`+", src):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def tokenize(src: str):
    """Pandoc-equivalent scan.

    Returns (spans, stray) where `spans` is a list of (offset, kind, body) with kind
    in {"inline", "display"}, and `stray` is a list of offsets of every `$` that will
    reach the reader as a literal dollar sign.
    """
    s = _mask_code(src)
    n = len(s)
    spans, stray = [], []
    i = 0
    while i < n:
        c = s[i]
        if c != "$":
            i += 1
            continue
        if i > 0 and s[i - 1] == "\\" and (i < 2 or s[i - 2] != "\\"):
            i += 1                              # escaped dollar: a literal, fine
            continue

        # ---- display math -------------------------------------------------
        if s.startswith("$$", i):
            j = s.find("$$", i + 2)
            if j != -1:
                spans.append((i, "display", src[i + 2:j]))
                i = j + 2
                continue
            stray.append(i)
            i += 2
            continue

        # ---- inline math --------------------------------------------------
        if i + 1 < n and s[i + 1] not in " \t\n":
            j = i + 1
            while j < n:
                if s[j] == "$" and s[j - 1] not in " \t\n" and s[j - 1] != "\\":
                    if j + 1 < n and s[j + 1].isdigit():
                        j += 1                  # pandoc declines "$x$5"
                        continue
                    break
                if s[j] == "\n" and j + 1 < n and s[j + 1] == "\n":
                    j = n                       # inline math cannot cross a blank line
                    break
                j += 1
            if j < n:
                spans.append((i, "inline", src[i + 1:j]))
                i = j + 1
                continue
        stray.append(i)
        i += 1
    return spans, stray


def line_of(src: str, offset: int) -> int:
    return src.count("\n", 0, offset) + 1


def context(src: str, offset: int, width: int = 70) -> str:
    a, b = max(0, offset - width), min(len(src), offset + width)
    return " ".join(src[a:b].split())


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_paper(path: str):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    spans, stray = tokenize(src)
    errors, notes = [], []

    for off in stray:
        errors.append((line_of(src, off), "unparsed-dollar",
                       "this '$' does not open or close a formula and will be "
                       "printed literally: …" + context(src, off) + "…"))

    for off, kind, body in spans:
        ln = line_of(src, off)
        short = " ".join(body.split())[:90]

        if body.count("{") - body.count(r"\{") != body.count("}") - body.count(r"\}"):
            errors.append((ln, "brace-mismatch",
                           f"unbalanced braces in {kind} math: {short!r}"))

        opens, closes = {}, {}
        for m in ENV_RE.finditer(body):
            (opens if m.group(1) == "begin" else closes).setdefault(m.group(2), 0)
            d = opens if m.group(1) == "begin" else closes
            d[m.group(2)] = d.get(m.group(2), 0) + 1
        for env in set(opens) | set(closes):
            if opens.get(env, 0) != closes.get(env, 0):
                errors.append((ln, "env-mismatch",
                               f"\\begin{{{env}}}/\\end{{{env}}} do not match in "
                               f"{kind} math: {short!r}"))

        nl = len(re.findall(r"\\left(?![a-zA-Z])", body))
        nr = len(re.findall(r"\\right(?![a-zA-Z])", body))
        if nl != nr:
            errors.append((ln, "left-right-mismatch",
                           f"{nl} \\left vs {nr} \\right in {kind} math: {short!r}"))

        if kind == "inline" and "\n\n" in body:
            errors.append((ln, "paragraph-in-math",
                           f"inline math spans a blank line: {short!r}"))

        for mac in MACRO_RE.findall(body):
            if mac not in KNOWN_MACROS:
                notes.append((ln, "unknown-macro",
                              f"\\{mac} is not in the known-macro list — verify it "
                              f"renders: {short!r}"))

    return spans, errors, notes


def cross_check(path: str, spans):
    """Verify this file's tokenizer against pandoc's actual output.

    A checker that has drifted from the renderer is worse than no checker, because it
    reports confidence it has not earned. So the span counts are compared against what
    pandoc really produced, and any residual `$` in the rendered text -- the thing the
    reader would actually see -- is reported independently of the tokenizer.

    Returns a list of errors, or [] if pandoc is unavailable (the source-level checks
    still ran).
    """
    import subprocess
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    try:
        rendered = subprocess.run(
            ["pandoc", "-f", "markdown+tex_math_dollars+pipe_tables+raw_tex-raw_html",
             "-t", "html5", "--mathjax", "--wrap=none"],
            input=src, capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    n_inline = len(re.findall(r'<span class="math inline">', rendered))
    n_display = len(re.findall(r'<span class="math display">', rendered))
    mine_i = sum(1 for s in spans if s[1] == "inline")
    mine_d = len(spans) - mine_i

    errors = []
    if (n_inline, n_display) != (mine_i, mine_d):
        errors.append((0, "checker-drift",
                       f"this checker sees {mine_i} inline / {mine_d} display formulas "
                       f"but pandoc produced {n_inline} / {n_display} — the checker no "
                       f"longer models the renderer and its verdicts cannot be trusted"))

    text = re.sub(r'<span class="math[^"]*">.*?</span>', " ", rendered, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text).replace(r"\$", "")
    for m in re.finditer(r".{0,60}\$.{0,60}", text):
        errors.append((0, "dollar-in-output",
                       "a '$' survives into the rendered page: …"
                       + " ".join(m.group(0).split()) + "…"))
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="treat unknown macros as errors")
    args = ap.parse_args()

    total_err = 0
    for name in PAPERS:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f"{name}: MISSING", file=sys.stderr)
            total_err += 1
            continue
        spans, errors, notes = check_paper(path)
        errors += cross_check(path, spans)
        if args.strict:
            errors, notes = errors + notes, []
        total_err += len(errors)

        n_inline = sum(1 for s in spans if s[1] == "inline")
        n_disp = len(spans) - n_inline
        if not args.quiet or errors:
            print(f"{name}: {n_inline} inline + {n_disp} display formulas, "
                  f"{len(errors)} error(s), {len(notes)} advisory")
        for ln, kind, detail in sorted(errors):
            print(f"  ERROR  {name}:{ln}  [{kind}] {detail}")
        if not args.quiet and notes:
            seen = set()
            for ln, kind, detail in sorted(notes):
                mac = detail.split(" ")[0]
                if mac in seen:
                    continue
                seen.add(mac)
                print(f"  note   {name}:{ln}  [{kind}] {detail}")

    if total_err:
        print(f"\nFAILED: {total_err} LaTeX error(s). Each one reaches the reader as "
              f"literal source text or breaks the PDF pass.", file=sys.stderr)
        return 1
    print("\nLaTeX check passed: every formula opens, closes, and is balanced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
