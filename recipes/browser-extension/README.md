<h1 align="center">🧩 Browser Extension</h1>

<p align="center">
  <em>A Manifest V3 extension you can load unpacked, plus a demo page that runs the same popup code.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The output comes in two halves. One is a real extension folder Chrome will load. The other is a
mock-browser page that runs the popup's own code, so you can try the idea without installing
anything. Claude only picks ideas that need to live in the browser, asks for the permissions the
code actually uses, and explains each one in a table.

| | |
|:---|:---|
| **Output** | `browser-extensions/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `extension/` (`manifest.json`, `popup.html`, `popup.css`, `popup.js`, `content.js`, optional `background.js`), `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🔌 Load it

Open `chrome://extensions`, turn on **Developer mode**, click **Load unpacked**, and pick the
artifact's `extension/` folder. The manifest ships without icons, so Chrome shows its default badge.

## ✅ What the runner checks

Nothing is published if:

- `extension/manifest.json` doesn't parse, isn't `manifest_version` 3, lacks `name` or `version`, or
  names a popup, service worker, options page, side panel, content script or icon that isn't in
  `extension/`;
- the content security policy allows `unsafe-eval` or remote script sources;
- an extension page loads an external script, or an extension script uses `eval`, `new Function` or
  a remote `importScripts`;
- `sample-data.json` isn't valid JSON, or `index.html` points at a missing local file;
- any script fails `node --check`, or the demo page throws when loaded in a headless browser.

It can't tell whether every declared permission is used. The README's permissions table is where to
check that.

## 🧪 Sample

> **Exit Ramp** — Marks the real cancel button on a subscription page, labels the retention tricks
> around it, and keeps a timestamped log you can paste into a complaint.
>
> *First live pilot run, 2026-10-14 · Opus, about 7 minutes · a loadable MV3 extension plus its demo page*

## ▶️ Run it

```bash
python recipes/browser-extension/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../finance-app-prototype/README.md">Next: Finance App Prototype →</a>
</p>
