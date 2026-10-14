# Finance App Prototype

Goal: build ONE runnable app prototype in **personal / consumer finance** — an everyday money tool a
regular person would actually open and use — plus the description of a cover.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Theme: `{{THEME}}`** — chosen by the runner to keep the catalogue balanced. {{THEME_GUIDE}}

You may add ONE secondary theme if the idea genuinely spans two (e.g. `Rewards + Discounts`) — never
more. The primary stays `{{THEME}}`.

**Ideas already built** (date · slug · title — pitch). Don't repeat one:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research** with **WebSearch** (and **WebFetch** to read sources):
   - current rates and products where relevant — high-yield-savings APYs, card welcome bonuses and
     category multipliers, loan APRs, this year's IRA/401(k) contribution limits. Use `after:` /
     `before:` qualifiers: last 90 days for rates and offers, the current tax year for limits;
   - real pain points and popular approaches — r/personalfinance, r/churning, r/Frugal, Bogleheads,
     NerdWallet / Investopedia explainers, The Points Guy for redemption values.
2. **Choose the idea.** Genuinely useful to someone managing their own money; runnable with **no real
   accounts, logins, or API keys** (synthetic local data only); not a duplicate of anything listed
   above; with a stated, credible benefit — dollars saved or earned a year, hours saved, a decision
   made clearer, a habit made easier.
3. **Load the writing skills** (below) and write `README.md` and `requirements.md`.
4. **Build the app**: `index.html`, `style.css`, `script.js`, `sample-data.json`.
5. **Load `image-prompt-craft`** and write the cover description into `cover_prompt`.
6. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write the README and requirements, and run
`humanizer`'s final pass on both.** Money writing has its own slop dialect — the personal-finance-blog
voice that sounds authoritative and says nothing.

Carve-outs, because those skills were written for interactive editing:

- **Ignore their workflow and output instructions** — no audit, no report, no questions.
- **The OUTPUT FORMAT below wins on structure.** The skills apply to the sentences inside it.
- **Never invent a number to sound credible.** "Experts recommend", "studies show", "the average
  American spends" — cite a Sources entry or drop the claim. This is the one domain where a reader
  might act on it.

Specific beats confident: the actual formula, the actual fee it dodges, the case where it doesn't work.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `README.md`

```markdown
# <Idea Display Name>

> <one-line pitch — what it does and who it's for>

**Date**: {{DATE}}
**Theme**: {{THEME}}[ + <Secondary>]
**Status**: Prototype

## What it is
<2–3 sentences, plain English.>

## Who it serves
<Primary persona, e.g. "someone paying down three credit cards who wants a clear payoff order".>

## The money problem it addresses
<The real friction — untracked subscriptions, unclaimed welcome bonuses, high fund fees, an emergency
fund with no plan — and how this changes it.>

## How it works
<The screens and the interactive flow.>

## What's in this folder
<Each file and what it holds.>

## How to run it
Open `index.html` in any modern browser.

## Estimated impact
<Honest and specific, with the assumption shown, e.g. "Cuts fund fees ~$1,100 over 10 years on a
$50k balance at 0.25% vs 0.03%".>

## Good to know
<One short paragraph: an organizer/estimator, not personalized financial, investment, or tax advice;
rates and offers change; verify current numbers before acting.>

## Sources
- <full URL> — <what it grounded>
```

### `requirements.md`

Goals · Primary user · Functional requirements (FR1… 8–15) · User stories (5–10) · Non-functional
requirements · Out of scope · Open questions. Bulleted, unambiguous, testable.

### `index.html` · `style.css` · `script.js` · `sample-data.json`

- The app demonstrates the core flow a real user touches — enter numbers and see a result, compare
  options, track goals, walk a payoff plan, pick the best card per purchase.
- **Runs from `file://`.** Put the sample data in an inline
  `<script type="application/json" id="sample-data">` block that `script.js` reads, and ship the same
  data as `sample-data.json` (8–25 realistic, **synthetic** records — no real people, no real account
  numbers).
- Vanilla JS; one HTTPS-CDN library only if genuinely needed (e.g. Chart.js). All math runs
  client-side; nothing leaves the browser.
- **Money math in integer cents** — never binary floats for currency.
- Every local file the page references must exist.

Rules:

- Correct vocabulary: APY vs APR, expense ratio, avalanche vs snowball, welcome bonus vs spend
  threshold, tax-advantaged vs taxable. Verify any rule or limit that might have changed before
  stating it.
- Every rate, limit, offer or statistic comes from a cited source. Never fabricate numbers.
- Educational, tool-first framing. Never tell the user to buy a specific security.
- Exact dates and years — never "this year".

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single concept-art illustration capturing the idea **metaphorically** —
reward optimizer → a fanned deck of glowing cards funnelling into a coin; emergency fund → an umbrella
sheltering a growing stack of coins; debt avalanche → descending stair-steps of coins melting away.
Follow `image-prompt-craft`'s formula; these rules win where they differ:

- Modern editorial-tech illustration: soft gradients, smooth shapes, subtle depth.
- Palette tilted toward money and trust: deep green, emerald, a gold/amber accent, slate, with teal
  or navy support.
- Subject centered or slightly above, with breathing room; the scene runs **full-bleed** — no inset
  panel, card or frame. The runner renders 16:9 — don't put the ratio in the prompt.
- **Forbidden:** any text, numbers, or currency symbols as glyphs; logos, real bank/card/company
  names or trade dress; screenshots, app mockups, charts, device frames; recognisable people.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Idea Display Name>",
  "slug": "<kebab-case-slug, max 6 words>",
  "summary": "<the one-line pitch>",
  "theme": "{{THEME}}",
  "secondary_theme": "<a second theme, or null>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
