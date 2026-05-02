---
name: edslides
description: >
  Create professional HTML slide deck presentations. Use this skill whenever the
  user wants to create slides, a presentation, a deck, or course material in HTML
  format. Triggers on: "create slides", "make a presentation", "build a deck",
  "diapositivas", "presentación", "slides for my course", "course slides", or any
  request to turn an outline or content into a visual slide deck. Also use when
  the user provides slide titles and bullet content and asks to "make it visual"
  or "turn this into a presentation". The user can define the visual style (colors,
  fonts, theme); if not specified, ask before generating. Supports quizzes as a
  special slide type. Always produces a single downloadable HTML file per deck
  with keyboard/click navigation. The layout library is extensible — invent new
  layouts when the content demands something not covered by the existing types.
---

# EDslides — HTML Slide Deck Generator

Generates self-contained HTML slide decks: configurable theme, modern typography,
smooth transitions, keyboard navigation, and optional interactive quizzes.

**Always read before writing any code:**
- `references/slide-types.md` — built-in layout library + rules for inventing new ones
- `references/html-spec.md` — full CSS scaffold and technical requirements
- `references/themes.md` — theme presets and how to build custom themes

---

## Workflow

### 1 · Gather content and style

Collect from the user (or infer from context):
- **Deck title** and optional subtitle/eyebrow
- **Language** — auto-detect from content; apply to all UI labels (nav, quiz, feedback)
- **Visual style** — see "Style negotiation" below
- **Cover slide** — include unless the user says otherwise
- **Slides** — for each: title + content
- **Quiz questions** (if any) — question text + 4 options + correct answer + optional explanation

**Style negotiation:**
If the user specifies a style, honor it exactly.
If the user says nothing about style, ask one focused question before generating:

> "¿Alguna preferencia de estilo? Por ejemplo: oscuro con acento dorado (como el módulo 1),
> oscuro azul, claro minimalista, o dime un color y lo adapto."

If the user is in a hurry ("just make it"), default to `dark-gold`.

### 2 · Choose and invent slide layouts

Read `references/slide-types.md` for the full built-in library.

**Inferring layout from content shape:**
| Content shape | Suggested layout |
|---|---|
| Two things to contrast | VS Split or BVS Comparison |
| Named sequential steps/artifacts | Artifact Flow or Flow Steps |
| Feature/tool showcase (3–4 items) | Tools Grid |
| Historical progression | Timeline |
| 4 reasons / benefits | Reasons Grid |
| Named attributes or config options | Attribute Grid |
| Multiple audiences or contexts | Context Columns |
| Feature matrix (3 columns) | Comparison Table |
| End-of-module review | Quiz |

**When to invent a new layout:**
If the content doesn't fit any existing type, design a new one. Rules for custom layouts:
- Must use the same CSS variables (`--bg`, `--surface`, `--accent`, etc.)
- Must include `animation: fadeUp 0.5s ease both` with staggered `animation-delay`
- Must respect the same spacing rhythm (`max-width: 900px`, `margin-top: 36–40px`)
- Add the new layout's CSS inside the `<style>` block under a clearly named comment
- Document it briefly in a comment above the HTML so future edits are easy

Aim for layout variety — avoid the same type more than twice in a row.

### 3 · Build the theme

Read `references/themes.md` for presets.
For a custom style requested by the user:
1. Pick the closest preset as a base
2. Override `--accent` and `--accent2` to match the user's color
3. Adjust `--bg`, `--surface`, `--surface2` to match the overall mood (dark vs light)
4. Keep `--green`, `--red`, `--blue` as semantic colors — don't tint them with the theme accent

### 4 · Generate the HTML file

Follow `references/html-spec.md` exactly. Key rules:
- Single `.html` file, fully self-contained (only Google Fonts as external dependency)
- One `<style>` block, one `<script>` block at the bottom
- `TOTAL` in JS must equal the exact number of `<div class="slide">` elements
- Slide IDs: `s0`, `s1`, `s2` … in order; first slide gets `class="slide active"`
- All UI text (nav buttons, quiz labels) must match the deck's detected language
- Quiz JS lives inside the main `<script>` block — never a separate `<script>` tag

### 5 · Save and present

Save to `/mnt/user-data/outputs/<deck-name>.html` and call `present_files`.

---

## Content principles

**One idea per slide.** If a slide needs more than 6 bullet points, split it.

**Anchor every title.** Wrap the key word or phrase with `<span class="accent">word</span>`.

**Rhythm matters.** Alternate dense layouts (tables, grids) with sparse ones (VS split,
flow steps). A deck that feels monotonous loses attention fast.

**Quiz questions test understanding, not memory.** Avoid "what year was X introduced"
style questions. Write questions that require the student to apply or compare concepts.
If the user doesn't provide questions, generate 4–5 from the deck content.

---

## Reference files

| File | When to read |
|---|---|
| `references/slide-types.md` | **Always** — before writing any HTML |
| `references/html-spec.md` | **Always** — CSS scaffold and checklist |
| `references/themes.md` | When building or customizing a theme |
