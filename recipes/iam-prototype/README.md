<h1 align="center">🔐 IAM App Prototype</h1>

<p align="center">
  <em>A runnable identity-and-access tool built on synthetic data, one pain area at a time.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Think certification-fatigue triage, a joiner-mover-leaver tracer, a role-drift explorer, a
break-glass review board. Claude reads what practitioners are complaining about this quarter and
the standard that defines the behaviour, then builds the tool on invented identities and
applications. It assumes a large estate: tens of thousands of identities, hundreds of connected
systems. Vendor-neutral by rule: generic IGA vocabulary and the open standards (SCIM, OIDC, SAML),
never one product's platform. Every source is a page the agent actually fetched; anything it
couldn't confirm goes under *Design assumptions* rather than borrowing a citation.

| | |
|:---|:---|
| **Output** | `iam-prototypes/<YYYY-MM>/<date>_<slug>/` → `README.md`, `requirements.md`, `index.html`, `style.css`, `script.js`, `sample-data.json`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🗂️ Pain areas

Ten: **aggregation**, **certifications**, **lifecycle**, **roles**, **workflow**, **reporting**,
**integration**, **compliance**, **privileged**, **end-user**. Each run takes the least-used one.
Force one with `--area certifications`.

## ✅ What the runner checks

The same checks as [App Prototype](../app-prototype/README.md): valid `sample-data.json`, no missing
local or non-HTTPS references in `index.html`, every script passes `node --check`, and the page
loads in a headless browser without throwing.

## ▶️ Run it

```bash
python recipes/iam-prototype/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../browser-game/README.md">Next: Browser Game →</a>
</p>
