---
name: site-com-referencias
description: Orquestra o processo completo de criar um site com IA generativa a partir de sites de referência — briefing, coleta de referências, extração de HTML, wireframes, design system e construção. Use sempre que o usuário quiser criar, clonar o estilo, redesenhar ou "fazer um site parecido com" outros sites, mencionar sites de referência/inspiração, ou pedir para começar um projeto de site/landing page do zero, mesmo que não cite as etapas. Também use quando o usuário perguntar "em que etapa estou" ou "qual o próximo passo" num projeto de site.
---

# Site com referências — orquestrador

Esta skill coordena um fluxo de 6 etapas. Cada etapa tem sua própria skill com as instruções detalhadas. O papel daqui é descobrir em que etapa o projeto está, garantir que nenhuma seja pulada e passar os arquivos certos de uma para a outra.

## Por que esse fluxo existe

A IA gera sites melhores quando recebe **texto estruturado** (HTML, wireframes em SVG, especificações, tokens) do que quando recebe imagens. Prints de tela escondem valores exatos (tamanho de fonte, espaçamento, cor), e a IA tende a chutar. Por isso o fluxo converte tudo em arquivos de texto antes de escrever código, e o `design_system.md` vira a fonte única da verdade.

## Etapas e skills

| # | Etapa | Skill | Saída principal |
|---|-------|-------|-----------------|
| S | Setup: `grill-me`, entrevista, demais skills | `grilling` (via `grill-me`) + `auditar-skill` | `etapas/00_briefing/entrevista.md`, `prompts_imagens.md`, skills instaladas |
| 0–1 | Briefing e referências | `referencias-briefing` | `etapas/00_briefing/briefing.md`, `etapas/00_briefing/referencias.md` |
| 2 | Extrair HTML das referências | `extrair-html-referencia` | `etapas/01_extracao/codigo/<site>/resumo.md` |
| 3 | Prints → wireframe SVG → especificação | `print-para-wireframe` | `etapas/04_wireframes/wireframe_<pagina>-desktop.svg` (+ `-mobile.svg`), `especificacao_componentes.md` |
| 4 | Design system | `gerar-design-system` | `etapas/05_design_system/design_system.md`, `tokens.css` |
| 5–6 | Construir e validar | `construir-site` | `site/` |

## Etapa S — Setup (sempre a primeira)

Nenhuma outra etapa começa antes desta.

1. **Instalar `grill-me` e `grilling`.** A `grill-me` é só um atalho para a `grilling` (que tem as instruções da entrevista). Se elas ainda não estiverem disponíveis, peça ao usuário para rodar `./scripts/setup-skills.sh inicial` (audita e instala o commit auditado). Peça ao usuário para reiniciar o Claude Code se a skill não aparecer.
2. **Entrevista.** Acione a skill `grilling` (a `grill-me` não pode ser acionada pelo modelo, só pelo usuário com `/grill-me`) para fazer uma série de perguntas sobre o website ou landing page (tipo — site ou landing page —, objetivo, público, páginas e seções, conteúdo, stack, tom, restrições, animações/vídeos). Salve as respostas e o plano para codificar em `etapas/00_briefing/entrevista.md`.
3. **Prompts de imagens.** Com base **só** no plano de `etapas/00_briefing/entrevista.md`, gere `etapas/00_briefing/prompts_imagens.md` usando o modelo `assets/prompts_imagens_template.md`:
   - uma **base comum** (tipo de site, público, tom, paleta e tipografia vindos do plano);
   - **mockups** de cada página do plano, desktop e mobile, descrevendo as seções na ordem do plano — as imagens geradas vão para `etapas/03_mockup/` e entram na `print-para-wireframe` como qualquer print (nunca são referência final);
   - **imagens de conteúdo** (hero, ilustrações, ícones) com onde entram e formato.
   Não invente o que o plano não diz: o que estiver "a definir" fica genérico. Nunca peça para gerar pessoas reais (ex.: equipe, alunos, egressos) — use fotos autorizadas ou `[FOTO: ...]`. Mostre os prompts ao usuário; ele gera as imagens na ferramenta de sua preferência.
4. **Instalar as demais skills** com `./scripts/setup-skills.sh obrigatorias` (lista em `docs/skills-obrigatorias.md`). Se a entrevista indicar animações ou vídeos, também `./scripts/setup-skills.sh animacao`.
5. **Seguir o plano** `docs/plano.md`, a partir da etapa 0–1. A `referencias-briefing` deve reaproveitar `entrevista.md` e só perguntar o que faltar.

## Estrutura de pastas do projeto

```
projeto-site/
├── etapas/                    construção do site, na ordem do fluxo
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

Crie essa estrutura no início se ela não existir.

## Como conduzir

1. **Descubra o estado atual.** Verifique quais arquivos acima já existem (no projeto, nos uploads ou na conversa). A primeira etapa sem saída é a etapa atual.
2. **Leia a skill da etapa atual** e siga as instruções dela.
3. **Ao terminar uma etapa**, mostre ao usuário um resumo curto do que foi gerado e peça confirmação antes de avançar. Decisões de design tomadas cedo contaminam todo o resto, então vale a pausa.
4. **Não pule etapas.** Se o usuário pedir "já cria o site", explique em uma frase que sem design system o resultado fica genérico e ofereça fazer as etapas de forma rápida. Se ele insistir, respeite, mas registre as suposições feitas.
5. **Quando o usuário voltar para ajustar algo**, atualize o arquivo de origem (ex.: a cor muda no `design_system.md`, não só no CSS), para a fonte da verdade continuar correta.

## Regra de conteúdo das referências

Referências servem para estrutura e estilo. Textos, imagens, logos e código proprietário dos sites de referência nunca vão para o site final — use o conteúdo do briefing ou placeholders claramente marcados.
