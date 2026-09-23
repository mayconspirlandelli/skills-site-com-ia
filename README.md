# Template: sites com IA generativa + Skills

Template de projeto para criar sites com o Claude Code a partir de sites de referência.
O fluxo transforma referências em texto estruturado (HTML limpo, wireframes, especificações
e design system) antes de gerar código, o que deixa o resultado muito mais fiel e consistente.

Plano completo: [`docs/plano.md`](docs/plano.md)

## Como usar

1. No GitHub, clique em **Use this template** → crie o repositório do novo site.
2. Clone e abra o Claude Code na pasta:
   ```bash
   git clone https://github.com/<usuario>/<novo-site>.git
   cd <novo-site>
   claude
   ```
3. Diga algo como: *"Quero criar um site para [seu negócio]. Tenho estes sites de referência: ..."*

A skill `site-com-referencias` conduz o processo e chama as demais na ordem certa.

## O que vem no template

```
├── CLAUDE.md              instruções permanentes lidas em toda sessão
├── .claude/
│   ├── settings.json      marketplaces e plugins do projeto
│   └── skills/            skills do fluxo (versionadas com o projeto)
├── auditorias/           relatórios de auditoria das skills instaladas
├── docs/plano.md          o plano do processo
├── scripts/
│   └── adicionar-skill.sh instala skills de outros repositórios
├── 00_briefing/           briefing.md
├── 01_referencias/        referencias.md + prints/
├── 02_html_referencias/   HTML limpo e resumo de cada referência
├── 03_wireframes/         wireframes e especificação de componentes
├── 04_design_system/      design_system.md + tokens.css
└── 05_site/               código do site
```

## Skills incluídas

| Skill | Etapa |
|-------|-------|
| `site-com-referencias` | Orquestra o fluxo e indica o próximo passo |
| `referencias-briefing` | Briefing e coleta de referências |
| `extrair-html-referencia` | Limpa o HTML e extrai fontes, cores, breakpoints (script Python) |
| `print-para-wireframe` | Prints → wireframe em texto → especificação |
| `gerar-design-system` | design_system.md, tokens.css e verificação de contraste |
| `construir-site` | Código seção por seção + checklist de validação |
| `auditar-skill` | Auditoria de segurança de skills de terceiros antes de instalar |

Requisito dos scripts: Python 3 e `pip install beautifulsoup4`.

## Adicionando skills durante o projeto

> 🔒 **Toda skill de terceiros passa pela auditoria antes de ser instalada.**
> Skills dão instruções à IA e podem trazer scripts que rodam no seu computador,
> com acesso a arquivos, rede e credenciais. A skill `auditar-skill` verifica prompt
> injection, envio de dados, acesso a credenciais, código ofuscado, persistência e
> comandos destrutivos, e dá um veredito: ✅ OK, ⚠️ REVISAR ou ⛔ BLOQUEAR.
> Os relatórios ficam em `auditorias/`.

**Opção 1 — Script com auditoria automática (recomendado).**
```bash
./scripts/adicionar-skill.sh https://github.com/<usuario>/<repo> caminho/da/skill
./scripts/adicionar-skill.sh <url> caminho/da/skill --global   # para todos os projetos
```
Baixa em pasta temporária, audita e só instala se passar (REVISAR pede sua confirmação,
BLOQUEAR impede a instalação).

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

Se uma skill criada no projeto se mostrar útil, copie-a de volta para este template.

## Usando no Claude.ai (sem Claude Code)

- Instale os arquivos `.skill` em Configurações → Skills.
- Crie um Projeto, cole o conteúdo do `CLAUDE.md` nas instruções e suba os arquivos
  do design system e wireframes como conhecimento do projeto conforme ficarem prontos.
