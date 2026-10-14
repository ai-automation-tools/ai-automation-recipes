---
name: image-prompt-craft
version: 1.0.0
description: >-
  Write image-generation prompts that produce the picture you actually asked
  for. Covers the prompt formula (subject → style → palette → composition →
  constraints), the negative-constraint block that keeps invented text, stat
  blocks, watermarks and borders out of a render, likeness anchoring for real
  people, the look-at-it-then-regenerate verification loop, and which engine to
  route to (Gemini or OpenAI image models via the recipe's image step).
  Use whenever writing or revising a prompt for a cover, portrait, poster, key
  art, scene illustration, album cover, collage, meme, wallpaper or icon — or
  when a generated image came back with garbled text, a wrong or invented
  subject, a faceless silhouette, or simply not what the prompt said.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Image Prompt Craft

You are not talking to a person. An image model has no idea what you meant, only what you wrote —
and it fills every gap you leave with the most generic thing in its training data.

> **The single most important rule in this skill:** a generative image model **adds what you
> describe, including the frame you describe it in.** Ask for a "trading card" and you get stat
> blocks and edition numbers. Ask for a "movie poster" and you get invented billing-block text. Ask
> for a "book cover" and you get a garbled title. The fix is almost never a stronger prohibition —
> it's naming a different *object*. Ask for a clean illustrated portrait instead.

## When to load which reference

| Need | Reference |
|---|---|
| The known failures and their fixes — text creep, invented names, silhouettes, wrong likeness | [`references/failure-modes.md`](references/failure-modes.md) |
| A recipe for a specific artifact type (cover, portrait, key art, collage, meme, wallpaper…) | [`references/prompt-patterns.md`](references/prompt-patterns.md) |
| Which engine, what it can and can't do, aspect ratios, quotas | [`references/engines.md`](references/engines.md) |

---

## The prompt formula

Write **one continuous descriptive prompt**, in this order. Every element earns its place; vagueness
anywhere is filled in generically.

1. **Subject** — the focal thing, concretely. Not "a developer" but "a woman at a standing desk, lit
   by three monitors."
2. **Style** — the medium and aesthetic. "Flat vector editorial illustration," "1970s airbrushed
   sci-fi paperback art," "cinematic mock-photojournalism." Naming an era or a medium does more work
   than a pile of adjectives.
3. **Palette** — three or four colours, named. "Deep teal, warm amber, off-white, charcoal." This is
   the highest-leverage line in the whole prompt: it's what makes a set of images look like a set.
4. **Composition & lighting** — framing, where the subject sits, negative space, light direction.
   "Centered, head-and-shoulders, generous negative space above, dramatic side lighting."
5. **Mood** — one clause. "Quietly ominous." "Wry and warm."
6. **The constraint block** — see below. Always last, always explicit.

**Length:** aim for 60–120 words. Under 40 and the model improvises; past ~150 it starts dropping
clauses, usually the ones at the end — which is why constraints go last but stay *short*.

## The constraint block

Nearly every artifact these recipes produce wants a **wordless** image. Models add text unbidden — garbled
text, because they can't spell. End the prompt with an explicit block:

> STRICT: no text, letters, words, numbers, captions, titles, labels, banners, credits,
> stat blocks, logos, watermarks, signatures, UI chrome, or borders anywhere in the image.

**This exact sentence is also `core/images/constraints.py`** (`NO_TEXT`). Use the skill's copy when
*you* are writing a prompt; use the constant when **code** appends the constraint. If you change one,
change the other — one canonical wording is the point. (Before it was consolidated, the original
private fleet had drifted to ~25 wordings of this one rule.)

Two things to understand about it:

- **It is a backstop, not the primary fix.** If the prompt describes a poster, a card, a magazine
  cover, a book jacket, an album sleeve, a UI screen, or a diagram, the model will render text no
  matter how emphatic the prohibition. **Change the noun first**, then add the block.
- **Name the specific failure you just saw.** On a regeneration, a generic "no text" is weaker than
  "no stat block, no RANK/AGE fields, no edition number." Call out what actually went wrong.

**When you *do* want text** — a meme caption baked into the image, a stylized single-word headline —
say so explicitly, keep it to a handful of words, and expect to verify spelling by eye. Long or
small text will be garbled; that is not fixable by prompting. See `prompt-patterns.md`.

## Never put these in the prompt text

- **Aspect ratio.** The recipe's image step sets it from the recipe (`1:1`, `2:3`, `16:9`). Writing "16:9" in the prompt body is at best redundant and at worst renders as text.
- **The output path or filename.** The image step handles it.
- **Instructions to the agent** ("save this as…", "use your image tool"). The prompt is the *picture
  description* only.

---

## Verify the render — do not skip this

**An image step exiting 0 means a valid PNG landed on disk. It says nothing about whether the image is
right.** After any successful generation, **open the image and actually look at it.**

Reject and regenerate if:

- there's **any text, lettering, or a number** you didn't ask for;
- the **subject is wrong** — a different person, an invented character, a generic stand-in;
- a person is a **silhouette, faceless, back-turned, or has an obscured face** when you asked for a portrait;
- the **likeness is wrong** — wrong skin tone, ethnicity, gender, age, or a missing defining feature;
- it doesn't match the **palette** you specified (the giveaway that the model ignored the back half of your prompt);
- it's **not the thing you asked for** at all.

**To regenerate:** tighten the prompt — make the subject description more specific and name the exact
problem you saw — then re-run the same image step. **Retry at most twice.**
If it still fails, take the least-bad valid PNG and note the issue in metadata. A clean but
slightly-off image beats a stat card or a silhouette; a missing image fails the run.

---

## Consistency across a set

When one run produces several images — a cover plus inline scenes, a 6-panel collage, a pack —
they must look like one artist made them:

- **Reuse the exact same style and palette clauses, verbatim,** in every prompt of the set. Don't
  paraphrase between images; paraphrase is how a set drifts.
- Vary **only** subject, composition, and lighting.
- Keep recurring characters or objects anchored with the *same* physical description each time —
  models don't remember the previous image. There is no continuity between calls.
- If the set needs true visual continuity (the same face across images), that's **image-to-image with
  a reference**, which a plain text-to-image call cannot do. See `references/engines.md`.

---

## Scope

This skill owns **how to write the prompt and verify the result**. It does not own:

- **The creative brief** — subject matter, theme, house style, and the artifact's aspect ratio come
  from the job's own prompt. Where they conflict, the brief wins.
- **The image call** — engine, fallback order, metadata fields, and file conventions live in the
  recipe's runner, not in the prompt.
- **Image *selection*** (the recipe jobs download a real photo rather than generating one). Different
  problem, not covered here.
