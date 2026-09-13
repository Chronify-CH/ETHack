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

    a(f"# {entry['company']} — {entry['report_year']} report — disclosure audit")
    a("")
    a(f"- **Sector (as used in this corpus):** {entry['sector']}")
    a(f"- **Report edition:** {entry['report_year']} — \"{entry['report_title_as_printed']}\" "
      "(read off the document's own title page, not inferred from the filename)")
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


def render_index(prov, results_by_slug, labels_all) -> str:
    lines: list[str] = []
    a = lines.append
    a("# Analysed reports")
    a("")
    ok = [e for e in prov if e.get("status") == "ok"]
    missing = [e for e in prov if e.get("status") != "ok"]
    scored_docs = [e for e in ok if e["slug"] in results_by_slug]
    a(f"{len(ok)} report documents, one folder each. Every folder holds `source.txt` — the exact "
      "extracted text, hash-verified in `absence/data/provenance.json`. Folders for documents that "
      "have been through the detector also hold `analysis.md`, their per-item audit trail.")
    a("")
    a(f"**{len(scored_docs)} of {len(ok)} documents have been scored.** The rest are fetched and "
      "cached but not yet run through the pipeline; they are listed below as *not yet scored*, "
      "which means exactly that and nothing about the companies concerned.")
    a("")
    a("Regenerate this file and the analyses with `python -m absence.export_reports`.")
    a("")

    order = ["Energy", "Technology", "Financials"]
    sectors = sorted({e["sector"] for e in ok}, key=lambda s: (order.index(s) if s in order else 99, s))
    for sector in sectors:
        a(f"## {sector}")
        a("")
        rows = [e for e in ok if e["sector"] == sector]
        subs = sorted({e.get("subsector") or "" for e in rows})
        for sub in subs:
            group = sorted((e for e in rows if (e.get("subsector") or "") == sub),
                           key=lambda e: (e["ticker"], -e["report_year"]))
            if sub:
                a(f"### {sub}")
                a("")
            a("| folder | company | year | chars | status |")
            a("|---|---|---:|---:|---|")
            for e in group:
                row = results_by_slug.get(e["slug"])
                if row is None:
                    status = "not yet scored"
                    link = f"`{e['slug']}/`"
                else:
                    labels = labels_all.get(e["slug"], {})
                    checkable = [
                        (i, row["items"][i.id], labels.get(i.id))
                        for i in ITEMS
                        if i.scored and row["items"].get(i.id, {}).get("applicable")
                        and labels.get(i.id) is not None
                    ]
                    agree = sum(1 for _, c, l in checkable if bool(c.get("found")) == bool(l))
                    status = (f"scored, {agree}/{len(checkable)} agree with the hand read"
                              if checkable else "scored, no hand-labelled cells")
                    link = f"[`{e['slug']}/`]({e['slug']}/analysis.md)"
                caveat = " ⚠︎" if e.get("document_type_caveat") else ""
                a(f"| {link} | {e['company']}{caveat} | {e['report_year']} | "
                  f"{e['extracted_text_chars']:,} | {status} |")
            a("")

    if missing:
        a("## Documents that could not be retrieved")
        a("")
        a("Recorded rather than omitted, so the corpus can never look more complete than it is. "
          "None of these is evidence about the company: each is a fact about the source.")
        a("")
        a("| intended document | company | year | why not retrieved |")
        a("|---|---|---:|---|")
        for e in sorted(missing, key=lambda e: e["slug"]):
            reason = (e.get("unavailable_reason") or "").replace("|", "/")
            a(f"| `{e['slug']}` | {e['company']} | {e.get('report_year_from_url', '')} | {reason} |")
        a("")

    caveated = [e for e in ok if e.get("document_type_caveat")]
    if caveated:
        a("## ⚠︎ Document-type caveats")
        a("")
        for e in caveated:
            a(f"- **{e['slug']}** — {e['document_type_caveat']}")
        a("")

    a("## Reading the year column")
    a("")
    a("Every year here was confirmed against the document's own title page, not taken from its "
      "filename. The three editions held for one company are its three most recent available, "
      "which are not the same three years across companies: some archives reach 2024 or 2025 and "
      "others stop at 2022. A difference between two companies in this corpus can therefore be a "
      "difference in reporting year rather than in disclosure. Compare within a year where the "
      "corpus allows it.")
    a("")
    scored_ids = [i.id for i in ITEMS if i.scored]
    a(f"Only the {len(scored_ids)} validated items count toward the agreement figures above: "
      + ", ".join(f"`{i}`" for i in scored_ids) + ". The other "
      f"{len(ITEMS) - len(scored_ids)} appear in each analysis file marked excluded, with the "
      "reason, because their evidence is still worth auditing even though their accuracy is "
      "unknown or measurably poor.")
    a("")
    return "\n".join(lines)


def run() -> None:
    prov = json.load(open(PROVENANCE_PATH))
    results = json.load(open(RESULTS_PATH))
    labels_all = json.load(open(LABELS_PATH))["labels"]
    results_by_slug = {r["slug"]: r for r in results}

    for entry in prov:
        row = results_by_slug.get(entry["slug"])
        if row is None:
            print(f"  no results row for {entry['company']}; skipped")
            continue
        out = REPORTS_DIR / entry["slug"] / "analysis.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(entry, row, labels_all.get(entry["slug"], {})))
        print(f"  wrote {out}")

    index = REPORTS_DIR / "INDEX.md"
    index.write_text(render_index(prov, results_by_slug, labels_all))
    print(f"  wrote {index}")


if __name__ == "__main__":
    run()
