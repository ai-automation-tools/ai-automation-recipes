<h1 align="center">🧰 Agent Toolkit</h1>

<p align="center">
  <em>24+ things to install into an LLM or coding agent, half proven and half new.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/cover-optional_image_key-F59E0B?style=for-the-badge" alt="Cover needs an image key, optional">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Skills, slash commands, MCP servers, IDE plugins, hooks, loops and harnesses. Every bucket gets one
established pick and one recent arrival, and each entry names its install path in the sentence.

| | |
|:---|:---|
| **Output** | `agent-toolkit/<YYYY-MM>/<date>_agent-toolkit/` → `digest.md`, `cover.png`, `bookmarks.html`, `artifact.json` |
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
full list of entries already featured. An entry can come back after at least 8 weeks, and only if
it has shipped something worth a second look.

## Run it

```bash
python recipes/agent-toolkit/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../ai-stack-radar/README.md">Next: AI Stack Radar →</a>
</p>
