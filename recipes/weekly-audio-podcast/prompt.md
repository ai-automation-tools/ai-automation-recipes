# Audio Podcast — cast the voices

Goal: prepare one finished podcast script for audio. You **cast a preset voice for every speaker**
and write the episode's show notes; the runner then renders the episode with text-to-speech. You
do not change a word of the script.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THE SCRIPT

Rendering: `{{SCRIPT_PATH}}`. Speakers, in order of appearance: {{SPEAKERS}}.

````markdown
{{SCRIPT}}
````

{{CAST_NOTES}}

--------------------------------------------------
## CAST THE VOICES

Speech engine for this run: **{{ENGINE}}**. Pick from these preset voices only — never anything
else:

{{VOICES}}

- Every speaker gets a voice. **No two speakers share one** while there are enough voices to go
  round; if there are more speakers than voices, reuse the voice of the speaker least like them.
- Match the persona: age, energy, gender as written, how they'd sound on a real show. The host
  should be the clearest voice of the set.
- Give each speaker a short **delivery** note the engine reads as direction, phrased to follow the
  word "Say": e.g. `"with deadpan, unhurried confidence"`, `"excitedly, talking fast"`. Keep it to
  tone and pace; don't describe a real person.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `episode.md`

```markdown
# <Episode Title>

**Date**: {{DATE}}
**Host**: <host>
**Cast**: <guests>

## About this episode

<2–3 sentences: what the debate is about and why it's fun to listen to>

## Cast and voices

| Speaker | Voice | Delivery |
|:---|:---|:---|
| <name> | <preset> | <delivery note> |

## Highlights

- <3–5 bullets: the best clashes, callbacks or lines, in your own words>
```

Load `llm-writing` and `humanizer` for the show notes; skip their audit steps.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Episode Title — usually the topic>",
  "slug": "<kebab-case-slug>",
  "summary": "<one-sentence episode description>",
  "voices": {"<Speaker>": "<preset>"},
  "delivery": {"<Speaker>": "<delivery note>"},
  "error": null
}
```

Use the speaker names exactly as they appear in the script.
