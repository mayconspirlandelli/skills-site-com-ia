---
name: site-com-referencias
description: Orquestra o processo completo de criar um site ou landing page com IA generativa em 8 passos — entrevista e briefing, extração do design das referências (código e prints), prévia, imagem do site, wireframes, design system e construção com validação — com aprovação do usuário entre as etapas. Use sempre que o usuário quiser criar, redesenhar ou "fazer um site parecido com" outros sites, mencionar sites de referência/inspiração, ou começar um projeto de site/landing page do zero, mesmo que não cite as etapas. Também use quando o usuário perguntar "em que etapa estou" ou "qual o próximo passo" num projeto de site.
---

# Site com referências — orquestrador

Esta skill coordena um fluxo de 8 passos. Cada passo tem sua própria skill com as instruções detalhadas. O papel daqui é descobrir em que passo o projeto está, garantir que nenhum seja pulado, respeitar as aprovações do usuário e passar os arquivos certos de um passo para o outro.

## Por que esse fluxo existe

A IA gera sites melhores quando recebe **texto estruturado** (briefing, design extraído, wireframes em SVG, tokens) do que quando improvisa a partir de imagens. O fluxo primeiro entende o negócio, depois extrai o design das referências, deixa a criatividade acontecer numa imagem do site, fixa a estrutura em wireframes e o estilo no design system — e só então escreve código. As aprovações existem porque decisões tomadas cedo contaminam todo o resto: corrigir um briefing custa minutos, corrigir um site pronto custa horas.

## Passos e skills

| # | Passo | Skill | Saída principal | Aprovação |
|---|-------|-------|-----------------|-----------|
| 1 | Entrevista e briefing | `entrevista-site` | `etapas/00_briefing/briefing.md` (+ `prints/`) | ✅ obrigatória |
| 2 | Design extraído do código das referências | `extrair-html-referencia` | `etapas/01_extracao/codigo/<site>/resumo.md` | — |
| 3 | Design extraído dos prints | `extrair-design-prints` | `etapas/01_extracao/prints/resumo.md` | — |
| 4 | Prévia do site | `gerar-previa` | `etapas/02_previa/previa_site.md` | — |
| 5 | Imagem do site | `gerar-mockup` | `etapas/03_mockup/prompt_imagem.md` + imagem (PNG ou SVG) | ✅ obrigatória |
| 6 | Wireframes de todas as páginas | `gerar-wireframes` | `etapas/04_wireframes/*.svg` + `especificacao_componentes.md` | ✅ obrigatória |
| 7 | Design system | `gerar-design-system` | `etapas/05_design_system/design_system.md`, `design_system.html`, `tokens.css` | ✅ obrigatória |
| 8 | Plano, construção e validação | `construir-site` | `etapas/06_construcao/plano_construcao.md`, `site/`, `relatorio_validacao.md` | — |

Passos sem referência de um tipo são pulados com registro: sem URLs, o passo 2 não se aplica; sem prints, o passo 3 não se aplica. Anote "não se aplica" em `etapas/aprovacoes.md` e siga.

## Antes do passo 1 — setup das skills

As skills de terceiros não vêm no template. Se `frontend-design`, `playwright-cli` e as demais obrigatórias (lista em `docs/skills-obrigatorias.md`) não estiverem disponíveis, peça ao usuário para rodar `./scripts/setup-skills.sh obrigatorias` e reiniciar o Claude Code. Se a entrevista indicar animações ou vídeos, depois também `./scripts/setup-skills.sh animacao`. Nunca instale skill de terceiros sem a auditoria do script.

## Aprovações

Os passos 1, 5, 6 e 7 só terminam quando o usuário aprova explicitamente o resultado.

1. Ao concluir um desses passos, mostre o que foi gerado (abra a imagem, os SVGs ou o HTML no navegador quando possível) e pergunte se aprova ou o que quer mudar.
2. Ajuste e mostre de novo até ele aprovar. Não interprete silêncio ou "ok, e agora?" como aprovação — pergunte.
3. Aprovado, registre em `etapas/aprovacoes.md`: passo, arquivos aprovados, data e observações. Só então avance.
4. Se o usuário mudar algo de um passo já aprovado, atualize o arquivo de origem, marque a aprovação como "revisada" e confira se os passos seguintes precisam ser refeitos (ex.: mudar o briefing pode mudar a prévia e a imagem).

## Estrutura de pastas do projeto

```
projeto-site/
├── etapas/                    construção do site, na ordem do fluxo
│   ├── aprovacoes.md          registro das aprovações do usuário
│   ├── auditorias/            relatórios de auditoria das skills + exceções revisadas
│   ├── 00_briefing/           briefing.md (aprovado) + prints/ enviados pelo usuário
│   ├── 01_extracao/
│   │   ├── codigo/<site>/     design extraído do HTML/CSS/JS das referências
│   │   └── prints/            design extraído dos prints
│   ├── 02_previa/             previa_site.md
│   ├── 03_mockup/             prompt da imagem + imagem do site aprovada
│   ├── 04_wireframes/         wireframes SVG de todas as páginas (aprovados)
│   ├── 05_design_system/      design_system.md + design_system.html + tokens.css
│   └── 06_construcao/         plano_construcao.md + relatorio_validacao.md
└── site/                      só o código do site (pronto para Docker e deploy)
```

Crie as pastas que faltarem.

## Como conduzir

1. **Descubra o passo atual.** Leia `etapas/aprovacoes.md` e veja quais saídas da tabela já existem. O passo atual é o primeiro cuja saída não existe — ou, nos passos com aprovação, cuja aprovação não está registrada.
2. **Leia a skill do passo atual** e siga as instruções dela.
3. **Ao terminar um passo sem aprovação** (2, 3, 4), mostre um resumo curto do que foi gerado e siga para o próximo, a menos que o usuário queira revisar.
4. **Não pule passos.** Se o usuário pedir "já cria o site", explique em uma frase que sem briefing, wireframes e design system aprovados o resultado fica genérico, e ofereça fazer os passos de forma rápida. Se ele insistir, respeite, mas registre as suposições no `plano_construcao.md`.
5. **Ajustes de estilo voltam para a fonte.** Uma cor que muda durante a construção muda no `design_system.md` (e em `tokens.css` pelo script), não só no CSS.

## Ordem de confiança dos valores de design

Quando fontes diferentes discordam (tamanho de fonte, cor, espaçamento):

1. Decisão do usuário registrada no briefing ou numa aprovação.
2. Valor extraído do código das referências (passo 2) — é medido, não estimado.
3. Valor estimado dos prints (passo 3) — sempre marcado como "(estimado)".
4. Valor proposto pela imagem do site (passo 5) — direção criativa, não medida.

## Regra de conteúdo das referências

Referências servem para estrutura e estilo. Textos, imagens, logos e código proprietário dos sites de referência nunca vão para o site final — use o conteúdo do briefing ou placeholders claramente marcados (`[TEXTO: ...]`, `[FOTO: ...]`). Nunca gere por IA imagens de pessoas reais que o site apresenta como reais (equipe, clientes, alunos).
