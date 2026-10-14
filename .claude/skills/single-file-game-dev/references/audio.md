# Audio with no asset files

A single-file game cannot ship a `.wav`. Everything is synthesised at runtime with the WebAudio API — which is fine, because arcade SFX are exactly what oscillators are good at.

## The silent-on-mobile bug

**Every browser blocks audio until the user has interacted with the page.** An `AudioContext` created on load starts `suspended`, and every sound played into it is silently discarded. On desktop the developer usually clicks something before noticing; on iOS the game is simply silent forever.

Create the context lazily on the first real input, and resume it:

```js
let actx = null;
function audio() {
  if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
  if (actx.state === 'suspended') actx.resume();   // needed after tab-away too
  return actx;
}

// Call from the FIRST user gesture — the same handler that starts the game.
canvas.addEventListener('pointerdown', () => audio(), { once: true });
```

Two details that bite:

- **`resume()` must be called from inside the gesture handler**, not from a timer or a promise chain scheduled by it.
- **A context can re-suspend** when the tab is backgrounded on mobile. Calling `audio()` at the top of every sound function (as above) is cheap and makes it self-healing.

## A sound function that covers most of a game

One envelope-shaped oscillator handles blips, jumps, pickups, hits, and explosions — the difference is waveform, pitch sweep, and decay:

```js
function sfx({ freq = 440, to = null, type = 'square', dur = 0.12, vol = 0.25 }) {
  const a = audio(); if (a.state !== 'running') return;   // never throw from audio
  const t = a.currentTime;
  const osc = a.createOscillator(), gain = a.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, t);
  if (to) osc.frequency.exponentialRampToValueAtTime(to, t + dur);  // sweep
  gain.gain.setValueAtTime(vol, t);
  gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);          // decay
  osc.connect(gain).connect(a.destination);
  osc.start(t); osc.stop(t + dur);
}

sfx({ freq: 880, to: 1760, type: 'square',   dur: 0.08 });  // pickup / coin
sfx({ freq: 220, to: 440,  type: 'triangle', dur: 0.15 });  // jump
sfx({ freq: 160, to: 40,   type: 'sawtooth', dur: 0.30 });  // hit / explosion
sfx({ freq: 120, to: 60,   type: 'sine',     dur: 0.50, vol: 0.3 });  // game over
```

**Use `exponentialRampToValueAtTime`, never ramp to exactly 0** — zero is invalid for an exponential ramp and throws. `0.0001` is the idiom.

For noise (explosions, footsteps, static) fill a short buffer with random samples once at startup and play it through a filter — do not generate the buffer per shot.

## Rules that keep it from becoming a problem

- **Never let audio break the game.** Wrap creation in the state guard above and let sound fail silently. A thrown `AudioContext` error inside the frame loop kills the whole game for a sound effect.
- **Cap concurrent voices.** Twenty simultaneous oscillators on a phone is audible distortion and real CPU cost. Track active count and drop new sounds past ~8, or reuse one node per sound class.
- **Never create nodes in the render path.** Only on discrete events. `createOscillator()` per frame is the audio version of the allocation bug in `performance-and-structure.md`.
- **Provide a mute.** A single `masterGain` node everything connects through, toggled to 0 — and remember the choice for the session. Web games that cannot be muted get closed.
- **Keep default volume low** (`0.2`–`0.3`). Synthesised square waves are much louder than they look on paper, and the player has no idea what is coming.

## Check

Load the game, tap once, confirm sound. Then background the tab, return, and confirm sound still works — that second step is what catches the re-suspend case.
