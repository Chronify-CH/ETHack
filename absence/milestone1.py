"""Milestone 1 runner: extract -> paragraphs -> 8 disclosure items -> silence table.

Per ABSENCE_BRIEF.md Section 13: "10 hand-picked reports from 3 sectors,
hard-coded URLs. Extract -> paragraphs -> 8 disclosure items via entailment ->
print a silence table. No corpus, no database, no peers. Prove the extraction
and entailment work, by eye, on real documents. Report what fraction of items
you got right against a manual read."

Logged deviation from the brief, permanent for this environment (see
absence/data/provenance.json and extract.py's module docstring for detail):
absence/corpus/extract.py segments TinyFish's own extracted text rather than
doing PyMuPDF block extraction on raw PDF bytes.

Detection now uses real BM25 retrieval (rank_bm25) over rechunk()-bounded
paragraphs and real DeBERTa-v3-MNLI entailment scoring -- see entail.py's
module docstring for the two earlier, worse-performing iterations this
replaced and why they were worse, not just "a stub we upgraded".

Run: python -m absence.milestone1
"""

import json
import time

from absence.corpus.extract import rechunk, segment_paragraphs
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
        paragraphs = rechunk(segment_paragraphs(company["text"]))
        print(f"[{company_idx}/{len(companies)}] {company['slug']} — {company['company']} ({company['sector']}, {len(paragraphs)} paragraphs)...", flush=True)
        row = {
            "slug": company["slug"],
            "company": company["company"],
            "report_year": company.get("report_year"),
            "sector": company["sector"],
            "n_paragraphs": len(paragraphs),
            "items": {},
        }
        for item in ITEMS:
            if item.sector_applicability and company["sector"] not in item.sector_applicability:
                row["items"][item.id] = {"applicable": False}
                continue
            t_item_start = time.time()
            found, score, evidence, chunk_idx = detect_item(item, paragraphs)
            row["items"][item.id] = {
                "applicable": True,
                "found": found,
                "score": score,
                # The exact sentence window that scored highest, not a 220-char
                # slice of a ~900-char chunk: this is the auditable unit.
                "evidence": evidence,
                "source_chunk_idx": chunk_idx,
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
