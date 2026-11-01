# Template: AI-generated websites + Skills

🇧🇷 [Português](README.md) · 🇺🇸 English

A template for building **websites, company sites and landing pages** with Claude Code from
reference sites. The workflow turns references into structured text (clean HTML, SVG wireframes,
component specs and a design system) before any code is generated, which makes the result far
more faithful and consistent.

> The workflow files, skills and in-project docs are written in **Portuguese (PT-BR)**.
> Claude Code works fine with them — you can talk to it in English.

Full plan (PT-BR): [`docs/plano.md`](docs/plano.md)

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

### 2. Install the first skills (`grill-me` + `grilling`)

From the project folder (on Windows, use Git Bash):

```bash
./scripts/setup-skills.sh inicial
```

### 3. Open Claude Code and do the interview

```bash
claude
```

Type `/grill-me` or say something like: *"I want to build a landing page for [your business]."*
The `site-com-referencias` skill drives the process:

1. **Interview:** `grill-me` asks a series of questions about the site or landing page
   (goal, audience, pages, content, stack, animations...) and writes the coding plan to
   `00_briefing/entrevista.md`.
2. **Image prompts:** based on that plan, Claude writes prompts to generate page mockups and
   site images (`00_briefing/prompts_imagens.md`). The generated mockups become visual
   references for the wireframe step.
3. **Remaining skills:** run `./scripts/setup-skills.sh obrigatorias` (plus `animacao` if the
   site has animations or videos).
4. **Plan:** follow the steps in [`docs/plano.md`](docs/plano.md) — briefing, references,
   HTML extraction, wireframes, design system and building the site.

### Requirements

- [Claude Code](https://claude.com/claude-code)
- Git and Bash (Git Bash on Windows)
- Python 3 and `pip install beautifulsoup4`
- Node.js (for the site and for `playwright-cli`)

## Workflow

| Step | Skill | Output |
|------|-------|--------|
| Setup & interview | `grill-me` (third-party) | `00_briefing/entrevista.md` |
| Briefing & references | `referencias-briefing` | `00_briefing/`, `01_referencias/` |
| HTML extraction | `extrair-html-referencia` | `02_html_referencias/` |
| Wireframes & specs | `print-para-wireframe` | `03_wireframes/` (SVG wireframes) |
| Design system | `gerar-design-system` | `04_design_system/` |
| Build & validate | `construir-site` | `05_site/` |

`auditar-skill` audits any third-party skill before it is installed.

## Third-party skills (installed by script)

They are **not bundled** with the template — each one has its own license and author.
`scripts/setup-skills.sh` downloads each skill to a temp folder, runs the security audit,
saves the report in `auditorias/` and installs only the audited commit.
Details and manual `npx` commands: [`docs/skills-obrigatorias.md`](docs/skills-obrigatorias.md).

| Group | Skills | Command |
|-------|--------|---------|
| First | `grill-me`, `grilling` | `./scripts/setup-skills.sh inicial` |
| Required | `frontend-design`, `web-design-guidelines`, `image-to-code`, `design-taste-frontend`, `playwright-cli`, `diagram-design` | `./scripts/setup-skills.sh obrigatorias` |
| Animation/video (optional) | `remotion-best-practices`, `motion-design` | `./scripts/setup-skills.sh animacao` |

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
