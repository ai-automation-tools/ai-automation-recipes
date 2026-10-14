# Security Toolkit

[← All recipes](../../README.md)

A monthly haul of **24+ security tools** — identity and access, offensive and recon, detection and response, OSINT, privacy, AppSec and supply chain, cloud, security AI, and labs. Licences are named when they aren't plainly open source. **Tools, not targets:** no weaponized PoCs, no named third-party targets, no intrusion how-tos; offensive tooling is framed for systems you own or are authorized to test.

| | |
|:---|:---|
| **Output** | `security-toolkit/<YYYY-MM>/<date>_security-toolkit/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Schedule** | Monthly, the 28th, 12:30 UTC |
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
python recipes/security-toolkit/run.py --output-dir ~/ai-output
```
