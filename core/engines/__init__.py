"""Text engines, by name. Add a backend by registering it in ENGINES."""

from __future__ import annotations

from .base import EngineError, EngineRequest, EngineResult, TextEngine
from .claude import ClaudeEngine

ENGINES: dict[str, type] = {
    "claude": ClaudeEngine,
}


def get_engine(name: str) -> TextEngine:
    try:
        return ENGINES[name]()
    except KeyError:
        raise EngineError(f"Unknown engine {name!r}. Available: {', '.join(sorted(ENGINES))}") from None


__all__ = ["ENGINES", "EngineError", "EngineRequest", "EngineResult", "TextEngine", "get_engine"]
