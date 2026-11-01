---
name: gerar-design-system
description: Cria o design system do site em Markdown (design_system.md — paleta, tipografia, espaçamento, grid, breakpoints, bordas, sombras, componentes e regras) e em HTML (design_system.html, versão visual para revisão), mais tokens.css e tokens para Tailwind, com verificação de contraste WCAG e aprovação do usuário. Use no passo 7 do fluxo, depois dos wireframes aprovados, ou sempre que o usuário pedir design system, guia de estilo, style guide, paleta, tipografia ou tokens para um site.
---

# Design system (passo 7)

O `design_system.md` é a **fonte única da verdade** visual do site. Todo código do passo 8 obedece a ele, e toda mudança de estilo começa nele. Este passo transforma a direção visual aprovada (imagem do site) e os valores extraídos das referências num sistema próprio, coerente e verificado — e o usuário aprova vendo a versão em HTML.

## Entradas

- `etapas/00_briefing/briefing.md` — cores obrigatórias da marca, gostos, tom.
- `etapas/02_previa/previa_site.md` — paleta e tipografia candidatas, com a origem de cada valor.
- `etapas/03_mockup/` — a imagem aprovada: a direção visual que o usuário escolheu.
- `etapas/01_extracao/codigo/*/resumo.md` e `etapas/01_extracao/prints/resumo.md` — valores medidos e estimados.
- `etapas/04_wireframes/especificacao_componentes.md` — papéis tipográficos, espaçamentos e componentes usados.

## Como montar

Parta de `assets/design_system_template.md` e preencha **com decisões, não com cópias**. Quando as fontes discordarem, siga a ordem de confiança: decisão do usuário > medido no código > estimado dos prints > lido da imagem aprovada. A imagem aprovada manda na **direção** (clima, contraste geral, onde a cor principal aparece); os valores exatos vêm de decisões e medições.

1. **Cores.** Comece pelas cores obrigatórias da marca. Defina papéis (primária, hover, secundária, texto, texto secundário, fundo, superfície, borda, erro, sucesso). Paleta curta: poucas cores bem usadas parecem mais profissionais. Se o briefing pediu modo escuro, defina os pares claro/escuro.
2. **Tipografia.** No máximo 2 famílias (títulos e texto), gratuitas (Google Fonts), sempre com fallback. Fonte paga numa referência → alternativa gratuita parecida, e avise o usuário. Escala com H1, H2, H3, body e small; `clamp()` para títulos grandes.
3. **Espaçamento.** Escala de 4px ou 8px. Espaço entre seções no desktop e no celular.
4. **Layout.** Largura máxima do container, padding lateral, grid e breakpoints (os medidos no código, se houver).
5. **Bordas e sombras.** Poucos níveis (2–3 raios, 2 sombras).
6. **Componentes.** Todos os que aparecem nos wireframes aprovados — botões (variantes e estados), cards, campos, links, menu, e os específicos do site.
7. **Regras.** Proibições e padrões (nada fora dos tokens, foco sempre visível).

Registre em "Princípios" de onde veio cada decisão importante — ajuda o usuário a revisar.

## Formato dos tokens

Toda tabela de tokens tem a **primeira coluna no formato `` `--nome` ``** e a segunda com o valor — é assim que os scripts encontram os tokens. Prefixos reconhecidos: `--color-`, `--space-`, `--radius-`, `--shadow-`, `--font-`, `--text-` (e `--container-`, `--bp-` para layout). Na tabela de `--text-*`, mantenha as colunas Peso e Altura de linha: a versão HTML usa as duas.

## Verificar contraste

Para cada combinação de texto e fundo usada:

```bash
python .claude/skills/gerar-design-system/scripts/contraste.py "#111827:#FFFFFF" "#FFFFFF:#1A56DB"
```

Cole o resultado na tabela de contraste. Texto normal abaixo de 4.5:1 → ajuste a cor e explique a mudança ao usuário. Não calcule contraste "de cabeça".

## Gerar os arquivos

```bash
S=.claude/skills/gerar-design-system/scripts
D=etapas/05_design_system
python $S/gerar_tokens.py $D/design_system.md --saida $D/tokens.css --tailwind $D/tailwind.tokens.js   # --tailwind só se a stack usar Tailwind
python $S/gerar_html.py $D/design_system.md --saida $D/design_system.html
```

O `design_system.html` é a versão visual: amostras de cor com contraste calculado, escala tipográfica renderizada, espaçamentos, raios, sombras, layout e componentes de exemplo montados só com os tokens. **Nunca edite o HTML nem o `tokens.css` à mão** — mude o `.md` e gere de novo.

Variáveis CSS não funcionam dentro de `@media`: os tokens `--bp-*` são documentação; nas media queries, use os valores literais.

## Aprovação

Abra o `design_system.html` no navegador e mostre ao usuário, junto com um resumo (paleta, fontes, escala). Ajuste no `.md`, regenere e mostre de novo até ele aprovar explicitamente. Aprovado, registre em `etapas/aprovacoes.md` (passo 7, `05_design_system/`, `aprovado`, data).

Depois de aprovado, qualquer ajuste de estilo — inclusive durante a construção — é feito no `design_system.md`, com os tokens e o HTML regenerados.

Próximo passo: `construir-site` (passo 8).
