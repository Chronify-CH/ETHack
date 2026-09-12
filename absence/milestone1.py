"""Milestone 1 runner: extract -> paragraphs -> 8 disclosure items -> silence table.

Per ABSENCE_BRIEF.md Section 13: "10 hand-picked reports from 3 sectors,
hard-coded URLs. Extract -> paragraphs -> 8 disclosure items via entailment ->
print a silence table. No corpus, no database, no peers. Prove the extraction
and entailment work, by eye, on real documents. Report what fraction of items
you got right against a manual read."

Two logged deviations from the brief, both required by this environment's
network policy (see absence/data/provenance.json and module docstrings for
detail, not repeated here):
  - absence/corpus/extract.py segments TinyFish's own extracted text rather
    than doing PyMuPDF block extraction on raw PDF bytes.
  - absence/detect/entail.py is a keyword-heuristic stub with the real
    entailment call's signature, not calibrated DeBERTa-v3-MNLI.

Run: python -m absence.milestone1
"""

import json
import sys
import time

from absence.corpus.extract import segment_paragraphs
from absence.detect.entail import detect_item
from absence.detect.items import ITEMS

PROVENANCE_PATH = "absence/data/provenance.json"


def load_companies():
    with open(PROVENANCE_PATH) as f:
        provenance = json.load(f)
    companies = []
    for entry in provenance:
        with open(entry["local_path"]) as f:
            text = f.read()
        companies.append({**entry, "text": text})
    return companies


def run():
    companies = load_companies()
    results = []

    for company_idx, company in enumerate(companies, 1):
        t_company_start = time.time()
        paragraphs = segment_paragraphs(company["text"])
        print(f"[{company_idx}/{len(companies)}] {company['company']} ({company['sector']}, {len(paragraphs)} paragraphs)...", flush=True)
        row = {
            "company": company["company"],
            "sector": company["sector"],
            "n_paragraphs": len(paragraphs),
            "items": {},
        }
        for item in ITEMS:
            if item.sector_applicability and company["sector"] not in item.sector_applicability:
                row["items"][item.id] = {"applicable": False}
                continue
            t_item_start = time.time()
            found, score, best_para = detect_item(item, paragraphs)
            row["items"][item.id] = {
                "applicable": True,
                "found": found,
                "score": score,
                "snippet": (best_para.text[:220] + "...") if best_para else None,
            }
            tag = "FOUND " if found else "absent"
            print(f"    {item.id:32} {tag} {score:.3f}  ({time.time()-t_item_start:.1f}s)", flush=True)
        results.append(row)
        print(f"  -> done in {time.time()-t_company_start:.1f}s", flush=True)

    print_silence_table(results)
    with open("absence/data/milestone1_results.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


def print_silence_table(results):
    item_ids = [item.id for item in ITEMS]
    header = f"{'company':<28} {'sector':<12} {'paras':>6}  " + "  ".join(f"{i[:10]:>10}" for i in item_ids)
    print(header)
    print("-" * len(header))
    for row in results:
        cells = []
        for item_id in item_ids:
            cell = row["items"][item_id]
            if not cell.get("applicable", True):
                cells.append(f"{'n/a':>10}")
            elif cell["found"]:
                cells.append(f"{'FOUND '+str(cell['score']):>10}")
            else:
                cells.append(f"{'absent '+str(cell['score']):>10}")
        print(f"{row['company']:<28} {row['sector']:<12} {row['n_paragraphs']:>6}  " + "  ".join(cells))


if __name__ == "__main__":
    run()
