---
name: print-para-wireframe
description: Converte prints/imagens de tela de sites em wireframes no formato SVG (arquivo .svg em tons de cinza, com seções anotadas) e depois em uma especificação detalhada de componentes com tipografia, posição, espaçamento, responsividade e estados. Use sempre que o usuário enviar prints, screenshots ou imagens de sites ou layouts e quiser reproduzir, adaptar ou se inspirar na estrutura, ou pedir wireframe, wireframe SVG, esqueleto de página, estrutura de layout ou especificação de componentes.
---

# Imagem → wireframe SVG → especificação

A IA erra detalhes finos quando lê imagens: tamanhos de fonte, espaçamentos, cores exatas e alinhamentos. Então o print **nunca** é a referência final. Ele é apenas a entrada para gerar um **wireframe em SVG**, e o wireframe é que passa a ser a referência oficial. O SVG é texto: a IA lê a estrutura pelos `id` e atributos `data-*`, e o usuário vê o desenho no navegador. Os valores numéricos de estilo vêm do HTML extraído (etapa anterior), não da imagem.

## Entradas

- Prints/imagens das seções (idealmente um por seção, em largura desktop; prints de mobile ajudam muito na responsividade).
- `02_html_referencias/<site>/resumo.md`, se existir.
- `00_briefing/briefing.md` e `01_referencias/referencias.md`.

## Parte 1 — Wireframe SVG (só estrutura)

Para cada página, analise as imagens **de cima para baixo, seção por seção**, e desenhe um SVG. Nesta parte, ignore cores e estilos da referência: o wireframe é sempre em tons de cinza. Separar estrutura de estilo evita que a IA "grude" no visual da referência.

Comece copiando `assets/wireframe_template.svg` e siga as convenções dele.

### Arquivos

- `03_wireframes/wireframe_<pagina>-desktop.svg` — obrigatório, largura 1440 (`viewBox="0 0 1440 <altura>"`).
- `03_wireframes/wireframe_<pagina>-mobile.svg` — recomendado, largura 390. Se não houver print mobile, deduza a partir do desktop e marque as suposições com `(incerto)`.

### Convenções do SVG

- Raiz `<svg>` com `viewBox`, `data-pagina` e `data-viewport` (`desktop` | `mobile`), seguida de `<title>` e `<desc>` (referências usadas).
- **Cada seção é um `<g class="secao">`** posicionado com `transform="translate(0,y)"`, com:
  - `id` em minúsculas (`header`, `hero`, `features`...);
  - `data-nome` — nome padrão: HEADER, HERO, LOGOS, FEATURES, COMO FUNCIONA, DEPOIMENTOS, PREÇOS, FAQ, CTA, FOOTER;
  - `data-layout` — `1 coluna`, `2 colunas 60/40`, `grid 3 colunas`...;
  - `data-largura` (`container` | `full-width`), `data-altura` (`auto`, `~100vh`...);
  - `data-elementos` — lista com quantidades (`H1, parágrafo, 2 botões, imagem`);
  - `data-mobile` — o que muda no mobile (obrigatório no arquivo desktop);
  - opcionais: `data-alinhamento`, `data-comportamento` (ex.: `fixo no topo`).
- Rótulo da seção em `<text class="rotulo-sec">` no canto superior esquerdo.
- Elementos desenhados com as classes do `<style>` do modelo:
  - `texto` — barras cinza no lugar de títulos/parágrafos (uma barra por linha);
  - `bloco` — logo, cards, containers;
  - `botao-prim` / `botao` — botões primário e secundário;
  - `imagem` + duas linhas `imagem-x` em diagonal — imagens e ilustrações.
- Cada elemento tem um `<text class="rotulo">` dizendo a **função** do texto (`H1 (proposta de valor, ~8 palavras, 2 linhas)`), nunca o texto da referência.
- Grupos repetidos levam `data-elemento` e `data-quantidade` (`<g data-elemento="card" data-quantidade="3">`).
- Mantenha proporções e posições aproximadas do print (colunas, alinhamentos, alturas relativas), dentro do container de 1200px centralizado (margens de 120px no desktop).
- Ambíguo no print (cortado, pequeno demais)? Escreva `(incerto)` num `<text class="nota">` em vez de inventar.

### Proibido no SVG

- `<image>`, `<script>`, `<foreignObject>`, links externos e imagens em base64 — nunca embuta o print nem partes dele.
- Cores, fontes, logos ou textos copiados da referência.

### Adapte ao briefing

O wireframe final é do site do usuário, não da referência. Remova seções que ele não precisa, acrescente as que estão no briefing, e combine referências conforme o mapa página → referência.

### Validar e aprovar

1. Rode o validador (sintaxe, atributos obrigatórios e itens proibidos):
   ```bash
   python3 .claude/skills/print-para-wireframe/scripts/validar_wireframe.py 03_wireframes/*.svg
   ```
   Corrija tudo o que aparecer com ✗.
2. Mostre o SVG ao usuário (abra no navegador) e peça aprovação antes da Parte 2. Mudar estrutura depois é caro.

## Parte 2 — Especificação de componentes

Com o wireframe aprovado, detalhe cada componente em `03_wireframes/especificacao_componentes.md` (modelo em `assets/especificacao_template.md`):

- **Tipografia:** estilo do design system (H1, H2, body...), peso, alinhamento.
- **Posição e alinhamento** dentro da seção.
- **Espaçamentos** internos e entre elementos, na escala de espaçamento.
- **Responsividade:** o que muda em tablet e mobile (colunas empilham? menu vira hambúrguer? imagem some ou vai para cima?).
- **Estados:** hover, foco, ativo, desabilitado.

De onde vêm os valores, em ordem de preferência:
1. `resumo.md` do HTML extraído (valores reais).
2. Design system, se já existir.
3. Estimativa a partir do print — marcar como "(estimado)".

Quando o design system ainda não existe, referencie os valores por nome de papel (ex.: "H1", "espaço-lg") e registre os valores reais numa tabela no fim. A próxima skill (`gerar-design-system`) vai consolidar esses nomes em tokens.

Próxima etapa: `gerar-design-system`.
