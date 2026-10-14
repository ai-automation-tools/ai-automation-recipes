# Future Cities 2500

[← All recipes](../../README.md)

One real city a week, imagined in the year 2500: Claude extrapolates from its geography,
landmarks, culture and climate, writes the vision, and describes one wide cinematic establishing
shot; the runner renders it at 16:9. The point is that a viewer who knows the city can still name
it.

| | |
|:---|:---|
| **Output** | `future-cities/<YYYY-MM>/<date>_<slug>/` → `city.md`, `cityscape.png`, `artifact.json` |
| **Schedule** | Saturdays, 14:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) — the cityscape is the output |

## Cities

Sixty-eight, least-used first, from San Francisco to Anchorage (see `run.py`). Force one with
`--city "Lisbon"` — any real city works.

## Run it

```bash
python recipes/future-cities/run.py --output-dir ~/ai-output
```
