---
name: extrair-design-prints
description: Extracts the design system from screenshots of reference sites — color palette with area and contrast (script), typography, size scale, spacing, radii, shadows and component style (visual analysis) — producing a resumo.md with every value marked as estimated. Use in step 3 of the workflow, when the approved briefing has screenshots in etapas/00_briefing/prints/, or whenever the user sends screenshots and asks for their colors, fonts or "style".
---

# Design extracted from screenshots (step 3)

Goal: pull from the screenshots sent during the interview the **style** the user liked — colors, typography, spacing, shapes — into a `resumo.md` that the preview (step 4) and the design system (step 7) can use.

This step is about **style**, not structure: page structure becomes wireframes in step 6.

Inputs: the screenshots in `etapas/00_briefing/prints/` and the briefing's **Screenshots received** table (which site each one is from and what the user wants to take). Without screenshots, record step 3 as `not applicable` in `etapas/aprovacoes.md` and move on to step 4.

Output: `etapas/01_extracao/prints/` with `cores.md`, `cores.json` and `resumo.md`.

## Honest limitation

An image doesn't keep exact values: compression, antialiasing, shadows and the screenshot's scale change colors and measurements. That's why **every value in this step is "(estimated)"** and, in the project's trust order, loses to the value measured in code (step 2). If the same site went through step 2, use the screenshot only to confirm and for what the code didn't show.

## 1. Colors (script)

```bash
pip install pillow   # if needed
python .claude/skills/extrair-design-prints/scripts/extrair_cores.py etapas/00_briefing/prints --saida etapas/01_extracao/prints
```

For each screenshot, the script lists: size and **likely scale** (1x or retina — use it to convert measurements), dominant colors with area percentage, likely background/text/accent and the contrast of those pairs; plus a combined palette of all screenshots. It quantizes loosely so it doesn't swallow small colors such as a button's.

Check the result by looking at the image: the script doesn't know what's a logo, photo or widget. A color that only appears in a photo isn't part of the palette.

## 2. Typography, spacing and shapes (visual analysis)

Open each screenshot and estimate, converting by its scale (a 2880px-wide screenshot is 2x: divide measurements by 2):

| Item | What to record |
|------|----------------|
| **Typography** | category of heading and body fonts (serif, geometric sans, humanist, grotesque, monospace, handwritten), apparent weight, uppercase, letter spacing. If you recognize the font with confidence, name it; if not, suggest 2–3 similar free fonts (Google Fonts). |
| **Size scale** | approximate height of h1, h2, body and small text in px; the heading/body ratio. |
| **Spacing** | section breathing room (vertical padding), distance between elements, approximate content width. Say whether it's generous, medium or compact. |
| **Shapes** | corner radius (square, slightly rounded, pill), borders, shadows (none, subtle, strong). |
| **Components** | style of buttons (filled, outline, text), cards, inputs, icons (line, filled), images (photo, illustration, cutouts). |
| **Overall mood** | three adjectives (e.g. "clean, editorial, sober") — they help the image prompt in step 5. |

## 3. Summary

Generate `etapas/01_extracao/prints/resumo.md`:

```markdown
# Design extracted from screenshots

> All values are estimated from images.

## Palette (estimated)
| Role | Color | From which screenshot | Note |
| background | `#f6f6f6` | ref1_hero.png | |
| text | ... | | |
| primary / accent | ... | | contrast with background: 4.75:1 ✅ |

## Typography (estimated)
| Use | Category | Font (recognized or suggested) | Approx. size | Weight |

## Spacing and shapes (estimated)
...

## Components
...

## Per screenshot
### ref1_hero.png — <site>
- What the user wants to take (from the briefing): ...
- What this screenshot shows of it: ...

## Overall mood
...
```

Relate each finding to what the user said they want to **take** or **avoid** in the briefing. A screenshot sent "for the colors" weighs more on the palette; one sent "for the layout" weighs little here.

## Wrap up

Show the user the estimated palette and typography (a short table) and move on to step 4 (`gerar-previa`). This step doesn't require approval; record `done` in `etapas/aprovacoes.md`.

## Usage limits

Screenshots are for extracting style. Never crop or reuse images, logos, icons or text from the screenshots in the final site.
