# Projeto de site com IA generativa

Este repositório segue um fluxo em etapas para criar sites a partir de referências.
O plano completo está em `docs/plano.md`.

## Como começar
- No início de qualquer sessão, use a skill **site-com-referencias** para descobrir em que etapa o projeto está e qual é o próximo passo.
- Siga as etapas na ordem. Não gere código do site antes de existir `04_design_system/design_system.md`, a menos que o usuário peça explicitamente — nesse caso, registre as suposições feitas.

## Etapas e pastas
| Etapa | Skill | Pasta |
|-------|-------|-------|
| Briefing e referências | referencias-briefing | `00_briefing/`, `01_referencias/` |
| Extração de HTML | extrair-html-referencia | `02_html_referencias/` |
| Wireframe e especificação | print-para-wireframe | `03_wireframes/` |
| Design system | gerar-design-system | `04_design_system/` |
| Construção e validação | construir-site | `05_site/` |

## Regras permanentes
- `04_design_system/design_system.md` é a fonte única da verdade visual. Mudança de estilo começa nele; depois regenere `tokens.css` com o script da skill gerar-design-system.
- No código, use apenas tokens (nada de cores, tamanhos ou espaçamentos soltos).
- Prints de tela nunca são referência final: viram wireframe em texto. Valores numéricos vêm do HTML extraído.
- Nunca copie textos, imagens, logos ou código das referências para o site final. Use o conteúdo do briefing ou placeholders `[TEXTO: ...]`.
- Construa o site seção por seção, conferindo cada uma com o wireframe.
- Converse com o usuário em português.

## Stack padrão
<!-- Ajuste por projeto. Se o briefing definir outra, o briefing vale. -->
HTML + Tailwind, mobile-first.

## Skills adicionais deste projeto
<!-- Registre aqui as skills instaladas durante o projeto e quando usá-las. -->
| Skill | Origem | Quando usar |
|-------|--------|-------------|
| | | |
