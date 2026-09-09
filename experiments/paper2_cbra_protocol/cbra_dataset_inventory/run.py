"""H4 -- systematic inventory of public datasets against the three CBRA properties.

An inventory, not a simulation: it records each credible public candidate's status on the
three properties dataset_viability_gate defined, plus host reachability, and issues the
pre-registered verdict. See PRE-REGISTRATION.md.

Usage:
    python -m experiments.paper2_cbra_protocol.cbra_dataset_inventory.run
"""
from __future__ import annotations

import json
import os
import subprocess

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "_results",
                           "cbra_dataset_inventory")

# property keys: p1 raw-EEG + concurrent cardiac; p2 I+/I- contrast; p3 MR-length
CANDIDATES = [
    {"dataset": "I-CARE (post-arrest EEG+ECG)", "host": "https://physionet.org",
     "p1_rawEEG_plus_cardiac": True, "p2_Iplus_Iminus": True, "p3_MR_length": True,
     "note": "the only corpus with all three; but the boundary residual is not estimable on it "
             "(B1 = 29% vs 60% bar) -- viable but the signal is not there / is confounded by "
             "sedation-TTM-pressors. Viability is not the blocker here; estimability is."},
    {"dataset": "VitalDB (surgical)", "host": "https://vitaldb.net",
     "p1_rawEEG_plus_cardiac": False, "p2_Iplus_Iminus": False, "p3_MR_length": True,
     "note": "ECG + drug timing + length, but BIS INDEX not raw EEG (fails p1), and essentially "
             "pure I+ (almost all surgical patients recover; fails p2). Confirmed by the Sci Data "
             "descriptor."},
    {"dataset": "MIMIC-III/IV Waveform (ICU)", "host": "https://physionet.org",
     "p1_rawEEG_plus_cardiac": False, "p2_Iplus_Iminus": True, "p3_MR_length": True,
     "note": "ECG + long ICU records + outcome contrast, but no concurrent raw EEG (fails p1)."},
    {"dataset": "Sleep-EDF / SHHS / MASS (sleep)", "host": "https://physionet.org",
     "p1_rawEEG_plus_cardiac": True, "p2_Iplus_Iminus": False, "p3_MR_length": True,
     "note": "raw EEG (+ ECG in SHHS/MASS) and length, but sleep is a reversible I+ transition "
             "with no I- non-recovery contrast (fails p2)."},
    {"dataset": "TUH-EEG / CHB-MIT (seizure)", "host": "https://physionet.org",
     "p1_rawEEG_plus_cardiac": False, "p2_Iplus_Iminus": False, "p3_MR_length": True,
     "note": "raw EEG and length, but typically no concurrent cardiac channel and no I-status "
             "contrast (fails p1 and p2)."},
]
CATALOGS = ["https://github.com/openlists/ElectrophysiologyData",
            "https://github.com/meagmohit/EEG-Datasets"]


def reachable(url):
    try:
        out = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                              "--max-time", "20", url], capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception as e:
        return f"err:{type(e).__name__}"


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("H4 -- CBRA dataset viability inventory\n")
    rows = []
    for c in CANDIDATES:
        code = reachable(c["host"])
        allthree = c["p1_rawEEG_plus_cardiac"] and c["p2_Iplus_Iminus"] and c["p3_MR_length"]
        rows.append({**c, "http": code, "all_three": bool(allthree)})
        print(f"  [{'ALL 3' if allthree else 'fails'}] {c['dataset']:34s} host[{code}] "
              f"p1={int(c['p1_rawEEG_plus_cardiac'])} p2={int(c['p2_Iplus_Iminus'])} "
              f"p3={int(c['p3_MR_length'])}")
    cat_codes = {u: reachable(u) for u in CATALOGS}

    all_three = [r for r in rows if r["all_three"]]
    only_icare = (len(all_three) == 1 and all_three[0]["dataset"].startswith("I-CARE"))
    reach = sum(1 for r in rows if r["http"].startswith(("2", "3")))

    if only_icare:
        verdict = (
            f"POSITIVE ARM NOT EXECUTABLE ON PUBLIC DATA (as of 2026-09) -- the bottleneck is "
            f"data, and the binding constraint is the I+/I- contrast coexisting with raw EEG. Of "
            f"the credible public candidates ({reach}/{len(rows)} hosts reachable, so access is "
            f"not the issue), I-CARE is the ONLY corpus clearing all three properties -- and it "
            f"fails not on viability but on estimability (B1 = 29%). Every other candidate fails a "
            f"specific property: VitalDB gives a BIS index not raw EEG and is essentially pure I+; "
            f"MIMIC has no concurrent EEG; sleep banks have no I- non-recovery contrast; seizure "
            f"banks lack concurrent cardiac and an I-status contrast. So H3's re-test on a cleaner "
            f"cohort has NO public venue: a healthier cohort with a clean consciousness transition "
            f"(surgical emergence) exists in VitalDB but only as BIS and pure-I+, which cannot "
            f"carry the I+/I- dissociation. The positive arm is data-limited, and confirming that "
            f"is Paper 2's honest §14.2 estimability-condition result strengthened, not weakened.")
    elif all_three:
        verdict = ("NEW VENUE FOUND: " + "; ".join(r["dataset"] for r in all_three) +
                   " clears all three properties and becomes H3's target for a pre-registered "
                   "re-test of the positive arm.")
    else:
        verdict = ("NO public dataset clears all three properties, not even I-CARE on this "
                   "reading -- the positive arm is not executable on public data.")

    summary = {
        "experiment": "cbra_dataset_inventory",
        "question": "does any public dataset satisfy all three CBRA properties (venue for H3)?",
        "inventory_date": "2026-09",
        "candidates": rows,
        "catalogs_reachability": cat_codes,
        "hosts_reachable": reach,
        "only_viable_is_icare": bool(only_icare),
        "preregistered_criterion": "all three properties in one public corpus => new venue; else not executable, bottleneck is data",
        "binding_constraint": "raw EEG + concurrent cardiac + I+/I- contrast co-occurring (VitalDB has the clean transition but only BIS + pure-I+)",
        "verdict": verdict,
        "figures": [],
    }
    with open(os.path.join(RESULTS_DIR, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n" + "=" * 72); print(verdict)
    print(f"\nResults in {os.path.relpath(RESULTS_DIR)}"); print("=" * 72)


if __name__ == "__main__":
    main()
