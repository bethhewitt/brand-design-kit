# Brand file audit and rewrite

Use when the user asks to audit, check, clean up, standardise, migrate or
rewrite a repo's `DESIGN.md` / brand guidelines into this skill's structure,
or to set up brand files for a repo.

The rewrite **reorganises what the brand already says**. It never improves,
modernises or fills gaps with taste. Every value in the output traces to a
source file or to the user's answer.

## 1. Gather

1. Run `python3 <brand-design>/scripts/discover.py` from the repo root.
2. Read every written brand doc it lists (DESIGN.md, BRAND.md, guideline
   PDFs, style guides) in full, plus the token, theme and Tailwind files and
   the top stylesheets.
3. Note the logo, font and imagery files that exist.

## 2. Audit — report before writing anything

Give the user this report and stop for confirmation:

```
Brand audit: <brand name>

Sources read: brand/DESIGN.md, src/styles/tokens.css, tailwind.config.js, …

Sections (target structure: assets/DESIGN.template.md)
  ✔ 1 Visual theme        from DESIGN.md §1
  ◐ 2 Colour palette      roles missing for surface, border
  ✔ 3 Typography          …
  ✘ 4 Component styling   not documented
  … all 10

Required tokens (references/brand-contract.md)
  stated:    bg, fg, accent, font-display, font-body
  derivable: surface, muted, border, accent-on   (will be marked derived)
  missing:   —

Conflicts
  accent: DESIGN.md #1f5c4a vs tailwind.config.js #1e5b49 → propose DESIGN.md (written docs win)

Missing files
  DESIGN.md names "Söhne" but no font files or licence are in the repo
  logo-white.svg referenced but not found

Contrast (check.py --brand on the proposed tokens)
  muted on bg 4.1:1, fails 4.5:1 → muted is derived, propose #5f6f72

Content not covered by the template (kept in an "Additional notes" section)
  …
```

Use ✔ complete, ◐ partial, ✘ missing. Ask the user to settle each conflict and
each failing **stated** colour. Never silently pick a side on a stated value.

## 3. Rewrite — after confirmation

1. **DESIGN.md.** Rebuild it in the 10-section order of
   `assets/DESIGN.template.md`, at the same path as the existing file (or at
   the repo root if none exists).
   - Move every existing rule, value, example and piece of voice guidance
     into its section. Keep the original wording where it works.
   - Content that fits no section goes in a final `## Additional notes`.
     Nothing is dropped.
   - Gaps become `TODO: needs decision — <what's missing>`, never invented
     values.
   - Fill the colour and type tables from the resolved values.
2. **tokens.css.** Write or update it next to DESIGN.md with the contract
   token names (`assets/tokens.template.css`). Values must match DESIGN.md
   exactly. Mark derived tokens `/* derived */`. If the repo already has a
   tokens file the app depends on, don't rename its variables. Add the
   contract names as aliases, e.g. `--accent: var(--brand-pine);`.
3. **Keep the old version recoverable.** If the repo is under git, the diff
   is the record; say so. If it isn't, save the original as
   `DESIGN.legacy.md` first.
4. **Re-check.** Run `check.py --brand tokens.css`. If its aliases point at
   variables defined in another file that tokens.css doesn't `@import`, pass
   that file first: `check.py --brand src/styles/app-tokens.css tokens.css`.
   No check may SKIP. All stated colours must be unchanged from the sources
   the user approved.
5. **Reset the cache.** Delete `.brand-design/` so the next design task
   re-resolves the brand from the new files. Then run
   `python3 ../brand-preflight/scripts/preflight.py --save` (path relative
   to `<brand-design>`) and include its new verdict in the handover.

## 4. Hand over

Summarise what moved where, any values changed (only derived ones, or ones
the user approved), the open TODOs as a checklist, and the files touched.
Don't commit unless asked.

## Common mistakes

- Writing the new file before the user has seen the audit.
- "Tidying" a stated hex or font to something nicer.
- Dropping guidance that doesn't fit a template section.
- Renaming token variables the app's code already uses.
- Leaving a stale `.brand-design/` cache behind.
