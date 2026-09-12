# ExxonMobil — disclosure audit

- **Sector (as used in this corpus):** Energy
- **Source document:** https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/e/NYSE_XOM_2023.pdf
- **Resolved to:** `https://206.189.187.49/HostedData/ResponsibilityReportArchive/e/NYSE_XOM_2023.pdf`
- **Retrieved:** 2026-09-12T14:35:28.729765Z via TinyFish fetch_content (extracted text; raw PDF bytes not available)
- **Extracted text:** 37,080 chars, sha256 `8e3ebd6101d75084b3832dd6acb2f6e38296db5cc1e8efa446ee4b4983f75df6`
- **Local copy:** `absence/reports/xom_energy/source.txt` (the exact bytes scored below)
- **Paragraph chunks after rechunk():** 54

**Agreement with the hand read: 4/4 scored items** (4 of this document's cells are both validated and hand-labelled; the rest are excluded or unverified and are listed but not counted).

| item | pillar | score | threshold | gate | decision | hand read | |
|---|---|---:|---:|---:|---|---|---|
| `scope1_absolute` | INTEGRITY | 0.077 | 0.20 | — | not detected | not present | agrees |
| `scope2_market_based` *(excluded)* | INTEGRITY | 0.042 | 0.50 | — | not detected | unverified | — |
| `scope3_category_breakdown` | INTEGRITY | 0.328 | 0.46 | 2 | not detected | not present | agrees |
| `target_net_zero_year` *(excluded)* | TRAJECTORY | 0.087 | 0.03 | — | detected | present | agrees |
| `assurance_provider_named` | INTEGRITY | 0.007 | 0.80 | — | not detected | not present | agrees |
| `board_committee_climate_mandate` | INTEGRITY | 0.003 | 0.93 | — | not detected | not present | agrees |
| `injury_rate_trir` *(excluded)* | SOCIAL | 0.941 | 0.94 | — | detected | present | agrees |
| `scenario_analysis_quantified` *(excluded)* | OPTIONALITY | 0.843 | 0.99 | — | not detected | not present | agrees |

`score` is P(entailment) from the highest-scoring sentence window in the top-8 BM25 chunks. `gate` is the minimum number of distinct anchor terms that must appear next to a figure before the item can fire, which can override a score above threshold. Items marked *(excluded)* failed validation and may not feed any aggregate — their rows are shown so the evidence stays auditable.

---

## `scope1_absolute`

*The company disclosed its absolute Scope 1 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.077** against threshold 0.20
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 32 of 54

> echnical or operational difficulties; the outcome of research efforts and future technology developments, including the ability to scale projects and technologies such as electrification of operations, advanced recycling, CCS, hydrogen production, or direct lithium extraction on a commercially competitive basis; availability of feedstocks for lower-emission fuels, hydrogen, or advanced recycling; changes in the relative energy mix across activities and geographies; the actions of competitors; changes in regional and global economic growth rates and consumer preferences; actions taken by governments and consumers resulting from a pandemic; changes in population growth, economic development or migration patterns; military build-ups, armed conflicts, or terrorism; and other factors discussed in this release and in Item 1A.

## `scope2_market_based`

*The company disclosed its market-based Scope 2 greenhouse gas emissions in tonnes of CO2 equivalent.*

- Score **0.042** against threshold 0.50
- Pipeline: **not detected**  ·  hand read: **unverified**  ·  —
- **EXCLUDED from scored output.** Never validated: no labelled cells exist for this item, so neither precision nor recall is known.
- Highest-scoring span came from chunk 43 of 54

> ExxonMobil has also provided links in this report to third-party websites for ease of reference. ExxonMobil’s use of the third-party content is not an endorsement or adoption of such information.

## `scope3_category_breakdown`

*The company reported a numeric breakdown of its Scope 3 greenhouse gas emissions across individual GHG Protocol categories, giving separate figures for categories such as purchased goods and services, business travel, or use of sold products, rather than a single combined Scope 3 total.*

- Score **0.328** against threshold 0.46, structural gate ≥2 anchors with an adjacent figure
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 17 of 54

> Our scientists and product stewardship professionals collaborate with industry and academic researchers, regulatory bodies, and policy makers to help ensure that the best available science informs industry product safety policy. We work to identify and manage risks associated with our products and to avoid the manufacture and sale of products that cannot meet an appropriate level of safety for people and the environment.

## `target_net_zero_year`

*The company disclosed a specific target year by which it aims to reach net-zero greenhouse gas emissions.*

- Score **0.087** against threshold 0.03
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus: all 10 companies state a target year, so there are no negative examples and precision is unmeasurable. Needs a corpus containing companies that do not state one.
- Highest-scoring span came from chunk 39 of 54

> Actions needed to advance ExxonMobil’s 2030 greenhouse gas emission-reductions plans are incorporated into its medium-term business plans, which are updated annually. The reference case for planning beyond 2030 is based on the Company’s Global Outlook research and publication.

## `assurance_provider_named`

*The company named the specific third-party firm that provided external assurance or verification over its reported emissions data.*

- Score **0.007** against threshold 0.80
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 35 of 54

> See “ABOUT THE ADVANCING CLIMATE SOLUTIONS AND SUSTAINABILITY REPORTS” at the end of this document for additional information on these reports and the use of non-GAAP and other financial measures. ABOUT THE ADVANCING CLIMATE SOLUTIONS AND SUSTAINABILITY REPORTS The Advancing Climate Solutions Report contains terms used by the TCFD, as well as information about how the disclosures in this report are consistent with the recommendations of the TCFD.

## `board_committee_climate_mandate`

*The company disclosed that a specific board committee holds explicit oversight responsibility for climate-related risks.*

- Score **0.003** against threshold 0.93
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- Highest-scoring span came from chunk 32 of 54

> echnical or operational difficulties; the outcome of research efforts and future technology developments, including the ability to scale projects and technologies such as electrification of operations, advanced recycling, CCS, hydrogen production, or direct lithium extraction on a commercially competitive basis; availability of feedstocks for lower-emission fuels, hydrogen, or advanced recycling; changes in the relative energy mix across activities and geographies; the actions of competitors; changes in regional and global economic growth rates and consumer preferences; actions taken by governments and consumers resulting from a pandemic; changes in population growth, economic development or migration patterns; military build-ups, armed conflicts, or terrorism; and other factors discussed in this release and in Item 1A.

## `injury_rate_trir`

*The company disclosed a numeric total recordable incident rate (TRIR) or equivalent workplace injury rate statistic.*

- Score **0.941** against threshold 0.94
- Pipeline: **detected**  ·  hand read: **present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated: only 3 labelled cells (Energy-only item) and all 3 are positive, so there are no negatives and the base rate is 1.00.
- Highest-scoring span came from chunk 23 of 54

> ExxonMobil's Core Values 33% overall board diversity as of May 31, 2023 >50% increase in women and minority executives from 2016 to 2022 0.02 LTIR our industry-leading lost-time incident rate per 200,000 work hours ~12,000 internal job rotations in support of development plans

## `scenario_analysis_quantified`

*The company estimated, using climate scenario analysis, a specific monetary amount of financial impact on its business -- for example expected losses, asset write-downs, or costs expressed in dollars under a named climate scenario.*

- Score **0.843** against threshold 0.99
- Pipeline: **not detected**  ·  hand read: **not present**  ·  agrees
- **EXCLUDED from scored output.** Cannot be validated on this corpus and still produces false positives: no company here attaches a monetary figure to scenario-analysis results, so there are zero positives and recall is undefined. The rewrite cut false positives at the old 0.5 cut from 7 to 4, but 4 remain (ExxonMobil 0.843, ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655).
- Highest-scoring span came from chunk 33 of 54

> “Risk Factors” in ExxonMobil’s Annual Report on Form 10-K for 2022 and subsequent Quarterly Reports on Forms 10-Q, as well as under the heading “Factors Affecting Future Results” on the Investors page of ExxonMobil’s website at www.exxonmobil.com. The Advancing Climate Solutions Report includes 2022 greenhouse gas emissions performance data and Scope 3 Category 11 estimates for full-year 2022 as of March 1, 2023.

---

**Reading this file.** "not detected" means this detector did not find a qualifying passage in this document. It is not a claim that the company failed to disclose the item, and not a claim about intent. Where the hand read column says `unverified`, the cell was deliberately left unlabelled rather than guessed. Method, known faults and the per-item reliability figures are in `absence/HOW_TO_READ_RESULTS.md`, `absence/FAULTS.md` and `absence/PER_METRIC.md`.
