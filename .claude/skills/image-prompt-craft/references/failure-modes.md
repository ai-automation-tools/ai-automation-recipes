# Failure Modes

Every entry here is a **real failure observed running these automations in production**, with the fix that resolved it. When a
render comes back wrong, find the symptom here before rewriting the prompt from scratch.

---

## 1. Invented text — stat blocks, credits, banners

**Symptom.** You asked for a portrait; you got a trading card with `RANK`, `AGE`, `CLASS` fields, an
edition number, and an illustrator credit line. Or a poster with a garbled billing block.

**Root cause — this is the important one.** The prompt named an **object that has text on it**. A
trading card, a movie poster, a magazine cover, a book jacket, an album sleeve, a UI screen, a
newspaper front page, an infographic — the model renders the *whole convention*, text included,
because that's what those objects look like.

**Fix, in order:**
1. **Change the noun.** "Clean illustrated portrait," not "trading card." "Illustration of X," not
   "poster of X." This alone resolves most cases.
2. Add the constraint block, naming the specific artifacts you saw: *no stat blocks, no RANK/AGE/CLASS
   fields, no edition numbers, no credit lines, no name banners.*
3. On retry, escalate specificity, not volume. "No text" repeated three times is weaker than naming
   the exact thing that appeared.

**Why prohibitions alone fail:** the noun is a positive instruction and the prohibition is a negative
one. Positive descriptions win. You cannot out-prohibit a described object.

---

## 2. Invented or substituted subject

**Symptom.** A prompt naming a real person renders a *different, fictional* person — sometimes with a
made-up name rendered as text.

**Observed:** a "Conor McGregor" prompt produced a stat card for a fictional **"Arthur Vance."**

**Fix.** Include the real name **and** an explicit physical description (see #4), and add *no invented
character, alias, or substitute name — the subject is the real figure* to the constraint block.
Dropping the trading-card framing usually clears this one too, since the invented name arrives as
part of the card convention.

---

## 3. Self-censoring to a silhouette

> **Scope: portraits of real, identifiable people.** A *decorative* silhouette — an anonymous figure
> as a compositional element in concept art — is a legitimate choice and some jobs explicitly allow
> it. This entry is only about a render that was supposed to show a specific person's face and
> didn't.

**Symptom.** A prompt for a well-known person returns a faceless black silhouette, a back-turned
figure, or a shadowed obscured face.

**Observed:** a "Michael Jackson" prompt self-censored to a faceless black silhouette.

**Fix — lead with the positive.** State the requirement as something to render, not something to
avoid, and put it in the **subject** clause where it carries the most weight:

> *…their actual face rendered in full illustrated detail, fully visible, lit and facing the viewer.*

⚠️ **Be sparing with the words "silhouette," "shadow figure," and "faceless."** A model weighs the
concepts in a prompt more than the little negating words attached to them, so a prohibition can prime
the very thing it forbids. That doesn't make negation useless — it makes it **second**:

- **Do:** put the positive face requirement in the subject clause, then *optionally* add a short
  `no silhouette, no obscured face` at the end of the constraint block.
- **Don't:** rely on the prohibition alone, lead with it, or pile up variants of it. If the only
  mention of the face is inside a "no …" list, the prompt is describing a faceless image.

This is the same mechanism as failure #1 — **a positive description always outranks a negative one**,
so the fix is to describe what you want, not to forbid harder.

---

## 4. Wrong likeness from a name-only prompt

**Symptom.** The name is right, the face is a generic stranger.

**Observed:** a name-only "Dave Chappelle" prompt produced a light-skinned man. A no-name prompt
("a Canadian academic professor") produced a generic face for Jordan Peterson.

**Fix — the name alone is never enough.** Always pair it with a brief explicit physical anchor:

- skin tone / ethnicity
- hair — colour, style, facial hair
- build and approximate age
- one or two distinguishing features

> "Black American comedian, warm medium-brown skin, short black hair, neat short beard, sly grin"
>
> "lean angular gaunt face, deep-set pale blue eyes, short receding greying hair swept back, short grey beard"

The description is what locks the likeness; the name alone is a suggestion the model may ignore.

---

## 5. Text you *wanted* comes out garbled

**Symptom.** A meme caption or headline renders as misspelled nonsense.

**Fix / limits.** Not fully fixable by prompting. Reduce the risk:
- Keep it to a **handful of words**, ideally one short line.
- Ask for it **large and prominent**, never small — small text always garbles.
- Quote the exact string and say it must be spelled exactly.
- **Verify by eye**, every time. Spelling is the single most common defect in text-bearing renders.

If the text must be exact and correct, render the image wordless and composite the text afterward.

---

## 6. The palette was ignored

**Symptom.** The subject and composition are right, the colours are generic.

**Cause.** The prompt was too long and the model dropped its back half — or the palette was vague
("warm tones," "a nice colour scheme").

**Fix.** Name three or four **specific** colours, and keep the whole prompt under ~150 words. If it
still slips, move the palette clause earlier, right after the style.

---

## 7. A set that doesn't look like a set

**Symptom.** Six panels that read as six different illustrators.

**Cause.** The style and palette were paraphrased differently in each prompt. **There is no memory
between image calls** — nothing carries over unless you write it again.

**Fix.** Copy the style and palette clauses **verbatim** into every prompt in the set. Vary only
subject, composition, and lighting.

---

## 8. Real public figures get refused

**Symptom.** A portrait of a real, identifiable person returns no image at all —
`GEMINI_IMAGE_NONE: Gemini returned no image part`, or `IMAGE_OTHER`.

**Verified 2026-07-27 on `gemini-3.1-flash-image`:**

| Prompt | Result |
|---|---|
| Red apple | ✅ renders |
| Portrait naming a real celebrity | ❌ refused |
| Same portrait, **name removed** — "a famous American YouTuber and WWE wrestler" | ❌ **still refused** |
| **Identical** physical description, labelled "a FICTIONAL young male athlete character" | ✅ renders |

**The trigger is the referring description, not the literal name.** So **removing the name is not a
workaround** — it looks like one, and isn't. If the description still points at a specific real
person, it gets refused; if it doesn't, you've lost the likeness anyway.

Also confirmed refused historically: Jake Paul, Gordon Ramsay, Obama, PewDiePie.

**What this means:** a recipe whose premise is real-person likenesses cannot rely on the standard chain.
That's an **engine** decision for the recipe owner, not something to fix by rewriting the prompt — say so
plainly rather than quietly substituting a generic subject, which produces a plausible stranger and a
misleading artifact.

---

## 9. The image step "succeeded" but the image is wrong

**Symptom.** The run logs `IMAGE_OK`, exit 0, and the picture is unusable.

**Cause.** The image step validates that a **real, non-empty PNG** landed at the path — a file-integrity
check, not a content check. Nothing in the pipeline looks at the image.

**Fix.** A person (or a vision check) is the content check. Look at it. See the verification loop in
`SKILL.md`.
