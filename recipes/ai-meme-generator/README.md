# AI Meme

[← All recipes](../../README.md)

One original meme, twice a week. Claude invents a visual joke in a rotating theme and writes the
caption; the runner renders it square with the caption baked in. Never a copied meme template,
never a real person.

| | |
|:---|:---|
| **Output** | `ai-memes/<YYYY-MM>/<date>_<slug>/` → `meme.md` (caption + alt text), `meme.png`, `artifact.json` |
| **Schedule** | Tuesdays and Fridays, 13:00 UTC |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `image-prompt-craft` (its meme pattern — the documented text exception) |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`) — the meme is the output |

## Themes

Twelve, least-used first: AI at work, AI assistants at home, tech culture, internet life, prices
and subscriptions, streaming, gaming, dating apps, smart gadgets, office life, science and the
future, everyday chaos. Force one with `--theme "…"`.

## Idea queue (optional)

Create `<output-dir>/ai-memes/meme-ideas.md`:

```markdown
- [ ] AI replacing everyone except the people who keep scheduling meetings
- [ ] Nineteen streaming subscriptions to watch one show
```

Each run takes the first unchecked idea and ticks it off with a link to the meme it became.

## Check it by eye

Image models misspell. The prompt keeps captions short and asks for exact spelling, but nothing
automated reads the picture — look before you share it.

## Run it

```bash
python recipes/ai-meme-generator/run.py --output-dir ~/ai-output
```
