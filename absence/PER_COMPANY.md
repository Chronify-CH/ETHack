# Per-company assessment

## Read this first: what is and isn't being graded

**These are not disclosure-quality grades for the companies.** The detector
has measured faults (`FAULTS.md`) that make an `absent` cell mean "not
detected", which conflates three different things: the company didn't
disclose it, retrieval never found it, or it was found and scored on a chunk
that destroyed the signal. Publishing a company ranking off that would be the
precise failure `ABSENCE_BRIEF.md` Section 14 warns about — "treating a low
item-detection rate as a finding about companies when it is a finding about
the detector."

What follows is graded instead on **how much the row can be trusted**, plus
every cell verified by hand against the source text.

Detector verdicts below are run 3 (BM25 + base model), the canonical config.

---

## First real per-item recall measurement: `assurance_provider_named`

All 10 companies hand-verified for this one item, using the strict reading of
its hypothesis ("**named** the specific third-party firm"):

| Company | Firm named in document? | Detector | Verdict |
|---|---|---|---|
| Apple | Yes — Apex Companies | FOUND 0.808 | ✅ |
| Microsoft | **Yes — "Deloitte & Touche LLP performed a review…"** | absent 0.007 | ❌ **false negative** |
| Alphabet | No (probe's "ERM" hits are *Enterprise Risk Management*, a false friend) | absent 0.363 | ✅ |
| ExxonMobil | No | absent 0.008 | ✅ |
| Chevron | Assurance obtained, firm **not named** in this document | absent 0.143 | ✅ |
| ConocoPhillips | Assurance described, firm **not named** | absent 0.026 | ✅ |
| Occidental | Yes — ERM CVS | FOUND 0.968 | ✅ |
| JPMorgan | No (its "verified by" refers to carbon credits) | absent 0.030 | ✅ |
| Bank of America | No (its "verified by" refers to *client* data) | absent 0.010 | ✅ |
| Goldman Sachs | **No** — PwC's letter assures *green-bond proceeds allocation* ("provides no assurance on allocations in excess of net proceeds"), not emissions data | absent 0.017 | ✅ (corrected — I first scored this a false negative) |

**Precision 2/2 = 100%. Recall 2/3 = 67%. Accuracy 9/10.**

> **Correction, and the third ground-truth error in this project.** Goldman
> Sachs was first recorded here as a false negative because its report names
> PricewaterhouseCoopers. Reading what PwC actually attested to, it is the
> Sustainability *Issuance* Report — assurance over green-bond proceeds
> allocation, which the document itself says "provides no assurance on
> allocations in excess of net proceeds". The item's hypothesis asks for
> assurance "over its reported **emissions data**". So Goldman does not
> disclose one, the detector's `absent` was right, and I was wrong.
>
> Note the direction: the LTIR error under-claimed a disclosure, this one
> over-claimed one. Both came from matching a *keyword* (LTIR-adjacent terms;
> "PricewaterhouseCoopers") instead of reading what the hypothesis actually
> requires. `groundtruth_probe.py` surfaces candidates; it cannot do this
> judgement step, and nothing except reading the surrounding text can.

Recall of 0.67 is still below Section 11's 0.7 cutoff, so
**`assurance_provider_named` remains unreliable for scored output** on the
run-3 pipeline. (The Fault 1+2 fixes recover Microsoft's Deloitte disclosure
-- 0.007 to 0.805 -- which would take this item to 3/3 recall; the full
fixed-pipeline run will confirm or refute that.) Note the asymmetry: the detector never invents a disclosure, it misses
real ones — so its `absent` cells are unreliable while its `FOUND` cells have
held up under every check so far.

---

## Per-company grades (trustworthiness of the row, not the company)

| Company | Cells verified | Grade | Why |
|---|---|---|---|
| **Apple** | **7 / 7** | **A−** | The only fully hand-audited row. 6/7 correct; one false negative (`target_net_zero_year` 0.069 on a chunk that literally reads "carbon neutral by 2030"). Confirmed true absences for board committee and quantified scenario analysis. This row can be discussed with confidence. |
| **Occidental** | 2 / 8 | **C** | One clean true positive (ERM CVS, 0.968) and one severe, fully-diagnosed false negative: its report says "BOARD COMMITTEES — The S&SE Committee oversees… climate-related risks", retrieved at rank 1, scored 0.007. Six cells unverified. |
| **ExxonMobil** | ~3 / 8 | **C** | Structurally different input: a 19-page *Executive Summary*, not a full report, so several absences are genuine document-scope effects rather than non-disclosure. `injury_rate_trir` correct (0.736, the LTIR case). `target_net_zero_year` a false negative. |
| **Chevron** | ~4 / 8 | **C** | Lowest detection count (1/8), but verification shows much of it is *correct*: Chevron reports Scope 1+2 as **intensity** (kg CO₂e/boe), not absolute tonnes, so `scope1_absolute` absent is arguably right — exactly the distinction the item exists to catch. `scope3_category_breakdown` confirmed genuinely absent. |
| **ConocoPhillips** | 2 / 8 | **C−** | `injury_rate_trir` correct with the real TRIR table (0.977). Assurance correctly absent under the strict reading. Six cells unverified. |
| **Goldman Sachs** | 2 / 7 | **C−** | One confirmed false negative (PwC assurance). `scenario_analysis_quantified` correctly absent in run 3 — though run 4 produced a confident false positive on the same cell, so this item is volatile here. |
| **Microsoft** | 1 / 7 | **D+** | One cell checked, and it was a false negative (Deloitte & Touche). Nothing else verified. |
| **Alphabet** | 1 / 7 | **D+** | One cell checked and correct. Highest raw detection scores in the corpus (scope2 0.974, target 0.994), none of which are verified. |
| **JPMorgan** | 1 / 7 | **D+** | One cell checked and correct. Rest unverified. |
| **Bank of America** | 1 / 7 | **D+** | One cell checked and correct. Rest unverified. |

**The grade tracks my verification coverage, not the company.** A D+ means
"almost nothing here has been checked", not "this company discloses poorly".

---

## Sector pattern worth investigating (not yet a finding)

All three Financials score near-zero on `target_net_zero_year` (0.023–0.102)
while all three Tech firms score high (0.654–0.994). A plausible explanation
is structural: banks express targets as sector-by-sector financed-emissions
intensity pathways rather than one firmwide net-zero year, which the item's
hypothesis doesn't accommodate. **This is a hypothesis, not a result** — it
needs the same hand-verification the assurance item just received before it
can be repeated as anything else.

---

## What would make these grades real

For any company to get a defensible *disclosure* grade, in order:
1. Fix Faults 1–3 (retrieval recall, sentence-level scoring, calibration).
2. Hand-verify all 8 items for that company, as was done for Apple.
3. Report per-item recall as done above for `assurance_provider_named`, and
   drop every item below 0.7 recall from the scored set.

Until then the only company row I would discuss out loud is Apple's, and even
that one contains a known false negative.
