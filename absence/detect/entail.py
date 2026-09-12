"""Milestone 1 item-detection via real zero-shot NLI entailment.

Per ABSENCE_BRIEF.md Section 7: retrieve candidate paragraphs by anchor-term
overlap (standing in for prefilter.py's BM25 pass at this milestone's scale),
then score each (premise=paragraph, hypothesis=item.hypothesis) pair with an
off-the-shelf MNLI-style model and take the max entailment probability across
candidates.

Model: MoritzLaurer/deberta-v3-base-zeroshot-v2.0 -- verified as the current,
maintained identifier via the model's HuggingFace API response (not assumed);
it is the author's own recommended default for zero-shot NLI use, trained
specifically as a binary entailment / not_entailment classifier (id2label:
{0: "entailment", 1: "not_entailment"}), which is exactly the (premise,
hypothesis) -> P(entailment) interface Section 7 calls for -- no 3-way
NLI-to-binary conversion needed.

This replaces the keyword-heuristic stub from the first iteration of this
milestone (see git history / MILESTONE1_RESULTS.md for that stub's behavior
and its 65% by-eye accuracy, with every miss traced to keyword retrieval
surfacing boilerplate/glossary text over the real supporting passage). The
retrieval step below is unchanged (still anchor-term overlap, not real BM25 or
semantic retrieval) -- the model change only affects scoring, so retrieval
misses are still possible if the real evidence never makes it into the
top-k candidates.

STUB_FOUND_THRESHOLD is still an uncalibrated placeholder cut point -- formal
calibration against 200 hand-labelled item/report pairs, with per-item
precision/recall, is Milestone 2's job (Section 11), not this one's.
"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from absence.corpus.extract import Paragraph
from absence.detect.items import DisclosureItem

MODEL_ID = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"

# Uncalibrated -- a placeholder cut point only, see module docstring.
STUB_FOUND_THRESHOLD = 0.5

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


def _anchor_hits(item: DisclosureItem, text: str) -> int:
    lowered = text.lower()
    return sum(1 for anchor in item.regex_anchors if anchor.lower() in lowered)


def retrieve_candidates(item: DisclosureItem, paragraphs: list[Paragraph], k: int = 8) -> list[Paragraph]:
    """Cheap anchor-term retrieval standing in for prefilter.py's BM25 pass."""
    scored = [(p, _anchor_hits(item, p.text)) for p in paragraphs]
    scored = [(p, s) for p, s in scored if s > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return [p for p, _ in scored[:k]]


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
        max_length=512,
    )
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)
    return probs[:, 0].tolist()  # index 0 = "entailment"


def score_paragraph(item: DisclosureItem, paragraph_text: str) -> float:
    return round(score_paragraphs_batch(item, [paragraph_text])[0], 3)


def detect_item(item: DisclosureItem, paragraphs: list[Paragraph], k: int = 8):
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
