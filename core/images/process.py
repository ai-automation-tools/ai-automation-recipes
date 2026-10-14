"""Post-processing for rendered images: aspect crops, icon files, SVG rasterizing.

Pillow does the raster work. SVG rendering needs an optional package (`resvg-py`, or `cairosvg`
where the Cairo library is installed); without one, `svg_to_png` raises ImageError and the
recipe decides whether to ship SVG only.
"""

from __future__ import annotations

from pathlib import Path

from . import ImageError

ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)


def _ratio(aspect: str) -> float:
    w, h = (int(x) for x in aspect.split(":"))
    return w / h


def crop_to_aspect(src: Path, out: Path, aspect: str, width: int | None = None) -> Path:
    """Center-crop `src` to `aspect`, optionally resize to `width`, save as PNG."""
    from PIL import Image

    with Image.open(src) as im:
        im = im.convert("RGB")
        target = _ratio(aspect)
        w, h = im.size
        if w / h > target:  # too wide: trim the sides
            nw = round(h * target)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:  # too tall: trim top and bottom
            nh = round(w / target)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        if width:
            im = im.resize((width, round(width / target)), Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, format="PNG")
    return out


def make_ico(src: Path, out: Path, sizes: tuple[int, ...] = ICO_SIZES) -> Path:
    """A multi-size .ico from a square PNG (transparent background kept)."""
    from PIL import Image

    with Image.open(src) as im:
        im = im.convert("RGBA")
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, format="ICO", sizes=[(s, s) for s in sizes if s <= max(im.size)])
    return out


def svg_to_png(svg: Path, out: Path, size: int = 512) -> Path:
    """Rasterize an SVG to a square transparent PNG with whichever renderer is installed."""
    data = svg.read_bytes()
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        import resvg_py  # type: ignore[import-not-found]

        png = resvg_py.svg_to_bytes(svg_string=data.decode("utf-8"), width=size, height=size)
        out.write_bytes(bytes(png))
        return out
    except ImportError:
        pass
    try:
        import cairosvg  # type: ignore[import-not-found]

        cairosvg.svg2png(bytestring=data, write_to=str(out), output_width=size, output_height=size)
        return out
    except (ImportError, OSError) as exc:  # OSError: cairosvg installed but the Cairo library isn't
        raise ImageError("No SVG renderer: pip install resvg-py (or cairosvg with Cairo)") from exc


def use_as_cover(staging: Path, image: str) -> str:
    """after_cover helper: copy a rendered image to cover.png and return the name to publish."""
    import shutil

    shutil.copy2(staging / image, staging / "cover.png")
    return "cover.png"


def svg_renderer_available() -> bool:
    for mod in ("resvg_py", "cairosvg"):
        try:
            __import__(mod)
            return True
        except (ImportError, OSError):
            continue
    return False
