---
name: entrevista-site
description: Conduz a entrevista de um novo site ou landing page em rodadas de perguntas, cada uma com resposta recomendada — negócio, objetivo, público, páginas, arquitetura (HTML/CSS, Tailwind, Vite, frameworks), hospedagem, Docker, design (cores, tipografia, celular) e sites/prints de referência — e gera o briefing.md para aprovação do usuário. Use no passo 1 do fluxo, sempre que o usuário começar um projeto de site/landing page, quiser "fazer um site", listar sites de inspiração, ou quando etapas/00_briefing/briefing.md ainda não existir ou não estiver aprovado.
---

# Entrevista e briefing (passo 1)

Objetivo: sair deste passo com `etapas/00_briefing/briefing.md` **aprovado pelo usuário**, respondendo o que vamos construir, para quem, com que tecnologia, onde vai rodar, com que cara e inspirado em quê. Todo o resto do fluxo lê este arquivo; uma lacuna aqui vira um chute lá na frente.

## Método: rodadas com resposta recomendada

Entreviste até chegar a um entendimento comum, sem deixar nada assumido em silêncio.

- **Pense em árvore de decisões.** Algumas respostas dependem de outras (a hospedagem depende da arquitetura; a arquitetura depende do tipo de site). A cada rodada, pergunte só o que já pode ser respondido sem adivinhar respostas que você ainda não ouviu.
- **Rodadas curtas.** De 3 a 6 perguntas por rodada, numeradas. Espere as respostas antes da próxima rodada.
- **Sempre com recomendação.** Cada pergunta traz sua resposta recomendada, com o motivo em meia frase. Formule a pergunta de modo que "sim" aceite a recomendação — isso deixa o usuário responder rápido o que ele não tem opinião forte.
- **Fatos você mesmo busca.** Se o usuário já deu a informação (nesta conversa, num arquivo, num site dele), não pergunte de novo. Se ele citar um site existente da empresa, abra e leia antes de perguntar sobre marca e conteúdo.
- **Decisões são do usuário.** Coloque cada decisão para ele e espere. "Não sei" vira `a definir` — exceto nos itens obrigatórios (abaixo), em que você explica o impacto e propõe uma escolha.

Formato de cada rodada:

```
**Rodada N — <tema>**

❓ **P1 — <título curto>**: <pergunta, com opções quando ajudar>
➡️ Recomendo: <resposta> — <motivo curto>

❓ **P2 — ...**
➡️ Recomendo: ...
```

## Roteiro

Cubra todos os blocos. A ordem abaixo respeita as dependências; junte blocos numa mesma rodada quando as perguntas já estiverem liberadas.

### A. Negócio e tipo de site
- Domínio de negócio: o que a empresa/projeto faz, o que oferece, o diferencial.
- Tipo: landing page (uma página, um objetivo), site institucional (várias páginas), portfólio, blog, catálogo.
- Já existe site ou marca (logo, manual de marca)? Se existir, peça o link e leia.
- Concorrentes ou projetos parecidos que o usuário conhece.

### B. Objetivo
- Ação principal que o visitante deve fazer (comprar, agendar, preencher formulário, chamar no WhatsApp, baixar, se inscrever).
- Objetivos secundários e como medir (formulário enviado, cliques no CTA, analytics).

### C. Público
- Quem visita: perfil, o que procura, o que o convence.
- Contexto de uso: maioria no celular ou no computador? Idioma(s)?
- Necessidades de acessibilidade (público idoso, baixa visão, leitores de tela).

### D. Páginas, conteúdo e funcionalidades
- Páginas e, em cada uma, as seções previstas (para landing page: as seções da página única).
- Conteúdo disponível: textos, logo, fotos, depoimentos, números. O que falta vira placeholder.
- Funcionalidades: formulário de contato, WhatsApp, newsletter, mapa, blog, área restrita, multilíngue, analytics.
- Animações ou vídeos? (Se sim, o passo de setup instala as skills de animação.)

### E. Arquitetura
- Stack: HTML + CSS puro · HTML + Tailwind · Vite (com ou sem React/Vue/Svelte) · Astro · Next.js · outro.
- Precisa de CMS ou de o próprio cliente editar conteúdo?
- SEO importa (site público que precisa ser encontrado no Google)?
- Recomendação padrão: landing page ou site estático simples → **HTML + Tailwind** (ou **Vite + Tailwind** se quiser build e componentes); muitas páginas com conteúdo → **Astro**; interatividade pesada ou app → **Vite + React** ou **Next.js**.

### F. Hospedagem e entrega
- Onde vai rodar: GitHub Pages · Netlify · Vercel · Cloudflare Pages · VPS/servidor próprio · servidor da instituição.
- Vai rodar em **Docker**? (Comum em VPS ou servidor próprio: site estático servido por Nginx num container.)
- Domínio próprio? Deploy automático a cada push (CI/CD)?

### G. Design
- Cores de que gosta e de que não gosta; cores obrigatórias da marca (peça os hex, se houver).
- Tipografia: serifada, sem serifa, geométrica, manuscrita? Alguma fonte específica?
- Tom visual: minimalista, sóbrio, acolhedor, premium, técnico, divertido, acadêmico...
- Modo escuro?
- Celular: só **layout responsivo** (padrão, mobile-first) ou também **app instalável (PWA)**?

### H. Referências
- **3 a 5 sites de referência** (URLs, de preferência das páginas específicas, não só da home). Para cada um: **o que aproveitar**, **o que evitar** e o aspecto principal (layout, tipografia, cores, espaçamento, conteúdo). URL sem justificativa faz a IA copiar tudo, inclusive o que o usuário não gosta — se ele não souber explicar, ofereça opções concretas.
- **Prints de telas** de sites de que ele gosta. Os passos seguintes precisam dos **arquivos**: peça para salvar em `etapas/00_briefing/prints/` com nomes descritivos (`ref1_hero.png`, `ref2_rodape.png`). Se ele colar imagens no chat, descreva o que vê, use na conversa e peça que salve os arquivos na pasta.

### Itens obrigatórios (não podem ficar "a definir")
Tipo de site, objetivo principal, público, lista de páginas/seções, stack e hospedagem. Se o usuário não souber, explique o impacto em uma frase e proponha uma escolha para ele aceitar.

## Saída

Gere `etapas/00_briefing/briefing.md` a partir de `assets/briefing_template.md`. Regras:

- Registre as respostas do usuário, não a sua recomendação, quando ele escolheu outra coisa.
- Marque com `(recomendação aceita)` o que veio de uma recomendação aceita com "sim" — ajuda a revisar depois.
- Liste os prints recebidos com o caminho do arquivo.
- Pendências vão para a seção **A definir**, cada uma com o passo em que precisa estar resolvida.

## Validação antes de pedir aprovação

- Todos os blocos A–H foram cobertos e os itens obrigatórios estão definidos.
- Toda referência tem "aproveitar" e "evitar".
- Nenhuma contradição óbvia (ex.: "minimalista" + referência escolhida pelas animações pesadas; "GitHub Pages" + "Next.js com servidor"; "Docker" + hospedagem que não usa container). Se houver, aponte e resolva com o usuário.
- Cada página tem pelo menos uma referência de layout associada (ou a decisão de não ter).

## Aprovação

Mostre um resumo do briefing (uma linha por bloco) e o caminho do arquivo, e pergunte se aprova ou o que quer mudar. Ajuste até ele aprovar explicitamente. Aprovado, registre em `etapas/aprovacoes.md` (passo 1, `00_briefing/briefing.md`, `aprovado`, data). Se não houver URLs, registre o passo 2 como `não se aplica`; se não houver prints, o passo 3.

Se a entrevista indicou animações ou vídeos, lembre o usuário de rodar `./scripts/setup-skills.sh animacao`.

Próximo passo: `extrair-html-referencia` (passo 2).
