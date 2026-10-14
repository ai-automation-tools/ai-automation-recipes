"""Gemini CLI (`gemini -p`) as a text engine.

Runs the agent headless in the run's staging folder with every tool call
auto-approved (`--approval-mode yolo`), which is what a scheduled run needs:
nobody is there to answer a prompt. The staging folder is the working
directory, and the prompt's contract tells the agent to write nowhere else.
Gemini has no per-tool allowlist, so the recipe's tool list is advisory.

Skills: Gemini reads project skills from `.gemini/skills/`, so the runner
stages the recipe's skills there. Auth is whatever the local `gemini` CLI is
set up for: GEMINI_API_KEY (the same key the image step uses) or a Google
login.

Output: `-o json` prints one object, `{"session_id", "response", "stats",
"error", "warnings"}`. `error` present means the run failed.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess

from .base import EngineError, EngineRequest, EngineResult, model_for

log = logging.getLogger(__name__)


def parse_output(stdout: str) -> dict[str, object]:
    """The JSON object Gemini printed, tolerating any banner text before it."""
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        start = stdout.find("{")
        if start < 0:
            raise EngineError(f"gemini printed no JSON:\n{stdout[-2000:]}") from None
        try:
            return json.loads(stdout[start:])
        except json.JSONDecodeError as exc:
            raise EngineError(f"gemini printed unparseable JSON:\n{stdout[-2000:]}") from exc


def busiest_model(stats: object, fallback: str) -> str:
    """The model that produced the most output tokens, from Gemini's stats block."""
    models = stats.get("models") if isinstance(stats, dict) else None
    if not isinstance(models, dict) or not models:
        return fallback

    def out_tokens(entry: object) -> int:
        tokens = entry.get("tokens") if isinstance(entry, dict) else None
        if isinstance(tokens, dict):
            return int(tokens.get("candidates") or tokens.get("output") or 0)
        return 0

    return max(models, key=lambda m: out_tokens(models[m]))


class GeminiEngine:
    name = "gemini"
    skills_dir = ".gemini/skills"

    def __init__(self) -> None:
        self.binary = os.environ.get("GEMINI_BIN", "gemini")

    def preflight(self) -> None:
        if shutil.which(self.binary) is None:
            raise EngineError(
                f"`{self.binary}` is not on PATH. Install the Gemini CLI (`npm i -g @google/gemini-cli`) "
                "and set GEMINI_API_KEY or sign in, or set GEMINI_BIN."
            )

    def command(self, request: EngineRequest) -> list[str]:
        cmd = [
            shutil.which(self.binary) or self.binary,
            "-p", "",  # the prompt arrives on stdin and is appended to this
            "-o", "json",
            "--approval-mode", "yolo",
            "--skip-trust",  # a fresh staging folder is never in the trusted-folders list
        ]
        model = model_for(self.name, request.model)
        if model:
            cmd += ["-m", model]
        return cmd

    def run(self, request: EngineRequest) -> EngineResult:
        cmd = self.command(request)
        log.info("gemini: running in %s (model=%s)", request.workdir, model_for(self.name, request.model) or "default")
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
            raise EngineError(f"gemini timed out after {request.timeout_s}s") from exc

        if not proc.stdout.strip():
            raise EngineError(f"gemini exited {proc.returncode} with no output:\n{(proc.stderr or '')[-2000:]}")
        payload = parse_output(proc.stdout)
        if payload.get("error"):
            err = payload["error"]
            msg = err.get("message") if isinstance(err, dict) else err
            raise EngineError(f"gemini run failed: {str(msg)[:2000]}")
        if proc.returncode != 0:
            raise EngineError(f"gemini exited {proc.returncode}:\n{(proc.stderr or proc.stdout)[-2000:]}")
        for w in payload.get("warnings") or []:
            log.warning("gemini: %s", str(w)[:300])

        fallback = model_for(self.name, request.model) or "default"
        return EngineResult(
            text=str(payload.get("response", "")),
            model=busiest_model(payload.get("stats"), fallback),
            meta={"session_id": payload.get("session_id")},
        )
