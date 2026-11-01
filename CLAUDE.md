# Projeto de site com IA generativa

Este repositório segue um fluxo em etapas para criar sites a partir de referências.
O plano completo está em `docs/plano.md`.

## Como começar
- No início de qualquer sessão, use a skill **site-com-referencias** para descobrir em que etapa o projeto está e qual é o próximo passo.
- **Setup obrigatório, nesta ordem, antes de qualquer outra etapa:**
  1. Auditar e instalar as skills `grill-me` e `grilling` — sempre as primeiras do projeto (`./scripts/setup-skills.sh inicial`).
  2. Entrevistar o usuário com a `grilling` (ou o usuário digita `/grill-me`) sobre o website/landing page e salvar o plano em `00_briefing/entrevista.md`.
  3. Com base no plano da entrevista, criar os prompts para gerar as imagens do site (mockups das páginas e imagens de conteúdo) em `00_briefing/prompts_imagens.md`.
  4. Auditar e instalar as demais skills obrigatórias (`./scripts/setup-skills.sh obrigatorias`; ver `docs/skills-obrigatorias.md`).
  5. Seguir os passos de `docs/plano.md`.
- Siga as etapas na ordem. Não gere código do site antes de existir `04_design_system/design_system.md`, a menos que o usuário peça explicitamente — nesse caso, registre as suposições feitas.

## Etapas e pastas
| Etapa | Skill | Pasta |
|-------|-------|-------|
| Setup e entrevista | grill-me / grilling (terceiros) | `00_briefing/entrevista.md` |
| Briefing e referências | referencias-briefing | `00_briefing/`, `01_referencias/` |
| Extração de HTML | extrair-html-referencia | `02_html_referencias/` |
| Wireframe e especificação | print-para-wireframe | `03_wireframes/` |
| Design system | gerar-design-system | `04_design_system/` |
| Construção e validação | construir-site | `05_site/` |

## Regras permanentes
- `04_design_system/design_system.md` é a fonte única da verdade visual. Mudança de estilo começa nele; depois regenere `tokens.css` com o script da skill gerar-design-system.
- No código, use apenas tokens (nada de cores, tamanhos ou espaçamentos soltos).
- Prints de tela nunca são referência final: viram wireframe em SVG (`03_wireframes/wireframe_<pagina>-desktop.svg`). Valores numéricos vêm do HTML extraído.
- Nunca copie textos, imagens, logos ou código das referências para o site final. Use o conteúdo do briefing ou placeholders `[TEXTO: ...]`.
- Construa o site seção por seção, conferindo cada uma com o wireframe.
- Converse com o usuário em português.

## Segurança de skills de terceiros
- **Nunca** instale, copie ou ative skill, plugin ou marketplace de terceiros sem antes usar a skill **auditar-skill**.
- Audite sempre em pasta temporária, sem executar nada da skill. Prefira `./scripts/adicionar-skill.sh`, que já audita antes de instalar.
- Veredito BLOQUEAR: não instale. REVISAR: só com confirmação explícita do usuário após ver os achados.
- Registre o commit auditado na tabela abaixo. Atualizou a skill? Audite de novo.

## Skills obrigatórias
Todo projeto de website precisa de: `grill-me` e `grilling` (as primeiras), `frontend-design`, `web-design-guidelines`, `image-to-code`,
`design-taste-frontend`, `playwright-cli` e `diagram-design`. Comandos e passo a passo em `docs/skills-obrigatorias.md`.
No início do projeto, verifique se estão instaladas; se faltar alguma, audite com **auditar-skill** antes de instalar.
Se o projeto precisar de animações ou vídeos, inclua também `remotion-best-practices` e `motion-design` (`./scripts/setup-skills.sh animacao`).

## Stack padrão
A stack é decidida na entrevista (`grill-me`) e registrada no briefing. Sem definição, use HTML + Tailwind, mobile-first.

## Skills adicionais deste projeto
<!-- Registre aqui as skills instaladas durante o projeto e quando usá-las. -->
| Skill | Origem @ commit auditado | Veredito | Quando usar |
|-------|--------------------------|----------|-------------|
| | | | |
