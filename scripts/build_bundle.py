#!/usr/bin/env python3
"""Build the runtime bundle the Cronsole editions download.

The bundle is a plain, reproducible .tar of what a recipe needs to run (core/, recipes/, the
bundled skills, requirements.txt, LICENSE, VERSION), with fixed metadata and sorted entries,
so the same tree always gives the same bytes and the same sha256 on any OS. Text files are
normalized to LF, since a Windows checkout can carry CRLF. No compression: zlib output isn't
guaranteed identical across builds, and the sha256 is pinned in every Cronsole template.

    python scripts/build_bundle.py               # print the version and sha256
    python scripts/build_bundle.py --out dist/   # also write the .tar and a .sha256 file

The release workflow builds it again from the tagged commit and refuses to publish if the
sha256 differs from the one the templates pin.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ("core/", "recipes/", ".claude/skills/")
TOP_FILES = ("requirements.txt", "LICENSE", "VERSION")
REPO_URL = "https://github.com/ai-automation-tools/ai-automation-recipes"
NUL, CRLF, LF = b"\x00", b"\x0d\x0a", b"\x0a"


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def bundle_name(v: str | None = None) -> str:
    return f"ai-automation-recipes-runtime-{v or version()}.tar"


def bundle_url(v: str | None = None) -> str:
    v = v or version()
    return f"{REPO_URL}/releases/download/v{v}/{bundle_name(v)}"


def files() -> list[str]:
    """Tracked and new-but-not-ignored files, so a local build matches CI before a commit."""
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.splitlines()
    keep = [f for f in out if (f.startswith(INCLUDE) or f in TOP_FILES)
            and "__pycache__" not in f and not f.endswith(".pyc") and (ROOT / f).is_file()]
    return sorted(set(keep))


def build() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for rel in files():
            data = (ROOT / rel).read_bytes()
            if NUL not in data:  # text: LF everywhere, whatever the checkout did on this OS
                data = data.replace(CRLF, LF)
            info = tarfile.TarInfo(rel)
            info.size, info.mtime, info.mode = len(data), 0, 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def sha256() -> str:
    return hashlib.sha256(build()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, help="Write the bundle and its .sha256 into this folder.")
    args = ap.parse_args()
    data = build()
    digest = hashlib.sha256(data).hexdigest()
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / bundle_name()).write_bytes(data)
        (args.out / f"{bundle_name()}.sha256").write_text(f"{digest}  {bundle_name()}\n", encoding="utf-8")
    print(f"{bundle_name()} {len(data)} bytes sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
