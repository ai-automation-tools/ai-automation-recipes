<h1 align="center">📋 Registry</h1>

<p align="center">
  <em>The Cronsole catalog for these recipes, generated, checksummed and ready to import.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/templates-98-8B5CF6?style=for-the-badge" alt="98 templates">
  <img src="https://img.shields.io/badge/schema-Registry_v1-0078D4?style=for-the-badge" alt="Registry v1">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

> [!WARNING]
> Don't edit anything in here by hand. Cronsole checks each file's sha256 over its exact bytes, so a
> hand edit or a CRLF conversion breaks the import. Edit `recipes/*/cronsole.json` or `cronsole/*.json`
> and run `python scripts/build_registry.py`.

| Path | What it holds |
|:---|:---|
| [**index.json**](index.json) | Every template and pack, each with its path and sha256 |
| [**templates/**](templates/) | One Registry v1 template per recipe, plus the two helpers |
| [**packs/**](packs/) | Importable bundles: everything, or one recipe group |

## 🌐 Where it's published

The Homepage workflow publishes `index.json`, `templates/` and `packs/` beside the homepage at
`https://ai-automation-recipes.ai-automation-tools.dev/registry/`. The
[Cronsole gallery](https://cronsole.ai-automation-tools.dev/#/collection/ai-recipes) reads the catalog
from there, so a merge to `main` that changes `registry/` shows up in the gallery with no Cronsole
release. The workflow waits until the runtime release for `VERSION` exists before it publishes. The
daily *Registry drift* workflow (`scripts/check_registry_published.py`) fails if the hosted copy stops
matching `main`. Each recipe README links to its own templates in the gallery.

## 📦 Packs

| Pack | Holds |
|:---|:---|
| [**ai-recipes**](packs/ai-recipes.json) | All 48 recipes and both helpers |
| [**ai-recipes-cronsole**](packs/ai-recipes-cronsole.json) | The Cronsole edition of every recipe: no clone, no `.env` |
| [**ai-recipes-apps-games**](packs/ai-recipes-apps-games.json) | The 9 apps and games recipes |
| [**ai-recipes-writing**](packs/ai-recipes-writing.json) | The 8 writing recipes |
| [**ai-recipes-food-maps**](packs/ai-recipes-food-maps.json) | The 4 food and map recipes |
| [**ai-recipes-digests**](packs/ai-recipes-digests.json) | The 12 research digests and briefings |
| [**ai-recipes-images**](packs/ai-recipes-images.json) | The 9 image recipes |
| [**ai-recipes-audio**](packs/ai-recipes-audio.json) | The 4 audio recipes |
| [**ai-recipes-repo-ops**](packs/ai-recipes-repo-ops.json) | The 2 repo automations, report-only by default |

Every pack carries the two helper templates, which live in [`cronsole/`](../cronsole/) rather than
in a recipe folder: **AI Recipes: Update Clone** (`git pull --ff-only` on your clone) and **AI
Recipes: Rebuild Viewer**.

## 📥 Importing

Download a pack or template from the
[Cronsole gallery](https://cronsole.ai-automation-tools.dev/#/collection/ai-recipes) (or from
`packs/` here), import it in Cronsole's Templates tab, then apply a template. A clone edition asks
for the path to your clone of this repo and an output folder; recipes also offer the Claude model and the
image engine. A recipe can run as a Cronsole-native job (Cronsole runs the command and keeps its
output) or as a Windows scheduled task.

Template schedules are defaults in UTC, so change them to whatever suits you.

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="../scripts/README.md">Scripts</a> ·
  <a href="../tests/README.md">Next: Tests →</a>
</p>
