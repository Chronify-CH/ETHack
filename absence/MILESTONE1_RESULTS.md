# Milestone 1 results

Per `ABSENCE_BRIEF.md` Section 13: 10 hand-picked reports across 3 sectors, extract
→ paragraphs → 8 disclosure items → silence table, validated by eye, fraction
correct reported. This report has two parts: the initial keyword-heuristic-stub
run, and the real-entailment run that replaced it once `huggingface.co` access
was granted. **The second run is not simply "better" — read the comparison
below before trusting either number.**

## What actually ran

- **Corpus**: 10 real, current S&P 500 sustainability/ESG report PDFs — Technology
  (Apple, Microsoft, Alphabet/Google), Energy (ExxonMobil, Chevron, ConocoPhillips,
  Occidental Petroleum), Financials (JPMorgan Chase, Bank of America, Goldman Sachs).
  Fetched via the TinyFish web-fetch connector (see "Environment deviations" below);
  provenance in `absence/data/provenance.json`, raw text cached in
  `absence/data/raw/*.txt`.
- **Extraction**: `absence/corpus/extract.py` segments extracted text into
  paragraphs (blank-line delimited, boilerplate/short-fragment filtering).
- **Items**: 8 of the ~50-item Section 7 inventory (`absence/detect/items.py`).
- **Detection**: `absence/detect/entail.py` retrieves up to `k` anchor-term
  candidate paragraphs per item, then scores each against
  `MoritzLaurer/deberta-v3-base-zeroshot-v2.0` (identifier verified live
  against the HF API, not assumed) -- a model trained specifically as a binary
  entailment/not_entailment classifier, matching Section 7's
  (premise, hypothesis) -> P(entailment) interface exactly.
- **Runner**: `python -m absence.milestone1` prints the silence table and writes
  `absence/data/milestone1_results.json`.

## Environment deviations (logged, not hidden)

This session's network egress initially blocked `sec.gov`, company IR domains,
and `huggingface.co`; over the course of this milestone the user widened the
allowlist twice more (`huggingface.co` itself, then its CDN host
`us.aws.cdn.hf.co`, discovered because HF serves model weight files via a
redirect to a separate domain from the one hosting model pages/API). One
deviation remains permanent regardless: **no raw PDF bytes.** The only working
fetch path was TinyFish, which returns its own extracted text, not raw bytes --
so there is no real SHA-256 over source PDF bytes, no true page count, and no
PyMuPDF block-level extraction (Section 5) on this corpus. Paragraph
segmentation runs over TinyFish's flattened text instead. By eye this did not
produce column-interleaving garbage on these 10 documents, but it does produce
**oversized merged paragraphs where tables lack blank-line separation from
surrounding prose** -- average paragraph length in this corpus is ~2,800
characters, well above a normal prose paragraph, which turned out to matter a
great deal (see below).

## Two runs, not one

**Run 1 (keyword-heuristic stub, `entail.py` before this milestone's later
commits):** anchor-term overlap + number-presence, `k=8` candidates,
uncalibrated. By-eye accuracy on 17 grep-verified item/company cells: **65%
(11/17)**, with every miss traced to retrieval surfacing boilerplate or a
glossary page over the real supporting text. Full methodology preserved in
git history of this file.

**Run 2 (real DeBERTa-v3-MNLI entailment):** same retrieval design, but tuned
down to `k=4` candidates and `max_length=256` tokens purely for CPU runtime
on this environment's 4-core machine (measured: `k=8`/`max_length=512` against
this corpus's oversized paragraphs was projected at ~80+ minutes; `k=4`/`256`
brought the full run to ~12 minutes). Full log of every item score is in
`/tmp/milestone1_run.log` at time of writing; final scores in
`absence/data/milestone1_results.json`.

## Manual accuracy check, run 2

Same method as run 1: grep the actual extracted document text for ground
truth, don't just trust the printed snippet. 12 item/company cells audited,
covering the same companies as before plus new spot-checks:

| Company | Item | System said | Ground truth | Verdict |
|---|---|---|---|---|
| Apple | scope1_absolute | absent (0.034) | Present (real numbers, e.g. "Scope 1 55,200...") | ❌ **false negative** — retrieval surfaced a GHG-Protocol methodology paragraph, not the numeric table |
| Apple | scope2_market_based | absent (0.418) | Present ("Scope 2 (market-based)... 3,000...") | ❌ **false negative** (borderline — retrieved an energy-consumption input table, not the derived Scope 2 line, likely truncated before it) |
| Apple | scope3_category_breakdown | absent (0.198) | Present ("Manufacturing (purchased goods and services) 13,400,000...") | ❌ **false negative** — retrieved a generic "avoided emissions" sentence instead |
| Apple | target_net_zero_year | absent (0.004) | Present ("2030" stated repeatedly) | ❌ **false negative** — retrieved paragraph is climate-impact framing text, not Apple's own target statement |
| Apple | assurance_provider_named | absent (0.008) | Present ("Apex Companies, LLC") | ❌ **false negative, and the concerning kind** — retrieval found the *exact right paragraph* ("Apex Companies, LLC... provide reasonable assurance...") and the model still scored it near zero |
| Apple | board_committee_climate_mandate | absent (0.000) | Absent (confirmed, no such text anywhere in doc) | ✅ correct |
| Apple | scenario_analysis_quantified | FOUND (0.878) | Absent (qualitative only, no $ figure) | ❌ **false positive, high confidence** — retrieved an unrelated paragraph about European retail store energy efficiency |
| ConocoPhillips | injury_rate_trir | FOUND (0.686) | Present (real TRIR table: "Employee TRIR... 0.457, 0.532") | ✅ **correct, and now with the actual correct evidence** (the stub had matched a glossary page for this same true label) |
| Chevron | scope3_category_breakdown | absent (0.0, no candidates) | Absent (confirmed) | ✅ correct |
| ExxonMobil | target_net_zero_year | absent (0.004) | Present (qualitative "net zero... by 2050", "...by 2030") | ❌ **false negative** — retrieved a different paragraph about the "Advancing Climate Solutions Report" in general, not the target sentence |
| Occidental | assurance_provider_named | FOUND (0.92) | Present | ✅ **correct, excellent evidence** ("Independent Limited Assurance Report... ERM Certification and Verification Services, Inc. ('ERM CVS') was engaged...") |
| Goldman Sachs | scenario_analysis_quantified | FOUND (0.772) | Absent (no scenario-analysis dollar impact in retrieved text) | ❌ **false positive** — retrieved a green-bond issuance paragraph ($100 million notes), unrelated to scenario analysis |

**Result: 4 / 12 correct (33%) — worse than the stub's 65% on a comparable audit.**

## This is the actual finding of Milestone 1, and it is not flattering

Swapping a keyword heuristic for a real, purpose-built NLI model did not
improve the system, on this audit. Two independent, honestly-reportable
causes:

1. **Retrieval, unchanged in design, got worse in practice.** The stub used
   `k=8`; the real model was tuned to `k=4` and 256-token truncation purely to
   fit a CPU runtime budget on this environment's 4-core machine. On a corpus
   whose paragraphs average ~2,800 characters (because tables aren't separated
   from prose -- the extraction deviation noted above), that is nowhere near
   enough candidates or context to reliably surface the one paragraph that
   actually contains the disclosed fact. 5 of the 6 real misses above are
   retrieval misses: the right paragraph exists in the document but never
   reached the model.
2. **The model itself is sometimes wrong even when retrieval succeeds.**
   Apple's `assurance_provider_named` is the clean counterexample: retrieval
   found the exact right paragraph, naming Apex Companies LLC explicitly and
   describing the assurance work, and `deberta-v3-base-zeroshot-v2.0` scored
   it 0.008 -- essentially zero entailment. This is a genuine model-accuracy
   limitation on this item's hypothesis phrasing, not a pipeline bug.
3. **One item (`scenario_analysis_quantified`) produced confident false
   positives twice** (Apple, Goldman Sachs), both times by matching
   financially-flavored but topically unrelated paragraphs (retail store
   energy costs; a green bond issuance). Its anchor terms (`$`, `million`,
   `billion`) are too generic for a report full of dollar figures for
   unrelated reasons. Per Section 11's own instruction ("items with recall
   below 0.7 should be dropped... and reported as unreliable rather than left
   in to add noise"), **`scenario_analysis_quantified` as currently specified
   should be treated as unreliable pending a redesigned anchor set or a
   two-stage check that first confirms the paragraph is about scenario
   analysis at all.**

## What this means for whoever picks up Milestone 2

Do not treat "we now have a real NLI model" as the fix. The retrieval step
(Section 7's "top-k candidate paragraphs by anchor-term BM25") is still the
keyword-overlap placeholder from Milestone 1's first iteration, now starved
down to `k=4` for CPU speed on top of already being a weak retrieval method.
Before calibrating thresholds against the 200 hand-labelled pairs Section 11
calls for, fix retrieval first: real BM25 (not raw anchor-count), a larger
`k` (afforded by either more compute or a smaller/faster NLI model), and --
most importantly given the extraction deviation -- splitting the oversized
merged paragraphs this corpus produces into sub-2000-character chunks so
truncation stops discarding real content before the model ever sees it.

## Extraction spot-check (by eye), unchanged from the first iteration

Manually read the first ~1,500 characters and tail of several documents
(Apple, Chevron, ExxonMobil, Goldman Sachs). All coherent, correctly
attributed, non-garbled prose -- no multi-column interleaving. ExxonMobil's
document is genuinely a short 19-page "Executive Summary" by design, not a
truncation artifact.

## What this does and doesn't prove

**Proven**: the plumbing works end-to-end on real documents with a real,
verified, currently-maintained NLI model -- real report discovery, real text,
paragraph segmentation, item-level retrieval and scoring against a genuine
zero-shot entailment model, a printed silence table, all traceable back to
source URLs and grep-able source text.

**Not proven, and explicitly not claimed**: that this detector, as currently
tuned, says anything reliable about these companies. 67% of the audited
calls in run 2 were wrong. The dominant cause is retrieval starvation from a
CPU-speed tradeoff, not the entailment model being fundamentally unsuited --
Occidental's assurance-provider match and ConocoPhillips's TRIR match show
the model does the right thing when retrieval actually hands it the real
evidence. Milestone 2's threshold calibration is meaningless until retrieval
is fixed to reliably do that.
