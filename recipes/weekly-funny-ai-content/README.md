# Weekly Funny AI Content

[← All recipes](../../README.md)

One satirical concept a week about an absurd, uncomfortable or questionably useful AI-agent use case
— "using AI to automate your divorce" energy. Each one is a ready-to-shoot bit: the joke, why it
lands, an on-screen treatment, five script beats, the fake automation workflow, and a wordless cover
gag.

| | |
|:---|:---|
| **Output** | `funny-ai-content/<YYYY-MM>/<date>_<slug>/` → `concept.md`, `cover.png`, `artifact.json` |
| **Schedule** | Fridays, 14:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

Five premise families, picked by least-used: emotionally delicate situations, over-automated
domestic life, weird business workflows, petty productivity, socially cursed agents. Force one with
`--family`.

## Run it

```bash
python recipes/weekly-funny-ai-content/run.py --output-dir ~/ai-output
```
