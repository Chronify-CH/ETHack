# Apple Inc. — disclosure audit

- **Sector (as used in this corpus):** Technology
- **Source document:** https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2023.pdf
- **Retrieved:** 2026-09-12T14:35:28.718372Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 405,050 chars, sha256 `07258e011e9c5846773c83bdeec524283bc662b0080caadb8b7188052b42fea9`
- **Local copy:** `absence/reports/apple_technology/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 594

**Agreement with the hand read: 4/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.843 | 0.20 | — | detected | present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.937 | 0.50 | — | detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.461 | 0.46 | 2 | detected | present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.943 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.987 | 0.80 | — | detected | present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.028 | 0.93 | — | not detected | not present | agrees |
| `injury_rate_trir` | SOCIAL | — | — | — | n/a (not material for Technology) | — | |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.080 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.843** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 381 of 594

> hout offsets) (metric tons CO2e)12 20,600,000 23,200,000 22,600,000 25,100,000 25,200,000 Total net carbon footprint (after applying offsets) (metric tons CO2e)12 20,300,000 22,530,000 22,530,000 25,100,000 25,200,000 Notes: For data on years prior to 2018, please reference past Environmental Progress Reports. T otals might not add up due to rounding. 1 Apple’s carbon footprint boundary is aligned with the Greenhouse Gas (GHG) Protocol framework and includes emissions that are material and relevant to Apple, where data is available.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.937** against threshold 0.50
- Pipeline: **detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 379 of 594

> 2e)2 Gross emissions 324,100 166,380 334,430 573,730 586,170 Scope 1 55,200 55,200 47,4 30 52,730 57 ,440 Natural gas, diesel, propane 39,700 40,070 39,340 40,910 42,840 Fleet vehicles 12,600 12,090 4,270 6,950 11,110 Other emissions3 2,900 3,040 3,830 4,870 3,490 Scope 2 (market-based)4 3,000 2,780 0 0 8,730 Electricity 0 0 0 0 8,730 Steam, heating, and cooling5 3,000 2,780 0 0 0 Scope 3 265,800 108,400 287 ,000 521,000 520,000 Business travel 113,500 22,850 153,000 326,000 337 ,000 Employee commute6 134,200 85,570 134,000 195,000 183,000 Upstream fuel 10,600 0 0 0 0 Work from home (market-based) 7,5 0 0 0 0 0 0 Transmission and distribution loss (market-based) 0 N/A N/A N/A N/A Third-party cloud (market-based) 0 0 0 0 0 Carbon removals Corporate carbon offsets7 –324,100 –167 ,0008 –70,0009 0 0 Product life cycle emissions (metric tons CO2e)10 Gross emissions (Scope 3) 20,280,000 23,020

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.461** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 569 of 594

> business commute, work from home, and third-party cloud services. 2 Apple follows the GHG Protocol Corporate Accounting and Reporting Standard (GHG Protocol) to calculate value chain emissions. The GHG Protocol defines scope 1 emissions as direct greenhouse gas emissions that occur from sources that are owned or controlled by the company; scope 2 emissions as the indirect greenhouse gas emissions from the generation of purchased electricity, steam, heat, and cooling consumed by the company; and scope 3 emissions as all “other indirect emissions” that occur in the value chain of the reporting company, including both upstream and downstream emissions.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.943** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 26 of 594

> We’ve committed to achieving carbon neutrality across our entire value chain by 2030 — reducing emissions by 75 percent compared with 2015 and balancing the residual emissions with high-quality carbon removal.7 This means that our goal to be carbon neutral also extends to all our products.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.987** against threshold 0.80
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 457 of 594

> chain was 10.6 gigawatts, generating 18.6 million megawatt-hours and avoiding 14.2 million metric tons of carbon emissions. 2 Apple’s independent assurance provider for the Supplier Clean Energy Program conducts work against standard procedures and guidelines for external verification of sustainability reports, based on current best practice in independent assurance.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.028** against threshold 0.93
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 158 of 594

> These include our role on the steering committee of the Responsible Minerals Initiative (RMI).

## `injury_rate_trir`

Not material for Technology in this inventory; not scored.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.080** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 45 of 594

> For example, in 2022, we expanded our corporate footprint to include work from home emissions, third-party cloud services, electricity transmission and distribution losses, and upstream impacts from scope 1 fuels.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
