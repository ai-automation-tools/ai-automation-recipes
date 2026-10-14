<h1 align="center">⚙️ Core</h1>

<p align="center">
  <em>The runner every recipe goes through, and the helpers recipes share.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge" alt="Python 3.10+">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

A recipe's `run.py` builds a `Recipe` and hands it to `core.run()`. Everything that should behave the
same for every recipe lives here: staging, the agent call, file checks, media rendering and
publishing. The step-by-step version is in [Architecture](../docs/ARCHITECTURE.md).

| Module | What it does |
|:---|:---|
| [**runner.py**](runner.py) | The run loop: `Recipe`, `ImageSpec`, `RunContext`, the hooks, `NothingToDo` |
| [**run-contract.md**](run-contract.md) | The headless rules spliced into every prompt as `{{RUN_CONTRACT}}` |
| [**artifacts.py**](artifacts.py) | Output layout, `artifact.json`, rotation and do-not-repeat helpers |
| [**engines/**](engines/__init__.py) | Text engines behind one interface. Only `claude` today |
| [**images/**](images/__init__.py) | Gemini and OpenAI rendering, the no-text and lettering constraints, resolution tiers |
| [**images/process.py**](images/process.py) | Aspect crops, multi-size ICO, SVG to PNG |
| [**audio/**](audio/__init__.py) | Speech from Gemini or ElevenLabs preset voices; ElevenLabs music from a composition plan |
| [**video.py**](video.py) | ffmpeg slideshow over an audio track; skipped when ffmpeg isn't installed |
| [**web.py**](web.py) | Checks for HTML and JS output: references, `node --check`, Manifest V3, the headless-browser smoke test |
| [**food/**](food/__init__.py) | The recipe-validator safety gate, allergen fixes and the Cook's Card |
| [**digest/**](digest/__init__.py) | The research-digest toolkit: fetchers, parser, bookmark and OPML writers |
| [**deliver.py**](deliver.py) | Optional webhook announcement of each published artifact |

> [!IMPORTANT]
> Agents never call an image, speech or music API. They describe what they want in their final
> JSON, and code in this folder renders it with keys the agent can't see.

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="../docs/ARCHITECTURE.md">Architecture</a> ·
  <a href="../scripts/README.md">Next: Scripts →</a>
</p>
