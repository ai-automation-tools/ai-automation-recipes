# Cool Websites

[← All recipes](../../README.md)

A monthly roundup of **28+ genuinely useful, lesser-known websites** across 8–12 categories — always a security/privacy/OSINT category and a 3D modeling & printing category (with at least one GitHub repo). Hidden gems over mega-sites; no site ever repeats.

| | |
|:---|:---|
| **Output** | `cool-websites/<YYYY-MM>/<date>_cool-websites/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 18th, 21:30 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only. |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner regenerates `all-bookmarks.html` at the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari (*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and hands the agent the full list of what was already featured.

## Run it

```bash
python recipes/cool-websites/run.py --output-dir ~/ai-output
```
