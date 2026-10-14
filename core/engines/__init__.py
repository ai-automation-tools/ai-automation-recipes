"""Text engines, by name. Add a backend by registering it in ENGINES."""

from __future__ import annotations

from .base import CLAUDE_ALIASES, EngineError, EngineRequest, EngineResult, TextEngine, model_for
from .claude import ClaudeEngine
from .codex import CodexEngine
from .gemini import GeminiEngine

ENGINES: dict[str, type] = {
    "claude": ClaudeEngine,
    "codex": CodexEngine,
    "gemini": GeminiEngine,
}


def get_engine(name: str) -> TextEngine:
    try:
        return ENGINES[name]()
    except KeyError:
        raise EngineError(f"Unknown engine {name!r}. Available: {', '.join(sorted(ENGINES))}") from None


__all__ = ["CLAUDE_ALIASES", "ENGINES", "EngineError", "EngineRequest", "EngineResult", "TextEngine",
           "get_engine", "model_for"]
