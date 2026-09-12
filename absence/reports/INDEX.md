# Analysed reports

One folder per document the pipeline read. Each holds `source.txt` — the exact extracted text that was scored, hash-verified in `absence/data/provenance.json` — and `analysis.md`, its per-item audit trail. Regenerate the analyses with `python -m absence.export_reports`.

| folder | company | sector | year | chars | scored items agreeing with the hand read |
|---|---|---|---:|---:|---|
| [`apple_technology_2023/`](apple_technology_2023/analysis.md) | Apple Inc. | Technology | 2023 | 405,050 | 4/4 |
| [`msft_technology_2022/`](msft_technology_2022/analysis.md) | Microsoft Corporation | Technology | 2022 | 232,714 | 4/4 |
| [`googl_technology_2024/`](googl_technology_2024/analysis.md) | Alphabet Inc. (Google) | Technology | 2024 | 355,405 | 2/3 |
| [`xom_energy_2023/`](xom_energy_2023/analysis.md) | ExxonMobil | Energy | 2023 | 37,080 | 4/4 |
| [`cvx_energy_2023/`](cvx_energy_2023/analysis.md) | Chevron Corporation | Energy | 2023 | 165,535 | 2/4 |
| [`cop_energy_2022/`](cop_energy_2022/analysis.md) | ConocoPhillips | Energy | 2022 | 536,681 | 4/4 |
| [`oxy_energy_2023/`](oxy_energy_2023/analysis.md) | Occidental Petroleum | Energy | 2023 | 272,303 | 4/4 |
| [`jpm_financials_2024/`](jpm_financials_2024/analysis.md) | JPMorgan Chase & Co. | Financials | 2024 | 261,455 | 3/3 |
| [`bac_financials_2025/`](bac_financials_2025/analysis.md) | Bank of America | Financials | 2025 | 230,222 | 4/4 |
| [`gs_financials_2022/`](gs_financials_2022/analysis.md) | Goldman Sachs Group Inc. | Financials | 2022 | 249,024 | 3/3 |

Only the 4 validated items count toward those fractions: `scope1_absolute`, `scope3_category_breakdown`, `assurance_provider_named`, `board_committee_climate_mandate`. The other 4 items appear in every analysis file, marked excluded with the reason, because their evidence is still worth auditing even though their accuracy is unknown or measurably poor.
