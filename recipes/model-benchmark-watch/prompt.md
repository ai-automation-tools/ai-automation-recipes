# Model Benchmark Watch

Goal: research and write a **briefing on the newest AI models, commercial and open-weight, and how
the current frontier stacks up head-to-head on benchmarks**, plus a cover description. Every number
in it traces to a source you fetched.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE PREVIOUS EDITION (continuity, not repetition)

Lead with what is **new since this** and what **moved**. The table may carry stable entries over,
but call out movement; don't restate last edition's news as this edition's.

{{PREVIOUS}}

Editions so far (date · slug · title — summary):

{{EXISTING}}

--------------------------------------------------
## RESEARCH

This is a web-research job. Use **WebSearch** and **WebFetch** heavily, and **never rely on memory
for a model version, a score, a price, a context window or a date.** Look it up and cite it.

- **New and updated models, the last ~7 days.** Commercial and closed (OpenAI, Anthropic, Google
  DeepMind, xAI, Meta, Amazon, Microsoft, Mistral, Cohere, …) **and** open-weight (Llama, Qwen,
  DeepSeek, Mistral, Gemma, Phi, GLM, Kimi, Command, …). For each: name and version, who released
  it, open or closed and the licence, size if open, context window, modalities, and the headline
  benchmark claim **as the source states it**.
- **Leaderboard standings, current.** LMArena, Artificial Analysis, official model cards and release
  posts, the Open LLM Leaderboard, SWE-bench, GPQA Diamond, MMLU-Pro, AIME, LiveCodeBench, Aider,
  and reputable coverage. Verify current values; trackers change weekly.
- **What moved.** A new #1 anywhere, an open model closing on a closed one, a price or speed shift
  that changes the calculus, a surprising eval, a benchmark-integrity dispute.

**Accuracy is the whole beat.** A figure you could not fetch is written as `—` (in the table) or
`see source` (in prose), never estimated. A lab's headline claim is reported *as a claim*, attributed,
never laundered into your own voice and never deleted either.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Model Benchmark Watch — <Month D, YYYY>"
date: {{DATE}}
type: model-benchmark-watch
new_models: <count of models in the New & Updated section>
compared: <count of rows in the Head-to-Head table>
tags: [ai-models, benchmarks, leaderboards, open-weight, commercial]
---

# Model Benchmark Watch — <Month D, YYYY>

> <One sentence: the week's headline in the model race — what dropped, what moved.>

## Overview

<Two to four sentences on the most important developments, grounded in your sources.>

## New & Updated Models

### <Model name and version>
**Who / licence:** <lab; open-weight (licence) or closed>. **What's notable:** <size, context,
modality, the headline claim as the source states it>. **Source:** [<page>](<url>).

<…one block per model; group commercial and open-weight if it reads better. A quiet week says so in
one line and moves on. Never pad.>

## Head-to-Head

| Model | Org | Open? | LMArena Elo | AA Index | MMLU-Pro | GPQA | SWE-bench | Context | $/Mtok in / out |
|:---|:---|:--:|--:|--:|--:|--:|--:|--:|:--|
| <6–10 rows across the closed and open frontier; `—` where you could not verify a cell> |

<A short paragraph reading the state of play: who leads where, best open vs best closed, best
price-to-performance. Every number in the table traces to a link under Sources.>

## Benchmark & Leaderboard Movement

- <what changed since the previous edition: new #1s, jumps, open models closing the gap, new evals,
  integrity notes; exact dates>

## Analysis

<Two to four sentences for builders: which model to reach for by task (coding, reasoning,
long-context, cheap-and-fast), and the open-vs-closed gap right now.>

## Sources

- [<Publisher — page title>](<url>)
<…every source you used, at least ten; this is where every number is backed up.>
```

Rules:

- The four `##` sections after Overview are the required shape; the runner rejects the file without
  them, without at least 5 table rows, or with fewer than 10 source links.
- Exact dates (`YYYY-MM-DD`) everywhere. Columns you can't source for most rows may be dropped or
  swapped for ones you can; the table must still be a markdown table.
- No "approximately", "roughly" or "around" before a number in the table. The figure, or `—`.
- A quiet week still ships a useful edition: a short New Models section and a **current** table are
  always worth publishing.

--------------------------------------------------
## WRITING

{{SKILLS}}

Load `llm-writing` and `humanizer` before you write, and run `humanizer`'s final pass over the prose
before you save. Carve-outs: skip their workflow and output steps (no audit, no report, no
questions); the template above wins on structure; **the table is data and the skills do not apply
inside it**; and `humanizer` flags vague attribution as a tell, but `see source`, `—` and "<Lab>
claims" are this beat's honesty, not hedging to strip.

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. Motif: an abstract **leaderboard** — stacked horizontal bars of
different lengths, a few glowing nodes overtaking others, a faint grid. Fixed palette: **graphite,
electric cyan, signal orange, bone white**. Vary the composition and light from edition to edition,
never the palette. No lettering, numerals, logos, model names, screens or charts with readable
axes; describe the abstract motif. End with the skill's constraint block, verbatim. The runner
renders it at 16:9; don't put the ratio in the prompt.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Model Benchmark Watch — <Month D, YYYY>",
  "slug": "model-benchmark-watch",
  "summary": "<the intro sentence>",
  "new_models": 0,
  "compared": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
