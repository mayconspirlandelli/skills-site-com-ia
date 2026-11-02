---
name: gerar-mockup
description: Generates the site image from the preview — writes the prompt and draws a full-color SVG mockup — and iterates with the user until approval. Use in step 5 of the workflow, after the preview, or when the user asks for "the site image", "a mockup", "how the site will look" or a prompt to generate the site image.
---

# Site image (step 5)

Goal: see the site before building it. This is the workflow's **creative** step: the preview says what the site has; the image proposes how it looks. What comes out is an image **approved by the user**, which guides the wireframes (step 6) and the design system (step 7).

Input: `etapas/02_previa/previa_site.md` (and the briefing to cross-check).
Output: `etapas/03_mockup/` with `prompt_imagem.md` and the images.

## 1. Write the prompt

Generate `etapas/03_mockup/prompt_imagem.md` from `assets/prompt_imagem_template.md`:

- **Common base:** type of site, domain, audience, goal, mood, palette (hex), typography, shapes — all from the preview.
- **One prompt per screen:** Home desktop and Home mobile are the minimum. Other pages only if they are very different from the Home (e.g. a pricing page).
- **Sections in the preview's order**, each with the suggested organization and short real content (heading, button text).
- **Content images** (hero, illustrations, icons) in a separate table — they serve step 8.

Don't invent what the preview doesn't say. Never ask for real people that the site presents as real.

## 2. Draw the SVG mockup

Claude draws the mockup in SVG from the prompt — faithful to the preview and easy to adjust. Before drawing, load the `frontend-design` and `design-taste-frontend` skills to avoid a generic look.

- `mockup_home-desktop_v1.svg` with `viewBox="0 0 1440 <height>"`; `mockup_home-mobile_v1.svg` with width 390.
- **In color and with real typography** (it's not a wireframe): the preview's palette and fonts (`font-family` with fallback), headings and buttons with short real text, other text as lines or neutral sentences.
- Images as blocks with a soft gradient from the palette and a discreet label (`[PHOTO: team]`). Simple icons drawn in SVG.
- No external `<image>`, scripts or crops from references.

`prompt_imagem.md` can also be used by the user to generate the image in an AI image tool, if they want. If they bring an image generated elsewhere, save it in `etapas/03_mockup/` and treat it as another version for approval.

## 3. Approval

1. Show the images: open them in the app's browser when possible, or give the file paths.
2. Ask whether they approve or what they want to change. Record each request in the "Requested adjustments" table of `prompt_imagem.md` and generate a new version (`_v2`, `_v3`) — don't overwrite the previous ones.
3. When a request changes a preview decision (e.g. a different main color), also update `previa_site.md`.
4. Approved: copy the chosen version to `mockup_home-desktop.png|svg` (and `-mobile`) and record it in `etapas/aprovacoes.md` (step 5, files, `approved`, date, chosen version).

The approved image is **visual direction**, not specification: in the trust order, measured values and user decisions are worth more than colors and measurements "read" from the image. The official structure is born in the wireframes.

Next step: `gerar-wireframes` (step 6).
