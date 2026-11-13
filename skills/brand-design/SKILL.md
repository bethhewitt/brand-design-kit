---
name: brand-design
description: Use when asked to design, make or produce an on-brand visual asset inside a repository (one-pager, report, whitepaper, email graphic or email, social post or carousel, landing page) or to "make it on brand", "use our brand", or design for a brand whose files live in the repo. Also use when asked to audit, set up, standardise or rewrite a repo's DESIGN.md, brand guidelines or design tokens.
---

# Brand Design

Produce marketing and communication assets that are on brand for whatever
repository you are in. The brand comes from the repo's own files, never from
taste or memory. This skill is the shared core. Each asset type has a task
skill that runs this core and then adds its own layout rules.

`<brand-design>` below means this skill's base directory.

## Task skills

| Asset | Skill |
|---|---|
| One-pager, sell sheet, fact sheet, product brief | `brand-one-pager` |
| Report, whitepaper, e-guide, case study, annual or quarterly report | `brand-report` |
| Email header / banner / inline graphic, or a full HTML email | `brand-email-graphic` |
| Social post, carousel, story, LinkedIn / Instagram / X / Facebook graphic | `brand-social-post` |
| Landing page, campaign page, waitlist page, product page | `brand-landing-page` |

If the request clearly matches one, invoke that skill. It sends you back
here for steps 1–3. If it matches none, say which five exist and offer the
closest. For something genuinely different, apply steps 1–3 and 5–6 with
the general web seed.

**Auditing or rewriting brand files** (not producing an asset): follow
`references/brand-audit.md` instead of the core workflow below.

## Core workflow (every task, every time)

1. **Resolve the brand.** Follow `references/brand-discovery.md`. The output
   is `.brand-design/brand-block.css` and `.brand-design/brand-notes.md` at
   the repo root. Don't start layout until the user has seen the brand summary
   once in this repo.
2. **Ask for the output, every time.** Use the AskUserQuestion tool, or plain
   questions if it isn't available. Offer the task skill's format and size
   menu, even if the user named a format earlier in another task. Formats
   differ per job. Ask in the same call for any missing content the task
   skill marks as required.
3. **Collect the content.** Use only what the user supplied or what exists in
   the repo (docs, READMEs, data files, existing copy). Never invent stats,
   quotes, customer names or claims. Leave a labelled placeholder
   (`[QUOTE: needs source]`) and list each one in your reply.
4. **Build.** Write the HTML source to
   `brand-output/<task>/<YYYY-MM-DD>-<slug>/`, or wherever the user or the
   repo's own instructions (CLAUDE.md) say drafts go. Paste the brand block
   as the first `:root` rule. Embed logos as `data:` URIs (resized to about
   4× their display width) so the HTML works when opened on its own, for
   example in a preview pane; trimming a logo file's transparent padding is
   fine. Reference font files with relative paths. Read the
   craft files the task skill lists from `references/craft/`.
5. **Export and check.** Render with
   `bash <brand-design>/scripts/render.sh <in.html> <out.png|pdf> [options]`.
   The first run installs Chromium, which takes about a minute. Run
   `python3 <brand-design>/scripts/check.py <in.html>`, then **look at the
   rendered file** and walk `references/qa-checklist.md`. Fix and re-render
   until P0 is clean.
6. **Hand over.** List the files written, the brand sources used, any
   placeholders needing input, and anything you couldn't make on brand (for
   example, no licensed font file in the repo).

## Shared resources

| File | Use |
|---|---|
| `references/brand-discovery.md` | Finding and resolving the repo's brand |
| `references/brand-audit.md` | Auditing existing brand files and rewriting them into the standard structure |
| `references/brand-contract.md` | Token names every template reads, and the DESIGN.md format |
| `references/qa-checklist.md` | Pre-handover checks |
| `references/craft/*.md` | Typography, hierarchy, editorial type, colour, accessibility, anti-AI-slop rules |
| `assets/web-seed.html` + `assets/layouts.md` | Token-driven base page and 8 section layouts |
| `assets/DESIGN.template.md`, `assets/tokens.template.css` | Starter brand files for repos without one |
| `scripts/discover.py` | Lists brand files in the repo; `--check-cache` checks whether the resolved brand is fresh |
| `scripts/check.py` | Mechanical QA on HTML; `--brand` checks token contrast |
| `scripts/render.sh` | HTML → PNG / PDF (multi-frame with `--selector`) |

## Common mistakes

- Designing before the brand is resolved, then retrofitting colours.
- Treating a remembered format choice as permission to skip step 2.
- Hardcoding a hex value "just this once" outside the brand block.
- Typing the company name in a font instead of using the logo file.
- Judging the result from the HTML source instead of the rendered output.
- Writing a plausible statistic to fill a stat slot.
