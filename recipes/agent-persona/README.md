<h1 align="center">🎤 Agent Persona (Known Figure)</h1>

<p align="center">
  <em>A debate-ready persona card for a real person or an established character, researched from their public record.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The other half of the persona pair. [Original Agent Persona](../agent-persona-original/README.md)
invents people; this one writes figures the audience already knows: celebrities, politicians,
comedians, athletes, founders, hosts, historical figures, and characters from existing shows, films,
games and books. Claude researches how the figure actually talks and what they actually argue, then
writes a caricature of the persona and rhetoric. The source prompt's guardrails carry over as
written: public record only, no fabricated misdeeds about living people, no slurs, safe for work,
public figures only.

| | |
|:---|:---|
| **Output** | `agent-personas/<YYYY-MM>/<date>_<slug>/` → `persona.md`, `cover.png`, `avatar.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `character-sim`, `llm-writing`, `humanizer`, `image-prompt-craft` |

## Subcategories

Least-used first: **Comedy**, **Political**, **Celebrity**, **Fictional**, **Sports**, **Music**,
**Tech**, **Host**, **Internet**, **Historical**. Force one with `--subcategory`, or name the figure
with `--figure gordon-ramsay`.

## The card contract

Same contract as the original-character recipe, plus `real_or_fictional` in the frontmatter and the
final JSON. The collection is shared between the two recipes, so a slug that already has a card is
rejected instead of written again.

With an image key set, the cover prompt carries the figure's name and an explicit physical
description, because a name-only prompt renders a stranger. Image engines sometimes decline a real
person's likeness; the run then publishes the card without that picture.

## Run it

```bash
python recipes/agent-persona/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../agent-persona-original/README.md">Next: Original Agent Persona →</a>
</p>
