# Milestone 1 results

Per `ABSENCE_BRIEF.md` Section 13: 10 hand-picked reports across 3 sectors, extract
→ paragraphs → 8 disclosure items → silence table, validated by eye, fraction
correct reported. This is that report.

## What actually ran

- **Corpus**: 10 real, current S&P 500 sustainability/ESG report PDFs — Technology
  (Apple, Microsoft, Alphabet/Google), Energy (ExxonMobil, Chevron, ConocoPhillips,
  Occidental Petroleum), Financials (JPMorgan Chase, Bank of America, Goldman Sachs).
  Fetched via the TinyFish web-fetch connector (see "Environment deviations" below);
  provenance for every document — source URL, final URL, retrieval timestamp,
  SHA-256 of the extracted text, character count — is in `absence/data/provenance.json`.
  Raw extracted text is cached in `absence/data/raw/*.txt` so this milestone is
  reproducible without re-fetching.
- **Extraction**: `absence/corpus/extract.py` segments the extracted text into
  paragraphs (blank-line delimited, boilerplate/short-fragment filtering).
- **Items**: 8 of the ~50-item Section 7 inventory, spanning INTEGRITY, TRAJECTORY,
  SOCIAL and OPTIONALITY pillars (`absence/detect/items.py`).
- **Detection**: `absence/detect/entail.py` — a keyword-anchor-plus-heuristic stub
  with the same call signature the real DeBERTa-v3-MNLI entailment call will have.
- **Runner**: `python -m absence.milestone1` prints the silence table and writes
  `absence/data/milestone1_results.json`.

## Environment deviations (logged, not hidden)

This session's network egress policy blocks direct access to `sec.gov`,
company IR domains, and `huggingface.co` (confirmed via curl, WebFetch, and
Python `requests` — all get a `403` from the egress proxy; this is an
organization network policy, not a code issue). Two consequences, both
documented in the affected modules' docstrings:

1. **No raw PDF bytes.** The only working fetch path was the TinyFish
   connector, which returns its own already-extracted text, not raw bytes.
   So there is no real SHA-256 over source PDF bytes, no true page count, and
   no PyMuPDF block-level extraction (bounding boxes, geometric caption/table
   dropping) as Section 5 specifies — paragraph segmentation here runs over
   TinyFish's flattened text instead. By eye, this did not produce the
   column-interleaving garbage the brief warns naive extraction causes on
   these 10 documents (see spot-checks below) — but that is not a
   corpus-scale guarantee, and whoever builds Milestone 3 should replace this
   with real PyMuPDF extraction the moment raw bytes are obtainable.
2. **No real entailment model.** `huggingface.co` is unreachable, so
   ClimateBERT and DeBERTa-v3-MNLI cannot be downloaded. `entail.py` is an
   anchor-term-overlap-plus-number-presence heuristic standing in for real
   NLI scoring, with the same `score_paragraph(item, text) -> float`
   signature the real model will have. Its scores are **not calibrated** and
   must not be read as measuring anything about the companies.

## Manual accuracy check (the brief's required "by eye" validation)

I manually verified, by grepping the actual extracted document text (not just
the truncated snippet printed in the silence table), whether each system
"found"/"absent" call was actually correct — for 17 item×company cells across
4 companies (Apple, ExxonMobil, Chevron, ConocoPhillips), chosen to cover both
sectors and both outcome types.

| Company | Item | System said | Ground truth (grep-verified) | Verdict |
|---|---|---|---|---|
| Apple | scope1_absolute | FOUND | Present, real numbers (line 7335, 5827) | ✅ correct |
| Apple | scope2_market_based | FOUND | Present (line 5831, "Scope 2 (market-based)") | ✅ correct |
| Apple | scope3_category_breakdown | FOUND | Present (line 5847, "purchased goods and services" with figures) | ✅ correct |
| Apple | target_net_zero_year | FOUND | Present, "2030" stated repeatedly | ✅ correct |
| Apple | assurance_provider_named | FOUND | Present, "Apex Companies, LLC" named | ✅ correct |
| Apple | board_committee_climate_mandate | FOUND | **Absent** — no "board committee"/"committee of the board" text anywhere in the extracted document | ❌ **false positive** |
| Apple | scenario_analysis_quantified | FOUND | **Absent** — scenario analysis is discussed but purely qualitatively; no dollar figure attached to it anywhere nearby | ❌ **false positive** |
| ExxonMobil | scope1_absolute | FOUND | **Absent** — this is a 19-page "Executive Summary" doc with no numeric emissions table at all | ❌ **false positive** |
| ExxonMobil | scope2_market_based | FOUND | **Absent** (same reason) | ❌ **false positive** |
| ExxonMobil | scope3_category_breakdown | FOUND | **Absent** (same reason) | ❌ **false positive** |
| ExxonMobil | target_net_zero_year | FOUND | Present — "net zero... by 2050", "...by 2030" (Permian) both stated qualitatively | ✅ correct (label), evidence retrieved was a boilerplate legal-disclaimer paragraph, not this text |
| ExxonMobil | assurance_provider_named | absent | Absent — no assurance language anywhere in doc | ✅ correct |
| ExxonMobil | board_committee_climate_mandate | absent | Absent | ✅ correct |
| ExxonMobil | injury_rate_trir | absent | Absent (this doc doesn't cover safety data) | ✅ correct |
| ExxonMobil | scenario_analysis_quantified | FOUND | **Absent** — matched "$20 billion in lower-emission investments," which is a capex figure, not a scenario-analysis financial impact | ❌ **false positive** |
| Chevron | scope3_category_breakdown | absent | Absent — no category-level Scope 3 breakdown anywhere in the document | ✅ correct |
| ConocoPhillips | injury_rate_trir | FOUND | Present — real "Employee TRIR / Contractor TRIR / Combined TRIR" table exists (line ~11700) | ✅ correct (label), evidence retrieved was an acronym glossary entry, not the real table |

**Result: 11 / 17 correct (65%).**

The more important pattern than the raw percentage: **every miss was the
retrieval step returning the wrong candidate paragraph**, not a scoring
threshold problem. The stub retrieves by raw anchor-term overlap, so a long
boilerplate legal disclaimer (XOM) or an acronym glossary (ConocoPhillips)
that happens to contain many matching terms and stray numbers outranks the
actual relevant table. Two of the "correct" calls above (XOM target year,
ConocoPhillips TRIR) got the right found/absent label for the wrong reason —
the system never actually surfaced the real supporting text. This is exactly
the failure mode Section 7 predicts keyword matching would have and real NLI
entailment (scoring semantic support for the specific hypothesis, not term
co-occurrence) is designed to fix. It is a finding about the detector, not
about the companies, per Section 14's explicit warning.

## Extraction spot-check (by eye)

Manually read the first ~1,500 characters and tail of several documents
(Apple, Chevron, ExxonMobil, Goldman Sachs). All four are coherent,
correctly-attributed, non-garbled prose — no evidence of the multi-column
interleaving failure mode naive PDF-to-text conversion is known to cause. One
document (ExxonMobil) is genuinely a short 19-page "Executive Summary" by the
company's own design, not a truncation artifact — confirmed by the complete
absence of any numeric emissions table in its ~37K characters of extracted
text, consistent with the shorter page count.

## Fetch reliability note

4 of the first 9 non-Apple fetch attempts (Chevron, ConocoPhillips, Occidental,
Goldman Sachs direct link) failed with `target_unreachable` on the first try
and succeeded on retry (or via a `responsibilityreports.com` mirror for
Chevron and Goldman Sachs, whose direct `chevron.com` / `goldmansachs.com`
links stayed unreachable even after retry — likely bot-protection on those
origins). This matches Section 5's expectation that discovery/fetch at any
real scale needs retries and fallback routes, not a single fetch attempt.

## What this does and doesn't prove

**Proven**: the plumbing works end-to-end on real documents — real report
discovery, real text, paragraph segmentation, item-level retrieval and
scoring, a printed silence table, all traceable back to source URLs and
grep-able source text.

**Not proven, and explicitly not claimed**: that this detector says anything
reliable about these companies. 35% of the audited calls were wrong, all
via the same retrieval weakness, and the detector itself is an uncalibrated
stub. Milestone 2's threshold calibration against 200 hand-labelled pairs is
meaningless until real entailment (or at minimum a real BM25 retrieval pass
per Section 7, not top-1-by-anchor-count) replaces this stub.
