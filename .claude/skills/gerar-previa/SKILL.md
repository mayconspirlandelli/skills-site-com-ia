---
name: gerar-previa
description: Compiles the approved briefing and the design extracted from the references (code and screenshots) into a Markdown site preview — pages and sections in order, content of each, visual direction (candidate palette and typography), what comes from each reference and technical decisions — which is the basis for the image prompt and the wireframes. Use in step 4 of the workflow, after the extractions, or when the user asks for a "preview", "overview" or "site summary" before designing.
---

# Site preview (step 4)

Goal: bring everything known so far into a single document that describes the site **before** designing it — `etapas/02_previa/previa_site.md`. The site image (step 5) and the wireframes (step 6) read this file; it is the bridge between "what the user wants" and "how it will look".

## Inputs

- `etapas/00_briefing/briefing.md` (approved) — the main source.
- `etapas/01_extracao/codigo/<site>/resumo.md` — design measured in code (step 2), if any.
- `etapas/01_extracao/prints/resumo.md` — design estimated from screenshots (step 3), if any.

## How to compile

1. **Structure comes from the briefing.** The preview's pages and sections are the briefing's, in the same order. Use the references only to suggest *how* each section is organized (e.g. "2-column hero, like Ref 1"), never to add sections the user didn't ask for.
2. **Real content or placeholder.** For each section, say what it communicates and which briefing content goes in. Whatever doesn't exist becomes `[TEXT: ...]`, `[PHOTO: ...]`, `[TESTIMONIAL: ...]`. Never use text from the references.
3. **Visual direction by consensus.** Build the candidate palette and typography by cross-checking the sources, in the project's trust order: user decision (brand colors, tastes in the briefing) > value measured in code > value estimated from screenshots. For each color and font, say where it came from. Discard what the user said they want to **avoid**.
4. **Conflicts in plain sight.** If the references pull in opposite directions (one dark and dense, another light and airy), don't choose silently: list the conflict and propose a decision.
5. **Technical decisions at the end.** Stack, hosting, Docker, responsive/PWA, features — copied from the briefing, so step 8 has everything in one place.

Use `assets/previa_template.md`.

## Wrap up

Show the user the page map and the visual direction (palette + typography in a short table) and any conflicts found. This step doesn't require formal approval, but resolve the conflicts with the user before moving on — the site image will materialize these choices. Record `done` in `etapas/aprovacoes.md`.

Next step: `gerar-mockup` (step 5).
