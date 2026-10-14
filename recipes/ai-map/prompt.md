# AI Map

Goal: research and build ONE interactive Leaflet map — a standalone HTML guide to 8–20 real places
on a single theme — plus a companion guide, a sources file, and the description of a cover image.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

{{TOPIC}}

**Maps already built** (date · slug · title — summary). Pick a clearly different topic and place:

{{EXISTING}}

Prefer a topic with 8–20 real locations, natural categories, and enough public information to make
a useful guide. U.S. topics are fine by default; global topics are welcome when especially good.

--------------------------------------------------
## RESEARCH

- Use **WebSearch** / **WebFetch**. Prefer official tourism boards, park services, city pages,
  venue sites, trail organizations, OpenStreetMap/Nominatim, and reputable travel publications.
- Real place names, approximate latitude/longitude. Never invent hours, prices or conditions — keep
  uncertain details qualitative.
- Outdoor topics get safety notes and a "verify current conditions" line.
- Record every source URL in `metadata.md`.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before writing `guide.md` and the stop descriptions; run
`humanizer`'s final pass over them.** Travel writing is the most cliché-saturated genre there is —
ban "nestled in the heart of", "hidden gem", "must-see", "bucket list", "stunning vistas",
"something for everyone". **If a sentence could describe any place on earth, it is not a
description.** A stop earns its entry with something true and specific: what you actually see,
why it's worth the detour, what to skip.

Carve-outs: skip the skills' audit/report steps and ask no questions; the output format wins on
structure; they apply to prose only — never the HTML/CSS/JS or the frontmatter. 🚨 **Keep the
qualitative hedges** ("verify before you go", "hours change seasonally") — accuracy outranks style.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `index.html` — the map

- **Standalone:** opens straight from disk. All CSS and JS inline. Leaflet 1.9.4 from
  `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css` and `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`,
  OpenStreetMap tiles (`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` with the standard
  attribution). No other external files, no API keys, no paid services, no build step.
- Right after `<title>`, this favicon line, exactly:
  `<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23060606'/%3E%3Cpath d='M50 16c-13.8 0-25 11-25 24.6C25 59 50 84 50 84s25-25 25-43.4C75 27 63.8 16 50 16z' fill='none' stroke='%2338bdf8' stroke-width='7' stroke-linejoin='round'/%3E%3Ccircle cx='50' cy='41' r='9' fill='%2338bdf8'/%3E%3C/svg%3E">`
- **Data:** a top-level `const stops = [ { ... }, ... ]`. Every stop has `name`, `category`, `lat`,
  `lng`, a short `desc` and/or `tip`, and `website` — the best public URL (official page or its
  Wikipedia article), or `null` only if none exists after searching. **No photos:** do not
  download, hotlink or embed images of the places.
- A title, short subtitle, and a compact side panel listing the stops (clicking a row flies the
  map to it), at least two marker categories with a visible legend or category toggles, and a route
  line or category structure where it helps.
- **Popups:** bind with `{ maxWidth: 330, minWidth: 300, maxHeight: 380, autoPanPadding: L.point(40, 40) }`;
  style the wrapper `padding: 0; overflow: hidden;` and `.leaflet-popup-content { margin: 0; }`,
  padding your own inner `<div>`. Inside: a coloured category badge, the name, `desc`, `tip` as a
  styled callout, then pill links — "Website" when there is one, and always "Directions" to
  `https://www.google.com/maps/dir/?api=1&destination=<lat>,<lng>`. `bindTooltip(stop.name)` on
  every marker.
- **Phone-usable popups** — include this override (the `!important` beats Leaflet's inline width;
  never use `width: auto`, which shrink-wraps the card):

  ```css
  @media (max-width: 560px) {
    .leaflet-popup { max-width: 92vw !important; }
    .leaflet-popup-content-wrapper { max-width: 92vw; }
    .leaflet-popup-content { width: min(88vw, 320px) !important; max-height: min(46vh, 320px) !important; }
  }
  ```
- **No top-level use of late-assigned variables** — one uncaught error during initial script
  execution leaves a blank map. The runner syntax-checks the script with `node --check`.

### `guide.md` — the companion guide

YAML frontmatter with `title`, `date`, `description`, `tags`. Then: the map's concept and who it's
for, how to use it, the top stops, a relative link to `index.html`, and a short "Verify before you
go" note for anything time-sensitive.

### `metadata.md` — provenance

The topic and why it was chosen; every stop with coordinates and its `website`; every research
source URL; and the items a reader should verify manually.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. `cover_prompt` describes one polished, editorial travel illustration
that reads as this map's topic at thumbnail size — name the scene physically (the coastline, the
ridge, the street at dusk). A "map" or "guide" subject invites signage, labelled pins, legends and
book covers, all of which carry text — avoid those nouns. Commit to a 3–4 colour palette; one clear
subject; full-bleed, no inset panel or frame. The runner renders 16:9 — don't put the ratio in the
prompt. **Forbidden:** text, labels, logos, brand marks, UI screenshots, recognisable people. End
with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Map title>",
  "slug": "<kebab-case-topic-slug>",
  "summary": "<one sentence: what the map covers and who it's for>",
  "topic_type": "<the content type from the rotation, or custom>",
  "place": "<city, region or route>",
  "stops": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
