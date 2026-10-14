# Engines

Which renderer gets the prompt, and what that means for how you write it.

---

## The routing rule

The agent never calls an image model itself. It writes the **picture description** into its run
manifest (`cover_prompt`), and the recipe's runner renders it after the agent exits. That keeps
the image step identical whichever text engine wrote the prompt, and keeps API keys out of the
agent's reach.

The runner walks a ladder and stops at the first engine that returns a real PNG:

```
gemini (GEMINI_API_KEY)  ──fails──▶  openai (OPENAI_API_KEY)  ──fails──▶  run fails, or skips the cover with --image-engine none
```

Only engines whose key is set are tried. `--image-engine gemini|openai|auto|none` picks one
explicitly.

| Engine | Model (override with env) | Key | Aspect ratios |
|---|---|---|---|
| `gemini` | `gemini-3.1-flash-image` (`GEMINI_IMAGE_MODEL`) | `GEMINI_API_KEY` | Native: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9` |
| `openai` | `gpt-image-1` (`OPENAI_IMAGE_MODEL`) | `OPENAI_API_KEY` | Snapped to `1024x1024`, `1536x1024` (landscape) or `1024x1536` (portrait) |

**Write one prompt that works on both.** Don't add engine-specific phrasing — a fallback render
should be the same picture from a different hand.

## What a text-to-image call can't do

- **Continuity across images.** Each call starts fresh. Two renders of "the same" character will
  differ. True continuity needs image-to-image with a reference, which these recipes don't use.
- **Long or small text.** It garbles. See the meme pattern in `prompt-patterns.md`.
- **Real people.** Both engines refuse likenesses of identifiable people, and removing the name
  doesn't help if the description still points at them. See `failure-modes.md` §8.

## Cost

Both engines bill per image. A cover a day on either is on the order of a few dollars a month —
check the provider's current pricing before scheduling a high-frequency recipe.
