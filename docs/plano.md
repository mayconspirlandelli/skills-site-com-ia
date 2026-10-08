# Plano: Criação de Site com IA Generativa e Skills

## Visão geral

Este plano organiza o processo de criação de um site usando IA generativa, partindo de sites de referência e transformando-os em artefatos estruturados (código, wireframes, especificações e design system) que a IA consegue interpretar com precisão. A ideia central é **não depender de imagens como fonte de detalhes**, e sim converter tudo em texto estruturado (HTML, Markdown, especificações), que é o formato em que a IA trabalha melhor.

### Estrutura de pastas sugerida

```
projeto-site/
├── 00_briefing/
│   ├── entrevista.md
│   └── briefing.md
├── 01_referencias/
│   ├── referencias.md
│   └── prints/
├── 02_html_referencias/
│   ├── site-a/
│   └── site-b/
├── 03_wireframes/
│   ├── wireframe_home-desktop.svg
│   └── especificacao_componentes.md
├── 04_design_system/
│   └── design_system.md
├── skills/
│   └── design-system-site/SKILL.md
└── 05_site/
```

---

## Passo S — Setup e entrevista (obrigatório, sempre o primeiro)

1. **Instale as skills `grill-me` e `grilling` antes de qualquer outra** (o script audita antes de instalar):
   ```bash
   ./scripts/setup-skills.sh inicial
   ```
2. **Faça a entrevista** (digite `/grill-me`). A `grilling` faz uma série de perguntas sobre o website ou landing page e monta o plano para codificar. Salve em `00_briefing/entrevista.md`.
3. **Instale as demais skills** (`./scripts/setup-skills.sh obrigatorias`; lista em `docs/skills-obrigatorias.md`).
4. **Siga os passos abaixo**, a partir do Passo 0 — que reaproveita as respostas da entrevista.

---

## Passo 0 — Briefing do projeto (recomendado)

Antes de buscar referências, defina o que o site precisa entregar. Sem isso, a IA mistura estilos sem critério.

**O que documentar em `briefing.md`:**

- Objetivo do site (vender, captar leads, portfólio, institucional)
- Público-alvo
- Lista de páginas (Home, Sobre, Serviços, Contato...)
- Seções de cada página
- Conteúdo real disponível (textos, logo, fotos)
- Tecnologia de saída (HTML/CSS puro, Tailwind, React, Next.js, WordPress...)
- Tom da marca (sério, divertido, minimalista, premium)

---

## Passo 1 — Coletar vários sites de referência

**Orientação ao usuário:** forneça de **3 a 5 sites de referência**, e para cada um explique **o que você gosta nele**. Referência sem justificativa leva a IA a copiar tudo, inclusive o que você não queria.

**Modelo para `referencias.md`:**

```markdown
## Referência 1 — https://exemplo-a.com
- O que usar: estrutura do hero e menu fixo
- O que NÃO usar: paleta de cores
- Páginas relevantes: home, /precos

## Referência 2 — https://exemplo-b.com
- O que usar: tipografia e espaçamento generoso
- O que NÃO usar: animações pesadas
```

**Dicas:**

- Separe referências por aspecto: uma para layout, outra para tipografia, outra para cores.
- Prefira sites do mesmo segmento ou com o mesmo objetivo do seu.
- Anote as URLs das páginas específicas, não só da home.

---

## Passo 2 — Baixar o código HTML dos sites de referência

**Objetivo:** dar à IA a estrutura real (hierarquia de seções, classes, fontes, variáveis CSS) em vez de uma interpretação visual.

**Como fazer:**

- Navegador: `Ctrl+S` → "Página web, completa", ou DevTools → aba Elements → copiar o `<html>`.
- Linha de comando: `wget --page-requisites --convert-links https://exemplo.com` ou `curl https://exemplo.com -o index.html`.
- Para sites feitos com JavaScript (React, Vue), use o HTML **renderizado** (DevTools → Elements), pois o código-fonte bruto vem quase vazio.

**Limpeza antes de enviar para a IA (importante):**

- Remova `<script>`, trackers, SVGs gigantes e CSS minificado irrelevante — isso economiza contexto e reduz ruído.
- Extraia separadamente o que importa: variáveis CSS (`:root { --color-... }`), `@font-face`, links do Google Fonts, breakpoints (`@media`).
- Peça para a IA gerar um resumo estruturado: "Liste as seções desta página na ordem, com a hierarquia de títulos, fontes usadas, cores encontradas e breakpoints".

> ⚠️ Use o código como **referência de estrutura e estilo**, não para copiar textos, imagens, logos ou código proprietário.

---

## Passo 3 — Converter prints de tela em wireframes (não usar prints como referência direta)

**Motivo:** a IA interpreta mal detalhes finos em imagens (tamanhos exatos de fonte, espaçamentos, cores precisas, alinhamentos). Por isso, o print serve **apenas como entrada** para a IA gerar um wireframe em texto — e é o wireframe que vira a referência oficial.

### 3.1 — Gerar o wireframe

**Prompt sugerido:**

```
Analise este print de tela e crie um wireframe em Markdown/ASCII,
seção por seção, de cima para baixo. Para cada seção indique:
nome da seção, layout (colunas/grid), elementos presentes
(título, subtítulo, botão, imagem, card, ícone) e alinhamento.
Não descreva cores nem estilos ainda, apenas estrutura.
```

**Exemplo de saída esperada:**

```
[HEADER] fixo, altura ~80px
| Logo (esq) | Menu 5 itens (centro) | Botão CTA (dir) |

[HERO] 2 colunas 50/50
| H1 + parágrafo + 2 botões | Imagem ilustrativa |

[FEATURES] grid 3 colunas
| Card: ícone + H3 + texto | x3 |
```

### 3.2 — Detalhar tipografia e posicionamento dos componentes

Com o wireframe pronto, peça a especificação detalhada em `especificacao_componentes.md`:

```
Com base no wireframe e no HTML da referência, descreva para cada
componente: tipografia (fonte, tamanho, peso, altura de linha),
posição e alinhamento, espaçamentos internos e externos,
comportamento responsivo (desktop, tablet, mobile) e estados
(hover, ativo, foco).
```

**Dica:** cruze o wireframe com o HTML do Passo 2 — os valores numéricos (tamanhos, fontes) devem vir preferencialmente do código, não da imagem.

---

## Passo 4 — Criar o arquivo `design_system.md`

Este arquivo é a **fonte única da verdade** visual do site. Toda geração de código deve obedecer a ele.

**Conteúdo mínimo:**

```markdown
# Design System

## Paleta de cores
| Token            | Hex     | Uso                     |
|------------------|---------|-------------------------|
| --color-primary  | #1A56DB | Botões, links           |
| --color-text     | #111827 | Texto principal         |
| --color-bg       | #FFFFFF | Fundo                   |

## Tipografia
- Títulos: Inter, 700
- Texto: Inter, 400
- Escala: H1 48px / H2 36px / H3 24px / Body 16px / Small 14px
- Altura de linha: títulos 1.2 / texto 1.6

## Espaçamento
Escala de 4px: 4, 8, 12, 16, 24, 32, 48, 64, 96

## Grid e breakpoints
- Container máx.: 1200px
- Mobile < 640px / Tablet 640–1024px / Desktop > 1024px

## Bordas e sombras
- Raio: 4px (inputs), 8px (cards), 999px (pílulas)
- Sombra card: 0 4px 12px rgba(0,0,0,.08)

## Componentes
- Botão primário, secundário, link
- Card, input, header, footer
(com estados hover/foco/desabilitado)

## Regras de uso
- Nunca usar cores fora da paleta
- Contraste mínimo WCAG AA
```

**Dica:** peça à IA para gerar também um arquivo `tokens.css` com essas variáveis, para que o código use os tokens em vez de valores soltos.

---

## Passo 4.1 — Transformar o design system em uma Skill

Crie uma Skill (pasta com `SKILL.md`) que instrua a IA a **sempre** ler o `design_system.md` e a especificação de componentes antes de gerar qualquer código. Assim o padrão se mantém em todas as sessões e páginas.

```markdown
---
name: design-system-site
description: Use sempre que for criar ou editar páginas/componentes do site.
---
1. Leia design_system.md e especificacao_componentes.md antes de escrever código.
2. Use apenas os tokens de tokens.css.
3. Siga o wireframe da página correspondente.
4. Gere HTML semântico, responsivo e acessível.
```

---

## Passo 5 — Gerar o site a partir das referências

Envie para a IA, juntos: `briefing.md`, `referencias.md`, os wireframes, `especificacao_componentes.md`, `design_system.md` e o resumo do HTML das referências.

**Estratégia de geração (recomendada):**

1. Gere primeiro a base: `tokens.css`, estilos globais, header e footer.
2. Gere **seção por seção**, não a página inteira de uma vez — o resultado é muito mais fiel.
3. Depois de cada seção, compare com o wireframe e peça ajustes.
4. Monte as demais páginas reutilizando os componentes.

**Prompt sugerido:**

```
Usando a skill design-system-site, crie a seção HERO da Home
conforme wireframe_home-desktop.svg. Use conteúdo real do briefing.
Stack: HTML + Tailwind. Mobile-first.
```

---

## Passo 6 — Revisão e validação

- Comparar cada seção com o wireframe e o design system.
- Testar responsividade (mobile, tablet, desktop).
- Rodar Lighthouse (performance, acessibilidade, SEO).
- Verificar contraste de cores e navegação por teclado.
- Substituir qualquer texto ou imagem das referências por conteúdo próprio.
- Registrar ajustes aprovados de volta no `design_system.md` para manter a fonte da verdade atualizada.
