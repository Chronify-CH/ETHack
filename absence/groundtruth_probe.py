"""Synonym-aware ground-truth probe for by-eye auditing.

Why this exists: MILESTONE1_RESULTS.md documents a real error where I recorded
ExxonMobil's `injury_rate_trir` as absent because `grep -i "trir"` found
nothing -- while the document actually disclosed "0.02 LTIR ... lost-time
incident rate per 200,000 work hours". The item's hypothesis explicitly
admits "TRIR *or equivalent workplace injury rate statistic*", so my search
terms were narrower than the item definition and the ground truth was wrong.

This module exists so that mistake is harder to repeat: each item gets an
explicit, deliberately broad set of surface forms a real disclosure might
use, and the probe prints every match with surrounding context for a human
to read. It does NOT decide presence/absence -- it surfaces candidate
evidence for a person to judge. An empty result is evidence of absence only
to the extent the synonym list is complete, which is exactly the assumption
that failed before, so treat an empty result as "nothing found with these
terms", not "confirmed absent".

Usage:
    python -m absence.groundtruth_probe <slug> <item_id>
    python -m absence.groundtruth_probe xom_energy injury_rate_trir
"""

import re
import sys

# Deliberately broader than items.py's regex_anchors: anchors are tuned for
# retrieval (precision matters, they feed BM25), these are tuned for auditing
# (recall matters, a human filters the noise).
GROUND_TRUTH_TERMS: dict[str, tuple[str, ...]] = {
    "scope1_absolute": (
        r"scope\s*1", r"direct emissions", r"direct ghg", r"operational emissions",
    ),
    "scope2_market_based": (
        r"scope\s*2", r"market[- ]based", r"purchased electricity", r"indirect emissions",
    ),
    "scope3_category_breakdown": (
        r"scope\s*3", r"category\s*\d+", r"purchased goods", r"use of sold products",
        r"end[- ]use", r"value chain emissions", r"upstream emissions", r"downstream",
    ),
    "target_net_zero_year": (
        r"net[- ]zero", r"net zero", r"carbon neutral", r"climate neutral",
        r"by 20\d\d", r"20\d\d target", r"emissions? target",
    ),
    "assurance_provider_named": (
        r"assurance", r"assured by", r"verified by", r"verification statement",
        r"independent (limited|reasonable)", r"third[- ]party (review|verif|assur)",
        r"\bERM\b", r"\bLRQA\b", r"\bDNV\b", r"\bApex\b", r"\bBureau Veritas\b", r"\bSGS\b",
        r"\bDeloitte\b", r"\bPwC\b", r"\bKPMG\b", r"\bEY\b", r"Ernst & Young",
    ),
    "board_committee_climate_mandate": (
        r"board committee", r"committee of the board", r"board of directors",
        r"audit committee", r"sustainability committee", r"governance committee",
        r"risk committee", r"board oversight", r"committee oversees",
    ),
    "injury_rate_trir": (
        # The synonym set that would have caught the ExxonMobil miss.
        r"\bTRIR\b", r"\bTRR\b", r"\bLTIR\b", r"\bDART\b", r"\bOSHA\b",
        r"recordable", r"lost[- ]time", r"incident rate", r"injury rate",
        r"per 200,000", r"fatalit",
    ),
    "scenario_analysis_quantified": (
        r"scenario analysis", r"climate scenario", r"\bIEA\b", r"\bNGFS\b",
        r"\bSSP\d", r"\bRCP\d", r"1\.5\s*°?\s*C", r"2\s*°?\s*C", r"below 2",
        r"stress test", r"transition risk", r"physical risk",
    ),
}


def probe(slug: str, item_id: str, context_chars: int = 110) -> list[str]:
    if item_id not in GROUND_TRUTH_TERMS:
        raise KeyError(f"no ground-truth terms defined for {item_id!r}")
    text = open(f"absence/data/raw/{slug}.txt").read()
    hits: list[str] = []
    seen_spans: list[tuple[int, int]] = []
    for pattern in GROUND_TRUTH_TERMS[item_id]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            if any(s <= match.start() <= e for s, e in seen_spans):
                continue
            seen_spans.append((start, end))
            snippet = re.sub(r"\s+", " ", text[start:end]).strip()
            hits.append(f"[{pattern}] ...{snippet}...")
    return hits


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    slug, item_id = sys.argv[1], sys.argv[2]
    hits = probe(slug, item_id)
    print(f"{slug} / {item_id}: {len(hits)} candidate span(s)")
    print("NOTE: an empty result means 'nothing matched these terms', NOT 'confirmed absent'.")
    for hit in hits[:25]:
        print("  -", hit)
    if len(hits) > 25:
        print(f"  ... and {len(hits) - 25} more")


if __name__ == "__main__":
    main()
