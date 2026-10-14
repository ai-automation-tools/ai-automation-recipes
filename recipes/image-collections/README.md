<h1 align="center">🗂️ Image Collections</h1>

<p align="center">
  <em>Long-running image series that each gain one researched entry per run.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

A collection is either a year-by-year series or an ordered list worked through from start to
finish. On each run Claude researches the next entry in every active collection, writes a sourced
note, and writes one image prompt per entry; the runner renders them. An entry may letter a short
title or year into its image, and only the exact words quoted in the prompt are allowed.

| | |
|:---|:---|
| **Output** | `collections/<YYYY-MM>/<date>_collections-<date>/` → `entries.md`, `images/*.png`, `cover.png`, `artifact.json` |
| **Config** | `collections/collections.json`, seeded on the first run and yours to edit |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `image-prompt-craft`, `llm-writing`, `humanizer` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) |

## The seeded collections

| id | Kind | Covers |
|:---|:---|:---|
| `science-breakthroughs` | years | 2000 to the last complete year: a popular-science montage of each year's breakthroughs |
| `technology-milestones` | list | 37 milestones from the control of fire to modern AI, as cartoon editorial scenes |
| `exoplanets` | list | 25 real exoplanets, each with a plausible creature shaped by its world |

Looking for a cities series? That's its own recipe, [Future Cities 2500](../future-cities/README.md).

## Adding your own

Add an object to `collections` in `collections.json`:

```json
{
  "id": "space-missions", "title": "Space Missions", "active": true,
  "kind": "years", "start": 1957, "end": 1999, "aspect": "3:2", "research": true,
  "lettering": "the year, e.g. \"1969\"",
  "brief": "One retro-futurist mission-control montage per year: ..."
}
```

`kind` is `years` (`start` to `end`, where `end` can be `"last-complete"`) or `list` (an `items`
array of `{"key", "label"}`). `lettering` is the short text to letter into the image, or `"none"`.
Set `active` to `false` to pause a collection. Progress is read from the published entries, so
editing the file never loses your place. When every collection is finished, the run skips without
calling Claude.

## Cost

One billed image per active collection per run, so three with the seeds.

## Run it

```bash
python recipes/image-collections/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../song-generator/README.md">Next: Song →</a>
</p>
