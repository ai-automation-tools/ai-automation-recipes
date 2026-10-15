"""The text-engine contract every agent backend implements.

A recipe never talks to a CLI or an SDK directly. It hands an engine a prompt,
a working directory the agent may write into, and the tools it may use; the
engine runs the agent to completion and returns its final message. Swapping
Claude for another agent means adding one JSON profile to `clis/`, not touching a recipe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

# Claude Code's model aliases. A recipe's `default_model` is one of these, so an engine that
# isn't Claude treats them as "use your own default" rather than passing them through.
CLAUDE_ALIASES = frozenset({"sonnet", "opus", "haiku"})


def model_for(engine_name: str, model: str | None) -> str | None:
    """The model id to hand a non-Claude CLI: a Claude alias means that CLI's default."""
    if not model or (engine_name != "claude" and model in CLAUDE_ALIASES):
        return None
    return model


class EngineError(RuntimeError):
    """The agent could not be run, or it ended in an error state."""


@dataclass(frozen=True)
class EngineRequest:
    prompt: str
    workdir: Path
    tools: tuple[str, ...]
    model: str | None = None
    timeout_s: int = 1800


@dataclass(frozen=True)
class EngineResult:
    text: str
    model: str
    meta: dict[str, object] = field(default_factory=dict)


class TextEngine(Protocol):
    name: str
    # Where this agent looks for project skills, relative to its working directory. The runner
    # copies the recipe's skills there and tells the prompt where they are.
    skills_dir: str

    def preflight(self) -> None:
        """Raise EngineError if the engine cannot run on this machine."""

    def run(self, request: EngineRequest) -> EngineResult:
        """Run the agent headless in request.workdir and return its final message."""
