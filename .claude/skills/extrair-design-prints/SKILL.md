---
name: extrair-design-prints
description: Extrai o design system de prints de tela de sites de referência — paleta de cores com área e contraste (script), tipografia, escala de tamanhos, espaçamentos, raios, sombras e estilo de componentes (análise visual) — gerando um resumo.md com todos os valores marcados como estimados. Use no passo 3 do fluxo, quando o briefing aprovado tiver prints em etapas/00_briefing/prints/, ou sempre que o usuário enviar prints e pedir as cores, fontes ou o "estilo" deles.
---

# Design extraído dos prints (passo 3)

Objetivo: tirar dos prints enviados na entrevista o **estilo** que o usuário gostou — cores, tipografia, espaçamentos, formas — num `resumo.md` que a prévia (passo 4) e o design system (passo 7) conseguem usar.

Este passo cuida de **estilo**, não de estrutura: a estrutura das páginas vira wireframe no passo 6.

Entradas: os prints em `etapas/00_briefing/prints/` e a tabela **Prints recebidos** do briefing (de qual site é cada um e o que o usuário quer aproveitar). Sem prints, registre o passo 3 como `não se aplica` em `etapas/aprovacoes.md` e siga para o passo 4.

Saída: `etapas/01_extracao/prints/` com `cores.md`, `cores.json` e `resumo.md`.

## Limite honesto

Imagem não guarda valores exatos: compressão, antialiasing, sombras e a escala do print alteram cores e medidas. Por isso **todo valor deste passo é "(estimado)"** e, na ordem de confiança do projeto, perde para o valor medido no código (passo 2). Se o mesmo site tiver passado pelo passo 2, use o print só para confirmar e para o que o código não mostrou.

## 1. Cores (script)

```bash
pip install pillow   # se necessário
python .claude/skills/extrair-design-prints/scripts/extrair_cores.py etapas/00_briefing/prints --saida etapas/01_extracao/prints
```

O script lista, por print: tamanho e **escala provável** (1x ou retina — use para converter medidas), cores dominantes com percentual de área, fundo/texto/destaque prováveis e o contraste desses pares; e uma paleta combinada de todos os prints. Ele quantiza com folga para não engolir cores pequenas como a de um botão.

Confira o resultado olhando a imagem: o script não sabe o que é logo, foto ou widget. Uma cor que só aparece numa foto não é da paleta.

## 2. Tipografia, espaçamento e formas (análise visual)

Abra cada print e estime, convertendo pela escala do print (um print de 2880px de largura está em 2x: divida as medidas por 2):

| Item | O que registrar |
|------|-----------------|
| **Tipografia** | categoria da fonte de títulos e de texto (serifada, sem serifa geométrica, humanista, grotesca, monoespaçada, manuscrita), peso aparente, caixa alta, espaçamento entre letras. Se reconhecer a fonte com segurança, cite; se não, sugira 2–3 fontes livres parecidas (Google Fonts). |
| **Escala de tamanhos** | altura aproximada de h1, h2, texto e texto pequeno em px; a razão entre título e texto. |
| **Espaçamento** | respiro das seções (padding vertical), distância entre elementos, largura aproximada do conteúdo. Diga se é generoso, médio ou compacto. |
| **Formas** | raio dos cantos (reto, levemente arredondado, pílula), bordas, sombras (sem, sutil, marcada). |
| **Componentes** | estilo de botões (cheio, contorno, texto), cards, campos, ícones (linha, preenchido), imagens (foto, ilustração, recortes). |
| **Clima geral** | três adjetivos (ex.: "limpo, editorial, sóbrio") — ajudam o prompt da imagem no passo 5. |

## 3. Resumo

Gere `etapas/01_extracao/prints/resumo.md`:

```markdown
# Design extraído dos prints

> Todos os valores são estimados a partir de imagens.

## Paleta (estimado)
| Papel | Cor | De qual print | Observação |
| fundo | `#f6f6f6` | ref1_hero.png | |
| texto | ... | | |
| primária / destaque | ... | | contraste com o fundo: 4.75:1 ✅ |

## Tipografia (estimado)
| Uso | Categoria | Fonte (reconhecida ou sugerida) | Tamanho aprox. | Peso |

## Espaçamento e formas (estimado)
...

## Componentes
...

## Por print
### ref1_hero.png — <site>
- O que o usuário quer aproveitar (do briefing): ...
- O que este print mostra disso: ...

## Clima geral
...
```

Relacione cada achado com o que o usuário disse querer **aproveitar** ou **evitar** no briefing. Um print enviado "pelas cores" pesa mais na paleta; um enviado "pelo layout" pesa pouco aqui.

## Fechar

Mostre ao usuário a paleta e a tipografia estimadas (uma tabela curta) e siga para o passo 4 (`gerar-previa`). Este passo não exige aprovação; registre `concluído` em `etapas/aprovacoes.md`.

## Limite de uso

Os prints servem para extrair estilo. Nunca recorte ou reutilize imagens, logos, ícones ou textos dos prints no site final.
