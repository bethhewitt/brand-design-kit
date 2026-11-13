---
name: brand-one-pager
description: Use when asked for an on-brand one-pager, sell sheet, fact sheet, leave-behind, product or service overview, or single-page brief/flyer for the brand in the current repository.
---

# Brand one-pager

One page, one idea, scannable in 30 seconds. A one-pager is a sales or
briefing document, not a shrunken website.

**First:** run `brand-preflight` (the DESIGN.md check) if it hasn't run in
this task. Then read `../brand-design/SKILL.md` and complete core steps 1–3
(resolve the brand, ask for the output, collect content).
Build with core step 4 plus the rules below, then finish with core steps 5–6
(`check.py`, the QA checklist, the hand-over list). Paths below are relative
to `../brand-design/`.

## Step 2 — ask every time

**Format** (single choice):
- PDF, A4 portrait (print and email attachment)
- PDF, US Letter portrait
- PNG, for sharing in chat or social (1240×1754 for A4, at 2×)
- HTML page (web-hosted one-pager)

**Content to request if missing:** audience; the one thing the reader
should do next (CTA plus a real URL or contact); 3–5 key points; any
proof (numbers, quotes, logos) **with sources**.

## Structure

Keep to 300–450 words. Default order, top to bottom:

1. **Masthead.** Logo file (top left), document type or category label
   (top right, small caps, tracked).
2. **Headline + promise.** A display headline of 12 words or fewer, plus one
   sentence on what changes for the reader.
3. **Context.** 2–3 sentences on the problem or situation.
4. **Key points.** 3 (or 4) blocks, each a short heading plus 1–2 sentences.
   Use a grid, or a numbered list down a narrow column with a visual in the
   wide one.
5. **Proof.** A stat row (real numbers only, each with a source line) **or**
   one customer quote with attribution. Never both if space is tight.
6. **Offer / how it works.** Optional: 3 numbered steps or a short spec list.
7. **CTA + contact block.** One action, a real URL or QR placeholder, the
   contact name and email if supplied.
8. **Footer.** Legal line, website, date or version.

Vary from the default when the content asks for it. A comparison table or a
single big diagram can replace steps 4–6.

## Build

- **PDF/PNG:** one `<div class="page">` sized `210mm × 297mm` (or
  `8.5in × 11in`) with `@page { size: A4; margin: 0 }`. Inner margin is at
  least 14mm. Use `overflow: hidden` on `.page` so overflow shows up in the
  render warning instead of spilling onto page 2.
- **HTML:** start from `assets/web-seed.html` and use Layouts 1/2, 3, 4/5, 6.
- Print discipline: solid fills, not `rgba()`
  tints; hairline rings instead of heavy shadows; `font-variant-numeric:
  tabular-nums` on numbers; body 10–11pt (≈13–15px) for print.

Craft files: `typography.md`, `typography-hierarchy.md`, `color.md`, `anti-ai-slop.md`.

## Export

```bash
bash ../brand-design/scripts/render.sh one-pager.html one-pager.pdf
bash ../brand-design/scripts/render.sh one-pager.html one-pager.png --selector .page --scale 2
```

## Task-specific checks

- Fits on exactly one page. If the render warns about overflow, cut words
  before shrinking type below 10pt.
- The headline and CTA are readable from arm's length (squint test on the PNG).
- No more than one accent-coloured element per quadrant.
