---
name: site-com-referencias
description: Orchestrates the complete process of building a website or landing page with generative AI in 8 steps — interview and briefing, design extraction from references (code and screenshots), preview, site image, wireframes, design system and build with validation — with user approval between steps. Use whenever the user wants to create, redesign or "make a site like" other sites, mentions reference/inspiration sites, or starts a website/landing page project from scratch, even if they don't name the steps. Also use when the user asks "which step am I on" or "what's the next step" in a website project.
---

# Site from references — orchestrator

This skill coordinates an 8-step workflow. Each step has its own skill with the detailed instructions. The job here is to find out which step the project is on, make sure none is skipped, respect the user's approvals and pass the right files from one step to the next.

## Why this workflow exists

AI builds better sites when it receives **structured text** (briefing, extracted design, SVG wireframes, tokens) than when it improvises from images. The workflow first understands the business, then extracts the design from the references, lets creativity happen in a site image, pins down the structure in wireframes and the style in the design system — and only then writes code. The approvals exist because decisions made early contaminate everything else: fixing a briefing takes minutes, fixing a finished site takes hours.

## Steps and skills

| # | Step | Skill | Main output | Approval |
|---|------|-------|-------------|----------|
| 1 | Interview and briefing | `entrevista-site` | `etapas/00_briefing/briefing.md` (+ `prints/`) | ✅ required |
| 2 | Design extracted from the references' code | `extrair-html-referencia` | `etapas/01_extracao/codigo/<site>/resumo.md` | — |
| 3 | Design extracted from screenshots | `extrair-design-prints` | `etapas/01_extracao/prints/resumo.md` | — |
| 4 | Site preview | `gerar-previa` | `etapas/02_previa/previa_site.md` | — |
| 5 | Site image | `gerar-mockup` | `etapas/03_mockup/prompt_imagem.md` + image (PNG or SVG) | ✅ required |
| 6 | Wireframes of every page | `gerar-wireframes` | `etapas/04_wireframes/*.svg` + `especificacao_componentes.md` | ✅ required |
| 7 | Design system | `gerar-design-system` | `etapas/05_design_system/design_system.md`, `design_system.html`, `tokens.css` | ✅ required |
| 8 | Plan, build and validation | `construir-site` | `etapas/06_construcao/plano_construcao.md`, `site/`, `relatorio_validacao.md` | — |

Steps without a reference of a given type are skipped and recorded: without URLs, step 2 doesn't apply; without screenshots, step 3 doesn't apply. Write "not applicable" in `etapas/aprovacoes.md` and move on.

## Before step 1 — skills setup

Third-party skills don't ship with the template. If `frontend-design`, `playwright-cli` and the other required ones (listed in `docs/skills-obrigatorias.md`) aren't available, ask the user to run `./scripts/setup-skills.sh obrigatorias` and restart Claude Code. If the interview points to animations or videos, afterwards also `./scripts/setup-skills.sh animacao`. Never install a third-party skill without the script's audit.

## Approvals

Steps 1, 5, 6 and 7 only finish when the user explicitly approves the result.

1. When one of these steps is done, show what was generated (open the image, SVGs or HTML in the browser when possible) and ask whether they approve or what they want to change.
2. Adjust and show it again until they approve. Don't interpret silence or "ok, what now?" as approval — ask.
3. Once approved, record it in `etapas/aprovacoes.md`: step, approved files, date and notes. Only then move on.
4. If the user changes something in an already-approved step, update the source file, mark the approval as "revised" and check whether the following steps need to be redone (e.g. changing the briefing may change the preview and the image).

## Project folder structure

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

Create any missing folders.

## How to drive it

1. **Find the current step.** Read `etapas/aprovacoes.md` and see which outputs in the table already exist. The current step is the first one whose output doesn't exist — or, for steps with approval, whose approval isn't recorded.
2. **Read the current step's skill** and follow its instructions.
3. **When a step without approval finishes** (2, 3, 4), show a short summary of what was generated and move on to the next one, unless the user wants to review.
4. **Don't skip steps.** If the user says "just build the site", explain in one sentence that without an approved briefing, wireframes and design system the result is generic, and offer to do the steps quickly. If they insist, respect it, but record the assumptions in `plano_construcao.md`.
5. **Style adjustments go back to the source.** A color that changes during the build changes in `design_system.md` (and in `tokens.css` via the script), not just in the CSS.

## Trust order for design values

When different sources disagree (font size, color, spacing):

1. User decision recorded in the briefing or in an approval.
2. Value extracted from the references' code (step 2) — it's measured, not estimated.
3. Value estimated from screenshots (step 3) — always marked "(estimated)".
4. Value proposed by the site image (step 5) — creative direction, not measured.

## Reference content rule

References are for structure and style. Text, images, logos and proprietary code from the reference sites never go into the final site — use the briefing's content or clearly marked placeholders (`[TEXT: ...]`, `[PHOTO: ...]`). Never use AI to generate images of real people that the site presents as real (team, clients, students).
