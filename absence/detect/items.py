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
        # Rewritten after run 5 measured precision 60% (4 false positives:
        # ExxonMobil, Chevron, JPMorgan, Goldman) on 10/10 detections. The old
        # anchors included the bare token "category", which matched Bank of
        # America's Equator Principles "Category A / Category B / Category C"
        # project classifications and Goldman's "asset class breakdown", neither
        # of which is a Scope 3 category. The hypothesis also failed to require
        # per-category figures, so any methodology paragraph mentioning Scope 3
        # could satisfy it.
        hypothesis=(
            "The company reported a numeric breakdown of its Scope 3 greenhouse "
            "gas emissions across individual GHG Protocol categories, giving "
            "separate figures for categories such as purchased goods and "
            "services, business travel, or use of sold products, rather than a "
            "single combined Scope 3 total."
        ),
        # Only category names specific enough that they cannot occur as ordinary
        # English. "investments" and "capital goods" are deliberately excluded:
        # both appear constantly in financial reports in their everyday sense.
        regex_anchors=(
            "scope 3", "scope3",
            "purchased goods and services", "use of sold products",
            "employee commuting", "business travel",
            "fuel- and energy-related", "upstream transportation",
            "downstream transportation", "processing of sold products",
            "end-of-life treatment", "waste generated in operations",
            "category 1:", "category 11:", "category 15:",
        ),
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
        # Rewritten after run 5 measured precision 0% -- seven detections, all
        # false. Verified ground truth: no company in this corpus attaches a
        # monetary figure to scenario-analysis results (six discuss scenario
        # analysis; none quantify it), so every detection was wrong. The old
        # anchors included the bare tokens "$", "million" and "billion", which
        # match any financial passage in documents full of them: the detections
        # landed on a G-SIB capital surcharge, a Green Fund, a Climate
        # Innovation Fund, an industry initiative and a non-GAAP header. The
        # hypothesis also said "quantified dollar financial impact" without
        # tying the figure to scenario analysis as its source.
        hypothesis=(
            "The company estimated, using climate scenario analysis, a specific "
            "monetary amount of financial impact on its business -- for example "
            "expected losses, asset write-downs, or costs expressed in dollars "
            "under a named climate scenario."
        ),
        # Scenario-identifying terms only. No bare currency or magnitude tokens:
        # the monetary requirement belongs in the hypothesis, which the NLI model
        # evaluates, not in retrieval, which cannot tell a scenario-derived
        # figure from any other number.
        regex_anchors=(
            "scenario analysis", "climate scenario", "scenario planning",
            "ngfs", "iea scenario", "sds scenario", "net zero 2050 scenario",
            "1.5°c scenario", "2°c scenario", "below 2°c", "orderly transition",
            "disorderly transition", "climate stress test", "stress testing",
        ),
    ),
)

ITEMS_BY_ID = {item.id: item for item in ITEMS}
