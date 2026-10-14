#!/usr/bin/env python3
"""IAM App Prototype — one runnable identity-and-access-management tool per run, rotating pain points.

    python recipes/iam-prototype/run.py --output-dir ~/ai-output [--area certifications]

Vendor-neutral: the prototype speaks generic IGA/IAM (identities, accounts, entitlements, roles,
access requests, certifications, SoD, joiner-mover-leaver, privileged access, SSO/MFA) and the open
standards (SCIM, OIDC, SAML). It runs on synthetic data; it never reads a real directory.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import Recipe, RunContext, run  # noqa: E402
from core.artifacts import least_used  # noqa: E402
from core.web import browser_smoke, check_json, check_refs, node_check  # noqa: E402

AREAS: dict[str, str] = {
    "aggregation": "Account aggregation performance and freshness: full vs delta reads, scheduling, partial "
                   "failures, drift between what the IGA platform believes and what the source system holds.",
    "certifications": "Certification fatigue: review volume, rubber-stamping, delegation, evidence quality, "
                      "stalled decisions and the campaigns nobody finishes.",
    "lifecycle": "Joiner / mover / leaver lag: lifecycle events firing late, orphaned accounts after a "
                 "termination, access missing on day one, movers keeping what they no longer need.",
    "roles": "Role mining and role drift: stale role definitions, entitlement creep, separation-of-duties "
             "violations, roles that nobody can explain.",
    "workflow": "Workflow and approval debugging: steps failing silently, stuck cases, re-runs, approval "
                "chains with no owner, audit-trail gaps.",
    "reporting": "Reporting: long-running access reports, schema-coupled SQL, export pipelines, summaries "
                 "an executive would actually read.",
    "integration": "Connector and integration sprawl: hundreds of applications means a long tail of edge "
                   "cases, config drift, version skew, SCIM and API quirks.",
    "compliance": "Audit and compliance evidence: SOX, HIPAA, PCI DSS, ISO 27001; assembling and defending "
                  "the access trail when the auditor asks.",
    "privileged": "Privileged access: emergency and break-glass access, just-in-time elevation, standing "
                  "admin rights, vault check-outs that never check back in.",
    "end-user": "End-user experience: the access-request portal, password reset, request forms that ask "
                "the wrong questions, nobody knowing where their request is.",
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--area", choices=sorted(AREAS), help="Override the IAM pain-area rotation.")


def prepare(ctx: RunContext) -> dict[str, str]:
    area = ctx.args.area or least_used(list(AREAS), ctx.existing, "iam_area")
    return {"AREA": area, "AREA_GUIDE": AREAS[area]}


def validate(staging: Path, manifest: dict[str, object]) -> None:
    check_json(staging, "sample-data.json")
    check_refs(staging, "index.html")
    node_check(staging, pages=("index.html",), scripts=("script.js",))
    browser_smoke(staging, "index.html")  # loads it in a real browser; fails on uncaught errors


RECIPE = Recipe(
    name="iam-prototype",
    collection="iam-prototypes",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=("README.md", "requirements.md", "index.html", "style.css", "script.js", "sample-data.json"),
    skills=("llm-writing", "humanizer", "image-prompt-craft"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
    fields=("iam_area",),
    cover_aspect="16:9",
    default_model="opus",
    timeout_s=3600,
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
