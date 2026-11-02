# Template third-party skills

Every website project created from this template must have the skills below installed,
in addition to the workflow skills already shipped in `.claude/skills/`.

Third-party skills are **not versioned in the template** (each one has its own license and
author). They are audited and installed in your project by the `scripts/setup-skills.sh` script.

## When to install

1. **Before step 1:** the **required** ones (`./scripts/setup-skills.sh obrigatorias`). They are used
   by the workflow: `playwright-cli` measures the references (step 2) and validates the site (step 8);
   `frontend-design` and `design-taste-frontend` give direction to the mockup (step 5) and the build.
2. **After the interview:** the **animation** ones, only if the briefing asks for animations or videos.
3. **Optional:** the **extras**, for interviews outside the workflow.

The workflow's interview is the `entrevista-site` skill, which ships with the template — it does not depend on third-party skills.

## Skills

### Required (before step 1)

| Skill | Repository | What it's for |
|-------|------------|---------------|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) | Intentional visual direction, typography and choices that don't look like a template |
| `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Reviews the interface against web design and accessibility best practices |
| `image-to-code` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Converts images/screenshots into interface code |
| `design-taste-frontend` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Avoids generic interfaces in landing pages, portfolios and redesigns |
| `playwright-cli` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Opens the site in the browser to test, take screenshots and validate responsiveness |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Diagrams (flowchart, sequence, architecture, user journey, sitemap/tree...) in HTML/SVG/PNG, with Mermaid, draw.io and Excalidraw import. The audit gives **REVIEW** due to false positives (phrases like "do not silently ship" and OAuth/git examples); manually reviewed at commit `0cf73c3` |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design direction, critique, audit and polish of interfaces, with a design-issue detector. **Installed at fixed commit `e89e3ad`** (reviewed exception): downloads and runs a binary from GitHub verified by checksum and can install hooks in Claude Code (asks for consent). Review in `etapas/auditorias/impeccable_e89e3ad_revisao.md` |

### Animation and video (only when needed)

| Skill | Repository | When to install |
|-------|------------|-----------------|
| `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Animations or videos generated with code (Remotion/React) |
| `motion-design` | [lottiefiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill) | Animations / motion design (e.g. Lottie) |

### Extras (optional)

| Skill | Repository | What it's for |
|-------|------------|---------------|
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) | `/grill-me` shortcut for a round-based interview about any plan (user-triggered only) |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | The interview itself, called by `grill-me` |

## How to install

> 🔒 Project rule (see `CLAUDE.md`): **no third-party skill is installed without an audit.**

### Option 1 — Setup script (recommended)

From the project root (on Windows, use Git Bash):

```bash
./scripts/setup-skills.sh obrigatorias
```

Only if the briefing asks for animations or videos:

```bash
./scripts/setup-skills.sh animacao
```

Optional:

```bash
./scripts/setup-skills.sh extras
```

For each skill, the script downloads the repository to a temporary folder, runs the audit
(`auditar-skill`), saves the report in `etapas/auditorias/` and installs into `.claude/skills/`
**only the same commit that was audited**:

- ✅ **OK** — installs.
- ⚠️ **REVIEW** — shows the findings and asks for your confirmation.
- ⛔ **BLOCK** — does not install.

**Fixed commit and reviewed exceptions.** An entry in `setup-skills.sh` can pin the commit
(3rd field), so the reviewed version is always installed. Skills with REVIEW/BLOCK approved by the
user after manual review are listed in `etapas/auditorias/excecoes.txt` (`<skill> <commit> <reason>`):
for that exact commit, the script shows the findings and asks for confirmation instead of blocking.
To install a single skill at a given commit: `./scripts/adicionar-skill.sh <url> <path> --commit <full-sha>`.

Requirements: Git, Python 3 and Bash (on Windows, Git Bash).

### Option 2 — `npx skills add` (manual)

`npx` installs directly, **without auditing**, and always the latest version of the repository. Use it only
after auditing the skill by asking Claude Code: *"audit the `<name>` skill from repository `<url>`"*.

```bash
npx skills add https://github.com/anthropics/skills --skill frontend-design
```

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
```

```bash
npx skills add https://github.com/leonxlnx/taste-skill --skill image-to-code
```

```bash
npx skills add https://github.com/leonxlnx/taste-skill --skill design-taste-frontend
```

```bash
npx skills add https://github.com/microsoft/playwright-cli --skill playwright-cli
```

```bash
npx skills add https://github.com/cathrynlavery/diagram-design --skill diagram-design
```

```bash
npx skills add https://github.com/pbakaus/impeccable --skill impeccable
```
(`npx` installs the latest version, not the reviewed commit — prefer the script)

```bash
npx skills add https://github.com/remotion-dev/skills --skill remotion-best-practices
```

```bash
npx skills add https://github.com/lottiefiles/motion-design-skill --skill motion-design
```

```bash
npx skills add https://github.com/mattpocock/skills --skill grill-me
```

```bash
npx skills add https://github.com/mattpocock/skills --skill grilling
```

Requirement: Node.js.

## After installing

Fill in the **Additional skills in this project** table in `CLAUDE.md` with the source, audited
commit and verdict of each skill, and restart Claude Code. Updated a skill? Audit it again.

## Checklist

- [ ] `frontend-design` — audited and installed
- [ ] `web-design-guidelines` — audited and installed
- [ ] `image-to-code` — audited and installed
- [ ] `design-taste-frontend` — audited and installed
- [ ] `playwright-cli` — audited and installed
- [ ] `diagram-design` — audited and installed
- [ ] `impeccable` — installed at reviewed commit `e89e3ad`
- [ ] `remotion-best-practices` — only if there are animations/videos
- [ ] `motion-design` — only if there are animations/motion design
- [ ] `grill-me` and `grilling` — optional
- [ ] `CLAUDE.md` table filled in
