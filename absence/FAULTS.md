# Known faults, with evidence

Every claim here is backed by a reproducible command against the committed
corpus. This is deliberately written as a list of things that are *wrong*,
because the silence table looks far more authoritative than it is.

---

## Fault 1 (severe): BM25 retrieval has poor recall on gold evidence

**Claim:** the retrieval step frequently fails to surface the chunks that
actually contain the disclosure, and when it does surface one, it is often
not the best one.

**Evidence — Apple, `assurance_provider_named`:**

Nine chunks in Apple's report name "Apex Companies" (its assurance provider).
Scored individually against the item hypothesis, they range enormously:

| chunk | 471 | 476 | 482 | 485 | **505** | 510 | 517 | 553 | 554 |
|---|---|---|---|---|---|---|---|---|---|
| score | 0.968 | 0.008 | 0.036 | 0.018 | **0.995** | 0.001 | 0.698 | 0.007 | **0.007** |

BM25's top-8 was `[554, 457, 474, 521, 508, 487, 570, 514]` — of the nine gold
chunks it retrieved exactly **one (chunk 554), the joint-worst-scoring one
(0.007)**. The 0.995 chunk was never considered. The pipeline's reported 0.808
came from a non-gold chunk that happened to score well.

**Root cause:** `retrieve_candidates` builds its BM25 query from the item's
full hypothesis sentence plus its anchors. The hypothesis contributes
high-frequency terms ("the", "company", "reported", "emissions", "data")
that match nearly every chunk in an emissions report, swamping the
discriminative terms ("assurance", "verification"). Combined with `k=8` out
of 594 chunks (1.3% of the document), recall is poor by construction.

**Reproduce:**
```
python3 -c "
from absence.detect.entail import retrieve_candidates, score_paragraphs_batch
from absence.detect.items import ITEMS_BY_ID
from absence.corpus.extract import segment_paragraphs, rechunk
item=ITEMS_BY_ID['assurance_provider_named']
paras=rechunk(segment_paragraphs(open('absence/data/raw/apple_technology.txt').read()))
gold=[p for p in paras if 'Apex Companies' in p.text]
print(list(zip([p.idx for p in gold], score_paragraphs_batch(item,[p.text for p in gold]))))
print([p.idx for p in retrieve_candidates(item,paras,k=8)])"
```

**Fix direction:** strip stopwords and down-weight hypothesis terms relative
to anchors; raise `k` substantially (recall at k, not runtime, should set it);
measure recall@k against known-gold chunks before tuning anything else.

---

## Fault 2 (severe): ~900-character chunks dilute the entailment signal

**Claim:** the NLI model comprehends these claims correctly, but scoring a
whole multi-topic chunk instead of the sentence carrying the fact destroys
the signal.

**Evidence — Occidental, `board_committee_climate_mandate`:**

The report states outright: *"BOARD COMMITTEES The S&SE Committee oversees
external reporting on ESG and sustainability matters, including
climate-related risks and opportunities."* BM25 retrieved this chunk at
**rank 1**. The same fact, three ways:

| Score | Premise form |
|---|---|
| **0.007** | The raw ~900-char chunk, exactly as the pipeline scores it |
| **0.939** | "The S&SE Committee of the Board oversees climate-related risks and opportunities." |
| **0.982** | A clean paraphrase naming the committee and its remit |

A **134x** difference for an identical claim. The failure is not
comprehension — it is that a chunk of concatenated headings, bullet glyphs
("»"), and several unrelated statements is far outside the distribution of
short, fluent premises MNLI-style models are trained on.

This is the direct downstream consequence of the extraction deviation
documented in `corpus/extract.py`: without real PyMuPDF block geometry,
tables and headings are merged into prose, and `rechunk()` only bounds the
damage rather than repairing it.

**Consequence:** `board_committee_climate_mandate` scored `absent` for
**all 10 companies** (0.001–0.315). At least two companies (Occidental,
Chevron) disclose it plainly. That column is ~0% recall — it is not a
finding about companies, it is a broken detector.

**Fix direction:** score at sentence or sentence-window granularity and take
the max, keeping the chunk only for retrieval. Cheap to test: on the four
known failures, best-sentence beat whole-chunk in 3 of 4.

---

## Fault 3 (severe): scores are not comparable, so the 0.5 threshold is arbitrary

Fault 1's table is also evidence for this: nine chunks, all containing the
same disclosed fact, score anywhere from 0.001 to 0.995. The score is
dominated by chunk composition, not by whether the company disclosed the
thing. Until Section 11's calibration exists, a `FOUND`/`absent` label
mostly reflects how the text happened to be chunked.

Concretely: Occidental *does* disclose a board climate mandate and scores
0.065; Goldman Sachs scores 0.022 for the same item. Those two numbers do
not mean Goldman disclosed less — they are not on a common scale.

---

## Fault 4 (moderate): at least two of the eight items are mis-specified

- **`scenario_analysis_quantified`** — anchors include `$`, `million`,
  `billion`, which match any financial passage. It produced confident false
  positives on a Goldman Sachs green-bond issuance (0.772, run 3) and a
  Chevron carbon-intensity/capex passage. The hypothesis asks for a *dollar
  impact from scenario analysis*; the anchors retrieve *any dollar figure*.
- **`board_committee_climate_mandate`** — see Fault 2; 0/10 with known
  disclosures present.

Per Section 11 ("items with recall below 0.7 should be dropped... and
reported as unreliable rather than left in to add noise"), **both should be
excluded from any scored output until fixed.** The other six items have not
been validated as specifications at all — only spot-checked.

---

## Fault 5 (moderate): the accuracy figure rests on 13 hand-audited cells

85% (11/13) is the headline. On a 13-cell sample the 95% confidence interval
runs roughly **55%–98%** — consistent with the detector being good, and also
consistent with it being mediocre. No claim finer than "clearly better than
the keyword stub" is supportable from this sample.

Worse, the audit itself contained **two errors I made**, both caught only by
re-deriving from raw logs:
1. A ground-truth miss (searched `trir`, missed "0.02 LTIR ... lost-time
   incident rate") — corrected run 1 from 65% to 59%.
2. A transcription error putting run 2's ExxonMobil score in run 3's column —
   corrected run 3 from 77% to 85%.

`groundtruth_probe.py` exists to make the first class of error harder. The
second class has no guard other than re-deriving every number from logs.

---

## Fault 6 (structural): extraction is the weakest layer and everything sits on it

No raw PDF bytes were obtainable in this environment, so there is:
- no SHA-256 over source bytes (the provenance hash is over extracted text),
- no true page count,
- no PyMuPDF block geometry, therefore no table/prose separation, therefore
  the oversized merged chunks that cause Fault 2.

The brief's own warning — *"extraction quality dominates every downstream
number"* — is confirmed by Fault 2's 134x measurement. Any future work that
improves models or thresholds while leaving extraction as-is is optimising
the wrong layer.

---

## Fault 7 (scope): most of the brief does not exist

Milestone 1 only. Absent entirely: peer/index baselines, Conditional Silence
Score, attention misallocation (KL vs MATERIALITY), disclosure retreat,
evidence gap and the EPA/OSHA entity crosswalk, the validation suite
(Section 11's four falsification tests), the talk-vs-walk chart, SQLite
state, and parquet export. `classify.py` (cheap-talk) exists but has never
been run over the corpus or wired into the runner.

---

## What this list implies about the headline numbers

The silence table currently conflates three different things under one
`absent` label:
1. the company genuinely did not disclose it,
2. retrieval never found the disclosure (Fault 1),
3. the disclosure was found but scored on a chunk that destroyed the signal
   (Fault 2).

Nothing in the output distinguishes these. Until Faults 1–3 are fixed, an
`absent` cell should be read as **"not detected"**, never as *"not
disclosed"* — which is precisely the distinction the whole project exists to
measure, and therefore the most important thing to fix before Milestone 4's
Conditional Silence Score is computed on top of it.

---

## Fault 8 (introduced by the Fault 2 fix): max-over-N inflates scores

The Fault 2 fix scores overlapping sentence windows and takes the **max**.
That raised the number of premises per item from ~8 chunks to ~30 windows —
so there are now roughly four times as many chances for one spuriously
high-scoring premise to win. Max over more samples is upward-biased; this is
an ordinary multiple-comparisons effect, and it applies to true and false
cells alike.

Measured on the first three companies of the fixed run, against ground truth
established in `PER_METRIC.md`:

**Recovered (the fix working as intended):**

| Cell | run 3 | fixed | Ground truth |
|---|---|---|---|
| Apple `target_net_zero_year` | 0.069 absent | **0.943 FOUND** | present ✅ |
| Microsoft `assurance_provider_named` | 0.007 absent | **0.805 FOUND** | present ✅ |
| Microsoft `scope1_absolute` | 0.500 FOUND | **0.078 absent** | absent ✅ (false positive removed) |
| Occidental `board_committee` (validation) | 0.065 absent | **0.980 FOUND** | present ✅ |

**Introduced (the cost):**

| Cell | run 3 | fixed | Ground truth |
|---|---|---|---|
| Apple `scenario_analysis_quantified` | 0.031 absent | **0.979 FOUND** | **absent** ❌ new false positive |
| Alphabet `assurance_provider_named` | 0.363 absent | **0.860 FOUND** | **absent** ❌ new false positive |

So the fix trades false negatives for false positives. For a silence ledger
that trade is *directionally* right — inventing silence is worse than missing
it — but it is not free, and it lands hardest on the two items already known
to be mis-specified (`scenario_analysis_quantified`'s `$`/`million`/`billion`
anchors; `assurance_provider_named`'s reliance on a firm name appearing near
assurance language).

**The correct response is not to revert.** It is that the 0.5 threshold, which
was already uncalibrated, is now definitively wrong: it was never fitted, and
the quantity it thresholds (max over N premises) changed its distribution when
N changed. Any threshold must be calibrated *for a fixed N*, and N must be
reported alongside it. This makes Section 11's calibration a blocker rather
than a nice-to-have.

---

## Fault 9 (diagnosed and fixed): flattened tables make "names it" look like "reports it"

**The wrong diagnosis I nearly acted on.** `scope3_category_breakdown` was
anti-informative (leave-one-out 0.44 against a 0.67 base rate), and the visible
symptom pointed at retrieval: ConocoPhillips discloses category text yet scored
0.091 on a paragraph about Alberta wildfires. I was about to rewrite retrieval.

**Retrieval was fine.** All three ConocoPhillips gold chunks were already in
the top 8. The wildfire sentence won only because every gold sentence scored
*lower* — and the model was right to score them low. ConocoPhillips' category
text is a footnote, "Intended to address Scope 3, Categories 1 and 2", which
describes what a target covers, and the document contains **no per-category
figures at all**.

**Two more of my ground-truth labels were wrong** (the seventh and eighth in
this project, both from reading a phrase rather than what it asserts):
Occidental names Categories 9, 10 and 11 with no figures; Microsoft names
Categories 1, 2 and 11 and then says "Learn more in the Environmental Data
Fact Sheet", deferring the numbers to a separate document exactly as it does
for `scope1_absolute`. Corrected split: 3 present, 6 absent, 1 borderline.

**The real cause is Fault 6 reaching downstream.** Once a table has been
flattened into prose, "these are the categories that matter to us" and "here
is a figure for each category" are nearly the same string. The discriminating
evidence — numbers aligned to labels — is destroyed before the model sees it,
so no hypothesis rewrite and no retrieval change can recover it.

**Fix: a structural gate.** `DisclosureItem.min_anchors_with_figure` counts
how many *distinct* anchor terms appear within 80 characters of a
grouped-thousands figure across the retrieved chunks — the surviving trace of a
table row. Prose that merely names categories has no figure beside them. On the
labelled corpus the separation is clean: positives 5–9 categories-with-figures,
negatives 0–1.

Result, as-shipped: **9/9 labelled cells correct**, against a 0.67 base rate.
The gate blocks exactly the three confident false positives (Microsoft 0.974,
Occidental 0.896, Chevron 0.836) while keeping all three true positives.

**Two caveats that keep this honest:**
- The gate was designed after seeing this corpus, so 9/9 is **in-sample**. It
  is a definitional check rather than a fitted parameter — requiring two or
  more categories with figures is what "a breakdown" means — but it needs
  confirming on unseen companies.
- `calibrate.py`'s leave-one-out machinery sweeps thresholds over `score` and
  therefore **cannot see gates at all**; it still reports 0.56 for this item.
  That is why the calibration output now carries a separate as-shipped table.
  A gate has no fitted parameter to hold out, so leave-one-out is not the right
  instrument for it; out-of-sample companies are.
