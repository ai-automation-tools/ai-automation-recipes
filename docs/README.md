<a id="docs-top"></a>

<h1 align="center">📚 AI Automation Recipes Documentation</h1>

<p align="center">
  <em>How the recipes run, how to write one, and what's left to build.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/audience-recipe_authors-8B5CF6?style=for-the-badge" alt="Audience: recipe authors">
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/plan-ROADMAP-2ea44f?style=for-the-badge" alt="Roadmap"></a>
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

Start with the root [README](../README.md) if you only want to run a recipe. These pages are for
changing how the recipes work or adding one of your own.

## 🧱 Guides

| Document | What's in it |
|:---|:---|
| [**🧱 Architecture**](ARCHITECTURE.md) | The run loop step by step, the `artifact.json` contract, engines and skills |
| [**🛠️ Adding a recipe**](ADDING-A-RECIPE.md) | The four files a recipe needs, the hooks, and the checks before a PR |
| [**🧭 Diagrams**](diagrams/README.md) | The run-loop diagram the homepage shows: template → runner → agent CLI → checks → media → published folder. Interactive, every node linked to its code, and drift-checked in CI |

## 🗺️ Planning

| Document | What's in it |
|:---|:---|
| [**🗺️ Roadmap**](ROADMAP.md) | Which recipes have had a real run, and the work left to do |
| [**📋 Changelog**](CHANGELOG.md) | Every change since the pilot, newest first |
| [**🌐 Upstreams**](UPSTREAMS.md) | Every agent CLI, API and runtime the recipes depend on, and where to check it |
| [**❓ Open questions**](OPEN-QUESTIONS.md) | Decisions only the maintainer can make, asked by the routines |

## 🔗 Elsewhere in the repo

| Index | What's in it |
|:---|:---|
| [**🍳 Recipes**](../recipes/README.md) | All 48 recipes, grouped, with what each needs |
| [**⚙️ Core**](../core/README.md) | The modules behind the run loop |
| [**📋 Registry**](../registry/README.md) | The Cronsole packs and how to import them |
| [**🤖 AGENTS.md**](../AGENTS.md) | House rules for an AI agent editing this repo (`CLAUDE.md` imports it) |

<p align="right">(<a href="#docs-top">back to top</a>)</p>

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="ARCHITECTURE.md">Next: Architecture →</a>
</p>
