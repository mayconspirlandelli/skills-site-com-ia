---
name: gerar-wireframes
description: Generates SVG wireframes (grayscale, annotated sections) of every page and subpage of the site, desktop and mobile, from the approved site image and the preview, with a review page for the user's approval; then details the component specification. Use in step 6 of the workflow, after the site image is approved, or when the user asks for a wireframe, page skeleton, layout structure, page map or component specification.
---

# Wireframes of every page (step 6)

Goal: pin down the **structure** of each page of the site in an SVG wireframe approved by the user. The site image (step 5) showed how the site could look; the wireframe says exactly which sections exist, in what order, with what layout and how many elements — and what changes on mobile. During the build (step 8), the approved wireframe is the official structure reference.

The wireframes are grayscale on purpose: separating structure from style avoids discussing color when the subject is layout. Style is decided in step 7.

## Inputs

- `etapas/02_previa/previa_site.md` — **all** pages and sections, in order. It's the list of what to draw.
- `etapas/03_mockup/` — the approved image (`mockup_home-desktop`, `-mobile`): proportions, section organization, rhythm.
- `etapas/00_briefing/briefing.md` — to cross-check features and content.

## Part 1 — SVG wireframes

Draw **one page at a time**, top to bottom, section by section, copying `assets/wireframe_template.svg` and following its conventions.

### Which pages
- Every page in the preview (Home and subpages: About, Services, Contact, detail pages...).
- Pages without an approved image follow the Home's language: the same header and footer, the same grid and spacing logic. Repeated components (header, footer, card, CTA) have the same structure on every page.
- Landing page: a single page, but with all its sections.

### Files
- `etapas/04_wireframes/wireframe_<page>-desktop.svg` — required, width 1440 (`viewBox="0 0 1440 <height>"`).
- `etapas/04_wireframes/wireframe_<page>-mobile.svg` — required for the Home; recommended for the others. Without a mobile image, infer from desktop and mark assumptions with `(uncertain)`.
- `<page>` in lowercase, without accents: `home`, `about`, `services`, `contact`.

### SVG conventions
- Root `<svg>` with `viewBox`, `data-pagina` and `data-viewport` (`desktop` | `mobile`), followed by `<title>` and `<desc>`.
- **Each section is a `<g class="secao">`** positioned with `transform="translate(0,y)"`, with:
  - `id` in lowercase (`header`, `hero`, `services`...);
  - `data-nome` — section name in uppercase (HEADER, HERO, SERVICES, TESTIMONIALS, CTA, FOOTER...);
  - `data-layout` — `1 column`, `2 columns 60/40`, `3-column grid`...;
  - `data-largura` (`container` | `full-width`), `data-altura` (`auto`, `~100vh`...);
  - `data-elementos` — list with quantities (`H1, paragraph, 2 buttons, image`);
  - `data-mobile` — what changes on mobile (required in the desktop file);
  - optional: `data-alinhamento`, `data-comportamento` (e.g. `sticky at the top`).
- Section label in `<text class="rotulo-sec">`.
- Elements use the classes from the template's `<style>`: `texto` (bars instead of text, one per line), `bloco` (logo, cards), `botao-prim` / `botao`, `imagem` + two `imagem-x` lines.
- Each element has a `<text class="rotulo">` with the content's **function** (`H1 (value proposition, ~8 words, 2 lines)`).
- Repeated groups carry `data-elemento` and `data-quantidade` (`<g data-elemento="card" data-quantidade="3">`).
- Proportions and positions as in the approved image, inside the 1200px container (120px margins on desktop).
- When in doubt, `(uncertain)` in a `<text class="nota">` — don't invent.

### Forbidden in the SVG
`<image>`, `<script>`, `<foreignObject>`, external links, base64 images, colors, fonts, logos or text copied from the references.

### Validate and build the review
```bash
S=.claude/skills/gerar-wireframes/scripts
python $S/validar_wireframe.py etapas/04_wireframes/*.svg
python $S/gerar_indice.py etapas/04_wireframes
```
Fix everything the validator flags with ✗. `gerar_indice.py` creates `etapas/04_wireframes/index.html` with every page side by side (desktop and mobile) and the list of sections of each.

### Approval
Open `index.html` in the browser and ask the user to review **every** page. Adjust until they explicitly approve; regenerate the index each round. Once approved, record it in `etapas/aprovacoes.md` (step 6, approved pages, `approved`, date). Changing structure after the build is expensive — the pause is worth it.

## Part 2 — Component specification

With the wireframes approved, detail each component in `etapas/04_wireframes/especificacao_componentes.md` (template in `assets/especificacao_template.md`):

- **Typography:** role (H1, H2, body...), weight, alignment.
- **Position and alignment** within the section.
- **Spacing** inside and between elements, by role (`space-lg`).
- **Responsiveness:** what changes on tablet and mobile.
- **States:** hover, focus, active, disabled.

The design system doesn't exist yet at this point: reference values by role and record the candidate values in a table at the end, with their source, in the project's trust order — user decision > measured in code (step 2) > estimated from screenshots (step 3) > read from the approved image (step 5). Step 7 turns these roles into tokens.

Next step: `gerar-design-system` (step 7).
