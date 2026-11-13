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

## What you need

- **A Claude subscription that includes Claude Code.** Use it in the Claude
  desktop app (the Code tab), in a terminal, or in your code editor.
  Nothing else is needed to install the kit.
- **Node.js, for PNG and PDF export.** It's free. If you don't have it,
  Claude tells you when you first export and explains how to get it: go to
  [nodejs.org](https://nodejs.org), download the version marked LTS, and run
  the installer. Until then you still get the HTML file, which you can open
  in a browser and print to PDF.
- **On a Mac,** the first run may show a pop-up asking to install "command
  line developer tools". Click Install. It's an Apple download and takes a
  few minutes.

The first PNG or PDF export downloads a rendering engine (a few hundred MB,
one time only), so it takes a couple of minutes. Later exports are quick.

## Install

### Ask Claude to install it (works everywhere)

1. Open Claude Code: in the Claude desktop app, go to the Code tab and start
   a new session in any folder.
2. Copy this message, paste it in, and send it:

   ```
   Please install the brand design kit for me. Download https://github.com/bethhewitt/brand-design-kit/archive/refs/heads/main.zip, unzip it into a temporary folder, and copy the six folders inside its skills folder into my personal Claude skills folder (~/.claude/skills on Mac and Linux, or .claude\skills in my user folder on Windows). Create that folder if it doesn't exist, and replace any older copies of those six folders. Then delete the download and tell me when it's done.
   ```

3. Claude may ask permission to run a few commands. Allow them.
4. When it says it's done, **start a new session**. A session that was
   already open won't see the new skills.
5. To check, ask the new session: "Which brand design skills do you have?"
   It should list six, starting with `brand-design`.

**To update** later, send the same message again, then start a new session.

**To remove** the kit, ask Claude: "Delete the six brand- folders from my
personal Claude skills folder."

### As a plugin (if you use Claude Code in a terminal)

If you run Claude Code in a terminal, you can install it as a plugin instead,
which makes updates easier. Send these as two separate messages, waiting for
the first to finish. Pasting both at once only runs the first.

```
/plugin marketplace add bethhewitt/brand-design-kit
```

```
/plugin install brand-design-kit@brand-design-kit
```

Then start a new session. Use one install route or the other, not both, or
you'll have every skill twice.

## First run

Start a Claude Code session in your project folder (any folder works, even
an empty one) and ask for something, for example:

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

After the first run the brand is saved in a `.brand-design/` folder inside
your project. If you use git, commit it so your team shares one brand. The cache is rebuilt
automatically when its source files change.

### No brand files yet?

The kit says so and offers three routes:

1. **Extract from a website.** Give it your URL and it pulls colours, fonts
   and the logo from the live site.
2. **Create brand files.** It asks a few questions (name, colours, fonts,
   logo file, three tone words, any don'ts) and writes `DESIGN.md` and
   `tokens.css` in your project folder from its starter templates. You can also
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
