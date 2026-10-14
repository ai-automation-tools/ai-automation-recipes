# Structure and performance

Two problems that only show up after the game has been running for a while: state handled by scattered booleans, and garbage collected mid-frame.

## Screens: one state machine, not five booleans

The booleans version always arrives at the same bugs — pausing during the game-over screen, input still moving the player after death, a menu that cannot be closed, restart that leaves the old score:

```js
// WRONG
let isPlaying = false, isPaused = false, isGameOver = false, showMenu = true;
```

Because those four flags encode sixteen states, and only four are legal.

```js
const S = { TITLE:'title', PLAY:'play', PAUSE:'pause', OVER:'over' };
let state = S.TITLE;

function setState(next) {
  if (state === next) return;
  state = next;
  if (next === S.PLAY && !world) startRun();     // enter-transition work
  if (next === S.OVER) submitScore();
}

function update(dt) {
  if (state !== S.PLAY) return;    // ONE place decides whether the world ticks
  world.step(dt);
}

function render() {
  drawWorld();                     // always draw, so pause/over overlay the game
  if (state === S.TITLE) drawTitle();
  if (state === S.PAUSE) drawPauseOverlay();
  if (state === S.OVER)  drawGameOver();
}

function press(p) {                // input is routed BY state, never global
  if (state === S.TITLE) return setState(S.PLAY);
  if (state === S.OVER)  return restart();
  if (state === S.PLAY)  return world.onPress(p);
}
```

The loop keeps running in every state — only `update` is gated. That is what lets the pause screen animate and the game show through behind it.

**Restart must rebuild state, not patch it.** `startRun()` should construct a fresh world object. Resetting fields by hand is how a "new game" keeps the previous run's difficulty multiplier.

## Allocation: the stutter that appears after 30 seconds

The frame loop runs 60× a second. Anything allocated inside it becomes garbage, and the collector eventually pauses the main thread — a game that is smooth at first and hitches periodically later.

```js
// WRONG — three allocations per enemy per frame
enemies.forEach(e => {
  const dir = { x: player.x - e.x, y: player.y - e.y };
  const len = Math.hypot(dir.x, dir.y);
  e.pos = { x: e.x + dir.x/len * SPD * dt, y: e.y + dir.y/len * SPD * dt };
});
```

```js
// RIGHT — mutate in place, no temporaries
for (let i = 0; i < enemies.length; i++) {
  const e = enemies[i];
  const dx = player.x - e.x, dy = player.y - e.y;
  const len = Math.hypot(dx, dy) || 1;
  e.x += dx / len * SPD * dt;
  e.y += dy / len * SPD * dt;
}
```

The offenders, in rough order of impact: object/array literals per entity per frame; `map`/`filter`/`slice` in the loop (each returns a new array); string building for the HUD every frame; closures created per entity per frame.

**`ctx.fillText(score, ...)` is fine — building `"Score: " + score.toLocaleString()` 60× a second is not.** Cache the string and rebuild it only when the score changes.

## Object pooling

For anything spawned in quantity and destroyed constantly — bullets, particles, enemies — allocate once and reuse. Pooling is the single highest-value performance pattern in this class of game:

```js
function makePool(size, factory) {
  const items = Array.from({ length: size }, factory);
  return {
    items,
    spawn(init) {
      for (let i = 0; i < items.length; i++) {
        if (!items[i].alive) { items[i].alive = true; init(items[i]); return items[i]; }
      }
      return null;                   // pool exhausted: drop it, never grow mid-frame
    }
  };
}

const bullets = makePool(200, () => ({ x:0, y:0, vx:0, vy:0, alive:false }));
bullets.spawn(b => { b.x = player.x; b.y = player.y; b.vy = -600; });
```

Then **never splice the array** — iterate all slots and skip dead ones. `splice` reindexes the whole array every removal and reintroduces the churn pooling just removed:

```js
for (let i = 0; i < bullets.items.length; i++) {
  const b = bullets.items[i];
  if (!b.alive) continue;
  b.x += b.vx * dt; b.y += b.vy * dt;
  if (b.y < -20) b.alive = false;     // "destroy" = a flag
}
```

A fixed pool also caps the worst case: the game cannot spawn itself to death, which is a real failure mode in a difficulty ramp with no ceiling.

## Drawing on a phone

- **State changes are the cost, not the shapes.** Group by `fillStyle` and draw all of one colour, then the next. Hundreds of `ctx.fillStyle = ...` switches per frame is a measurable hit.
- **`save()`/`restore()` are not free.** For a simple translate, add and subtract the offset instead of pushing a full context state.
- **Never render text with a fresh `font` string per call.** Set it once per group.
- **Offscreen-cache anything static** — a starfield, a tiled background, a pre-rendered sprite — onto a second canvas at startup and `drawImage` it. Redrawing 200 stars per frame is pure waste.
- **Budget: ~16ms per frame at 60fps**, and a mid-range phone is several times slower than the machine writing the code. Prefer fewer, larger draws.
- **Cap the particle count** with a hard constant, not a difficulty-scaled one. Particles are where "it got slow at high scores" comes from.

## Check

Play for two full minutes and watch for periodic hitching — that pattern (smooth, hitch, smooth, hitch) is GC, and it means allocation in the loop. Then push the game to its highest difficulty and confirm the frame rate holds with maximum entities on screen.
