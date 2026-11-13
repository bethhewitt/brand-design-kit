---
name: brand-social-post
description: Use when asked for on-brand social media graphics — a post, carousel, LinkedIn document, Instagram post or story, X/Twitter image, Facebook graphic, quote card, stat card, or announcement graphic — for the brand in the current repository.
---

# Brand social post / carousel

Social graphics are read on a phone, in a feed, in under two seconds. That
means big type, one idea per frame, and the brand recognisable from a
thumbnail.

**First:** run `brand-preflight` (the DESIGN.md check) if it hasn't run in
this task. Then read `../brand-design/SKILL.md` and complete core steps 1–3.
Paths below are relative to `../brand-design/`.

## Step 2 — ask every time

**Platform and size** (multi-select allowed):

| Option | Size (px) |
|---|---|
| Instagram / LinkedIn square | 1080×1080 |
| Instagram / LinkedIn portrait | 1080×1350 |
| Story / Reel cover | 1080×1920 |
| LinkedIn link / landscape | 1200×627 |
| X / Twitter | 1600×900 |
| Facebook link | 1200×630 |

**Single or carousel?** For a carousel, ask how many frames (3–10) and
whether it's a LinkedIn document carousel (exported as PDF) or an image
carousel (PNG per frame).

**Content to request if missing:** the message or the source to adapt (blog
post, report, announcement); the CTA; whether to write the caption, alt
text and hashtags too.

## Composition

- **Frame types:** hook / statement, stat, quote, list (3 points maximum),
  how-to step, announcement, CTA. A carousel runs hook → value frames → CTA.
- **Type size at 1080px wide:** headline 64–120px, supporting text at least
  32px, nothing under 24px. Maximum ~20 words per frame; the hook frame
  ideally 8 or fewer.
- **One focal element per frame.** The accent is used once or twice.
- **Consistent system across a carousel:** same margins (at least 72px),
  same logo position and size, same index style (`01 / 06`, in the brand's label style; mono only if the brand uses one), and a
  layout grid that repeats while the content changes. The last frame
  carries the CTA and the logo.
- **Safe zones:** stories keep the top 250px and bottom 300px free of key
  content. Square posts keep text away from the outer 60px.
- **Imagery:** brand photography or illustration from the repo first. If
  there's none, use type and colour fields. Never use stock-placeholder
  URLs or invented screenshots.
- The brand should be identifiable with the logo covered (colour, type,
  layout signature).

## Build

One HTML file, with every frame a `<div class="frame">` at exact pixel size
(`width:1080px;height:1350px;overflow:hidden`), stacked with a gap. For
several sizes of the same post, make one frame per size and adapt the
layout to each. Don't just scale it.

Craft files: `typography.md`, `typography-hierarchy.md`, `color.md`, `anti-ai-slop.md`.

## Export

```bash
# PNG per frame, exact platform pixels
bash ../brand-design/scripts/render.sh post.html post.png --selector .frame --scale 1 --width 1700
# LinkedIn document carousel: add @page { size: 1080px 1350px; margin: 0 } and a page break after each .frame
bash ../brand-design/scripts/render.sh post.html carousel.pdf
```

## Hand-over extras

If asked, give the post caption (platform-appropriate length, brand voice,
CTA at the end), alt text per frame, and hashtags (3–5, relevant). Don't
invent engagement claims or statistics in the caption either.

## Task-specific checks

- View each PNG at 25% size. Is the message still readable and the brand
  still recognisable?
- No frame overflows (render warns). Every carousel frame index is correct.
