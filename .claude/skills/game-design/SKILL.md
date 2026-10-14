---
name: game-design
version: 1.0.0
description: >-
  Design the game itself — the core loop, the moment-to-moment verbs, how
  difficulty and reward ramp over a session, and how to pitch it in a brief.
  Covers what makes a short arcade game worth a second attempt, difficulty
  curves that stay fair, scoring and progression models, feedback and game feel,
  and the failure modes of generated game concepts (a genre label instead of a
  loop, difficulty that only scales one number, no reason to replay). Use when
  inventing a game concept, writing or reviewing a game design brief, or
  diagnosing why a working game is not fun.
---

# Game design

This skill is about whether the game is **worth playing**. The runtime and browser layer — frame timing, canvas, touch, audio — is `single-file-game-dev`. Load both when building a game; load this one alone when writing a design brief.

## Start from the loop, not the genre

The most common failure in a generated concept is naming a genre and treating the design as done. *"An endless runner where you play as a robot"* is a theme and a label. It says nothing about what the player is deciding.

A core loop is **verb → obstacle → feedback → change**, and it must fit in one sentence with no genre words in it:

> Time a tap to jump a gap, land on a narrower platform, and the gaps get wider as you speed up.

That sentence has a verb (tap to jump), a pressure (narrowing platforms), and an escalation (speed). Write that before writing anything else — if you can't, the concept isn't finished, and no amount of art direction will rescue it.

**The test for a good loop: the player should be able to say why they lost, and believe they could do better.** Both halves matter. "I don't know what killed me" and "there was nothing I could have done" are the two ways a short arcade game dies.

## What makes a two-minute game worth replaying

These games are played in one sitting, often once. Everything that matters happens in the first thirty seconds.

- **Playable in five seconds.** No tutorial, no menu tree, no options screen. The first screen should be the game with one line of text on it. If the game needs instructions, the controls are wrong.
- **One verb, deep.** A single action with variable outcome (how long you hold, when you release, where you tap) beats four shallow buttons. Depth comes from *when* and *how much*, not from *how many*.
- **Failure is instant and cheap.** Death to retry in under a second, no confirmation, no animation the player has to sit through. The whole "one more go" property lives in that second.
- **A visible number that went up.** Score, distance, combo, streak. The player needs a reason to believe the next run can beat this one — and needs to see the personal best they are chasing.
- **Something changes within 30 seconds.** A new obstacle type, a speed step, a mechanic that layers on. A game whose second minute looks exactly like its first has already ended.

## The failure modes to check a concept against

Run these against any brief before shipping it. Each has a fix, not just a complaint:

| Failure | What it looks like | Fix |
|:--|:--|:--|
| **Genre-as-design** | "A match-3 with a space theme" | Write the one-sentence loop. Name the decision the player makes every few seconds. |
| **One-number difficulty** | Everything scales by multiplying speed | Ramp *kinds* of pressure, not just magnitude → `references/difficulty-and-progression.md` |
| **Unfair, not hard** | Off-screen spawns, unavoidable hits, input the game ignored | Telegraph every threat; guarantee a reachable path |
| **No feedback** | Points appear, nothing else happens | Hit-stop, flash, shake, sound, particles → `references/feel-and-feedback.md` |
| **Flat after 20s** | Minute five is identical to minute one | Introduce one new element on a timer or score threshold |
| **Nothing to chase** | No score, no best, no streak | Show the number and the personal best |
| **Reads as a chore** | Optimal play is repetitive and safe | Reward risk — make the greedy line the fun line |

## Scoring: make the interesting choice the rewarding one

A score model is a design statement about what the game wants. If the safest play is also the highest-scoring one, the game teaches boredom.

- **Risk multipliers** — near-misses, staying low, skipping the safe route. Reward proximity to danger.
- **Combos with decay** — chaining pays, but the chain lapses, so the player must keep committing.
- **Distance × pressure** — surviving longer is worth more *because* it is getting harder.

Avoid pure time-survival scoring: it rewards passivity, and the optimal strategy is to do as little as possible.

## Writing the brief

A design brief is judged on whether someone else could build the game from it. Concretely: the loop sentence, the controls, the difficulty ramp with actual numbers, the scoring model, the failure state, and what changes over a session. `references/pitch-and-brief.md` covers the structure and the vagueness traps.

⚠️ **Do not describe the game as a product.** "Engaging", "addictive", "endless fun", "players will love" — none of these are design. State what the player does and what the game does back. If a sentence would survive being pasted into a brief for a different game, it is not carrying information.

## References

| File | Read it for |
|:--|:--|
| `references/difficulty-and-progression.md` | Ramp shapes, pressure types, pacing, fairness rules, tuning numbers |
| `references/feel-and-feedback.md` | Game feel — hit-stop, screen shake, easing, input forgiveness, juice |
| `references/pitch-and-brief.md` | Brief structure, what makes a concept buildable, vagueness traps |
