---
name: brand-email-graphic
description: Use when asked for an on-brand email header, banner, hero image, inline email graphic, newsletter graphic, email signature banner, or a full HTML marketing email or newsletter template for the brand in the current repository.
---

# Brand email graphic / email

Email is the most hostile rendering environment. Many clients ignore CSS
variables, web fonts and modern layout, and many readers have images off.
Design for that.

**First:** read `../brand-design/SKILL.md` and complete core steps 1–3.
Paths below are relative to `../brand-design/`.

## Step 2 — ask every time

**What to make** (single choice):
- Header / hero banner image (PNG): 600×200, 600×300, or custom height
- Inline graphic (PNG): stat card, announcement, event card, product feature
- Signature banner (PNG): 600×120
- Full HTML email (single-column template, 600px)
- Set: header + inline graphic + footer banner

**Also ask:** light or dark email background (graphics must sit on it
cleanly); export at 2× (default, crisp on retina) or 1×.

**Content to request if missing:** the headline or message; CTA plus a real
URL (for full emails); the email client or ESP if known (Mailchimp,
HubSpot, Klaviyo…), since some need merge tags such as `*|UNSUB|*`.

## Graphics (PNG)

- Build each graphic as a `<div class="frame">` at the display size (for
  example 600×300). Export at `--scale 2`, so the file is 1200px wide and
  displays at 600.
- Text in images must be at least 22px at display size, 6–10 words at most.
  The image must make sense even when the email body repeats the message.
- Keep 24px safe margins. Put the logo file in a consistent corner or omit
  it if the email masthead already shows it.
- Keep each PNG under about 200KB. Prefer flat fills and type over photos.
  For photos, also export a JPG.
- Write alt text for each image in your reply.

## Full HTML email

Structure, adapted from a product-launch email pattern: masthead (logo
image, optional 2–3 text links) → hero image → optional sentence-case label → headline → 2–3
sentence body → **one** bulletproof CTA button → optional 2×2 stat or
feature grid → footer (logo, address, unsubscribe, view-in-browser).

Hard rules:
- Use `<table role="presentation">` for layout, 600px max width, centred, and
  inline `style=""` on every element. Use no `<style>`-only layout and no
  flexbox or grid.
- **Resolve tokens to literal hex values.** CSS variables don't work in
  Outlook or Gmail. Every hex value must come from the brand block. Keep the
  brand block as an HTML comment at the top for traceability.
  `check.py`'s raw-hex P1 doesn't apply to emails; matching the brand
  values does.
- Fonts: brand web font first, then a safe fallback (Arial/Helvetica or
  Georgia) that keeps the hierarchy when the web font is dropped.
- Buttons: a table cell with a background colour and padding plus a link.
  Never use an image for the button.
- Headline and CTA are live text, never baked into an image. Every image has
  `alt`, and the email still makes sense with images off.
- Include a hidden preheader line (40–90 characters).

Craft files: `typography.md`, `color.md`, `anti-ai-slop.md`, `accessibility-baseline.md`.

## Export

```bash
bash ../brand-design/scripts/render.sh graphics.html header.png --selector .frame --scale 2
bash ../brand-design/scripts/render.sh email.html email-preview.png --width 680 --full-page
```

## Task-specific checks

- Graphics look right on both white and the chosen background (check edges
  and anti-aliasing).
- Full email: view a preview at 375px width (`--width 375`). It must reflow
  to a single readable column.
- Exactly one primary CTA. Unsubscribe and address are present in full emails.
