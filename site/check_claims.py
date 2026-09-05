#!/usr/bin/env python3
"""Verify the papers' headline numbers against the committed results.

The repository's most frequent failure mode is not a broken formula or a broken proof
-- the latex and lean gates already catch those -- but PROSE THAT MISDESCRIBES A NUMBER:
a sentence that says 0.71 while `result.json` says 0.81, or a claim left in a paper
after the run that produced it changed. Nothing checked that automatically, and every
end-to-end review has had to do it by hand. This gate does it in CI.

It is manifest-driven rather than NLP. `experiments/claims.json` lists each headline
claim as:

    {
      "id":      "detection repair AUC",
      "result":  "detection_statistic_repair",         # _results/<result>/result.json
      "path":    "variants.a_scale_normalised.detection_auc",  # dotted, list indices ok
      "tol":     0.01,
      "papers":  {"Paper3.md": "lifts detection to AUC \\$\\\\mathbf\\{([0-9.]+)\\}\\$"}
    }

For each claim the gate:
  1. reads the ACTUAL value from result.json at `path`;
  2. for every paper listed, finds `pattern`, extracts its numeric capture group, and
     confirms the number the PAPER states is within `tol` of the actual value.

So a paper number that drifts from the result, or a claim whose sentence has been
edited away, fails the build. The manifest cannot drift from the results either: its
job is only to say WHERE each number lives, and the value is always read live.

Coverage is the manifest's honest limit: a number nobody tagged is not checked. The
gate therefore also prints how many committed result.json files have at least one
tagged claim, so the coverage gap is visible rather than hidden.

Usage:
    python site/check_claims.py [--quiet]
Exit status is non-zero if any tagged claim fails.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "experiments", "_results")
MANIFEST = os.path.join(ROOT, "experiments", "claims.json")
QUALIFICATIONS = os.path.join(ROOT, "experiments", "qualifications.json")
VERDICT_GUARDS = os.path.join(ROOT, "experiments", "verdict_guards.json")


def dotted(obj, path):
    """Traverse a nested dict/list by a dotted path; integer segments index lists."""
    cur = obj
    for seg in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(seg)]
        else:
            cur = cur[seg]
    return cur


def load_result(name):
    with open(os.path.join(RESULTS, name, "result.json"), encoding="utf-8") as fh:
        return json.load(fh)



def check_qualifications(quiet=False):
    """The numbers gate applied to CLAIMS.

    A number can match its result.json and still mislead, if the sentence quoting it has
    been separated from the qualification that makes it honest -- a pre-registered arm
    that did not replicate, a margin inside binomial noise, a threshold missed. That is
    the divergence risk between a repository that reports fully and a manuscript written
    to pass review, and it is the one failure mode the numeric gate cannot see.

    Each entry names a `claim` regex and a `requires` regex that must appear in the SAME
    PARAGRAPH of the same paper. If the claim is present without its qualification, the
    build fails.
    """
    if not os.path.exists(QUALIFICATIONS):
        return 0, []
    with open(QUALIFICATIONS, encoding="utf-8") as fh:
        quals = json.load(fh)
    errors, checked = [], 0
    for q in quals:
        path = os.path.join(ROOT, q["paper"])
        with open(path, encoding="utf-8") as fh:
            paragraphs = fh.read().split("\n\n")
        hits = [p for p in paragraphs if re.search(q["claim"], p)]
        if not hits:
            errors.append(f"[{q['id']}] claim pattern not found in {q['paper']} -- "
                          f"the sentence it guards was edited away or reworded")
            continue
        for para in hits:
            checked += 1
            if not re.search(q["requires"], para):
                errors.append(
                    f"[{q['id']}] {q['paper']}: the claim appears WITHOUT its required "
                    f"qualification (/{q['requires']}/). {q['why']}")
    if not quiet or errors:
        print(f"qualifications gate: {len(quals)} guarded claims, {checked} paragraph checks")
    return checked, errors



def check_verdict_guards(quiet=False):
    """The qualifications idea applied to the most citable artifact: verdict strings.

    A result.json verdict is what the site's index renders and what a reader copies. The
    index compresses it, and compression is where a qualification gets lost: the
    repository's most contested experiment led with "THE GEODESIC DETECTOR WINS ON THE
    REAL TASK" while the caveats sat two sentences further down, outside the compression
    window. That is a headline claim travelling without its qualification -- inside the
    tool built to prevent it.

    This replicates the site's compression and requires the declared qualification to
    survive it. Supersessions are checked too: a superseded result must name a target
    that actually exists.
    """
    if not os.path.exists(VERDICT_GUARDS):
        return 0, []
    with open(VERDICT_GUARDS, encoding="utf-8") as fh:
        cfg = json.load(fh)
    errors, checked = [], 0

    for g in cfg.get("guards", []):
        rj = os.path.join(RESULTS, g["result"], "result.json")
        if not os.path.exists(rj):
            errors.append(f"[verdict guard {g['result']}] no such committed result")
            continue
        with open(rj, encoding="utf-8") as fh:
            data = json.load(fh)
        verdict = data.get("verdict") or data.get("outcome") or ""
        sents = re.split(r"(?<=[.!?])\s+", str(verdict).strip())
        out, pat = sents[0], re.compile(g["must_include"], re.I)
        if not pat.search(out):
            for nxt in sents[1:]:
                out = out + " " + nxt
                if pat.search(out) or len(out) > 700:
                    break
        checked += 1
        if not pat.search(out):
            errors.append(
                f"[verdict guard {g['result']}] the rendered headline does not reach its "
                f"qualification (/{g['must_include']}/) within the compression window. "
                f"{g['why']}")

    for sp in cfg.get("supersessions", []):
        for key in ("result", "superseded_by"):
            slug = sp[key]
            if not os.path.exists(os.path.join(RESULTS, slug, "result.json")):
                errors.append(f"[supersession {sp['result']}] '{slug}' is not a committed result")
        checked += 1

    if not quiet or errors:
        print(f"verdict-guard gate: {len(cfg.get('guards', []))} guarded verdicts, "
              f"{len(cfg.get('supersessions', []))} supersessions, {checked} checks")
    return checked, errors


def check(quiet=False):
    with open(MANIFEST, encoding="utf-8") as fh:
        claims = json.load(fh)

    paper_text = {}
    def text(paper):
        if paper not in paper_text:
            with open(os.path.join(ROOT, paper), encoding="utf-8") as fh:
                paper_text[paper] = fh.read()
        return paper_text[paper]

    errors, checked = [], 0
    tagged_results = set()

    for c in claims:
        cid = c["id"]
        try:
            actual = float(dotted(load_result(c["result"]), c["path"]))
        except (KeyError, IndexError, FileNotFoundError, ValueError, TypeError) as e:
            errors.append(f"[{cid}] cannot read {c['result']}:{c['path']} — {e!r}")
            continue
        tagged_results.add(c["result"])
        tol = float(c.get("tol", 0.005))
        scale = float(c.get("scale", 1.0))   # e.g. 100 when the paper states a percent
        actual *= scale

        for paper, pattern in c["papers"].items():
            body = text(paper)
            matches = re.findall(pattern, body)
            if not matches:
                errors.append(f"[{cid}] pattern not found in {paper} — the claim's "
                              f"sentence may have been edited away: /{pattern}/")
                continue
            for m in matches:
                grp = m if isinstance(m, str) else m[0]
                try:
                    stated = float(grp)
                except ValueError:
                    errors.append(f"[{cid}] {paper}: capture {grp!r} is not a number")
                    continue
                checked += 1
                if abs(stated - actual) > tol:
                    errors.append(
                        f"[{cid}] {paper} states {stated} but "
                        f"{c['result']}:{c['path']} = {actual:.6g} (tol {tol})")

    n_results = len([d for d in os.listdir(RESULTS)
                     if os.path.exists(os.path.join(RESULTS, d, "result.json"))])
    if not quiet or errors:
        print(f"claims gate: {len(claims)} claims, {checked} paper-number checks, "
              f"{len(tagged_results)}/{n_results} result files have a tagged claim")
    _, qerrors = check_qualifications(quiet)
    _, verrors = check_verdict_guards(quiet)
    qerrors = qerrors + verrors
    for e in errors:
        print(f"  ERROR  {e}")
    for e in qerrors:
        print(f"  ERROR  {e}")
    if errors or qerrors:
        if errors:
            print(f"\nFAILED: {len(errors)} numeric claim(s) do not match the committed "
                  f"results.", file=sys.stderr)
        if qerrors:
            print(f"FAILED: {len(qerrors)} claim(s) appear without the qualification that "
                  f"makes them honest.", file=sys.stderr)
        return 1
    print("claims gate passed: every tagged paper number matches its result.json, and "
          "every guarded claim carries its qualification.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    return check(args.quiet)


if __name__ == "__main__":
    sys.exit(main())
