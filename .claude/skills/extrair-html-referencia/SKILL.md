---
name: extrair-html-referencia
description: Extracts the design system of the reference sites straight from the code — HTML, CSS and the result of JavaScript (computed styles in the browser via playwright-cli) — producing a resumo.md per site with palette, typography, size scale, spacing, radii, shadows, containers and breakpoints. Use in step 2 of the workflow, when the approved briefing has reference URLs, or whenever the user asks to "grab the code", "analyze the CSS" or "extract the style/design system" of a site.
---

# Design extracted from the references' code (step 2)

Goal: turn each reference site in the briefing into a `resumo.md` with **measured values** — colors, fonts, sizes, spacing, radii, shadows, breakpoints — instead of visual impressions. In the project's trust order, these values only lose to user decisions.

Inputs: the URLs in section **H. References** of `etapas/00_briefing/briefing.md` (approved), with what to take and what to avoid from each one. Without URLs, record step 2 as `not applicable` in `etapas/aprovacoes.md` and move on to step 3.

Output: one folder per site in `etapas/01_extracao/codigo/<site-name>/`.

## Why two captures

- **Static code** (`extrair_referencia.py`): clean HTML, concatenated CSS, variables, `@font-face`, breakpoints. Fast, but React/Vue/Next sites arrive almost empty.
- **Rendered page** (`playwright-cli` + `estilos_computados.js`): the browser opens the site, JavaScript runs, and we measure what was **actually applied** — color of each text, background per area, font by amount of text, style of h1/button/input. Works for any site and is the most faithful measurement.

Do both whenever `playwright-cli` is available. Without it, use only the static one and tell the user about the limitation.

## 1. Capture the rendered page

For each URL (replace `<site-name>` with a short name, e.g. `ref1-acme`):

```bash
D=etapas/01_extracao/codigo/<site-name>; mkdir -p $D
JS=.claude/skills/extrair-html-referencia/scripts/estilos_computados.js
playwright-cli open <url>
playwright-cli resize 1440 900
playwright-cli --raw eval "document.documentElement.outerHTML" > $D/renderizado.html
playwright-cli --raw eval "$(cat $JS)" > $D/computados-desktop.json
playwright-cli resize 390 844
playwright-cli --raw eval "$(cat $JS)" > $D/computados-mobile.json
playwright-cli close
```

If a cookie banner covers the page, decline the non-essential ones (the most restrictive option) before measuring. Don't log in or fill in forms.

`estilos_computados.js` only reads the page: it changes nothing and sends no data.

## 2. Run the scripts

```bash
pip install beautifulsoup4   # if needed
S=.claude/skills/extrair-html-referencia/scripts
python $S/extrair_referencia.py --html $D/renderizado.html --base-url <url> --saida $D
python $S/resumir_computados.py --entrada $D/computados-desktop.json $D/computados-mobile.json --saida $D
```

Without `playwright-cli`: `python $S/extrair_referencia.py --url <url> --saida $D` (or `--html` with the page saved by the user: `Ctrl+S` → "Web Page, Complete").

Outputs in the site folder: `limpo.html`, `estilos.css`, `resumo.md`, `dados.json` (static) and `computados.md` (measured).

**Read the warnings.** If the page looks empty, there's no CSS, or `computados.md` analyzed few elements (e.g. block page, captcha, "access denied"), don't continue with bad data: tell the user and ask for the saved page or another URL.

## 3. Consolidate the site's design system

Append to the end of `resumo.md` the **"Extracted design system"** section, cross-checking `resumo.md` (static) and `computados.md` (measured). When they disagree, the measured value wins.

| Item | How to get there |
|------|------------------|
| **Palette with roles** | background (largest area), text (most characters), primary (button background/links), secondary, borders, states. Discard colors from third-party widgets (chat, cookies, maps). |
| **Typography** | heading and body fonts (separate icon fonts and fallbacks), weights used. |
| **Size scale** | h1 → h4, body, small text — on desktop and mobile ("Typography by viewport" table). |
| **Spacing** | recurring gaps and paddings; try to recognize the scale (multiples of 4 or 8). |
| **Radii and shadows** | the 2–3 most used values and where they appear (buttons, cards, inputs). |
| **Container and breakpoints** | maximum content width and main media queries. |
| **Relation to the briefing** | highlight the values tied to what the user wants to **take** and flag the ones they want to **avoid**. |

Mark as "(likely)" whatever was inferred instead of measured.

## 4. Repeat per reference and wrap up

One folder per site. At the end, show the user a short table with each reference's palette and fonts and move on to step 3 (`extrair-design-prints`). This step doesn't require approval; record `done` in `etapas/aprovacoes.md`.

## Usage limits

The extracted code is a reference for style values and structure. Don't copy text, images, logos, icons or code blocks from the sites into the final site. Paid fonts that show up in the extraction can't be used without a license — flag them in the summary and suggest free alternatives.
