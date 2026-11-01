---
name: gerar-wireframes
description: Gera os wireframes em SVG (tons de cinza, seções anotadas) de todas as páginas e subpáginas do site, em desktop e celular, a partir da imagem do site aprovada e da prévia, com página de revisão para aprovação do usuário; depois detalha a especificação de componentes. Use no passo 6 do fluxo, depois da imagem do site aprovada, ou quando o usuário pedir wireframe, esqueleto de página, estrutura de layout, mapa das páginas ou especificação de componentes.
---

# Wireframes de todas as páginas (passo 6)

Objetivo: fixar a **estrutura** de cada página do site num wireframe SVG aprovado pelo usuário. A imagem do site (passo 5) mostrou como o site pode ficar; o wireframe diz exatamente quais seções existem, em que ordem, com que layout e quantos elementos — e o que muda no celular. Na construção (passo 8), o wireframe aprovado é a referência oficial de estrutura.

Os wireframes são em tons de cinza de propósito: separar estrutura de estilo evita discutir cor quando o assunto é layout. O estilo é decidido no passo 7.

## Entradas

- `etapas/02_previa/previa_site.md` — **todas** as páginas e seções, em ordem. É a lista do que desenhar.
- `etapas/03_mockup/` — a imagem aprovada (`mockup_home-desktop`, `-mobile`): proporções, organização das seções, ritmo.
- `etapas/00_briefing/briefing.md` — para conferir funcionalidades e conteúdo.

## Parte 1 — Wireframes SVG

Desenhe **uma página por vez**, de cima para baixo, seção por seção, copiando `assets/wireframe_template.svg` e seguindo as convenções dele.

### Quais páginas
- Toda página da prévia (Home e subpáginas: Sobre, Serviços, Contato, páginas de detalhe...).
- Páginas que não têm imagem aprovada seguem a linguagem da Home: o mesmo header e footer, a mesma lógica de grid e espaçamento. Componentes que se repetem (header, footer, card, CTA) têm a mesma estrutura em todas as páginas.
- Landing page: uma página só, mas com todas as seções.

### Arquivos
- `etapas/04_wireframes/wireframe_<pagina>-desktop.svg` — obrigatório, largura 1440 (`viewBox="0 0 1440 <altura>"`).
- `etapas/04_wireframes/wireframe_<pagina>-mobile.svg` — obrigatório para a Home; recomendado para as demais. Sem imagem de celular, deduza do desktop e marque suposições com `(incerto)`.
- `<pagina>` em minúsculas, sem acento: `home`, `sobre`, `servicos`, `contato`.

### Convenções do SVG
- Raiz `<svg>` com `viewBox`, `data-pagina` e `data-viewport` (`desktop` | `mobile`), seguida de `<title>` e `<desc>`.
- **Cada seção é um `<g class="secao">`** posicionado com `transform="translate(0,y)"`, com:
  - `id` em minúsculas (`header`, `hero`, `servicos`...);
  - `data-nome` — nome da seção em caixa alta (HEADER, HERO, SERVIÇOS, DEPOIMENTOS, CTA, FOOTER...);
  - `data-layout` — `1 coluna`, `2 colunas 60/40`, `grid 3 colunas`...;
  - `data-largura` (`container` | `full-width`), `data-altura` (`auto`, `~100vh`...);
  - `data-elementos` — lista com quantidades (`H1, parágrafo, 2 botões, imagem`);
  - `data-mobile` — o que muda no celular (obrigatório no arquivo desktop);
  - opcionais: `data-alinhamento`, `data-comportamento` (ex.: `fixo no topo`).
- Rótulo da seção em `<text class="rotulo-sec">`.
- Elementos com as classes do `<style>` do modelo: `texto` (barras no lugar de textos, uma por linha), `bloco` (logo, cards), `botao-prim` / `botao`, `imagem` + duas linhas `imagem-x`.
- Cada elemento tem um `<text class="rotulo">` com a **função** do conteúdo (`H1 (proposta de valor, ~8 palavras, 2 linhas)`).
- Grupos repetidos levam `data-elemento` e `data-quantidade` (`<g data-elemento="card" data-quantidade="3">`).
- Proporções e posições como na imagem aprovada, dentro do container de 1200px (margens de 120px no desktop).
- Na dúvida, `(incerto)` num `<text class="nota">` — não invente.

### Proibido no SVG
`<image>`, `<script>`, `<foreignObject>`, links externos, imagens em base64, cores, fontes, logos ou textos copiados das referências.

### Validar e montar a revisão
```bash
S=.claude/skills/gerar-wireframes/scripts
python $S/validar_wireframe.py etapas/04_wireframes/*.svg
python $S/gerar_indice.py etapas/04_wireframes
```
Corrija tudo o que o validador marcar com ✗. O `gerar_indice.py` cria `etapas/04_wireframes/index.html` com todas as páginas lado a lado (desktop e celular) e a lista de seções de cada uma.

### Aprovação
Abra o `index.html` no navegador e peça ao usuário para revisar **todas** as páginas. Ajuste até ele aprovar explicitamente; regenere o índice a cada rodada. Aprovado, registre em `etapas/aprovacoes.md` (passo 6, páginas aprovadas, `aprovado`, data). Mudar estrutura depois da construção é caro — vale a pausa.

## Parte 2 — Especificação de componentes

Com os wireframes aprovados, detalhe cada componente em `etapas/04_wireframes/especificacao_componentes.md` (modelo em `assets/especificacao_template.md`):

- **Tipografia:** papel (H1, H2, body...), peso, alinhamento.
- **Posição e alinhamento** dentro da seção.
- **Espaçamentos** internos e entre elementos, por papel (`espaço-lg`).
- **Responsividade:** o que muda em tablet e celular.
- **Estados:** hover, foco, ativo, desabilitado.

O design system ainda não existe neste ponto: referencie os valores por papel e registre os valores candidatos numa tabela no fim, com a origem, na ordem de confiança do projeto — decisão do usuário > medido no código (passo 2) > estimado dos prints (passo 3) > lido da imagem aprovada (passo 5). O passo 7 transforma esses papéis em tokens.

Próximo passo: `gerar-design-system` (passo 7).
