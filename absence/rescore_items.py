"""Re-score selected items across the corpus and merge into the results file.

A full milestone1 run takes ~78 minutes on this machine. When only an item's
hypothesis or anchors change, re-scoring the other six items is wasted work and
would also silently re-time-stamp results that did not change. This re-scores
exactly the named items, leaves every other cell byte-identical, and records
which items were re-scored so nobody has to guess later which numbers came from
which item definition.

Run: python -m absence.rescore_items scenario_analysis_quantified scope3_category_breakdown
"""

import json
import sys
import time

from absence.corpus.extract import rechunk, segment_paragraphs
from absence.detect.entail import detect_item
from absence.detect.items import ITEMS_BY_ID

RESULTS_PATH = "absence/data/milestone1_results.json"
PROVENANCE_PATH = "absence/data/provenance.json"


def run(item_ids: list[str]) -> None:
    for item_id in item_ids:
        if item_id not in ITEMS_BY_ID:
            raise KeyError(f"unknown item: {item_id}")

    provenance = {p["company"]: p for p in json.load(open(PROVENANCE_PATH))}
    results = json.load(open(RESULTS_PATH))

    for row in results:
        entry = provenance[row["company"]]
        paragraphs = rechunk(segment_paragraphs(open(entry["local_path"]).read()))
        print(f"[{row['company']}] {len(paragraphs)} chunks", flush=True)
        for item_id in item_ids:
            item = ITEMS_BY_ID[item_id]
            cell = row["items"].get(item_id)
            if cell is None or not cell.get("applicable"):
                continue
            before = cell["score"]
            t0 = time.time()
            found, score, evidence, chunk_idx = detect_item(item, paragraphs)
            cell.update({
                "found": found,
                "score": score,
                "evidence": evidence,
                "source_chunk_idx": chunk_idx,
                "rescored": True,
            })
            arrow = "->" if abs(score - before) > 0.001 else "=="
            print(f"    {item_id:32} {before:.3f} {arrow} {score:.3f} "
                  f"{'FOUND' if found else 'absent'} ({time.time() - t0:.0f}s)", flush=True)

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nmerged into {RESULTS_PATH}; re-scored items: {', '.join(item_ids)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    run(sys.argv[1:])
