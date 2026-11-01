---
name: gerar-design-system
description: Cria o design_system.md de um site (paleta de cores, tipografia, espaçamento, grid, breakpoints, bordas, sombras, componentes e regras) e gera tokens.css e tokens para Tailwind a partir dele, com verificação de contraste WCAG. Use sempre que o usuário pedir design system, guia de estilo, style guide, paleta de cores, tipografia ou tokens para um site, ou quando for consolidar referências visuais antes de programar um site.
---

# Gerar design system

O `design_system.md` é a **fonte única da verdade** visual do site. Todo código gerado depois deve obedecer a ele, e toda mudança de estilo começa nele. Isso é o que mantém consistência entre páginas e entre sessões diferentes com a IA.

## Entradas

Leia, se existirem:
- `etapas/00_briefing/briefing.md` — tom da marca e cores obrigatórias.
- `etapas/00_briefing/referencias.md` — o que aproveitar e evitar de cada referência.
- `etapas/01_extracao/codigo/*/resumo.md` — valores reais (fontes, cores, tamanhos, breakpoints).
- `etapas/04_wireframes/especificacao_componentes.md` — papéis tipográficos e espaçamentos usados.

## Como montar

Parta de `assets/design_system_template.md` e preencha **com decisões, não com cópias**. O objetivo é um sistema próprio, coerente com o briefing, inspirado nas referências.

1. **Cores.** Comece pelas cores obrigatórias da marca (briefing). Depois use as referências marcadas como "cores" no `referencias.md`. Defina papéis (primária, hover, secundária, texto, texto secundário, fundo, superfície, borda, erro, sucesso). Mantenha a paleta curta: poucas cores bem usadas parecem mais profissionais.
2. **Tipografia.** No máximo 2 famílias (títulos e texto). Prefira fontes gratuitas (Google Fonts) e sempre com fallback. Se a referência usa fonte paga, sugira uma alternativa gratuita parecida e avise o usuário. Escala tipográfica com H1, H2, H3, body e small; use `clamp()` para títulos grandes responsivos.
3. **Espaçamento.** Escala baseada em 4px ou 8px. Defina o espaço entre seções.
4. **Layout.** Largura máxima do container, padding lateral, grid e breakpoints (use os do HTML extraído, se houver).
5. **Bordas e sombras.** Poucos níveis (2–3 raios, 2 sombras).
6. **Componentes.** Botões (variantes e todos os estados), card, input, link, e os componentes específicos que aparecem no wireframe.
7. **Regras.** Proibições e padrões (ex.: nada fora dos tokens, foco sempre visível).

Registre na seção "Princípios" de qual referência veio cada decisão importante — isso ajuda o usuário a revisar.

## Formato dos tokens

Toda tabela de tokens precisa ter a **primeira coluna no formato `` `--nome` ``** e a segunda com o valor. É assim que o script encontra os tokens. Prefixos que o gerador de Tailwind reconhece: `--color-`, `--space-`, `--radius-`, `--shadow-`, `--font-`, `--text-`.

## Verificar contraste

Antes de finalizar, rode para as combinações de texto/fundo usadas:

```bash
python scripts/contraste.py "#111827:#FFFFFF" "#FFFFFF:#1A56DB"
```

Cole o resultado na tabela de contraste do design system. Se algum par de texto normal ficar abaixo de 4.5:1, ajuste a cor (escurecer/clarear) e explique a mudança ao usuário. Não calcule contraste "de cabeça" — use o script.

## Gerar os arquivos de tokens

```bash
python scripts/gerar_tokens.py etapas/05_design_system/design_system.md \
  --saida etapas/05_design_system/tokens.css \
  --tailwind etapas/05_design_system/tailwind.tokens.js   # só se a stack usar Tailwind
```

Observação: variáveis CSS não funcionam dentro de `@media`. Os tokens `--bp-*` são documentação; nas media queries, use os valores literais.

## Entrega

Mostre ao usuário um resumo visual curto (paleta, fontes, escala) e peça aprovação. Depois de aprovado, qualquer ajuste de estilo deve ser feito no `design_system.md` e os tokens regenerados.

Próxima etapa: `construir-site`.
