"""Render a cover image from a text prompt.

The agent writes the picture description; this module renders it after the
agent exits, so the image step is the same whichever text engine wrote the
prompt and API keys never enter the agent's environment.

Engines are tried in ladder order and only when their key is set. Every engine
returns raw image bytes; Pillow re-encodes them to a real PNG so a JPEG never
ends up behind a `.png` name.
"""

from __future__ import annotations

import io
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .constraints import NO_TEXT, with_constraints

log = logging.getLogger(__name__)

ASPECTS = ("1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9")


class ImageError(RuntimeError):
    """No engine produced a usable image."""


@dataclass(frozen=True)
class ImageResult:
    path: Path
    engine: str
    model: str


def _gemini(prompt: str, aspect: str) -> tuple[bytes, str]:
    from google import genai
    from google.genai import types

    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")
    # Keep a reference: a temporary Client is collected mid-call, closing its HTTP session.
    client = genai.Client()
    resp = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect),
        ),
    )
    for candidate in resp.candidates or []:
        for part in (candidate.content.parts if candidate.content else None) or []:
            if part.inline_data is not None and part.inline_data.data:
                return part.inline_data.data, model
    raise ImageError("Gemini returned no image part (often a content refusal).")


def _openai(prompt: str, aspect: str) -> tuple[bytes, str]:
    import base64

    from openai import OpenAI

    model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
    w, h = (int(x) for x in aspect.split(":"))
    size = "1024x1024" if w == h else ("1536x1024" if w > h else "1024x1536")
    resp = OpenAI().images.generate(model=model, prompt=prompt, size=size, n=1)
    data = resp.data[0].b64_json if resp.data else None
    if not data:
        raise ImageError("OpenAI returned no image data.")
    return base64.b64decode(data), model


# Ladder order, each with the env var that must be set for it to be tried.
ENGINES: dict[str, tuple[str, Callable[[str, str], tuple[bytes, str]]]] = {
    "gemini": ("GEMINI_API_KEY", _gemini),
    "openai": ("OPENAI_API_KEY", _openai),
}


def available_engines() -> list[str]:
    return [name for name, (env, _) in ENGINES.items() if os.environ.get(env)]


def render(prompt: str, out: Path, aspect: str, engine: str = "auto") -> ImageResult:
    """Render `prompt` to `out` as PNG. engine: auto | gemini | openai."""
    if aspect not in ASPECTS:
        raise ImageError(f"Unsupported aspect {aspect!r}; use one of {ASPECTS}.")
    ladder = available_engines() if engine == "auto" else [engine]
    if not ladder:
        raise ImageError("No image engine configured: set GEMINI_API_KEY or OPENAI_API_KEY.")

    from PIL import Image

    prompt = with_constraints(prompt)
    errors: list[str] = []
    for name in ladder:
        if name not in ENGINES:
            raise ImageError(f"Unknown image engine {name!r}.")
        env, fn = ENGINES[name]
        if not os.environ.get(env):
            errors.append(f"{name}: {env} not set")
            continue
        try:
            raw, model = fn(prompt, aspect)
            img = Image.open(io.BytesIO(raw))
            out.parent.mkdir(parents=True, exist_ok=True)
            img.save(out, format="PNG")
            if out.stat().st_size == 0:
                raise ImageError("encoded PNG is empty")
            log.info("IMAGE_OK %s (%s / %s)", out, name, model)
            return ImageResult(path=out, engine=name, model=model)
        except Exception as exc:  # noqa: BLE001 - fall through the ladder on any engine failure
            log.warning("image engine %s failed: %s", name, exc)
            errors.append(f"{name}: {exc}")
    raise ImageError("All image engines failed — " + "; ".join(errors))


__all__ = ["ASPECTS", "NO_TEXT", "ImageError", "ImageResult", "available_engines", "render", "with_constraints"]
