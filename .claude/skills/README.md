<h1 align="center">🧠 Skills</h1>

<p align="center">
  <em>The skills recipes load, copied into each run's staging folder so a run behaves the same everywhere.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/skills-14-8B5CF6?style=for-the-badge" alt="14 skills">
  <a href="../../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

A recipe names the skills it wants in `Recipe(skills=...)`, and its prompt says when to load each one
and what it must not touch. Prompts never paste skill text, so a skill has one copy, here.

## ✍️ Writing

| Skill | What it does | Source |
|:---|:---|:---|
| [**llm-writing**](llm-writing/SKILL.md) | Word choice and the default LLM phrasing to strip before a draft ships | Apache-2.0, [creative-writing-skills](_vendor/creative-writing-skills/README.md) |
| [**humanizer**](humanizer/SKILL.md) | The tells of AI writing and a final pass to remove them | MIT, Siqi Chen ([license](humanizer/LICENSE)) |
| [**writing-principles**](writing-principles/SKILL.md) | Prose fundamentals the fiction recipes write against | Apache-2.0, creative-writing-skills |
| [**creative-writing-craft**](creative-writing-craft/SKILL.md) | Scene construction, prose and genre references | Apache-2.0, creative-writing-skills |
| [**creative-writing-modes**](creative-writing-modes/SKILL.md) | Prose modes for long-form chapters | Apache-2.0, creative-writing-skills |
| [**story-review**](story-review/SKILL.md) | The antipattern list the novella writes against | Apache-2.0, creative-writing-skills |
| [**story-planning**](story-planning/SKILL.md) | Arc and chapter planning; a companion the others reference | Apache-2.0, creative-writing-skills |
| [**reader-sim**](reader-sim/SKILL.md) | A simulated reader's reaction; a companion the others reference | Apache-2.0, creative-writing-skills |
| [**character-sim**](character-sim/SKILL.md) | Voice and character work for the persona recipe | Apache-2.0, creative-writing-skills |
| [**songwriting-craft**](songwriting-craft/SKILL.md) | Lyrics sized to an ElevenLabs composition plan | CC0, derived from [claude-ai-music-skills](_vendor/claude-ai-music-skills/README.md) |

## 🎨 Building and drawing

| Skill | What it does | Source |
|:---|:---|:---|
| [**image-prompt-craft**](image-prompt-craft/SKILL.md) | How to write an image prompt that gets the picture you meant | This repo |
| [**game-design**](game-design/SKILL.md) | Core loops, difficulty curves and what makes a short game worth replaying | This repo |
| [**single-file-game-dev**](single-file-game-dev/SKILL.md) | Delta time, high-DPI canvases, touch input and audio unlock for one-file games | This repo |
| [**recipe-validator**](recipe-validator/SKILL.md) | Food safety, nutrition and allergen checks, with a scanner script | This repo |

> [!NOTE]
> Vendored skills are copied as published, apart from `songwriting-craft`, which was retargeted from
> Suno to ElevenLabs. License texts are in [`_vendor/`](_vendor/) and in each skill's own folder.

---

<p align="center">
  <a href="../../README.md">← Repository home</a> ·
  <a href="../../tests/README.md">Tests</a> ·
  <a href="../../docs/README.md">Next: Docs →</a>
</p>
