# Weekly AI Map

[← All recipes](../../README.md)

One researched, interactive map a week. Claude picks a theme — a scenic drive, a coffee crawl, a
waterfall loop, a music-history walk — finds 8–20 real places with coordinates and official
links, and builds a standalone Leaflet map: category legend, a stop list that flies the map,
phone-friendly popups with Website and Directions links. A companion guide, a sources file and a
cover come with it.

| | |
|:---|:---|
| **Output** | `maps/<YYYY-MM>/<date>_<slug>/` → `index.html`, `guide.md`, `metadata.md`, `cover.png`, `artifact.json` |
| **Schedule** | Mondays, 12:30 UTC |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Topics

Eight types, least-used first: scenic drives, food trails, outdoor recreation, parks and public
lands, city guides, culture tours, seasonal outings, niche practical guides. Build a specific map
with `--idea "coffee crawl in Portland"`.

## What the runner checks

`index.html` is rejected if it loads anything other than Leaflet from a CDN (or a `data:` URI),
has no `stops = [...]` array, or has an inline script that fails `node --check`. Map tiles come
from OpenStreetMap at view time.

The map has **no place photos** — downloading or hotlinking images of venues raises licensing
questions, so stops carry a website link instead.

## Run it

```bash
python recipes/weekly-ai-map/run.py --output-dir ~/ai-output
```
