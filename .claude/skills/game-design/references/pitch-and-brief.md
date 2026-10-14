# Pitching and briefing a game concept

A design brief has exactly one job: **someone else could build the game from it and arrive at roughly the game you meant.** Everything that does not serve that is decoration.

## The one-sentence loop comes first

Before any section, write the loop. No genre nouns, no theme, no adjectives:

> *Hold to charge a jump, release to launch; longer charges go further but leave you helpless in the air.*

That sentence contains a verb, a tradeoff, and a cost. Compare with what generated concepts usually open on:

> *A fast-paced arcade platformer where players navigate challenging levels.*

Which contains no information at all — it describes several hundred existing games equally well. **If the loop sentence would fit another game unchanged, it is not a loop sentence.**

## Sections that earn their place

- **The loop** — the sentence above.
- **Controls** — every input and what it does. For a browser game, keyboard *and* mouse *and* touch. If a control needs a paragraph, it is too complex.
- **The obstacle** — what is trying to end the run, and how the player reads it coming.
- **Difficulty ramp** — with numbers. "Gets harder over time" is not a ramp; "spawn interval 1.8s → 0.5s in six steps of 20s, new enemy type at step 2" is.
- **Scoring** — the model, and *what behaviour it rewards*. State the intended optimal strategy; if that strategy is boring, the model is wrong.
- **Failure and restart** — what death looks like, and how fast the retry is.
- **What changes over a session** — the answer to "why is minute two different from minute one?"
- **Art and audio direction** — a named palette (3–4 colours), the visual style, how sound is produced. Concrete enough to implement.

## Vagueness traps

Each of these is a phrase that survives into briefs while carrying nothing. The fix is always the same: replace the claim with the mechanism.

| Vague | Why it fails | Replace with |
|:--|:--|:--|
| "Challenging but fair" | Every game claims this | The fairness guarantees — telegraphing, spawn rules, buffering |
| "Fast-paced action" | Describes a speed, not a design | The actual speed and what forces the pace |
| "Intuitive controls" | Unfalsifiable | The control list |
| "Progressively harder" | The default assumption | The ramp table with numbers |
| "Addictive gameplay loop" | Marketing, not design | What makes the player retry — the number they're chasing |
| "Polished visuals" | Says nothing implementable | Palette, shapes, effects |
| "Players will love…" | A prediction, not a spec | Delete it |

⚠️ **A brief is not a pitch deck.** No target market, no monetisation, no "in a world where". These jobs produce a design document, and superlatives about how fun it will be are the clearest signal that the loop underneath was never worked out.

## The buildability test

Read the brief back and ask, for each of these, whether the answer is *in the document*:

1. What does the player press, and what happens?
2. How does a run end?
3. What is on screen at second 5, second 30, and second 90 — and how do they differ?
4. What number goes up, and what behaviour makes it go up fastest?
5. What does the player see the instant before they die?
6. What are the actual difficulty values at each step?

Any "it depends" or "the implementer would decide" is a hole. Fill it — those are exactly the decisions that get made badly by default.

## Concept generation: variety without gimmickry

When rotating through concepts (as a weekly job does), the temptation is a theme swap — same loop, new skin. Genuine variety comes from changing the *decision*:

- **Change the verb** — from dodging to catching, timing to positioning, reacting to planning.
- **Change what is scarce** — time, space, health, ammo, attention.
- **Change the failure condition** — one hit, a depleting bar, a timer, a wrong choice.
- **Invert a known loop** — you are the obstacle; you place hazards rather than avoiding them; the level plays and you position.
- **Constrain the input** — one button, no buttons (movement only), input that also costs a resource.

Check a new concept against the recent ones on the *loop* sentence, not the theme. Two games can look completely different and be the same game.
