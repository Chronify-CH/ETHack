"""Milestone 1 item-detection scorer.

STUB, NOT THE REAL METHOD -- LOGGED HONESTLY:

ABSENCE_BRIEF.md Section 7 specifies zero-shot NLI entailment against a strong
off-the-shelf MNLI model (the DeBERTa-v3-MNLI family) as the detection method:
retrieve candidate paragraphs by anchor-term BM25, then score
(premise=paragraph, hypothesis=item.hypothesis) -> entailment probability.

This environment's network egress blocks huggingface.co, so no such model can
be downloaded here (confirmed: pip/requests/curl all get a 403 from the egress
proxy; this is an environment/session network-policy restriction, not a code
problem). What follows is a keyword-overlap-plus-heuristic stand-in with the
SAME call signature the real entailment call will have
(score_paragraph(item, paragraph_text) -> float in [0, 1]), so that swapping in
real DeBERTa-v3-MNLI later is a one-function change, not a rewrite.

This stub has NOT been calibrated against the 200 hand-labelled item/report
pairs Section 11 calls for (that calibration is meaningless without the real
model), and its scores/thresholds must not be read as measuring anything about
the companies -- only as a mechanical placeholder proving the pipeline
plumbing (retrieval -> scoring -> silence table) runs end to end on real text.
"""

import re

from absence.corpus.extract import Paragraph
from absence.detect.items import DisclosureItem

_NUMBER_RE = re.compile(r"\b\d[\d,]*(\.\d+)?\s*(%|percent|tonnes?|tco2e?|mtco2e?|million|billion|\$)?\b", re.IGNORECASE)

# Uncalibrated -- a placeholder cut point only, see module docstring.
STUB_FOUND_THRESHOLD = 0.35


def _anchor_hits(item: DisclosureItem, text: str) -> int:
    lowered = text.lower()
    return sum(1 for anchor in item.regex_anchors if anchor.lower() in lowered)


def retrieve_candidates(item: DisclosureItem, paragraphs: list[Paragraph], k: int = 5) -> list[Paragraph]:
    """Cheap anchor-term retrieval standing in for prefilter.py's BM25 pass."""
    scored = [(p, _anchor_hits(item, p.text)) for p in paragraphs]
    scored = [(p, s) for p, s in scored if s > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return [p for p, _ in scored[:k]]


def score_paragraph(item: DisclosureItem, paragraph_text: str) -> float:
    """Stub entailment probability. See module docstring: not calibrated NLI."""
    hits = _anchor_hits(item, paragraph_text)
    if hits == 0:
        return 0.0
    anchor_density = min(hits / max(len(item.regex_anchors), 1), 1.0)
    has_number = bool(_NUMBER_RE.search(paragraph_text))
    score = 0.5 * anchor_density + (0.5 if has_number else 0.0)
    return round(min(score, 1.0), 3)


def detect_item(item: DisclosureItem, paragraphs: list[Paragraph], k: int = 5):
    """Returns (found: bool, best_score: float, best_paragraph: Paragraph | None)."""
    candidates = retrieve_candidates(item, paragraphs, k=k)
    if not candidates:
        return False, 0.0, None
    scored = [(p, score_paragraph(item, p.text)) for p in candidates]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    best_paragraph, best_score = scored[0]
    return best_score >= STUB_FOUND_THRESHOLD, best_score, best_paragraph
