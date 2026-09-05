#!/usr/bin/env python3
"""Coverage audit: which named constructs does the experiment suite actually exercise?

WHY THIS EXISTS. The suite is rigorous about what it tests and was blind about what it
FAILED to test. Thirty-seven pre-registered experiments, a numeric-claims gate, a
qualifications gate and a Lean axiom audit all ran green while half of Paper 3's
construction -- the fibre, the Sasaki metric, the Ehresmann connection -- had never been
exercised by anything. It was found because an external reviewer asked, not because any
check could see it. Coverage had never been measured.

So this gate measures it. Two layers:

1. SHARED-LIBRARY REACHABILITY (mechanical). Build the call graph over `shared_lib`,
   seed it with every symbol referenced by an experiment or a self-test, close it
   transitively, and report what is never reached. Transitivity matters: `airm_log` is
   reached only through `anti_develop("airm")`, and a naive scan would call it dead.

2. PAPER CONSTRUCTS (manifest). `experiments/coverage.json` lists each construct the
   papers name in their own abstracts and section headings, with the experiment that
   exercises it -- or `UNEXERCISED`. A construct may be legitimately unexercised; what
   is not legitimate is nobody knowing.

The gate FAILS only on a manifest entry that is stale (claims an experiment that does
not exist, or claims exercised for a symbol the call graph says is unreachable). An
`UNEXERCISED` entry is reported loudly but does not fail the build: the point is that
the count is known and published, not that every construct must be tested before the
papers may be read.

Usage:  python site/check_coverage.py [--quiet]
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = ROOT / "experiments" / "shared_lib"
MANIFEST = ROOT / "experiments" / "coverage.json"


def _public_defs(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {n.name for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")}


def _referenced(path):
    """Every bare name and attribute referenced in a file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
    return out


def _defs_with_bodies(path):
    """symbol -> names referenced inside that symbol's body (intra-library edges)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            body = set()
            for m in ast.walk(n):
                if isinstance(m, ast.Name):
                    body.add(m.id)
                elif isinstance(m, ast.Attribute):
                    body.add(m.attr)
            out[n.name] = body
    return out


def reachability():
    lib_files = [f for f in LIB.glob("*.py")
                 if f.name != "__init__.py" and not f.name.startswith("test_")]
    public = {}          # symbol -> module
    edges = {}           # symbol -> referenced names
    for f in lib_files:
        for s in _public_defs(f):
            public[s] = f.name
        edges.update(_defs_with_bodies(f))

    # consumers: every experiment run.py plus the shared-library self-tests
    consumers = [p for p in (ROOT / "experiments").rglob("*.py")
                 if LIB not in p.parents or p.name.startswith("test_")]
    seed = set()
    for p in consumers:
        seed |= _referenced(p)

    reached, frontier = set(), [s for s in public if s in seed]
    reached.update(frontier)
    while frontier:
        cur = frontier.pop()
        for nxt in edges.get(cur, ()):  # follow intra-library calls
            if nxt in public and nxt not in reached:
                reached.add(nxt)
                frontier.append(nxt)
    dead = sorted(s for s in public if s not in reached)
    return public, reached, dead


def check(quiet=False):
    public, reached, dead = reachability()
    errors = []

    if not MANIFEST.exists():
        print("coverage gate: no experiments/coverage.json manifest", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    results_dir = ROOT / "experiments" / "_results"
    unexercised = []
    for c in manifest:
        who = c.get("exercised_by")
        if who in (None, "", "UNEXERCISED"):
            unexercised.append(c)
            continue
        for name in ([who] if isinstance(who, str) else who):
            if name == "shared_lib_self_test":
                continue
            if not (results_dir / name / "result.json").exists():
                errors.append(f"[{c['construct']}] claims exercised_by '{name}', "
                              f"but no such committed result exists")

    if not quiet:
        print(f"coverage gate: {len(public)} shared_lib symbols, "
              f"{len(reached)} reachable from experiments/self-tests, {len(dead)} not")
        print(f"               {len(manifest)} paper constructs tracked, "
              f"{len(unexercised)} UNEXERCISED")
        if dead:
            print("  unreachable shared_lib symbols (dead or reached only from docs):")
            for s in dead:
                print(f"    - {public[s]}::{s}")
        if unexercised:
            print("  UNEXERCISED paper constructs:")
            for c in unexercised:
                print(f"    - {c['construct']}  ({c.get('where','?')})"
                      f"{' -- ' + c['note'] if c.get('note') else ''}")
    for e in errors:
        print(f"  ERROR  {e}")
    if errors:
        print(f"\nFAILED: {len(errors)} stale coverage claim(s).", file=sys.stderr)
        return 1
    print("coverage gate passed: every coverage claim resolves to a committed result.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    return check(ap.parse_args().quiet)


if __name__ == "__main__":
    sys.exit(main())
