<h1 align="center">🧪 App Prototype</h1>

<p align="center">
  <em>A working single-page app prototype for an idea that could make money.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude looks at the last 30 days for a real gap, picks an idea with a believable revenue model, and
builds it as a page you open straight from disk. You get the pitch, a requirements doc, the HTML,
CSS and JavaScript, and sample data to click through. Browser extensions are out of scope here;
[Browser Extension](../browser-extension/README.md) covers those.

| | |
|:---|:---|
| **Output** | `app-prototypes/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## ✅ What the runner checks

Nothing is published if:

- `sample-data.json` isn't valid JSON;
- `index.html` points at a local file that doesn't exist, or at a non-HTTPS URL;
- `script.js` or an inline script fails `node --check` (skipped with a warning when Node is missing);
- the page throws a JavaScript error when loaded in a headless browser and clicked (skipped when no
  Chrome, Edge or Playwright Chromium is installed).

## ▶️ Run it

```bash
python recipes/app-prototype/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../browser-extension/README.md">Next: Browser Extension →</a>
</p>
