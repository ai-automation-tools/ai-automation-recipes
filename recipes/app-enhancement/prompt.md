# App Enhancement

Goal: ship **one** small, high-value, additive enhancement to **one** static web app, and write a
short technical note about it. Work like a careful senior engineer shipping a small PR to
production. **When in doubt, do less.** A modest, correct, additive improvement is worth more than
an ambitious change that breaks a working app.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

**One exception to the contract above, and only this one:** the app you are enhancing is a copy at
**`{{APP_COPY}}`**. Edit that copy in place with Read, Edit and Write. Those edits are the
deliverable: the runner diffs the copy against the original into `enhancement.patch` and, when the
user asked for it, applies the patch for them. Touch nothing outside that folder and this staging
folder. Never edit the original app.

--------------------------------------------------
## THIS RUN

**App: `{{APP}}`** (chosen by the runner as the least-enhanced app in the folder; the others are
{{OTHER_APPS}}). Its files:

{{APP_FILES}}

**Earlier enhancements to this app** (date · title — summary). Never repeat one; prefer a different
part of the app.

{{PAST}}

**All earlier enhancements**, every app:

{{EXISTING}}

--------------------------------------------------
## HARD RULES

1. **Exactly one enhancement.** Don't bundle two features. Scope tightly.
2. **Additive and backward-compatible only.** A new feature, or an improvement to an existing one,
   that changes or removes no existing behaviour. Existing links, data, keyboard shortcuts and
   saved state keep working exactly as before. No rewrites, no renamed or deleted files, no removed
   features.
3. **At most three files change**, and a new file is under 50 KB. The runner rejects more.
4. **It must work with the app's real data, now and later.** If the app renders a data file or a
   manifest, derive everything from that data's actual shape: never hardcode a count, a title or a
   list, and use optional chaining and fallbacks so an entry missing your new field can't crash
   the app. Assume the data grows and varies.
5. **No new dependencies.** Vanilla HTML, CSS and JS only. No `<script>` or `<link>` to an external
   host, no package manager, no build-system changes.
6. **Match the app's existing style**: naming, indentation, structure, how it already binds events
   and renders. Keep the diff minimal and readable.
7. **The page must still load clean.** The runner checks every local reference in `index.html`,
   runs `node --check` on each script you touched, and loads the page in a headless browser; an
   uncaught error fails the run.

--------------------------------------------------
## HOW TO WORK

1. **Read the app in full** before writing a line: `index.html`, its stylesheet, its scripts, and any
   data file it loads. Understand its actual data shape and how it degrades when a field is absent.
2. **Pick the single highest-value enhancement** that fits the rules: a filter, a sort, a search box,
   a keyboard shortcut, a share or export action, an empty state, an accessibility fix (focus order,
   labels, contrast), a small quality-of-life affordance, or a new view of data the app already has.
   Small and self-contained, implementable in one or two files, low blast radius.
3. **Implement it in the copy.** Progressive enhancement: the app must still work if your feature's
   data is missing for some or all entries.
4. **Check your own work**: re-read every changed file, trace the new code path once by hand, and
   confirm nothing existing changed. If you cannot make a change you are sure is safe, make a
   smaller one. Only if **no** safe additive change exists at all, end with the JSON block and an
   `error` saying why; that is rare.
5. **Write the note.**

--------------------------------------------------
## SKILLS

{{SKILLS}}

Load `llm-writing` and `humanizer` before writing `enhancement.md`; it is read by a person. Ignore
their workflow and output instructions, and never let them touch the code.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `enhancement.md`

```markdown
# <App display name> — <short enhancement title>

- **App:** `{{APP}}`
- **Date:** {{DATE}}
- **Type:** New feature | Enhancement of existing feature
- **Files changed:** <list, relative to the app folder>

## What it does
<2–5 sentences: the user-facing behaviour, what someone using the app can now do.>

## Why
<1–3 sentences: the gap it fills.>

## How it works
<The implementation: which functions and elements, the data it reads, how it stays
backward-compatible and defensive.>

## Compatibility
<What happens when the new data is missing, how it behaves as the data grows, why it can't break
existing behaviour.>

## Verification
<What you checked by hand. The runner adds its own reference, syntax and browser checks.>
```

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<app display name> — <short enhancement title>",
  "slug": "{{APP}}-<short-kebab-title>",
  "summary": "<one line: what the app can now do>",
  "app": "{{APP}}",
  "files_changed": <number of files you changed or added in the copy>,
  "error": null
}
```
