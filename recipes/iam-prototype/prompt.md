# IAM App Prototype

Goal: build ONE runnable app prototype for **identity and access management** — a tool an IAM
engineer, access reviewer, GRC analyst or ordinary employee would actually open — plus the
description of a cover.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Pain area: `{{AREA}}`** — chosen by the runner to keep the catalogue balanced. {{AREA_GUIDE}}

Assume a large identity estate: tens of thousands of identities, hundreds of connected
applications, a long tail of odd systems. The small case is the rare case. You may add ONE
secondary area if the idea genuinely spans two (e.g. `lifecycle + privileged`); the primary stays
`{{AREA}}`.

**Vendor-neutral.** The prototype speaks the generic vocabulary of identity governance and access
management: identities, accounts, entitlements, roles, access requests, approvals, certifications,
separation of duties, joiner / mover / leaver, privileged access, SSO and MFA, and the open
standards (SCIM, OIDC, SAML, OAuth). Name a product only in `## Sources` when a fetched page from
its documentation grounded a claim. Never build the tool *for* one vendor's platform.

**Ideas already built** (date · slug · title — pitch). Don't repeat one:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research** with **WebSearch** (and **WebFetch** to read sources):
   - what practitioners are complaining about in this area right now — community forums, vendor
     documentation, conference talks, release notes, NIST and CISA guidance. Constrain with
     `after:` / `before:` for the last 90 days where recency matters;
   - the standards and reference behaviour the idea leans on, read from the page that defines it.
2. **Choose the idea.** Genuinely useful to someone who runs or lives inside an access program;
   runnable with **no real directory, no logins, no API keys** (synthetic local data only); not a
   duplicate of anything listed above; with a stated, credible benefit — hours saved a week,
   decisions made faster, a control that becomes provable.
3. **Load the writing skills** (below) and write `README.md` and `requirements.md`.
4. **Build the app**: `index.html`, `style.css`, `script.js`, `sample-data.json`.
5. **Load `image-prompt-craft`** and write the cover description into `cover_prompt`.
6. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## GROUNDING

A citation is a promise that you opened the thing. Every `## Sources` entry is a public URL you
fetched during this run. If you cannot confirm a platform behaviour from a page you read, either
leave it out or say in the README that it is a design assumption. Never cite a local path or a
document you did not open. Do not name a real customer or a non-public vulnerability detail.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write the README and requirements, and run
`humanizer`'s final pass on both.** The reader is a practitioner who spots vendor-brochure language
instantly and stops reading.

Carve-outs, because those skills were written for interactive editing:

- **Ignore their workflow and output instructions** — no audit, no report, no questions.
- **The OUTPUT FORMAT below wins on structure.** The skills apply to the sentences inside it.
- **Vendor-speak has a specific tell here:** "industry best practice suggests", "most organizations
  struggle with", "could potentially reduce manual effort". Cite a source, put a number in
  *Estimated impact*, or say plainly that you don't have one.

A practitioner trusts specifics: the connector count, the actual failure mode, the step that still
needs a human.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `README.md`

```markdown
# <Idea Display Name>

> <one-line pitch — what it does and who it's for>

**Date**: {{DATE}}
**Area**: {{AREA}}[ + <secondary>]
**Status**: Prototype

## What it is
<2–3 sentences, plain English.>

## Who it serves
<Primary persona, e.g. "an IAM engineer triaging weekly aggregation failures", "a manager with
forty certification items due Friday".>

## The access pain it addresses
<Be specific. Name the object or process — the certification campaign, the lifecycle event, the
provisioning request, the role definition. What is broken or expensive today, and how this changes
it.>

## How it works
<The screens and the interactive flow.>

## What's in this folder
<Each file and what it holds.>

## How to run it
Open `index.html` in any modern browser.

## Estimated impact
<Honest and specific, with the assumption shown, e.g. "Cuts certifier follow-up by about six hours
a week on a 2,000-item campaign by flagging decisions stalled more than five days".>

## Why it fits a large identity estate
<One short paragraph: how it holds up at tens of thousands of identities and hundreds of
applications, and what still needs a human.>

## Design assumptions
<Platform behaviour the idea depends on that you could not confirm from a fetched page, one line
each, or "None".>

## Sources
- <full URL> — <what it grounded>
```

### `requirements.md`

Goals · Primary user · Functional requirements (FR1… 8–15) · User stories (5–10) · Non-functional
requirements · Out of scope · Open questions. Bulleted, unambiguous, testable.

### `index.html` · `style.css` · `script.js` · `sample-data.json`

- The app demonstrates the core flow an operator or end user would touch — search and filter
  identities, walk a certification, trace a lifecycle event, simulate an approval step, rank role
  candidates, review a break-glass log.
- **Runs from `file://`.** Put the sample data in an inline
  `<script type="application/json" id="sample-data">` block that `script.js` reads, and ship the same
  data as `sample-data.json` (8–25 realistic, **synthetic** records — invented people, invented
  applications, no real employee names, no real account identifiers).
- Vanilla JS; one HTTPS-CDN library only if genuinely needed (e.g. Chart.js). Nothing leaves the
  browser.
- Every local file the page references must exist.

Rules:

- Correct vocabulary: entitlement vs role, account vs identity, certification vs attestation,
  SoD vs least privilege, SCIM vs just-in-time provisioning. Verify any standard's behaviour on the
  page that defines it before stating it.
- Every statistic or rule comes from a cited source. Never fabricate numbers.
- Exact dates and years — never "this quarter".

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single concept-art illustration capturing the idea **metaphorically** —
orphaned-account sweeper → a lone key on a sorting tray; certification velocity → a stopwatch over a
stack of checklists; lifecycle tracer → a glowing footprint trail through a doorway; SoD bridge →
two interlocking gears with a shield between them. Follow `image-prompt-craft`'s formula; these
rules win where they differ:

- Modern editorial-tech illustration: soft gradients, clean vector-influenced shapes, subtle depth.
- Palette tilted toward security: deep navy, slate, electric blue, an accent of teal or amber.
- Subject centered or slightly above, with breathing room; the scene runs **full-bleed** — no inset
  panel, card or frame. The runner renders 16:9 — don't put the ratio in the prompt.
- **Forbidden:** any text, numbers or glyphs; logos, real product UIs or company marks; screenshots,
  app mockups, charts, device frames; recognisable people (stylised hands or silhouettes are fine
  if subordinate to the concept); violent or political imagery.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Idea Display Name>",
  "slug": "<kebab-case-slug, max 6 words>",
  "summary": "<the one-line pitch>",
  "iam_area": "{{AREA}}",
  "secondary_area": "<a second area, or null>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
