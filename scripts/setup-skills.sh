#!/usr/bin/env bash
# Audits and installs the template's third-party skills (listed in docs/skills-obrigatorias.md).
# Each skill goes through ./scripts/adicionar-skill.sh: downloads to a temporary folder, audits
# and installs only the audited commit into .claude/skills/. An entry can pin the commit (3rd field).
#
# Usage:
#   ./scripts/setup-skills.sh obrigatorias  # before step 1: skills used by the workflow
#   ./scripts/setup-skills.sh animacao      # only if the briefing calls for animations or videos
#   ./scripts/setup-skills.sh extras        # optional: grill-me + grilling (interviews outside the workflow)
set -euo pipefail

OBRIGATORIAS=(
  "https://github.com/anthropics/skills frontend-design"
  "https://github.com/vercel-labs/agent-skills web-design-guidelines"
  "https://github.com/leonxlnx/taste-skill image-to-code"
  "https://github.com/leonxlnx/taste-skill design-taste-frontend"
  "https://github.com/microsoft/playwright-cli playwright-cli"
  "https://github.com/cathrynlavery/diagram-design diagram-design"
  "https://github.com/pbakaus/impeccable .claude/skills/impeccable e89e3ada3e875a89ac2c5d33d11e65ebef6fe285"   # fixed commit: reviewed exception
)
ANIMACAO=(
  "https://github.com/remotion-dev/skills remotion-best-practices"
  "https://github.com/lottiefiles/motion-design-skill motion-design"
)
EXTRAS=(
  "https://github.com/mattpocock/skills grill-me"
  "https://github.com/mattpocock/skills grilling"   # grill-me just calls grilling
)

case "${1:-}" in
  obrigatorias) LISTA=("${OBRIGATORIAS[@]}") ;;
  animacao)     LISTA=("${ANIMACAO[@]}") ;;
  extras)       LISTA=("${EXTRAS[@]}") ;;
  *) sed -n '2,9p' "$0"; exit 1 ;;
esac

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
FALHAS=()
for item in "${LISTA[@]}"; do
  read -r repo skill commit <<< "$item"
  echo
  echo "════ $skill ════"
  "$RAIZ/scripts/adicionar-skill.sh" "$repo" "$skill" ${commit:+--commit "$commit"} || FALHAS+=("$(basename "$skill")")
done

echo
if [ ${#FALHAS[@]} -eq 0 ]; then
  echo "✅ All skills installed. Record them in the CLAUDE.md table and restart Claude Code."
else
  echo "⚠️  Not installed: ${FALHAS[*]} — see the reports in etapas/auditorias/."
  exit 1
fi
