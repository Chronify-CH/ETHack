# ConocoPhillips — 2022 report — disclosure audit

- **Sector (as used in this corpus):** Energy
- **Report edition:** 2022 — "Sustainability Report 2022" (read off the document's own title page, not inferred from the filename)
- **Source document:** https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/c/NYSE_COP_2022.pdf
- **Resolved to:** `https://206.189.187.49/HostedData/ResponsibilityReportArchive/c/NYSE_COP_2022.pdf`
- **Retrieved:** 2026-09-12T14:35:28.739339Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 536,681 chars, sha256 `91197559a339fdb645f0fdf6f4b315e317470a47f2b5f4152952382d5edd1445`
- **Local copy:** `absence/reports/cop_energy_2022/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 754

**Agreement with the hand read: 4/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.904 | 0.20 | — | detected | present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.966 | 0.50 | — | detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.091 | 0.46 | 2 | not detected | not present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.889 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.898 | 0.80 | — | detected | present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.939 | 0.93 | — | detected | present | agrees |
| `injury_rate_trir` *(excluded)* | SOCIAL | 0.976 | 0.94 | — | detected | present | agrees |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.956 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.904** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 720 of 754

> INDICATOR UNITS 2021 2022 1. Direct GHG Emissions (Scope 1) 1.1 Direct GHG Emissions (Scope 1) – All GHGs million metric tons CO2e 17.7 15.0 1.1.1 Upstream – All GHGs million metric tons CO2e 15.3 12.5 1.1.1.1 Methane (CH4) million metric tons CO2e 1.7 1.7 1.1.1.2 Upstream Flaring – All GHGs (subset of Direct GHG Emissions – Scope 1) million metric tons CO2e 1.9 1.5 1.1.1.3 Volume of Flares mmcf 19,615 17,182 1.1.2 Midstream – All GHGs million metric tons CO2e n/a n/a 1.1.2.1 Methane (CH4) million metric tons CO2e n/a n/a 1.1.3 Downstream – All GHGs million metric tons CO2e n/a n/a 1.1.4 LNG – All GHGs million metric tons CO2e 2.1 2.1 1.1.5 Oil and Natural Gas Field Services – All GHGs million metric tons CO2e 0.3 0.3 2.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.966** against threshold 0.50
- Pipeline: **detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 721 of 754

> Indirect GHG Emissions from Imported Energy (Scope 2) 2.1 Indirect GHG Emissions from Imported Electricity + Heat + Steam + Cooling (Scope 2, Market-based) 1.03 1.06 2.1.1 Upstream – All GHGs million metric tons CO2e 1.01 1.06 2.1.2 Midstream – All GHGs million metric tons CO2e n/a n/a 2.1.3 Downstream – All GHGs million metric tons CO2e n/a n/a 2.1.4 LNG – All GHGs million metric tons CO2e 0 0 2.1.5 Oil and Natural Gas Field Services – All GHGs million metric tons CO2e 0.02 0.002 3. GHG Mitigation 3.1 GHG Mitigation from CCUS, Credits, and Offsets million metric tons CO2e n/a n/a 3.1.1 Carbon Capture Utilization and Storage (CCUS) – All GHGs million metric tons CO2e n/a n/a 3.1.2 Renewable Energy Credits – (RECs for Indirect Emissions) – All GHGs million metric tons CO2e n/a n/a 3.1.3 Offsets – All GHGs million metric tons CO2e n/a n/a 4.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.091** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 197 of 754

> Similarly, in response to previous years’ increased wildfire activity in Alberta, our Surmont team undertook reactive forest fuel reductions near critical infrastructure and completed a Fire Smart hazard assessment where we are working on an integrated land management plan with a local forest company to strategically reduce forest fuel loading in areas of future infrastructure development. We have 4 Upstream Scope 3 emissions covered under the strategy include Category 1, purchased goods and services and Category 2, capital goods.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.889** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 269 of 754

> These targets include: Achieving our stated ambition to reach net‑zero emissions for Scope 1 and 2 emissions by 2050. Strengthening our previously announced operational GHG emissions intensity reduction target to 50‑60% by 2030 on both a gross operated and net equity basis.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.898** against threshold 0.80
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 730 of 754

> Limited assurance1 is performed by an external third party, ERM CVS, on all environmental metrics as well as reasonable assurance2 in countries with a regulatory requirement to verify reported greenhouse gas (GHG) emissions and energy (where relevant), including Australia, Canada and Norway.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.939** against threshold 0.93
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 24 of 754

> Reviewing and endorsing agenda and meeting content for the Public Policy and Sustainability Committee (PPSC) of the board. The SPEC is also the governance link to the PPSC, whose oversight covers SD matters including climate and nature related risks.

## `injury_rate_trir`

*The company disclosed a numeric total recordable incident rate (TRIR) or equivalent workplace injury rate statistic.*

- Score **0.976** against threshold 0.94
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated: only 3 labelled cells (Energy-only item) and all 3 are positive, so there are no negatives and the base rate is 1.00.
- Highest-scoring span came from chunk 659 of 754

> Including lost workday cases related to COVID‑19, our 2022 total recordable rate (TRR) was 0.28. Excluding COVID‑19 cases, our TRR was 0.14.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.956** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 138 of 754

> IEA estimates this to average $394 billion each year from 2022 to 2050 globally in the Announced Pledges Scenario (APS) and $255 billion per year from 2022 to 2050 in the Net Zero Emissions scenario, a total of approximately $11.4 trillion globally and $7 .4 trillion respectively for the period 2022 to 2050. Achieving the IEA APS (limiting temperature to 1.7 degrees Celsius) requires significant progress on several fronts:1 Improving energy efficiency of power generation, transportation and industrial processes.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
