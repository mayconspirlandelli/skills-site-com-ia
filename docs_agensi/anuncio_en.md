# Agensi.io listing

Copy-paste texts in the order of the "New skill" form.

---

## Step 1 — ZIP upload

File: `docs_agensi/dist/site-com-referencias.zip` (built by `python docs_agensi/montar_zip.py`).
The `SKILL.md` at the ZIP root is the `site-com-referencias` orchestrator; the site fills name and description from its header.

---

## Step 2 — Skill details

### Logo
`docs_agensi/logo.svg` → export to a 512×512 PNG (see README).

### Skill name (max 60)
```
Site from References: Brief to Website in 8 Steps
```
(49 characters)

### Summary (max 300)
```
Build websites and landing pages with AI in 8 approved steps: interview and brief, design measured from your references' code and screenshots, mockup, SVG wireframes, token-based design system, and a built, validated site. No more generic AI sites: structured text instead of improvisation.
```

### Full description
```markdown
## Stop getting generic websites from AI

Ask an AI agent to "make a site like this one" and you usually get the same thing: a template-looking layout, guessed colors, random typography, and hours of rework. The reason is simple — the AI improvises from images and a vague request.

**Site from References** replaces improvisation with a process. It is a bundle of 10 skills that walks your agent through **8 steps**, from understanding the business to a validated, deploy-ready site. Each step writes a structured text file that the next one reads, and the steps that shape the result only move forward with your approval.

## The 8 steps

| # | Step | What you get | Approval |
|---|------|--------------|----------|
| 1 | Interview & brief | Questions in rounds, each with a recommended answer → `briefing.md` | ✅ |
| 2 | Design from code | Colors, fonts, spacing, radii, shadows and breakpoints **measured** in a real browser (computed styles) | |
| 3 | Design from screenshots | Palette with area and contrast (script) + typography and shape analysis, marked as estimated | |
| 4 | Site preview | Pages, sections, content and visual direction in Markdown | |
| 5 | Site image | Prompt + full-color SVG mockup | ✅ |
| 6 | Wireframes | SVG for **every** page, desktop and mobile, with a review page | ✅ |
| 7 | Design system | `design_system.md` + visual HTML version + `tokens.css` + Tailwind tokens, with WCAG contrast checks | ✅ |
| 8 | Build & validate | Build plan, section-by-section code (tokens only), Docker/deploy and a validation report | |

## Why it works

- **Measured, not guessed.** Step 2 opens your references in a real browser and reads computed styles — including what JavaScript renders.
- **Explicit trust order.** Your decision > value measured in code > value estimated from a screenshot > mockup proposal. No silent conflicts.
- **One visual source of truth.** `design_system.md` rules; code uses tokens only. Changing a color? Change it in the design system and regenerate tokens with a script.
- **Approvals at the right moments.** Fixing a brief takes minutes; fixing a finished site takes hours.
- **Resumable.** Progress lives in `etapas/aprovacoes.md`. Stop today, continue tomorrow — the orchestrator figures out which step you're on.
- **Ethical by default.** References inform structure and style only. Their text, images, logos and code never reach your site — your brief's content or clearly marked placeholders do.
- **Secure.** Ships with `auditar-skill`, which scans any third-party skill for prompt injection, data exfiltration, credential access, obfuscated code and destructive commands **before** installing it.

## What's included

- 10 skills: orchestrator + one skill per step + security audit
- 9 Python/JS scripts (computed-style extraction, screenshot palette, WCAG contrast, CSS/Tailwind tokens, HTML design system, wireframe validation)
- Templates for brief, preview, image prompt, wireframe, design system, build plan and validation report
- Ready project structure (`etapas/`, `site/`, `CLAUDE.md`) and setup scripts that audit and install the companion skills
- Stack chosen in the interview (HTML/CSS, Tailwind, Vite or frameworks); default HTML + Tailwind, mobile-first

## Who it's for

Freelancers and agencies shipping landing pages, developers tired of "looks like a template", and founders who know what they want but can't translate it into design.
```

---

## Step 3 — See it in action

> ⚠️ Representative example. Ideally replace it with output from a real session before publishing
> (the site asks for the full result, never a truncated excerpt).

### The request
```markdown
I want a landing page for my pilates studio in Austin, **Balance Studio**. The goal is booking a free trial class through WhatsApp. I like the look of https://reference-one.example and https://reference-two.example, and I saved 2 screenshots in `etapas/00_briefing/prints/`.
```

### The result
```markdown
## Summary
All 8 steps are done for **Balance Studio**. Steps 1, 5, 6 and 7 were approved by you and logged in `etapas/aprovacoes.md`. The site lives in `site/`, validated against the build plan, with a Dockerfile ready.

## Progress

| # | Step | File | Status |
|---|------|------|--------|
| 1 | Brief | `etapas/00_briefing/briefing.md` | ✅ approved |
| 2 | Code extraction (2 sites) | `etapas/01_extracao/codigo/*/resumo.md` | done |
| 3 | Screenshot extraction (2) | `etapas/01_extracao/prints/resumo.md` | done |
| 4 | Preview | `etapas/02_previa/previa_site.md` | done |
| 5 | Site image | `etapas/03_mockup/mockup_home-desktop.svg` | ✅ approved (v2) |
| 6 | Wireframes (1 page × desktop/mobile) | `etapas/04_wireframes/` | ✅ approved |
| 7 | Design system | `etapas/05_design_system/` | ✅ approved |
| 8 | Build & validation | `site/`, `etapas/06_construcao/` | done |

## Design system (excerpt of generated tokens)

| Token | Value | Source |
|-------|-------|--------|
| `--color-primary` | `#2F5D50` | your decision in the brief |
| `--color-bg` | `#FAF7F2` | measured on reference 1 |
| `--color-secondary` | `#D98E5F` | estimated from screenshot 2 |
| `--font-heading` | Fraunces 600 | measured on reference 2 |
| `--font-body` | Inter 400 | measured on reference 1 |
| `--space-24` | `96px` between sections (`--space-16` on mobile) | measured on reference 1 |

WCAG contrast: body text on background **9.8:1 (AAA)**; primary button **5.1:1 (AA)**.

```css
:root {
  --color-primary: #2F5D50;
  --color-bg: #FAF7F2;
  --color-secondary: #D98E5F;
  --font-heading: "Fraunces", serif;
  --font-body: "Inter", sans-serif;
  --radius-full: 999px;
  --space-24: 96px;
}
```

## Sections built (checked against the wireframe)
Sticky header · Hero with "Book a free trial" CTA (WhatsApp) · Benefits (3 cards) · Classes · Instructors `[PHOTO: real team]` · Testimonials `[TEXT: real testimonials]` · Pricing · FAQ · Map & contact · Footer.

## Validation (`relatorio_validacao.md`)
- ✅ 0 hard-coded colors/sizes — everything through tokens
- ✅ Responsive at 375, 768 and 1280 px (screenshots in the report)
- ✅ No text, image or logo copied from the references
- ⚠️ 2 placeholders waiting for real content (team photos, testimonials)

**Next steps**
1. Replace the `[PHOTO: ...]` and `[TEXT: ...]` placeholders with real content.
2. Run `docker build -t balance-studio site/` and deploy to the host chosen in the brief.
3. Want a different color? Edit `design_system.md` and ask to regenerate the tokens.
```

---

## Step 4 — Compatibility note
```
Built for Claude Code (uses CLAUDE.md and .claude/skills). Requires Python 3.9+ (beautifulsoup4, pillow), Node.js 18+, Git and Bash (Git Bash on Windows). Third-party companion skills (e.g. playwright-cli, frontend-design) are installed by the included setup script, after a security audit.
```

---

## Step 5 — Pricing
Suggested: **One-time purchase**. See the pricing/license note in this folder's `README.md`.

---

## Tags, categories, use cases

- **Tags:** landing page, website, web design, design system, wireframes, mockup, frontend, tailwind, design tokens, claude code
- **Category:** Design / Frontend / Web development
- **Use cases:**
  - Build a landing page from reference websites
  - Extract a design system and tokens from existing sites
  - Wireframe every page before writing code
  - Redesign a business website with a process and approvals

---

## Permissions

### Required tools & software (one per line)
```
Claude Code
Python 3.9+ (beautifulsoup4, pillow)
Node.js 18+
Git
Bash (Git Bash on Windows)
playwright-cli (installed by the setup script)
```

### Tools used
- [x] Terminal / Shell — runs the Python/JS scripts and playwright-cli
- [x] Read files
- [x] Write files
- [x] Browser — playwright-cli measures the references' styles and validates the site
- [x] Network access — fetches the reference URLs' HTML/CSS and installs companion skills
- [ ] Environment variables — not used

### Needs access to
No account required. Optional: `github.com` (companion skills downloaded by the setup script).

### File scopes
```
etapas/**
site/**
.claude/skills/**
docs/**
CLAUDE.md
```

### Notes
```
Reads and writes stay inside the project: etapas/ holds the brief, extractions, wireframes and design system; site/ holds the generated code. Network is used only to fetch the HTML/CSS of the reference URLs you provide and, during setup, to download companion skills from GitHub — each audited before install. No data is sent to external servers and no API key is needed.
```

---

## FAQ

**Do I need to know how to code?**
Not to run the flow: you answer the interview and approve the steps. Publishing the site is easier with basic Git and hosting knowledge — step 8 already prepares Docker and deployment for the host you picked.

**Does it work without reference sites?**
Yes. Without URLs step 2 is skipped; without screenshots, step 3. The design comes from the brief and the mockup.

**Does it copy the reference site?**
No. References inform structure and style only. Their text, images, logos and code never reach your site.

**Which stack does the site use?**
The one you pick in the interview (HTML/CSS, Tailwind, Vite, frameworks). Default: HTML + Tailwind, mobile-first.

**Can I stop halfway?**
Yes. Progress is stored in `etapas/aprovacoes.md` and the orchestrator resumes from the right step in a new session.

**Does it work with agents other than Claude Code?**
It was built and tested on Claude Code. The `SKILL.md` files follow the open standard, but the flow relies on `CLAUDE.md` and several skills loaded together — other agents may need adjustments.

**Why do I need third-party skills?**
They belong to other authors and have their own licenses, so they are not bundled. The included script downloads each one, audits it and installs only the audited commit.

**Why are some folder and skill names in Portuguese?**
The project started in Brazil. All instructions, templates and messages are in English; only identifiers such as `etapas/` (steps) or `entrevista-site` (site interview) keep their original names so paths stay stable.

---

## Showcase

### Screenshots (up to 6)
1. `docs/diagrama-processo.png` — 8-step diagram (already exists)
2. Interview in progress (question with recommended answer)
3. Wireframe review page (`etapas/04_wireframes/index.html`)
4. `design_system.html` in the browser
5. Approved SVG mockup
6. Final site, desktop and mobile side by side

### 30-second demo video — script
1. (0–5 s) Request: "I want a landing page for my studio…"
2. (5–12 s) Interview with recommended answers
3. (12–18 s) Mockup and wireframes appearing
4. (18–24 s) Design system in HTML
5. (24–30 s) Final site in the browser, desktop and mobile

### Documentation link
```
https://github.com/mayconspirlandelli/skills-site-com-ia
```
(only if the repository stays public — see this folder's README)
