# Analysed reports

60 report documents, one folder each. Every folder holds `source.txt` — the exact extracted text, hash-verified in `absence/data/provenance.json`. Folders for documents that have been through the detector also hold `analysis.md`, their per-item audit trail.

**10 of 60 documents have been scored.** The rest are fetched and cached but not yet run through the pipeline; they are listed below as *not yet scored*, which means exactly that and nothing about the companies concerned.

Regenerate this file and the analyses with `python -m absence.export_reports`.

## Energy

### Equipment & Services

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| `bkr_energy_2024/` | Baker Hughes | 2024 | 530,418 | not yet scored |
| `bkr_energy_2023/` | Baker Hughes | 2023 | 461,117 | not yet scored |
| `bkr_energy_2022/` | Baker Hughes | 2022 | 361,680 | not yet scored |
| `hal_energy_2023/` | Halliburton | 2023 | 176,698 | not yet scored |
| `hal_energy_2022/` | Halliburton | 2022 | 234,123 | not yet scored |
| `hal_energy_2021/` | Halliburton | 2021 | 218,570 | not yet scored |
| `slb_energy_2022/` | Schlumberger | 2022 | 183,216 | not yet scored |
| `slb_energy_2021/` | Schlumberger | 2021 | 175,022 | not yet scored |
| `slb_energy_2020/` | Schlumberger | 2020 | 322,761 | not yet scored |

### Exploration & Production

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| [`cop_energy_2022/`](cop_energy_2022/analysis.md) | ConocoPhillips | 2022 | 536,681 | scored, 4/4 agree with the hand read |
| `cop_energy_2021/` | ConocoPhillips | 2021 | 513,008 | not yet scored |
| `cop_energy_2020/` | ConocoPhillips | 2020 | 445,688 | not yet scored |
| `ctra_energy_2023/` | Coterra Energy | 2023 | 119,482 | not yet scored |
| `ctra_energy_2022/` | Coterra Energy | 2022 | 109,136 | not yet scored |
| `dvn_energy_2023/` | Devon Energy | 2023 | 328,779 | not yet scored |
| `dvn_energy_2022/` | Devon Energy | 2022 | 307,863 | not yet scored |
| `dvn_energy_2021/` | Devon Energy | 2021 | 298,854 | not yet scored |
| `eog_energy_2021/` | EOG Resources | 2021 | 235,619 | not yet scored |
| `eog_energy_2020/` | EOG Resources | 2020 | 200,999 | not yet scored |
| `eqt_energy_2022/` | EQT Corporation | 2022 | 347,943 | not yet scored |
| `eqt_energy_2021/` | EQT Corporation | 2021 | 345,061 | not yet scored |
| `eqt_energy_2020/` | EQT Corporation | 2020 | 324,435 | not yet scored |
| `exe_energy_2024/` | Expand Energy | 2024 | 273,983 | not yet scored |
| `exe_energy_2023/` | Expand Energy | 2023 | 257,226 | not yet scored |
| `exe_energy_2022/` | Expand Energy | 2022 | 212,718 | not yet scored |
| `fang_energy_2023/` | Diamondback Energy | 2023 | 159,122 | not yet scored |
| `fang_energy_2022/` | Diamondback Energy | 2022 | 136,168 | not yet scored |
| `fang_energy_2021/` | Diamondback Energy | 2021 | 134,733 | not yet scored |
| [`oxy_energy_2023/`](oxy_energy_2023/analysis.md) | Occidental Petroleum | 2023 | 272,303 | scored, 4/4 agree with the hand read |
| `oxy_energy_2021/` | Occidental Petroleum | 2021 | 196,960 | not yet scored |

### Integrated

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| [`cvx_energy_2023/`](cvx_energy_2023/analysis.md) | Chevron Corporation | 2023 | 165,535 | scored, 2/4 agree with the hand read |
| `cvx_energy_2022/` | Chevron Corporation | 2022 | 224,470 | not yet scored |
| `cvx_energy_2021/` | Chevron Corporation | 2021 | 248,669 | not yet scored |
| [`xom_energy_2023/`](xom_energy_2023/analysis.md) | ExxonMobil ⚠︎ | 2023 | 37,080 | scored, 4/4 agree with the hand read |
| `xom_energy_2021/` | ExxonMobil | 2021 | 104,478 | not yet scored |

### Midstream

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| `kmi_energy_2022/` | Kinder Morgan | 2022 | 441,005 | not yet scored |
| `kmi_energy_2021/` | Kinder Morgan | 2021 | 367,650 | not yet scored |
| `kmi_energy_2020/` | Kinder Morgan | 2020 | 386,295 | not yet scored |
| `oke_energy_2022/` | ONEOK | 2022 | 217,783 | not yet scored |
| `oke_energy_2021/` | ONEOK | 2021 | 175,635 | not yet scored |
| `oke_energy_2020/` | ONEOK | 2020 | 178,620 | not yet scored |
| `trgp_energy_2024/` | Targa Resources | 2024 | 207,674 | not yet scored |
| `trgp_energy_2022/` | Targa Resources | 2022 | 250,153 | not yet scored |
| `wmb_energy_2022/` | Williams Companies | 2022 | 455,021 | not yet scored |
| `wmb_energy_2020/` | Williams Companies | 2020 | 321,028 | not yet scored |

### Refining & Marketing

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| `mpc_energy_2022/` | Marathon Petroleum | 2022 | 257,379 | not yet scored |
| `mpc_energy_2021/` | Marathon Petroleum | 2021 | 238,434 | not yet scored |
| `mpc_energy_2020/` | Marathon Petroleum | 2020 | 211,392 | not yet scored |
| `psx_energy_2023/` | Phillips 66 | 2023 | 202,866 | not yet scored |
| `psx_energy_2022/` | Phillips 66 | 2022 | 175,656 | not yet scored |
| `psx_energy_2021/` | Phillips 66 | 2021 | 164,572 | not yet scored |
| `vlo_energy_2023/` | Valero Energy | 2023 | 220,369 | not yet scored |
| `vlo_energy_2022/` | Valero Energy | 2022 | 199,539 | not yet scored |
| `vlo_energy_2020/` | Valero Energy | 2020 | 178,285 | not yet scored |

## Technology

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| [`apple_technology_2023/`](apple_technology_2023/analysis.md) | Apple Inc. | 2023 | 405,050 | scored, 4/4 agree with the hand read |
| [`googl_technology_2024/`](googl_technology_2024/analysis.md) | Alphabet Inc. (Google) | 2024 | 355,405 | scored, 2/3 agree with the hand read |
| [`msft_technology_2022/`](msft_technology_2022/analysis.md) | Microsoft Corporation | 2022 | 232,714 | scored, 4/4 agree with the hand read |

## Financials

| folder | company | year | chars | status |
|---|---|---:|---:|---|
| [`bac_financials_2025/`](bac_financials_2025/analysis.md) | Bank of America | 2025 | 230,222 | scored, 4/4 agree with the hand read |
| [`gs_financials_2022/`](gs_financials_2022/analysis.md) | Goldman Sachs Group Inc. | 2022 | 249,024 | scored, 3/3 agree with the hand read |
| [`jpm_financials_2024/`](jpm_financials_2024/analysis.md) | JPMorgan Chase & Co. | 2024 | 261,455 | scored, 3/3 agree with the hand read |

## Documents that could not be retrieved

Recorded rather than omitted, so the corpus can never look more complete than it is. None of these is evidence about the company: each is a fact about the source.

| intended document | company | year | why not retrieved |
|---|---|---:|---|
| `eog_energy_2022` | EOG Resources | 2022 | The fetcher consistently returns null content for this URL, matching the 'Report Locked -- EOG Resources has reached its limit for free report views' notice the archive shows for this company's most recent edition. Not a transport failure: the host is withholding the document. |
| `trgp_energy_2023` | Targa Resources | 2023 | Rejected as content_too_large. Targa's own site lists this edition at 100.5 MB, several times the size of any other document here, and it is not on ResponsibilityReports.com. Deterministic, so not retried further. |
| `wmb_energy_2021` | Williams Companies | 2021 | Unreachable on eleven separate attempts, while NYSE_WMB_2022.pdf and NYSE_WMB_2020.pdf from the same directory fetched normally. Broken on the host rather than rate-limited. |
| `xom_energy_2022` | ExxonMobil | 2022 | Unreachable on eleven separate attempts spread over hours, while NYSE_XOM_2023.pdf and NYSE_XOM_2021.pdf from the same archive directory fetched normally. The file appears to be broken on the host rather than rate-limited. ExxonMobil's own site serves only a five-page executive summary for 2022 (~5,000 characters), which is not a substitute for a full report and was rejected by the length floor. |

## ⚠︎ Document-type caveats

- **xom_energy_2023** — This is ExxonMobil's Sustainability Report EXECUTIVE SUMMARY, not the full report: 37,080 characters against a corpus median in the low hundreds of thousands. Items scored absent here are substantially a fact about the document's length and purpose, not about the company's disclosure. Do not compare this document's silence against full reports.

## Reading the year column

Every year here was confirmed against the document's own title page, not taken from its filename. The three editions held for one company are its three most recent available, which are not the same three years across companies: some archives reach 2024 or 2025 and others stop at 2022. A difference between two companies in this corpus can therefore be a difference in reporting year rather than in disclosure. Compare within a year where the corpus allows it.

Only the 4 validated items count toward the agreement figures above: `scope1_absolute`, `scope3_category_breakdown`, `assurance_provider_named`, `board_committee_climate_mandate`. The other 4 appear in each analysis file marked excluded, with the reason, because their evidence is still worth auditing even though their accuracy is unknown or measurably poor.
