"""Any agent CLI as a text engine, described by a JSON profile instead of code.

A profile in `core/engines/clis/<name>.json` (or in `$RECIPES_CLI_DIR`, which wins) says how
to launch the CLI headless, how the prompt gets in, and where the final message, errors and
model name sit in what it prints. `CliEngine` reads that and does the rest. Adding a CLI is
adding a file; the profile format is documented in `core/engines/clis/README.md`.

At run time `get_engine` prefers the copy of a profile on the repo's `main` (cached for a day), so
a CLI that renames a flag is fixed for every install by one merged PR. A local `$RECIPES_CLI_DIR`
file still wins, and `RECIPES_CLI_REMOTE=0` turns the fetch off.

argv tokens:
    {workdir} {model} {tools} {prompt} {promptFile}   substituted in place
    "@model"   splices `modelArgs` when there is a model to pass, else nothing
    "@tools"   splices `toolArgs` when the run has tools, else nothing
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .base import CLAUDE_ALIASES, EngineError, EngineRequest, EngineResult

log = logging.getLogger(__name__)

PROFILE_DIR = Path(__file__).resolve().parent / "clis"
REMOTE_URL = "https://raw.githubusercontent.com/ai-automation-tools/ai-automation-recipes/main/core/engines/clis/"
REMOTE_TTL = 24 * 3600
MISSING = object()


def dig(obj: Any, path: str) -> Any:
    """`a.b.c` into nested dicts; MISSING when any step is absent."""
    for key in path.split("."):
        if not isinstance(obj, dict) or key not in obj:
            return MISSING
        obj = obj[key]
    return obj


def matches(obj: Any, rule: dict[str, Any]) -> bool:
    """Every `path: value` in rule equals what's at that path in obj."""
    return all(dig(obj, path) == want for path, want in rule.items())


def failed(payload: Any, rules: list[dict[str, Any]]) -> bool:
    """A JSON payload is an error if any rule hits: {path, truthy} or {path, not}."""
    for rule in rules:
        got = dig(payload, rule["path"])
        if rule.get("truthy") and got is not MISSING and got:
            return True
        if "not" in rule and got != rule["not"]:
            return True
    return False


def message_at(payload: Any, path: str | None) -> str:
    got = dig(payload, path) if path else MISSING
    if isinstance(got, dict):
        got = got.get("message", got)
    return "" if got is MISSING else str(got)


def parse_json(stdout: str) -> Any:
    """The JSON object a CLI printed, tolerating banner text before it."""
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        start = stdout.find("{")
        if start >= 0:
            try:
                return json.loads(stdout[start:])
            except json.JSONDecodeError:
                pass
    raise EngineError(f"no JSON result in the output:\n{stdout[-2000:]}")


def busiest_model(payload: Any, spec: dict[str, Any] | None, fallback: str) -> str:
    """The model that produced the most output, from a {model: stats} map in the payload."""
    models = dig(payload, spec["map"]) if spec else MISSING
    if not isinstance(models, dict) or not models:
        return fallback

    def tokens(entry: Any) -> int:
        for path in spec.get("tokens", []):
            got = dig(entry, path)
            if isinstance(got, (int, float)):
                return int(got)
        return 0

    return max(models, key=lambda m: tokens(models[m]))


def parse_jsonl(stdout: str, out: dict[str, Any]) -> tuple[str | None, dict[str, Any], list[str]]:
    """(final text, usage, notices) from an event stream. Raises EngineError on a fail event."""
    text: str | None = None
    usage: dict[str, Any] = {}
    notices: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "fail" in out and matches(evt, out["fail"]["match"]):
            raise EngineError(f"run failed: {message_at(evt, out['fail'].get('message')) or evt}")
        if matches(evt, out["text"]["match"]):
            got = dig(evt, out["text"]["path"])
            text = "" if got is MISSING else str(got)
        elif "notice" in out and matches(evt, out["notice"]["match"]):
            notices.append(message_at(evt, out["notice"].get("path"))[:300])
        elif "usage" in out and matches(evt, out["usage"]["match"]):
            got = dig(evt, out["usage"]["path"])
            usage = got if isinstance(got, dict) else {}
    return text, usage, notices


class CliEngine:
    def __init__(self, profile: dict[str, Any]) -> None:
        self.profile = profile
        self.name: str = profile["name"]
        self.skills_dir: str = profile.get("skillsDir", f".{self.name}/skills")
        env = profile.get("binaryEnv")
        self.binary = (os.environ.get(env) if env else None) or profile["binary"]

    def preflight(self) -> None:
        if shutil.which(self.binary) is None:
            how = self.profile.get("install", "install it")
            env = self.profile.get("binaryEnv")
            raise EngineError(f"`{self.binary}` is not on PATH. {how}" + (f", or set {env}." if env else "."))

    def model(self, requested: str | None) -> str | None:
        """A Claude alias means "your default" to any CLI that doesn't take Claude aliases."""
        if not requested:
            return None
        if requested in CLAUDE_ALIASES and not self.profile.get("claudeAliases"):
            return None
        return requested

    def command(self, request: EngineRequest, prompt_file: Path | None = None) -> list[str]:
        model = self.model(request.model)
        values = {
            "workdir": str(request.workdir),
            "model": model or "",
            "tools": self.profile.get("toolsJoin", ",").join(request.tools),
            "prompt": request.prompt,
            "promptFile": str(prompt_file or ""),
        }
        argv: list[str] = [shutil.which(self.binary) or self.binary]
        for token in self.profile.get("argv", []):
            if token == "@model":
                parts = self.profile.get("modelArgs", []) if model else []
            elif token == "@tools":
                parts = self.profile.get("toolArgs", []) if request.tools else []
            else:
                parts = [token]
            argv += [p.format_map(values) for p in parts]
        return argv

    def make_home(self) -> Path | None:
        """A throwaway home holding only the profile's `isolatedHome` files, so the CLI starts
        without the user's own config (MCP servers, logins, model overrides). None if unset."""
        files = self.profile.get("isolatedHome")
        if not files:
            return None
        home = Path(tempfile.mkdtemp(prefix=f"recipes-{self.name}-home-"))
        for rel, content in files.items():
            path = home / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        return home

    def run(self, request: EngineRequest) -> EngineResult:
        via = self.profile.get("prompt", "stdin")
        prompt_file = None
        if via == "file":
            prompt_file = request.workdir / self.profile.get("promptFile", ".prompt.md")
            prompt_file.write_text(request.prompt, encoding="utf-8")
        cmd = self.command(request, prompt_file)
        model = self.model(request.model)
        log.info("%s: running in %s (model=%s)", self.name, request.workdir, model or "default")
        home = self.make_home()
        try:
            proc = subprocess.run(
                cmd,
                input=request.prompt if via == "stdin" else None,
                cwd=request.workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=request.timeout_s,
                env={**os.environ, "HOME": str(home), "USERPROFILE": str(home)} if home else None,
            )
        except subprocess.TimeoutExpired as exc:
            raise EngineError(f"{self.name} timed out after {request.timeout_s}s") from exc
        finally:
            if prompt_file:
                prompt_file.unlink(missing_ok=True)
            if home:
                shutil.rmtree(home, ignore_errors=True)
        return self.parse(proc.stdout or "", proc.stderr or "", proc.returncode, model or "default")

    def parse(self, stdout: str, stderr: str, code: int, fallback_model: str) -> EngineResult:
        out = self.profile.get("output", {"format": "text"})
        fmt = out.get("format", "text")
        tail = (stderr or stdout)[-2000:]
        exit_matters = self.profile.get("exitCode", "error") != "ignore"

        if fmt == "jsonl":
            text, usage, notices = parse_jsonl(stdout, out)
            for n in notices:
                log.warning("%s: %s", self.name, n.splitlines()[0] if n else n)
            if exit_matters and code != 0:
                raise EngineError(f"{self.name} exited {code}:\n{tail}")
            if text is None:
                raise EngineError(f"{self.name} produced no final message:\n{tail}")
            meta = {k: usage.get(k) for k in out.get("usageKeys", [])}
            return EngineResult(text=text, model=fallback_model, meta=meta)

        if fmt == "json":
            if not stdout.strip():
                raise EngineError(f"{self.name} exited {code} with no output:\n{tail}")
            try:
                payload = parse_json(stdout)
            except EngineError as exc:
                raise EngineError(f"{self.name} exited {code}: {exc}") from None
            if failed(payload, out.get("errors", [])):
                msg = message_at(payload, out.get("errorMessage")) or json.dumps(payload)[:500]
                raise EngineError(f"{self.name} run failed: {msg[:2000]}")
            if exit_matters and code != 0:
                raise EngineError(f"{self.name} exited {code}:\n{tail}")
            warnings = dig(payload, out["warnings"]) if out.get("warnings") else MISSING
            for w in warnings if isinstance(warnings, list) else []:
                log.warning("%s: %s", self.name, str(w)[:300])
            text = dig(payload, out.get("text", "result"))
            meta = {k: (None if (v := dig(payload, p)) is MISSING else v) for k, p in out.get("meta", {}).items()}
            return EngineResult(text="" if text is MISSING else str(text),
                                model=busiest_model(payload, out.get("model"), fallback_model), meta=meta)

        if exit_matters and code != 0:
            raise EngineError(f"{self.name} exited {code}:\n{tail}")
        if not stdout.strip():
            raise EngineError(f"{self.name} printed nothing:\n{tail}")
        return EngineResult(text=stdout, model=fallback_model)


def profile_dirs() -> list[Path]:
    """User profiles first, so a local file can override or add to the bundled ones."""
    dirs = [Path(p).expanduser() for p in os.environ.get("RECIPES_CLI_DIR", "").split(os.pathsep) if p]
    return dirs + [PROFILE_DIR]


def load_profiles() -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for d in reversed(profile_dirs()):
        for f in sorted(d.glob("*.json")) if d.is_dir() else []:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                log.warning("skipping CLI profile %s: %s", f, exc)
                continue
            if isinstance(data, dict) and data.get("name") and data.get("binary"):
                profiles[data["name"]] = data
    return profiles


def local_override(name: str) -> bool:
    """True when a $RECIPES_CLI_DIR folder has this profile: the user's own file always wins."""
    return any((d / f"{name}.json").is_file() for d in profile_dirs()[:-1])


def cache_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "ai-automation-recipes" / "clis"


def acceptable(data: Any, name: str, bundled: dict[str, Any] | None) -> bool:
    """A fetched profile is used only if it is well formed and can't swap the executable.

    The remote copy may change flags and output parsing, which is the point; it may not point a
    bundled engine at a different binary, and it may not be older than what shipped.
    """
    if not (isinstance(data, dict) and data.get("name") == name and data.get("binary")
            and isinstance(data.get("argv"), list) and isinstance(data.get("output", {}), dict)):
        return False
    if bundled is None:
        return True
    if (data["binary"], data.get("binaryEnv")) != (bundled["binary"], bundled.get("binaryEnv")):
        return False
    return str(data.get("verified", {}).get("checked", "")) >= str(bundled.get("verified", {}).get("checked", ""))


def remote_profile(name: str, bundled: dict[str, Any] | None) -> dict[str, Any] | None:
    """The newest published profile for `name`, or None. Never raises: offline means bundled."""
    if os.environ.get("RECIPES_CLI_REMOTE", "1") == "0" or local_override(name):
        return None
    cached = cache_dir() / f"{name}.json"
    fetched = False
    if not (cached.is_file() and time.time() - cached.stat().st_mtime < REMOTE_TTL):
        url = os.environ.get("RECIPES_CLI_URL", REMOTE_URL).rstrip("/") + f"/{name}.json"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                body = resp.read(256 * 1024)
            if acceptable(json.loads(body), name, bundled):
                cached.parent.mkdir(parents=True, exist_ok=True)
                cached.write_bytes(body)
                fetched = True
        except (OSError, urllib.error.URLError, ValueError) as exc:
            log.debug("no remote profile for %s: %s", name, exc)
    try:
        data = json.loads(cached.read_text(encoding="utf-8")) if cached.is_file() else None
    except (OSError, ValueError):
        return None
    if not acceptable(data, name, bundled):
        return None
    log.info("engine %s: profile from %s (checked %s)", name, "upstream" if fetched else "cache",
             data.get("verified", {}).get("checked", "?"))
    return data
