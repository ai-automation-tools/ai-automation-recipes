<h1 align="center">🗞️ Satirical News</h1>

<p align="center">
  <em>One deadpan, Onion-style article under the masthead The Overcorrect, with pictures that play it straight.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/beats-12-0078D4?style=for-the-badge" alt="12 beats">
  <img src="https://img.shields.io/badge/pictures-optional_image_key-F59E0B?style=for-the-badge" alt="Pictures need an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

The headline is the joke, the body reports it as established fact, and the invented experts escalate
it. Claude may anchor the piece on a real story found with WebSearch, recorded in the frontmatter
so the reader can see what was bent, or make it up outright. The guardrails from the source
automation carry over as written: no slurs or protected-class punchlines, public figures only and
only as obvious parody, no fabricated defamatory claims, no real-world harm content, and the piece
must read as satire rather than a hoax.

| | |
|:---|:---|
| **Output** | `satirical-news/<YYYY-MM>/<date>_<slug>/` → `article.md`, `metadata.md`, `cover.png`, `images/{thumbnail,supporting-1,supporting-2}.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |

## Beats

Least-used first: AI Tool Releases, New Technology & Products, Politics, Finance & Economy, Space
& Aliens, Science & Discovery, Sports, Entertainment & Celebrity, Health & Wellness, Local / Area
Man, Business & Corporate, Environment & Climate. Force one with `--beat`, or hand over a premise
with `--topic "hoa bans weather"`.

## What the runner checks

Frontmatter at byte 0 with a `news_category` from the twelve, a bold dateline opener, a body of 350
to 650 words with the image lines excluded, a real URL in `inspired_by` whenever
`based_on_true_event` is true, and a sidecar with at least three key points and a summary.

With an image key set, the four pictures share one pasted style clause so they look like one
publication shot them. Without a key the article still publishes, image lines and all.

## Run it

```bash
python recipes/satirical-news/run.py --output-dir ~/ai-output --beat "Space & Aliens"
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../content-idea-gen/README.md">Next: Content Idea →</a>
</p>
