# Plan: building websites and landing pages with generative AI and skills

## Overview

The template organizes building a site into **8 steps**, from understanding the business to a validated site. The core idea: AI works better with **structured text** (briefing, extracted design, wireframes, tokens) than when improvising from images — so each step produces a file the next one reads. Four steps only move on with the **user's approval**, because decisions made early contaminate everything else.

![Diagram of the 8 steps](diagrama-processo.png)

Interactive version: [`diagrama-processo.html`](diagrama-processo.html) (open in the browser).

| # | Step | Skill | Output | Approval |
|---|------|-------|--------|----------|
| 1 | Interview and briefing | `entrevista-site` | `etapas/00_briefing/briefing.md` | ✅ |
| 2 | Design extracted from the references' code | `extrair-html-referencia` | `etapas/01_extracao/codigo/<site>/resumo.md` | |
| 3 | Design extracted from screenshots | `extrair-design-prints` | `etapas/01_extracao/prints/resumo.md` | |
| 4 | Site preview | `gerar-previa` | `etapas/02_previa/previa_site.md` | |
| 5 | Site image | `gerar-mockup` | `etapas/03_mockup/` (prompt + SVG mockup) | ✅ |
| 6 | Wireframes of every page | `gerar-wireframes` | `etapas/04_wireframes/*.svg` | ✅ |
| 7 | Design system | `gerar-design-system` | `etapas/05_design_system/` (.md + .html + tokens) | ✅ |
| 8 | Plan, build and validation | `construir-site` | `site/` + `etapas/06_construcao/` | |

The `site-com-referencias` skill drives everything: it finds out which step the project is on (from the folders and `etapas/aprovacoes.md`) and calls the right skill.

### Folder structure

```
site-project/
├── etapas/                    site construction, in workflow order
│   ├── aprovacoes.md          log of the user's approvals
│   ├── auditorias/            skill audit reports + reviewed exceptions
│   ├── 00_briefing/           briefing.md (approved) + prints/ (screenshots) sent by the user
│   ├── 01_extracao/
│   │   ├── codigo/<site>/     design extracted from the references' HTML/CSS/JS
│   │   └── prints/            design extracted from screenshots
│   ├── 02_previa/             previa_site.md
│   ├── 03_mockup/             image prompt + approved site image
│   ├── 04_wireframes/         SVG wireframes of every page (approved)
│   ├── 05_design_system/      design_system.md + design_system.html + tokens.css
│   └── 06_construcao/         plano_construcao.md + relatorio_validacao.md
└── site/                      site code only (ready for Docker and deploy)
```

---

## Before you start — third-party skills

```bash
./scripts/setup-skills.sh obrigatorias
```

The script audits each skill before installing it (see [`skills-obrigatorias.md`](skills-obrigatorias.md)). Restart Claude Code afterwards.

---

## Step 1 — Interview and briefing ✅

Claude interviews the user in **short rounds of questions, each with a recommended answer** — a "yes" is enough to accept. The script covers:

- **Business:** domain, what it offers, type of site (landing page, company site, portfolio...).
- **Goal** and **audience** (profile, mobile or desktop, language, accessibility).
- **Pages, content and features** (form, WhatsApp, animations...).
- **Architecture:** HTML + CSS, Tailwind, Vite, Astro, Next.js...
- **Hosting and Docker:** GitHub Pages, Netlify, Vercel, VPS; container or not; domain.
- **Design:** colors they like and avoid, brand colors, typography, tone, dark mode, responsive or PWA.
- **References:** 3 to 5 URLs with what to take and what to avoid from each, and **screenshots** (saved in `etapas/00_briefing/prints/`).

**Output:** `briefing.md`, approved by the user. Animations or videos in the briefing → `./scripts/setup-skills.sh animacao`.

## Step 2 — Design extracted from the references' code

For each URL, the browser (`playwright-cli`) opens the site, JavaScript runs, and we measure what was **actually applied**: text and background colors, fonts, size scale (desktop and mobile), radii, shadows, containers, breakpoints and CSS variables. The rendered HTML is also cleaned and summarized.

**Output:** one `resumo.md` per site, with the "Extracted design system" section. Without URLs, the step does not apply.

## Step 3 — Design extracted from screenshots

A script pulls the palette from each screenshot (with each color's area, probable accent and contrast); Claude analyzes typography, spacing, shapes and components. Everything is marked as **estimated** — an image does not keep exact values.

**Output:** `etapas/01_extracao/prints/resumo.md`. Without screenshots, the step does not apply.

## Step 4 — Site preview

Combines briefing and extractions in one document: pages and sections in order, content of each, visual direction (candidate palette and typography, with the source of each value), what comes from each reference, conflicts to decide and technical decisions.

**Output:** `previa_site.md`.

## Step 5 — Site image ✅

The creative step: Claude writes a **prompt** from the preview and **draws the mockup in SVG** (in color, with real typography) — Home on desktop and mobile, at least. The prompt can also be used to generate the image in any AI image tool. Each adjustment creates a new version.

**Output:** `prompt_imagem.md` + mockup approved by the user.

## Step 6 — Wireframes of every page ✅

The structure of **every page and subpage** in gray SVG, desktop and mobile: sections, layout, quantities and what changes on mobile, annotated in attributes the AI reads during the build. An `index.html` page shows them all side by side for review. Once approved, they become the component specification.

**Output:** `wireframe_<page>-desktop.svg` / `-mobile.svg`, `index.html`, `especificacao_componentes.md`.

## Step 7 — Design system ✅

The **single visual source of truth**: palette with roles, typography, spacing, layout, borders, shadows, components and rules — its own decisions, consistent with the approved image, with WCAG contrast checked by script. Generates `tokens.css` (and Tailwind tokens) and `design_system.html`, the visual version for the user to approve.

Trust order when sources disagree: **user decision > measured in code > estimated from screenshots > read from the image**.

**Output:** `design_system.md`, `design_system.html`, `tokens.css`.

## Step 8 — Plan, build and validation

1. **Build plan:** stack, folders, pages and sections (which become a checklist), components, content and placeholders, features, delivery and acceptance criteria. The user confirms before any code.
2. **Build** in `site/`, section by section, tokens only, checking each section against the wireframe.
3. **Delivery:** `Dockerfile` + `nginx.conf` if Docker is used; hosting files (GitHub Pages, Netlify, Vercel...).
4. **Validation against the plan:** every section, feature and delivery file; responsiveness at 375/768/1280px; accessibility; build and Docker; Lighthouse.

**Output:** `site/`, `plano_construcao.md` and `relatorio_validacao.md` (✅ passed · ❌ failed · ⚠️ not verified).

---

## Rules for every step

- The approved `design_system.md` is the single visual source of truth: style changes start there, and tokens are regenerated.
- In code, tokens only — no loose colors, sizes or spacing.
- Never copy text, images, logos or code from the references: briefing content or `[TEXT: ...]` placeholders.
- Never use AI to generate images of real people that the site presents as real.
- Third-party skills or MCP servers only after an audit (`auditar-skill`).
