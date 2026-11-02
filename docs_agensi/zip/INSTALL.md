# Installation — Site from References

This package has 10 skills and the project structure they use.

```
SKILL.md        orchestrator (site-com-referencias)
skills/         the other 9 skills (one per step + auditar-skill)
template/       project structure: CLAUDE.md, etapas/, site/, docs/, scripts/
```

## 1. Create the project

Create an empty folder for the site and copy **the contents** of `template/` into it
(including the hidden `.claude/` folder).

## 2. Install the skills

Inside the project folder:

```bash
mkdir -p .claude/skills/site-com-referencias
cp /path/to/package/SKILL.md .claude/skills/site-com-referencias/
cp -r /path/to/package/skills/* .claude/skills/
```

When done, `.claude/skills/` should have 10 folders, each with its own `SKILL.md`.

## 3. Requirements

- [Claude Code](https://claude.com/claude-code)
- Git and Bash (Git Bash on Windows)
- Python 3.9+ and `pip install beautifulsoup4 pillow`
- Node.js 18+

## 4. Companion skills (third-party)

The workflow uses skills by other authors (e.g. `playwright-cli`, `frontend-design`). They are not
bundled because they have their own licenses. The script downloads each one, audits it and installs only the audited commit:

```bash
git init   # the script needs a git repository
./scripts/setup-skills.sh obrigatorias
```

If the site has animations or videos: `./scripts/setup-skills.sh animacao`.

## 5. Start

```bash
claude
```

Say: *"I want to build a landing page for [your business]."* The orchestrator drives the 8 steps,
starting with the interview. Progress lives in `etapas/aprovacoes.md`.

Folder and skill names keep their original Portuguese identifiers (`etapas/` = steps,
`entrevista-site` = site interview); everything you read and every message is in English.

Process details: `template/docs/plano.md`.
