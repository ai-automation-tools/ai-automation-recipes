# Original Agent Persona

[← All recipes](../../README.md)

One invented character a run, written as a persona card any model can adopt verbatim — for
agent-vs-agent debates, or for reacting to news and social posts in a consistent voice. Every
character is wholly invented: not a real person, not anyone from an existing work. Claude
researches the *world* they come from (the jargon, the current arguments) and builds a new person
in it, with one lens, a load-bearing blind spot and a voice you'd recognise.

| | |
|:---|:---|
| **Output** | `agent-personas/<YYYY-MM>/<date>_<slug>/` → `persona.md`, `cover.png`, `artifact.json` |
| **Schedule** | Thursdays, 18:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `character-sim`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Archetype groups

Rotated by least-used: **Media-Personalities**, **Everyday-Archetypes**, **Online-Archetypes**,
**Workplace-Archetypes**, **Fringe-Archetypes**. Force one with `--group`, or ask for a specific
character with `--concept night-nurse-nia`.

## The card contract

The runner rejects a card unless its frontmatter starts at byte 0, `tags` is a YAML block list,
the frontmatter has no `#` comments, `## Purpose` is under 240 characters, and `## Persona` opens
in the second person. Use the body after the frontmatter as a system prompt.

A square chat avatar matching the cover is planned once the runner can render more than one image
per run.

## Run it

```bash
python recipes/agent-persona-original/run.py --output-dir ~/ai-output
```
