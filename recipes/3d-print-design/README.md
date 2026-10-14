<h1 align="center">🖨️ 3D Print Design</h1>

<p align="center">
  <em>One original FDM-printable product, specified well enough to model in CAD.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an optional image key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude starts from what actually sells on maker and marketplace sites, then writes a build-ready
package: dimensions, parts, fits and tolerances, a CAD modeling guide, print settings and a price.
`design-spec.json` carries the same design in a form a modeling agent can read. The cover is a
product mockup.

| | |
|:---|:---|
| **Output** | `3d-print-designs/<YYYY-MM>/<date>_<slug>/` → `README.md`, `design-spec.json`, `sources.csv`, `cover.png` (1:1), `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Needs** | Claude Code. A Gemini or OpenAI key for the cover (optional; without one it publishes uncovered) |

## 🗂️ Subcategories

Nine, least-used first: Household, Organization and Storage, Desk and Tech, Toys and Fidgets, Puzzles
and Games, Art and Decor, Sports and Fan Gear, Tools and Workshop, Outdoor and Garden. Force one with
`--subcategory Desk-and-Tech`.

## ✅ What the runner checks

Nothing is published if `design-spec.json` doesn't parse or has no `parts` array, any part's
bounding box is missing or larger than 220 mm, a part named in the JSON isn't in the README, or
`sources.csv` lacks the `title,url,note` header or has fewer than 4 or more than 8 sources.

## ▶️ Run it

```bash
python recipes/3d-print-design/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../family-recipe/README.md">Next: Family Recipe →</a>
</p>
