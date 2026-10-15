#!/usr/bin/env python3
"""Draft a CLI profile for an agent CLI the repo doesn't know yet, then test it.

Reads the CLI's own --help (plus the help of a headless subcommand if it has one), asks an
engine you already have working to write the profile, checks every flag against that help,
and sends it a one-line ping. The draft is written for you to review; nothing schedules it.

    python scripts/new_cli.py aider                      # drafted by Claude, written to core/engines/clis/
    python scripts/new_cli.py aider --with codex         # drafted by another engine
    python scripts/new_cli.py aider --out ~/my-clis      # a folder on $RECIPES_CLI_DIR

Exits 1 if the draft passes a flag its --help doesn't list, or the ping doesn't come back.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from check_clis import check, run  # noqa: E402
from core.engines import CliEngine, EngineError, EngineRequest, get_engine  # noqa: E402
from core.engines.cli import PROFILE_DIR, parse_json  # noqa: E402

log = logging.getLogger("new_cli")
# Subcommands that usually mean "run one prompt and exit". Their help is where the headless flags live.
HEADLESS = ("exec", "run", "prompt", "ask", "chat")
EXAMPLES = ("claude", "codex", "opencode")

PROMPT = """You are writing a JSON profile that lets a Python runner drive the agent CLI `{binary}`
headless: one prompt in, the agent works in a folder unattended, its final message out.

The profile format, from the repo's documentation:

{format}

Three working profiles, for shape:

{examples}

The CLI's own help text (this is the only source of truth for flags; never invent one):

{help}

Rules:
- Pick the flags for a single non-interactive run that never stops to ask for approval. Prefer
  the narrowest option that does that (a sandbox or a tool allowlist) over a flag that bypasses
  every check, and say which you chose and why in `_toolPolicy`.
- Prefer a machine-readable output mode (`json` or `jsonl`) if the help lists one, and describe
  where the final message sits. If you can't tell the event shape from the help, use `text`.
- `toolPolicy` is `allowlist` only if `toolArgs` really limits tools by name.
- `name` is "{name}", `binary` is "{binary}". `check.help` lists the help pages you used.
- `verified` is {{"version": "{version}", "checked": "{today}", "liveRun": false}}.

Reply with the JSON object only, no prose, no code fence."""


def help_pages(binary: str) -> tuple[str, list[list[str]]]:
    """Top-level --help, plus the --help of any headless-looking subcommand it lists."""
    top = run(binary, ["--help"])
    pages, text = [["--help"]], [f"$ {binary} --help\n{top}"]
    for sub in HEADLESS:
        if re.search(rf"^\s+{sub}\b", top, re.M):
            pages.append([sub, "--help"])
            text.append(f"$ {binary} {sub} --help\n{run(binary, [sub, '--help'])}")
    return "\n\n".join(text)[:60000], pages


def format_doc() -> str:
    doc = (PROFILE_DIR / "README.md").read_text(encoding="utf-8")
    start, end = doc.find("## Format"), doc.find("Keys starting with `_`")
    return doc[start:end].strip() if start >= 0 else doc


def draft(binary: str, name: str, drafter: str) -> dict:
    help_text, pages = help_pages(binary)
    version = next((l.strip() for l in run(binary, ["--version"]).splitlines() if re.search(r"\d+\.\d+", l)), "")
    examples = "\n\n".join((PROFILE_DIR / f"{n}.json").read_text(encoding="utf-8") for n in EXAMPLES)
    prompt = PROMPT.format(binary=binary, name=name, format=format_doc(), examples=examples,
                           help=help_text, version=version, today=date.today().isoformat())
    engine = get_engine(drafter)
    engine.preflight()
    with tempfile.TemporaryDirectory() as tmp:
        result = engine.run(EngineRequest(prompt=prompt, workdir=Path(tmp), tools=(), timeout_s=600))
    text = re.sub(r"^```(?:json)?\s*|\s*```\s*$", "", result.text.strip())
    profile = parse_json(text)
    if not isinstance(profile, dict):
        raise EngineError("the drafter didn't return a JSON object")
    profile.update(name=name, binary=binary)
    profile.setdefault("check", {"version": ["--version"], "help": pages})
    profile.setdefault("verified", {"version": version, "checked": date.today().isoformat(), "liveRun": False})
    return profile


def ping(profile: dict) -> str:
    """The CLI's reply to a trivial prompt through the drafted profile, or the error."""
    with tempfile.TemporaryDirectory() as tmp:
        try:
            result = CliEngine(profile).run(EngineRequest(prompt="Reply with exactly the word PONG and nothing else.",
                                                          workdir=Path(tmp), tools=(), timeout_s=300))
        except EngineError as exc:
            return f"error: {exc}"
    return result.text.strip()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("binary", help="the CLI's executable, as you'd type it")
    ap.add_argument("--name", help="engine name (default: the binary's name)")
    ap.add_argument("--with", dest="drafter", default="claude", help="engine that writes the draft (default: claude)")
    ap.add_argument("--out", type=Path, default=PROFILE_DIR, help=f"folder to write <name>.json into (default: {PROFILE_DIR})")
    ap.add_argument("--force", action="store_true", help="overwrite an existing profile")
    args = ap.parse_args()

    if shutil.which(args.binary) is None:
        log.error("`%s` is not on PATH", args.binary)
        return 2
    name = args.name or Path(args.binary).stem.lower()
    target = args.out.expanduser() / f"{name}.json"
    if target.exists() and not args.force:
        log.error("%s exists; pass --force to replace it", target)
        return 2

    log.info("drafting %s with %s ...", name, args.drafter)
    try:
        profile = draft(args.binary, name, args.drafter)
    except EngineError as exc:
        log.error("draft failed: %s", exc)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")

    report = check(profile)
    reply = ping(profile)
    ok = not report.get("missing") and "PONG" in reply.upper()
    profile["verified"]["smoke"] = f"PONG prompt {'answered' if ok else 'failed'} {date.today().isoformat()}"
    target.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")

    log.info("wrote %s", target)
    log.info("  runs as:   %s %s", args.binary, " ".join(profile.get("argv", [])))
    log.info("  tools:     %s - %s", profile.get("toolPolicy", "?"), profile.get("_toolPolicy", ""))
    log.info("  flags:     %s", "all in --help" if not report.get("missing") else "NOT IN --help: " + " ".join(report["missing"]))
    log.info("  ping:      %s", reply[:200] or "(empty)")
    log.info("Review the flags above before you schedule anything on it: they decide what the agent may do unattended.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
