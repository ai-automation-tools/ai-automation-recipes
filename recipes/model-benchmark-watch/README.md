<h1 align="center">📏 Model Benchmark Watch</h1>

<p align="center">
  <em>The week's model releases, and the current frontier head-to-head, with every number traced to a source.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Not a link list. The centre of the briefing is a comparison table of six to ten models across the
closed and open-weight frontier on the benchmarks that matter (LMArena, Artificial Analysis,
MMLU-Pro, GPQA, SWE-bench, context, price), with a reading of who leads where. Around it: what
launched this week, what moved on the leaderboards since the previous edition, and what a builder
should reach for by task.

This started life as a feed-driven beat and failed: there is no reliable RSS for model releases or
leaderboards, so a feed version is inference-engine changelog noise. It works as a web-research job.

| | |
|:---|:---|
| **Output** | `model-benchmark-watch/<YYYY-MM>/<date>_model-benchmark-watch/` → `digest.md`, `cover.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only |

## Continuity

Before each run, the runner hands the agent the previous edition's Head-to-Head table and its
movement section, so the new edition leads with what changed rather than restating standings.

## What the runner rejects

A briefing missing any of the four required sections, a table with fewer than 5 data rows, fewer
than 10 distinct source links, a hedged number in the table ("roughly 1,400"), or a `compared`
count that doesn't match the table. Unverifiable cells are `—`, by rule; the prompt forbids
estimating a score from memory, and the `humanizer` skill is told that "see source" is honesty
here, not a tell to strip.

## Run it

```bash
python recipes/model-benchmark-watch/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../news-digest/README.md">Next: News Digest →</a>
</p>
