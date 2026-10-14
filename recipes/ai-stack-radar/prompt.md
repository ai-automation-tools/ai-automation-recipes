# AI Stack Radar

Goal: research and write a **radar of hosted AI products and services** — at least 24, sorted into
buckets by the job they do, each with what it replaces and what it costs — plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

A list of **things you can sign up for and use today**: hosted products, managed services, APIs and
installable apps that have a homepage and a pricing page.

It is deliberately **not a repo list.** `top-10-github-repos`, `oss-spotlight` and `trending-movers`
cover GitHub. If the only URL you can give for something is a `github.com/...` link, it doesn't
belong here. The line to hold: **a repo is source code; a product is something running that you
point your account at.** A self-hostable project qualifies only if it also ships a hosted tier with
its own domain — link the product site, not the repo.

It is also not `cool-websites`, which is broad-internet and favours the obscure and delightful. This
one is narrow and practical: AI, and only AI, judged on whether it would earn a slot in a working
stack.

--------------------------------------------------
## ALREADY FEATURED — DO NOT REPEAT

Every product earlier runs listed (date · name — URL). Match on name **and** root domain:

{{FEATURED}}

One carve-out: a product may return **at least 8 weeks** after it was last covered if it has shipped
something that changes what it is for — a new modality, a new tier, a pivot. Say so in the entry
("last covered YYYY-MM-DD; returns because …").

--------------------------------------------------
## RESEARCH

Places to mine for candidates, then go well beyond them:

- Show HN and the Hacker News front page; Product Hunt's AI category; Betalist.
- Lab and vendor changelogs — Anthropic, OpenAI, Google DeepMind, Mistral, Meta AI, Cohere,
  Together, Fireworks, Replicate, Modal, Baseten.
- r/LocalLLaMA, r/MachineLearning, r/AI_Agents, r/selfhosted.
- MCP server directories and registries; agent-framework docs sites.
- Funding announcements and launch posts from the last 30 days.

**What earns a slot:**

- **Hosted and reachable** — it resolves, and it is the product you think it is.
- **AI-native** — its core value comes from a model doing something. A CRM that added a summarize
  button does not qualify.
- **Usable without a sales call** — self-serve signup, a documented public API, or a free tier. Skip
  anything whose only call to action is "Book a demo".
- **Specific enough to place in a stack** — if you can't say what it replaces or sits next to, it
  isn't ready.
- **Useful but underexposed** beats famous. Assume the reader knows ChatGPT, Claude, Midjourney and
  Copilot; include a major vendor only for a specific new surface, not the brand.

--------------------------------------------------
## BUCKETS

**7–10 buckets, 2–4 products each, at least 24 in total** (aim for 24–30). Rotate the mix; you
needn't use every bucket and may add a sensible new one.

- **Agents & Orchestration** — agent platforms and hosting, multi-agent runtimes, workflow builders
- **MCP & Tool Plumbing** — MCP servers and registries, tool-calling gateways, connector platforms
  (*include most runs*)
- **Coding & Dev** — assistants, review, test generation, migration, agentic IDEs
- **Text & Reasoning APIs** — model providers, routers, gateways, structured-output services
- **Image & Design** — generation, editing, upscaling, background removal, brand and asset tooling
- **Video & Motion** — generation, editing, dubbing, lipsync, avatars
- **Voice & Audio** — TTS, STT, voice cloning, music, real-time speech
- **Research & Retrieval** — search APIs, RAG platforms, vector stores, document extraction, scraping
- **Local & Self-Hosted Inference** — runners, quantization, model servers, desktop apps (hosted-tier
  rule still applies)
- **Evals, Observability & Guardrails** — tracing, eval harnesses, prompt management, safety filters
- **Data & Training** — labeling, synthetic data, fine-tuning platforms, dataset tooling
- **Automation & Integration** — no-code runners, schedulers, webhook and glue platforms

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "AI Stack Radar — <Month D, YYYY>"
date: {{DATE}}
type: ai-stack-radar
site_count: <number of products listed>
categories: [<the bucket names you used>]
tags: [ai-stack-radar, ai, tools, agents, mcp, apis]
---

# AI Stack Radar — <Month D, YYYY>

> <One sentence: N hosted AI products worth knowing about, sorted by the job they do.>

## 🤖 Agents & Orchestration

### [<Product Name>](<https URL>)
<1–2 sentences: what it does, and the specific thing it does that its neighbours don't.> **Replaces:** <what it slots in for or sits next to>. **Pricing:** <free tier / freemium / paid — one clause>.

<...every bucket, every product in the same shape...>

---

*<total> products this run.*
```

Rules for the body:

- Every product is a `### [Name](URL)` link, then the description, then **Replaces:** and
  **Pricing:** in the same paragraph. That trailing pair is what makes the list usable — never drop it.
- Link the **product homepage**, not docs, a blog post, or a GitHub repo.
- A leading emoji on each `##` bucket heading. Don't number products; don't repeat one within the run.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: product marketing copy is itself LLM-shaped, and it is right there on every page
you fetch. Two dozen entries lifted in tone from two dozen landing pages reads like a press-release
feed.

--------------------------------------------------
## COVER IMAGE

Motif: an abstract **"stack"** — layered translucent planes, signal sweeps and constellation nodes.
Fixed palette: **deep indigo, electric violet, warm amber, off-white**.

Dangerous nouns for this digest: "dashboard", "UI", "app window", "logo", "product card", "icon grid".

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "AI Stack Radar — <Month D, YYYY>",
  "slug": "ai-stack-radar",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
