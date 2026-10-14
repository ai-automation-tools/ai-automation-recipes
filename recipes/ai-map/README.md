<h1 align="center">📍 AI Map</h1>

<p align="center">
  <em>A researched, interactive map of 8 to 20 real places on one theme.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The theme might be a scenic drive, a coffee crawl, a waterfall loop or a music-history walk. Claude
finds the places, their coordinates and official links, and builds a standalone Leaflet map with a
category legend, a stop list that flies the map to each stop, and popups with Website and Directions
links that work on a phone. A guide, a metadata file and a cover come with it.

| | |
|:---|:---|
| **Output** | `maps/<YYYY-MM>/<date>_<slug>/` → `index.html`, `guide.md`, `metadata.md`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🧭 Topics

Eight types, least-used first: scenic drives, food trails, outdoor recreation, parks and public
lands, city guides, culture tours, seasonal outings, niche practical guides. To build one specific
map instead, pass `--idea "coffee crawl in Portland"`.

## ✅ What the runner checks

Nothing is published if `index.html` loads anything other than Leaflet from a CDN (or a `data:`
URI), has no `stops = [...]` array, has an inline script that fails `node --check`, or throws when
loaded in a headless browser. Map tiles come from OpenStreetMap when you view the map.

The map has **no photos of the places**. Downloading or hotlinking venue images raises licensing
questions, so each stop links to its website instead.

## ▶️ Run it

```bash
python recipes/ai-map/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../agent-toolkit/README.md">Next: Agent Toolkit →</a>
</p>
