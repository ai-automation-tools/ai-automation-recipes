# Voiceover Script

Goal: one short, voiceover-ready narration (90–180 seconds, **240–480 words**) about a **real-world
story**, with direction notes, a narrator voice, scene stills for a vertical short, and a cover.
The runner narrates it with text-to-speech and, when ffmpeg is installed, cuts a 9:16 video.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Categories so far** (count of scripts):

{{CATEGORIES}}

**Scripts already written** (date · slug · title — logline). Never repeat a story:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Pick a category.** Reuse one with fewer than ~6 scripts and untouched ground, or start a new
   one — concrete and visually evocative, kebab-case: `business-collapses`, `historical-scams`,
   `survival-stories`, `internet-mysteries`, `failed-startups`, `criminal-capers`,
   `historical-oddities`, `accidental-success`, `expensive-mistakes`, `cyber-crime-stories`,
   `world-changing-inventions`, `dangerous-jobs`, `escape-stories`, `preventable-disasters`,
   `tech-disasters`, `impossible-survivors`…
2. **Pick a specific real-world story** in it — a real company, person or event with verifiable
   facts. Never fabricate a story.
3. **Research it** with **WebSearch** and read promising pages with **WebFetch**. Capture 2–4
   credible primary or authoritative sources with working URLs. Don't rely on memory for dates,
   dollar amounts, names or quotes.
4. Load the writing skills (below) and write `script.md` and `direction-notes.md`.
5. **Choose the narrator.** {{VOICE}}
6. **Describe 4–6 scene stills** for the vertical short — one per beat, in story order — and the
   cover. Load `image-prompt-craft` first.

--------------------------------------------------
## WRITING SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `script.md`, and run `humanizer`'s final pass
on your draft before you write the file.** This script is *performed out loud*: AI cadence a reader
skims past is unmissable in a voice.

- **Ignore their workflow and output instructions** — no audit, no report, no questions.
- **Ignore their document-formatting rules.** The script body is continuous spoken prose.
- **Test by ear, not by eye.** Say each line in your head at ~160 wpm — if your mouth stumbles, so
  will the narrator's.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `script.md`

```markdown
# <Hook Title — short, punchy, no clickbait>

**Category**: <Category Title Case>
**Topic**: <Real Story / Subject in Title Case>
**Length**: <NN seconds> (~<NN> words)

---

<The narration. Plain prose, narrator voice, no stage directions. 240–480 words at ~160 wpm. Open
with a hook in the first sentence; end with a kicker line. Short sentences, hard verbs, present
tense where it lifts the energy. Never invent dialogue or specifics — only facts you can attribute.
Spell out numbers the way they should be spoken where it helps the read.>

---

## Sources

- [Title of source 1](https://...)
- [Title of source 2](https://...)
```

The runner narrates exactly the text between the two `---` lines.

### `direction-notes.md`

```markdown
# Direction Notes — <Hook Title>

## Tone
<2–4 lines describing the voice>

## Pacing
- Target run time: <NN seconds>
- Reading speed: ~160 wpm; slow to ~130 wpm on the kicker
- Beats / pauses: <specific lines that need a beat>

## Emphasis cues
- **<word/phrase>** — why

## B-roll / visual hooks
- <one visual idea per beat>
```

--------------------------------------------------
## IMAGES

**Cover** (`cover_prompt`, rendered 16:9): one concept-art illustration capturing the specific story
metaphorically — e.g. a blood vial cracking against a corporate skyscraper silhouette. Modern
editorial-tech illustration, soft gradients, clean shapes; a 3–4 colour palette matched to the
story's emotional register.

**Scene stills** (`images`, 4–6 entries, each `"aspect": "9:16"`, files `scene-1.png`, `scene-2.png`…):
one per beat of the narration, in order, in the same style and palette as the cover (repeat the
style and palette clauses verbatim in every prompt). Vertical composition, subject in the middle
third.

**Forbidden in every image:** text of any kind, logos or real brand marks, **real human likenesses**
(stylised silhouettes or symbolic stand-ins only), charts, screenshots, device frames, violent or
graphic imagery. End every prompt with the `image-prompt-craft` constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Hook Title>",
  "slug": "<topic-slug, 2–6 kebab-case words>",
  "summary": "<one-line logline>",
  "category": "<category-slug>",
  "topic": "<Real Story / Subject>",
  "word_count": 0,
  "narrator": "<preset voice>",
  "delivery": "<a short delivery note that follows the word 'Say', e.g. 'with low, steady urgency'>",
  "cover_prompt": "<cover description>",
  "images": [
    {"file": "scene-1.png", "prompt": "<scene description>", "aspect": "9:16"}
  ],
  "error": null
}
```
