---
name: gerar-previa
description: Compila o briefing aprovado e o design extraído das referências (código e prints) numa prévia do site em Markdown — páginas e seções na ordem, conteúdo de cada uma, direção visual (paleta e tipografia candidatas), o que vem de cada referência e decisões técnicas — que serve de base para o prompt da imagem e para os wireframes. Use no passo 4 do fluxo, depois das extrações, ou quando o usuário pedir uma "prévia", "visão geral" ou "resumo do site" antes de desenhar.
---

# Prévia do site (passo 4)

Objetivo: juntar tudo o que se sabe até aqui num único documento que descreve o site **antes** de desenhá-lo — `etapas/02_previa/previa_site.md`. A imagem do site (passo 5) e os wireframes (passo 6) leem este arquivo; ele é a ponte entre "o que o usuário quer" e "como vai ficar".

## Entradas

- `etapas/00_briefing/briefing.md` (aprovado) — a fonte principal.
- `etapas/01_extracao/codigo/<site>/resumo.md` — design medido no código (passo 2), se houver.
- `etapas/01_extracao/prints/resumo.md` — design estimado dos prints (passo 3), se houver.

## Como compilar

1. **Estrutura vem do briefing.** As páginas e seções da prévia são as do briefing, na mesma ordem. Use as referências só para sugerir *como* cada seção se organiza (ex.: "hero em 2 colunas, como na Ref 1"), nunca para acrescentar seções que o usuário não pediu.
2. **Conteúdo real ou placeholder.** Para cada seção, diga o que ela comunica e qual conteúdo do briefing entra. O que não existe vira `[TEXTO: ...]`, `[FOTO: ...]`, `[DEPOIMENTO: ...]`. Nunca use textos das referências.
3. **Direção visual por consenso.** Monte a paleta e a tipografia candidatas cruzando as fontes, na ordem de confiança do projeto: decisão do usuário (cores da marca, gostos do briefing) > valor medido no código > valor estimado dos prints. Para cada cor e fonte, diga de onde veio. Descarte o que o usuário disse querer **evitar**.
4. **Conflitos à vista.** Se as referências puxam para lados opostos (uma escura e densa, outra clara e arejada), não escolha em silêncio: liste o conflito e proponha uma decisão.
5. **Decisões técnicas no fim.** Stack, hospedagem, Docker, responsivo/PWA, funcionalidades — copiadas do briefing, para o passo 8 ter tudo num lugar.

Use `assets/previa_template.md`.

## Fechar

Mostre ao usuário o mapa de páginas e a direção visual (paleta + tipografia em uma tabela curta) e os conflitos encontrados, se houver. Este passo não exige aprovação formal, mas resolva os conflitos com o usuário antes de seguir — a imagem do site vai materializar essas escolhas. Registre `concluído` em `etapas/aprovacoes.md`.

Próximo passo: `gerar-mockup` (passo 5).
