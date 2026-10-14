---
name: single-file-game-dev
version: 1.0.0
description: >-
  Build a playable game as ONE self-contained `index.html` — no build step, no
  bundler, no asset files. Covers the frame loop and delta timing (so speed does
  not change with refresh rate), canvas sizing on high-DPI and phone screens,
  keyboard/mouse/touch input that does not fight the browser, unlocking WebAudio
  on mobile, a screen state machine, and the allocation discipline that keeps a
  phone at 60fps. Use whenever writing, reviewing, or debugging a browser or
  mobile game that ships as a single HTML file — especially when it runs at the
  wrong speed, is blurry, scrolls or zooms while playing, is silent on iOS, or
  stutters after a minute.
---

# Single-file game dev

One `index.html`. Inline `<style>` and `<script>`. Art drawn at runtime, audio synthesised at runtime, no external files and no build step. Everything here is about the failure modes *that shape* creates.

**Scope.** This skill is the runtime and browser layer. It says nothing about whether the game is fun — that is `game-design`. Load both when writing a game; load this one alone when debugging one.

## The seven that actually break these games

Ranked by how often they ship. The first three are silent on a desktop dev machine and obvious on a phone, which is exactly why they survive review.

| # | Bug | Symptom | Fix |
|---|---|---|---|
| 1 | Movement is per-frame, not per-second | Runs ~2× fast on a 120Hz phone, slow-motion on a loaded tab | Delta time → `references/loop-and-timing.md` |
| 2 | Canvas has no `devicePixelRatio` scaling | Blurry / soft on every phone and retina display | Backing-store scale → `references/display-and-input.md` |
| 3 | Touch handlers don't `preventDefault` | Page scrolls, pinch-zooms, or rubber-bands mid-game | Non-passive listeners → `references/display-and-input.md` |
| 4 | Audio context created before a user gesture | Completely silent on iOS, fine on desktop | Unlock on first input → `references/audio.md` |
| 5 | Allocating objects inside the frame loop | Smooth for 30s, then periodic GC hitches | Pool and reuse → `references/performance-and-structure.md` |
| 6 | Screens managed with scattered booleans | Pause during game-over, input after death, unclosable menus | One state machine → `references/performance-and-structure.md` |
| 7 | No `visibilitychange` handling | Tab away 5 minutes, return to one catastrophic frame | Clamp dt / pause → `references/loop-and-timing.md` |

## The shape that works

```html
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<style> html,body{margin:0;height:100%;background:#111;overflow:hidden;
        touch-action:none;-webkit-user-select:none;user-select:none} </style>
<canvas id="c"></canvas>
<script>
// 1. Grab every element reference HERE, at the top. The script is the last thing
//    in the body, so the DOM already exists. Never declare-at-top-assign-later.
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

// 2. State machine, not booleans.
const S = { TITLE:'title', PLAY:'play', PAUSE:'pause', OVER:'over' };
let state = S.TITLE;

// 3. Fixed-step update, interpolation-free render. See loop-and-timing.md.
let last = performance.now(), acc = 0;
const STEP = 1000 / 60;
function frame(now) {
  acc += Math.min(now - last, 250);   // clamp: tab-away must not spiral
  last = now;
  while (acc >= STEP) { update(STEP / 1000); acc -= STEP; }
  render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
```

Three things that block are worth naming, because they are structural rather than stylistic:

- **All element references at the top of the script, or all listeners inside one init callback — never a mix.** The half-and-half version throws a single `TypeError` during initial execution, which aborts the *entire* inline script including the `load` handler at the bottom. You get a title screen that renders correctly and responds to nothing.
- **`touch-action:none` in CSS is not optional** and is not a substitute for `preventDefault` — you need both. CSS stops the gesture from starting; `preventDefault` stops the ones already in flight.
- **`overflow:hidden` on `html,body`** — otherwise iOS rubber-band scrolling fights every vertical drag.

## Verify before shipping

A single-file game has no test suite, so the check is a short manual pass. Do it in this order — each step catches something the next one masks:

1. **Does it start?** Open the file directly from disk (`file://`, no server). A blank canvas or a dead title screen is bug #1 above, not a rendering problem.
2. **Does it run at the right speed?** Throttle the frame rate (DevTools → Rendering → 30fps) and confirm the game plays at the *same* speed, just choppier. If it slows down, movement is per-frame.
3. **Is it sharp and reachable on a phone?** Device-emulate a narrow portrait screen. Check it is not blurry, that the page does not scroll or zoom while you drag, and that nothing important sits under the notch or home indicator.
4. **Does it make sound after a tap?** Silent-on-first-load is the gesture-unlock bug.
5. **Play it for two minutes.** Pooling and allocation bugs only appear after the first few GC cycles.
6. **Die, restart, pause, tab away, come back.** This is where the state machine either holds or falls apart.

**Report what you actually verified.** "Renders and is playable" after opening the file once is not step 2–6, and this job class has shipped a game that looked fine and responded to nothing.

## References

| File | Read it for |
|:--|:--|
| `references/loop-and-timing.md` | rAF, delta vs fixed timestep, pause, `visibilitychange`, spiral-of-death |
| `references/display-and-input.md` | devicePixelRatio, resize + letterbox, safe-area insets, keyboard/mouse/touch, tap zones |
| `references/audio.md` | Unlocking WebAudio on a gesture, synthesising SFX with no asset files |
| `references/performance-and-structure.md` | Screen state machine, object pooling, per-frame allocation, phone budget |
