# Chevron Corporation — 2023 report — disclosure audit

- **Sector (as used in this corpus):** Energy
- **Report edition:** 2023 — "2023 corporate sustainability report" (read off the document's own title page, not inferred from the filename)
- **Source document:** https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/c/NYSE_CVX_2023.pdf
- **Resolved to:** `https://206.189.187.49/HostedData/ResponsibilityReportArchive/c/NYSE_CVX_2023.pdf`
- **Retrieved:** 2026-09-12T14:35:28.733107Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 165,535 chars, sha256 `e8f2e862140e1d667878c681dbeb43bdf6611d65e72373fa13689515b23d67fc`
- **Local copy:** `absence/reports/cvx_energy_2023/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 232

**Agreement with the hand read: 2/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.381 | 0.20 | — | detected | not present | DISAGREES |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.262 | 0.50 | — | not detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.836 | 0.46 | 2 | not detected | not present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.034 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.989 | 0.80 | — | detected | not present | DISAGREES |
| `board_committee_climate_mandate` | INTEGRITY | 0.328 | 0.93 | — | not detected | not present | agrees |
| `injury_rate_trir` *(excluded)* | SOCIAL | 0.936 | 0.94 | — | not detected | unverified | — |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.042 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.381** against threshold 0.20
- Pipeline: **detected**  ·  hand read: **not present**  ·  DISAGREES
- Highest-scoring span came from chunk 48 of 232

> GHG mitigation projects Permian Basin, U.S.: We lowered the carbon intensity of our Permian Basin drilling and completion activities by replacing diesel as the primary fuel in drilling operations. Since the initiative began in 2020, we’ve saved $87 million and reduced approximately 270,000 tonnes of carbon dioxide equivalent (CO2e) emissions.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.262** against threshold 0.50
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 37 of 232

> introduction socialclimate environment governance performance targets to lower the carbon intensity of our operations $2.0 billion in carbon reduction projects from 2021 through 2028 $8.0 billion in lower carbon energy investments from 2021 through 2028 71 g CO₂e/MJ portfolio carbon intensity (Scope 1, 2 and 3) by 2028 24 kg CO₂e/boe gas carbon intensity (Scope 1 and 2) by 2028 36 kg CO₂e/boe refining carbon intensity (Scope 1 and 2) by 2028 24 kg CO₂e/boe oil carbon intensity (Scope 1 and 2) by 2028 planned capital allocation our outlook The world’s energy demand is greater now than at any time in human history. The world’s energy needs continue to grow as populations and incomes rise, urban areas expand, and billions of people in less-developed countries seek a higher standard of living.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.836** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 200 of 232

> Methane intensity The amount of methane per unit of measure.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.034** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 208 of 232

> Net zero upstream aspiration (Scope 1 and 2) Chevron aspires to reach net zero upstream emissions (Scope 1 and 2) by 2050.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.989** against threshold 0.80
- Pipeline: **detected**  ·  hand read: **not present**  ·  DISAGREES
- Highest-scoring span came from chunk 52 of 232

> In 2023, Chevron contracted GHGSat to monitor 18 onshore assets worldwide. verifying methane performance While methane detection technology is maturing, challenges remain in quantification accuracy.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.328** against threshold 0.93
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 150 of 232

> The Board also oversees Chevron’s strategic and business planning process and related climate and sustainability matters. executive committee The Executive Committee comprises corporate officers and is chartered by the Board of Directors to carry out policies in managing the company’s business.

## `injury_rate_trir`

*The company disclosed a numeric total recordable incident rate (TRIR) or equivalent workplace injury rate statistic.*

- Score **0.936** against threshold 0.94
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Cannot be validated: only 3 labelled cells (Energy-only item) and all 3 are positive, so there are no negatives and the base rate is 1.00.
- Highest-scoring span came from chunk 113 of 232

> In 2023, we experienced 17 Tier 1 LOC events, which repre- sents an improvement over the previous two years. Chevron safety performance (Process) Safety fundamentals Chevron is a member of IOGP and participates in several of its committees.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.042** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 195 of 232

> This report builds on our previous editions and has updates throughout as we outline our governance framework, risk management, strategy, portfolio, performance and policy, and metrics.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
