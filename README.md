# Template: sites com IA generativa + Skills

🇧🇷 Português · 🇺🇸 [English](README.en.md)

Template para criar **websites, sites institucionais e landing pages** com o Claude Code a
partir de sites de referência. O fluxo transforma referências em texto estruturado (HTML limpo,
wireframes SVG, especificações e design system) antes de gerar código, o que deixa o resultado
muito mais fiel e consistente.

Plano completo: [`docs/plano.md`](docs/plano.md) · Diagrama do processo: [`docs/diagrama-processo.html`](docs/diagrama-processo.html)

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

### 2. Instale as primeiras skills (`grill-me` + `grilling`)

Na pasta do projeto (no Windows, use o Git Bash):

```bash
./scripts/setup-skills.sh inicial
```

### 3. Abra o Claude Code e faça a entrevista

```bash
claude
```

Digite `/grill-me` ou diga algo como: *"Quero criar uma landing page para [seu negócio]."*
A skill `site-com-referencias` conduz o processo:

1. **Entrevista:** a `grill-me` faz uma série de perguntas sobre o site ou landing page
   (objetivo, público, páginas, conteúdo, stack, animações...) e monta o plano para codificar
   em `etapas/00_briefing/entrevista.md`.
2. **Prompts de imagens:** a partir do plano, o Claude cria os prompts para gerar mockups das
   páginas e imagens do site (`etapas/00_briefing/prompts_imagens.md`). Os mockups gerados viram
   referência visual na etapa de wireframes.
3. **Demais skills:** você roda `./scripts/setup-skills.sh obrigatorias` (e `animacao`, se
   houver animações ou vídeos).
4. **Plano:** segue os passos de [`docs/plano.md`](docs/plano.md) — briefing, referências,
   extração de HTML, wireframes, design system e construção do site.

### Requisitos

- [Claude Code](https://claude.com/claude-code)
- Git e Bash (no Windows, Git Bash)
- Python 3 e `pip install beautifulsoup4`
- Node.js (para o site e para o `playwright-cli`)

## O que vem no template

```
├── CLAUDE.md              instruções permanentes lidas em toda sessão
├── .claude/
│   ├── settings.json      marketplaces e plugins do projeto
│   └── skills/            skills do fluxo (versionadas com o projeto)
├── auditorias/            relatórios de auditoria das skills instaladas
├── docs/
│   ├── plano.md           o plano do processo
│   ├── diagrama-processo.html  diagrama das etapas (abra no navegador)
│   ├── skills-obrigatorias.md  skills de terceiros e como instalar
│   └── recursos.md        links úteis (referências, animações, skills)
├── scripts/
│   ├── setup-skills.sh    audita e instala as skills de terceiros do template
│   └── adicionar-skill.sh audita e instala qualquer outra skill
├── etapas/                construção do site, uma pasta por etapa
│   ├── 00_briefing/       briefing.md + prints/ enviados
│   ├── 01_extracao/       design extraído do código (codigo/) e dos prints (prints/)
│   ├── 02_previa/         prévia do site
│   ├── 03_mockup/         prompt e imagem do site
│   ├── 04_wireframes/     wireframes SVG
│   ├── 05_design_system/  design_system.md + tokens.css
│   └── 06_construcao/     plano de construção e relatório de validação
└── site/                  código do site (pronto para Docker e deploy)
```

## Skills incluídas

| Skill | Etapa |
|-------|-------|
| `site-com-referencias` | Orquestra o fluxo e indica o próximo passo |
| `referencias-briefing` | Briefing e coleta de referências |
| `extrair-html-referencia` | Limpa o HTML e extrai fontes, cores, breakpoints (script Python) |
| `print-para-wireframe` | Prints → wireframe SVG → especificação (com validador) |
| `gerar-design-system` | design_system.md, tokens.css e verificação de contraste |
| `construir-site` | Código seção por seção + checklist de validação |
| `auditar-skill` | Auditoria de segurança de skills de terceiros antes de instalar |

## Skills de terceiros (instaladas pelo script)

Não vêm versionadas no template — cada uma tem licença e autor próprios. O
`scripts/setup-skills.sh` audita e instala cada uma no seu projeto. Detalhes e comandos
`npx` manuais em [`docs/skills-obrigatorias.md`](docs/skills-obrigatorias.md).

| Grupo | Skills | Comando |
|-------|--------|---------|
| Inicial | `grill-me`, `grilling` | `./scripts/setup-skills.sh inicial` |
| Obrigatórias | `frontend-design`, `web-design-guidelines`, `image-to-code`, `design-taste-frontend`, `playwright-cli`, `diagram-design` | `./scripts/setup-skills.sh obrigatorias` |
| Animação/vídeo (opcional) | `remotion-best-practices`, `motion-design` | `./scripts/setup-skills.sh animacao` |

## Adicionando outras skills

> 🔒 **Toda skill de terceiros passa pela auditoria antes de ser instalada.**
> Skills dão instruções à IA e podem trazer scripts que rodam no seu computador,
> com acesso a arquivos, rede e credenciais. A skill `auditar-skill` verifica prompt
> injection, envio de dados, acesso a credenciais, código ofuscado, persistência e
> comandos destrutivos, e dá um veredito: ✅ OK, ⚠️ REVISAR ou ⛔ BLOQUEAR.
> Os relatórios ficam em `auditorias/`.

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
