"""Milestone 1 disclosure item inventory.

This is a deliberately small subset (8 items) of the ~50-item inventory specified
in ABSENCE_BRIEF.md Section 7, chosen to span multiple pillars and sectors, per
Section 13's Milestone 1 scope. The full inventory is Milestone 2.

Each item carries:
  id                    stable identifier, matches ABSENCE_BRIEF.md naming
  pillar                one of the six veritas/framework.py pillars this feeds
  hypothesis            natural-language claim for NLI entailment scoring
  regex_anchors         cheap keyword/regex terms used to retrieve candidate
                         paragraphs before entailment is run (prefilter.py's job
                         at full scale; used directly here at Milestone 1 scale)
  sector_applicability  GICS sectors (as used in this corpus) this item is
                         material for; empty tuple = applicable to all sectors
  granularity_levels    human-readable description of the 0-4 granularity scale
                         for this item (Section 7)
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DisclosureItem:
    id: str
    pillar: str
    hypothesis: str
    regex_anchors: tuple[str, ...]
    sector_applicability: tuple[str, ...] = field(default_factory=tuple)
    granularity_levels: tuple[str, ...] = (
        "0 absent",
        "1 qualitative mention only",
        "2 a number",
        "3 number + baseline year + scope boundary",
        "4 all of the above + third-party assured",
    )


ITEMS: tuple[DisclosureItem, ...] = (
    DisclosureItem(
        id="scope1_absolute",
        pillar="INTEGRITY",
        hypothesis=(
            "The company disclosed its absolute Scope 1 greenhouse gas emissions "
            "in tonnes of CO2 equivalent."
        ),
        regex_anchors=("scope 1", "scope1", "direct emissions", "co2e", "co2-e", "mtco2"),
    ),
    DisclosureItem(
        id="scope2_market_based",
        pillar="INTEGRITY",
        hypothesis=(
            "The company disclosed its market-based Scope 2 greenhouse gas "
            "emissions in tonnes of CO2 equivalent."
        ),
        regex_anchors=("scope 2", "scope2", "market-based", "market based"),
    ),
    DisclosureItem(
        id="scope3_category_breakdown",
        pillar="INTEGRITY",
        hypothesis=(
            "The company disclosed a breakdown of its Scope 3 greenhouse gas "
            "emissions by individual category (such as purchased goods and "
            "services, use of sold products, or investments), not just a single "
            "combined Scope 3 total."
        ),
        regex_anchors=("scope 3", "scope3", "category 1", "category 11", "category 15", "purchased goods", "use of sold products"),
    ),
    DisclosureItem(
        id="target_net_zero_year",
        pillar="TRAJECTORY",
        hypothesis=(
            "The company disclosed a specific target year by which it aims to "
            "reach net-zero greenhouse gas emissions."
        ),
        regex_anchors=("net zero", "net-zero", "carbon neutral", "by 2050", "by 2030", "by 2040"),
    ),
    DisclosureItem(
        id="assurance_provider_named",
        pillar="INTEGRITY",
        hypothesis=(
            "The company named the specific third-party firm that provided "
            "external assurance or verification over its reported emissions data."
        ),
        regex_anchors=("assurance", "independent verification", "verified by", "assured by", "limited assurance", "reasonable assurance"),
    ),
    DisclosureItem(
        id="board_committee_climate_mandate",
        pillar="INTEGRITY",
        hypothesis=(
            "The company disclosed that a specific board committee holds "
            "explicit oversight responsibility for climate-related risks."
        ),
        regex_anchors=("board committee", "board of directors", "oversight", "governance committee", "risk committee"),
    ),
    DisclosureItem(
        id="injury_rate_trir",
        pillar="SOCIAL",
        hypothesis=(
            "The company disclosed a numeric total recordable incident rate "
            "(TRIR) or equivalent workplace injury rate statistic."
        ),
        regex_anchors=("trir", "total recordable incident rate", "recordable injury", "lost time incident", "safety performance"),
        sector_applicability=("Energy",),
    ),
    DisclosureItem(
        id="scenario_analysis_quantified",
        pillar="OPTIONALITY",
        hypothesis=(
            "The company disclosed a quantified dollar financial impact from "
            "climate scenario analysis, not merely a statement that scenario "
            "analysis was conducted."
        ),
        regex_anchors=("scenario analysis", "climate scenario", "1.5", "2 degree", "physical risk", "transition risk", "$", "billion", "million"),
    ),
)

ITEMS_BY_ID = {item.id: item for item in ITEMS}
