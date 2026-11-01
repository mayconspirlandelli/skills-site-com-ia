---
name: gerar-mockup
description: Gera a imagem do site a partir da prévia — escreve o prompt e desenha um mockup colorido em SVG — e itera com o usuário até a aprovação. Use no passo 5 do fluxo, depois da prévia, ou quando o usuário pedir "a imagem do site", "um mockup", "como o site vai ficar" ou um prompt para gerar a imagem do site.
---

# Imagem do site (passo 5)

Objetivo: ver o site antes de construí-lo. Este é o passo **criativo** do fluxo: a prévia diz o que o site tem; a imagem propõe como ele fica. Sai daqui uma imagem **aprovada pelo usuário**, que guia os wireframes (passo 6) e o design system (passo 7).

Entrada: `etapas/02_previa/previa_site.md` (e o briefing para conferir).
Saída: `etapas/03_mockup/` com `prompt_imagem.md` e as imagens.

## 1. Escrever o prompt

Gere `etapas/03_mockup/prompt_imagem.md` a partir de `assets/prompt_imagem_template.md`:

- **Base comum:** tipo de site, domínio, público, objetivo, clima, paleta (hex), tipografia, formas — tudo da prévia.
- **Um prompt por tela:** Home desktop e Home celular são o mínimo. Outras páginas só se forem muito diferentes da Home (ex.: página de preços).
- **Seções na ordem da prévia**, cada uma com a organização sugerida e o conteúdo real curto (título, texto do botão).
- **Imagens de conteúdo** (hero, ilustrações, ícones) numa tabela à parte — servem ao passo 8.

Não invente o que a prévia não diz. Nunca peça pessoas reais que o site apresenta como reais.

## 2. Desenhar o mockup em SVG

O Claude desenha o mockup em SVG a partir do prompt — fiel à prévia e fácil de ajustar. Antes de desenhar, carregue as skills `frontend-design` e `design-taste-frontend` para fugir do visual genérico.

- `mockup_home-desktop_v1.svg` com `viewBox="0 0 1440 <altura>"`; `mockup_home-mobile_v1.svg` com largura 390.
- **Colorido e com tipografia de verdade** (não é wireframe): paleta e fontes da prévia (`font-family` com fallback), títulos e botões com o texto real curto, demais textos como linhas ou frases neutras.
- Imagens como blocos com gradiente suave da paleta e um rótulo discreto (`[FOTO: equipe]`). Ícones simples desenhados em SVG.
- Nada de `<image>` externo, scripts ou recortes de referências.

O `prompt_imagem.md` também serve para o usuário gerar a imagem numa ferramenta de IA de imagem, se quiser. Se ele trouxer uma imagem gerada fora, salve em `etapas/03_mockup/` e trate como mais uma versão para aprovação.

## 3. Aprovação

1. Mostre as imagens: abra no navegador do app quando possível, ou diga o caminho dos arquivos.
2. Pergunte se aprova ou o que quer mudar. Registre cada pedido na tabela "Ajustes pedidos" do `prompt_imagem.md` e gere uma nova versão (`_v2`, `_v3`) — não sobrescreva as anteriores.
3. Quando um pedido mudar uma decisão da prévia (ex.: outra cor principal), atualize também a `previa_site.md`.
4. Aprovado: copie a versão escolhida para `mockup_home-desktop.png|svg` (e `-mobile`) e registre em `etapas/aprovacoes.md` (passo 5, arquivos, `aprovado`, data, versão escolhida).

A imagem aprovada é **direção visual**, não especificação: na ordem de confiança, valores medidos e decisões do usuário valem mais que cores e medidas "lidas" da imagem. A estrutura oficial nasce nos wireframes.

Próximo passo: `print-para-wireframe` (passo 6).
