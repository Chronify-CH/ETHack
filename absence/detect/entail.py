"""Milestone 1 item-detection via real BM25 retrieval + zero-shot NLI entailment.

Per ABSENCE_BRIEF.md Section 7: retrieve candidate paragraphs by anchor-term
BM25, then score each (premise=paragraph, hypothesis=item.hypothesis) pair
with an off-the-shelf MNLI-style model and take the max entailment
probability across candidates.

Model: MoritzLaurer/deberta-v3-base-zeroshot-v2.0 -- verified as the current,
maintained identifier via the model's HuggingFace API response (not assumed);
trained as a binary entailment/not_entailment classifier (id2label:
{0: "entailment", 1: "not_entailment"}), matching Section 7's
(premise, hypothesis) -> P(entailment) interface directly.

The "large" size of the same model was tried (run 4) and reverted: it scored
9/13 vs base's 10/13 on an identical by-eye audit while running 3.6x slower.
That one-cell difference is inside noise and does NOT establish base as
better -- but it does establish that large showed no measurable gain for its
cost. See MILESTONE1_RESULTS.md for the audit and, more importantly, for why
the pre-test that motivated the swap was misleading: it sampled only cells
the base model already failed, which cannot surface regressions.

HISTORY, kept because the failure modes are the point:
- First iteration: keyword-count retrieval + keyword-heuristic scoring stub.
  59% by-eye accuracy (corrected from 65%, see MILESTONE1_RESULTS.md);
  misses traced to keyword retrieval surfacing
  boilerplate/glossary text over the real supporting passage.
- Second iteration: same keyword-count retrieval, real entailment scoring
  (base model), but k cut 8->4 and truncation cut 512->256 tokens purely for
  CPU runtime. 33% by-eye accuracy -- WORSE. Root cause per
  MILESTONE1_RESULTS.md: this corpus's paragraphs average ~2,800 characters
  (tables merged into prose by the extraction deviation noted in extract.py),
  so cutting k and truncation meant the real evidence usually never reached
  the model at all.
- Third iteration: real BM25 (rank_bm25, proper term-frequency/IDF ranking,
  not raw anchor counting) over paragraphs pre-split by extract.rechunk() into
  bounded ~900-character chunks, base model, k restored to 8. 83% by-eye
  accuracy. Remaining failures isolated to one item (target_net_zero_year)
  where retrieval found good evidence and the base model still scored
  entailment near zero on both audited cases.
- Fourth iteration (large model, REVERTED): targeted test against exactly those two
  failing cases, using their real retrieved evidence text and each item's own
  hypothesis (not a shared placeholder), confirmed the large model fixes one
  outright (0.069 -> 0.955) and substantially improves the other
  (0.021 -> 0.464, now borderline rather than clearly wrong), with no
  regression on two control cases re-tested with their own hypotheses.
  The full run then scored 9/13 vs base's 10/13 on the identical audit, at
  3.6x the cost (77 minutes vs ~21), introducing a confident false positive
  (Chevron scope3, 0.857) and re-introducing the Apex-style false negative
  run 3 had fixed (Apple assurance, 0.027 on a passage naming two providers).
  Reverted. The lesson is about the pre-test, not the model: sampling only
  cells the incumbent already fails cannot surface regressions, so it can
  only ever look favourable.

STUB_FOUND_THRESHOLD is still an uncalibrated placeholder cut point -- formal
calibration against 200 hand-labelled item/report pairs, with per-item
precision/recall, is Milestone 2's job (Section 11), not this one's.
"""

import re

import torch
from rank_bm25 import BM25Okapi
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from absence.corpus.extract import Paragraph
from absence.detect.items import DisclosureItem

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())

MODEL_ID = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"

# Uncalibrated -- a placeholder cut point only, see module docstring.
STUB_FOUND_THRESHOLD = 0.5

# CPU-only performance tuning (measured empirically on this environment's
# 4-core machine against real corpus text via extract.rechunk()-bounded
# chunks, not synthetic samples). Chunks are now bounded to ~900 characters
# (roughly 160-200 tokens for this corpus's prose), so MAX_SEQ_LEN=256 rarely
# truncates real content anymore -- unlike the previous iteration, where
# candidates were the raw ~2,800-character merged paragraphs and truncation
# routinely cut off the disclosed fact before the model saw it. DEFAULT_K=8
# (up from 4) was chosen because BM25 with bounded chunks measured ~20s per
# 8-candidate batch on the worst-case document (ConocoPhillips) -- an
# estimated ~25 minutes for the full 10-document corpus, accepted here in
# exchange for retrieval actually having a chance to surface the real
# evidence, which the smaller k could not (see MILESTONE1_RESULTS.md).
MAX_SEQ_LEN = 256
DEFAULT_K = 8
torch.set_num_threads(4)

_tokenizer = None
_model = None


def _load():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        _model.eval()
        assert _model.config.id2label[0] == "entailment", (
            f"unexpected label order from {MODEL_ID}: {_model.config.id2label}"
        )
    return _tokenizer, _model


def retrieve_candidates(item: DisclosureItem, paragraphs: list[Paragraph], k: int = DEFAULT_K) -> list[Paragraph]:
    """Real BM25 retrieval, query-expanded with the item's anchor terms.

    Per Section 7: "retrieve the top-k candidate paragraphs by anchor-term
    BM25". The query is the item's hypothesis plus its regex_anchors list
    (anchors get the query closer to the specific vocabulary a real
    disclosure would use, e.g. "scope 1", "tonnes"); BM25's term-frequency/
    inverse-document-frequency weighting (not raw anchor-hit counting) then
    ranks chunks. A zero-score chunk is dropped rather than padding out k --
    BM25 with a well-formed query returning score 0 means no query term
    appears in that chunk at all, which is a stronger signal than "ran out of
    anchor hits" was in the earlier keyword-count version.
    """
    if not paragraphs:
        return []
    corpus_tokens = [_tokenize(p.text) for p in paragraphs]
    bm25 = BM25Okapi(corpus_tokens)
    query_tokens = _tokenize(item.hypothesis + " " + " ".join(item.regex_anchors))
    scores = bm25.get_scores(query_tokens)
    ranked = sorted(zip(paragraphs, scores), key=lambda pair: pair[1], reverse=True)
    return [p for p, s in ranked[:k] if s > 0]


@torch.inference_mode()
def score_paragraphs_batch(item: DisclosureItem, paragraph_texts: list[str]) -> list[float]:
    """Real NLI entailment probability for (paragraph, item.hypothesis) pairs."""
    if not paragraph_texts:
        return []
    tokenizer, model = _load()
    # DeBERTa-v3-MNLI convention: premise first, hypothesis second.
    inputs = tokenizer(
        paragraph_texts,
        [item.hypothesis] * len(paragraph_texts),
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_SEQ_LEN,
    )
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)
    return probs[:, 0].tolist()  # index 0 = "entailment"


def score_paragraph(item: DisclosureItem, paragraph_text: str) -> float:
    return round(score_paragraphs_batch(item, [paragraph_text])[0], 3)


def detect_item(item: DisclosureItem, paragraphs: list[Paragraph], k: int = DEFAULT_K):
    """Returns (found: bool, best_score: float, best_paragraph: Paragraph | None)."""
    candidates = retrieve_candidates(item, paragraphs, k=k)
    if not candidates:
        return False, 0.0, None
    scores = score_paragraphs_batch(item, [p.text for p in candidates])
    scored = list(zip(candidates, scores))
    scored.sort(key=lambda pair: pair[1], reverse=True)
    best_paragraph, best_score = scored[0]
    best_score = round(best_score, 3)
    return best_score >= STUB_FOUND_THRESHOLD, best_score, best_paragraph
