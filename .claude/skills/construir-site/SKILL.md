---
name: construir-site
description: Planeja, constrói e valida o site — escreve o plano de construção a partir do briefing, wireframes e design system aprovados, gera o código em site/ seção por seção (só com tokens), prepara Docker e deploy conforme a hospedagem do briefing e, ao final, valida tudo contra o plano num relatório. Use no passo 8 do fluxo, depois do design system aprovado, ou quando o usuário pedir "agora cria o site", "monta a página", "cria o hero/header/footer", deploy, Dockerfile, ou revisar/validar o site gerado.
---

# Plano, construção e validação (passo 8)

Objetivo: transformar o que foi aprovado (briefing, wireframes, design system) num site funcionando em `site/`, pronto para a hospedagem escolhida — e provar, num relatório, que ele cumpre o plano.

## Antes de começar

Confirme em `etapas/aprovacoes.md` que os passos 1, 6 e 7 estão aprovados. Se o design system não estiver, pare e avise: sem ele o site fica genérico e inconsistente. Leia, nesta ordem:

1. `etapas/05_design_system/design_system.md` e `tokens.css`
2. `etapas/04_wireframes/wireframe_<pagina>-desktop.svg` e `-mobile.svg` (os atributos `data-*` de cada `<g class="secao">`) e `especificacao_componentes.md`
3. `etapas/00_briefing/briefing.md` — stack, hospedagem, Docker, conteúdo, funcionalidades
4. `etapas/02_previa/previa_site.md` e `etapas/03_mockup/prompt_imagem.md` (imagens de conteúdo)

## Fase 1 — Plano de construção

Escreva `etapas/06_construcao/plano_construcao.md` a partir de `assets/plano_construcao_template.md`:

- **Stack e estrutura de pastas** de `site/` (veja `references/stacks.md`).
- **Páginas e seções**: uma linha por seção de cada wireframe aprovado, com os componentes que ela usa. Essa lista vira o checklist da validação.
- **Componentes reutilizáveis** (header, footer, botão, card...) e onde aparecem.
- **Tokens**: como o design system entra no código (`tokens.css` importado; Tailwind estendido com `tailwind.tokens.js`).
- **Conteúdo**: textos do briefing por seção e a lista de placeholders `[TEXTO: ...]` / `[FOTO: ...]` que o usuário vai preencher.
- **Funcionalidades**: formulário, WhatsApp, analytics, PWA... e como cada uma será feita.
- **Entrega**: hospedagem, Docker (sim/não), deploy automático — os arquivos que serão criados (veja `references/deploy.md`).
- **Critérios de aceite**: o que a validação vai checar (seções, responsividade, acessibilidade, Lighthouse, build/Docker).
- **Suposições** feitas por falta de informação.

Mostre o plano ao usuário e confirme antes de escrever código. Mudanças de escopo depois disso entram no plano primeiro.

## Fase 2 — Construção em `site/`

### Regras de código
- **Só tokens.** Cores, fontes, tamanhos, espaços, raios e sombras vêm de `tokens.css` (ou das classes Tailwind geradas a partir dele). Nada de hex ou px soltos. Valor novo → proponha acrescentar ao design system primeiro.
- **Os tokens no site são gerados, não copiados à mão:** gere `tokens.css` (e `tailwind.tokens.js`) direto no caminho do site com `gerar_tokens.py --saida site/<caminho>/tokens.css`, e regenere sempre que o design system mudar.
- **HTML semântico:** `header`, `nav`, `main`, `section` com `aria-labelledby`, `footer`; um único `h1` por página; títulos sem pular níveis.
- **Mobile-first**, seguindo o `data-mobile` dos wireframes e a especificação.
- **Acessibilidade:** foco visível, `alt` em imagens, labels em campos, área de toque ≥ 44px, `prefers-reduced-motion`.
- **Conteúdo:** textos do briefing; onde faltar, placeholder marcado. Nunca textos, imagens ou logos das referências.
- `site/` contém só o que vai para produção: nada de arquivos das etapas lá dentro.

### Ordem
Gerar tudo de uma vez produz resultado genérico. Construa em partes, conferindo cada uma:

1. **Base:** estrutura de pastas, tokens, estilos globais (reset, tipografia base, container).
2. **Header e footer.**
3. **Uma seção por vez**, na ordem do wireframe. Ao terminar cada seção: confira com o wireframe (elementos, quantidades, alinhamento) e com a especificação (tipografia, espaçamento, estados, celular); marque no plano; mostre ao usuário. Se ele preferir velocidade, agrupe 2–3 seções por rodada, mantendo a conferência.
4. **Demais páginas**, reutilizando os componentes.
5. **Funcionalidades** (formulário, integrações, PWA).

Ajuste de estilo pedido pelo usuário (cor, fonte, espaçamento) muda o `design_system.md` e os tokens são regenerados — não só o CSS.

## Fase 3 — Entrega

Conforme o briefing, crie os arquivos de entrega descritos em `references/deploy.md`: `Dockerfile` + `nginx.conf` (se Docker), workflow do GitHub Pages, `netlify.toml`, `vercel.json`, `.dockerignore`. Teste o que puder testar localmente (`npm run build`; `docker build` se o Docker estiver instalado). Nunca faça deploy, push ou publicação sem o usuário pedir.

## Fase 4 — Validação contra o plano

Valide e escreva `etapas/06_construcao/relatorio_validacao.md` a partir de `assets/relatorio_validacao_template.md`:

1. **Plano item a item:** cada seção de cada página — existe, na ordem, com as quantidades do wireframe? Cada funcionalidade e arquivo de entrega do plano foi feito?
2. **Checklist** de `references/checklist_validacao.md` (design system, responsividade, acessibilidade, performance/SEO, conteúdo e direitos).
3. **No navegador** (com `playwright-cli`): abra cada página em 375, 768 e 1280px, tire screenshots para `etapas/06_construcao/screenshots/`, confira rolagem horizontal, menu do celular, foco por teclado e erros no console.
4. **Build e Docker:** o build passa? A imagem Docker sobe e serve o site?
5. **Lighthouse:** rode se houver ferramenta; senão, explique ao usuário como rodar (DevTools → Lighthouse → Analyze).

O relatório diz, para cada item: ✅ passou, ❌ falhou (e o que foi corrigido ou o que falta) ou ⚠️ não verificado (e por quê). Seja honesto: item não testado não é item aprovado. Corrija as falhas que puder, revalide, e entregue ao usuário o resumo e a lista de pendências (placeholders a preencher, itens não verificados). Registre `concluído` em `etapas/aprovacoes.md`.
