"""Turn a fetched batch into corpus documents, without transcribing them.

TinyFish returns extracted report text through the MCP layer, which persists
any large result to a file on disk. This script reads that file directly and
writes each document to absence/reports/<slug>/source.txt, recording
provenance. Nothing about the document passes through the agent's own output,
which is what makes a 50-document corpus practical at all.

Guards, all of them there because a silently-wrong document is worse than a
missing one (ABSENCE_BRIEF.md Section 4):

  * A result that came back short is NOT written. Locked pages, 404 bodies and
    interstitials all return a couple of KB of HTML-derived text that would
    otherwise be indistinguishable from a very short report. The floor is
    MIN_CHARS; anything under it is recorded as unavailable with its length,
    so the failure is visible in provenance rather than absent from it.
  * The year comes from the archive URL, and is written as report_year_from_url
    until a human or a later pass confirms it against the document's own title
    page. verify_years() does that confirmation and fills report_title_as_printed.
  * Re-ingesting is idempotent: an existing slug is overwritten only if the new
    text is longer, so a retry cannot replace a good document with a stub.

Usage:
    python -m absence.ingest_reports <persisted-tool-result-file> [...]
    python -m absence.ingest_reports --verify-years
"""

import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

PROVENANCE_PATH = pathlib.Path("absence/data/provenance.json")
TARGETS_PATH = pathlib.Path("absence/data/targets_energy.json")
REPORTS_DIR = pathlib.Path("absence/reports")
MIN_CHARS = 15_000

ARCHIVE_RE = re.compile(r"/([A-Z]+)_([A-Z0-9]+)_(\d{4})(?:_[0-9a-f]+)?\.pdf$", re.IGNORECASE)

# Tickers a company's older editions are filed under. The document is the same
# company's report; only the name on the cover changed. The alias maps it onto
# the current ticker so the three editions sit together, and the rename is
# recorded on the entry rather than hidden by it.
TICKER_ALIASES = {"CHK": ("EXE", "Published under the company's former name, Chesapeake Energy.")}


def _load_payload(path: pathlib.Path) -> dict:
    """Accept every shape the MCP layer persists results in."""
    raw = path.read_text()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        # Plain-text dump of the JSON payload.
        start = raw.find("{")
        obj = json.loads(raw[start:])
    if isinstance(obj, list) and obj and isinstance(obj[0], dict) and "text" in obj[0] and "results" not in obj[0]:
        obj = json.loads(obj[0]["text"])
    return obj if isinstance(obj, dict) else {"results": obj, "errors": []}


def _targets_by_ticker() -> dict:
    return {c["ticker"].upper(): c for c in json.load(open(TARGETS_PATH))["companies"]}


# Documents fetched from a company's own site instead of the archive. Their
# URLs carry no ticker or year, so the mapping is stated explicitly here rather
# than parsed. Every entry is provisional until verify_years() confirms the
# edition against the document's own title page: where a site lists assets by
# opaque id, the year is an inference from page order and nothing else.
MANUAL_URL_MAP: dict[str, tuple[str, int]] = {
    "https://www.targaresources.com/static-files/13aa5b46-c3a6-4086-8455-6e26ac7807f9": ("TRGP", 2022),
    "https://www.targaresources.com/static-files/c7f9001a-da7e-44ff-b6bd-0f7b73a30a1c": ("TRGP", 2024),
    "https://www.targaresources.com/static-files/f16d011c-8387-4f94-a4c5-212888a49db8": ("TRGP", 2023),
}


def ingest(paths: list[str]) -> None:
    prov = json.loads(PROVENANCE_PATH.read_text())
    by_slug = {e["slug"]: e for e in prov}
    targets = _targets_by_ticker()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    written = skipped = 0

    for path in paths:
        payload = _load_payload(pathlib.Path(path))

        # A URL the fetcher could not reach is a data point, not a non-event.
        # It is recorded so the corpus can never look complete when it is not
        # -- but never over an entry that already succeeded, so replaying an
        # old batch file cannot demote a document fetched since.
        for err in payload.get("errors", []):
            m = ARCHIVE_RE.search(err.get("url", ""))
            if not m:
                continue
            ticker, year = m.group(2).upper(), int(m.group(3))
            target = targets.get(ticker)
            slug = f"{ticker.lower()}_energy_{year}"
            if by_slug.get(slug, {}).get("status") == "ok" or target is None:
                continue
            by_slug[slug] = {
                "slug": slug, "ticker": ticker, "company": target["company"],
                "sector": "Energy", "subsector": target["subsector"],
                "source_url": err["url"], "retrieved_via": "TinyFish fetch_content",
                "retrieved_at": now, "report_year_from_url": year,
                "status": "unavailable",
                "unavailable_reason": f"Fetcher returned {err.get('error')!r} for this URL.",
            }
            print(f"  !! {slug:22} UNREACHABLE ({err.get('error')})")
            skipped += 1

        for r in payload.get("results", []):
            url = r.get("url", "")
            m = ARCHIVE_RE.search(url)
            if m:
                ticker, year = m.group(2).upper(), int(m.group(3))
            elif url in MANUAL_URL_MAP:
                ticker, year = MANUAL_URL_MAP[url]
            else:
                print(f"  ?? no ticker/year in URL, skipped: {url}")
                continue
            alias_note = ""
            if ticker in TICKER_ALIASES:
                ticker, alias_note = TICKER_ALIASES[ticker]
            target = targets.get(ticker)
            if target is None:
                print(f"  ?? {ticker} is not in the target manifest, skipped")
                continue
            slug = f"{ticker.lower()}_energy_{year}"
            text = r.get("text") or ""

            if len(text) < MIN_CHARS:
                # Logged, never imputed: the entry records what came back.
                by_slug[slug] = {
                    "slug": slug, "ticker": ticker, "company": target["company"],
                    "sector": "Energy", "subsector": target["subsector"],
                    "source_url": url, "final_url": r.get("final_url", url),
                    "retrieved_via": "TinyFish fetch_content",
                    "retrieved_at": now, "report_year_from_url": year,
                    "status": "unavailable",
                    "unavailable_reason": (
                        f"Fetch returned {len(text)} characters, below the {MIN_CHARS} floor "
                        "for a plausible report. Not written to disk; most likely a locked "
                        "page, a 404 body or an interstitial rather than the report."
                    ),
                }
                print(f"  -- {slug:22} UNAVAILABLE ({len(text)} chars)")
                skipped += 1
                continue

            out = REPORTS_DIR / slug / "source.txt"
            if out.exists() and len(out.read_text()) >= len(text):
                print(f"  == {slug:22} kept existing ({len(out.read_text()):,} >= {len(text):,} chars)")
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text)

            by_slug[slug] = {
                "slug": slug, "ticker": ticker, "company": target["company"],
                "sector": "Energy", "subsector": target["subsector"],
                "source_url": url, "final_url": r.get("final_url", url),
                "retrieved_via": "TinyFish fetch_content (extracted text; raw PDF bytes not available)",
                "retrieved_at": now,
                "report_year_from_url": year,
                "report_year": year,
                "report_title_as_printed": None,  # filled by --verify-years
                "extracted_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "extracted_text_chars": len(text),
                "status": "ok",
                "local_path": str(out),
            }
            if alias_note:
                by_slug[slug]["filed_under_former_name"] = alias_note
            print(f"  ++ {slug:22} {len(text):>9,} chars")
            written += 1

    prov = sorted(by_slug.values(), key=lambda e: e["slug"])
    PROVENANCE_PATH.write_text(json.dumps(prov, indent=2) + "\n")
    print(f"\n{written} written, {skipped} unavailable, {len(prov)} documents in provenance")


def verify_years() -> None:
    """Confirm each document's edition year against its own title page.

    The archive filename year is a convention, not a fact about the document.
    This reads the first 1,200 characters of each source and reports the years
    it finds there, so a mismatch surfaces instead of propagating into every
    downstream table.
    """
    prov = json.loads(PROVENANCE_PATH.read_text())
    write = "--write-titles" in sys.argv
    for e in prov:
        if e.get("status") == "unavailable" or not e.get("local_path"):
            continue
        head = pathlib.Path(e["local_path"]).read_text()[:1200]
        head_flat = re.sub(r"\s+", " ", head)
        years = sorted({int(y) for y in re.findall(r"\b(20[0-2]\d)\b", head_flat)})
        claimed = e.get("report_year_from_url") or e.get("report_year")
        flag = "" if claimed in years else "   <-- filename year not on title page"
        print(f"{e['slug']:24} url={claimed} title-page years={years}{flag}")
        print(f"    {head_flat[:150]}")
        if write and not e.get("report_title_as_printed"):
            # The document's opening line, quoted rather than paraphrased, so the
            # edition can be checked without opening the source.
            e["report_title_as_printed"] = head_flat[:120].strip()
    if write:
        PROVENANCE_PATH.write_text(json.dumps(prov, indent=2) + "\n")
        print("\ntitles written to provenance")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "--verify-years":
        verify_years()
    else:
        ingest(args)
