# Build brief: measuring what an ESG report leaves out

Drop this in the repo root and start with: *"Read ABSENCE_BRIEF.md and build Milestone 1."*

---

## 0. What already exists

There is a working scoring engine in this repo:

- `veritas/core.py` — robust z-scores (median/MAD, sector-relative), weighted geometric aggregation, hard guardrails
- `veritas/framework.py` — six pillars (LEVEL, TRAJECTORY, **INTEGRITY**, NATURE, SOCIAL, OPTIONALITY), a `MATERIALITY` dict of per-sector pillar weights derived from the SASB materiality map, and `REQUIRED_RATE` (SBTi-style 1.5C decarbonisation pathways by sector)
- `veritas/fastsim.py` — vectorised Monte Carlo that propagates data-quality uncertainty and weight ambiguity into a rank distribution
- `veritas/diagnostics.py` — falsification tests (size bias, predictive validity via AUC, divergence from a vendor rating)
- `pipeline/fetch_free_sources.py` — connectors for SEC EDGAR XBRL, EPA GHGRP, EPA TRI, EPA ECHO, Climate TRACE, SBTi, OSHA, USPTO PatentsView

**Extend this. Do not rebuild it.** The new work produces indicators that feed the existing INTEGRITY pillar and make the currently-synthetic `flag_restated_emissions` guardrail real. Reuse `MATERIALITY` rather than defining new sector weights.

---

## 1. Objective

Build a pipeline that reads a company's public ESG/sustainability reporting and measures **what is missing from it**, benchmarked two ways:

1. against its GICS sub-industry peers
2. against the full S&P 500

Output a per-company **Silence Ledger**: every disclosure item we looked for, whether it was found, how specific it was, what share of peers disclosed it, and — where external data exists — whether there is evidence the company had something to disclose and didn't.

---

## 2. Non-goals

- **Do not build a lie detector.** Text alone cannot establish truth. Style-based greenwashing classifiers learn to flag vague prose, which inverts under adversarial pressure: a firm that hires better writers scores better while behaving identically.
- **Do not train a greenwashing model from scratch.** There are no labels. Use pretrained classifiers plus zero-shot entailment, and validate against realised outcomes.
- **Do not generate any company data you did not retrieve.** If a fetch fails, log it and mark the field `unavailable`. Never impute silently. A missing value and an imputed value must never be indistinguishable downstream.
- Do not write output language that characterises intent. Use "not disclosed" and "no corresponding disclosure found". Never "concealed", "hid", "lied", or "false".

---

## 3. The central idea

Absence is not measurable inside a single document. It is only measurable against a reference distribution.

Silence about a topic nobody in the sector discusses tells you nothing. Silence about a topic 94% of peers disclose, in a sector where that topic is material, and where external regulatory data shows the company has exposure to it, is close to dispositive.

So everything here reduces to one construction: build the expected disclosure profile from the corpus, then measure the gap.

Four mechanisms, in ascending order of how damning they are:

| Mechanism | What it catches |
|---|---|
| **Attention misallocation** | Report text distributed differently from where the sector's material risks are |
| **Conditional silence** | Item absent that most peers disclose |
| **Disclosure retreat** | Item present last year, gone this year |
| **Evidence gap** | External data shows exposure; the report never mentions it |

---

## 4. Architecture

```
absence/
  corpus/
    discover.py        find report URLs per company per year
    fetch.py           download, hash, cache, provenance log
    extract.py         PDF -> layout-aware blocks -> paragraphs
  detect/
    prefilter.py       cheap keyword screen before any transformer
    classify.py        ClimateBERT heads: detector / specificity / commitment
    items.py           the disclosure item inventory + hypothesis bank
    entail.py          zero-shot NLI item detection
    values.py          numeric + unit + scope + year extraction
  baseline/
    peers.py           per-item coverage rates by sub-industry and index-wide
    expected.py        expected topic distribution from MATERIALITY
  metrics/
    silence.py         conditional silence score
    retreat.py         year-over-year disclosure retreat + granularity decay
    attention.py       KL divergence of topic share vs materiality
    evidence_gap.py    cross-reference against EPA / OSHA / SEC
  ledger.py            assemble the per-company Silence Ledger
  validate.py          falsification tests
```

Store everything in a single SQLite database (`absence.db`) with parquet exports. Every stage must be independently resumable from the database — a 1,500-PDF crawl *will* fail partway through and must not lose work.

---

## 5. Stage A — corpus

Target: every S&P 500 company, three most recent reporting years. Roughly 1,200–1,500 documents.

**Discovery, in priority order:**

1. **SEC EDGAR** (`data.sec.gov`, free, no key, requires a descriptive `User-Agent`). 10-K Items 1/1A, DEF 14A for climate-linked executive compensation, and any 8-K sustainability exhibits. This is the most reliable source and the only one with guaranteed coverage and clean provenance. Start here.
2. **responsibilityreports.com** — free directory of CSR/ESG report PDFs with per-company pages.
3. **Company IR sites** — resolve via search for `"{company} sustainability report {year} filetype:pdf"`. Respect `robots.txt`.
4. **Net Zero Tracker** and the **SBTi company dashboard** for structured target data to cross-check what the PDFs claim.

**Requirements:**

- Record for every document: source URL, retrieval timestamp, SHA-256, byte size, page count, and which discovery route found it. Provenance is what makes any finding defensible when a company disputes it.
- Content-hash cache. Never re-download a document whose hash is unchanged.
- Rate limit: 5 req/s ceiling, exponential backoff, descriptive User-Agent with a contact address.
- Store the raw PDF bytes. Re-extraction with better parsers is likely; re-downloading 1,500 PDFs is not.
- Log every discovery failure with the reason. Report corpus coverage as a headline number — if we only found reports for 340 of 500 companies, that is a finding, not something to paper over.

**Extraction:** ESG reports are design artifacts — multi-column, pull quotes, infographic captions, and twenty pages of photography before any content. Naive `pdftotext` interleaves columns into nonsense. Use PyMuPDF block extraction (keep block bounding boxes so captions and sidebars can be dropped by geometry) or `docling`. Validate on ten documents by eye before running the corpus. **Extraction quality dominates every downstream number.**

Keep tables separate from prose. Most of the quantitative claims live in tables, and paragraph classifiers applied to table fragments produce garbage.

---

## 6. Stage B — classification

Pretrained, free, no labelling required:

| Model | Task | Granularity |
|---|---|---|
| `climatebert/distilroberta-base-climate-detector` | climate-related or not | paragraph |
| `climatebert/distilroberta-base-climate-specificity` | specific vs non-specific | paragraph |
| `climatebert/distilroberta-base-climate-commitment` | commitment/action vs not | paragraph |
| `climatebert/environmental-claims` | is this an environmental claim | **sentence** |

The specificity and commitment models are trained on paragraphs and the authors warn they degrade on sentences. Respect the granularity split: segment into paragraphs for those three, sentences for environmental-claims. Do not feed sentences to paragraph models.

**Compute:** 1,500 reports × ~1,500 paragraphs ≈ 2M paragraph inferences. On CPU this is 20+ hours. Two mitigations, both required:
- Run `prefilter.py` first — a keyword screen (emissions, scope, carbon, water, safety, target, net zero, …) that drops the ~70% of paragraphs about community volunteering and office recycling before any transformer touches them.
- Batch at 64, use GPU if available. If no GPU, subsample to 150 companies and say so in the output metadata rather than quietly running on less data.

Cheap talk index, per the ClimateBERT authors' own suggested construction:

```
cheap_talk = P(commitment) * (1 - P(specific))
```

---

## 7. Stage C — the disclosure item inventory

This is the core of the build. Absence of a *topic* is fuzzy. Absence of a *specific named fact* is unambiguous, and unambiguous is what survives a hostile question.

Define ~50 items in `items.py`. Each carries: `id`, `pillar`, `hypothesis` (a natural-language statement for entailment), `regex_anchors`, `sector_applicability` (which GICS sectors it is material for, derived from SASB), and `granularity_levels`.

**Emissions accounting**
`scope1_absolute` · `scope2_location_based` · `scope2_market_based` · `scope3_total` · `scope3_category_breakdown` · `scope3_cat1_purchased_goods` · `scope3_cat11_use_of_sold_products` · `scope3_cat15_investments` · `emissions_baseline_year` · `emissions_restatement_note` · `biogenic_emissions_separate` · `methane_specific`

**Targets**
`target_net_zero_year` · `target_interim_milestone` · `target_covers_scope3` · `target_sbti_validated` · `target_absolute_or_intensity_stated` · `offset_volume_quantified` · `offset_type_disclosed` (avoidance vs removal, durable vs nature-based)

**Money**
`transition_capex_amount` · `green_revenue_share` · `internal_carbon_price_level` · `exec_comp_climate_linked_weight` · `climate_capex_share_of_total`

**Assurance and governance**
`assurance_provider_named` · `assurance_level` (limited vs reasonable) · `assurance_scope_itemised` · `board_committee_climate_mandate` · `board_climate_expertise`

**Lobbying**
`trade_association_alignment_review` · `political_contributions_disclosed` · `lobbying_climate_position_statement`

**Nature**
`water_withdrawal_total` · `water_in_stressed_basins` · `hazardous_waste_separate` · `sites_near_protected_areas` · `toxic_releases_quantified`

**Social**
`injury_rate_trir` · `fatalities_count` · `contractor_vs_employee_safety_split` · `voluntary_turnover_rate` · `supply_chain_audit_findings_count` · `raw_gender_pay_gap` (unadjusted, not the adjusted figure) · `living_wage_quantified`

**Risk**
`scenario_analysis_quantified` (a dollar impact, not merely "we conducted one") · `physical_risk_asset_level` · `stranded_asset_exposure`

Several of these are chosen because they are the things companies drop first when the number goes the wrong way: `contractor_vs_employee_safety_split`, `raw_gender_pay_gap`, `offset_volume_quantified`, `scope3_category_breakdown`, `supply_chain_audit_findings_count`.

**Detection method — hypothesis bank + entailment.**

Rather than writing 50 bespoke parsers, use one generic verifier. For each item, retrieve the top-k candidate paragraphs by anchor-term BM25, then run a natural language inference model with the item's hypothesis:

```
hypothesis: "The company disclosed its market-based Scope 2 emissions in tonnes of CO2 equivalent."
premise:    <candidate paragraph>
-> entailment / neutral / contradiction
```

Use a strong off-the-shelf MNLI model (the DeBERTa-v3 MNLI family on HuggingFace is the usual choice — verify the exact identifier is current before pinning it). Item is present if max entailment probability across candidates exceeds a threshold calibrated on a hand-labelled set of 200 item/report pairs. Keep the probability, not just the binary — it feeds the existing uncertainty machinery.

Where the item has a number, run `values.py` to extract value, unit, scope boundary, and reporting year. Disagreement between the entailment result and the value extractor is itself a flag worth logging.

**Granularity, not just presence.** Score each found item 0–4:

```
0 absent
1 qualitative mention only
2 a number
3 number + baseline year + scope boundary
4 all of the above + third-party assured
```

Granularity decay year over year is a signal in its own right, and a softer one than outright disappearance, so it catches companies being careful.

---

## 8. Stage D — the four metrics

**1. Conditional Silence Score.** For company *i* in sub-industry *s*:

```
peer_coverage(k,s)  = share of peers in s disclosing item k
CSS(i) = Σ_k  absent(i,k) · peer_coverage(k,s) · materiality(k,s)
         ────────────────────────────────────────────────────────
         Σ_k  peer_coverage(k,s) · materiality(k,s)
```

Range 0–1. Weighting by peer coverage is what makes this informative: omitting something nobody discloses contributes nothing; omitting something 94% of peers disclose contributes almost its full weight.

Compute twice — once against sub-industry peers, once against the whole S&P 500 — and report both. The gap between them is interesting on its own: a company that looks normal against peers but anomalous against the index tells you the *sector* has a disclosure norm problem.

Require at least 8 peers in a sub-industry; otherwise fall back to the GICS industry group and flag the fallback.

**2. Disclosure retreat.** Items at granularity ≥2 in year *T−1* and ≤1 in year *T*. Report the list, not just a count. Then join to the numeric time series in the existing engine and compute **retreat under pressure**: of the items dropped, what share had a deteriorating underlying value in the two years before they were dropped? That conditional share is the most quotable number this whole system will produce.

**3. Attention misallocation.** Classify each climate-related paragraph into one of the six pillars. Compute the observed share of report text per pillar, then:

```
AM(i) = KL( observed_share_i || MATERIALITY[sector_i] )
```

Report the per-pillar residuals too, not only the scalar — "forty pages on community engagement, three on process emissions" is the finding, and the scalar hides it.

**4. Evidence gap.** See Stage E.

---

## 9. Stage E — evidence gap

The strongest mechanism, because it is the only one where absence is provably meaningful rather than merely unusual. For each company, pull external records already available through `pipeline/fetch_free_sources.py` and ask whether the report acknowledges them:

| External evidence | Expected disclosure |
|---|---|
| EPA TRI release records above a threshold | toxic releases quantified; the named chemical or facility appears |
| EPA GHGRP facilities in high-stress Aqueduct basins | water in stressed basins |
| OSHA fatality or high TRIR at a named establishment | fatalities count; safety narrative |
| EPA ECHO enforcement action with assessed penalty | any acknowledgement of the action |
| Reported Scope 1 materially below GHGRP/Climate TRACE roll-up | methodology or boundary explanation |
| Sector where Scope 3 exceeds ~60% of footprint | Scope 3 quantified by category |

```
EG(i) = Σ_e severity(e) · unmentioned(e)  /  Σ_e severity(e)
```

Entity matching is the hard part and where the time goes. EPA uses FRS IDs and facility names, OSHA uses establishment names, SEC uses CIK. Build the crosswalk in a dedicated module, cache it, and **report match rate honestly** — an evidence gap computed on a 40% match rate is not a finding.

Only score `EG` where facility-level coverage exceeds 60%. Below that, flag rather than score. Joint ventures, tolling arrangements, and operational-control versus equity-share boundaries all produce apparent gaps that are not omissions.

---

## 10. Outputs

Per company, `ledger.parquet` and a JSON record:

```json
{
  "company": "...", "cik": "...", "sector": "...", "sub_industry": "...",
  "report": {"url": "...", "retrieved": "...", "sha256": "...", "pages": 112},
  "coverage": {"items_checked": 50, "items_applicable": 38, "items_found": 24},
  "scores": {
    "conditional_silence_peer": 0.41,
    "conditional_silence_index": 0.28,
    "attention_misallocation_kl": 0.63,
    "evidence_gap": 0.22,
    "evidence_gap_match_rate": 0.71,
    "cheap_talk": 0.37,
    "retreat_count": 3,
    "retreat_under_pressure_share": 0.67
  },
  "silence_ledger": [
    {"item": "scope3_category_breakdown", "found": false, "granularity": 0,
     "peer_coverage": 0.81, "index_coverage": 0.64, "material": true,
     "prior_year_granularity": 3, "retreat": true,
     "underlying_trend_before_drop": "+11%/yr"}
  ],
  "evidence_gaps": [
    {"source": "EPA TRI 2023", "facility": "...", "quantity_lb": 41200,
     "report_mentions_facility": false, "report_mentions_chemical": false,
     "match_confidence": 0.88}
  ]
}
```

Every entry must be traceable to a page number and a text span in the source PDF. If a judge or a company asks "where does that come from", the answer is a page reference, not a model output.

**The chart to produce:** x-axis cheap talk index, y-axis delivered decarbonisation rate minus required rate, point size = conditional silence, colour = evidence gap. Quiet achievers top-left, loud underperformers bottom-right.

---

## 11. Validation

Four tests, all of which must run in `validate.py` and appear in the output:

1. **Does silence predict the bad number?** For items where *some* companies disclose, is the disclosed value systematically worse among companies that nearly omitted it (low granularity)? If silence is uninformative, this shows nothing.
2. **Does retreat track deterioration?** Of items dropped, what share had a worsening underlying value beforehand? A null result here kills the retreat metric, and you should be willing to report that.
3. **Does CSS predict future adverse events?** Same AUC test `diagnostics.predictive_validity` already runs on the INTEGRITY pillar. Report AUC and n.
4. **Is this secretly a report-length ranking?** Regress every metric on log(page count) and log(market cap) with sector dummies. Large companies publish longer reports and disclose more. If CSS is mostly "this company published a short PDF", it is worthless. Report incremental R² from length and size exactly as `diagnostics.size_bias` does — and if it fails, fix it by normalising per-item detection against document length, not by changing the threshold.

Hand-label 200 item/report pairs for threshold calibration and report precision/recall per item. Items with recall below 0.7 should be dropped from the scored set and reported as unreliable rather than left in to add noise.

---

## 12. Constraints

- Python 3.11+, `uv` or `pip`. Pin versions in `requirements.txt`.
- SQLite for state, parquet for exports. No cloud dependencies.
- Every network call cached to disk with a TTL. Every stage resumable.
- Log all failures with reasons. Never silently skip.
- Deterministic seeds everywhere.
- No API keys required except PatentsView (free) — if a source needs a paid licence, do not use it.

---

## 13. Build order

Do not build the whole thing before anything runs.

**Milestone 1 (first)** — 10 hand-picked reports from 3 sectors, hard-coded URLs. Extract → paragraphs → 8 disclosure items via entailment → print a silence table. No corpus, no database, no peers. Prove the extraction and entailment work, by eye, on real documents. Report what fraction of items you got right against a manual read.

**Milestone 2** — Full item inventory (50) + threshold calibration on 200 hand-labelled pairs. Precision/recall per item.

**Milestone 3** — Corpus build. SEC EDGAR first, then the other routes. Report coverage.

**Milestone 4** — Peer and index baselines, CSS, attention misallocation.

**Milestone 5** — Multi-year: retreat and granularity decay.

**Milestone 6** — Evidence gap and the entity crosswalk.

**Milestone 7** — Validation suite and the talk-vs-walk chart.

If time runs out, a fully validated Milestone 4 beats a broken Milestone 7.

---

## 14. Failure modes to avoid

- Writing 3,000 lines before anything executes against a real PDF.
- Trusting PDF extraction without looking at the output by eye.
- Running transformers over the whole corpus before the prefilter and thresholds are calibrated.
- Inventing HuggingFace model identifiers or API endpoints. Verify each one resolves before pinning it; if a model in this brief has moved, search for the current identifier rather than guessing.
- Treating a low item-detection rate as a finding about companies when it is a finding about the detector. Calibrate first.
- Computing an evidence gap on a poor entity match rate.
- Filling gaps with plausible values so the pipeline runs cleanly. A crashed pipeline is recoverable; a silently fabricated dataset is not.
