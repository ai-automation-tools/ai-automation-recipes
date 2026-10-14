# Cool Websites

Goal: research and write a roundup of **at least 28 genuinely cool, useful, lesser-known websites**,
organized by category, plus a cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## ALREADY FEATURED — DO NOT REPEAT

Every site earlier runs listed (date · name — URL). Match on name and root domain — except GitHub
repos, which match on the full `github.com/<owner>/<repo>` path (otherwise every repo after the first
would count as a repeat):

{{FEATURED}}

No carve-out: this roundup stays fresh every run.

--------------------------------------------------
## RESEARCH

Good source lists to mine for candidates, then go beyond them:

- https://github.com/atakanaltok/awesome-useful-websites and other `awesome-*` lists
- https://www.labnol.org/internet/101-useful-websites/18078
- r/InternetIsBeautiful, r/coolgithubprojects, r/selfhosted; Show HN; Product Hunt
- For 3D: https://github.com/ad-si/awesome-3d-printing, `awesome-cad`, GitHub topics `3d-printing` /
  `openscad` / `cad`, r/3Dprinting, r/functionalprint, r/openscad

**What earns a slot:**

- **Genuinely cool or useful, ideally lesser-known.** Hidden gems over mega-sites — skip Google,
  Wikipedia, YouTube, Canva and the like.
- **Free, or a meaningful free tier**, wherever possible — note it when a site is paid or freemium.
- **Safe for work and legal to link.** Security and OSINT tools that demonstrate exposure (public
  cameras, metadata viewers) are fine with a short caution; nothing whose main purpose is illegal.

--------------------------------------------------
## CATEGORIES

**8–12 categories, 2–4 sites each, at least 28 in total** (aim for 28–35). Rotate so runs feel
different; add a sensible new category when one fits.

- **Security & Privacy** — encrypted notes and sharing, anonymity tools, privacy checkers.
  *Always include at least one category from the security / privacy / OSINT family.*
- **3D Modeling & Printing** — model repositories, browser CAD, slicers, mesh/STL tools, parametric
  libraries, and **GitHub repos** (OpenSCAD libraries, slicer forks, firmware, generators). *Always
  include it, 2–4 entries, at least one GitHub repo.* Skip the defaults everyone knows (Thingiverse,
  Printables, Tinkercad, Cura, PrusaSlicer, Blender) and aim one step past them.
- **OSINT & Investigation** — recon, asset lookup, metadata, geolocation, maritime/flight tracking
- **Cyber / Hacking Tools** — CTF, recon, analysis, learning labs
- **IT & Sysadmin Tools** — networking, DNS, diagnostics, conversion, regex, cron
- **AI Tools** — useful AI utilities beyond the big chatbots
- **Video & Image Tools** — editing, conversion, background removal, compression, stock
- **Developer Tools** — APIs, playgrounds, generators, docs
- **Windows Software** — free and portable utilities, install managers
- **Open Source Software** — notable self-hostable or FOSS projects
- **Productivity & Collaboration** — notes, whiteboards, scheduling, file transfer
- **Learning & Reference** — courses, interactive explainers, docs
- **Games** — browser games, indie gems, puzzle and typing games
- **Travel** — flight deals, maps, planning, visa and timezone tools
- **Money & Finance** — calculators, trackers, deal finders
- **Fun / Weird Internet** — the oddly satisfying and the delightful

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Cool Websites — <Month D, YYYY>"
date: {{DATE}}
type: cool-websites
site_count: <number of sites listed>
categories: [<the category names you used>]
tags: [cool-websites, web, tools, security, privacy, 3d-printing]
---

# Cool Websites — <Month D, YYYY>

> <One sentence: a fresh batch of N hand-picked, genuinely useful corners of the internet.>

## 🔐 Security & Privacy

### [<Site Name>](<https URL>)
<1–2 sentences: what it is, and the cool or useful part.>

<...every category, every site in the same shape...>

---

*<total> sites this run.*
```

Rules for the body:

- Every site is a `### [Name](URL)` link followed by a 1–2 sentence description. Concrete and
  specific — what it does and the cool part — never marketing fluff.
- A leading emoji on each `##` category heading. Don't number sites; don't repeat one within the run.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: thirty back-to-back blurbs is the easiest place to sound like a machine. If twenty
descriptions open "A free tool that lets you…", the list reads as generated even when every line is
clean. The best description names the one thing this site does that its competitors don't, and stops.

--------------------------------------------------
## COVER IMAGE

Motif: a sleek **"cool corners of the internet"** collage — a dark hacker-tech aesthetic, a globe /
network motif, abstract glowing rectangles and connection lines. Fixed palette: **near-black, neon
green, cyan, off-white**.

Dangerous nouns for this digest: "browser window", "UI", "tab bar", "address bar", "icon", "tool
glyph". Ask for abstract glowing rectangles and network nodes instead of browser chrome.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Cool Websites — <Month D, YYYY>",
  "slug": "cool-websites",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
