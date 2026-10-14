# Difficulty and progression

The default generated ramp is one line: `speed *= 1.05` every level. It produces a game that is trivial for forty seconds and impossible three seconds later, with no interesting stretch in between.

## Ramp *kinds* of pressure, not one number

Speed is the crudest axis and the first one everyone reaches for. Real difficulty comes from layering different *types* of demand, staged so the player learns each one before the next arrives:

| Axis | Example | What it demands |
|:--|:--|:--|
| **Speed** | Everything moves faster | Reaction time |
| **Density** | More obstacles per screen | Spatial reading |
| **Variety** | A new enemy that moves differently | Recognition, not just reflex |
| **Precision** | Narrower gaps, tighter windows | Motor accuracy |
| **Compound** | Two mechanics that interact | Planning |
| **Resource** | Less time, ammo, or health | Economy decisions |
| **Cognitive** | Two things to track at once | Attention splitting |

**Introduce one axis at a time, and never raise two on the same beat.** A jump from "faster" to "faster *and* a new enemy *and* narrower gaps" reads as the game cheating.

## Shape of the curve

Not linear, and not exponential:

```
difficulty
   |                                    ____ plateau (mastery)
   |                              _____/
   |                        _____/  ← step: new mechanic
   |                  _____/
   |            _____/
   |      _____/  ← gentle opening, ~15-20s
   |_____/
   +-------------------------------------------- time
```

- **Opening (0–20s):** easy enough to be impossible to lose. The player is learning the controls whether you tell them to or not — this *is* the tutorial.
- **Steps, not slopes:** raise difficulty in discrete jumps at score or time thresholds, then hold. The plateau after each step is where the player feels themselves getting good. A smooth continuous ramp denies them that entirely.
- **Plateau near the end of the expected run:** cap the ramp. Past a point, more difficulty just adds randomness, and the run ends on a coin flip rather than a mistake.

A workable default for a two-minute arcade game: a new step every **20–30 seconds** or every **~500 points**, with the ramp flattening after about four steps.

## Concrete tuning starting points

Numbers to start from and then tune by playing — not to ship unexamined:

- **Scroll/enemy speed:** start `100%`, `+8–12%` per step, cap at `~250%` of the opening.
- **Spawn interval:** start `1.5–2.0s`, scale down `×0.9` per step, floor at `~0.4s` (below that it stops being readable).
- **Gap/window size:** never shrink below **1.5× the player's hitbox** — past that, success is luck.
- **First new mechanic:** ~20 seconds in. Any later and the game feels flat; any earlier and the opening is crowded.
- **Expected run length:** 60–120 seconds for a skilled player. If a first run lasts eight seconds, the opening is too hard; if it lasts five minutes, the ramp is too shallow.

## Fairness — the rules that separate "hard" from "cheap"

A hard game the player blames themselves for is fun. A hard game they blame the game for gets closed. The difference is a short list of guarantees:

- **Telegraph every threat.** A visible warning before anything that can kill — a flash, a tell, an approach. Minimum ~0.3s of notice, longer at speed.
- **Never spawn on top of the player,** and never spawn off-screen into an immediate collision. Enforce a minimum spawn distance scaled to closing speed.
- **Always leave a reachable path.** With randomised obstacles, validate that a gap exists which the player can physically reach from their current position — this is a real generator bug, not a theoretical one.
- **Honour input.** If the player pressed jump 50ms before landing, buffer it and jump on landing. See input forgiveness in `feel-and-feedback.md`.
- **The player's hitbox should be smaller than the sprite.** Generosity here is invisible and universally used.
- **Random ≠ fair.** Pure RNG produces impossible clusters. Constrain it: minimum spacing, no more than N in a row, guarantee a safe lane every M spawns.

## Progression within a single run

Short games have no meta-progression, so the arc happens inside one run:

- **Escalating stakes:** later obstacles are worth more, so a long run is also a high-scoring one.
- **Earned power:** a temporary ability at a threshold gives a relief beat and a spike of competence — then it expires and the pressure resumes.
- **Visible milestones:** a marker every 500 points. Something to be *just short of* is what starts the next run.

## Checking a ramp

Play three runs. If all three ended at roughly the same score, the ramp has a wall — find the step that is doing it. If they varied wildly with no sense of improvement, the difficulty is random rather than escalating. **The right feeling is that each run gets a little further than the last**, which means the curve is readable and the skill is real.
