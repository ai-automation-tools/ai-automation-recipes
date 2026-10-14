"""Claude Code (`claude --print`) as a text engine.

Runs the agent with its working directory set to the run's staging folder, so
the only place it can write is the folder the runner will publish from. Tools
are an explicit allowlist under `--permission-mode dontAsk`: anything not
listed is denied rather than prompted, which is what a scheduled run needs.

Auth is whatever the local `claude` CLI already uses — a Claude subscription
login or ANTHROPIC_API_KEY. `--bare` is deliberately not used: it ignores
subscription logins.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess

from .base import EngineError, EngineRequest, EngineResult

log = logging.getLogger(__name__)


class ClaudeEngine:
    name = "claude"
    skills_dir = ".claude/skills"

    def __init__(self) -> None:
        self.binary = os.environ.get("CLAUDE_BIN", "claude")

    def preflight(self) -> None:
        if shutil.which(self.binary) is None:
            raise EngineError(
                f"`{self.binary}` is not on PATH. Install Claude Code "
                "(https://docs.claude.com/claude-code) and sign in, or set CLAUDE_BIN."
            )

    def run(self, request: EngineRequest) -> EngineResult:
        cmd = [
            shutil.which(self.binary) or self.binary,
            "--print",
            "--output-format", "json",
            "--permission-mode", "dontAsk",
            "--allowedTools", ",".join(request.tools),
        ]
        if request.model:
            cmd += ["--model", request.model]

        log.info("claude: running in %s (model=%s)", request.workdir, request.model or "default")
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
            raise EngineError(f"claude timed out after {request.timeout_s}s") from exc

        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            tail = (proc.stderr or proc.stdout)[-2000:]
            raise EngineError(f"claude exited {proc.returncode} without a JSON result:\n{tail}") from exc

        if payload.get("is_error") or payload.get("subtype") != "success":
            raise EngineError(
                f"claude run ended as {payload.get('subtype')!r}: {str(payload.get('result'))[:2000]}"
            )

        model = request.model or "default"
        usage = payload.get("modelUsage")
        if isinstance(usage, dict) and usage:
            # The model that did the most output work, by its full id.
            model = max(usage, key=lambda m: usage[m].get("outputTokens", 0))

        return EngineResult(
            text=str(payload.get("result", "")),
            model=model,
            meta={
                "num_turns": payload.get("num_turns"),
                "duration_ms": payload.get("duration_ms"),
                "session_id": payload.get("session_id"),
            },
        )
