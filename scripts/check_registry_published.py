#!/usr/bin/env python3
"""Check that the published Cronsole catalog matches registry/ on this checkout.

Fetches index.json from the hosted copy (build_registry.HOSTED), compares every template and pack
id and sha256 with the committed registry/index.json, then downloads each file and hashes what is
actually served. Exits 1 on any difference. A merged catalog that never deployed, or a host serving
altered bytes, looks fine from inside the repo; this is the check that can see it.

    python scripts/check_registry_published.py [base-url]
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_registry import HOSTED, OUT  # noqa: E402


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-automation-recipes-registry-check"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def entries(index: dict) -> dict[str, str]:
    return {e["path"]: e["sha256"] for e in index.get("templates", []) + index.get("packs", [])}


def main() -> int:
    base = (sys.argv[1] if len(sys.argv) > 1 else HOSTED).rstrip("/") + "/"
    local = entries(json.loads((OUT / "index.json").read_text(encoding="utf-8")))
    live = entries(json.loads(fetch(base + "index.json")))

    problems = [f"missing from the host: {p}" for p in sorted(local.keys() - live.keys())]
    problems += [f"on the host but not in registry/: {p}" for p in sorted(live.keys() - local.keys())]
    problems += [f"different sha256 in the hosted index: {p}" for p in sorted(local.keys() & live.keys())
                 if local[p] != live[p]]
    for path, digest in sorted(live.items()):
        if hashlib.sha256(fetch(base + path)).hexdigest() != digest:
            problems.append(f"served bytes don't match the hosted index: {path}")

    for p in problems:
        print(f"DRIFT {p}")
    print(f"{base}: {len(live)} files checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
