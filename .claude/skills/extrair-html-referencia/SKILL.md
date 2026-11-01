---
name: extrair-html-referencia
description: Baixa, limpa e resume o código HTML/CSS de sites de referência, extraindo estrutura de seções, fontes, cores, variáveis CSS, breakpoints, bordas e sombras em um resumo.md. Use sempre que o usuário enviar um arquivo HTML de um site, pedir para "pegar o código", "baixar o HTML", "analisar o CSS" ou "extrair o estilo" de um site de referência, ou quando um projeto de site precisar de valores exatos de design vindos de sites existentes.
---

# Extrair HTML de referência

Objetivo: transformar cada site de referência em um `resumo.md` enxuto que a IA consegue ler inteiro, com valores exatos (fontes, tamanhos, cores, breakpoints) em vez de impressões visuais.

HTML bruto de sites modernos é enorme e cheio de ruído (scripts, trackers, SVGs, CSS minificado). Colocar isso inteiro no contexto gasta espaço e piora a análise. O script faz a limpeza de forma determinística; a IA entra depois para interpretar.

## 1. Obter o HTML

Tente nesta ordem:

1. **Arquivo enviado pelo usuário** (em uploads ou no projeto). É o caminho mais confiável.
2. **`--url`** no script, se houver acesso à rede para o domínio. Em ambientes com rede restrita isso falha; nesse caso, peça o arquivo ao usuário.

Instruções para passar ao usuário quando for preciso salvar a página:
- **Site comum:** no navegador, `Ctrl+S` → "Página da Web, completa". Enviar o `.html` e a pasta `_arquivos` (ou pelo menos os `.css`).
- **Site em React/Vue/Next (o HTML vem quase vazio):** abrir DevTools (F12) → aba Elements → clicar com o botão direito na tag `<html>` → Copy → Copy outerHTML → colar num arquivo `.html`. Para o CSS: aba Network → filtrar por CSS → recarregar → salvar os arquivos.
- Linha de comando: `wget --page-requisites --convert-links <url>`.

## 2. Rodar o script

```bash
pip install beautifulsoup4 --break-system-packages  # se necessário
python scripts/extrair_referencia.py --html pagina.html --css estilo.css --saida etapas/01_extracao/codigo/<nome-site>
# ou
python scripts/extrair_referencia.py --url https://exemplo.com --saida etapas/01_extracao/codigo/<nome-site>
```

Use `--base-url` junto com `--html` quando o CSS estiver linkado com caminho relativo e houver rede.

Saídas: `limpo.html`, `estilos.css`, `resumo.md`, `dados.json`.

**Leia os avisos do script.** Se ele disser que a página parece renderizada por JavaScript ou que não achou CSS, não continue com dados vazios — peça ao usuário o HTML renderizado ou os arquivos CSS, explicando como obter.

## 3. Interpretar o resumo

O resumo traz dados brutos. Complete o `resumo.md` com uma seção **"Interpretação"** no final, respondendo:

- **Ordem das seções da página** em linguagem simples (ex.: header fixo → hero 2 colunas → logos de clientes → 3 cards de recursos → depoimentos → CTA → footer).
- **Fonte de títulos e fonte de texto.** Separe fontes da marca de fontes de fallback/ícones.
- **Paleta provável:** identifique primária, secundária, texto, fundo, bordas e estados. Cores muito frequentes costumam ser texto e fundo; a cor dos botões costuma ser a primária. Descarte cores de bibliotecas de terceiros (widgets, ícones).
- **Escala tipográfica** (tamanhos de H1 a texto pequeno).
- **Breakpoints principais.**
- **Relação com o `referencias.md`:** destaque os valores ligados ao que o usuário disse querer aproveitar, e sinalize os que ele disse querer evitar.

Seja honesto sobre incerteza: se um valor foi deduzido, marque como "(provável)".

## 4. Repetir por referência

Uma pasta por site. Ao final, confirme com o usuário se todas as referências foram processadas e siga para `print-para-wireframe`.

## Limite de uso

O código extraído serve como referência de estrutura e valores de estilo. Não copie textos, imagens, logos ou blocos de código dos sites para o site final.
