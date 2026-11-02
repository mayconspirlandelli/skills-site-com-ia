---
name: construir-site
description: Plans, builds and validates the site — writes the build plan from the approved briefing, wireframes and design system, generates the code in site/ section by section (tokens only), prepares Docker and deployment according to the briefing's hosting and, at the end, validates everything against the plan in a report. Use in step 8 of the workflow, after the design system is approved, or when the user asks to "now build the site", "put the page together", "create the hero/header/footer", deploy, Dockerfile, or to review/validate the generated site.
---

# Plan, build and validation (step 8)

Goal: turn what was approved (briefing, wireframes, design system) into a working site in `site/`, ready for the chosen hosting — and prove, in a report, that it meets the plan.

## Before you start

Confirm in `etapas/aprovacoes.md` that steps 1, 6 and 7 are approved. If the design system isn't, stop and say so: without it the site comes out generic and inconsistent. Read, in this order:

1. `etapas/05_design_system/design_system.md` and `tokens.css`
2. `etapas/04_wireframes/wireframe_<page>-desktop.svg` and `-mobile.svg` (the `data-*` attributes of each `<g class="secao">`) and `especificacao_componentes.md`
3. `etapas/00_briefing/briefing.md` — stack, hosting, Docker, content, features
4. `etapas/02_previa/previa_site.md` and `etapas/03_mockup/prompt_imagem.md` (content images)

## Phase 1 — Build plan

Write `etapas/06_construcao/plano_construcao.md` from `assets/plano_construcao_template.md`:

- **Stack and folder structure** of `site/` (see `references/stacks.md`).
- **Pages and sections**: one line per section of each approved wireframe, with the components it uses. This list becomes the validation checklist.
- **Reusable components** (header, footer, button, card...) and where they appear.
- **Tokens**: how the design system enters the code (`tokens.css` imported; Tailwind extended with `tailwind.tokens.js`).
- **Content**: briefing text per section and the list of `[TEXT: ...]` / `[PHOTO: ...]` placeholders the user will fill in.
- **Features**: form, WhatsApp, analytics, PWA... and how each will be done.
- **Delivery**: hosting, Docker (yes/no), automatic deploy — the files that will be created (see `references/deploy.md`).
- **Acceptance criteria**: what validation will check (sections, responsiveness, accessibility, Lighthouse, build/Docker).
- **Assumptions** made for lack of information.

Show the plan to the user and confirm before writing code. Scope changes after that go into the plan first.

## Phase 2 — Build in `site/`

### Code rules
- **Tokens only.** Colors, fonts, sizes, spacing, radii and shadows come from `tokens.css` (or the Tailwind classes generated from it). No loose hex or px. New value → propose adding it to the design system first.
- **The site's tokens are generated, not copied by hand:** generate `tokens.css` (and `tailwind.tokens.js`) straight into the site path with `gerar_tokens.py --saida site/<path>/tokens.css`, and regenerate whenever the design system changes.
- **Semantic HTML:** `header`, `nav`, `main`, `section` with `aria-labelledby`, `footer`; a single `h1` per page; headings without skipping levels.
- **Mobile-first**, following the wireframes' `data-mobile` and the specification.
- **Accessibility:** visible focus, `alt` on images, labels on inputs, touch target ≥ 44px, `prefers-reduced-motion`.
- **Content:** briefing text; where it's missing, a marked placeholder. Never text, images or logos from the references.
- `site/` contains only what goes to production: no step files inside it.

### Order
Generating everything at once produces a generic result. Build in parts, checking each one:

1. **Base:** folder structure, tokens, global styles (reset, base typography, container).
2. **Header and footer.**
3. **One section at a time**, in wireframe order. When each section is done: check it against the wireframe (elements, quantities, alignment) and the specification (typography, spacing, states, mobile); tick it in the plan; show the user. If they prefer speed, group 2–3 sections per round, keeping the check.
4. **Other pages**, reusing the components.
5. **Features** (form, integrations, PWA).

A style adjustment requested by the user (color, font, spacing) changes `design_system.md` and the tokens are regenerated — not just the CSS.

## Phase 3 — Delivery

According to the briefing, create the delivery files described in `references/deploy.md`: `Dockerfile` + `nginx.conf` (if Docker), GitHub Pages workflow, `netlify.toml`, `vercel.json`, `.dockerignore`. Test what can be tested locally (`npm run build`; `docker build` if Docker is installed). Never deploy, push or publish without the user asking.

## Phase 4 — Validation against the plan

Validate and write `etapas/06_construcao/relatorio_validacao.md` from `assets/relatorio_validacao_template.md`:

1. **Plan item by item:** each section of each page — does it exist, in order, with the wireframe's quantities? Was each feature and delivery file in the plan done?
2. **Checklist** from `references/checklist_validacao.md` (design system, responsiveness, accessibility, performance/SEO, content and rights).
3. **In the browser** (with `playwright-cli`): open each page at 375, 768 and 1280px, take screenshots into `etapas/06_construcao/screenshots/`, check horizontal scrolling, mobile menu, keyboard focus and console errors.
4. **Build and Docker:** does the build pass? Does the Docker image start and serve the site?
5. **Lighthouse:** run it if a tool is available; otherwise explain to the user how to run it (DevTools → Lighthouse → Analyze).

For each item the report says: ✅ passed, ❌ failed (and what was fixed or what's missing) or ⚠️ not verified (and why). Be honest: an untested item is not an approved item. Fix the failures you can, revalidate, and give the user the summary and the list of open items (placeholders to fill, unverified items). Record `done` in `etapas/aprovacoes.md`.
