# Bank of America — disclosure audit

- **Sector (as used in this corpus):** Financials
- **Source document:** https://about.bankofamerica.com/content/dam/about/report-center/esg/2025/SustainabilityatBofA2025_WCAG2.2_121625.pdf
- **Resolved to:** `https://23.211.139.198/content/dam/about/report-center/esg/2025/SustainabilityatBofA2025_WCAG2.2_121625.pdf`
- **Retrieved:** 2026-09-12T14:35:28.744637Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 230,222 chars, sha256 `bb4370c23de4122ab5f67093ac27d9166d4a630bc4fa640c2d3d4d6414fb317d`
- **Local copy:** `absence/reports/bac_financials/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 324

**Agreement with the hand read: 4/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.203 | 0.20 | — | detected | present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.046 | 0.50 | — | not detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.771 | 0.46 | 2 | detected | present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.809 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.010 | 0.80 | — | not detected | not present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.966 | 0.93 | — | detected | present | agrees |
| `injury_rate_trir` | SOCIAL | — | — | — | n/a (not material for Financials) | — | |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.073 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.203** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 207 of 324

> All of the environmental metrics we disclose in the following pages undergo internal review, controls and governance and several undergo third-party verification each year (see bankofamerica.com/sustainabilityreports). GHG emissions Units 2010 (baseline) 2022 2023 2024 Scope 1 and location-based Scope 2 emissions Scope 1 direct emissions Metric tons CO2e 106,870 66,775 68,050 65,763 Location-based Scope 2 indirect emissions Metric tons CO2e 1,678,547 634,510 610,013 617,413 Total Scope 1 and location-based Scope 2 emissions Metric tons CO2e 1,78

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.046** against threshold 0.50
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 209 of 324

> 9 0 0 0 Reduction in total net Scope 1 and market-based Scope 2 emissions Percent decrease from base year Not applicable 100% 100% 100% Scope 3 indirect emissions Category 1 - Purchased goods and services Metric tons CO2e Not available 1,571,077 1,722,654 1,625,076 Category 2 - Capital goods Metric tons CO2e Not available 47,621 48,570 35,375 Category 3 - Fuel and energy-related activities Metric tons CO2e 341,783 164,599 168,018 150,799 Category 4 - Upstream transportation and distribution Metric tons CO2e 243,881 176,322 152,752 147,437 Category 5 - Waste (traditional disposal) Metric tons CO2e Not available 18,826 18,406 19,090 Category 6 - Business travel Metric tons CO2e 189,977 82,583 92,818 96,359 Business Travel Carbon Credits Retired Metric tons CO2e 0 80,172 92,819 96,359 Total Net Scope 3 Business Travel Emissions Metric tons CO2e 189,977 2,411 0 0 Category 7 - Employee commut

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.771** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 40 of 324

> Utilize sustainable aviation fuel (SAF) for at least 20% of the company’s total annual corporate and commercial jet fuel usage, equivalent to 100% of corporate jet fuel and a significant percentage of fuel associated with employee travel on commercial airlines. Financing activity Auto manufacturing Reduce intensity by 48% by 2030 (gCO2e/km Scopes 1, 2 and 3 end use) from 2019 baseline.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.809** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 179 of 324

> ry 2030 financing activity targets as a part of our Net Zero Goal for the following sectors: auto manufacturing, aviation, cement, energy, iron and steel, maritime shipping and power generation.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.010** against threshold 0.80
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 180 of 324

> Calculations disclosed herein were subject to multiple levels of review and challenge as well as third- party limited assurance review and validation - the resulting Environmental Assurance Statements can be found on bankofamerica.com/sustainabilityreports.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.966** against threshold 0.93
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 166 of 324

> The Board’s Enterprise Risk Committee oversees risk and receives updates on our company’s risk management efforts, including periodically on climate risk. The Board and the ERC receive risk reporting on key and emerging risks.

## `injury_rate_trir`

Not material for Financials in this inventory; not scored.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.073** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 154 of 324

> Operational risk is the risk of loss resulting from inadequate or failed int

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
