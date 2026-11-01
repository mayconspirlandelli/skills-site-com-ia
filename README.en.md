# Template: AI-generated websites + Skills

🇧🇷 [Português](README.md) · 🇺🇸 English

A template for building **websites, company sites and landing pages** with Claude Code in
**8 steps**, from understanding the business to a validated site ready to deploy. Each step
produces a structured text file the next one reads (briefing, design extracted from references,
preview, SVG wireframes, design system) — and four of them only move on with your approval.

> The workflow files, skills and in-project docs are written in **Portuguese (PT-BR)**.
> Claude Code works fine with them — you can talk to it in English.

Full plan (PT-BR): [`docs/plano.md`](docs/plano.md) · Process diagram: [`docs/diagrama-processo.html`](docs/diagrama-processo.html)

## The 8 steps

| # | Step | Skill | Approval |
|---|------|-------|----------|
| 1 | **Interview & briefing** — business, goal, audience, architecture, hosting, Docker, design, reference URLs and screenshots | `entrevista-site` | ✅ |
| 2 | **Design extracted from the references' code** (HTML, CSS and computed styles after JavaScript) | `extrair-html-referencia` | |
| 3 | **Design extracted from screenshots** | `extrair-design-prints` | |
| 4 | **Site preview** in Markdown | `gerar-previa` | |
| 5 | **Site image** — prompt + SVG mockup | `gerar-mockup` | ✅ |
| 6 | **SVG wireframes** of every page, desktop and mobile | `gerar-wireframes` | ✅ |
| 7 | **Design system** in Markdown and HTML, with tokens | `gerar-design-system` | ✅ |
| 8 | **Plan, build & validation** — code in `site/`, Docker/deploy files and a report | `construir-site` | |

`site-com-referencias` orchestrates the steps; `auditar-skill` audits any third-party skill before it is installed.

## How to use

### 1. Create your project from the template

On GitHub, open this repository and click **Use this template → Create a new repository**.
Or from the command line with the [GitHub CLI](https://cli.github.com/):

```bash
gh repo create my-site --template mayconspirlandelli/skills-site-com-ia --private --clone
```

If you created it on the website, clone the new repository:

```bash
git clone https://github.com/<user>/<my-site>.git
```

### 2. Install the third-party skills

From the project folder (on Windows, use Git Bash). The script audits each skill before installing:

```bash
./scripts/setup-skills.sh obrigatorias
```

### 3. Open Claude Code and start

```bash
claude
```

Say something like: *"I want to build a landing page for [your business]."* The
`site-com-referencias` skill drives the 8 steps, starting with the interview. Progress lives in
the `etapas/` folders and in `etapas/aprovacoes.md`, so you can stop and resume in another session.

### Requirements

- [Claude Code](https://claude.com/claude-code)
- Git and Bash (Git Bash on Windows)
- Python 3 and `pip install beautifulsoup4 pillow`
- Node.js (for the site and for `playwright-cli`)

## Folder layout

```
├── .claude/skills/   ·  scripts/  ·  docs/  ·  auditorias/     framework
├── etapas/                 one folder per step (briefing → extraction → preview →
│                           mockup → wireframes → design system → build) + aprovacoes.md
└── site/                   the site code only, ready for Docker and deploy
```

## Third-party skills (installed by script)

They are **not bundled** with the template — each one has its own license and author.
`scripts/setup-skills.sh` downloads each skill to a temp folder, runs the security audit,
saves the report in `auditorias/` and installs only the audited commit.
Details and manual `npx` commands: [`docs/skills-obrigatorias.md`](docs/skills-obrigatorias.md).

| Group | Skills | Command |
|-------|--------|---------|
| Required | `frontend-design`, `web-design-guidelines`, `image-to-code`, `design-taste-frontend`, `playwright-cli`, `diagram-design` | `./scripts/setup-skills.sh obrigatorias` |
| Animation/video (if the briefing asks) | `remotion-best-practices`, `motion-design` | `./scripts/setup-skills.sh animacao` |
| Extras (optional) | `grill-me`, `grilling` | `./scripts/setup-skills.sh extras` |

## Adding other skills

> 🔒 **Every third-party skill is audited before installation.** Skills give instructions to
> the AI and may ship scripts that run on your machine with access to files, network and
> credentials. The verdict is ✅ OK, ⚠️ REVIEW (asks you) or ⛔ BLOCK (won't install).

```bash
./scripts/adicionar-skill.sh https://github.com/<user>/<repo> <skill-name-or-path>
```

After installing, record the skill and the audited commit in the **Skills adicionais** table
in `CLAUDE.md` and restart Claude Code.

## License

[MIT](LICENSE) — applies to this template's files. Third-party skills installed by
`setup-skills.sh` keep the license of their own source repositories.
