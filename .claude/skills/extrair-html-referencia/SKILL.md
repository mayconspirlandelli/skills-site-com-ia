---
name: extrair-html-referencia
description: Extrai o design system dos sites de referência direto do código — HTML, CSS e o resultado do JavaScript (estilos computados no navegador via playwright-cli) — gerando por site um resumo.md com paleta, tipografia, escala de tamanhos, espaçamentos, raios, sombras, containers e breakpoints. Use no passo 2 do fluxo, quando o briefing aprovado tiver URLs de referência, ou sempre que o usuário pedir para "pegar o código", "analisar o CSS" ou "extrair o estilo/design system" de um site.
---

# Design extraído do código das referências (passo 2)

Objetivo: transformar cada site de referência do briefing num `resumo.md` com **valores medidos** — cores, fontes, tamanhos, espaçamentos, raios, sombras, breakpoints — em vez de impressões visuais. Na ordem de confiança do projeto, estes valores só perdem para decisões do usuário.

Entradas: as URLs da seção **H. Referências** de `etapas/00_briefing/briefing.md` (aprovado), com o que aproveitar e o que evitar de cada uma. Sem URLs, registre o passo 2 como `não se aplica` em `etapas/aprovacoes.md` e siga para o passo 3.

Saída: uma pasta por site em `etapas/01_extracao/codigo/<nome-site>/`.

## Por que duas capturas

- **Código estático** (`extrair_referencia.py`): HTML limpo, CSS concatenado, variáveis, `@font-face`, breakpoints. Rápido, mas sites em React/Vue/Next chegam quase vazios.
- **Página renderizada** (`playwright-cli` + `estilos_computados.js`): o navegador abre o site, o JavaScript roda, e medimos o que foi **realmente aplicado** — cor de cada texto, fundo por área, fonte por quantidade de texto, estilo de h1/botão/campo. Funciona para qualquer site e é a medida mais fiel.

Faça as duas sempre que houver `playwright-cli`. Sem ele, use só a estática e avise o usuário sobre o limite.

## 1. Capturar a página renderizada

Para cada URL (troque `<nome-site>` por um nome curto, ex.: `ref1-acme`):

```bash
D=etapas/01_extracao/codigo/<nome-site>; mkdir -p $D
JS=.claude/skills/extrair-html-referencia/scripts/estilos_computados.js
playwright-cli open <url>
playwright-cli resize 1440 900
playwright-cli --raw eval "document.documentElement.outerHTML" > $D/renderizado.html
playwright-cli --raw eval "$(cat $JS)" > $D/computados-desktop.json
playwright-cli resize 390 844
playwright-cli --raw eval "$(cat $JS)" > $D/computados-mobile.json
playwright-cli close
```

Se aparecer banner de cookies cobrindo a página, recuse os não essenciais (a opção mais restritiva) antes de medir. Não faça login nem preencha formulários.

O `estilos_computados.js` só lê a página: não altera nada e não envia dados.

## 2. Rodar os scripts

```bash
pip install beautifulsoup4   # se necessário
S=.claude/skills/extrair-html-referencia/scripts
python $S/extrair_referencia.py --html $D/renderizado.html --base-url <url> --saida $D
python $S/resumir_computados.py --entrada $D/computados-desktop.json $D/computados-mobile.json --saida $D
```

Sem `playwright-cli`: `python $S/extrair_referencia.py --url <url> --saida $D` (ou `--html` com a página salva pelo usuário: `Ctrl+S` → "Página da Web, completa").

Saídas na pasta do site: `limpo.html`, `estilos.css`, `resumo.md`, `dados.json` (estático) e `computados.md` (medido).

**Leia os avisos.** Se a página parecer vazia, se não houver CSS ou se o `computados.md` analisar poucos elementos (ex.: página de bloqueio, captcha, "acesso negado"), não continue com dados ruins: avise o usuário e peça a página salva ou outra URL.

## 3. Consolidar o design system do site

Acrescente ao final do `resumo.md` a seção **"Design system extraído"**, cruzando `resumo.md` (estático) e `computados.md` (medido). Quando discordarem, vale o medido.

| Item | Como chegar |
|------|-------------|
| **Paleta com papéis** | fundo (maior área), texto (mais caracteres), primária (fundo do botão/links), secundária, bordas, estados. Descarte cores de widgets de terceiros (chat, cookies, mapas). |
| **Tipografia** | fonte de títulos e de texto (separe fontes de ícones e fallbacks), pesos usados. |
| **Escala de tamanhos** | h1 → h4, texto, texto pequeno — no desktop e no mobile (tabela "Tipografia por viewport"). |
| **Espaçamento** | gaps e paddings recorrentes; tente reconhecer a escala (múltiplos de 4 ou 8). |
| **Raios e sombras** | os 2–3 valores mais usados e onde aparecem (botões, cards, campos). |
| **Container e breakpoints** | largura máxima do conteúdo e media queries principais. |
| **Relação com o briefing** | destaque os valores ligados ao que o usuário quer **aproveitar** e marque os que ele quer **evitar**. |

Marque como "(provável)" o que foi deduzido em vez de medido.

## 4. Repetir por referência e fechar

Uma pasta por site. Ao final, mostre ao usuário uma tabela curta com a paleta e as fontes de cada referência e siga para o passo 3 (`extrair-design-prints`). Este passo não exige aprovação; registre `concluído` em `etapas/aprovacoes.md`.

## Limite de uso

O código extraído serve como referência de valores de estilo e estrutura. Não copie textos, imagens, logos, ícones nem blocos de código dos sites para o site final. Fontes pagas que aparecerem na extração não podem ser usadas sem licença — sinalize no resumo e sugira alternativas livres.
