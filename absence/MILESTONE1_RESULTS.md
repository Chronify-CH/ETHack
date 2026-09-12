# Milestone 1 results

Per `ABSENCE_BRIEF.md` Section 13: 10 hand-picked reports across 3 sectors, extract
→ paragraphs → 8 disclosure items → silence table, validated by eye, fraction
correct reported. This report covers four runs. **Read the comparison
below before trusting any single number** — accuracy did not improve
monotonically with "more sophisticated" methods; it got worse, then much
better, for identifiable reasons. One reported number was also corrected
downward after the models caught an error in my own ground truth.

| Run | Retrieval | Chunking | Scoring | By-eye accuracy |
|---|---|---|---|---|
| 1 | Raw anchor-term count | Blank-line paragraphs (~2,800 char avg) | Keyword heuristic | 59% (10/17, corrected -- see below) |
| 2 | Raw anchor-term count, k=4 | Same, unbounded | Real DeBERTa-v3-MNLI (base), 256-token truncation | 33% (4/12) |
| 3 | Real BM25, k=8 | `rechunk()`-bounded to ~900 chars | Same model | **83% (10/12); 85% (11/13) on the extended cell set** |
| 4 | Same as run 3 | Same as run 3 | DeBERTa-v3-**large**-zeroshot-v2.0 | 69% (9/13) -- **worse than run 3's 85% on identical cells** |

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
uncalibrated. By-eye accuracy on 17 grep-verified item/company cells: **59%
(10/17)** — originally reported as 65% (11/17); corrected downward after run 4
exposed an error in my own ground truth (see "A correction to the ground
truth" below). Misses traced to retrieval surfacing boilerplate or a
glossary page over the real supporting text. Full methodology preserved in
git history of this file.

### A correction to the ground truth (found by the model, not by me)

In run 1's audit I recorded ExxonMobil's `injury_rate_trir` as correctly
`absent`, on the strength of `grep -i "trir\|recordable incident"` returning
nothing in that document. **That ground truth was wrong.** ExxonMobil's
Executive Summary discloses "0.02 LTIR — our industry-leading lost-time
incident rate per 200,000 work hours": a numeric workplace injury rate, which
is exactly what the item's hypothesis asks for ("total recordable incident
rate (TRIR) **or equivalent workplace injury rate statistic**"). My grep
terms were narrower than the item definition, so the disclosure was invisible
to my manual check.

This surfaced only because run 4's large model returned `FOUND 0.846` on that
cell, contradicting my recorded ground truth and prompting a re-check. The
consequences:
- Run 1's ExxonMobil `injury_rate_trir` was a **false negative**, not a true
  negative → run 1 drops from 11/17 to 10/17.
- Run 2's base model also scored this `absent` (0.000) — also a false
  negative. Run 3, after the BM25/rechunk fix, scored it FOUND 0.736, i.e.
  correctly; an earlier version of this document wrongly attributed run 2's
  miss to run 3.
- **Methodological warning for Milestone 2's 200-pair hand-labelling:** if
  the hand-labeller greps for the item's *name* rather than the full space of
  phrasings its *hypothesis* admits, the labels themselves will be wrong, and
  every precision/recall number computed from them will inherit the error in
  the direction that flatters a keyword-based detector and penalises a
  semantic one. Label from the hypothesis text, and search for synonyms
  (LTIR, TRR, DART, lost-time, recordable) before recording an absence.

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

**Result: 4 / 12 correct (33%) — worse than the stub's 59% on a comparable audit.**

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

## Run 3: real BM25 + bounded chunks fixed almost everything

Run 2's writeup said, in effect, "fix retrieval before touching the model."
That's what run 3 does: `extract.rechunk()` splits any paragraph over ~900
characters into overlapping bounded chunks (so truncation stops discarding
content mid-fact), and `entail.retrieve_candidates` now uses `rank_bm25`'s
BM25Okapi with a real query (item hypothesis + anchor terms) instead of raw
anchor-hit counting, with `k` restored to 8. Same 12-cell audit as run 2, same
companies and items, re-checked against the same grep-verified ground truth:

| Company | Item | Run 2 (bad retrieval) | Run 3 (BM25 + chunks) | Run 3 evidence |
|---|---|---|---|---|
| Apple | scope1_absolute | ❌ absent 0.034 | ✅ FOUND 0.736 | Real emissions data table |
| Apple | scope2_market_based | ❌ absent 0.418 | ✅ FOUND 0.937 | "Scope 1 55,200 55,200 47,430..." -- the real numeric table |
| Apple | scope3_category_breakdown | ❌ absent 0.198 | ✅ FOUND 0.944 | Correct appendix region (see caveat below) |
| Apple | target_net_zero_year | ❌ absent 0.004 | ❌ absent 0.069 | "Our plan to become carbon neutral by 2030..." -- **retrieval got the exact right sentence and the model still scored it near zero** |
| Apple | assurance_provider_named | ❌ absent 0.008 | ✅ FOUND 0.808 | "...Apple's independent assurance provider for the Supplie[r Clean Energy Program]..." |
| Apple | board_committee_climate_mandate | ✅ absent 0.000 | ✅ absent 0.002 | Correctly absent |
| Apple | scenario_analysis_quantified | ❌ FOUND 0.878 (wrong topic) | ✅ absent 0.031 | Correctly absent -- the earlier false positive is gone |
| ConocoPhillips | injury_rate_trir | ✅ FOUND 0.686 | ✅ FOUND 0.977 | "total recordable rate (TRR) was 0.28..." -- direct hit |
| Chevron | scope3_category_breakdown | ✅ absent 0.0 | ✅ absent 0.391 | Correct label; retrieved evidence (a board-member list) is irrelevant -- right answer, still not for a good reason |
| ExxonMobil | target_net_zero_year | ❌ absent 0.004 | ❌ absent 0.021 | "...ExxonMobil's 2030 greenhouse gas..." -- relevant evidence, **same near-zero score pattern as Apple above** |
| Occidental | assurance_provider_named | ✅ FOUND 0.92 | ✅ FOUND 0.968 | "ERM Certification and Verification Services, Inc." named directly |
| Goldman Sachs | scenario_analysis_quantified | ❌ FOUND 0.772 (wrong topic) | ✅ absent 0.043 | Correctly absent -- fixed |

**Result: 10/12 correct (83%).** Caveat on `scope3_category_breakdown`: the
retrieved chunk is in the right appendix region but doesn't itself itemize
categories the way the ground-truth line does ("Manufacturing (purchased
goods and services) 13,400,000...") -- credited as correct here because BM25
landed in the right table, but a stricter audit might call this "close but
not the precise supporting line," which is a caveat worth carrying into
Milestone 2's formal calibration rather than resolving by eye here.

**The one clear remaining pattern**: `target_net_zero_year` failed twice, and
in both cases retrieval is not the problem -- it found genuinely on-topic
sentences stating explicit target years ("carbon neutral by 2030",
"ExxonMobil's 2030 greenhouse gas [target]"), and the model still scored
entailment near zero. This is a specific, reproducible weakness in how
`deberta-v3-base-zeroshot-v2.0` handles this item's hypothesis wording, not a
retrieval gap -- exactly the kind of controlled test case worth trying against
a larger model before assuming "add BM25" is the only lever left.

## What this means for whoever picks up Milestone 2

BM25 + bounded chunking was the fix run 2's writeup called for, and it worked:
83% vs 33%. Before calibrating thresholds against the 200 hand-labelled pairs
Section 11 calls for, two things are still worth doing first: (1) resolve the
`scope3_category_breakdown` caveat above -- decide whether "right table, wrong
line" should count as found at all, since a stricter standard would change
the reported accuracy; (2) investigate the `target_net_zero_year` scoring
failure specifically -- try a larger NLI model (`deberta-v3-large-zeroshot-v2.0`)
on just this item's failing cases before committing to a full, slower re-run
across the whole corpus, since the failure looks scoring-specific rather than
systemic.

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

## Run 4: the large model, and a lesson about how I validated it

Run 3's writeup recommended trying `deberta-v3-large-zeroshot-v2.0` against
`target_net_zero_year`'s two failures before committing to a full re-run. I
did that: on the two failing cases (using each item's own hypothesis and its
real retrieved evidence), the large model fixed one outright (0.069 → 0.955)
and improved the other (0.021 → 0.464), with no regression on two controls.
That looked like clear evidence for the swap. It was not.

**The pre-test was a biased sample.** I tested the large model only on cells
the base model already got *wrong*, plus two controls it already got *right*.
A model evaluated solely on its predecessor's known failures can essentially
only look good — there is no way for that test to surface regressions on the
cells I never re-checked. Which is exactly where the regressions were.

Full run 4, audited against the same 13 cells as run 3 (the 12 from run 3
plus ExxonMobil's `injury_rate_trir`, once its ground truth was corrected):

| Company | Item | Ground truth | Run 3 (base) | Run 4 (large) | Who's right |
|---|---|---|---|---|---|
| Apple | scope1_absolute | present | 0.736 FOUND | 0.026 absent | **run 3** |
| Apple | scope2_market_based | present | 0.937 FOUND | 0.840 FOUND | both |
| Apple | scope3_category_breakdown | present | 0.944 FOUND | 0.516 FOUND | both |
| Apple | target_net_zero_year | present | 0.069 absent | 0.721 FOUND | **run 4** |
| Apple | assurance_provider_named | present | 0.808 FOUND | 0.027 absent | **run 3** |
| Apple | board_committee_climate_mandate | absent | 0.002 absent | 0.018 absent | both |
| Apple | scenario_analysis_quantified | absent | 0.031 absent | 0.361 absent | both |
| ConocoPhillips | injury_rate_trir | present | 0.977 FOUND | 0.960 FOUND | both |
| Chevron | scope3_category_breakdown | absent | 0.391 absent | 0.857 FOUND | **run 3** |
| ExxonMobil | target_net_zero_year | present | 0.021 absent | 0.066 absent | neither |
| Occidental | assurance_provider_named | present | 0.968 FOUND | 0.905 FOUND | both |
| Goldman Sachs | scenario_analysis_quantified | absent | 0.043 absent | 0.446 absent | both |
| ExxonMobil | injury_rate_trir | present | 0.736 FOUND | 0.846 FOUND | both |

**Run 3 (base): 11/13 (85%). Run 4 (large): 9/13 (69%).** The large model is
3.6x slower (77 minutes vs ~21) and scored *lower*.

(Corrected: these were first reported as 10/13 vs 9/13 because I transcribed
run 2's ExxonMobil `injury_rate_trir` score (0.000) into run 3's column. Run 3
actually scored that cell FOUND 0.736 -- correctly. This is the second
transcription/ground-truth error in this document's audits, both caught only
by re-deriving numbers from the raw logs rather than from my own earlier
summary. Treat every hand-assembled table here as needing that check.)

Two of run 4's errors are the confident kind, which is the concerning kind:
- **Apple `assurance_provider_named`, 0.027**: retrieval handed it a
  near-perfect passage — "We obtain third-party verification for some of the
  information in this report from **Apex Companies and the Fraunhofer
  Institute in Germany**" — naming two providers outright. The large model
  scored it 0.027. This is the *same failure class* the base model showed in
  run 2 (0.008 on the Apex paragraph), so the larger model did not fix it;
  it reintroduced it after run 3 had gotten the cell right.
- **Chevron `scope3_category_breakdown`, 0.857**: a confident false positive
  on a passage about carbon-intensity targets and "$2.0 billion in carbon
  reduction projects" — no Scope 3 category breakdown at all. Verified with
  `groundtruth_probe.py`: the document's only near-misses are "end use" inside
  an intensity-metric definition and "upstream"/"downstream" as *business
  segment* names, not emissions categories.

**Caveat on the size of this result, stated plainly:** 11/13 vs 9/13 is a
two-cell difference on a 13-cell sample. That is still a small sample and it
would be overclaiming to treat the gap as precisely measured. What it does
establish is the weaker but still decisive claim: **the large model shows no
measurable improvement at 3.6x the cost**, and the evidence that motivated
the swap was an artifact of how I sampled the test. Both models fail on
different cells rather than one dominating, which is itself a sign that
neither is reliable yet and that the real fix is calibration, not size.

**Action taken:** reverted `MODEL_ID` to `deberta-v3-base-zeroshot-v2.0` --
faster, no worse on the available evidence. Model choice should be settled by
Milestone 2's calibration against 200 hand-labelled pairs (Section 11), on a
sample drawn independently of which cells any particular model already fails,
not by a 13-cell by-eye audit in either direction.
