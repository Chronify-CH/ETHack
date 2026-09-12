# How to read Milestone 1's output

Three kinds of file matter. This is a guide to all three, plus the traps to avoid
when reading them.

> **Start here instead if you want one document at a time.**
> `absence/reports/INDEX.md` lists all ten analysed reports. Each
> `absence/reports/<slug>/` folder holds `source.txt` — the exact extracted text
> that was scored — next to `analysis.md`, which gives that document's per-item
> score, threshold, gate, decision, hand-verified label and the evidence span
> the score came from. That is the fastest way to check a single company; the
> three file types below are the corpus-wide view.

## 1. The console silence table (`python -m absence.milestone1`)

```
company                      sector        paras  scope1_abs  scope2_mar ...
Apple Inc.                   Technology      594  FOUND 0.736  FOUND 0.937 ...
```

- **`paras`** is the chunk count after `extract.rechunk()`, not raw paragraph
  count -- a document rechunked into 594 pieces isn't necessarily "denser"
  than one at 130; it just has more oversized blocks that needed splitting.
- **Each item cell** is `FOUND <score>`, `absent <score>`, or `n/a`.
  `n/a` means the item's `sector_applicability` in `items.py` excludes this
  company's sector (e.g. `injury_rate_trir` only applies to Energy) -- it is
  not a detection result at all, don't count it as either a hit or a miss.
- **The score is the model's raw entailment probability** (0-1), not a
  confidence percentage in the everyday sense. `FOUND` just means
  `score >= STUB_FOUND_THRESHOLD` (0.5, in `entail.py` -- see the trap below).

## 2. The full JSON (`absence/data/milestone1_results*.json`)

> **Which file is which.** `milestone1_results_run4_large.json` /
> `milestone1_run4_large.log` are run 4's output (the large model, since
> reverted -- see `MILESTONE1_RESULTS.md`). They are kept because the audit
> in that document cites them. Re-running `python -m absence.milestone1`
> with the current code writes `milestone1_results.json` using the base
> model, which is what the committed code actually does.

Same data as the table, plus the `snippet` field for every cell: the first
~220 characters of the actual retrieved chunk that produced the score. **This
is the important field.** The label alone (`found`/`absent`) tells you what
the system concluded; the snippet tells you *why*, and is the only way to
tell a correct answer from a right-label-wrong-reason answer (both happened
repeatedly across this milestone's three runs -- see `MILESTONE1_RESULTS.md`).
Read the snippet before trusting the label, always.

```python
import json
r = json.load(open("absence/data/milestone1_results.json"))
apple = next(row for row in r if row["company"] == "Apple Inc.")
print(apple["items"]["scope1_absolute"])
# {"applicable": true, "found": true, "score": 0.736, "snippet": "..."}
```

## 3. The per-item run log (`absence/data/milestone1_run*.log`)

Timestamped, per-item progress with per-batch timing -- useful for "did this
actually run, and how long did each part take," not for interpreting results.

## The three traps

**Trap 1: a FOUND/absent label is not proof, it's a pointer.** Always read
the snippet. Three real examples from this milestone where the label was
right and the evidence wasn't, or vice versa:
- Chevron's `scope3_category_breakdown` came back correctly `absent`, but the
  retrieved snippet was a list of board members' names -- irrelevant
  evidence that happened to produce a low score for the right reason by
  accident, not by understanding.
- Apple's `assurance_provider_named` came back `FOUND` with a snippet that
  cuts off mid-sentence right before the actual provider name appears
  ("Apple's independent assurance provider for the Supplie...") -- correct,
  but you have to go back to the source document to see the name itself.
- Apple's `target_net_zero_year` came back `absent` at 0.069 in run 3, with a
  snippet that says outright "Our plan to become carbon neutral by 2030" --
  a case where the retrieved evidence was exactly right and the model's
  score was simply wrong. (Run 4's large model scored this one correctly at
  0.721 -- but scored Apple's `assurance_provider_named` at 0.027 on a
  passage naming two providers outright, so the failure moved rather than
  went away.)

**Trap 2: `n/a` is not "not disclosed."** It means the item wasn't checked
for that company at all because it isn't material for that sector in
`items.py`. Counting `n/a` as either found or absent will silently distort
any aggregate score computed from this table.

**Trap 3: none of these scores are calibrated.** `STUB_FOUND_THRESHOLD = 0.5`
in `entail.py` is a placeholder, not a number derived from data. A company
scoring 0.51 and one scoring 0.49 are printed as opposite labels but are not
meaningfully different. `ABSENCE_BRIEF.md` Section 11 calls for calibrating
this threshold against 200 hand-labelled item/report pairs with reported
precision/recall per item -- that hasn't happened yet (it's Milestone 2).
Until it does, treat the silence table as "here's what the pipeline currently
outputs, for inspection," not "here's a company's real disclosure score."

## If you want the honest bottom line for a single cell

1. Open `milestone1_results.json`, find the company and item.
2. Read the `snippet`. Does it actually say what the item's `hypothesis` (in
   `items.py`) claims?
3. If you're unsure, run the synonym-aware probe rather than an ad-hoc grep:
   `python -m absence.groundtruth_probe <slug> <item_id>`. It searches a
   deliberately broad set of surface forms per item and prints each match in
   context. This exists because an ad-hoc grep *did* produce a wrong ground
   truth in this milestone (searching "trir" missed ExxonMobil's "0.02 LTIR
   ... lost-time incident rate"), so prefer it over inventing search terms.
   An empty probe result means "nothing matched these terms", not "confirmed
   absent".

## Comparing across the four runs

`MILESTONE1_RESULTS.md` has the full history and a per-cell table. Short
version: don't assume a more sophisticated method produced a better result
without checking. Run 2 (real model, worse retrieval) scored *worse* than
run 1 (a keyword-matching stub), because the model can only be as good as the
evidence retrieval hands it; run 3 (real BM25 + bounded chunks) fixed that;
run 4 (a 3.6x larger model, same retrieval) scored *worse again* and was
reverted. Two lessons generalize: when auditing any future run, check
retrieval (did the right paragraph get considered at all?) before blaming
the model -- and never evaluate a proposed change only on the cases the
incumbent already fails, which is how run 4's swap came to look justified.
