"""Threshold calibration against hand-verified labels (ABSENCE_BRIEF.md Section 11).

Section 11 asks for a threshold calibrated on hand-labelled item/report pairs,
with per-item precision and recall reported, and items below 0.7 recall dropped
from the scored set. This is a scaled-down version of that: 66 labelled cells
rather than 200, because the labels here are verified by reading the source
documents rather than assigned quickly, and five separate ground-truth errors
in this project came from labelling faster than that (see PER_METRIC.md).

Two things this deliberately does NOT do:

1. It does not report the in-sample optimum as if it were performance. Choosing
   the threshold that maximises accuracy on these cells and then reporting that
   accuracy is circular. The leave-one-out figure below is the honest one: for
   each cell, the threshold is chosen on the other 65 and applied to the held-out
   cell.

2. It does not produce one global threshold and stop. Fault 8 (FAULTS.md) showed
   scores shift when the number of scored premises changes, and per-item score
   distributions differ, so a per-item threshold is reported alongside the global
   one -- with the warning that per-item thresholds fitted on ~10 cells each are
   very weakly determined.

Run: python -m absence.calibrate
"""

import json

LABELS_PATH = "absence/data/labels.json"
RESULTS_PATH = "absence/data/milestone1_results.json"
GRID = [i / 100 for i in range(1, 100)]


def load_cells(results_path: str = RESULTS_PATH):
    """Return [(item_id, company, score, label_bool, shipped_found)] per labelled cell.

    `shipped_found` is the decision the pipeline actually made, which is not
    always `score >= threshold`: items carrying a structural gate
    (`min_anchors_with_figure`) can be scored high and still returned absent.
    The threshold sweep below can only see `score`, so for gated items it
    understates the pipeline -- hence the separate as-shipped table.
    """
    labels = json.load(open(LABELS_PATH))["labels"]
    results = json.load(open(results_path))
    cells = []
    for row in results:
        company_labels = labels.get(row["company"], {})
        for item_id, cell in row["items"].items():
            if not cell.get("applicable"):
                continue
            label = company_labels.get(item_id)
            if label is None:
                continue  # unverified -- excluded, never guessed
            cells.append((item_id, row["company"], cell["score"], bool(label), bool(cell.get("found"))))
    return cells


def metrics_at(cells, threshold: float):
    tp = sum(1 for _, _, s, y, _ in cells if s >= threshold and y)
    fp = sum(1 for _, _, s, y, _ in cells if s >= threshold and not y)
    fn = sum(1 for _, _, s, y, _ in cells if s < threshold and y)
    tn = sum(1 for _, _, s, y, _ in cells if s < threshold and not y)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision,
            "recall": recall, "f1": f1, "accuracy": (tp + tn) / len(cells)}


def best_threshold(cells, objective: str = "f1") -> float:
    """Threshold maximising the objective; ties broken toward the higher cut.

    Ties are broken high because the asymmetry matters for this project: a false
    positive asserts a disclosure exists when it does not, while a false negative
    only fails to credit one. For a ledger whose output is *absence*, however,
    the reverse is true -- a false negative manufactures silence. Both errors are
    costly, so f1 (not accuracy) is the default objective.
    """
    scored = [(metrics_at(cells, t)[objective] or 0.0, t) for t in GRID]
    best = max(s for s, _ in scored)
    return max(t for s, t in scored if s == best)


def leave_one_out(cells) -> dict:
    """Honest out-of-sample estimate: fit the threshold without each cell."""
    correct = 0
    for i in range(len(cells)):
        held_out = cells[i]
        rest = cells[:i] + cells[i + 1:]
        t = best_threshold(rest)
        predicted = held_out[2] >= t
        correct += int(predicted == held_out[3])
    return {"loo_accuracy": correct / len(cells), "n": len(cells)}


def run(results_path: str = RESULTS_PATH):
    cells = load_cells(results_path)
    print(f"Labelled cells: {len(cells)}  (positives: {sum(1 for c in cells if c[3])})\n")

    print("Global threshold sweep:")
    print(f"  {'thresh':>7} {'prec':>6} {'recall':>7} {'f1':>6} {'acc':>6}")
    for t in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        m = metrics_at(cells, t)
        p = f"{m['precision']:.2f}" if m["precision"] is not None else "  -- "
        r = f"{m['recall']:.2f}" if m["recall"] is not None else "  -- "
        print(f"  {t:>7.2f} {p:>6} {r:>7} {m['f1']:>6.2f} {m['accuracy']:>6.2f}")

    t_star = best_threshold(cells)
    m = metrics_at(cells, t_star)
    print(f"\nBest global threshold (max f1): {t_star:.2f}")
    print(f"  in-sample: precision {m['precision']:.2f} recall {m['recall']:.2f} "
          f"f1 {m['f1']:.2f} accuracy {m['accuracy']:.2f}   <-- circular, do not quote")
    loo = leave_one_out(cells)
    print(f"  leave-one-out accuracy: {loo['loo_accuracy']:.2f} (n={loo['n']})   <-- quote this one")

    print("\nPer-item (threshold fitted per item; each fitted on ~10 cells, so weakly determined):")
    print(f"  {'item':32} {'n':>3} {'pos':>4} {'t*':>5} {'prec':>6} {'recall':>7} {'verdict':>10}")
    by_item: dict[str, list] = {}
    for c in cells:
        by_item.setdefault(c[0], []).append(c)
    for item_id, item_cells in sorted(by_item.items()):
        pos = sum(1 for c in item_cells if c[3])
        ti = best_threshold(item_cells)
        mi = metrics_at(item_cells, ti)
        p = f"{mi['precision']:.2f}" if mi["precision"] is not None else "  -- "
        r = f"{mi['recall']:.2f}" if mi["recall"] is not None else "  -- "
        # Section 11: below 0.7 recall the item is dropped from the scored set.
        verdict = "DROP" if (mi["recall"] is None or mi["recall"] < 0.7) else "keep"
        print(f"  {item_id:32} {len(item_cells):>3} {pos:>4} {ti:>5.2f} {p:>6} {r:>7} {verdict:>10}")

    print("\nAs-shipped decisions (what detect_item actually returns, gates included):")
    print(f"  {'item':32} {'n':>3} {'correct':>8} {'acc':>6} {'base':>6}")
    for item_id, item_cells in sorted(by_item.items()):
        correct = sum(1 for _, _, _, y, shipped in item_cells if shipped == y)
        pos = sum(1 for c in item_cells if c[3])
        base = max(pos, len(item_cells) - pos) / len(item_cells)
        acc = correct / len(item_cells)
        note = "  <-- beats base rate" if acc > base else ""
        print(f"  {item_id:32} {len(item_cells):>3} {correct:>8} {acc:>6.2f} {base:>6.2f}{note}")

    print("\nPer-item leave-one-out (the honest version of the threshold table above):")
    print(f"  {'item':32} {'n':>3} {'loo_acc':>8} {'base_rate':>10}")
    for item_id, item_cells in sorted(by_item.items()):
        if len(item_cells) < 3:
            print(f"  {item_id:32} {len(item_cells):>3} {'too few':>8}")
            continue
        pos = sum(1 for c in item_cells if c[3])
        # Base rate = accuracy of always predicting the majority class. A
        # leave-one-out accuracy at or below this means the threshold is
        # carrying no information for this item.
        base = max(pos, len(item_cells) - pos) / len(item_cells)
        loo_i = leave_one_out(item_cells)["loo_accuracy"]
        flag = "  <-- no better than guessing" if loo_i <= base else ""
        print(f"  {item_id:32} {len(item_cells):>3} {loo_i:>8.2f} {base:>10.2f}{flag}")


if __name__ == "__main__":
    run()
