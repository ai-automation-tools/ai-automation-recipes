# Display and input

Everything here is invisible on a desktop browser at 100% zoom and wrong on a phone.

## Canvas sizing: the blurry-game bug

A canvas has two independent sizes: the **backing store** (`canvas.width/height`, actual pixels) and the **CSS box** (`style.width/height`, layout size). Set only the CSS size and the browser upscales a low-resolution buffer — soft, smeared output on every phone and retina display.

```js
function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);   // cap at 2: see below
  const w = window.innerWidth, h = window.innerHeight;
  canvas.style.width  = w + 'px';       // CSS size = layout
  canvas.style.height = h + 'px';
  canvas.width  = Math.round(w * dpr);  // backing store = real pixels
  canvas.height = Math.round(h * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);  // now draw in CSS pixels
}
window.addEventListener('resize', resize);
resize();
```

After `setTransform`, all drawing code works in CSS pixels and ignores DPR entirely. **Cap DPR at 2** — a 3× phone means 9× the fill rate for no visible gain, and it is a common cause of a game that is smooth on desktop and sluggish on a flagship phone.

⚠️ **Setting `canvas.width` resets the entire 2D context state** — transform, `fillStyle`, `lineWidth`, everything. Re-apply after every resize, and never resize inside the render loop.

### Fitting the play area

Pick one and be deliberate:

- **Letterbox a fixed logical size** — best when layout matters. Design against a constant world (say 720×1280 portrait), then scale to fit and centre with bars. Everything downstream can assume fixed coordinates.
  ```js
  const scale = Math.min(w / GAME_W, h / GAME_H);
  ctx.setTransform(dpr*scale, 0, 0, dpr*scale, (w - GAME_W*scale)*dpr/2, (h - GAME_H*scale)*dpr/2);
  ```
- **Fill and adapt** — best for endless/arcade games. The world is whatever size the screen is; spawn positions and bounds read from it. Must handle extreme aspect ratios without breaking.

## Safe areas — the notch and the home indicator

A full-bleed phone game puts its score under the notch and its buttons under the home indicator. Opt in with the viewport tag, then inset with the CSS environment variables:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
```
```css
#hud { padding-top: env(safe-area-inset-top); padding-bottom: env(safe-area-inset-bottom); }
```

For canvas-drawn HUD, read them once at startup and offset:
```js
const cs = getComputedStyle(document.documentElement);
const safeTop = parseFloat(cs.getPropertyValue('--sat')) || 0;  // via a CSS var set to env()
```
Simplest reliable rule: **keep anything interactive or readable at least 44 CSS px from every screen edge**, which covers notch, indicator, and fat-thumb reach in one number.

## Input

### Stopping the browser from fighting the player

The default gesture handling — scroll, pinch-zoom, double-tap-zoom, iOS rubber-band, long-press selection — all fires *during* play unless you turn it off. Two layers, both needed:

```css
html, body { margin:0; height:100%; overflow:hidden; touch-action:none;
             -webkit-user-select:none; user-select:none;
             -webkit-tap-highlight-color:transparent; }
```
```js
// preventDefault requires a NON-passive listener. Touch listeners default to
// passive:true in modern browsers, where preventDefault() silently does nothing.
canvas.addEventListener('touchstart', onTouch, { passive: false });
canvas.addEventListener('touchmove',  onTouch, { passive: false });
function onTouch(e) { e.preventDefault(); /* ... */ }
```

**`{ passive: false }` is the whole fix for "the page scrolls while I play".** Without it `preventDefault()` is a no-op and no error is raised — which is exactly why it survives review.

### Pointer events: one code path instead of three

Prefer Pointer Events — mouse, touch, and stylus arrive through the same handlers with correct capture semantics:

```js
canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); press(pos(e)); },
                        { passive: false });
canvas.addEventListener('pointermove', e => move(pos(e)), { passive: false });
canvas.addEventListener('pointerup',   e => release(pos(e)));

function pos(e) {                      // client → canvas coords, zoom-safe
  const r = canvas.getBoundingClientRect();
  return { x: (e.clientX - r.left) * (canvas.width / r.width / dpr),
           y: (e.clientY - r.top)  * (canvas.height / r.height / dpr) };
}
```

Always convert through `getBoundingClientRect()`. Using raw `clientX/clientY` breaks the moment the canvas is letterboxed, scaled, or offset — the game "ignores taps" near the edges.

### Keyboard

Track a held-key set; never drive movement from the `keydown` repeat, which has an OS-controlled initial delay and produces a stutter-step:

```js
const keys = new Set();
addEventListener('keydown', e => {
  if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key)) e.preventDefault();
  keys.add(e.key);
});
addEventListener('keyup', e => keys.delete(e.key));
// in update(dt):  if (keys.has('ArrowLeft')) player.x -= SPEED * dt;
```

`preventDefault` on arrows and space stops the page scrolling under the game — the desktop twin of the touch bug above.

### Touch controls that are actually usable

A keyboard game needs a real touch scheme, not a shrunken one:

- **Minimum 44×44 CSS px** for any tap target, with generous invisible padding.
- **Tap zones beat tiny buttons** — left half / right half, or tap-to-jump, is more reliable on a phone than a D-pad drawn at 30px.
- **Thumb reach:** bottom third of the screen, both sides. Never the top corners.
- **Drag beats buttons** for continuous movement — track the pointer directly.
- Show controls **only on touch devices**: gate on `matchMedia('(pointer: coarse)')`, not on user-agent sniffing.

## Quick check

Device-emulate a narrow portrait phone and confirm: sharp (not soft) rendering; the page does not scroll, zoom, or rubber-band while dragging; nothing important sits within 44px of an edge; taps register accurately at the corners of the play area.
