# Skills de terceiros do template

Todo projeto de website criado a partir deste template deve ter as skills abaixo instaladas,
além das skills do fluxo que já vêm em `.claude/skills/`.

As skills de terceiros **não vêm versionadas no template** (cada uma tem a licença e o autor
dela). Elas são auditadas e instaladas no seu projeto pelo script `scripts/setup-skills.sh`.

## Quando instalar

1. **Antes do passo 1:** as **obrigatórias** (`./scripts/setup-skills.sh obrigatorias`). Elas são usadas
   pelo fluxo: `playwright-cli` mede as referências (passo 2) e valida o site (passo 8);
   `frontend-design` e `design-taste-frontend` dão direção ao mockup (passo 5) e à construção.
2. **Depois da entrevista:** as de **animação**, só se o briefing pedir animações ou vídeos.
3. **Opcional:** os **extras**, para entrevistas fora do fluxo.

A entrevista do fluxo é a skill `entrevista-site`, que já vem no template — não depende de skill de terceiros.

## Skills

### Obrigatórias (antes do passo 1)

| Skill | Repositório | Para que serve |
|-------|-------------|----------------|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) | Direção visual intencional, tipografia e escolhas que não parecem template |
| `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Revisão da interface contra boas práticas de web design e acessibilidade |
| `image-to-code` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Converte imagens/prints em código de interface |
| `design-taste-frontend` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Evita interfaces genéricas em landing pages, portfólios e redesigns |
| `playwright-cli` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Abre o site no navegador para testar, tirar prints e validar responsividade |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Diagramas (fluxograma, sequência, arquitetura, jornada do usuário, sitemap/árvore...) em HTML/SVG/PNG, com importação de Mermaid, draw.io e Excalidraw. A auditoria dá **REVISAR** por falsos positivos (frases como "do not silently ship" e exemplos de OAuth/git); revisada manualmente no commit `0cf73c3` |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Direção de design, crítica, auditoria e polimento de interfaces, com detector de problemas de design. **Instalada no commit fixo `e89e3ad`** (exceção revisada): baixa e executa um binário do GitHub verificado por checksum e pode instalar hooks no Claude Code (pede consentimento). Revisão em `etapas/auditorias/impeccable_e89e3ad_revisao.md` |

### Animação e vídeo (só quando precisar)

| Skill | Repositório | Quando instalar |
|-------|-------------|-----------------|
| `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Animações ou vídeos gerados com código (Remotion/React) |
| `motion-design` | [lottiefiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill) | Animações / motion design (ex.: Lottie) |

### Extras (opcional)

| Skill | Repositório | Para que serve |
|-------|-------------|----------------|
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) | Atalho `/grill-me` para uma entrevista em rodadas sobre qualquer plano (só o usuário aciona) |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | A entrevista em si, chamada pela `grill-me` |

## Como instalar

> 🔒 Regra do projeto (ver `CLAUDE.md`): **nenhuma skill de terceiros é instalada sem auditoria.**

### Opção 1 — Script de setup (recomendado)

Na raiz do projeto (no Windows, use o Git Bash):

```bash
./scripts/setup-skills.sh obrigatorias
```

Só se o briefing pedir animações ou vídeos:

```bash
./scripts/setup-skills.sh animacao
```

Opcional:

```bash
./scripts/setup-skills.sh extras
```

Para cada skill, o script baixa o repositório numa pasta temporária, roda a auditoria
(`auditar-skill`), salva o relatório em `etapas/auditorias/` e só instala em `.claude/skills/`
**o mesmo commit que foi auditado**:

- ✅ **OK** — instala.
- ⚠️ **REVISAR** — mostra os achados e pede sua confirmação.
- ⛔ **BLOQUEAR** — não instala.

**Commit fixo e exceções revisadas.** Uma entrada do `setup-skills.sh` pode fixar o commit
(3º campo), para instalar sempre a versão revisada. Skills com REVISAR/BLOQUEAR aprovadas pelo
usuário depois de revisão manual ficam em `etapas/auditorias/excecoes.txt` (`<skill> <commit> <motivo>`):
para esse commit exato, o script mostra os achados e pede confirmação em vez de bloquear.
Para instalar uma skill avulsa num commit: `./scripts/adicionar-skill.sh <url> <caminho> --commit <sha-completo>`.

Requisitos: Git, Python 3 e Bash (no Windows, Git Bash).

### Opção 2 — `npx skills add` (manual)

O `npx` instala direto, **sem auditar**, e sempre a versão mais nova do repositório. Use só
depois de auditar a skill pedindo ao Claude Code: *"audite a skill `<nome>` do repositório `<url>`"*.

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
(o `npx` instala a versão mais nova, não o commit revisado — prefira o script)

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

Requisito: Node.js.

## Depois de instalar

Preencha a tabela **Skills adicionais deste projeto** no `CLAUDE.md` com a origem, o commit
auditado e o veredito de cada skill, e reinicie o Claude Code. Atualizou alguma skill? Audite de novo.

## Checklist

- [ ] `frontend-design` — auditada e instalada
- [ ] `web-design-guidelines` — auditada e instalada
- [ ] `image-to-code` — auditada e instalada
- [ ] `design-taste-frontend` — auditada e instalada
- [ ] `playwright-cli` — auditada e instalada
- [ ] `diagram-design` — auditada e instalada
- [ ] `impeccable` — instalada no commit revisado `e89e3ad`
- [ ] `remotion-best-practices` — só se houver animações/vídeos
- [ ] `motion-design` — só se houver animações/motion design
- [ ] `grill-me` e `grilling` — opcionais
- [ ] Tabela do `CLAUDE.md` preenchida
