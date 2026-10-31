# Open questions

Decisions only the maintainer can make. A run adds an entry under **Open**; the maintainer fills
in `- Answer:`; the next run applies it and moves the entry under **Answered**.

## Open

### Move the OpenCode profile to OpenCode 2, or stay on 1.x?

- Asked: 2026-10-31 by ai-recipes-cli-upstream
- Context: OpenCode 2 is released (v2.2.5 on 2026-10-30, https://github.com/anomalyco/opencode/releases)
  and the CLI docs say `opencode upgrade --major` upgrades to 2 and removes 1
  (https://opencode.ai/docs/cli/). The npm `latest` tag of `opencode-ai` is still 1.19.5, which is
  what the profile is verified against (`run --auto --format json --dir -f`, JSONL `type: text`
  events). The v2 CLI page does not list `run`'s flags or its JSON event shape, so nothing in the
  profile is shown to break and nothing is shown to hold. Recommendation: stay on 1.x until
  `opencode-ai@latest` moves to 2.x, then install it, run `python scripts/check_clis.py opencode`
  and a PONG prompt, and fix the profile from what that prints. Decide whether you want that done
  before `latest` moves.
- Answer:

## Answered

