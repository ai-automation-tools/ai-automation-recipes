# App Prototype

[← All recipes](../../README.md)

One runnable app prototype a week. Claude researches the last 30 days for a real gap, picks an idea
with a plausible way to make money, and builds it as a single page you open from disk: a README pitch,
a requirements doc, HTML/CSS/JS, and sample data. Browser extensions are out of scope.

| | |
|:---|:---|
| **Output** | `app-prototypes/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `cover.png`, `artifact.json` |
| **Schedule** | Thursdays, 17:00 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## What the runner checks

The run is rejected, and nothing is published, if `sample-data.json` isn't valid JSON, `index.html`
references a local file that doesn't exist or a non-HTTPS URL, or `script.js` / any inline script
fails `node --check` (skipped with a warning when Node isn't installed).

## Run it

```bash
python recipes/app-prototype/run.py --output-dir ~/ai-output
```
