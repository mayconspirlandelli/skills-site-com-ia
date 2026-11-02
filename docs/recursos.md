# Useful resources

Links that help in several steps of the workflow. Use them as inspiration and tools — the
references' content never goes straight into the site (see the rules in `CLAUDE.md`).

## Design references

- **[Refero Styles](https://styles.refero.design/)** — library of real-site styles to search for
  references (briefing and references step).

## Animations

- **[Kinetics](https://kinetics.colorion.co/#library)** — library of UI animations with spring
  physics (stiffness/damping) instead of fixed-duration easing. Generates CSS, React or a
  ready-made prompt for the AI.
- **[Remotion](https://www.remotion.dev/)** — creates videos and motion graphics with React; works
  with coding agents and batch rendering. To start a video project:
  ```bash
  npx create-video@latest
  ```
  Combine it with the `remotion-best-practices` skill (see [`skills-obrigatorias.md`](skills-obrigatorias.md)).

## Skills

- **[skills.sh](https://www.skills.sh/)** — catalog of skills for AI agents, installable with a
  single command. Before installing any of them, audit it (`./scripts/adicionar-skill.sh`).
- Third-party skills used by this template: [`skills-obrigatorias.md`](skills-obrigatorias.md).
