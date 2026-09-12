# Microsoft Corporation — disclosure audit

- **Sector (as used in this corpus):** Technology
- **Source document:** https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/m/NASDAQ_MSFT_2022.pdf
- **Resolved to:** `https://206.189.187.49/HostedData/ResponsibilityReportArchive/m/NASDAQ_MSFT_2022.pdf`
- **Retrieved:** 2026-09-12T14:35:28.727398Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 232,714 chars, sha256 `0449c87f16ec3317da5ce7ac38fa086a5bd017071518161bd32b907402812624`
- **Local copy:** `absence/reports/msft_technology/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 329

**Agreement with the hand read: 4/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.078 | 0.20 | — | not detected | not present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.931 | 0.50 | — | detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.974 | 0.46 | 2 | not detected | not present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.970 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.805 | 0.80 | — | detected | present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.966 | 0.93 | — | detected | present | agrees |
| `injury_rate_trir` | SOCIAL | — | — | — | n/a (not material for Technology) | — | |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.139 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.078** against threshold 0.20
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 47 of 329

> Scope 1A Current year Base year Metric tons CO2e Scope 2B Scope 3C 0M 3M 6M 9M 12M 15M FY21 FY20 FY22 B C C C A A A B 12,511,000 10,870,000 12,571,000 429,405 123,704 456,119 118,100 288,029 139,413 B -8M -6M -4M -2M 0M 2M 4M 6M 8M 10M 12M 14MMetric tons CO2e FY21FY22 Current year FY20 Base year FY30 Target year A Microsoft emissions Retirements from avoided emissionsB B E Retirements from carbon removalC Projected carbon removalEContracted carbon removalD C CC DD A A A A Carbon Table 1 Tracking our yearly progress toward carbon negative by 2030 In FY22, we procured 1.44 million metric tons and retired 514,156 metric tons of carbon removal as part of our effort toward achieving our annual carbon commitment to be carbon neutral. Carbon removal contracted each year includes credits retired in the same year and to be retired in future years.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.931** against threshold 0.50
- Pipeline: **detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 39 of 329

> Our total company emissions were just under 13 million metric tons of carbon dioxide equivalents (mtCO2e) (market- based and management-defined criteria for Scope 3 Category 11). Taking into account our renewable energy purchases, our Scope 1 and 2 emissions were approximately 428,000 mtCO2e.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.974** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 50 of 329

> Scope 3 Categories Waste Purchased Goods & Services Capital Goods Fuel-and Energy-Related Activities (Market-Based) Upstream Transportation Business Travel Employee Commuting Downstream Transportation Use of Sold Products End of Life of Sold Products Downstream Leased Assets 47.24% 30.97% 3.46% 1.85% 0.06% 1.07% 1.08% 0.53% 10.25% 0.14% 0.06% 96.71% Scope 3Scope 1 1.07% Scope 2 2.22% Carbon Table 3 Breaking down our FY22 Scope 3 emissions by source Microsoft’s Scope 3 emissions account for more than 96 percent of our total emissions, with the vast majority of these emissions coming from two categories upstream, Purchased Goods and Services (Category 1) and Capital Goods (Category 2), and one downstream, Use of Sold Products (Category 11).

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.970** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 43 of 329

> Commitments and progress Carbon negative by 2030 We are committed to being carbon negative by 2030 and by 2050 remove from the atmosphere an equivalent amount of all the carbon dioxide our company has emitted either directly or by our electricity consumption since we were founded in 1975.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.805** against threshold 0.80
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 326 of 329

> crosoft which provide an objective basis for measuring and reporting metrics as specified in section 1.10 of our Environmental Data Fact Sheet. 4.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.966** against threshold 0.93
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- Highest-scoring span came from chunk 322 of 329

> Governance The Environmental, Social, and Public Policy Committee of Microsoft's Board of Directors provides oversight and guidance on Microsoft's environmental sustainability strategy and commitments. During at least one meeting each year and on an as-needed basis, our President and Vice Chair and our Chief Environmental Officer present to this committee on our overall sustainability agenda, including our climate-related work, and solicit high-level input on new and emerging initiatives.

## `injury_rate_trir`

Not material for Technology in this inventory; not scored.

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.139** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 298 of 329

> Transform to Net Zero (TONZ) Microsoft is a founding member of TONZ, a cross- sector initiative to accelerate the transition to an inclusive net zero global economy. The group's 2025 goal is for the world's largest 1,000 companies to have targets backed up by transformation plans to achieve net zero no later than 2050.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
