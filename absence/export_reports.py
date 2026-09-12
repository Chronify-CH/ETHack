"""Write one folder per analysed report: the source text and its audit trail.

Each folder under absence/reports/<slug>/ holds the exact document the pipeline
read (source.txt, hash-verified against absence/data/provenance.json) next to
analysis.md, which records for every disclosure item the score, the calibrated
threshold, any structural gate, the pipeline's decision, the hand-verified
label, and the evidence span the score came from. Keeping the two together is
the point: every claim in analysis.md can be checked against the text sitting
beside it.

Two constraints from ABSENCE_BRIEF.md are enforced in the wording here:

  Section 12 -- no intent language. A cell the pipeline did not fire on is
  written "not detected", never "not disclosed", "omitted" or "concealed".
  "Not detected" is a statement about this detector on this document; it is not
  a statement about the company. The two are different claims and four of the
  eight items are not reliable enough to support the second one.

  Section 11 -- unvalidated items may not feed aggregates. Items carrying
  scored=False appear in full but are marked EXCLUDED with their reason, and
  the agreement counts at the top of each file are computed over scored items
  only.

Regenerate after any re-run: python -m absence.export_reports
"""

import json
import pathlib

from absence.detect.items import ITEMS, ITEMS_BY_ID

PROVENANCE_PATH = "absence/data/provenance.json"
RESULTS_PATH = "absence/data/milestone1_results.json"
LABELS_PATH = "absence/data/labels.json"
REPORTS_DIR = pathlib.Path("absence/reports")


def _decision(cell) -> str:
    return "detected" if cell.get("found") else "not detected"


def _label_text(label) -> str:
    if label is None:
        return "unverified"
    return "present" if label else "not present"


def _agreement(cell, label) -> str:
    if label is None:
        return "—"
    return "agrees" if bool(cell.get("found")) == bool(label) else "DISAGREES"


def _evidence_block(cell) -> str:
    evidence = (cell.get("evidence") or "").strip()
    if not evidence:
        return "_No candidate span was retrieved._"
    return "> " + evidence.replace("\n", " ")


def render(entry: dict, row: dict, labels: dict) -> str:
    lines: list[str] = []
    a = lines.append

    a(f"# {entry['company']} — disclosure audit")
    a("")
    a(f"- **Sector (as used in this corpus):** {entry['sector']}")
    a(f"- **Source document:** {entry['source_url']}")
    if entry.get("final_url") and entry["final_url"] != entry["source_url"]:
        a(f"- **Resolved to:** `{entry['final_url']}`")
    a(f"- **Retrieved:** {entry['retrieved_at']} via {entry['retrieved_via']}")
    a(f"- **Extracted text:** {entry['extracted_text_chars']:,} chars, "
      f"sha256 `{entry['extracted_text_sha256']}`")
    a(f"- **Local copy:** `{entry['local_path']}` (the exact bytes scored below)")
    a(f"- **Paragraph chunks after rechunk():** {row['n_paragraphs']}")
    a("")

    scored_cells = [
        (i, row["items"][i.id], labels.get(i.id))
        for i in ITEMS
        if i.scored and row["items"].get(i.id, {}).get("applicable")
    ]
    checkable = [(i, c, l) for i, c, l in scored_cells if l is not None]
    if checkable:
        agree = sum(1 for _, c, l in checkable if bool(c.get("found")) == bool(l))
        a(f"**Agreement with the hand read: {agree}/{len(checkable)} scored items** "
          f"({len(checkable)} of this document's cells are both validated and hand-labelled; "
          "the rest are excluded or unverified and are listed but not counted).")
    else:
        a("**Agreement with the hand read: no scored, hand-labelled cells for this document.**")
    a("")

    a("| item | pillar | score | threshold | gate | decision | hand read | |")
    a("|---|---|---:|---:|---:|---|---|---|")
    for item in ITEMS:
        cell = row["items"].get(item.id, {})
        if not cell.get("applicable"):
            a(f"| `{item.id}` | {item.pillar} | — | — | — | n/a (not material for {entry['sector']}) | — | |")
            continue
        label = labels.get(item.id)
        gate = str(item.min_anchors_with_figure) if item.min_anchors_with_figure else "—"
        mark = "" if item.scored else " *(excluded)*"
        a(f"| `{item.id}`{mark} | {item.pillar} | {cell['score']:.3f} | "
          f"{item.calibrated_threshold:.2f} | {gate} | {_decision(cell)} | "
          f"{_label_text(label)} | {_agreement(cell, label)} |")
    a("")
    a("`score` is P(entailment) from the highest-scoring sentence window in the top-8 "
      "BM25 chunks. `gate` is the minimum number of distinct anchor terms that must "
      "appear next to a figure before the item can fire, which can override a score "
      "above threshold. Items marked *(excluded)* failed validation and may not feed "
      "any aggregate — their rows are shown so the evidence stays auditable.")
    a("")
    a("---")
    a("")

    for item in ITEMS:
        cell = row["items"].get(item.id, {})
        a(f"## `{item.id}`")
        a("")
        if not cell.get("applicable"):
            a(f"Not material for {entry['sector']} in this inventory; not scored.")
            a("")
            continue
        label = labels.get(item.id)
        a(f"*{item.hypothesis}*")
        a("")
        a(f"- Score **{cell['score']:.3f}** against threshold {item.calibrated_threshold:.2f}"
          + (f", structural gate ≥{item.min_anchors_with_figure} anchors with an adjacent figure"
             if item.min_anchors_with_figure else ""))
        a(f"- Pipeline: **{_decision(cell)}**  ·  hand read: **{_label_text(label)}**  ·  {_agreement(cell, label)}")
        if not item.scored:
            a(f"- **EXCLUDED from scored output.** {item.exclusion_reason}")
        a(f"- Highest-scoring span came from chunk {cell.get('source_chunk_idx')} of {row['n_paragraphs']}")
        a("")
        a(_evidence_block(cell))
        a("")

    a("---")
    a("")
    a("**Reading this file.** \"not detected\" means this detector did not find a "
      "qualifying passage in this document. It is not a claim that the company "
      "failed to disclose the item, and not a claim about intent. Where the hand "
      "read column says `unverified`, the cell was deliberately left unlabelled "
      "rather than guessed. Method, known faults and the per-item reliability "
      "figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and "
      "`absence/PER_METRIC.md`.")
    a("")
    return "\n".join(lines)


def render_index(prov, results_by_company, labels_all) -> str:
    lines: list[str] = []
    a = lines.append
    a("# Analysed reports")
    a("")
    a("One folder per document the pipeline read. Each holds `source.txt` — the "
      "exact extracted text that was scored, hash-verified in "
      "`absence/data/provenance.json` — and `analysis.md`, its per-item audit "
      "trail. Regenerate the analyses with `python -m absence.export_reports`.")
    a("")
    a("| folder | company | sector | chars | scored items agreeing with the hand read |")
    a("|---|---|---|---:|---|")
    for entry in prov:
        row = results_by_company[entry["company"]]
        labels = labels_all.get(entry["company"], {})
        checkable = [
            (i, row["items"][i.id], labels.get(i.id))
            for i in ITEMS
            if i.scored and row["items"].get(i.id, {}).get("applicable")
            and labels.get(i.id) is not None
        ]
        agree = sum(1 for _, c, l in checkable if bool(c.get("found")) == bool(l))
        frac = f"{agree}/{len(checkable)}" if checkable else "—"
        a(f"| [`{entry['slug']}/`]({entry['slug']}/analysis.md) | {entry['company']} | "
          f"{entry['sector']} | {entry['extracted_text_chars']:,} | {frac} |")
    a("")
    scored_ids = [i.id for i in ITEMS if i.scored]
    a(f"Only the {len(scored_ids)} validated items count toward those fractions: "
      + ", ".join(f"`{i}`" for i in scored_ids) + ". The other "
      f"{len(ITEMS) - len(scored_ids)} items appear in every analysis file, marked "
      "excluded with the reason, because their evidence is still worth auditing "
      "even though their accuracy is unknown or measurably poor.")
    a("")
    return "\n".join(lines)


def run() -> None:
    prov = json.load(open(PROVENANCE_PATH))
    results = json.load(open(RESULTS_PATH))
    labels_all = json.load(open(LABELS_PATH))["labels"]
    results_by_company = {r["company"]: r for r in results}

    for entry in prov:
        row = results_by_company.get(entry["company"])
        if row is None:
            print(f"  no results row for {entry['company']}; skipped")
            continue
        out = REPORTS_DIR / entry["slug"] / "analysis.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(entry, row, labels_all.get(entry["company"], {})))
        print(f"  wrote {out}")

    index = REPORTS_DIR / "INDEX.md"
    index.write_text(render_index(prov, results_by_company, labels_all))
    print(f"  wrote {index}")


if __name__ == "__main__":
    run()
