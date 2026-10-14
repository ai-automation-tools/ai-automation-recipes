<h1 align="center">📖 Short Story</h1>

<p align="center">
  <em>A finished 2,000–4,000-word story in a rotating genre, with a portrait cover.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Each run writes one complete story. Claude gets the title and logline of every story already in the
collection and has to stay clear of their premises, characters and twists. The cover shows a single
moment from the story, not a summary of the plot.

| | |
|:---|:---|
| **Output** | `short-stories/<YYYY-MM>/<date>_<slug>/` → `story.md`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Genres

Eleven, least-used first: near-future AI fiction, cozy mystery, cyberpunk, office absurdism, magical
realism, quiet horror, tech satire, fantasy, identity/security thriller, comedy, hard sci-fi. Force
one with `--genre "cozy mystery"`.

## Sample

> **The Blue Words** — When a firmware update shows a retired Duluth dock worker which words his
> hearing aids have been quietly guessing, he learns that the one sentence that carried him through
> his wife's death was never said.
>
> *Near-future AI fiction · 3,165 words · first live pilot run, 2026-10-14 (Opus, about 3 minutes)*

## Idea queue (optional)

Create `<output-dir>/short-stories/story-ideas.md`:

```markdown
- [ ] A lighthouse keeper who starts receiving letters from the ships she failed to warn
- [ ] An HR chatbot that unionizes
```

A run takes the first unchecked idea as its premise and ticks it off with a link to the story it
became: `- [x] A lighthouse keeper… — story: 2026-10/2026-10-18_the-keeper`.

## Run it

```bash
python recipes/short-story/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../serialized-novella/README.md">Next: Serialized Novella →</a>
</p>
