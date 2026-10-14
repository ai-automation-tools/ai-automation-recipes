"""The one canonical no-text constraint. The image-prompt-craft skill quotes it verbatim."""

NO_TEXT = (
    "STRICT: no text, letters, words, numbers, captions, titles, labels, banners, credits, "
    "stat blocks, logos, watermarks, signatures, UI chrome, or borders anywhere in the image."
)


def with_constraints(prompt: str) -> str:
    """Append NO_TEXT unless the prompt already ends with it."""
    prompt = prompt.strip()
    if NO_TEXT in prompt:
        return prompt
    return f"{prompt}\n\n{NO_TEXT}"


# For images that are meant to carry words (meme captions, comic balloons, poster lettering).
LETTERING_ONLY = (
    "STRICT: the only text in the image is the lettering quoted in this prompt, spelled exactly as "
    "written; no other text, captions, labels, logos, watermarks, signatures, UI chrome, or borders."
)


def with_lettering_constraint(prompt: str) -> str:
    prompt = prompt.strip()
    return prompt if LETTERING_ONLY in prompt else f"{prompt}\n\n{LETTERING_ONLY}"
