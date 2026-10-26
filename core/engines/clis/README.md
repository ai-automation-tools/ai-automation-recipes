<h1 align="center">🔌 CLI profiles</h1>

<p align="center">
  <em>One JSON file per agent CLI. Swap the CLI a recipe runs on with <code>--engine &lt;name&gt;</code>, and add a new CLI without writing code.</em>
</p>

<p align="center">
  <a href="../../README.md"><img src="https://img.shields.io/badge/↩-core-6B7280?style=for-the-badge" alt="Back to core"></a>
</p>

---

A recipe never talks to a CLI. It hands the engine a prompt, a staging folder and a tool list;
`core/engines/cli.py` reads the profile for the chosen CLI and launches it headless. Every
profile here was checked against the CLI's own `--help` on the date in its `verified` block.

| Profile | CLI | Tool list | Live recipe run |
|:---|:---|:---|:---|
| [`claude`](claude.json) | Claude Code | enforced (`--allowedTools`) | ✅ |
| [`codex`](codex.json) | Codex CLI | advisory (sandbox is the boundary) | ✅ short-story, 2026-10-14 |
| [`gemini`](gemini.json) | Gemini CLI | advisory | ✅ short-story, 2026-10-26 (`GEMINI_API_KEY`) |
| [`opencode`](opencode.json) | OpenCode | advisory | ⬜ (answers a smoke prompt) |
| [`kimi`](kimi.json) | Kimi Code | advisory | ⬜ (answers a smoke prompt) |
| [`grok`](grok.json) | Grok Build | advisory | ⬜ (flags checked; needs `XAI_API_KEY` or `grok login`) |
| [`agy`](agy.json) | Antigravity CLI | advisory | ✅ short-story, 2026-10-26 (`GEMINI_API_KEY`) |

**Advisory** means the CLI has no way to limit tools by name, so the recipe's tool list only
reaches the agent through the prompt's contract. Run those CLIs somewhere the staging folder is
the only thing worth protecting.

## Staying current

A CLI renames a flag and every install breaks the same day. So at run time the engine prefers
the copy of its profile on this repo's `main`, fetched once a day into your cache
(`%LOCALAPPDATA%` or `~/.cache`, under `ai-automation-recipes/clis/`). The upstream routine fixes a
profile in one PR and every clone and Cronsole edition picks it up on its next run, with no update.

- A fetched profile is used only if it parses, keeps the same `binary` as the bundled one, and
  isn't older (`verified.checked`). It can change flags and output parsing; it can't swap the
  executable.
- Offline, or a bad fetch, means the bundled profile. A run never fails over this.
- A profile in `RECIPES_CLI_DIR` always wins and is never fetched over.
- `RECIPES_CLI_REMOTE=0` turns the fetch off (CI does); `RECIPES_CLI_URL` points it at a fork.

## Adding a CLI

Let an engine you already have draft it from the new CLI's own `--help`:

```bash
python scripts/new_cli.py <binary>                 # drafted by Claude into this folder
python scripts/new_cli.py <binary> --with codex --out ~/my-clis
```

It checks every flag against the help, sends the CLI a one-line ping through the draft, and prints
the flags it chose for unattended runs. **Read those before scheduling anything**: they decide what
the agent may do with nobody watching. The draft prefers a sandbox or a tool allowlist over a flag
that skips every check.

Or write one by hand: drop a `<name>.json` here, or in any folder on `RECIPES_CLI_DIR` (it wins
over a bundled file of the same name, so you can also override one locally). Then:

```bash
python scripts/check_clis.py <name>          # every flag you pass is in its --help?
python recipes/short-story/run.py --engine <name> --dry-run
python -m unittest discover -s tests          # the profile is complete
```

## Format

| Key | Meaning |
|:---|:---|
| `name`, `label` | Engine id (must match the file name) and display name |
| `binary`, `binaryEnv` | Executable, and an env var that overrides its path |
| `install`, `auth`, `docs` | Shown when the binary is missing; `docs` is where the upstream routine checks for changes |
| `skillsDir` | Where this CLI looks for project skills; the runner stages the recipe's skills there |
| `toolPolicy` | `allowlist` if `toolArgs` really limits tools, else `advisory` |
| `claudeAliases` | `true` only if the CLI understands `sonnet` / `opus` / `haiku`. Otherwise a Claude alias means "your default model" |
| `prompt` | `stdin`, `arg` (put `{prompt}` in `argv`) or `file` (written to `promptFile` in the staging folder, deleted after) |
| `argv` | Arguments after the binary. `{workdir}` `{model}` `{tools}` `{prompt}` `{promptFile}` are filled in; `"@model"` and `"@tools"` splice `modelArgs` / `toolArgs` only when there's a model or tool list to pass |
| `toolsJoin` | Separator for `{tools}` (default `,`) |
| `isolatedHome` | Files (relative path → string or JSON) for a throwaway home the CLI runs in: `HOME` and `USERPROFILE` point there for the run, then it's deleted. For a CLI whose own config (MCP servers, a login, a model override) gets in the way of a headless run (Antigravity) |
| `exitCode` | `ignore` if a non-zero exit with a valid result is still a result (Claude) |
| `output` | How to read what it printed, below |
| `check` | Commands `check_clis.py` runs: `version`, and the `help` pages to search for every flag |
| `verified` | CLI version and date the profile was last checked, and whether a recipe has run on it for real |

`output.format` is one of:

- **`json`**: one object. `text` is the dotted path to the final message; `errors` is a list of
  `{path, truthy: true}` or `{path, not: value}` rules, any of which marks a failed run;
  `errorMessage`, `warnings`, `meta` (name → path) and `model` (`{map, tokens}`: pick the model
  with the most output from a `{model: stats}` map) are optional.
- **`jsonl`**: an event stream. `text: {match, path}` takes the **last** matching event;
  `fail`, `notice` and `usage` are optional `{match, path|message}` rules. `match` compares
  dotted paths to values (`{"type": "item.completed", "item.type": "agent_message"}`).
- **`text`**: stdout is the final message.

Keys starting with `_` are comments. The
[upstream check](../../../docs/UPSTREAMS.md) keeps every profile current.

---

<p align="center">
  <a href="../../README.md">← Core</a> ·
  <a href="../../../docs/ARCHITECTURE.md">Architecture →</a>
</p>
