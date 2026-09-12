"""Stage B classification: ClimateBERT paragraph/sentence heads + cheap-talk index.

Per ABSENCE_BRIEF.md Section 6: four pretrained ClimateBERT classifiers, no
labelling required. Model identifiers verified live against the HuggingFace
API (not assumed) -- all four resolve and each returns a clean binary
id2label ({"0": <negative>, "1": <positive>}), so every score below is
P(positive class) from a plain softmax, no label-order guessing:

    climatebert/distilroberta-base-climate-detector      paragraph  {0: no,  1: yes}
    climatebert/distilroberta-base-climate-specificity   paragraph  {0: non, 1: spec}
    climatebert/distilroberta-base-climate-commitment    paragraph  {0: no,  1: yes}
    climatebert/environmental-claims                     SENTENCE   {0: no,  1: yes}

Section 6 is explicit that specificity/commitment are trained on paragraphs
and "the authors warn they degrade on sentences" -- so paragraphs (this
milestone's Paragraph/rechunk() output) go to the first three models, and a
separate, cruder sentence split (see _split_sentences) goes only to
environmental-claims. Do not feed one granularity to the other's model.

Cheap talk index, per the ClimateBERT authors' own suggested construction
(Section 6): cheap_talk = P(commitment) * (1 - P(specific)) -- high when a
paragraph reads as an action/commitment statement without being concrete.
Computed here per-paragraph, then aggregated per document as the mean over
paragraphs the detector scores as climate-related (P(climate) >= 0.5); this
aggregation rule is a Milestone 1 choice, not something Section 6 specifies
verbatim, and should be revisited once there's a real corpus to validate it
against.

Sanity-checked by eye against the first 15 chunks of Apple's report (not the
full corpus -- that run is deferred to avoid competing for CPU with the
concurrent large-model entailment run): all 15 correctly scored as
climate-related (p_climate ~0.998, unsurprising for an environmental report).
Within that sample, the lowest cheap_talk score (0.03) landed on "Carbon
neutral for corporate emissions... we've achieved carbon neutral..." -- a
concrete, specific factual claim (p_specific=0.97). The highest (0.781)
landed on "...we have to meet a global challenge with global solutions --
solutions that center on people..." -- vague, aspirational, low specificity
(0.156) despite high commitment (0.925). That is exactly the intended
behavior: the index is discriminating concrete disclosure from aspirational
rhetoric on real text, not just producing plausible-looking numbers. This is
a small-sample sanity check, not the full-corpus by-eye audit
MILESTONE1_RESULTS.md ran for entailment -- do that before relying on this
module's aggregate cheap_talk_index for anything beyond spot-checking.
"""

import re

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from absence.corpus.extract import Paragraph

DETECTOR_MODEL = "climatebert/distilroberta-base-climate-detector"
SPECIFICITY_MODEL = "climatebert/distilroberta-base-climate-specificity"
COMMITMENT_MODEL = "climatebert/distilroberta-base-climate-commitment"
CLAIMS_MODEL = "climatebert/environmental-claims"

MAX_SEQ_LEN = 256  # same CPU-runtime rationale as entail.py; these paragraphs are pre-bounded by rechunk()

_registry: dict[str, tuple] = {}  # model_id -> (tokenizer, model)

torch.set_num_threads(4)


def _load(model_id: str):
    if model_id not in _registry:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSequenceClassification.from_pretrained(model_id)
        model.eval()
        _registry[model_id] = (tokenizer, model)
    return _registry[model_id]


@torch.inference_mode()
def _score_positive_class(model_id: str, texts: list[str]) -> list[float]:
    """P(label==1) for each text, batched. Positive class is index 1 for all four models."""
    if not texts:
        return []
    tokenizer, model = _load(model_id)
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=MAX_SEQ_LEN)
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)
    return probs[:, 1].tolist()


# Deliberately simple: split on sentence-ending punctuation followed by
# whitespace and a capital letter or end of string. Section 6 only requires
# that environmental-claims gets sentences rather than paragraphs -- it does
# not require a fully correct sentence tokenizer, and building one (handling
# abbreviations, decimal numbers, etc.) is out of scope for this milestone.
# Known failure mode: "e.g." or "U.S." will sometimes trigger a false split.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'“]|$)")


def _split_sentences(text: str, min_chars: int = 15) -> list[str]:
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(text)]
    return [s for s in sentences if len(s) >= min_chars]


def classify_paragraphs(paragraphs: list[Paragraph]) -> list[dict]:
    """Per-paragraph scores from the three paragraph-level ClimateBERT heads."""
    texts = [p.text for p in paragraphs]
    p_climate = _score_positive_class(DETECTOR_MODEL, texts)
    p_specific = _score_positive_class(SPECIFICITY_MODEL, texts)
    p_commitment = _score_positive_class(COMMITMENT_MODEL, texts)
    results = []
    for para, pc, ps, pcm in zip(paragraphs, p_climate, p_specific, p_commitment):
        cheap_talk = pcm * (1 - ps)
        results.append({
            "idx": para.idx,
            "p_climate": round(pc, 3),
            "p_specific": round(ps, 3),
            "p_commitment": round(pcm, 3),
            "cheap_talk": round(cheap_talk, 3),
        })
    return results


def classify_sentences_environmental_claims(paragraphs: list[Paragraph]) -> dict:
    """Sentence-level environmental-claims rate, per Section 6's granularity split."""
    sentences: list[str] = []
    for para in paragraphs:
        sentences.extend(_split_sentences(para.text))
    if not sentences:
        return {"n_sentences": 0, "n_environmental_claims": 0, "environmental_claim_rate": 0.0}
    scores = _score_positive_class(CLAIMS_MODEL, sentences)
    n_claims = sum(1 for s in scores if s >= 0.5)
    return {
        "n_sentences": len(sentences),
        "n_environmental_claims": n_claims,
        "environmental_claim_rate": round(n_claims / len(sentences), 3),
    }


def document_cheap_talk_index(paragraph_scores: list[dict]) -> dict:
    """Aggregate per-paragraph cheap_talk into one document-level number.

    Mean cheap_talk over paragraphs the detector scores as climate-related
    (p_climate >= 0.5) -- averaging over non-climate paragraphs (community
    volunteering, office recycling, per Section 6's own examples) would
    dilute the signal with paragraphs the index isn't meant to describe.
    """
    climate_scores = [row["cheap_talk"] for row in paragraph_scores if row["p_climate"] >= 0.5]
    if not climate_scores:
        return {"n_climate_paragraphs": 0, "cheap_talk_index": None}
    return {
        "n_climate_paragraphs": len(climate_scores),
        "cheap_talk_index": round(sum(climate_scores) / len(climate_scores), 3),
    }
