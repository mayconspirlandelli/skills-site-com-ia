---
name: gerar-design-system
description: Creates the site's design system in Markdown (design_system.md — palette, typography, spacing, grid, breakpoints, borders, shadows, components and rules) and in HTML (design_system.html, a visual version for review), plus tokens.css and Tailwind tokens, with WCAG contrast checks and user approval. Use in step 7 of the workflow, after the wireframes are approved, or whenever the user asks for a design system, style guide, palette, typography or tokens for a site.
---

# Design system (step 7)

`design_system.md` is the site's **single visual source of truth**. All step 8 code obeys it, and every style change starts in it. This step turns the approved visual direction (site image) and the values extracted from the references into a system of its own, consistent and verified — and the user approves it by looking at the HTML version.

## Inputs

- `etapas/00_briefing/briefing.md` — mandatory brand colors, tastes, tone.
- `etapas/02_previa/previa_site.md` — candidate palette and typography, with the source of each value.
- `etapas/03_mockup/` — the approved image: the visual direction the user chose.
- `etapas/01_extracao/codigo/*/resumo.md` and `etapas/01_extracao/prints/resumo.md` — measured and estimated values.
- `etapas/04_wireframes/especificacao_componentes.md` — typographic roles, spacing and components used.

## How to build it

Start from `assets/design_system_template.md` and fill it in **with decisions, not copies**. When sources disagree, follow the trust order: user decision > measured in code > estimated from screenshots > read from the approved image. The approved image rules the **direction** (mood, overall contrast, where the main color appears); exact values come from decisions and measurements.

1. **Colors.** Start with the mandatory brand colors. Define roles (primary, hover, secondary, text, secondary text, background, surface, border, error, success). Short palette: a few well-used colors look more professional. If the briefing asked for dark mode, define the light/dark pairs.
2. **Typography.** At most 2 families (headings and body), free (Google Fonts), always with a fallback. Paid font in a reference → a similar free alternative, and tell the user. Scale with H1, H2, H3, body and small; `clamp()` for large headings.
3. **Spacing.** 4px or 8px scale. Space between sections on desktop and mobile.
4. **Layout.** Maximum container width, side padding, grid and breakpoints (the ones measured in code, if any).
5. **Borders and shadows.** Few levels (2–3 radii, 2 shadows).
6. **Components.** Every one that appears in the approved wireframes — buttons (variants and states), cards, inputs, links, menu, and the site-specific ones.
7. **Rules.** Prohibitions and standards (nothing outside the tokens, focus always visible).

Record in "Principles" where each important decision came from — it helps the user review.

## Token format

Every token table has its **first column in the `` `--name` `` format** and the second with the value — that's how the scripts find the tokens. Recognized prefixes: `--color-`, `--space-`, `--radius-`, `--shadow-`, `--font-`, `--text-` (and `--container-`, `--bp-` for layout). In the `--text-*` table, keep the Weight and Line height columns: the HTML version uses both.

## Check contrast

For each text/background combination used:

```bash
python .claude/skills/gerar-design-system/scripts/contraste.py "#111827:#FFFFFF" "#FFFFFF:#1A56DB"
```

Paste the result into the contrast table. Normal text below 4.5:1 → adjust the color and explain the change to the user. Don't compute contrast "in your head".

## Generate the files

```bash
S=.claude/skills/gerar-design-system/scripts
D=etapas/05_design_system
python $S/gerar_tokens.py $D/design_system.md --saida $D/tokens.css --tailwind $D/tailwind.tokens.js   # --tailwind only if the stack uses Tailwind
python $S/gerar_html.py $D/design_system.md --saida $D/design_system.html
```

`design_system.html` is the visual version: color swatches with computed contrast, rendered type scale, spacing, radii, shadows, layout and sample components built only with the tokens. **Never edit the HTML or `tokens.css` by hand** — change the `.md` and generate again.

CSS variables don't work inside `@media`: the `--bp-*` tokens are documentation; in media queries, use the literal values.

## Approval

Open `design_system.html` in the browser and show it to the user, together with a summary (palette, fonts, scale). Adjust the `.md`, regenerate and show it again until they explicitly approve. Once approved, record it in `etapas/aprovacoes.md` (step 7, `05_design_system/`, `approved`, date).

After approval, any style adjustment — including during the build — is made in `design_system.md`, with tokens and HTML regenerated.

Next step: `construir-site` (step 8).
