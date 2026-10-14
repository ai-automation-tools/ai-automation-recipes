<h1 align="center">🗺️ Alternate History</h1>

<p align="center">
  <em>One real turning point, changed, and traced forward through eight short sections.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-opus-8B5CF6?style=for-the-badge" alt="Default model: opus">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude picks a well-documented moment, changes exactly one thing, and follows the consequences from
days to years to decades. It stays grounded and non-graphic. Each section also gets a scene
illustration prompt, all written to one shared palette.

| | |
|:---|:---|
| **Output** | `alternate-history/<YYYY-MM>/<date>_<slug>/` → `story.md`, `scene-prompts.md`, `cover.png`, `artifact.json` |
| **Model** | `opus` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `writing-principles`, `creative-writing-craft`, `llm-writing`, `humanizer`, `image-prompt-craft` |

The runner rejects a piece unless `story.md` has exactly eight sections and `scene-prompts.md` has a
prompt for each. Only the 2:3 cover is rendered; the eight scene prompts are written but not
rendered.

## Premise queue (optional)

Create `<output-dir>/alternate-history/alt-history-ideas.md`:

```markdown
- [ ] The Library of Alexandria is never destroyed and survives to the present.
- [ ] The Apollo 13 crew does not make it home.
```

A run takes the first unchecked premise and ticks it off with the folder it became. With no queue,
Claude invents a divergence and avoids the ones already written.

## Run it

```bash
python recipes/alternate-history/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../agent-persona-original/README.md">Next: Original Agent Persona →</a>
</p>
