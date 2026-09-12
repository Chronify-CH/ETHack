# Alphabet Inc. (Google) — disclosure audit

- **Sector (as used in this corpus):** Technology
- **Source document:** https://www.gstatic.com/gumdrop/sustainability/google-2024-environmental-report.pdf
- **Retrieved:** 2026-09-12T14:35:28.729376Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 355,405 chars, sha256 `f76f7c2a40f90ec0cd8664fc248d0411ffd99fc2b522877d45e270cb1fe15678`
- **Local copy:** `absence/reports/googl_technology/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 492

**Agreement with the hand read: 2/3 scored items** (3 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.652 | 0.20 | — | detected | present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.985 | 0.50 | — | detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.973 | 0.46 | 2 | detected | present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 1.000 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.860 | 0.80 | — | detected | not present | DISAGREES |
| `board_committee_climate_mandate` | INTEGRITY | 0.414 | 0.93 | — | not detected | unverified | — |
| `injury_rate_trir` | SOCIAL | — | — | — | n/a (not material for Technology) | — | |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.039 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.652** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 126 of 492

> l- and energy-related activities (not included in Scope 1 or 2) 1,186,000 8% Scope 3: (4) Upstream transportation 584,000 4% Scope 3: (5) Waste generated in operations 10,000 <1% Scope 3: (6) Business travel 283,000 2% Scope 3: (7) Employee commuting (including teleworking) 113,000 <1% Scope 3: Other categories 2,993,000 21% Scope 3 (total) 10,812,000 75% Total emissions 14,314,800 100% Scope 1 emissions In 2023, our Scope 1 emissions were approximately 79,400 tCO2e, representing approximately 1% of our total carbon footprint. Compared to 2022, we reduced our Scope 1 emissions by 13% due to building electrification and decreases in emissions from transportation and data center generator use.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.985** against threshold 0.50
- Pipeline: **detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 122 of 492

> Target year: 2030 2023 PROGRESS Emissions reductions: Total GHG emissions were 14.3 million tCO 2e, representing a 48% increase compared to 2019 Residual emissions: Signed offtake deals for approximately 62,500 tCO 2e of removal credits TREND Emissions reductions: In 2023, our total GHG emissions increased 13% year-over- year, partially driven by a 37% year-over-year increase in our Scope 2 (market-based) emissions.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.973** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 375 of 492

> 1.0), in the following categories identified as relevant: Category 1: Purchased goods and services Category 2: Capital goods Category 3: Fuel- and energy-related activities not included in Scope 1 or Scope 2 Category 4: Upstream transportation and distribution Category 5: Waste generated in operations Category 6: Business travel Category 7: Employee commuting, including teleworking Category 11: Use of sold products Category 12: End-of-life treatment of sold products None of the Scope 3 categories have associated biogenic CO 2 emissions. For all reported Scope 3 categories, we report emissions according to their minimum boundaries listed by the Greenhouse Gas Protocol.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **1.000** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 112 of 492

> In 2021, we set an ambitious goal to reach net- zero emissions across all of our operations and value chain by 2030. We’re working toward this goal in two key ways: first, we’re focused on reducing emissions across our operations and value chain (including advancing 24/7 CFE), and after reducing our emissions, we’re addressing our residual emissions with carbon removals (see Figure 15).

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.860** against threshold 0.80
- Pipeline: **detected**  ·  hand read: **not present**  ·  DISAGREES
- Highest-scoring span came from chunk 376 of 492

> To calculate full supply chain emissions generated from manufacturing consumer devices, we perform third-party-verified Life Cycle Assessments (LCAs) in accordance with ISO 14040 and ISO 14044. To calculate emissions generated from our food program, we use LCA emission factors from WRI and annual procurement volumes from our offices.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.414** against threshold 0.93
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- Highest-scoring span came from chunk 77 of 492

> This powers the emissions estimates you see on Google Flights as well as other leading travel sites through our work in the Travalyst coalition. We’ve seen positive industry adoption of our model in aviation and, in 2023, we formalized our efforts by establishing an independent advisory committee to oversee future changes to the TIM.

## `injury_rate_trir`

Not material for Technology in this inventory; not scored.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.039** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 14 of 492

> pabilities can have a meaningful impact.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
