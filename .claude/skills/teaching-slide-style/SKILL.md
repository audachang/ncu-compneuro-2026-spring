---
name: teaching-slide-style
description: >-
  Use when creating, revising, analyzing, or outlining teaching slide decks
  for graduate courses in this repository — especially course slides,
  lecture slides, scientific teaching decks, PowerPoint/PPTX plans, visual
  explanations, storyboard-style lessons, concept diagrams, comparison
  diagrams, flow diagrams, or summary diagrams. Trigger when the user asks
  to "build slides", "make a deck", "design lecture cards", "convert this
  to PPTX", or asks for style matching against the instructor's existing
  decks. This skill preserves the instructor's slide style: clean
  black/white/gray with orange emphasis, restrained visuals, storyboard
  pacing, and diagrammatic consolidation suited to graduate students in
  cognitive neuroscience and behavioural science.
license: Internal use for NS5116 / CompBigData courses
---

# Teaching Slide Style — Claude Code Edition

This skill is the **instructor's house style** for course decks in
`2026_Spring_CompBigData/` and sister repos. It is invoked whenever
Claude Code is asked to design, generate, or revise teaching slides.

> The user's preferred slide style is **not primarily a surface look. It
> is a teaching judgement system.**
>
> Design slides to arrange student attention, control the order in which
> information appears, and make concepts visible step by step.
> A good teaching slide does not merely look polished; it *draws
> understanding*.

---

## When to Use This Skill

Trigger automatically when the user:

- 要求 "build / generate / revise slides / deck / PPTX / 投影片 / 講義"
- 要求 "outline a lecture" or "design slide cards"
- 要求 "match the existing deck style"
- 已經有一份 deck 而要求修訂、加頁、重畫
- 使用 `pptx` skill 並涉及 *teaching* slides（非 sales / product / status update）

When NOT to trigger: business pitch decks, status reports, posters, internal
comms (those have their own conventions).

---

## How to Use This Skill With Claude Code

This skill is **read-only style guidance**. It does not own a build script.
When invoked, Claude Code should:

1. Read this file fully before producing slide content.
2. Identify which two modes (storyboard / consolidation) each slide needs.
3. Use the colour palette and layout rules in §3 when calling `pptx` or
   when writing `python-pptx` / `pptxgenjs` code.
4. Run the Quality Check in §9 before declaring a deck done.
5. If the user has an existing `build_slides.py`, prefer **editing** it
   rather than starting from scratch — the visual idiom (palette,
   font, margins) is the contract.

This skill **does not run code**. It is reference material. Claude Code
remains responsible for the actual build / render / QA loop (typically
via `python-pptx` for this course, with LibreOffice → PDF → JPG for QA).

---

## 1. Audience Assumptions

The decks built with this skill are projected to **graduate students in
cognitive neuroscience, behavioural science, or related disciplines**.

- Bilingual classroom — slides are typically primarily Traditional Chinese
  (繁體中文 / 台灣慣用語) with English retained for code, library names,
  API names, and technical concepts.
- Students have entry-level Python and graduate-level statistics. Skip
  "what is a variable" explanations; do not skip "why is `stratify=y`
  important" explanations.
- The room sees the slides at a distance of ~10–15 m. Body text
  ≥ 14 pt; titles ≥ 28 pt; no sub-14 pt captions on critical content.

---

## 2. Core Principle

Each slide advances **one cognitive action**: ask, contrast, connect,
show change, conclude.

If a slide does two of these at once, split it. If two slides do the
same one, merge them.

This is the most important rule. Surface aesthetics are secondary.

---

## 3. Visual Baseline

### Palette

| Role | Hex | Use |
|------|-----|-----|
| Ink (body text) | `#1F2937` | Default text colour |
| Paper (background) | `#FFFFFF` or `#F7F7F7` | Slide background |
| Mid grey | `#9CA3AF` | Captions, footers, page numbers |
| Light grey | `#E5E7EB` | Card backgrounds, subtle dividers |
| **Emphasis orange** | `#F26B1F` | Reserved for *teaching focus only* — see §5 |
| Code dark | `#0F182E` | Code block background (one consistent token) |
| Code text | `#E2E8F0` | Code block text |

Do **not** introduce a second accent colour. The single orange is the
attention mechanism; multiple accents collapse the hierarchy.

### Typography

- Title: 28–36 pt, bold, ink.
- Subtitle: 14–16 pt, italic, mid grey.
- Body: 14–16 pt, ink.
- Caption / footer: 10–11 pt, mid grey.
- Code: Consolas / monospace, 12–14 pt, code-text colour on code-dark
  background.

CJK consideration: when rendering Traditional Chinese, set the font to
`Microsoft JhengHei UI` (`微軟正黑體`) or `Noto Sans CJK TC` so LibreOffice
and PowerPoint both render glyphs correctly. Mixing into Calibri for
Latin runs is fine; use the same point size on both.

### Layout principles

- Generous whitespace; minimum 0.5" margin from slide edge.
- One left-aligned title block. Bullets left-aligned (never centred).
- No drop shadows on cards. No rounded rectangles for emphasis — those
  read as "product UI", not "lecture board".
- No accent line under titles. (These are the hallmark of AI-generated
  slides and conflict with the storyboard discipline.)
- Cards: thin 0.75 pt ink-grey border, white fill. Used sparingly to
  group related content, not on every slide.

### Anti-patterns (do not do)

- Heavy gradients, full-page decorative backgrounds.
- Stock photos and clip art.
- Multiple accent colours (orange + teal + coral = three priorities → no
  hierarchy).
- "Slide art" — icons-in-circles, multi-coloured bullet dots.
- Text-only slides with no spatial logic.
- Putting both Teaching Storyboard and Consolidation on the same slide.

---

## 4. Two Slide Modes

### 4.1 Teaching Storyboard Mode

Use when students are **entering** a concept.

Purpose: *pace understanding.*

Pattern:

1. Introduce only the **current** actor / element / contrast / problem.
2. Add relationships gradually across consecutive slides.
3. Reveal **local** structure before the whole system.
4. Let a question or tension appear before the answer.
5. Delay conclusions until the setup is cognitively ready.
6. Advance **one** cognitive move per slide.

Do **not** compress all information into one complete infographic when
the concept still needs to unfold.

A storyboard sequence often runs 3–6 slides on a single concept; each
slide adds one element to the same diagram or layout, so students see
the picture growing.

### 4.2 Diagrammatic Consolidation Mode

Use **after** students have accumulated enough understanding and need
organization.

Purpose: *preserve understanding as structure.*

Use structure diagrams, comparison diagrams, flow diagrams, framework
diagrams, and summary diagrams to show:

- relationships
- categories
- cause and effect
- hierarchy
- sequence
- the whole conceptual map

This mode helps students *compare, connect, remember, and transfer*
what they have already encountered.

A good lecture alternates: storyboard → storyboard → storyboard →
**consolidation diagram** → storyboard for next concept.

---

## 5. Orange Emphasis Rules

The orange `#F26B1F` is a finite resource. Spend it on:

- The **one** key conclusion of a slide.
- A single arrow showing the direction of an argument.
- A box around a statement the student must remember.
- The current step of a storyboard (greying out earlier / later steps).

Do **not** spend orange on:

- Slide titles (they're already in heading weight).
- Bullet markers (they aren't a conclusion).
- Decorative borders.
- More than one element per slide.

Rule of thumb: if removing the orange from a slide changes nothing about
where the eye lands, you used it wrong.

---

## 6. Image and Icon Rules

Images are tools for **understanding**, not topic labels.

Avoid symbolic substitution as the primary visual strategy. Do **not**
add an icon merely because a keyword appears (a brain icon for cognition,
a book for learning, a lightbulb for ideas).

Prefer visuals that *show how the concept works*:

- Use arrows to show direction, dependency, change, or causality.
- Use left/right comparison to make differences visible.
- Use flow diagrams to show process and transformation.
- Use layered structures to show hierarchy.
- Use accumulated diagrams across slides when students need to feel a
  concept *growing*.
- Use a single simple shape or sentence when the moment requires focus
  rather than richness.

The standard:

> **Do not draw symbols; draw understanding.**

For technical content — sigmoid curve, ROC curve, confusion matrix,
training-loss curve — embed actual matplotlib plots saved as PNG.
Place them via `slide.shapes.add_picture()` (python-pptx) or
`slide.addImage()` (pptxgenjs). The plot itself is the visual.

---

## 7. Slide Planning Workflow

When planning or revising a deck:

1. Identify the **teaching moment**: entering a concept, contrasting
   concepts, or consolidating concepts already encountered.
2. Choose the mode: Teaching Storyboard or Diagrammatic Consolidation.
3. Define the **cognitive action** for each slide in one verb:
   `ask`, `contrast`, `connect`, `derive`, `show-change`, `conclude`.
4. Decide what must stay **hidden** until later (this is harder than it
   sounds; the urge to over-explain on slide 1 is constant).
5. Use visuals only when they reveal relation, contrast, causality,
   hierarchy, change, or focus. Otherwise, leave whitespace.
6. End sections with a **consolidation slide** when enough has
   accumulated. One consolidation slide every 6–8 storyboard slides is a
   reasonable rhythm.

---

## 8. Build Pipeline (project convention)

For `2026_Spring_CompBigData/` decks:

- Generator: `python-pptx` driven by a single `build_slides.py`
  next to the deck.
- Layout: 16:9 widescreen, 13.33" × 7.5".
- Output: `week-NN-slides.pptx` next to `build_slides.py`.
- Render to PDF for QA: LibreOffice headless.
- QA loop: `pdftoppm -jpeg -r 110 *.pdf slide` → spawn a subagent to
  inspect each slide image → fix → re-render.
- Archive: keep preview JPGs in `archive/slide_previews/` for the
  instructor to skim outside PowerPoint.

When the project already has a `build_slides.py`, treat it as the
canonical visual contract. **Edit it.** Do not rewrite from scratch
unless the visual identity is genuinely changing.

---

## 9. Quality Check (before declaring done)

For each slide, ask:

- Does this slide have **one** clear cognitive job?
- Is information appearing in an order that supports understanding, or
  am I dumping everything at once?
- Does every visual *explain operation* rather than decorate keywords?
- Are important relationships visible through layout, arrows, contrast,
  or grouping?
- Is the orange emphasis reserved for genuine teaching focus?
- Is any slide *too complete too early* — answering before the student
  has asked the question?
- After enough storyboard, is there a **consolidation diagram**?

For the whole deck:

- Does the orange appear at most once per slide, and only on the slides
  that need it?
- Is there a rhythm of storyboard → storyboard → consolidation, or are
  all 30 slides on the same cognitive level?
- Does the deck have a clear opening question and closing synthesis?

---

## 10. Anti-Examples (collected from past decks)

| Issue | Fix |
|-------|-----|
| 22 storyboard slides, 0 consolidation | Insert summary diagram every 6–8 slides |
| Two accent colours competing for "this is important" | Pick one; demote the other to ink |
| Icon next to every bullet | Delete all icons; rebuild card structure |
| Full conclusion shown on slide 1 of a concept | Split into storyboard sequence |
| Code block + diagram + bullets on one slide | Three slides |
| Orange used for the title | Move orange to the conclusion box; restore ink title |

---

## 11. CJK / Bilingual Handling

When the audience is Mandarin-speaking (this course):

- Main narrative (titles, subtitles, body, bullets) in **繁體中文** /
  Traditional Chinese, Taiwan usage.
- Code, function names, library names, API names, paths, and shell
  commands stay in **English**. Mixing them inline is normal:
  > "使用 `train_test_split` 把資料切成 75/25。"
- First-occurrence loanwords carry a 中文簡注:
  > "AUC (Area Under Curve, 曲線下面積)"
- Punctuation: 全形 for Chinese clauses (，。：；) and 半形 for
  English / code segments. Mixing is fine; do not force one style across
  both.
- Avoid translating technical terms that students will encounter on
  GitHub / Stack Overflow in English. `cross-entropy` stays
  `cross-entropy`, not 交叉熵, unless the student community uses the
  Chinese form first.

---

## 12. Related Skills

- `pptx` (Anthropic skill) — provides the rendering primitives and QA
  conversion scripts. Use *after* this skill has shaped the cognitive
  structure of the deck.
- `theme-factory` — has alternative palettes; ignore for this course
  unless the user explicitly opts in.
- `canvas-design` — for posters / one-page visuals, not lecture decks.

---

*Adapted from `C:\Users\audachang\.codex\skills\teaching-slide-style\SKILL.md`
(Codex form) into the Claude Code skill format used by this
repository. Last updated: 2026-05-18.*
