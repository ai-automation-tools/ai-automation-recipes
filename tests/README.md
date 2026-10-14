<h1 align="center">🧪 Tests</h1>

<p align="center">
  <em>Everything that can be checked without spending a key: the run loop, media steps, recipes, the viewer.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/runner-unittest-3776AB?style=for-the-badge" alt="unittest">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

```bash
python -m unittest discover -s tests
```

Agents, image, speech and music APIs are faked throughout. The one real external call is the browser
smoke test, which drives a local headless browser and skips itself when none is installed.

| File | What it covers |
|:---|:---|
| [**test_core.py**](test_core.py) | The run loop: JSON extraction, prompt filling, rotation, staging, hooks, all-or-nothing publishing |
| [**test_engines.py**](test_engines.py) | The three text engines: command shape, Claude-alias handling, and parsing of Codex's JSONL and Gemini's JSON, from recorded output |
| [**test_media.py**](test_media.py) | Multi-image runs, key preflight, crops, ICO, SVG, speech, music, video length |
| [**test_shared.py**](test_shared.py) | Web checks, the food safety gate, the Cook's Card, digests, the webhook, the browser smoke test |
| [**test_audio_recipes.py**](test_audio_recipes.py) | The song, podcast and voiceover recipes end to end with every engine faked |
| [**test_viewer.py**](test_viewer.py) | The viewer catalog, and that model-written HTML can't run in it |
| [**test_recipe_smoke.py**](test_recipe_smoke.py) | Runs the scripts in [`smoke/`](smoke/): a good and a bad run of every image recipe, plus a keyless run of the two whose images are optional |

> [!NOTE]
> Tests set `RECIPES_BROWSER_CHECK=off` so validators don't open a browser on every case.
> `BrowserSmokeTests` turns it back on for itself.

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="../registry/README.md">Registry</a> ·
  <a href="../.claude/skills/README.md">Next: Skills →</a>
</p>
