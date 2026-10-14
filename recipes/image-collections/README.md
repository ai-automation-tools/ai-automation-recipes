# Image Collections

[← All recipes](../../README.md)

Long-running image collections that grow by one entry per collection every run: a year-by-year
series, or an ordered list worked through from start to finish. Each run, Claude researches the
next entry in every active collection, writes a sourced note, and writes one image prompt per
entry; the runner renders them. Entries may letter a short title or year into the image — only
the exact words quoted in the prompt are allowed.

| | |
|:---|:---|
| **Output** | `collections/<YYYY-MM>/<date>_collections-<date>/` → `entries.md`, `images/*.png`, `cover.png`, `artifact.json` |
| **Config** | `collections/collections.json` — seeded on the first run, yours to edit |
| **Schedule** | Tuesdays and Saturdays, 15:00 UTC |
| **Model** | `sonnet` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `image-prompt-craft`, `llm-writing`, `humanizer` |

## The seeded collections

| id | Kind | Walks |
|:---|:---|:---|
| `science-breakthroughs` | years | 2000 → the last complete year: a popular-science montage of each year's breakthroughs |
| `technology-milestones` | list | 37 milestones from the control of fire to modern AI, as cartoon editorial scenes |
| `exoplanets` | list | 25 real exoplanets, each with a plausible creature shaped by its world |

Looking for a cities series? That's its own recipe, [`future-cities`](../future-cities/README.md).

## Adding your own

Add an object to `collections` in `collections.json`:

```json
{
  "id": "space-missions", "title": "Space Missions", "active": true,
  "kind": "years", "start": 1957, "end": 1999, "aspect": "3:2", "research": true,
  "lettering": "the year, e.g. \"1969\"",
  "brief": "One retro-futurist mission-control montage per year: …"
}
```

`kind` is `years` (`start`..`end`, where `end` can be `"last-complete"`) or `list` (an `items` array
of `{"key", "label"}`). `lettering` is the short text to letter into the image, or `"none"`. Set
`active` to `false` to pause a collection. Progress comes from the published entries, so editing
the file never loses your place; when every collection is finished, the run exits without calling
Claude.

## Cost

One billed image per active collection per run (three with the seeds).

## Run it

```bash
python recipes/image-collections/run.py --output-dir ~/ai-output
```
