# Prompt Patterns by Artifact Type

Patterns for the image types these automations produce. Each names the framing that works, the
trap to avoid, and the usual aspect ratio — passed as `--aspect`, never written in the prompt.

---

## Concept-art cover (app cards, game concepts, ideas, articles)

**Aspect:** `16:9` or `2:3` depending on the job.

Ask for **a single concept-art illustration of the central idea**, not a depiction of the product.
The strongest covers are one clear metaphor with room to breathe.

- Frame it as *"concept-art illustration of…"* — never *"a poster for…"*, *"an app icon"*, or *"a UI mockup"*, all of which drag in text and chrome.
- One focal subject, centred, with generous negative space.
- Avoid rendering screens, dashboards, or interfaces: they come back as garbled fake UI. If the idea is software, show the *metaphor*, not the app.
- Full constraint block.

---

## Illustrated portrait (personas, characters)

**Aspect:** `2:3`.

**Both of these are mandatory** — see `failure-modes.md` #2–#4:

1. The subject's **real name**, unsubstituted.
2. An **explicit physical description** — skin tone/ethnicity, hair, build, age, one or two distinguishing features.

Then: *stylized illustrated hero portrait, head-and-shoulders, face clearly visible and centred,
bold characterful comic/poster-art aesthetic (not photorealistic), dramatic lighting, background
that fits their vibe.*

- **Never** the words "trading card," "poster," "silhouette," or "faceless."
- Constraint block must forbid text **and** invented names **and** obscured faces.

---

## Editorial / mock-photojournalism (satirical news)

**Aspect:** varies.

*Polished editorial illustration / cinematic mock-photojournalism: believable-looking news imagery of
an absurd scene.* The comedy comes from playing an impossible situation completely straight — the
style should be sober, the content ridiculous.

- No real logos, no identifiable private individuals.
- No readable body text. A stylized masthead *feel* is acceptable; small body text always garbles.
- Constraint block, and keep the scene single-focus — crowded satirical scenes read as noise.

---

## Key art (game concepts)

**Aspect:** `16:9`.

*Key art* is the right noun — it means a hero illustration, not a box cover, so it doesn't invite a
title treatment. Name the genre, the world, the mood, and one hero element (character, vehicle,
landmark). Cinematic lighting, strong silhouette reading at thumbnail size.

- Never "box art," "Steam capsule," or "game poster" — all carry titles and logos.

---

## Scene illustration inside a story (alt-history, novella)

**Aspect:** typically `16:9`.

The trap is continuity: **the model remembers nothing between calls.** Re-state the same character
and setting description in every scene prompt, verbatim, or the protagonist changes appearance
between images.

- Reuse the style and palette clauses **exactly**.
- Vary only the moment depicted, the composition, and the light.
- Keep scenes wordless — no captions, no speech, no signage.

---

## Album cover (song jobs)

**Aspect:** `1:1`.

Capture the song's **emotional theme**, not its lyrics literally. Abstract or symbolic reads better
than illustrating a verse.

- **Never** "album cover" as the noun — it invites band-name and title text. Ask for *"a square
  illustration capturing…"* instead.
- Full constraint block. Real album art has text; the model knows that.

---

## Collage / multi-panel (news collages, montages)

**Aspect:** portrait for daily, landscape for weekly/monthly.

State the **grid explicitly** — "a 6-panel grid, two columns by three rows" — and describe each panel
in one short clause. Then one shared style + palette clause covering all panels.

- Panels drift apart without a shared style clause; state it once, prominently, and apply it to all.
- No panel labels, numbers, or captions.
- Keep each panel's content to a single clear action; six busy panels read as mud.

---

## Meme (daily AI meme) — the text exception

**Aspect:** typically `1:1`.

This is the one job that **wants** text baked in.

- Quote the caption **exactly** and require that spelling.
- Keep it to **one short line**, rendered **large** at top or bottom. Small text garbles.
- Classic meme framing: one clear subject, readable at thumbnail size.
- **Verify the spelling by eye** before committing — this is the highest-risk render of the lot.
- Everything *except* the caption still gets the constraint block: no watermarks, no extra text.

---

## Wallpaper / abstract (wallpaper packs, cosmic)

**Aspect:** `16:9` desktop, `9:16` mobile.

Composition matters more than subject: keep the centre relatively calm so desktop icons and phone
widgets stay legible. Say so — *"visual interest toward the edges, calm uncluttered centre."*

- Name the palette precisely; wallpapers live or die on colour.
- No focal subject demanding attention, no text, no borders or frames.
- ⚠️ Mobile 9:16 in the wallpaper pack is **image-to-image** from the desktop render — that path is
  SDK-only. See `engines.md`.

---

## Icon / pack (icon packs, image packs)

**Aspect:** `1:1`.

Consistency is the entire deliverable. One style clause, one palette, repeated **verbatim** across
every icon; vary only the object depicted.

- Say *"centred single object, flat, consistent stroke weight, generous even margins, plain background."*
- No text, no labels, no numbering.
- Uniform margins matter — without asking, sizes drift and the set looks ragged.
