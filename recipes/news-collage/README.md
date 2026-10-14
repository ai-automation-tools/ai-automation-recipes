<h1 align="center">🗞️ News Collage</h1>

<p align="center">
  <em>The news of a day, a week or a month as one cartoon-editorial image with short captions drawn in.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude researches the major U.S. stories in the window, writes them up with sources, and
describes the image with one exact 3–8 word caption per story. The runner renders it. Nobody real
is drawn: a named person's story is a labelled podium, a courthouse sketch, a ballot map, a
headline. Names appear only as in-world text.

| | |
|:---|:---|
| **Output** | `news-collages/<YYYY-MM>/<date>_<slug>/` → `stories.md`, `collage.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `image-prompt-craft` |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The image is the output, so the run stops before calling Claude without one |

## Windows

Three, least-used first, or forced with `--window`:

| Window | Stories | Image |
|:---|:---|:---|
| `day` | yesterday's six | vertical 2:3, a six-panel 3×2 grid, a `MM/DD/YYYY 11:59 PM` stamp bottom-right |
| `week` | six to ten from the previous Mon–Sun | landscape 3:2, one newsroom-style scene, no grid, titled **WEEK IN REVIEW** with the date range |
| `month` | six from the previous calendar month | the 2:3 grid with a `Month YYYY` stamp |

The dates come from the runner, never from the agent.

## What the runner checks

`stories.md` has one `### ` block per story (six, or six to ten for a week), each with a source
URL and a quoted `**Caption:**` of 3–8 words that is never numbered. The final JSON's
`story_count` matches, and its single image uses the window's aspect. Image models garble long
or small lettering, and the agent can't see the render, so short exact captions are the whole
defence.

## Run it

```bash
python recipes/news-collage/run.py --output-dir ~/ai-output --window week
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../future-cities/README.md">Next: Future Cities 2500 →</a>
</p>
