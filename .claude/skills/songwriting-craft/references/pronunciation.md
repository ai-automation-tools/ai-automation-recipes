# Pronunciation

A generative music model reads your lyrics as text and commits to one pronunciation. It gets
homographs wrong constantly, spells out numbers digit by digit, and mangles proper nouns — and you
don't find out until the render is paid for.

**The fix is phonetic respelling in the sung text.** Write what you want heard. Keep the correctly
spelled version in any human-facing lyrics file if the respelling looks wrong on the page — but note
that in this repo the saved lyrics file is supposed to match the sung text, so prefer respellings
that read acceptably.

---

## Category 1 — Homographs (highest risk)

Same spelling, different pronunciation. **Always disambiguate.**

| Word | Meaning A | Meaning B | Fix |
|---|---|---|---|
| live | LYVE (alive) | LIV (performance) | Always clarify |
| read | REED (present) | RED (past) | Use "red" for past tense |
| lead | LEED (guide) | LED (metal) | Use "led" for the metal |
| wind | WIND (air) | WYNED (coil) | Use "wynd" for coiling |
| close | KLOHS (near) | KLOHZ (shut) | Use "clohz" for shutting |
| tear | TEER (crying) | TARE (rip) | Use "tare" for ripping |
| bass | BAYSS (music) | BASS (fish) | Use "bass" only for the fish |
| wound | WOOND (injury) | WOWND (coiled) | Use "wownd" for coiled |
| bow | BOH (ribbon) | BOW (bend) | Use "bow" for bending |
| minute | MIN-it (time) | my-NOOT (tiny) | Use "my-noot" for tiny |
| desert | DEZ-ert (sand) | dih-ZERT (abandon) | Use "dih-zert" for abandon |
| object | OB-ject (thing) | ob-JECT (protest) | Use "ob-ject" for protest |
| present | PREZ-ent (gift) | prih-ZENT (to give) | Use "prih-zent" for giving |
| record | REK-ord (disc) | rih-KORD (capture) | Use "rih-kord" for capturing |
| refuse | REF-yoos (garbage) | rih-FYOOZ (decline) | Use "rih-fyooz" for declining |

## Category 2 — Tech terms

| Term | Common error | Write as |
|---|---|---|
| Linux | "LINE-ucks" | Lin-ucks |
| SQL | "squeal" | S-Q-L *or* sequel |
| GUI | — | gooey |
| API / CLI / SSH / DNS / VPN | — | A-P-I, C-L-I, S-S-H, D-N-S, V-P-N |
| IPv4 / IPv6 | varies | I-P-V-four |
| macOS | — | mack-oh-ess |
| iOS | — | eye-oh-ess |
| GPU / CPU / USB | — | G-P-U, C-P-U, U-S-B |
| RAM / ROM | — | ram, rom (already clear) |
| AI | — | A-I *or* ay-eye — pick one and stay consistent |

## Category 3 — Names & proper nouns

| Name | Common error | Write as |
|---|---|---|
| Ramos | "RAM-ohs" | Rah-mohs |
| Sinaloa | "sin-uh-LOW-uh" | Sin-ah-lo-ah |
| Kiev | varies | Kee-ev *or* Kye-ev |
| Qatar | "KAT-ar" | Kuh-tar |
| Nguyen | "NEW-win" | Win *or* Nwin |
| Zhang | "ZANG" | Jahng |
| Jose | "joe-SAY" | Ho-zay |
| Maria | "muh-REE-uh" | Mah-ree-ah |
| Mikhail | "mih-KYLE" | Mee-kah-eel |
| Björk | "bee-YORK" | Bee-york |

Any proper noun not on this list, that a general listener couldn't sound out confidently, gets a
respelling too.

## Category 4 — Acronyms & initialisms

**Rule: 3+ letters → spell out with hyphens, unless it's commonly said as a word.**

| Say as letters | Say as a word |
|---|---|
| F-B-I, C-I-A, N-S-A, G-P-S, A-T-M, C-E-O, L-L-C, P-H-D, H-T-M-L, C-S-S, P-D-F | Nah-sah (NASA), Scoo-bah (SCUBA), Ree-koh (RICO) |

## Category 5 — Numbers

Digits are the single most reliable way to get a garbled vocal. **Always write numbers as words.**

| Written | Risk | Write as |
|---|---|---|
| 1993 | "one nine nine three" | nineteen ninety-three |
| 2024 | "two zero two four" | twenty twenty-four |
| 63 | "six three" | sixty-three |
| 404 | "four zero four" | four-oh-four |
| 9/11 | "nine slash eleven" | nine-eleven *or* September eleventh |

## Category 6 — Commonly misstressed words

| Word | Wrong stress | Write as |
|---|---|---|
| legal | "leh-GAL" | lee-gul |
| illegal | "ILL-ih-gul" | ill-ee-gul |
| data | varies | day-tuh *or* dah-tuh — pick one |
| either / neither | varies | ee-ther / nee-ther *or* eye-ther / nye-ther |
| route | varies | root *or* rowt |
| schedule | varies | sked-yool *or* shed-yool |

---

## Scanning

Before finalizing, grep the lyrics for these:

```
\blive\b|\bread\b|\blead\b|\bwind\b|\bclose\b|\btear\b|\bbass\b|\bwound\b|\bbow\b   # homographs
\bminute\b|\bdesert\b|\bobject\b|\bpresent\b|\brecord\b|\brefuse\b                   # homographs
[A-Z]{2,5}                                                                          # acronyms
\d                                                                                   # ANY digit
```

A digit anywhere in sung text is a defect. Fix every hit before rendering.

## Consistency

Whatever variant you choose for an ambiguous word (A-I vs. ay-eye, root vs. rowt), **use it
everywhere in the track**. A word pronounced two ways across two verses sounds like an error even
when both are individually correct.
