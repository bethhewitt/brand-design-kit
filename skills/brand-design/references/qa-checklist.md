# QA checklist

Run before handing anything over. First `python3 <brand-design>/scripts/check.py <file.html>`.
Every P0 it reports must be fixed. Then look at the **rendered** output (the
PNG/PDF, or a screenshot of the HTML) and walk this list. Don't judge from
the source alone.

## P0 — must pass

- [ ] The brand block is the first `:root` rule and matches `.brand-design/brand-block.css`.
- [ ] No colour or font outside the brand block, except neutrals derived with `color-mix()` from tokens.
- [ ] Headlines use `var(--font-display)` and body uses `var(--font-body)`. The render shows the real brand fonts, not fallbacks (render.sh warns when a font fails to load).
- [ ] The real logo file from the repo is used, not retyped text, wherever the format has a logo slot. It is never stretched, recoloured or placed on a background that fails the brand's logo rules in `brand-notes.md`.
- [ ] No invented facts: every number, quote, name, date and claim came from the user or the repo. Gaps use a labelled placeholder (`[STAT: needs source]`) and are listed in your reply.
- [ ] No filler copy, no template leftovers, no dead links.
- [ ] Text contrast is at least 4.5:1 (3:1 for text 24px+ or 19px+ bold).
- [ ] Open the HTML file itself, not just the export: every image loads.
- [ ] Output is at the exact size the user chose. Nothing is clipped or overflows the frame or page.
- [ ] The seven cardinal sins in `craft/anti-ai-slop.md` are absent.
- [ ] **Side by side with the brand's own work.** Open the render next to two
      pieces listed under `## Observed in finished work` in `brand-notes.md`.
      Would someone who knows the brand believe the same person made all
      three? Check, in order: which colours take the area, what colour the
      headings and body are, the signature components, and how big the
      biggest elements are relative to the rest. Any mismatch with the
      observed notes is a P0, even when every token is correct.

## P1 — should pass

- [ ] One focal point per frame, screen or page. Accent appears about twice at most.
- [ ] Type follows `craft/typography.md`: no all-caps labels or eyebrows, display tracked negative (Latin only), body lines 50–75 characters, no more than 3 weights.
- [ ] Hierarchy reads in three levels (`craft/typography-hierarchy.md`): you can tell what to read first, second and third from a thumbnail.
- [ ] Copy is in the brand's voice (`brand-notes.md`). The CTA says what happens ("Download the report"), not "Learn more".
- [ ] Spacing comes from one scale and alignment is consistent. Nothing looks "nearly aligned".

## P2 — polish pass

Adapted from the Impeccable design-polish workflow:

1. **Audit.** Name the 3 highest-impact problems in hierarchy, spacing, colour, type and responsiveness.
2. **Polish.** Fix those 3. Prefer a few decisive fixes over broad cosmetic churn, and keep the user's content and intent.
3. **Harden.** Check narrow widths (web/email), long names or numbers, missing images, and print margins (PDF).
4. **Soul check.** Could someone outside the company identify the brand from a thumbnail? If not, push the one distinctive move further.
