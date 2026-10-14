# Finance Toolkit

Goal: research and write a toolkit of **at least 22 financial tools** — market-data APIs, quant and
backtesting libraries, broker SDKs, portfolio and accounting software, finance AI and agents, fintech
infrastructure, on-chain tooling, screeners, and the money apps worth running — sorted into buckets,
plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

The **finance corner of a working stack**: the library you `pip install` to backtest a strategy, the
API you call for prices, the SDK you place orders through, the open-source ledger you run your books
on, the agent that reads a 10-K for you, the terminal you screen with.

The test for every candidate: **would somebody who works with money or builds financial software put
this in their stack?** A market-data API passes. A backtesting framework passes. A double-entry
engine passes. An agent that parses filings passes. A budgeting app people genuinely use passes. A
generic "AI for business" SaaS with a finance page does not; neither does a news site, a subreddit,
or a trading course.

**Lean builder, not consumer.** About seven entries in ten should be something a developer or analyst
installs, imports or calls. **Personal Finance Tools** is the smallest bucket, never the anchor.

Overlap with `ai-stack-radar`, `agent-toolkit` and the repo digests is expected — this recipe is
scoped by subject. `github.com/...` links are normal here.

⚠️ **This is not investment advice and must never read like it.** Describe what a tool *does*, never
what to buy, hold or trade. No tickers as recommendations, no "poised to", no performance claims. A
backtesting library is a tool; a strategy that "returns 40% annually" is a claim, and it doesn't go in.

--------------------------------------------------
## ALREADY FEATURED — DO NOT REPEAT

Everything earlier runs of this recipe listed (date · name — URL). Match on name and URL:

{{FEATURED}}

One carve-out: an entry may return **at least 6 months** after it was last covered if it has shipped
something that changes what it is for — a new data class, an API v2, a licence change, a pivot. Say
so in the entry ("last covered YYYY-MM-DD; returns because …").

--------------------------------------------------
## RESEARCH

Finance tooling churns on two axes you can't guess: **free tiers get cut** and **APIs get
deprecated**. A pricing line from memory is the most likely thing in this digest to be wrong.

Places to mine for candidates, then go beyond them:

- **Data and APIs:** provider docs and pricing pages, `awesome-quant`, OpenBB's provider list,
  exchange and central-bank open-data portals, FRED / SEC EDGAR tooling, alt-data vendors.
- **Quant and research:** backtesting and portfolio-optimisation repos, factor and risk libraries,
  notebook-first research stacks, university and lab releases.
- **Brokers and execution:** broker API docs and official SDKs, paper-trading layers, FIX and
  market-connectivity libraries.
- **Books and back office:** open-source accounting and double-entry engines, plain-text accounting,
  invoicing, payroll and treasury tooling.
- **Finance AI:** filing and transcript parsing, finance-tuned models and evals, finance MCP
  servers, research agents, statement and contract extraction.
- **Infrastructure:** payments, ledgers, banking-as-a-service, reconciliation, KYC/AML, tax engines,
  timeseries stores built for market data.
- **On-chain:** indexers, RPC and node tooling, DeFi analytics libraries, wallet and custody SDKs.
- **Practitioners:** Show HN, r/algotrading, r/quant, r/plaintextaccounting, quant and fintech
  newsletters, GitHub Trending filtered to finance topics.

**What earns a slot:**

- **Usable, with an obvious entry point** — install instructions, public API docs, or a real signup.
- **Alive** — activity in the last ~6 months. An abandoned broker SDK still installs and still fails
  at the exchange.
- **Honest about cost and access** — say whether a free tier exists, what it caps (calls/day,
  symbols, history depth, delayed vs real-time), and whether data licensing restricts
  redistribution. **A wrong free-tier claim is the most damaging error this digest can make** —
  verify it on the provider's own pricing page, never a blog post.
- **Specific** — name the asset classes, the coverage, what it actually returns.
- **Not a brokerage ad** — link the API docs, repo or SDK, not an "open an account" page.

**Proven AND new, in every bucket:** at least one **established** entry (say what makes it the
default) and at least one **fresh** entry (shipped, rewritten or relicensed in roughly the last
6 months — say what and when, e.g. "v3 shipped 2026-07").

--------------------------------------------------
## BUCKETS

**7–9 buckets, 2–4 entries each, at least 22 in total** (aim for 22–28). Use these names exactly;
**Personal Finance Tools must never be the largest**.

- **Market Data & APIs** — price, fundamental, macro, alternative and reference data; client libraries
- **Quant & Backtesting** — engines, strategy frameworks, optimisation, risk and factor libraries
- **Trading & Broker SDKs** — broker and exchange APIs, SDKs, order routing, paper trading
- **Portfolio & Accounting** — P&L tracking, double-entry and plain-text accounting, back office
- **Finance AI & Agents** — filing parsing, finance models and evals, research agents, MCP servers
- **Fintech Infrastructure** — payments, ledgers, BaaS, reconciliation, KYC/AML, tax and compliance
- **Crypto & On-Chain** — indexers, RPC and node tooling, DeFi analytics, wallet and custody SDKs
- **Research & Screening** — screeners, terminals, valuation tooling, economic-data explorers
- **Personal Finance Tools** — budgeting, net worth, tax prep, retirement modelling, self-hosted money apps

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Finance Toolkit — <Month D, YYYY>"
date: {{DATE}}
type: finance-toolkit
site_count: <number of tools listed>
categories: [<the bucket names you used, spelled exactly as above>]
tags: [finance-toolkit, finance, fintech, quant, trading, open-source, ai]
---

# Finance Toolkit — <Month D, YYYY>

> <One sentence: N financial tools — data feeds, backtesting engines, broker SDKs and the money software worth running.>

## 📊 Market Data & APIs

### [<Tool Name>](<https URL>)
<2–3 sentences: what it covers (asset classes, history depth, update frequency), how a reader starts using it, and why this one over its neighbours. Say whether it is the established pick or a recent arrival, with a date if new.> **Pricing:** <free / open source / freemium with the cap named / paid from $X — one clause>.

<...every bucket, every tool in the same shape...>

---

*<total> tools this run. Nothing here is investment advice.*
```

Rules for the body:

- Every tool is a `### [Name](URL)` link, the description, then **Pricing:** as the **last** thing
  in the paragraph. **Name the free-tier cap in it** — "free tier: 25 calls/day, end-of-day only"
  beats "freemium".
- No `**Replaces:**` clause. Put the entry point in the sentence (`pip install`, "one REST endpoint",
  "self-host with Docker", "official Python + Go SDKs").
- Link the thing itself, never a blog post. Leading emoji on each `##`, bucket text exactly as above.
- **No advice, no forecasts, no performance claims.** This is the one content rule that is not
  stylistic.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: finance marketing copy is the most homogenous prose on the internet — every
provider is "institutional-grade", every library "production-ready", every fintech "democratizing
access to". Lead with the coverage, the install line, the licence, the constraint.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"structured flow"** — layered strata, routed channels, stacked bars and branching
conduits reading as value moving through a system. Fixed palette: **deep forest green, brass gold,
slate navy, off-white**.

Dangerous nouns for this digest: "stock chart", "candlestick", "ticker tape", "trading terminal",
"dollar sign", "coin", "bank", "bull", "logo". **No numerals at all** — a rendered "+14.2%" on a
finance cover reads as a claim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Finance Toolkit — <Month D, YYYY>",
  "slug": "finance-toolkit",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
