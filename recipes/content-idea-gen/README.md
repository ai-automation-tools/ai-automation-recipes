# Content Idea

[← All recipes](../../README.md)

One social-media series idea a run. Claude researches what is working right now in a rotating topic
area — formats, hooks, recurring patterns on TikTok, Shorts, Reels, Reddit, X and LinkedIn — and
pitches one series an automation could keep producing: audience, the trend it rides, treatment,
automation angle, repurposing and sources.

| | |
|:---|:---|
| **Output** | `content-ideas/<YYYY-MM>/<date>_<slug>/` → `idea.md`, `cover.png`, `artifact.json` |
| **Schedule** | Wednesdays, 18:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

Fourteen topic areas, picked by least-used (AI and automation, productivity, gaming, cybersecurity,
food, internet culture…). Force one with `--topic "Gaming"` (any string works).

## Run it

```bash
python recipes/content-idea-gen/run.py --output-dir ~/ai-output
```
