---
name: print-para-wireframe
description: Converte prints de tela de sites em wireframes em texto (Markdown/ASCII) e depois em uma especificação detalhada de componentes com tipografia, posição, espaçamento, responsividade e estados. Use sempre que o usuário enviar prints/screenshots de sites ou layouts e quiser reproduzir, adaptar ou se inspirar na estrutura, ou pedir wireframe, esqueleto de página, estrutura de layout ou especificação de componentes.
---

# Print → wireframe → especificação

A IA erra detalhes finos quando lê imagens: tamanhos de fonte, espaçamentos, cores exatas e alinhamentos. Então o print **nunca** é a referência final. Ele é apenas a entrada para gerar um wireframe em texto, e o wireframe é que passa a ser a referência oficial. Os valores numéricos vêm do HTML extraído (etapa anterior), não da imagem.

## Entradas

- Prints das seções (idealmente um print por seção, em largura desktop; prints de mobile ajudam muito na responsividade).
- `02_html_referencias/<site>/resumo.md`, se existir.
- `00_briefing/briefing.md` e `01_referencias/referencias.md`.

## Parte 1 — Wireframe (só estrutura)

Para cada print, descreva a página **de cima para baixo, seção por seção**. Nesta parte, ignore cores e estilos: foque em estrutura. Separar estrutura de estilo evita que a IA "grude" no visual da referência.

Formato obrigatório para cada seção (veja `assets/wireframe_template.md`):

```
### [NOME DA SEÇÃO]
Layout: <1 coluna | 2 colunas 60/40 | grid 3 colunas | ...>
Largura: <container | full-width>
Altura aproximada: <auto | ~100vh | ...>

| Coluna esquerda              | Coluna direita       |
|------------------------------|----------------------|
| Eyebrow (texto pequeno)      | Imagem ilustrativa   |
| H1 (2 linhas)                |                      |
| Parágrafo (3 linhas)         |                      |
| [Botão primário] [Botão sec.]|                      |

Elementos: H1, parágrafo, 2 botões, imagem
Alinhamento: texto à esquerda, bloco centralizado verticalmente
```

Regras:
- Use nomes de seção padrão (HEADER, HERO, LOGOS, FEATURES, COMO FUNCIONA, DEPOIMENTOS, PREÇOS, FAQ, CTA, FOOTER) para facilitar a reutilização.
- Registre quantidades (3 cards, 5 itens de menu, 6 logos).
- Não transcreva os textos da referência. Use a função do texto ("H1 com proposta de valor, ~8 palavras").
- Se algo no print estiver ambíguo (cortado, pequeno demais), escreva "(incerto)" em vez de inventar.

**Adapte ao briefing.** O wireframe final é do site do usuário, não da referência. Remova seções que ele não precisa, acrescente as que estão no briefing, e combine referências conforme o mapa página → referência.

Mostre o wireframe ao usuário e peça aprovação antes da Parte 2. Mudar estrutura depois é caro.

Saída: `03_wireframes/wireframe_<pagina>.md`.

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
