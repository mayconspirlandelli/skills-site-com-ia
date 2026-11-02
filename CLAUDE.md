# Website project with generative AI

This repository follows an 8-step workflow to build websites and landing pages from references,
with user approval between steps. The full plan is in `docs/plano.md`.

## Getting started
- At the start of any session, use the **site-com-referencias** skill to find out which step the project is on and what comes next. State lives in the `etapas/` folders and in `etapas/aprovacoes.md`.
- Before step 1, the required third-party skills must be installed (`./scripts/setup-skills.sh obrigatorias`).
- Follow the steps in order. Steps 1, 5, 6 and 7 only move on with the user's explicit approval, recorded in `etapas/aprovacoes.md`.
- Do not generate site code before an approved `etapas/05_design_system/design_system.md` exists, unless the user explicitly asks — in that case, record the assumptions made.

## Steps and folders
| # | Step | Skill | Folder | Approval |
|---|------|-------|--------|----------|
| 1 | Interview and briefing | entrevista-site | `etapas/00_briefing/` | ✅ |
| 2 | Design extracted from the references' code | extrair-html-referencia | `etapas/01_extracao/codigo/` | |
| 3 | Design extracted from screenshots | extrair-design-prints | `etapas/01_extracao/prints/` | |
| 4 | Site preview | gerar-previa | `etapas/02_previa/` | |
| 5 | Site image (SVG) | gerar-mockup | `etapas/03_mockup/` | ✅ |
| 6 | Wireframes of every page | gerar-wireframes | `etapas/04_wireframes/` | ✅ |
| 7 | Design system (.md + .html) | gerar-design-system | `etapas/05_design_system/` | ✅ |
| 8 | Plan, build and validation | construir-site | `etapas/06_construcao/` and `site/` | |

## Permanent rules
- `etapas/05_design_system/design_system.md` is the single visual source of truth. Style changes start there; then regenerate `tokens.css` with the gerar-design-system skill's script.
- In code, use tokens only (no loose colors, sizes or spacing).
- Trust order for design values: user decision > value extracted from the references' code > value estimated from screenshots (always marked "(estimated)") > site image proposal.
- The official page structure is the approved SVG wireframes (`etapas/04_wireframes/`), not screenshots or the site image.
- Never copy text, images, logos or code from the references into the final site. Use the briefing's content or `[TEXT: ...]` placeholders.
- Build the site in `site/` section by section, checking each one against the wireframe, and validate the result against `etapas/06_construcao/plano_construcao.md`.
- Talk to the user in English.

## Third-party skill security
- **Never** install, copy or enable a third-party skill, plugin or marketplace without first using the **auditar-skill** skill. This also applies to MCP servers: read the code before configuring.
- Always audit in a temporary folder, without running anything from the skill. Prefer `./scripts/adicionar-skill.sh`, which audits before installing.
- BLOCK verdict: do not install. REVIEW: only with the user's explicit confirmation after seeing the findings.
- Record the audited commit in the table below. Updated the skill? Audit it again.

## Required skills
Every website project needs: `frontend-design`, `web-design-guidelines`, `image-to-code`,
`design-taste-frontend`, `playwright-cli`, `diagram-design` and `impeccable` (fixed reviewed commit — see `etapas/auditorias/excecoes.txt`). Commands and step-by-step in `docs/skills-obrigatorias.md`.
At the start of the project, check that they are installed; if any is missing, audit it with **auditar-skill** before installing.
If the project needs animations or videos, also include `remotion-best-practices` and `motion-design` (`./scripts/setup-skills.sh animacao`).

## Default stack
Stack, hosting and Docker usage are decided in the interview and recorded in the briefing. If undefined, use HTML + Tailwind, mobile-first.

## Additional skills in this project
| Skill | Source @ audited commit | Verdict | When to use |
|-------|-------------------------|---------|-------------|
| | | | |
