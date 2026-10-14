# Browser Extension

Goal: build ONE browser-extension prototype — a **Manifest V3 extension** that solves a real, current
problem and has a plausible path to money — as two halves of the same idea: a real extension you can
load unpacked in Chrome, and a self-contained demo page that shows it working without installing
anything. Plus the description of a cover.

**Scope guard — this job owns browser extensions and nothing else.** The idea must genuinely need
one: read, change or react to pages the user is already on, live in the toolbar alongside their
browsing, or hook a browser surface (context menu, omnibox, side panel, downloads, tabs) a website
can't reach. If a plain web app would do just as well, pick a different idea.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Extensions already built** (date · slug · title — pitch). Pick a clearly different concept:

{{EXISTING}}

**App prototypes already built** (don't rebuild one of these as an extension):

{{SIBLING_EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research** with **WebSearch** (and **WebFetch**) in the last 30 days: recent launches,
   browser-platform changes (MV3 deprecations, new `chrome.*` APIs, side-panel / omnibox
   capabilities), privacy or regulatory shifts, extensions that were removed or went paid, pain
   points people are actively complaining about.
2. **Choose ONE idea.** It must be timely; **require a browser surface** — name it (content script on
   pages the user visits, toolbar popup, context menu, side panel, omnibox, `chrome.tabs` /
   `chrome.downloads` / `chrome.storage`, `declarativeNetRequest`); have a plausible monetization model
   (freemium, one-time, subscription, team licensing, affiliate, paid sync); be demonstrable from one
   mock page plus a sample-data JSON file; and **stay inside what MV3 allows** — no remotely hosted
   code, no `eval`, a non-persistent service worker. If the real product needs a backend, say so in the
   README and stub it in the demo.
3. **Load the writing skills** (below) and write `README.md` and `requirements.md`.
4. **Build both halves** per THE TWO HALVES and OUTPUT FILES.
5. **Verify both halves** before finishing: `extension/manifest.json` is strict JSON with
   `"manifest_version": 3` and every file it names exists in `extension/`; every permission is one the
   code actually uses (an unused `"<all_urls>"` is the commonest reason a real extension is
   rejected); the demo runs from `index.html` with no build step or keys and actually exercises the
   core loop. The runner re-checks the structure, rejects remote code, and runs `node --check` on
   every script.
6. **Load `image-prompt-craft`** and write the cover description into `cover_prompt`.
7. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## THE TWO HALVES — the demo and the extension share code

`extension/` is a **real MV3 extension**. The harness at the folder root is a **mock browser window**
hosting the same popup so the idea is clickable without installing. They must not be two
implementations of the same UI:

- `index.html` **`<link>`s `extension/popup.css`** — popup styling exists once, in the extension.
  `style.css` styles only the harness: the fake browser chrome, the toolbar, the mock page.
- `index.html` **loads `extension/popup.js`** — the same file the real popup loads — so `popup.js`
  must not assume the extension APIs exist:

  ```js
  const inExtension = typeof chrome !== "undefined" && !!chrome?.storage?.local;

  async function loadState() {
    if (inExtension) return (await chrome.storage.local.get("state")).state ?? {};
    // Demo harness: same shape, from the inline sample data.
    return JSON.parse(document.getElementById("sample-data").textContent).state ?? {};
  }
  ```

  Guard **every** `chrome.*` call this way — `storage`, `tabs`, `runtime.sendMessage`, all of it.
- The popup markup lives in `extension/popup.html`; the harness embeds the same markup in its simulated
  popup panel. If you find yourself writing a second, different popup for the demo, simplify the popup
  until one version serves both.
- `script.js` owns the harness only: render the mock page, wire the toolbar button that opens and
  closes the popup, and stand in for what the content script would do to a real page (highlights,
  badges, banners). Where it stands in for the content script, say so in a short comment.

The harness looks like a browser — title bar, URL bar with a plausible URL for the target site, a
toolbar with the extension's button, the mock page below — and stays restrained.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `README.md` / `requirements.md`, and run
`humanizer`'s final pass over both.** A pitch is where AI writing is worst — unearned superlatives,
*revolutionary / seamless / game-changing*, padded lists, confident demand claims with nothing behind
them. Carve-outs:

- **Ignore their workflow and output instructions** — no audit, no report, no questions.
- **The OUTPUT FORMAT below wins on structure.**
- **Prose only** — never anything under `extension/`, the harness code, the JSON, code comments, or
  the terse spec lines and user stories.
- 🚨 **Keep the honest hedges** — "Why it could be **profitable**", not "why it will be". Cite the
  trend, name the model, say where the demand rationale is thin.
- **Product register yes, marketing copy no.**

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

Optional: `extension/background.js` — only if the concept needs a service worker. Omit it otherwise,
and omit `background` from the manifest too.

### `README.md`

```markdown
# <Extension Display Name>

> <one-line pitch>

**Date**: {{DATE}}
**Form factor**: Browser extension (Manifest V3)
**Browser surface**: <content script | toolbar popup | context menu | side panel | omnibox | declarativeNetRequest | …>
**Status**: Prototype

## What it is
<2–3 sentences.>

## Why it has to be an extension
<The specific browser capability it needs — what it reads, changes or reacts to that a website couldn't.>

## Who it serves
<Primary persona and the specific pain point.>

## Why it could be profitable
<Model and an honest demand rationale, citing the timely trend(s) with at least one URL.>

## How to load it in Chrome
1. Open `chrome://extensions` and turn on **Developer mode**.
2. Click **Load unpacked** and select this folder's `extension/` directory.
3. <Anything else needed to see the core flow.>

## How to try the demo
1. Open `index.html` in any modern browser.
2. <Steps to see the core flow.>

<One sentence on what the demo simulates rather than really does.>

## Permissions, and why each one
| Permission | Why it's needed |
|:--|:--|
| `<permission>` | <the feature that requires it> |

## What's in this prototype
<Which surfaces, interactions and data are implemented; what is stubbed.>

## Roadmap
- <3–5 next features>

## Sources
- <URL> — <what it supports>
- <URL> — <what it supports>
```

### `requirements.md`

Goals · Primary user · Functional requirements (FR1… 8–15) · User stories (5–10) · **Extension
surfaces** (one line per surface and what it does there) · Non-functional requirements (including
permission minimalism) · Out of scope · Open questions.

### `extension/manifest.json`

- Strict JSON: `"manifest_version": 3`, `name`, `version` `"0.1.0"`, `description`.
- `action.default_popup` → `popup.html`.
- `content_scripts` `matches` **as narrow as the concept allows** — a named host or two, not
  `<all_urls>` unless the idea truly applies to every page (and then justify it in the README).
- `permissions` / `host_permissions` limited to what the code calls. No `background` key unless
  `background.js` exists.
- No `content_security_policy` relaxation, no remotely hosted code, no `eval` or `new Function`.
- **No `icons` key** — don't generate icon images; Chrome uses its default badge.

### `extension/popup.html` · `popup.css` · `popup.js` · `content.js`

- `popup.html` is the real popup: a fixed width of 320–420px, a heading, the core control, a compact
  result area. Links `popup.css` and `popup.js` by relative path. No external scripts.
- `popup.js`: vanilla JS, feature-detects `chrome.*` per THE TWO HALVES, works in both hosts.
- `content.js`: vanilla JS doing the real page-side work (read the DOM, inject the badge / banner /
  highlight, message the popup or service worker via `chrome.runtime`). Guard against double
  injection; scope selectors and prefix class names so you don't fight the host page.

### `index.html` · `style.css` · `script.js` · `sample-data.json`

- `index.html`: semantic HTML5 with the mock browser chrome, a stand-in page and the popup panel.
  Links `extension/popup.css` alongside `style.css`; loads `extension/popup.js` and `script.js`.
- **Runs from `file://`:** put the sample data in an inline
  `<script type="application/json" id="sample-data">` block, and ship the same data as
  `sample-data.json` (8–25 realistic records, strict JSON).
- Vanilla JS; HTTPS-CDN libraries only if the demo genuinely needs one. Every local file the page
  references must exist.

Rules: at least two real sources; never fabricate sources, statistics or quotes; exact dates. Product
tone in the README, engineering tone in the requirements; short readable code, commented where the
harness stands in for the real extension. A popup is small: one job per screen.

--------------------------------------------------
## COVER IMAGE

`cover_prompt` describes a single concept-art illustration of the extension's core idea
**metaphorically** — a price-history extension as a stylised tag trailing a faint downward ribbon; a
reading-focus extension as a page with everything but one column softened into fog. Follow
`image-prompt-craft`; these rules win:

- Modern editorial-tech illustration: soft gradients, smooth shapes, subtle depth; a named 3–4 colour
  palette.
- Subject centered or slightly above, with breathing room; full-bleed, no inset panel or frame (the
  runner renders 16:9 — don't write the ratio).
- **Forbidden:** any text, logos, real brands or product UIs, screenshots, app mockups, charts, device
  frames, recognisable people — and **no browser windows, toolbars, address bars, tabs, or
  puzzle-piece extension icons**. The literal picture of an extension is the cliché to avoid.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Extension Display Name>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-line pitch>",
  "browser_surface": "<the surfaces the manifest declares>",
  "permissions": ["<from the manifest>"],
  "monetization": "<the model, in a few words>",
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
