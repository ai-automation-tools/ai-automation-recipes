# Agent Toolkit

Goal: research and write a toolkit of **at least 24 things you install into an LLM or coding agent**
— skills, slash commands, plugins, MCP servers, hooks, loops, harnesses and prompt packs — sorted
into buckets, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

A list of **things that make an agent more capable**: a file you drop into a client's config, a
repo you point an MCP server at, a command pack you copy into `.claude/commands/`, an IDE plugin, a
harness you wrap a model in.

The test for every candidate: **does a reader install, register or copy this INTO an agent they
already run?** A Claude Code skill passes. An MCP server passes. A `CLAUDE.md` / `AGENTS.md` rule
pack passes. A prompt library passes. A general-purpose Python ML library does not — you import it
into a program; you don't equip an agent with it.

Neighbouring recipes draw the other lines:

- `ai-stack-radar` lists **hosted products** you sign up for. This one lists **artifacts you
  install**. A hosted agent platform is Stack Radar's; the MCP server you register with it is yours.
- The repo digests (`top-10-github-repos`, `oss-spotlight`, `trending-movers`) rank repos by
  popularity, whatever they do. This one selects on **what they plug into**. Overlap with them is
  fine — select on fit, never on whether a sibling got there first.

`github.com/...` links are **normal and expected** here — most of this category ships as a repo.

--------------------------------------------------
## ALREADY FEATURED — DO NOT REPEAT

Everything earlier runs of this recipe listed (date · name — URL). Match on name and URL:

{{FEATURED}}

One carve-out: an entry may return **at least 8 weeks** after it was last covered if it has shipped
something that changes what it is for — a new surface, a rewrite, a spec version, a pivot. Say so in
the entry ("last covered YYYY-MM-DD; returns because …"). Dedup against this recipe's history only.

--------------------------------------------------
## RESEARCH

Places to mine for candidates, then go well beyond them:

- **Skills and commands:** `anthropics/skills`, awesome-claude-code lists, `.claude/skills` and
  `.claude/commands` collections, Cursor rules directories, `AGENTS.md` / `CLAUDE.md` template repos.
- **MCP:** the official MCP servers repo and registry, `modelcontextprotocol/*`, directories (Smithery,
  PulseMCP, Glama), `awesome-mcp-servers`.
- **Plugins and extensions:** VS Code / Cursor / Zed / JetBrains marketplaces (AI category), Copilot
  extensions, Obsidian and Raycast AI plugins, browser-agent extensions.
- **Harnesses and loops:** agent-framework repos and their `examples/`, autonomous-loop projects,
  subagent orchestrators, terminal agents.
- **Practitioners:** Show HN, r/LocalLLaMA, r/ClaudeAI, r/ChatGPTCoding, release notes for the major
  agent CLIs, GitHub Trending filtered to the categories above.

**What earns a slot:**

- **Installable, with an obvious install path** — a README that says where the file goes, a
  marketplace listing, a registry entry, a one-line `npx` / `uvx`. If you can't say in six words how
  a reader adds it, it isn't ready.
- **Alive** — commits, releases or an active issue tracker in the last ~90 days. An abandoned skill
  pack fails silently inside someone's agent.
- **Specific** — name the capability it adds. "A collection of AI stuff" is not an entry.
- **Not a vendor's front door** — link the skill, server or plugin, not `claude.ai` or `cursor.com`.

**Proven AND new, in every bucket:** at least one **established** entry (real adoption — say what
makes it the default) and at least one **fresh** entry (shipped, rewritten or broke out in roughly
the last 60 days — say what's new and when, e.g. "shipped 2026-08-12").

--------------------------------------------------
## BUCKETS

**7–10 buckets, 2–4 entries each, at least 24 in total** (aim for 24–30). Use these names exactly;
rotate which you use.

- **Skills & Capability Packs** — skills, skill collections, capability bundles loaded on demand
- **Slash Commands & Prompt Packs** — command libraries, prompt collections, reusable task templates
- **MCP Servers & Connectors** — servers, registries, gateways, connector suites, transport bridges
- **Plugins & IDE Extensions** — editor and app plugins that add or steer an LLM
- **Agent Loops & Harnesses** — autonomous loops, multi-agent orchestrators, subagent frameworks
- **CLI Agents & Runners** — terminal agents, launchers, session managers, parallel-worktree tooling
- **Rules, Hooks & Guardrails** — rule packs, hook systems, permission and sandbox layers
- **Memory & Context** — context managers, memory servers, agent-oriented retrieval layers
- **Evals & Agent Observability** — eval harnesses, trace viewers, replay tools, regression suites
- **Workflow Recipes & Templates** — ready-made agent workflows and starter kits

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Agent Toolkit — <Month D, YYYY>"
date: {{DATE}}
type: agent-toolkit
site_count: <number of tools listed>
categories: [<the bucket names you used, spelled exactly as above>]
tags: [agent-toolkit, ai, agents, skills, mcp, plugins, commands]
---

# Agent Toolkit — <Month D, YYYY>

> <One sentence: N things to install into your agent — half proven, half brand new.>

## 🧠 Skills & Capability Packs

### [<Tool Name>](<https URL>)
<2–3 sentences: the capability it adds, where it goes (which client, which folder, or the one-line install), and why this one over its neighbours. Say whether it is the established pick or a recent arrival, with a date if new.> **Pricing:** <free / open source / freemium / paid — one clause>.

<...every bucket, every tool in the same shape...>

---

*<total> tools this run.*
```

Rules for the body:

- Every tool is a `### [Name](URL)` link, the description, then **Pricing:** as the **last** thing
  in the paragraph.
- No `**Replaces:**` clause — that belongs to `ai-stack-radar`. Say supersession in the prose.
- Put the install path in the sentence ("drops into `.claude/skills/`", "`npx -y <pkg>`", "one entry
  in `mcp.json`"). Backticks are fine.
- Link the thing itself — repo, marketplace listing, registry entry — never a blog post about it.
- A leading emoji on each `##` bucket heading, bucket text exactly as above. Don't number tools.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: every README you fetch was written with a model, and they all open "A powerful,
extensible framework that empowers developers to…". Two dozen paraphrases of that is a wall of one
sentence.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"modular attachment"** — interlocking geometric modules, socketed forms, branching
connectors. Fixed palette: **deep teal, cyan, warm coral, off-white**.

Dangerous nouns for this digest: "toolbox", "plugin", "terminal", "code editor", "IDE window", "logo",
"app icon".

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Agent Toolkit — <Month D, YYYY>",
  "slug": "agent-toolkit",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
