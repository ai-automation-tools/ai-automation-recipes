# Game feel and feedback

Two games with identical rules can feel completely different. Feel is where a mechanically-correct generated game usually falls down: everything works, nothing is satisfying. All of it is cheap — a few lines each — and it is the highest ratio of perceived quality to effort in the whole build.

## Every action needs a reaction

The rule: **no state change without sensory confirmation.** If the player did something and the score silently changed, the game did not acknowledge them.

A single impact should fire several channels at once — that stacking is what reads as "juice":

| Channel | Cheap version | When |
|:--|:--|:--|
| **Visual** | Flash the sprite white for 2 frames | Any hit |
| **Motion** | Scale-punch to 1.2 and ease back | Pickups, landings |
| **Screen** | 2–6px shake, decaying over ~0.2s | Impacts, explosions |
| **Time** | Freeze the whole game 30–80ms | Big hits only |
| **Particles** | 5–15 for a small event, 30+ for a big one | Anything destroyed |
| **Audio** | A pitch-swept blip | Everything |

## Hit-stop is the strongest single trick

Freezing the entire game for a few frames on impact does more for weight than any amount of art:

```js
let freeze = 0;
function onBigHit() { freeze = 0.06; }         // 60ms

function update(dt) {
  if (freeze > 0) { freeze -= dt; return; }    // world is paused; render continues
  world.step(dt);
}
```

Use it sparingly and only on significant events — a boss hit, a death, a big combo. Applied to every trivial pickup it just makes the game feel like it is stuttering.

## Screen shake, done correctly

```js
let shake = 0;
function addShake(amount) { shake = Math.min(shake + amount, 12); }  // cap it

function render() {
  ctx.save();
  if (shake > 0) {
    ctx.translate((Math.random()-0.5) * shake, (Math.random()-0.5) * shake);
    shake *= 0.88;                    // decay per frame; below 0.1 clamp to 0
  }
  drawWorld();
  ctx.restore();
}
```

**Cap the magnitude and decay fast.** Uncapped shake from stacked simultaneous events makes the game unreadable and, on a phone, genuinely unpleasant. Anything above ~10px is too much for a small screen.

## Easing — never move UI linearly

Linear motion reads as mechanical. One helper covers almost everything:

```js
const lerp  = (a, b, t) => a + (b - a) * t;
// call with a small t each frame for a smooth chase
score.display = lerp(score.display, score.actual, 0.15);
```

That single line — a score that counts *up* to its value instead of snapping — is one of the most noticeable polish wins available. The same applies to camera follow, health bars, and menu transitions.

For discrete animations, ease-out (fast then settling) suits almost everything in an arcade game: `t => 1 - Math.pow(1 - t, 3)`.

## Input forgiveness

Players are not frame-accurate, and the game should not require it. These are invisible when present and infuriating when absent:

- **Coyote time** — allow a jump for ~80–120ms *after* walking off a ledge. Nobody notices it; everybody notices its absence.
- **Input buffering** — if jump is pressed within ~120ms before landing, execute it on landing rather than dropping it.
- **Forgiving hitboxes** — the player's collision box smaller than the sprite; enemies' slightly larger. Universal, and never remarked on.
- **Generous tap targets** — see the 44px rule in `single-file-game-dev`.

```js
if (onGround) coyote = 0.1; else coyote -= dt;
if (jumpPressed) buffer = 0.12; else buffer -= dt;
if (buffer > 0 && coyote > 0) { jump(); buffer = 0; coyote = 0; }
```

## Readability beats beauty

On a phone, at speed, the player has milliseconds to parse the screen:

- **The player must be the highest-contrast thing on screen.** Always.
- **Danger gets one colour and keeps it.** Never reuse the threat colour for decoration.
- **Background stays low-contrast.** A busy background is the most common reason a game "feels bad" for no identifiable reason.
- **Silhouette first:** if the important objects are not distinguishable as black shapes, colour will not save them.
- **Never hide critical information in a corner** — score can live at the edge, but a health or countdown state the player must react to belongs near the action.

## Death and restart

The most replayed three seconds in the game:

- Death gets the biggest feedback moment in the build — freeze, shake, sound, particles.
- Show the score **and the personal best** together. The gap between them is the reason to press retry.
- **Restart in one input, under a second, no confirmation.** Any friction here — a dialog, a menu, a mandatory animation — is where the session ends.
