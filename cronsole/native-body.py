# __NAME__: the Cronsole edition, generated from recipes/__RECIPE__ by scripts/build_registry.py.
# Edit native-body.py or the recipe's cronsole.json in ai-automation-tools/ai-automation-recipes,
# never this copy.
#
# Needs only Python 3.10+ and the agent CLI on the machine Cronsole runs on. The first run
# downloads the pinned runtime release, checks its sha256, and builds a private virtualenv in
# your cache folder; later runs reuse it. API keys come from this task's Cronsole secrets.
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path

VERSION = "__VERSION__"
BUNDLE_URL = "__BUNDLE_URL__"
BUNDLE_SHA256 = "__BUNDLE_SHA256__"
RECIPE = "__RECIPE__"
ARGS = __ARGS__
# Optional keys: an unset secret arrives empty (or as its own unfilled reference on an older
# Cronsole) and is simply not passed on.
KEYS = __KEYS__


def cache_root() -> Path:
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "ai-automation-recipes"


def venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_runtime() -> Path:
    """The unpacked runtime for VERSION, with its virtualenv, building it once."""
    home = cache_root() / VERSION
    if (home / ".ready").is_file():
        return home
    home.parent.mkdir(parents=True, exist_ok=True)
    print(f"setup: fetching runtime {VERSION}", flush=True)
    with urllib.request.urlopen(BUNDLE_URL, timeout=120) as resp:
        data = resp.read()
    got = hashlib.sha256(data).hexdigest()
    if got != BUNDLE_SHA256:
        raise SystemExit(f"RECIPE_FAILED {RECIPE}: runtime bundle sha256 {got} != pinned {BUNDLE_SHA256}")
    work = Path(tempfile.mkdtemp(prefix=f"{VERSION}-", dir=home.parent))
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            for m in tar.getmembers():
                if m.name.startswith(("/", "..")) or ".." in Path(m.name).parts or not (m.isfile() or m.isdir()):
                    raise SystemExit(f"RECIPE_FAILED {RECIPE}: unsafe path in runtime bundle: {m.name}")
            if hasattr(tarfile, "data_filter"):
                tar.extractall(work / "src", filter="data")
            else:
                tar.extractall(work / "src")
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        subprocess.run([str(venv_python(work / "venv")), "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
                        "-r", str(work / "src" / "requirements.txt")], check=True)
        (work / ".ready").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")
        try:
            os.replace(work, home)
        except OSError:
            if not (home / ".ready").is_file():  # lost a race to a run that also failed
                raise
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return home


def main() -> int:
    home = ensure_runtime()
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    for name, value in KEYS.items():
        if value and not value.startswith("${secret."):
            env[name] = value
    logs = cache_root() / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log_file = logs / f"{RECIPE}-{time.strftime('%Y%m%d-%H%M%S')}.log"
    cmd = [str(venv_python(home / "venv")), str(home / "src" / "recipes" / RECIPE / "run.py"), *ARGS]
    with log_file.open("w", encoding="utf-8") as fh:
        code = subprocess.run(cmd, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    # Cronsole keeps the first 2,000 characters of a run's output: the verdict goes first.
    verdict = [l for l in lines if " RECIPE_OK " in l or " RECIPE_FAILED " in l or " RECIPE_SKIPPED " in l]
    print(verdict[-1].split(" ", 3)[-1] if verdict else f"{RECIPE} exited {code} with no verdict")
    print(f"engine run log: {log_file}")
    print("\n".join(lines[-25:]))
    return code


if __name__ == "__main__":
    sys.exit(main())
