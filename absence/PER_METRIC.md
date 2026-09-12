# Per-metric (per-item) grades

Grades are for **the detector's performance on each item**, measured against
hand-verified ground truth from the source documents. Verdicts below are the
run 3 pipeline (BM25 + base model, whole-chunk scoring) — the configuration
whose full results are recorded. The Fault 1+2 fixes are being re-run; where a
fixed-pipeline number is already known it is noted.

Section 11's rule is applied throughout: **an item with recall below 0.7 is
unreliable and must be excluded from scored output**, not left in to add noise.

---

## Summary

| Item | Precision | Recall | Accuracy | Grade | Scored-output status |
|---|---|---|---|---|---|
| `assurance_provider_named` | 2/2 (100%) | 2/3 (67%) | 9/10 | **B−** | ❌ excluded (recall < 0.7, narrowly) |
| `scope1_absolute` | 4/5 (80%) | 4/7 (57%) | 6/10 | **D+** | ❌ excluded |
| `target_net_zero_year` | 3/3 (100%) | 3/10 (30%) | 3/10 | **F** | ❌ excluded |
| `board_committee_climate_mandate` | — (0 positives) | 0/≥2 (0%) | ≤8/10 | **F** | ❌ excluded |
| `scenario_analysis_quantified` | low — 2 confident FPs seen | unmeasured | — | **F** | ❌ excluded |
| `injury_rate_trir` | 3/3 (100%) | 3/3+ (est. high) | 4/4 checked | **B** (provisional) | ⚠️ provisional |
| `scope2_market_based` | unmeasured | unmeasured | — | **unmeasured** | ⚠️ unknown |
| `scope3_category_breakdown` | unmeasured, 1 FP seen (run 4) | unmeasured | — | **unmeasured** | ⚠️ unknown |

**Not one of the eight items currently qualifies for scored output.** Three are
measured and fail; two are measured-enough to fail; three are unmeasured.

---

## Fully measured items

### `assurance_provider_named` — B−
Precision 100%, recall 67%, accuracy 9/10. All ten companies verified (table in
`PER_COMPANY.md`). The single miss is Microsoft's "Deloitte & Touche LLP
performed a review…" (0.007). **The Fault 2 fix recovers it: 0.007 → 0.805**,
which would make this item 3/3 recall and the first item to clear the 0.7 bar.

Two near-misses were *correct* and worth noting as evidence the item's strict
hypothesis works: Chevron and ConocoPhillips both describe obtaining assurance
but never name the firm, and both correctly scored absent.

### `scope1_absolute` — D+
Precision 80%, recall 57%, accuracy 6/10.

| Company | Ground truth | Detector | |
|---|---|---|---|
| Apple | present | FOUND 0.736 | ✅ |
| Microsoft | **absent** — only percentages ("declined by 0.5 percent", "22.7 percent"); absolute tonnes live in a separate Environmental Data Fact Sheet | FOUND 0.500 | ❌ **false positive** |
| Alphabet | present | FOUND 0.525 | ✅ |
| ExxonMobil | absent (executive summary, no emissions table) | absent 0.033 | ✅ |
| Chevron | absent — reports **intensity** (kg CO₂e/boe), not absolute | absent 0.067 | ✅ |
| ConocoPhillips | present | FOUND 0.503 | ✅ |
| Occidental | present | absent **0.490** | ❌ false negative |
| JPMorgan | present — "Scope 1 GHG emissions 100,024" tCO₂e | absent 0.174 | ❌ false negative |
| Bank of America | present | absent 0.107 | ❌ false negative |
| Goldman Sachs | present | FOUND 0.627 | ✅ |

**This item is the cleanest demonstration of Fault 3.** Look at the cluster
around the cut point: Occidental 0.490 (absent), Microsoft 0.500 (found),
ConocoPhillips 0.503 (found), Alphabet 0.525 (found). Four companies within
0.035 of each other land on both sides of a threshold nobody calibrated, and
the two nearest the line are a false negative and a false positive
respectively. The ordering here carries no information.

### `target_net_zero_year` — F
Precision 100%, recall **30%**, accuracy 3/10. Every company in the corpus
states a net-zero or carbon-neutral target year; the detector found three.

Verified misses: Apple ("carbon neutral by 2030"), ExxonMobil ("Scope 1 and 2
net zero … by 2050"), Chevron ("aspires to reach net zero upstream emissions …
by 2050"), Occidental ("Net-zero … before 2040"), JPMorgan, Bank of America
("our goal to achieve net zero greenhouse gas (GHG)"), Goldman Sachs ("align
our business with a net zero by 2050 pathway").

**This corrects a claim I made earlier.** I suggested a "sector pattern" —
Financials scoring near-zero because banks express targets as financed-emissions
pathways rather than a firmwide year. That was wrong: all three banks state
plain net-zero-by-2050 commitments in their own words. The pattern was a
detector artifact, which is exactly the trap Section 14 names and which I had
already written a warning about before half-repeating it anyway.

**The Fault 2 fix recovers Apple: 0.069 → 0.943.** If it generalises across the
other six misses this item moves from F to passing; the running re-run will say.

---

## Measured enough to fail

### `board_committee_climate_mandate` — F
Zero detections across all 10 companies (0.001–0.315), while at least two
companies disclose it plainly: Occidental ("BOARD COMMITTEES — The S&SE
Committee oversees … climate-related risks and opportunities", retrieved at
rank 1, scored 0.007) and Chevron ("Our highly experienced Board of Directors
oversees sustainability-related matters"). Recall 0%.

**The Fault 2 fix recovers Occidental: 0.065 → 0.980**, the single largest
improvement measured in this project.

### `scenario_analysis_quantified` — F
Not systematically measured, but it produced **two confident false positives**
on unrelated financial passages: Goldman Sachs at 0.772 (a green-bond issuance)
and Chevron at 0.857 in run 4 (carbon-intensity capex, "$2.0 billion in carbon
reduction projects"). Its anchors include `$`, `million`, `billion`, which match
any financial passage in documents full of them.

This is a **specification fault, not a tuning fault** — the hypothesis asks for
a dollar impact *derived from scenario analysis*, the anchors retrieve *any*
dollar figure. No threshold fixes that. Rewrite the item.

---

## Unmeasured

### `injury_rate_trir` — B (provisional)
4 of 4 checked cells correct: ConocoPhillips (real TRIR table, 0.977),
Occidental (0.881), ExxonMobil (0.736 — the LTIR case that caught my own
ground-truth error), Chevron absent 0.106 (unverified). Only applies to the 4
Energy companies, so the sample is inherently small. Provisional B.

### `scope2_market_based`, `scope3_category_breakdown` — unmeasured
No systematic ground truth established. `scope3_category_breakdown` has the
highest raw detection rate in the corpus (6/10), which given every other
measured item's low recall is more suspicious than reassuring — and run 4
produced a confident false positive on Chevron, where no Scope 3 breakdown
exists at all. Do not read either column.

---

## What this changes about the headline numbers

The 85% by-eye figure came from 13 cells chosen because they were diagnostically
interesting. Measuring whole items end-to-end gives a very different picture:
**accuracy per item runs 30%–90%**, and the two items with the most complete
ground truth (`target_net_zero_year` at 30%, `scope1_absolute` at 60%) are far
below it.

The consistent direction is **false negatives, not false positives**: across
every item measured, the detector misses real disclosures far more often than it
invents them. For a project whose output is a *silence* ledger, that bias is the
worst possible one — it manufactures silence that isn't there.
