<h1 align="center">😂 AI Meme</h1>

<p align="center">
  <em>One original square meme with its caption drawn into the image.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/model-sonnet-8B5CF6?style=for-the-badge" alt="Default model: sonnet">
  <img src="https://img.shields.io/badge/needs-GEMINI_or_OPENAI_key-F59E0B?style=for-the-badge" alt="Needs GEMINI or OPENAI key">
  <a href="../README.md"><img src="https://img.shields.io/badge/↩-all_recipes-6B7280?style=for-the-badge" alt="All recipes"></a>
</p>

---

Claude invents a visual joke inside a rotating theme and writes the caption. The runner renders
it at 1:1 with the caption baked in. It never copies an existing meme template and never shows a
real person.

| | |
|:---|:---|
| **Output** | `ai-memes/<YYYY-MM>/<date>_<slug>/` → `meme.md` (caption + alt text), `meme.png`, `artifact.json` |
| **Model** | `sonnet` |
| **Tools** | Read, Write, Edit, Glob, Grep, Skill (no web access) |
| **Skills** | `image-prompt-craft` (its meme pattern, the one place it allows text) |
| **Needs** | An image key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). The meme is the output |

## Themes

Twelve, least-used first: AI at work, AI assistants at home, tech culture, internet life, prices
and subscriptions, streaming, gaming, dating apps, smart gadgets, office life, science and the
future, everyday chaos. Force one with `--theme "..."`.

## Idea queue (optional)

Create `<output-dir>/ai-memes/meme-ideas.md`:

```markdown
- [ ] AI replacing everyone except the people who keep scheduling meetings
- [ ] Nineteen streaming subscriptions to watch one show
```

Each run takes the first unchecked idea and ticks it off with a link to the meme it became.

## Check it by eye

Image models misspell. The prompt keeps captions short and asks for exact spelling, but nothing
automated reads the picture, so look before you share it.

## Run it

```bash
python recipes/ai-meme-generator/run.py --output-dir ~/ai-output
```

---

<p align="center">
  <a href="../README.md">← All recipes</a> ·
  <a href="../poster/README.md">Next: Poster →</a>
</p>
