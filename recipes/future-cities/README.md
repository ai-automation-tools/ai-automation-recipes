<h1 align="center">🌆 Future Cities 2500</h1>

<p align="center">
  <em>A real city imagined in the year 2500, as one wide cinematic shot.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude works from the city's geography, landmarks, culture and climate, writes the vision, and
describes one wide establishing shot. The runner renders it at 16:9. The test is whether someone
who knows the city can still name it.

| | |
|:---|:---|
| **Output** | `future-cities/<YYYY-MM>/<date>_<slug>/` → `city.md`, `cityscape.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The cityscape is the output |

## Cities

Sixty-eight, least-used first, from San Francisco to Anchorage (see `run.py`). Force one with
`--city "Lisbon"`; any real city works.

## Run it

```bash
python recipes/future-cities/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../image-prompt-packs/README.md">Next: Image Prompt Pack →</a>
</p>
