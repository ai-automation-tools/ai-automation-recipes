"""Text engines, by name. Each one is a CLI described by a JSON profile in `clis/`.

Add a backend by dropping a profile into `core/engines/clis/` (or a folder on
$RECIPES_CLI_DIR); no code change. See `clis/README.md` for the format.
"""

from __future__ import annotations

from .base import CLAUDE_ALIASES, EngineError, EngineRequest, EngineResult, TextEngine, model_for
from .cli import CliEngine, load_profiles


def engine_names() -> list[str]:
    return sorted(load_profiles())


def get_engine(name: str) -> CliEngine:
    profiles = load_profiles()
    if name not in profiles:
        raise EngineError(f"Unknown engine {name!r}. Available: {', '.join(sorted(profiles))}")
    return CliEngine(profiles[name])


__all__ = ["CLAUDE_ALIASES", "CliEngine", "EngineError", "EngineRequest", "EngineResult", "TextEngine",
           "engine_names", "get_engine", "load_profiles", "model_for"]
