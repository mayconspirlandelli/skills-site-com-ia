---
name: site-com-referencias
description: Orquestra o processo completo de criar um site com IA generativa a partir de sites de referência — briefing, coleta de referências, extração de HTML, wireframes, design system e construção. Use sempre que o usuário quiser criar, clonar o estilo, redesenhar ou "fazer um site parecido com" outros sites, mencionar sites de referência/inspiração, ou pedir para começar um projeto de site/landing page do zero, mesmo que não cite as etapas. Também use quando o usuário perguntar "em que etapa estou" ou "qual o próximo passo" num projeto de site.
---

# Site com referências — orquestrador

Esta skill coordena um fluxo de 6 etapas. Cada etapa tem sua própria skill com as instruções detalhadas. O papel daqui é descobrir em que etapa o projeto está, garantir que nenhuma seja pulada e passar os arquivos certos de uma para a outra.

## Por que esse fluxo existe

A IA gera sites melhores quando recebe **texto estruturado** (HTML, wireframes em texto, especificações, tokens) do que quando recebe imagens. Prints de tela escondem valores exatos (tamanho de fonte, espaçamento, cor), e a IA tende a chutar. Por isso o fluxo converte tudo em arquivos de texto antes de escrever código, e o `design_system.md` vira a fonte única da verdade.

## Etapas e skills

| # | Etapa | Skill | Saída principal |
|---|-------|-------|-----------------|
| 0–1 | Briefing e referências | `referencias-briefing` | `00_briefing/briefing.md`, `01_referencias/referencias.md` |
| 2 | Extrair HTML das referências | `extrair-html-referencia` | `02_html_referencias/<site>/resumo.md` |
| 3 | Prints → wireframe → especificação | `print-para-wireframe` | `03_wireframes/wireframe_<pagina>.md`, `especificacao_componentes.md` |
| 4 | Design system | `gerar-design-system` | `04_design_system/design_system.md`, `tokens.css` |
| 5–6 | Construir e validar | `construir-site` | `05_site/` |

## Estrutura de pastas do projeto

```
projeto-site/
├── 00_briefing/briefing.md
├── 01_referencias/referencias.md  (+ prints/)
├── 02_html_referencias/<site>/
├── 03_wireframes/
├── 04_design_system/design_system.md, tokens.css
└── 05_site/
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
