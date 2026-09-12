"""Milestone 1 text-to-paragraph segmentation.

DEVIATION FROM ABSENCE_BRIEF.md SECTION 5, LOGGED HONESTLY:

The brief specifies PyMuPDF block-level extraction directly from raw PDF bytes
(bounding boxes, geometric dropping of captions/sidebars, tables kept separate
from prose) as the extraction method, because naive text extraction is known to
interleave multi-column ESG report layouts into nonsense.

This environment's network egress does not allow downloading raw PDF bytes
(see the corpus provenance log at absence/data/provenance.json --
retrieved_via notes this for every document). The only working path to real
report content was the TinyFish web-fetch connector, which returns its own
already-flattened text extraction, not raw bytes -- so PyMuPDF block extraction
is not possible on this corpus. What follows is paragraph segmentation over
that already-extracted text, which is a strictly weaker method than the brief
specifies. It was validated by eye against the source documents (see the
milestone1 runner's printed spot-checks) and did not show the column-
interleaving failure mode the brief warns about for these particular
documents, but this has not been verified at corpus scale and should not be
assumed to hold for documents with more complex layouts.

Whoever picks up Milestone 3 (corpus build) should replace this module with
real PyMuPDF block extraction the moment raw PDF bytes are obtainable.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Paragraph:
    idx: int
    text: str


_PAGE_MARKER_RE = re.compile(r"^\s*(page\s+)?\d{1,4}\s*$", re.IGNORECASE)
_BULLET_PREFIX_RE = re.compile(r"^[\*\-•]\s+")


def _is_boilerplate(line: str) -> bool:
    """Filter obvious non-prose lines: bare page numbers, markdown table rules."""
    stripped = line.strip()
    if not stripped:
        return True
    if _PAGE_MARKER_RE.match(stripped):
        return True
    if set(stripped) <= {"-", "|", " ", ":"}:
        return True
    return False


def segment_paragraphs(text: str, min_chars: int = 120) -> list[Paragraph]:
    """Split extracted document text into paragraph-sized chunks.

    Paragraphs are delimited by blank lines (the standard markdown convention
    TinyFish's extractor emits). Short fragments (headers, table-of-contents
    entries, captions) below min_chars are dropped -- they are exactly the
    kind of non-prose material the brief's own PyMuPDF approach would drop by
    geometry; here it is done by length instead, a cruder proxy.
    """
    raw_blocks = re.split(r"\n\s*\n", text)
    paragraphs: list[Paragraph] = []
    idx = 0
    for block in raw_blocks:
        lines = [ln for ln in block.splitlines() if not _is_boilerplate(ln)]
        if not lines:
            continue
        joined = " ".join(_BULLET_PREFIX_RE.sub("", ln).strip() for ln in lines)
        joined = re.sub(r"\s+", " ", joined).strip()
        if len(joined) < min_chars:
            continue
        paragraphs.append(Paragraph(idx=idx, text=joined))
        idx += 1
    return paragraphs
