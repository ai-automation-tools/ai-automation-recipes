"""The text-engine contract every agent backend implements.

A recipe never talks to a CLI or an SDK directly. It hands an engine a prompt,
a working directory the agent may write into, and the tools it may use; the
engine runs the agent to completion and returns its final message. Swapping
Claude for another agent means adding one module here, not touching a recipe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


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

    def preflight(self) -> None:
        """Raise EngineError if the engine cannot run on this machine."""

    def run(self, request: EngineRequest) -> EngineResult:
        """Run the agent headless in request.workdir and return its final message."""
