# Podcast Script

Goal: write one entertaining **AI-vs-AI debate podcast** episode as a speaker-labelled transcript
that the `weekly-audio-podcast` recipe can render to audio — plus a square cover description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Topic:** {{TOPIC}}

**Episodes already scripted** (date · slug · title — description). Don't repeat a topic:

{{EXISTING}}

--------------------------------------------------
## THE CAST

{{CAST}}

--------------------------------------------------
## WRITE THE EPISODE

A back-and-forth transcript using the host plus every guest above:

- The host opens with a punchy intro, names the topic, and introduces each guest by name and
  personality angle.
- **Each guest speaks at least 4 times and at most 7 times**, fully in character: their voice,
  slang, vocabulary, beliefs, mannerisms and quirks. Don't make anyone say what their card forbids.
- The host moderates: pointed questions, baited conflict, jokes, chat/audience references, called-out
  contradictions, pivots between angles.
- **Real back-and-forth** — interruptions, callbacks to earlier lines, direct disagreement — not
  stacked monologues.
- Cover at least three angles of the topic. End with a 1–3 line host wrap.
- **Length: 1,500–3,000 words.** Funny, unique and true to each persona.
- **No real people.** Every speaker is fictional; nobody impersonates or is named after a real
  living person. Guests may *mention* public figures in passing only as the topic requires.
- Parentheticals like `(whispers)` or `(laughs)` are fine — the render keeps them. No narrator or
  stage-direction lines outside the speaker blocks.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `script.md` — exact structure (the audio render parses it)

```markdown
# <Topic Title>

**Date**: {{DATE}}
**Host**: <Host display name>
**Cast**: <comma-separated guest display names>

## Topic Description

<one paragraph framing the topic and its angles>

## Script

### <Host Display Name>

<opening lines>

### <Guest Display Name>

<line>

### <Host Display Name>

<next line>
```

Every turn is a `### <Speaker>` heading followed by that speaker's lines. Use each speaker's name
**identically** every time.

{{CAST_FILE}}

--------------------------------------------------
## COVER IMAGE

Load `image-prompt-craft`. `cover_prompt` describes a square podcast-cover illustration that
captures the topic metaphorically — a bold central motif, a studio-microphone or broadcast feel
only if it helps, a 3–4 colour palette. **No text, no logos, no real people's likenesses**; the
cast may appear as clearly fictional stylised cartoon figures. End with the skill's constraint
block.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Topic Title>",
  "slug": "<kebab-case-topic-slug>",
  "summary": "<one-sentence episode description>",
  "topic": "<Topic Title>",
  "host": "<Host display name>",
  "cast": ["<guest>", "<guest>"],
  "word_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
