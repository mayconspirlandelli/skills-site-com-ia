# Projeto de site com IA generativa

Este repositório segue um fluxo de 8 passos para criar sites e landing pages a partir de referências,
com aprovação do usuário entre as etapas. O plano completo está em `docs/plano.md`.

## Como começar
- No início de qualquer sessão, use a skill **site-com-referencias** para descobrir em que passo o projeto está e qual é o próximo. O estado fica nas pastas de `etapas/` e em `etapas/aprovacoes.md`.
- Antes do passo 1, as skills obrigatórias de terceiros precisam estar instaladas (`./scripts/setup-skills.sh obrigatorias`).
- Siga os passos na ordem. Os passos 1, 5, 6 e 7 só avançam com aprovação explícita do usuário, registrada em `etapas/aprovacoes.md`.
- Não gere código do site antes de existir `etapas/05_design_system/design_system.md` aprovado, a menos que o usuário peça explicitamente — nesse caso, registre as suposições feitas.

## Passos e pastas
| # | Passo | Skill | Pasta | Aprovação |
|---|-------|-------|-------|-----------|
| 1 | Entrevista e briefing | entrevista-site | `etapas/00_briefing/` | ✅ |
| 2 | Design extraído do código das referências | extrair-html-referencia | `etapas/01_extracao/codigo/` | |
| 3 | Design extraído dos prints | extrair-design-prints | `etapas/01_extracao/prints/` | |
| 4 | Prévia do site | gerar-previa | `etapas/02_previa/` | |
| 5 | Imagem do site (SVG) | gerar-mockup | `etapas/03_mockup/` | ✅ |
| 6 | Wireframes de todas as páginas | gerar-wireframes | `etapas/04_wireframes/` | ✅ |
| 7 | Design system (.md + .html) | gerar-design-system | `etapas/05_design_system/` | ✅ |
| 8 | Plano, construção e validação | construir-site | `etapas/06_construcao/` e `site/` | |

## Regras permanentes
- `etapas/05_design_system/design_system.md` é a fonte única da verdade visual. Mudança de estilo começa nele; depois regenere `tokens.css` com o script da skill gerar-design-system.
- No código, use apenas tokens (nada de cores, tamanhos ou espaçamentos soltos).
- Ordem de confiança dos valores de design: decisão do usuário > valor extraído do código das referências > valor estimado dos prints (sempre marcado "(estimado)") > proposta da imagem do site.
- A estrutura oficial das páginas são os wireframes SVG aprovados (`etapas/04_wireframes/`), não prints nem a imagem do site.
- Nunca copie textos, imagens, logos ou código das referências para o site final. Use o conteúdo do briefing ou placeholders `[TEXTO: ...]`.
- Construa o site em `site/` seção por seção, conferindo cada uma com o wireframe, e valide o resultado contra `etapas/06_construcao/plano_construcao.md`.
- Converse com o usuário em português.

## Segurança de skills de terceiros
- **Nunca** instale, copie ou ative skill, plugin ou marketplace de terceiros sem antes usar a skill **auditar-skill**. Vale também para servidores MCP: leia o código antes de configurar.
- Audite sempre em pasta temporária, sem executar nada da skill. Prefira `./scripts/adicionar-skill.sh`, que já audita antes de instalar.
- Veredito BLOQUEAR: não instale. REVISAR: só com confirmação explícita do usuário após ver os achados.
- Registre o commit auditado na tabela abaixo. Atualizou a skill? Audite de novo.

## Skills obrigatórias
Todo projeto de website precisa de: `frontend-design`, `web-design-guidelines`, `image-to-code`,
`design-taste-frontend`, `playwright-cli`, `diagram-design` e `impeccable` (commit fixo revisado — ver `etapas/auditorias/excecoes.txt`). Comandos e passo a passo em `docs/skills-obrigatorias.md`.
No início do projeto, verifique se estão instaladas; se faltar alguma, audite com **auditar-skill** antes de instalar.
Se o projeto precisar de animações ou vídeos, inclua também `remotion-best-practices` e `motion-design` (`./scripts/setup-skills.sh animacao`).

## Stack padrão
A stack, a hospedagem e o uso de Docker são decididos na entrevista e registrados no briefing. Sem definição, use HTML + Tailwind, mobile-first.

## Skills adicionais deste projeto
<!-- Registre aqui as skills instaladas durante o projeto e quando usá-las. -->
| Skill | Origem @ commit auditado | Veredito | Quando usar |
|-------|--------------------------|----------|-------------|
| | | | |
