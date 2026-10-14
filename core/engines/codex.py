"""OpenAI Codex CLI (`codex exec`) as a text engine.

Runs the agent with the run's staging folder as its working root under the
`workspace-write` sandbox, so the folder is the only place it can write. Codex
has no per-tool allowlist: the sandbox is the boundary, and the recipe's tool
list is advisory (it is written into the prompt's contract, not enforced).

Skills: Codex reads project skills from `.agents/skills/`, so the runner stages
the recipe's skills there. Auth is whatever the local `codex` CLI already uses
(a ChatGPT login or OPENAI_API_KEY).

Output: `--json` streams JSONL events. The agent's final message is the last
`item.completed` whose item is an `agent_message`; `turn.completed` carries
token usage; `turn.failed` or a non-zero exit is an error.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess

from .base import EngineError, EngineRequest, EngineResult, model_for

log = logging.getLogger(__name__)


def parse_events(stdout: str) -> tuple[str | None, dict[str, object], list[str]]:
    """(last agent message, usage, non-fatal notices) from Codex's JSONL stream.

    Raises EngineError on a `turn.failed` event.
    """
    text: str | None = None
    usage: dict[str, object] = {}
    notices: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = evt.get("type")
        if kind == "item.completed":
            item = evt.get("item") or {}
            if item.get("type") == "agent_message":
                text = str(item.get("text", ""))
            elif item.get("type") == "error":
                # Codex reports ignored config keys and similar as error items but keeps going.
                notices.append(str(item.get("message", ""))[:300])
        elif kind == "turn.completed":
            usage = evt.get("usage") or {}
        elif kind == "turn.failed":
            err = evt.get("error") or {}
            raise EngineError(f"codex turn failed: {err.get('message') or err}")
    return text, usage, notices


class CodexEngine:
    name = "codex"
    skills_dir = ".agents/skills"

    def __init__(self) -> None:
        self.binary = os.environ.get("CODEX_BIN", "codex")

    def preflight(self) -> None:
        if shutil.which(self.binary) is None:
            raise EngineError(
                f"`{self.binary}` is not on PATH. Install the Codex CLI (`npm i -g @openai/codex`) "
                "and sign in, or set CODEX_BIN."
            )

    def command(self, request: EngineRequest) -> list[str]:
        cmd = [
            shutil.which(self.binary) or self.binary,
            "exec",
            "--json",
            "--ephemeral",            # no session files written for a scheduled run
            "--skip-git-repo-check",  # the staging folder is not a git repo
            "-s", "workspace-write",
            "-C", str(request.workdir),
        ]
        model = model_for(self.name, request.model)
        if model:
            cmd += ["-m", model]
        cmd.append("-")  # prompt on stdin
        return cmd

    def run(self, request: EngineRequest) -> EngineResult:
        cmd = self.command(request)
        log.info("codex: running in %s (model=%s)", request.workdir, model_for(self.name, request.model) or "default")
        try:
            proc = subprocess.run(
                cmd,
                input=request.prompt,
                cwd=request.workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=request.timeout_s,
            )
        except subprocess.TimeoutExpired as exc:
            raise EngineError(f"codex timed out after {request.timeout_s}s") from exc

        text, usage, notices = parse_events(proc.stdout)
        for n in notices:
            log.warning("codex: %s", n.splitlines()[0] if n else n)
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout)[-2000:]
            raise EngineError(f"codex exited {proc.returncode}:\n{tail}")
        if text is None:
            tail = (proc.stderr or proc.stdout)[-2000:]
            raise EngineError(f"codex produced no agent message:\n{tail}")

        return EngineResult(
            text=text,
            model=model_for(self.name, request.model) or "default",
            meta={
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "cached_input_tokens": usage.get("cached_input_tokens"),
            },
        )
