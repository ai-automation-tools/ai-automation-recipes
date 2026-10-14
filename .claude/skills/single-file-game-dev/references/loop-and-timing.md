# Loop and timing

The single most common defect in a generated browser game: **the game is faster on a better screen.** It is invisible on the machine that wrote it and obvious on a modern phone.

## Why per-frame movement is wrong

```js
// WRONG — "5 pixels per frame"
player.x += 5;
```

`requestAnimationFrame` fires at the display's refresh rate. That is 60Hz on an old laptop, **120Hz on a current phone or a ProMotion display**, 144Hz+ on a gaming monitor, and something erratic on a loaded tab. The line above means "5 pixels per frame", so the game literally runs twice as fast on the phone it was written for.

```js
// RIGHT — "300 pixels per second"
player.x += 300 * dt;   // dt in seconds
```

Every quantity that changes over time takes `dt`: velocity, gravity, spawn timers, cooldowns, animation, difficulty ramps, score-per-second. **A timer written as `frames++` is the same bug wearing a different hat.**

## Two loops, and when each is right

### Variable delta — simpler, fine for most arcade games

```js
let last = performance.now();
function frame(now) {
  const dt = Math.min((now - last) / 1000, 0.05);  // clamp! see below
  last = now;
  update(dt);
  render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

The clamp is not optional. Without it, a tab-away or a slow first paint hands `update()` a `dt` of 30+ seconds, and everything teleports through walls in one step. `0.05` (50ms) is a reasonable ceiling — the game stutters rather than breaking.

### Fixed timestep — required when physics or collision must be stable

Variable `dt` makes collision non-deterministic: the same jump clears a gap at 120Hz and clips it at 30Hz. When the game has platforming, stacking, bouncing, or anything where "it went through the wall" is possible, accumulate instead:

```js
const STEP = 1000 / 60;          // logic ticks at a constant 60/s
let last = performance.now(), acc = 0;

function frame(now) {
  acc += Math.min(now - last, 250);   // 250ms ceiling = spiral-of-death guard
  last = now;
  while (acc >= STEP) {
    update(STEP / 1000);              // dt is ALWAYS the same value
    acc -= STEP;
  }
  render();                            // render as often as the display allows
  requestAnimationFrame(frame);
}
```

**The 250ms ceiling is the important line.** Without it, a long stall makes `acc` huge, the `while` loop runs hundreds of updates, that takes longer than a frame, which grows `acc` further — the loop never exits and the tab hangs. That is the *spiral of death*, and the guard is one `Math.min`.

## Pausing, and the tab-away problem

`requestAnimationFrame` is throttled or stopped in a background tab, but `performance.now()` keeps advancing. Returning after five minutes delivers one enormous `dt`. The clamps above stop the explosion; handling `visibilitychange` stops the weirdness:

```js
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { paused = true; }
  else { last = performance.now(); acc = 0; }   // reset the clock, don't catch up
});
```

**Reset, never catch up.** Simulating the five minutes the player was away is never what they wanted.

Pausing itself belongs to the state machine, not to a `paused` flag checked in ten places — see `performance-and-structure.md`. The loop keeps running while paused; `update()` is what gets skipped, so the pause screen can still animate.

## Timers and cooldowns

Count down in seconds, not frames:

```js
// WRONG
if (--enemy.cooldown <= 0) enemy.fire();
// RIGHT
enemy.cooldown -= dt;
if (enemy.cooldown <= 0) { enemy.fire(); enemy.cooldown = 1.5; }
```

Set the reload to `+= 1.5` rather than `= 1.5` if the cooldown should not lose the fractional overshoot — it matters for anything that fires rapidly.

## Checking it

DevTools → Rendering → **Frame Rendering Stats / throttle to 30fps**. A correctly-timed game plays at the same speed and just looks choppier. If it plays in slow motion, something is still per-frame. This takes about ten seconds and is the single highest-value check on the list.
