# Analysed reports

One folder per document the pipeline read. Each holds `source.txt` — the exact extracted text that was scored, hash-verified in `absence/data/provenance.json` — and `analysis.md`, its per-item audit trail. Regenerate the analyses with `python -m absence.export_reports`.

| folder | company | sector | chars | scored items agreeing with the hand read |
|---|---|---|---:|---|
| [`apple_technology/`](apple_technology/analysis.md) | Apple Inc. | Technology | 405,050 | 4/4 |
| [`msft_technology/`](msft_technology/analysis.md) | Microsoft Corporation | Technology | 232,714 | 4/4 |
| [`googl_technology/`](googl_technology/analysis.md) | Alphabet Inc. (Google) | Technology | 355,405 | 2/3 |
| [`xom_energy/`](xom_energy/analysis.md) | ExxonMobil | Energy | 37,080 | 4/4 |
| [`cvx_energy/`](cvx_energy/analysis.md) | Chevron Corporation | Energy | 165,535 | 2/4 |
| [`cop_energy/`](cop_energy/analysis.md) | ConocoPhillips | Energy | 536,681 | 4/4 |
| [`oxy_energy/`](oxy_energy/analysis.md) | Occidental Petroleum | Energy | 272,303 | 4/4 |
| [`jpm_financials/`](jpm_financials/analysis.md) | JPMorgan Chase & Co. | Financials | 261,455 | 3/3 |
| [`bac_financials/`](bac_financials/analysis.md) | Bank of America | Financials | 230,222 | 4/4 |
| [`gs_financials/`](gs_financials/analysis.md) | Goldman Sachs Group Inc. | Financials | 249,024 | 3/3 |

Only the 4 validated items count toward those fractions: `scope1_absolute`, `scope3_category_breakdown`, `assurance_provider_named`, `board_committee_climate_mandate`. The other 4 items appear in every analysis file, marked excluded with the reason, because their evidence is still worth auditing even though their accuracy is unknown or measurably poor.
