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

```bash
python scripts/build_registry.py            # after editing any cronsole.json
python scripts/build_viewer.py --output-dir ~/ai-output
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
