<h1 align="center">🛡️ Security Toolkit</h1>

<p align="center">
  <em>24+ security tools across identity, detection, recon, AppSec, cloud and labs, with licenses named.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Buckets cover identity and access, offensive and recon, detection and response, OSINT, privacy,
AppSec and supply chain, cloud, security AI, and labs. A license is named whenever it isn't plainly
open source. The rule is tools, not targets: no weaponized PoCs, no named third-party targets, no
intrusion how-tos, and offensive tooling is framed for systems you own or are authorized to test.

| | |
|:---|:---|
| **Output** | `security-toolkit/<YYYY-MM>/<date>_security-toolkit/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill, WebSearch, WebFetch |
| **Skills** | `llm-writing`, `humanizer`, `image-prompt-craft` |
| **Network** | Web research only |

## Importable bookmarks

Each run writes `bookmarks.html` next to the digest, and the runner rebuilds `all-bookmarks.html` at
the collection root from every run. Both import into Chrome, Edge, Brave, Firefox or Safari
(*Import bookmarks from HTML file*).

## Not repeating itself

Before each run, the runner reads every earlier digest in the collection and gives the agent the
full list of tools already featured. A tool can come back after at least 6 months, and only if it
has shipped something worth a second look.

## Run it

```bash
python recipes/security-toolkit/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../finance-toolkit/README.md">Next: Finance Toolkit →</a>
</p>
