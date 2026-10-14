"""Output layout and the artifact.json manifest.

Every recipe publishes into the same shape, so one viewer can render all of them:

    <output-dir>/<collection>/<YYYY-MM>/<YYYY-MM-DD>_<slug>/
        artifact.json      # the manifest (schema below)
        <recipe files>     # card.md, index.html, story.md, …
        cover.png          # when the recipe has a cover

    <output-dir>/runs.jsonl  # one line per successful run, newest last

artifact.json is the contract with anything that displays the output. Change
it by adding fields; bump SCHEMA only for a breaking change.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

SCHEMA = "ai-automation-recipes/artifact@1"
MANIFEST = "artifact.json"


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:max_len].rstrip("-") or "untitled"


def artifact_dir(collection_dir: Path, day: date, slug: str) -> Path:
    """The final folder for a run, suffixed -2, -3… if the slug is taken that day."""
    base = collection_dir / day.strftime("%Y-%m")
    candidate = base / f"{day.isoformat()}_{slug}"
    n = 2
    while candidate.exists():
        candidate = base / f"{day.isoformat()}_{slug}-{n}"
        n += 1
    return candidate


@dataclass(frozen=True)
class Existing:
    title: str
    slug: str
    date: str
    summary: str
    fields: dict[str, object]


def load_existing(collection_dir: Path) -> list[Existing]:
    """Every published artifact in a collection, oldest first."""
    out: list[Existing] = []
    for path in sorted(collection_dir.glob(f"*/*/{MANIFEST}")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        out.append(
            Existing(
                title=str(data.get("title", "")),
                slug=str(data.get("slug", "")),
                date=str(data.get("date", "")),
                summary=str(data.get("summary", "")),
                fields=dict(data.get("fields") or {}),
            )
        )
    out.sort(key=lambda e: e.date)
    return out


def least_used(options: list[str], existing: list[Existing], field: str) -> str:
    """The option with the fewest artifacts; ties go to the one used least recently."""
    counts = Counter(str(e.fields.get(field)) for e in existing)
    last_used = {str(e.fields.get(field)): e.date for e in existing}
    return min(options, key=lambda o: (counts.get(o, 0), last_used.get(o, ""), options.index(o)))


def existing_digest(existing: list[Existing], limit: int = 150) -> str:
    """A compact list of what already exists, for the agent's do-not-repeat check."""
    if not existing:
        return "(none yet — this is the first run)"
    rows = existing[-limit:]
    return "\n".join(f"- {e.date} · {e.slug} · {e.title} — {e.summary}" for e in rows)


def write_manifest(folder: Path, data: dict[str, object]) -> None:
    data = {"schema": SCHEMA, **data, "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    (folder / MANIFEST).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_run_log(output_dir: Path, entry: dict[str, object]) -> None:
    with (output_dir / "runs.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
