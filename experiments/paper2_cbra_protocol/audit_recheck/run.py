"""E2.4 -- re-check the dataset audit's P1 column against the files (Paper 2, §2.6).

See PRE-REGISTRATION.md. CHB-MIT: first 30 EDF files in RECORDS, header only (HTTP range), count
files with an ECG/EKG channel label. TUH EEG: not checked (access requires an application).
VitalDB: open track list, count cases with raw EEG waveform tracks.

Usage:
    python -m experiments.paper2_cbra_protocol.audit_recheck.run
"""
from __future__ import annotations

import csv
import io
import json
import os
import time
import urllib.request

HERE = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(HERE, "..", "..", "_results", "audit_recheck")
CHB = "https://physionet.org/files/chbmit/1.0.0/"
N_FILES = 30


def get(url, headers=None, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")


def edf_labels(url):
    head = get(url, {"Range": "bytes=0-255"})
    ns = int(head[252:256].decode().strip())
    labels = get(url, {"Range": f"bytes=256-{256 + 16 * ns - 1}"})
    return [labels[i * 16:(i + 1) * 16].decode(errors="replace").strip() for i in range(ns)]


def chbmit():
    recs = [l.strip() for l in get(CHB + "RECORDS").decode().split("\n") if l.strip().endswith(".edf")][:N_FILES]
    rows = []
    for r in recs:
        labs = edf_labels(CHB + r)
        card = [l for l in labs if "ECG" in l.upper() or "EKG" in l.upper()]
        rows.append({"file": r, "n_signals": len(labs), "cardiac_labels": card, "has_cardiac": bool(card)})
        print(f"  {r}: {len(labs)} signals; cardiac {card}", flush=True)
    return rows


def vitaldb():
    try:
        raw = get("https://api.vitaldb.net/trks")
    except Exception as e:
        return {"done": False, "reason": str(e)[:200]}
    try:
        import gzip
        raw = gzip.decompress(raw)
    except Exception:
        pass
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    names = sorted({r["tname"] for r in rows})
    eeg = [n for n in names if "EEG" in n.upper()]
    cases = {}
    for r in rows:
        if r["tname"] in eeg:
            cases.setdefault(r["tname"], set()).add(r["caseid"])
    all_cases = len({r["caseid"] for r in rows})
    any_eeg = len(set().union(*cases.values())) if cases else 0
    return {"done": True, "n_cases_total": all_cases, "eeg_track_names": eeg,
            "cases_per_eeg_track": {k: len(v) for k, v in cases.items()}, "cases_with_any_eeg_track": any_eeg}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    chb = chbmit()
    n_card = sum(r["has_cardiac"] for r in chb)
    patients = sorted({r["file"].split("/")[0] for r in chb})
    pats_card = sorted({r["file"].split("/")[0] for r in chb if r["has_cardiac"]})
    vdb = vitaldb()
    vtxt = (f"VitalDB: {vdb['cases_with_any_eeg_track']} of {vdb['n_cases_total']} cases have a track named EEG "
            f"({', '.join(vdb['eeg_track_names'])})." if vdb.get("done") else f"VitalDB: not done ({vdb.get('reason')}).")
    verdict = (f"CHB-MIT: {n_card}/{len(chb)} of the first EDF files carry an ECG/EKG channel "
               f"(patients {', '.join(pats_card) if pats_card else 'none'} of {', '.join(patients)}). "
               f"TUH EEG: not checked (access requires an application). {vtxt} "
               f"None of these corpora has a recovery/non-recovery contrast; this only corrects Table 1's P1 column.")
    print("\n" + verdict)
    json.dump({"experiment": "audit_recheck", "plan_id": "E2.4", "fills": "R2.4",
               "question": "Do CHB-MIT files carry an ECG channel, and does VitalDB carry raw EEG tracks?",
               "chbmit": {"n_files": len(chb), "n_with_cardiac": n_card, "patients_with_cardiac": pats_card,
                          "per_file": chb},
               "tuh": {"done": False, "reason": "access requires an application"}, "vitaldb": vdb,
               "verdict": verdict},
              open(os.path.join(RESULTS_DIR, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
