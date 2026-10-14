"""Run the faked-engine smoke scripts for the image recipes (tests/smoke/*.py).

Each script drives every recipe in its group through a good run and a bad run with the
agent and the image engine faked, and exits non-zero on the first surprise.
"""

from __future__ import annotations


import os

# Validators open a real browser when one is available; tests opt in explicitly (BrowserSmokeTests).
os.environ.setdefault("RECIPES_BROWSER_CHECK", "off")

import subprocess
import sys
import unittest
from pathlib import Path

SMOKE = Path(__file__).resolve().parent / "smoke"


class RecipeSmokeTests(unittest.TestCase):
    def test_smoke_scripts(self):
        for script in sorted(SMOKE.glob("*.py")):
            with self.subTest(script=script.name):
                proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True,
                                      encoding="utf-8", cwd=SMOKE.parents[1])
                self.assertEqual(proc.returncode, 0, proc.stdout[-1500:] + proc.stderr[-1500:])


if __name__ == "__main__":
    unittest.main()
