# Brand design kit

Six Claude Code skills that make on-brand marketing assets from the brand
files already in your repository: one-pagers, reports, social posts and
carousels, email graphics and full HTML emails, and landing pages. Each one
is built as HTML, checked, and exported to PNG or PDF.

The kit has no brand of its own. It reads yours (a `DESIGN.md`, a tokens
file, your CSS, your logo and font files) and maps it onto one small set of
design tokens, so every template works for every brand. If your repo has no
brand files yet, it helps you write them.

## What's inside

| Skill | Makes |
|---|---|
| `brand-design` | The shared core: finds and resolves your brand, checks contrast, renders, runs QA. Also audits or writes `DESIGN.md` and tokens. |
| `brand-one-pager` | One-pagers, sell sheets, fact sheets (A4 or Letter PDF, PNG, HTML) |
| `brand-report` | Reports, whitepapers, case studies, e-guides (multi-page PDF or HTML long-read) |
| `brand-social-post` | Single posts and carousels for LinkedIn, Instagram, X and Facebook (PNG per frame, or a PDF document carousel) |
| `brand-email-graphic` | Email headers, inline graphics, signature banners, full table-based HTML emails |
| `brand-landing-page` | Self-contained landing pages, or pages built into your existing web app |

You don't call the core yourself. Ask for the asset and the matching skill
runs it.

## Requirements

- **Claude Code** (CLI, desktop app or IDE extension).
- **Python 3.8 or later** for the discovery and QA scripts. Standard library only.
- **Node.js 18 or later** for PNG and PDF export.
- **bash.** macOS and Linux have it. On Windows, use WSL or Git Bash.
- About 450 MB of disk for the export runtime.

The first time you export, `render.sh` installs Playwright into a per-user
cache (`~/.cache/brand-design/`) and Chromium into Playwright's own cache
(`~/Library/Caches/ms-playwright` on macOS, `~/.cache/ms-playwright` on
Linux). It takes a minute or two, needs internet access once, and never
touches your project's `package.json`. To put the Playwright install
elsewhere, set `BD_RUNTIME` to a folder path.

## Install

### As a plugin (recommended)

This takes two commands. Send them **one at a time**, as two separate
messages. If you paste both lines at once, only the first one runs: the
marketplace gets added but the plugin never installs.

First, in Claude Code, add the marketplace:

```
/plugin marketplace add bethhewitt/brand-design-kit
```

When that has finished, install the plugin:

```
/plugin install brand-design-kit@brand-design-kit
```

Then start a new Claude Code session. Skills from a newly installed plugin
don't appear in a session that was already open.

**From a terminal instead.** If `/plugin` isn't available where you use
Claude (some apps don't offer it), run the same two steps in a terminal
with the `claude` command line tool:

```bash
claude plugin marketplace add bethhewitt/brand-design-kit
```

```bash
claude plugin install brand-design-kit@brand-design-kit
```

**To check it worked**, run `claude plugin list` in a terminal and look for
`brand-design-kit` with status enabled.

**To update later**, run these in a terminal, one after the other, then
start a new session:

```bash
claude plugin marketplace update brand-design-kit
```

```bash
claude plugin update brand-design-kit@brand-design-kit
```

In plugin form the skills are named `brand-design-kit:brand-one-pager` and
so on, but you never need to type those names.

### As plain skills

Copy the six folders in `skills/` into `~/.claude/skills/` (for you, in every
project) or into a project's `.claude/skills/` (for everyone working on that
repo). Keep all six side by side: the asset skills find the core at
`../brand-design/`.

```bash
cp -R skills/brand-* ~/.claude/skills/
```

## First run in a repo

Open Claude Code in your project and ask for something, for example:

> Make a one-pager about our new service.

What happens:

1. **Brand discovery.** The kit lists brand-like files in the repo (docs,
   token files, stylesheets, logos, fonts, voice guides) and builds a brand
   block from them. Higher sources win when they conflict: written brand
   docs, then token files, then app styles. It shows you a short summary
   (colours, fonts, logo, anything it had to derive, any conflicts) and
   waits for your OK.
2. **Your choices.** It asks for the format and size every time (A4 or
   Letter, which platform sizes, PNG or PDF) and for any content it needs.
3. **Build, check, export.** It writes HTML, renders it, runs mechanical
   checks, looks at the rendered file and fixes problems before handing over.

After the first run the resolved brand is cached in `.brand-design/` at the
repo root. Commit it so your team shares one brand. The cache is rebuilt
automatically when its source files change.

### No brand files yet?

The kit says so and offers three routes:

1. **Extract from a website.** Give it your URL and it pulls colours, fonts
   and the logo from the live site.
2. **Create brand files.** It asks a few questions (name, colours, fonts,
   logo file, three tone words, any don'ts) and writes `DESIGN.md` and
   `tokens.css` at the repo root from its starter templates. You can also
   start those yourself: copy `skills/brand-design/assets/DESIGN.template.md`
   and `skills/brand-design/assets/tokens.template.css` into your repo and
   fill in the brackets.
3. **Go unbranded.** It uses a neutral palette and labels the output as
   unbranded.

You can also ask it to audit what you have: "audit our brand files" checks
your existing docs and tokens for gaps, conflicts and contrast failures and
proposes a tidy `DESIGN.md`.

## Where files go

Outputs are written to `brand-output/<task>/<date>-<slug>/`, unless your
repo's `CLAUDE.md` says drafts belong somewhere else, in which case the kit
follows that. Each folder holds the HTML source and the exported PNG or PDF.

## What it won't do

- **Invent facts.** No made-up statistics, quotes, customer names or
  results. Where it needs one it leaves a labelled gap such as
  `[STAT: needs source]` and lists every gap in its reply.
- **Invent a brand.** Every colour and font traces to a file in your repo, a
  URL you gave, or your own answer.
- **Fall back to stock AI looks.** Default indigo gradients, emoji icons,
  all-caps eyebrow labels and filler copy are flagged by the QA script.

## Making it yours

Everything is plain markdown, Python and a little JavaScript, so adapt it
freely.

- Change the questions and size menus in each asset skill's `SKILL.md`.
- Change the design rules in `skills/brand-design/references/craft/`.
- Change the mechanical checks in `skills/brand-design/scripts/check.py`.
- Add section layouts to `skills/brand-design/assets/layouts.md` (each must
  only use classes defined in `web-seed.html`).

## Useful commands

The skills run these for you, but they also work by hand. `<kit>` is
wherever `skills/brand-design` lives.

```bash
python3 <kit>/scripts/discover.py                  # list brand files in this repo
python3 <kit>/scripts/check.py --brand tokens.css  # contrast check on your tokens
python3 <kit>/scripts/check.py page.html           # QA an HTML output
bash <kit>/scripts/render.sh page.html page.pdf    # export to PDF
bash <kit>/scripts/render.sh post.html post.png --selector .frame --scale 1   # one PNG per frame
```

## Licence

MIT. See `LICENSE`. Some design rules and the web seed are adapted from
[OpenDesign](https://github.com/nexu-io/open-design) (Apache-2.0) and
[refero_skill](https://github.com/referodesign/refero_skill) (MIT); see
`THIRD_PARTY_NOTICES.md`.
