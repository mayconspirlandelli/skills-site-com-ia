# Template: sites com IA generativa + Skills

🇧🇷 Português · 🇺🇸 [English](README.en.md)

Template para criar **websites, sites institucionais e landing pages** com o Claude Code em
**8 passos**, do entendimento do negócio ao site validado e pronto para deploy. Cada passo gera um
arquivo de texto estruturado que o próximo lê (briefing, design extraído das referências, prévia,
wireframes SVG, design system) — e quatro deles só avançam com a sua aprovação.

Plano completo: [`docs/plano.md`](docs/plano.md) · Diagrama do processo: [`docs/diagrama-processo.html`](docs/diagrama-processo.html)

## Os 8 passos

![Diagrama dos 8 passos](docs/diagrama-processo.png)

| # | Passo | Aprovação |
|---|-------|-----------|
| 1 | **Entrevista e briefing** — negócio, objetivo, público, arquitetura, hospedagem, Docker, design, referências e prints | ✅ |
| 2 | **Design extraído do código** das referências (HTML, CSS e o resultado do JavaScript) | |
| 3 | **Design extraído dos prints** de telas | |
| 4 | **Prévia do site** em Markdown | |
| 5 | **Imagem do site** — prompt + mockup em SVG | ✅ |
| 6 | **Wireframes SVG** de todas as páginas, desktop e celular | ✅ |
| 7 | **Design system** em Markdown e HTML, com tokens | ✅ |
| 8 | **Plano, construção e validação** — código em `site/`, Docker/deploy e relatório | |

## Como usar

### 1. Crie seu projeto a partir do template

No GitHub, abra este repositório e clique em **Use this template → Create a new repository**.
Ou pela linha de comando, com o [GitHub CLI](https://cli.github.com/):

```bash
gh repo create meu-site --template mayconspirlandelli/skills-site-com-ia --private --clone
```

Se criou pelo site, clone o novo repositório:

```bash
git clone https://github.com/<usuario>/<meu-site>.git
```

### 2. Instale as skills de terceiros

Na pasta do projeto (no Windows, use o Git Bash). O script audita cada skill antes de instalar:

```bash
./scripts/setup-skills.sh obrigatorias
```

### 3. Abra o Claude Code e comece

```bash
claude
```

Diga algo como: *"Quero criar uma landing page para [seu negócio]."* A skill `site-com-referencias`
conduz os 8 passos, começando pela entrevista. O andamento fica nas pastas de `etapas/` e em
`etapas/aprovacoes.md` — você pode parar e continuar em outra sessão.

### Requisitos

- [Claude Code](https://claude.com/claude-code)
- Git e Bash (no Windows, Git Bash)
- Python 3 e `pip install beautifulsoup4 pillow`
- Node.js (para o site e para o `playwright-cli`)

## O que vem no template

```
├── CLAUDE.md              instruções permanentes lidas em toda sessão
├── .claude/
│   ├── settings.json      marketplaces e plugins do projeto
│   └── skills/            skills do fluxo (versionadas com o projeto)
├── docs/
│   ├── plano.md           o plano dos 8 passos
│   ├── diagrama-processo.html  diagrama dos 8 passos (+ .png)
│   ├── skills-obrigatorias.md  skills de terceiros e como instalar
│   └── recursos.md        links úteis (referências, animações, skills)
├── scripts/
│   ├── setup-skills.sh    audita e instala as skills de terceiros do template
│   └── adicionar-skill.sh audita e instala qualquer outra skill
├── etapas/                construção do site, uma pasta por passo
│   ├── aprovacoes.md      registro das suas aprovações
│   ├── auditorias/        relatórios de auditoria das skills e exceções revisadas
│   ├── 00_briefing/       briefing.md + prints/ enviados
│   ├── 01_extracao/       design extraído do código (codigo/) e dos prints (prints/)
│   ├── 02_previa/         prévia do site
│   ├── 03_mockup/         prompt e imagem do site
│   ├── 04_wireframes/     wireframes SVG
│   ├── 05_design_system/  design_system.md + design_system.html + tokens.css
│   └── 06_construcao/     plano de construção e relatório de validação
└── site/                  código do site (pronto para Docker e deploy)
```

## Skills incluídas

| Skill | Passo |
|-------|-------|
| `site-com-referencias` | Orquestra o fluxo, as aprovações e indica o próximo passo |
| `entrevista-site` | 1 — entrevista em rodadas com resposta recomendada e briefing.md |
| `extrair-html-referencia` | 2 — mede o design das referências no navegador (playwright-cli) e no código |
| `extrair-design-prints` | 3 — paleta dos prints (script) e análise de tipografia e formas |
| `gerar-previa` | 4 — prévia do site em Markdown |
| `gerar-mockup` | 5 — prompt e mockup do site em SVG |
| `gerar-wireframes` | 6 — wireframes SVG de todas as páginas + página de revisão |
| `gerar-design-system` | 7 — design_system.md + design_system.html, tokens e contraste |
| `construir-site` | 8 — plano, código em site/, Docker/deploy e relatório de validação |
| `auditar-skill` | Auditoria de segurança de skills de terceiros antes de instalar |

## Skills de terceiros (instaladas pelo script)

Não vêm versionadas no template — cada uma tem licença e autor próprios. O
`scripts/setup-skills.sh` audita e instala cada uma no seu projeto. Detalhes e comandos
`npx` manuais em [`docs/skills-obrigatorias.md`](docs/skills-obrigatorias.md).

| Grupo | Skills | Comando |
|-------|--------|---------|
| Obrigatórias | `frontend-design`, `web-design-guidelines`, `image-to-code`, `design-taste-frontend`, `playwright-cli`, `diagram-design`, `impeccable` | `./scripts/setup-skills.sh obrigatorias` |
| Animação/vídeo (se o briefing pedir) | `remotion-best-practices`, `motion-design` | `./scripts/setup-skills.sh animacao` |
| Extras (opcional) | `grill-me`, `grilling` | `./scripts/setup-skills.sh extras` |

## Adicionando outras skills

> 🔒 **Toda skill de terceiros passa pela auditoria antes de ser instalada.**
> Skills dão instruções à IA e podem trazer scripts que rodam no seu computador,
> com acesso a arquivos, rede e credenciais. A skill `auditar-skill` verifica prompt
> injection, envio de dados, acesso a credenciais, código ofuscado, persistência e
> comandos destrutivos, e dá um veredito: ✅ OK, ⚠️ REVISAR ou ⛔ BLOQUEAR.
> Os relatórios ficam em `etapas/auditorias/`.

**Opção 1 — Script com auditoria automática (recomendado).**
```bash
./scripts/adicionar-skill.sh https://github.com/<usuario>/<repo> <nome-ou-caminho-da-skill>
./scripts/adicionar-skill.sh <url> <skill> --global   # para todos os projetos
```
Baixa em pasta temporária, audita e só instala o commit auditado (REVISAR pede sua
confirmação, BLOQUEAR impede a instalação).

**Opção 2 — Marketplace de plugins.**
Antes de instalar um plugin, peça ao Claude Code: *"audite o plugin X do marketplace Y"* —
a skill `auditar-skill` clona o repositório e audita cada skill, comando e hook do plugin.
O marketplace oficial da Anthropic já está registrado no `.claude/settings.json`.
Dentro do Claude Code:
```
/plugin install example-skills@anthropic-agent-skills --scope project
```
O `--scope project` grava o plugin no `.claude/settings.json`, então ele vai junto no git.
Para outros marketplaces: `/plugin marketplace add <usuario>/<repo> --scope project`.

**Opção 3 — Criar uma skill nova.**
Peça ao Claude Code: *"use a skill-creator para criar uma skill que ... e salve em .claude/skills/"*.

Depois de instalar: registre a skill e o commit auditado na tabela **Skills adicionais**
do `CLAUDE.md` e reinicie o Claude Code. Atualizou a skill? Audite de novo.

## Usando no Claude.ai (sem Claude Code)

- Instale os arquivos `.skill` em Configurações → Skills.
- Crie um Projeto, cole o conteúdo do `CLAUDE.md` nas instruções e suba os arquivos
  do design system e wireframes como conhecimento do projeto conforme ficarem prontos.

## Licença

[MIT](LICENSE) — vale para os arquivos deste template. As skills de terceiros instaladas pelo
`setup-skills.sh` seguem a licença de cada repositório de origem.
