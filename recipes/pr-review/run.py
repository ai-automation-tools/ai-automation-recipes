#!/usr/bin/env python3
"""PR Review — review the open pull requests of one GitHub repo, and optionally act on them.

    python recipes/pr-review/run.py --output-dir ~/ai-output --repo owner/name [--base main] [--mode report]

Modes: `report` (default) only writes the review; `comment` also posts one review comment per PR;
`merge` also squash-merges every PR that passes every gate and leaves a hold comment on the rest.
The runner lists the PRs with `gh` before the agent starts and rejects a review that skips one,
or that ran a mutating `gh` command in report mode.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from core import NothingToDo, Recipe, RecipeError, RunContext, run  # noqa: E402

MAIN = "review.md"
MODES = ("report", "comment", "merge")
PR_FIELDS = "number,title,author,headRefName,isDraft,mergeable,url"
SECTION_RE = re.compile(r"^## PR #(\d+)\b", re.M)
VERDICT_RE = re.compile(r"\*\*Verdict:\*\*\s*(PASS|HOLD)\b")
# A `gh` call that changes something on GitHub. `gh api` is only mutating with a non-GET method.
MUTATING_RE = re.compile(
    r"\bgh\s+pr\s+(comment|review|merge|close|edit|ready|reopen|checkout|lock|unlock)\b"
    r"|\bgh\s+api\b.*(?:-X|--method)\s*(?:POST|PUT|PATCH|DELETE)\b"
    r"|\bgh\s+(issue|release|repo)\s+(create|delete|edit|close|comment)\b", re.I)

MODE_RULES = {
    "report": (
        "**Mode: `report`.** Read-only. Write the review and nothing else: no comments, no reviews, "
        "no merges. The only `gh` commands you may run are `gh pr list`, `gh pr view`, `gh pr diff`, "
        "`gh pr checks` and read-only `gh api` GETs."
    ),
    "comment": (
        "**Mode: `comment`.** After deciding each verdict, post exactly one comment per PR with "
        "`gh pr comment <n> --repo {repo} --body-file <file>` (write the body to a temp file in this "
        "folder first, then delete it). A PASS comment says what you checked; a HOLD comment names "
        "the exact files, check or conflict and what to do about it. Never merge."
    ),
    "merge": (
        "**Mode: `merge`.** For every PASS: `gh pr merge <n> --repo {repo} --squash` and confirm it "
        "merged with `gh pr view <n> --repo {repo} --json state,mergedAt`; if the merge call fails, "
        "the PR becomes a HOLD with the error as the reason. For every HOLD: post one comment with "
        "`gh pr comment` naming exactly why and what to check. Squash only: never a merge commit, "
        "never a rebase, never a force-push, never close a PR, never delete a branch."
    ),
}


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--repo", required=True, help="GitHub repository as owner/name.")
    p.add_argument("--base", help="Only PRs into this branch (default: every open PR).")
    p.add_argument("--mode", choices=MODES, default="report", help="report (default), comment or merge.")


def gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def list_prs(repo: str, base: str | None) -> list[dict]:
    auth = gh("auth", "status")
    if auth.returncode != 0:
        raise RecipeError(f"gh is not logged in: {(auth.stderr or auth.stdout).strip()[-300:]}")
    cmd = ["pr", "list", "--repo", repo, "--state", "open", "--limit", "50", "--json", PR_FIELDS]
    if base:
        cmd += ["--base", base]
    proc = gh(*cmd)
    if proc.returncode != 0:
        raise RecipeError(f"gh pr list failed for {repo}: {proc.stderr.strip()[-300:]}")
    try:
        prs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RecipeError(f"gh pr list returned no JSON: {exc}") from exc
    return [pr for pr in prs if isinstance(pr, dict) and "number" in pr]


def prs_block(prs: list[dict]) -> str:
    rows = []
    for pr in prs:
        author = pr.get("author") or {}
        login = author.get("login") if isinstance(author, dict) else str(author)
        flags = " · DRAFT" if pr.get("isDraft") else ""
        rows.append(f"- #{pr['number']} — {pr.get('title', '').strip()} — @{login or '?'} · "
                    f"`{pr.get('headRefName', '?')}` · mergeable: {pr.get('mergeable', 'UNKNOWN')}{flags}")
    return "\n".join(rows)


def prepare(ctx: RunContext) -> dict[str, str]:
    prs = list_prs(ctx.args.repo, ctx.args.base)
    if not prs:
        raise NothingToDo(f"no open pull requests in {ctx.args.repo}")
    ctx.state["numbers"] = [int(pr["number"]) for pr in prs]
    return {
        "REPO": ctx.args.repo,
        "BASE_RULE": (f"Only PRs into `{ctx.args.base}` are in scope." if ctx.args.base
                      else "Every open PR is in scope, whatever its base branch."),
        "MODE": ctx.args.mode,
        "MODE_RULES": MODE_RULES[ctx.args.mode].format(repo=ctx.args.repo),
        "PRS": prs_block(prs),
    }


def validate(staging: Path, manifest: dict[str, object], ctx: RunContext) -> None:
    text = (staging / MAIN).read_text(encoding="utf-8")
    wanted = [int(n) for n in ctx.state.get("numbers", [])]
    starts = [(m.start(), int(m.group(1))) for m in SECTION_RE.finditer(text)]
    found: dict[int, str] = {}
    for i, (pos, number) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        found[number] = text[pos:end]
    missing = [n for n in wanted if n not in found]
    if missing:
        raise RecipeError(f"{MAIN} has no `## PR #n` section for: {missing}")
    for number, body in found.items():
        if not VERDICT_RE.search(body):
            raise RecipeError(f"PR #{number} has no `**Verdict:** PASS` or `**Verdict:** HOLD` line")
    commands = re.search(r"^## Commands\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not commands:
        raise RecipeError(f"{MAIN} needs a `## Commands` section listing every gh command run")
    mode = ctx.args.mode
    mutating = [line.strip() for line in commands.group(1).splitlines() if MUTATING_RE.search(line)]
    if mode == "report" and mutating:
        raise RecipeError(f"report mode ran a mutating gh command: {mutating[0]}")
    if mode == "comment" and any(re.search(r"\bgh\s+pr\s+merge\b", m) for m in mutating):
        raise RecipeError("comment mode must never merge")
    if manifest.get("pr_count") != len(wanted):
        raise RecipeError(f"final JSON pr_count must be {len(wanted)}")
    merged = manifest.get("merged_count")
    if not isinstance(merged, int) or merged < 0:
        raise RecipeError("final JSON merged_count must be a non-negative integer")
    if mode != "merge" and merged:
        raise RecipeError(f"{mode} mode cannot have merged anything")


RECIPE = Recipe(
    name="pr-review",
    collection="pr-reviews",
    version="0.1.0",
    prompt_path=HERE / "prompt.md",
    files=(MAIN,),
    skills=("llm-writing", "humanizer"),
    tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "Bash"),
    fields=("pr_count", "merged_count"),
    cover_aspect=None,
    default_model="sonnet",
    add_args=add_args,
    prepare=prepare,
    validate=validate,
)

if __name__ == "__main__":
    sys.exit(run(RECIPE))
