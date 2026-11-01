# Skills de terceiros do template

Todo projeto de website criado a partir deste template deve ter as skills abaixo instaladas,
além das skills do fluxo que já vêm em `.claude/skills/`.

As skills de terceiros **não vêm versionadas no template** (cada uma tem a licença e o autor
dela). Elas são auditadas e instaladas no seu projeto pelo script `scripts/setup-skills.sh`.

## Ordem do setup

1. **`grill-me` primeiro, sempre.** É a primeira skill a ser instalada, junto com a `grilling`
   (a `grill-me` é só um atalho que chama a `grilling`, onde estão as instruções da entrevista).
2. **Entrevista.** Com a `grill-me`, o Claude faz uma série de perguntas sobre o website ou
   landing page e monta o plano para codificar. Saída: `etapas/00_briefing/entrevista.md`.
3. **Prompts de imagens.** A partir do plano da entrevista, o Claude cria os prompts para gerar
   as imagens do site — mockups das páginas e imagens de conteúdo. Saída: `etapas/00_briefing/prompts_imagens.md`.
4. **Instalar as demais skills** obrigatórias — e as de animação, se a entrevista indicar
   animações ou vídeos.
5. **Seguir os passos do plano** [`docs/plano.md`](plano.md)
   (briefing → referências → HTML → wireframes → design system → site), conduzidos pela skill
   `site-com-referencias`.

## Skills

### Inicial (antes da entrevista)

| Skill | Repositório | Para que serve |
|-------|-------------|----------------|
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) | Atalho `/grill-me` para iniciar a entrevista (só o usuário aciona) |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | A entrevista em si: rodadas de perguntas numeradas, cada uma com resposta recomendada, até fechar o plano |

### Obrigatórias (depois da entrevista)

| Skill | Repositório | Para que serve |
|-------|-------------|----------------|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) | Direção visual intencional, tipografia e escolhas que não parecem template |
| `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Revisão da interface contra boas práticas de web design e acessibilidade |
| `image-to-code` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Converte imagens/prints em código de interface |
| `design-taste-frontend` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Evita interfaces genéricas em landing pages, portfólios e redesigns |
| `playwright-cli` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Abre o site no navegador para testar, tirar prints e validar responsividade |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Diagramas (fluxograma, sequência, arquitetura, jornada do usuário, sitemap/árvore...) em HTML/SVG/PNG, com importação de Mermaid, draw.io e Excalidraw. A auditoria dá **REVISAR** por falsos positivos (frases como "do not silently ship" e exemplos de OAuth/git); revisada manualmente no commit `0cf73c3` |

### Animação e vídeo (só quando precisar)

| Skill | Repositório | Quando instalar |
|-------|-------------|-----------------|
| `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Animações ou vídeos gerados com código (Remotion/React) |
| `motion-design` | [lottiefiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill) | Animações / motion design (ex.: Lottie) |

## Como instalar

> 🔒 Regra do projeto (ver `CLAUDE.md`): **nenhuma skill de terceiros é instalada sem auditoria.**

### Opção 1 — Script de setup (recomendado)

Na raiz do projeto (no Windows, use o Git Bash):

```bash
./scripts/setup-skills.sh inicial
```

Faça a entrevista com a `grill-me` e depois:

```bash
./scripts/setup-skills.sh obrigatorias
```

Só se o projeto tiver animações ou vídeos:

```bash
./scripts/setup-skills.sh animacao
```

Para cada skill, o script baixa o repositório numa pasta temporária, roda a auditoria
(`auditar-skill`), salva o relatório em `auditorias/` e só instala em `.claude/skills/`
**o mesmo commit que foi auditado**:

- ✅ **OK** — instala.
- ⚠️ **REVISAR** — mostra os achados e pede sua confirmação.
- ⛔ **BLOQUEAR** — não instala.

Requisitos: Git, Python 3 e Bash.

### Opção 2 — `npx skills add` (manual)

O `npx` instala direto, **sem auditar**, e sempre a versão mais nova do repositório. Use só
depois de auditar a skill pedindo ao Claude Code: *"audite a skill `<nome>` do repositório `<url>`"*.

```bash
npx skills add https://github.com/mattpocock/skills --skill grill-me
```

```bash
npx skills add https://github.com/mattpocock/skills --skill grilling
```

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
npx skills add https://github.com/remotion-dev/skills --skill remotion-best-practices
```

```bash
npx skills add https://github.com/lottiefiles/motion-design-skill --skill motion-design
```

Requisito: Node.js.

## Depois de instalar

Preencha a tabela **Skills adicionais deste projeto** no `CLAUDE.md` com a origem, o commit
auditado e o veredito de cada skill, e reinicie o Claude Code. Atualizou alguma skill? Audite de novo.

## Checklist

- [ ] `grill-me` e `grilling` — auditadas e instaladas **(primeiras)**
- [ ] Entrevista feita → `etapas/00_briefing/entrevista.md`
- [ ] Prompts de imagens criados → `etapas/00_briefing/prompts_imagens.md`
- [ ] `frontend-design` — auditada e instalada
- [ ] `web-design-guidelines` — auditada e instalada
- [ ] `image-to-code` — auditada e instalada
- [ ] `design-taste-frontend` — auditada e instalada
- [ ] `playwright-cli` — auditada e instalada
- [ ] `diagram-design` — auditada e instalada
- [ ] `remotion-best-practices` — só se houver animações/vídeos
- [ ] `motion-design` — só se houver animações/motion design
- [ ] Tabela do `CLAUDE.md` preenchida
