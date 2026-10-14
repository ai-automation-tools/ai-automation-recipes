<h1 align="center">💡 Content Idea</h1>

<p align="center">
  <em>One social-media series an automation could keep producing, researched from what's working now.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude looks at formats, hooks and recurring patterns on TikTok, Shorts, Reels, Reddit, X and
LinkedIn in a rotating topic area, then pitches one series: audience, the trend it rides, treatment,
automation angle, repurposing, and sources.

| | |
|:---|:---|
| **Output** | `content-ideas/<YYYY-MM>/<date>_<slug>/` → `idea.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

Fourteen topic areas, least-used first (AI and automation, productivity, gaming, cybersecurity,
food, internet culture, and more). Force one with `--topic "Gaming"`; any string works.

## Run it

```bash
python recipes/content-idea-gen/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../funny-ai-content/README.md">Next: Funny AI Content →</a>
</p>
