<h1 align="center">📋 Registry</h1>

<p align="center">
  <em>The Cronsole catalog for these recipes, generated, checksummed and ready to import.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/templates-43-8B5CF6?style=for-the-badge" alt="43 templates">
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

## 📦 Packs

| Pack | Holds |
|:---|:---|
| [**ai-recipes**](packs/ai-recipes.json) | All 48 recipes and both helpers |
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

In Cronsole, import a pack file from the Templates tab, then apply a template. Each one asks for the
path to your clone of this repo and an output folder; recipes also offer the Claude model and the
image engine. A recipe can run as a Cronsole-native job (Cronsole runs the command and keeps its
output) or as a Windows scheduled task.

Template schedules are defaults in UTC, so change them to whatever suits you.

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="../scripts/README.md">Scripts</a> ·
  <a href="../tests/README.md">Next: Tests →</a>
</p>
