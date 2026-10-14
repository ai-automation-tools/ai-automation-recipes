<h1 align="center">🎭 Original Agent Persona</h1>

<p align="center">
  <em>An invented, debate-ready character, written as a persona card any model can adopt.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Use the card for agent-vs-agent debates, or to react to news and posts in a consistent voice. Every
character is invented: not a real person and not anyone from an existing work. Claude researches
the world they come from (the jargon, the arguments people are having now) and puts a new person in
it, with one lens, a blind spot that matters, and a voice you'd recognize.

| | |
|:---|:---|
| **Output** | `agent-personas/<YYYY-MM>/<date>_<slug>/` → `persona.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `character-sim`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Archetype groups

Least-used first: **Media-Personalities**, **Everyday-Archetypes**, **Online-Archetypes**,
**Workplace-Archetypes**, **Fringe-Archetypes**. Force one with `--group`, or ask for a specific
character with `--concept night-nurse-nia`.

## The card contract

The runner rejects a card unless its frontmatter starts at byte 0, `tags` is a YAML block list, the
frontmatter has no `#` comments, `## Purpose` is under 240 characters, and `## Persona` opens in the
second person. Everything after the frontmatter works as a system prompt.

The recipe doesn't render a square chat avatar yet; the portrait cover is the only image.

## Run it

```bash
python recipes/agent-persona-original/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../content-idea-gen/README.md">Next: Content Idea →</a>
</p>
