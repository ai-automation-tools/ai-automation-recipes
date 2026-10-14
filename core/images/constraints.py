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
