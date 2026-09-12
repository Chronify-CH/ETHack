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

---

# Run 5: the fixed pipeline (BM25 query fix + sentence-window scoring)

Full corpus, ~78 minutes. Ground truth is the same hand-verified set, with one
correction noted below.

## Fourth ground-truth error, again caught by the detector

I recorded ConocoPhillips' `assurance_provider_named` as absent because "the
firm is not named". The fixed run scored it 0.898 and returned as evidence:
*"Limited assurance is performed by an external third party, **ERM CVS**, on
all environmental metrics…"* The firm **is** named. My check had read only the
first few probe hits and stopped.

That is four ground-truth errors: LTIR (under-claimed), PwC (over-claimed),
a transcription slip, and now this (under-claimed). Three of the four were
surfaced by the detector disagreeing with me, not by my own re-checking.

## Per-item: run 3 → run 5

| Item | run 3 accuracy | run 5 accuracy | Recall 3→5 | Precision 3→5 | Grade |
|---|---|---|---|---|---|
| `board_committee_climate_mandate` | 0/10 detections, ~0% recall | **≥8/10** | 0% → **100%** (4/4 known) | — → 100% | **F → B+** |
| `target_net_zero_year` | 3/10 | **6/10** | 30% → **60%** | 100% → 100% | **F → D** |
| `assurance_provider_named` | 8/10 | **8/10** | 50% → **100%** | 100% → 67% | **B− → B−** |
| `scope1_absolute` | 6/10 | **7/10** | 57% → 57% | 80% → **100%** | **D+ → C** |
| `injury_rate_trir` | 4/4 checked | 4/4 checked | high | 100% | **B** |
| `scenario_analysis_quantified` | 2 known FPs | **~6 FPs of 7 detections** | — | ~14% | **F → F−** |
| `scope3_category_breakdown` | 6/10 detections | **10/10 detections** | — | ≤90% (Chevron FP confirmed) | **unmeasured, now suspicious** |
| `scope2_market_based` | unmeasured | unmeasured | — | — | **unmeasured** |

## What genuinely improved

`board_committee_climate_mandate` went from the worst item in the project to
one of the best. It now finds real, correctly-named committees:
- Microsoft: "The Environmental, Social, and Public Policy Committee of
  Microsoft's Board of Directors provides oversight… on environmental
  sustainability strategy"
- ConocoPhillips: "the Public Policy and Sustainability Committee (PPSC) of
  the board"
- Bank of America: "The Board's Enterprise Risk Committee oversees risk…
  including periodically on climate risk"
- Occidental: correctly FOUND (0.980)

Its true negatives are also correct *for the right reason*: Goldman scored
0.475 (just below) on its "Firmwide Climate Steering Group" — a management
body, not a board committee — and Chevron 0.328 on "The Board also oversees…
climate and sustainability matters", which is the board generally rather than
a named committee. Both are the strict reading the hypothesis asks for.

## What got worse, and it is not subtle

`scenario_analysis_quantified` produced **seven detections, of which roughly
six are false positives**, and the evidence strings show exactly why:

| Company | Score | What it actually matched |
|---|---|---|
| Goldman Sachs | 0.898 | "our G-SIB surcharge increased to 3.0%" — a bank capital ratio |
| Apple | 0.979 | "a Green Fund, which Apple launched in 2019" |
| Microsoft | 0.966 | "$1 billion Climate Innovation Fund" |
| Chevron | 0.942 | "OGCI is a CEO-led initiative" |
| JPMorgan | 0.982 | "clients operating in sectors more vulnerable to transition risk" |
| ExxonMobil | 0.968 | a non-GAAP supplemental-information header |

Precision ≈ 14%. This item is not mis-tuned, it is mis-specified, and the
Fault 8 max-over-N effect turned a mediocre item into an actively misleading
one. **It must be removed from the item set until rewritten** — the hypothesis
needs to require a scenario-linked monetary impact, and the anchors must stop
matching every dollar sign in the document.

`scope3_category_breakdown` now fires on **all 10 companies**, including
Chevron, where no Scope 3 category breakdown exists at all. A column that
detects something in every single document is not measuring absence.

## Honest overall read

The fixes did what they were designed to do — the two severe faults are
genuinely repaired, and recall roughly doubled on the items where retrieval or
chunk dilution was the blocker. But the same change inflated scores everywhere
(Fault 8), so the two mis-specified items now fail loudly instead of quietly.

Net across the four items with full ground truth: **run 3 = 17/40 cells
correct, run 5 = 29/40.** Real improvement, and still nowhere near
publishable. Three items must be excluded from scored output
(`scenario_analysis_quantified`, `scope3_category_breakdown` pending
verification, `target_net_zero_year` at 60% recall), and the threshold
remains uncalibrated at a new, higher-N operating point.

---

# Run 6: two items rewritten, thresholds calibrated

## The calibration result, stated first because it is the important one

`absence/calibrate.py` fits thresholds against `absence/data/labels.json`
(60 hand-verified cells; unverified cells are `null` and excluded, never
guessed). Leave-one-out is reported rather than in-sample, because choosing a
threshold on these cells and then reporting accuracy on the same cells is
circular.

**There is no usable global threshold.** Best global cut is 0.17 by f1;
leave-one-out accuracy **0.73 against a 0.57 base rate**. Per-item fitted cut
points span **0.03 to 0.94** — a 30x spread. That is Fault 3 measured: the
items' score distributions are not on a common scale, so one cut cannot serve
them all. Thresholds are now per-item (`items.py: calibrated_threshold`) and
`detect_item` uses them.

## Which items survive validation

Leave-one-out accuracy against each item's own base rate — an item whose LOO
does not beat its base rate is carrying no information:

| Item | n | LOO acc | Base rate | Threshold | Scored? |
|---|---|---|---|---|---|
| `scope1_absolute` | 10 | **0.90** | 0.70 | 0.20 | ✅ keep |
| `board_committee_climate_mandate` | 8 | **0.88** | 0.50 | 0.93 | ✅ keep |
| `assurance_provider_named` | 10 | **0.70** | 0.60 | 0.80 | ✅ keep |
| `scope3_category_breakdown` | 9 | 0.44 | 0.67 | 0.46 | ❌ **anti-informative** |
| `target_net_zero_year` | 10 | 0.90 | **1.00** | 0.03 | ❌ no negatives |
| `injury_rate_trir` | 3 | 0.67 | **1.00** | 0.94 | ❌ no negatives, n=3 |
| `scenario_analysis_quantified` | 10 | 1.00 | **1.00** | 0.99 | ❌ no positives |
| `scope2_market_based` | 0 | — | — | 0.50 | ❌ never labelled |

**Three of eight items are eligible for scored output.** Five are excluded,
each with the reason recorded in `items.py: exclusion_reason`.

## The structural problem this exposes

Four of the excluded items fail for the same reason and it is not the
detector's fault: **their label distribution is degenerate on this corpus.**
All 10 companies state a net-zero target year; none quantify a scenario
impact; all 3 labelled injury cells are positive. With one class absent,
precision or recall is undefined and no threshold can be fitted or validated.

This is a corpus-design finding for Milestone 2, and it changes what Section
11's "200 hand-labelled pairs" has to mean: the pairs must be **sampled to
contain both classes per item**, not drawn at random from ten large-cap
reports that all do roughly the same thing. Ten S&P 500 sustainability
reports are too homogeneous to calibrate against.

## Did the two rewrites work?

**`scenario_analysis_quantified` — improved, still unvalidatable.** False
positives at the old 0.5 cut fell **7 → 4** (remaining: ExxonMobil 0.843,
ConocoPhillips 0.956, JPMorgan 0.938, Goldman 0.655). Dropping the bare `$` /
`million` / `billion` anchors removed the G-SIB-surcharge and Green-Fund
matches. But with zero positives in the corpus, recall is undefined and the
item cannot be validated here at all.

**`scope3_category_breakdown` — not fixed.** In-sample precision rose
0.60 → 0.83, which looks like progress and is not: leave-one-out accuracy is
**0.44 against a 0.67 base rate**, meaning the score is *anti-correlated* with
ground truth. The rewrite changed which cells are wrong rather than making the
ordering right. The two decisive cells:

- **ConocoPhillips discloses** "Category 1, purchased goods and services and
  Category 2, capital goods" — and scores **0.091**, because retrieval
  returned a paragraph about wildfire mitigation in Alberta.
- **Chevron discloses no breakdown at all** — and scores **0.836** on a
  glossary line reading "Methane intensity The amount of methane per unit of
  measure."

That is a retrieval failure, not a hypothesis failure, so rewriting the
hypothesis again will not help. The item stays excluded.

## Sixth ground-truth error

Goldman's `scope3_category_breakdown` was labelled `false` on the strength of a
regex whose character class contained an en-dash but not an em-dash — which
hid the document's actual "Scope 3: Category 6 — Business Travel (tCO2e)
57,233". Re-reading, Goldman breaks out exactly one category with figures,
which is a genuinely borderline partial breakdown, so it is now labelled
`null` and excluded rather than forced either way.

Six ground-truth errors so far, every one from pattern-matching instead of
reading. The labels file now records the reasoning per item so the next reader
can check the judgement rather than inherit it.
