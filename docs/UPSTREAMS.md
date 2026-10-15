<h1 align="center">🌐 Upstreams</h1>

<p align="center">
  <em>Every agent CLI, API and runtime the recipes depend on, what the code assumes about each, and where to check that it still holds.</em>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/↩-docs_home-6B7280?style=for-the-badge" alt="Docs home"></a>
</p>

---

The weekly **AI Recipes CLI Upstream Check** routine works from this file and opens
`upstream/auto-*` PRs. Keep it current by hand too: a new CLI profile is a new row.

**Last checked** is filled in only with a date the source was actually read. `—` means never.

## Agent CLIs

Each CLI is one profile in [`core/engines/clis/`](../core/engines/clis/README.md). A profile
fact (a flag, the prompt mode, the output shape, the skills folder) lives **only** in that
file; `python scripts/check_clis.py <name>` checks every flag against the installed CLI's
`--help`. A changed profile changes the runtime bundle, so the same PR bumps `VERSION` and
reruns `scripts/build_registry.py`.

| Upstream | What the profile assumes | Profile | Check at | Last checked |
|:---|:---|:---|:---|:---|
| **Claude Code** (`claude`) | `--print --output-format json --permission-mode dontAsk --allowedTools`; prompt on stdin; one JSON result with `result`, `is_error`, `subtype`, `modelUsage`; skills in `.claude/skills` | [`claude.json`](../core/engines/clis/claude.json) | code.claude.com/docs/en/cli-reference; github.com/anthropics/claude-code `CHANGELOG.md` | 2026-10-14 |
| **Codex CLI** (`codex`) | `exec --json --ephemeral --skip-git-repo-check -s workspace-write -C`; prompt on stdin (`-`); JSONL events, final message is the last `item.completed` `agent_message`; skills in `.agents/skills` | [`codex.json`](../core/engines/clis/codex.json) | developers.openai.com/codex/cli/reference; github.com/openai/codex/releases | 2026-10-14 |
| **Gemini CLI** (`gemini`) | `-p "" -o json --approval-mode yolo --skip-trust`; prompt on stdin; one JSON object with `response`, `error`, `stats.models`; skills in `.gemini/skills` | [`gemini.json`](../core/engines/clis/gemini.json) | geminicli.com/docs/cli/headless/; github.com/google-gemini/gemini-cli/releases | 2026-10-14 |
| **OpenCode** (`opencode run`) | `--auto --format json --dir -f <file>`; prompt as an attached file; JSONL events, final text is the last `type: text` event's `part.text` | [`opencode.json`](../core/engines/clis/opencode.json) | opencode.ai/docs/cli/; github.com/anomalyco/opencode/releases | 2026-10-14 |
| **Kimi Code** (`kimi`) | `-p <prompt> --output-format stream-json`; prompt mode refuses `--yolo`/`--auto`; JSONL, final text is the last `role: assistant` line's `content` | [`kimi.json`](../core/engines/clis/kimi.json) | moonshotai.github.io/kimi-code/ | 2026-10-14 |
| **Grok Build** (`grok`) | `--prompt-file --output-format plain --always-approve --cwd`; plain text output | [`grok.json`](../core/engines/clis/grok.json) | docs.x.ai | 2026-10-14 (help text only) |
| **Antigravity** (`agy`) | *No profile.* `agy --print=<prompt>` hung with no output in a headless test on 2026-10-14 | — | antigravity.google/docs | 2026-10-14 |

## Media APIs

| Upstream | What the code assumes | Code | Check at | Last checked |
|:---|:---|:---|:---|:---|
| **Gemini image + TTS** | `google-genai` SDK; image model `gemini-3.1-flash-image`; preset TTS voices | `core/images/`, `core/audio/` | ai.google.dev/gemini-api/docs/changelog | — |
| **OpenAI images** | `openai` SDK image generation as the fallback cover engine | `core/images/` | platform.openai.com/docs/changelog | — |
| **ElevenLabs music + speech** | Music v2.5 and TTS endpoints | `core/audio/` | elevenlabs.io/docs/changelog | — |

## Platform

| Upstream | What the code assumes | Code | Check at | Last checked |
|:---|:---|:---|:---|:---|
| **Cronsole Registry v1** | `action: {kind: script, interpreter: python, body}` templates for `cronsole-native`; `{{param}}` pasted raw; `${secret.NAME?}` optional secrets and `execution.timeoutSec` honoured (cronsole PR #323); 60-minute native cap; first 2,000 characters of output kept | `scripts/build_registry.py`, `cronsole/native-body.py` | github.com/ai-automation-tools/cronsole `docs/` and `CHANGELOG.md` | 2026-10-14 |
| **Python** | 3.10+ for the runner; the Cronsole edition runs as `python` | everywhere | python.org/downloads | — |

---

<p align="center">
  <a href="README.md">← Docs home</a> ·
  <a href="ARCHITECTURE.md">Architecture →</a>
</p>
