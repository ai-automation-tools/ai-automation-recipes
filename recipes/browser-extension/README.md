# Browser Extension

[← All recipes](../../README.md)

One browser extension a week, in two halves: a real Manifest V3 extension you can load unpacked in
Chrome, and a mock-browser demo page that runs the same popup code so you can click through the idea
without installing anything. Claude only picks ideas that genuinely need a browser surface, keeps
permissions to what the code calls, and explains each one.

| | |
|:---|:---|
| **Output** | `browser-extensions/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `extension/` (`manifest.json`, `popup.html`, `popup.css`, `popup.js`, `content.js`, optional `background.js`), `cover.png`, `artifact.json` |
| **Schedule** | Mondays, 16:00 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Load it

Open `chrome://extensions`, turn on **Developer mode**, click **Load unpacked**, and pick the
artifact's `extension/` folder. The manifest ships without icons, so Chrome shows its default badge.

## What the runner checks

The run is rejected, and nothing is published, if:

- `extension/manifest.json` doesn't parse, isn't `manifest_version` 3, lacks `name` / `version`, or
  names a popup, service worker, options page, side panel, content script or icon that isn't in
  `extension/`;
- the content security policy allows `unsafe-eval` or remote script sources;
- an extension page loads an external script, or any extension script uses `eval`, `new Function`
  or remote `importScripts`;
- `sample-data.json` isn't valid JSON, or `index.html` references a missing local file;
- any script fails `node --check` (skipped with a warning when Node isn't installed).

It can't check that every permission is actually used — read the permissions table.

## Sample

> **Exit Ramp** — Marks the real cancel button on a subscription page, labels the retention tricks around it, and keeps a timestamped log you can paste into a complaint.
>
> *First live pilot run, 2026-10-14 · Opus, about 7 minutes · a loadable MV3 extension plus its demo page*

## Run it

```bash
python recipes/browser-extension/run.py --output-dir ~/ai-output
```
