<h1 align="center">🧰 Scripts</h1>

<p align="center">
  <em>Builders for the registry and the viewer, and the scan that runs before anything is published.</em>
</p>

<p align="center">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-repository_root-6B7280?style=for-the-badge" alt="Repository root"></a>
</p>

---

| Script | What it does |
|:---|:---|
| [**build_registry.py**](build_registry.py) | Rebuilds [`registry/`](../registry/README.md) from every `recipes/*/cronsole.json` and `cronsole/*.json`. Checks each template against Cronsole's rules first. `--check` exits 1 if the committed registry is stale |
| [**build_viewer.py**](build_viewer.py) | Writes `index.html` and `catalog.js` into an output folder: the browsable page for everything the recipes made |
| [**check_public.py**](check_public.py) | Fails on API-key shapes, personal home paths, emails, real IP addresses, and anything on a private denylist kept outside the repo |
| [**build_bundle.py**](build_bundle.py) | Builds the reproducible runtime bundle the Cronsole editions download, and prints its sha256 |
| [**check_clis.py**](check_clis.py) | Checks every CLI profile against the installed CLI: version, and every flag still in its `--help` |
| [**new_cli.py**](new_cli.py) | Drafts a profile for a CLI the repo doesn't know, from its own `--help`, then checks the flags and pings it |
| [**build-diagram.mjs**](build-diagram.mjs) | Builds the [run diagram](../docs/diagrams/README.md) with Archify and copies it into `homepage/diagram/`. `--check` exits 1 when code it cites changed since its pinned commit |

```bash
python scripts/build_registry.py            # after editing any cronsole.json, or anything in the bundle
python scripts/check_clis.py                # after editing a CLI profile
python scripts/new_cli.py <binary>          # draft a profile for a new agent CLI
python scripts/build_viewer.py --serve      # ./output (or $RECIPES_OUTPUT_DIR) at http://localhost:8000
python scripts/check_public.py              # before every commit
```

> [!NOTE]
> `check_public.py` reads a personal denylist from `~/.config/ai-automation-recipes/denylist.txt`
> (or `$RECIPES_DENYLIST`), one regex per line. It lives outside the repo because the list itself is
> the private part.

---

<p align="center">
  <a href="../README.md">← Repository home</a> ·
  <a href="../core/README.md">Core</a> ·
  <a href="../registry/README.md">Next: Registry →</a>
</p>
