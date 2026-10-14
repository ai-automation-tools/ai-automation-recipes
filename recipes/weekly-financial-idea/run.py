#!/usr/bin/env python3
"""Financial Idea — one runnable personal-finance app prototype per run, rotating themes.

    python recipes/weekly-financial-idea/run.py --output-dir ~/ai-output [--theme Debt]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from recipes._shared.webcheck import check_json, check_refs, node_check  # noqa: E402

THEMES: dict[str, str] = {
    "Investing": "Brokerage basics, index funds, dividends, dollar-cost averaging, allocation and "
                 "rebalancing, expense ratios, retirement accounts (401(k) / IRA / Roth), FIRE math. "
                 "Tools, organizers and education — never personalized 'buy this' advice.",
    "Budgeting": "Spending tracking, cash flow, zero-based or envelope budgeting, subscription audits, "
                 "bill calendars, category breakdowns.",
    "Saving": "Emergency-fund planning, savings goals and sinking funds, high-yield savings / APY "
              "comparison, CD laddering, automatic-transfer planning.",
    "Rewards": "Credit-card points and miles, category multipliers, welcome-bonus tracking, card-portfolio "
               "optimization, portal + card + gift-card stacking, redemption value.",
    "Discounts": "Cashback, coupons, price-drop tracking, price-per-unit comparison, sale-cycle timing, "
                 "membership break-even.",
    "Debt": "Payoff strategies (avalanche vs snowball), credit-score factors, loan / APR comparison, "
            "refinancing break-even, amortization.",
    "Taxes": "Tax-advantaged account planning, deduction organizers, estimated-payment helpers, "
             "withholding checkups. Educational only — not tax advice.",
    "Net-Worth": "Net-worth dashboards, financial-goal trackers, savings-rate visualizers.",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--theme", choices=sorted(THEMES), help="Override the theme rotation.")


def prepare(ctx: RunContext) -> dict[str, str]:
    theme = ctx.args.theme or least_used(list(THEMES), ctx.existing, "theme")
    return {"THEME": theme, "THEME_GUIDE": THEMES[theme]}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    check_json(staging, "sample-data.json")
    check_refs(staging, "index.html")
    node_check(staging, pages=("index.html",), scripts=("script.js",))


RECIPE = Recipe(
    name="weekly-financial-idea",
    collection="financial-ideas",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("README.md", "requirements.md", "index.html", "style.css", "script.js", "sample-data.json"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("theme",),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=3600,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
