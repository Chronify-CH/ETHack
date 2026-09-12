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

Thresholds are now calibrated per item (items.py `calibrated_threshold`),
fitted by absence/calibrate.py against 60 hand-verified labels. There is no
usable global threshold: fitted per-item cut points span 0.03 to 0.94, and the
best global cut scored 0.73 leave-one-out against a 0.57 base rate. Section 11
asks for 200 labelled pairs; this is 60, verified by reading rather than
keyword matching, because six ground-truth errors in this project came from
labelling faster than that.
"""

import re

import torch
from rank_bm25 import BM25Okapi
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from absence.corpus.extract import Paragraph
from absence.detect.items import DisclosureItem

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Fault 1 (FAULTS.md): the BM25 query was the item's full hypothesis sentence
# plus its anchors, so high-frequency terms that appear in nearly every chunk
# of an emissions report ("company", "reported", "emissions", "data") swamped
# the discriminative ones. Measured consequence: for Apple's
# assurance_provider_named, nine chunks name "Apex Companies" and score from
# 0.001 to 0.995, and BM25's top-8 retrieved exactly one of them -- the
# joint-worst. These are dropped from the query. Deliberately small and
# hand-checked rather than a generic English stoplist: domain words like
# "scope" or "emissions" must survive even though they are frequent, because
# they are what distinguishes one item from another.
_QUERY_STOPWORDS = frozenset("""
a an the this that these those its their his her it they them
and or but if then than as at by for from in into of on to with without over under
is are was were be been being has have had do does did
company companys corporation firm organisation organization business
disclose disclosed disclosure disclosures report reported reporting reports
provide provided provides include included includes including
specific specified select selected such other others
information data figure figures number numbers value values
year years annual
""".split())


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _build_query(item: DisclosureItem) -> list[str]:
    """BM25 query: content terms from the hypothesis, with anchors weighted up.

    Anchors are repeated so BM25's term-frequency component favours chunks
    containing the item's distinctive vocabulary ("scope 1", "trir",
    "market-based") over chunks that merely share the hypothesis's ordinary
    English. Repetition is a blunt way to weight, but it needs no change to
    the BM25 implementation and is easy to reason about.
    """
    hypothesis_terms = [t for t in _tokenize(item.hypothesis) if t not in _QUERY_STOPWORDS]
    anchor_terms = _tokenize(" ".join(item.regex_anchors))
    return hypothesis_terms + anchor_terms * 3

MODEL_ID = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"

# Uncalibrated -- a placeholder cut point only, see module docstring.
STUB_FOUND_THRESHOLD = 0.5  # legacy default; superseded by per-item calibrated_threshold

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
    scores = bm25.get_scores(_build_query(item))
    ranked = sorted(zip(paragraphs, scores), key=lambda pair: pair[1], reverse=True)
    return [p for p, s in ranked[:k] if s > 0]


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+(?=[A-Z\"'“»•]|$)")


def sentence_windows(text: str, max_sentences: int = 2, min_chars: int = 25) -> list[str]:
    """Split a chunk into overlapping 1-2 sentence windows for scoring.

    Fault 2 (FAULTS.md): scoring a whole ~900-character chunk destroys the
    entailment signal. Measured on Occidental's board_committee_climate_mandate,
    where BM25 retrieved the correct chunk at rank 1:

        raw chunk, as previously scored            0.007
        the single sentence carrying the fact      0.939
        a clean paraphrase of the same fact        0.982

    A 134x difference on an identical claim. The model comprehends it either
    way; a chunk of concatenated headings, bullet glyphs and several unrelated
    statements is simply far outside the short fluent premises MNLI-style
    models are trained on.

    Windows of one and two sentences are both emitted: one-sentence windows
    give the cleanest premise, two-sentence windows catch facts split across a
    sentence boundary ("We obtained limited assurance. The reviewer was X.").
    Cost is roughly flat versus scoring whole chunks, because transformer cost
    scales with sequence length and these premises are ~5x shorter.
    """
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(text)]
    sentences = [s for s in sentences if len(s) >= min_chars]
    if not sentences:
        return [text] if text.strip() else []
    windows = list(sentences)
    if max_sentences >= 2:
        windows += [" ".join(sentences[i:i + 2]) for i in range(len(sentences) - 1)]
    return windows


SUB_BATCH = 16


@torch.inference_mode()
def score_paragraphs_batch(item: DisclosureItem, paragraph_texts: list[str]) -> list[float]:
    """Real NLI entailment probability for (premise, item.hypothesis) pairs.

    Premises are length-sorted and processed in sub-batches, then restored to
    the caller's order. This matters because `padding=True` pads every premise
    in a batch to the longest one in it: sentence-window scoring (Fault 2)
    produces a mix of ~35-character and ~900-character premises, and padding
    them together inflated cost 3.8x versus scoring whole chunks. Grouping
    similar lengths makes the padding waste small, so the Fault 2 fix costs
    roughly its honest ~1.5x rather than 3.8x.
    """
    if not paragraph_texts:
        return []
    tokenizer, model = _load()
    order = sorted(range(len(paragraph_texts)), key=lambda i: len(paragraph_texts[i]))
    scores = [0.0] * len(paragraph_texts)
    for start in range(0, len(order), SUB_BATCH):
        idxs = order[start:start + SUB_BATCH]
        batch = [paragraph_texts[i] for i in idxs]
        # DeBERTa-v3-MNLI convention: premise first, hypothesis second.
        inputs = tokenizer(
            batch,
            [item.hypothesis] * len(batch),
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_SEQ_LEN,
        )
        probs = torch.softmax(model(**inputs).logits, dim=-1)[:, 0]  # index 0 = "entailment"
        for i, p in zip(idxs, probs.tolist()):
            scores[i] = p
    return scores


def score_paragraph(item: DisclosureItem, paragraph_text: str) -> float:
    return round(score_paragraphs_batch(item, [paragraph_text])[0], 3)


def detect_item(item: DisclosureItem, paragraphs: list[Paragraph], k: int = DEFAULT_K):
    """Returns (found, best_score, best_evidence_text, source_chunk_idx).

    Retrieval works on chunks (BM25 needs the wider context to rank well);
    scoring works on sentence windows within those chunks (Fault 2). The
    returned evidence is the exact window that scored highest, which is also
    far more readable than the ~900-character chunk the previous version
    returned -- an auditor can see the supporting sentence directly instead of
    hunting for it inside a wall of concatenated text.
    """
    candidates = retrieve_candidates(item, paragraphs, k=k)
    if not candidates:
        return False, 0.0, None, None

    premises: list[str] = []
    origins: list[int] = []
    for chunk in candidates:
        for window in sentence_windows(chunk.text):
            premises.append(window)
            origins.append(chunk.idx)
    if not premises:
        return False, 0.0, None, None

    scores = score_paragraphs_batch(item, premises)
    best_i = max(range(len(scores)), key=lambda i: scores[i])
    best_score = round(scores[best_i], 3)
    # Per-item calibrated cut, not the old global 0.5. Fitted cut points span
    # 0.03 to 0.94 across these items because their score distributions are not
    # comparable; a single global cut scored 0.73 leave-one-out against a 0.57
    # base rate. See absence/calibrate.py and items.py.
    return best_score >= item.calibrated_threshold, best_score, premises[best_i], origins[best_i]
