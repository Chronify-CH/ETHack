# JPMorgan Chase & Co. — 2024 report — disclosure audit

- **Sector (as used in this corpus):** Financials
- **Report edition:** 2024 — "Sustainability Report 2024" (read off the document's own title page, not inferred from the filename)
- **Source document:** https://www.jpmorganchase.com/content/dam/jpmorganchase/documents/about/jpmc-sustainability-report-2024.pdf
- **Resolved to:** `https://23.211.139.209/content/dam/jpmorganchase/documents/about/jpmc-sustainability-report-2024.pdf`
- **Retrieved:** 2026-09-12T14:35:28.743463Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 261,455 chars, sha256 `d4a29d7b8e543413ecb2b2525aa9f8fda8046fb424d1870e38bb96c8c6d4036a`
- **Local copy:** `absence/reports/jpm_financials_2024/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 368

**Agreement with the hand read: 3/3 scored items** (3 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.203 | 0.20 | — | detected | present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.630 | 0.50 | — | detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.105 | 0.46 | 2 | not detected | not present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.178 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.094 | 0.80 | — | not detected | not present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.008 | 0.93 | — | not detected | unverified | — |
| `injury_rate_trir` | SOCIAL | — | — | — | n/a (not material for Financials) | — | |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.938 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.203** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 98 of 368

> The table on the right summarizes our 2024 operational GHG emissions. 2024 2023 GHG emissions (tCO2e) Scope 1 GHG emissionsi 100,024 115,294 Natural gas 49,354 48,232 Propane 50 50 Fuel oil 422 420 Jet fuel 12,414 13,059 Fugitive emissionsii 33,121 48,658 Diesel 2,384 2,855 Fleet 1,627 1,892 Other energy useiii, iv 652 128 Scope 2 GHG emissions (location-based)i 773,852 792,479 Purchased electricity 767,046 788,837 Purchased steam, district heat and chilled wateriv

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.630** against threshold 0.50
- Pipeline: **detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 101 of 368

> Includes Scope 1 and Scope 2 (location-based) GHG emissions; tCO2e/million USD revenue. vi. Market-based emissions for purchased electricity are reported as zero due to the purchase of renewable electricity through unbundled EACs and contractual instruments, including PPAs, virtual pow er purchase agreements and renewable electricity supply contracts. vii.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.105** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 126 of 368

> loyees Risk management Governance Appendices Supporting secure and affordable energy and a transition to a low-carbon economy PORTFOLIO DETAILS BASELINEi TARGET JPMORGANCHASE PROGRESS Scope(s) included Unit of measurement Baseline year Portfolio carbon intensity baseline Portfolio carb on intensity as of December 31, 202 Change in portfolio carbon intensity from baselineii Energy Mixiii Scope 3 (end use) gCO2 / MJ 2019 45.9 29.5 -36% from baseline 30.6 -33.2% Oil & Gas Operational Scopes 1 and 2 gCO2e / MJ 2019 4.9 -45.0% from baseline 4.0 -17.2% Electric Power Scope 1 kgCO2 / MWh 2019 342.6 105.3 -69% from baseline 248.4 -2 7.5% Auto Manufacturing Scopes 1, 2 and 3 (tank-to-wheel) gCO2e / km 2019 164.8 86.1 -48% from baseline 131.3 -20.3% Aviation Scope 1 (tank-to-wake) gCO2 / RTK 2021 972.6 625.0 -36% from baseline 777 .3 -20.1% Shipping Scope 1 (tank-to-wake) gCO2 / t-nm 2021 10.9 (re

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.178** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 119 of 368

> We constructed our targets for 2030 as portfolio-level targets by sector, using output-based emissions intensity metrics and aligned to the International Ener gy Agency’s Net Zero Emissions by 2050 scenario21. We set targets using our own independent assessment of what we determined to be reasonable and science-based, and what would serve the best interests of our business and clients.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.094** against threshold 0.80
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 99 of 368

> 2 128 Scope 2 GHG emissions (location-based)i 773,852 792,479 Purchased electricity 767,046 788,837 Purchased steam, district heat and chilled wateriv 6,806 3,642 Scope 1 GHG emissions + Scope 2 GHG emissions (location-based) 873,876 907 ,773 GHG emissions intensityv 4.9 5.7 Scope 2 GHG emissions (market-based)i 6,806 3,642 Purchased electricityvi — — Purchased steam, district heat and chilled wateriv 6,806 3,642 Scope 1 GHG emissions + Scope 2 GHG emissions (market-based)i 106,830 118,936 Verified carbon credits i, vii 367,311 374,417 2024 2023 Electric power (MWh) Electricity production (on-site solar) 57,420 47,4 43 Purchased electricityi 2,041,374 2,016,262 Purchased renewable electricityi, ii 2,041,374 2,016,262 i. We engaged an external third-party to perform a limited assurance engagement over these metrics presented for 2023 and 2024.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.008** against threshold 0.93
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- Highest-scoring span came from chunk 237 of 368

> The information in this table is not considered when making employment decisions. As of December 31, 2024 T otal employees Senior level emplo yees 35 Operating Committee Board of Directors Race/Ethnicity36 White 43% 74% 86% 80% Hispanic 21% 6% 7% —% Asian 20% 14% 7% —% Black 13% 5% —% 20% Other37 3% 1% —% —% Gender38 Men 51% 71% 53% 50% Women 49% 29% 47% 50% LGBTQ+39 4% 2% 7% —% Military veterans39 3% 2% —% 10% People with Disabilities39 5% 3% —% —%40 35 Senior level employees represents employees with the titles of Managing Director and above. 36 Based on EEO metrics.

## `injury_rate_trir`

Not material for Financials in this inventory; not scored.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.938** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 303 of 368

> Additionally, companies may need to increase their capital expenditures through investments that improve resilience to a low-carbon transition (e.g., power companies investing in renewables). For clients operating in sectors more vulnerable to transition risk (e.g., Oil & Gas, Automotive Manufacturing, Power G eneration, Aviation, Steel and Cement Manufacturing), the Firm estimates the potential impact of a climate transition scenario on their credit rating by projecting detailed cashflows within the context of a transition scenario (refer to Scenario Analysis on page 51).

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
