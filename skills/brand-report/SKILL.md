---
name: brand-report
description: Use when asked for an on-brand report, whitepaper, e-guide, ebook, lead magnet, case study, research or annual/quarterly report, or any multi-page document for the brand in the current repository.
---

# Brand report / whitepaper

A multi-page reading document. It needs authored hierarchy, a steady reading
rhythm and figures that are honest about their data.

**First:** read `../brand-design/SKILL.md` and complete core steps 1–3.
Paths below are relative to `../brand-design/`.

## Step 2 — ask every time

**Format** (single choice):
- PDF, A4 portrait
- PDF, US Letter portrait
- PDF, 16:9 landscape (screen-read report)
- HTML long-read page (web article / gated content page)

**Also ask:** whether to export PNG previews of the cover plus 2 key pages
(useful for promotion).

**Content to request if missing:** the source material (doc, notes, data
files, or repo paths); audience and purpose (inform, persuade, capture
leads); title; author or byline; whether a contents page and
methodology/sources section are wanted. Work from the user's text. Edit
it for flow, but don't add claims.

## Structure

1. **Cover.** Logo, title (display, may run 2–3 lines), subtitle, date or
   edition, author. One strong visual move: a big colour field, an oversized
   type crop, or a brand image from the repo.
2. **Contents** (when there are more than 6 pages). Section numbers in mono,
   leader dots or rules.
3. **Executive summary / key findings.** 3–5 findings, each a bold sentence
   plus a short supporting line. This is the page most readers stop on.
4. **Sections.** Each opens with a number, a title and a 1–2 sentence deck.
   Body text sits in 1 column (portrait) or 2 (landscape). Alternate dense
   pages with breathing pages: a pull quote, a full-width figure, a stat
   spread.
5. **Figures.** Inline SVG charts built from the real data, coloured from
   tokens (`--accent`, `--accent-2`, `--fg-2`, `--muted`). Label lines
   directly instead of using a legend, and put a "Source: …" line under
   every figure.
6. **Methodology / sources**, if any data was used.
7. **Back page.** About the company, CTA, contact, legal.

## Build

- **PDF:** one `<section class="page">` per page with a fixed size
  (`210mm × 297mm`, `8.5in × 11in`, or `338.67mm × 190.5mm` for 16:9),
  `@page { size: …; margin: 0 }`, and `overflow: hidden`. Paginate
  manually. When the render warns that a page overflows, move content to
  the next page; never shrink body text below 10pt.
- Running footer on every page except the cover: document title (left), page
  number (right), mono, `--meta` colour.
- **HTML:** start from `assets/web-seed.html`, body column `max-width: 68ch`,
  sticky contents rail optional on desktop.
- Body 10.5–11.5pt print / 17–19px web; leading 1.5–1.6.

Craft files: `typography.md`, `typography-hierarchy.md`,
`typography-hierarchy-editorial.md`, `color.md`, `anti-ai-slop.md`; add
`accessibility-baseline.md` for HTML.

## Export

```bash
bash ../brand-design/scripts/render.sh report.html report.pdf
bash ../brand-design/scripts/render.sh report.html preview.png --selector .page --scale 1
```

The second command writes every page as a PNG. Keep the cover and the best
2, delete the rest unless asked.

## Task-specific checks

- Every chart value ties back to a source file or the user's data. No
  "illustrative" numbers.
- No orphaned headings at the bottom of a page, and no single lines stranded
  at the top.
- The contents page numbers match the rendered PDF.
- The key-findings page alone gives the reader the whole story.
