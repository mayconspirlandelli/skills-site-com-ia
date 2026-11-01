#!/usr/bin/env bash
# Audita e instala as skills de terceiros do template (lista em docs/skills-obrigatorias.md).
# Cada skill passa por ./scripts/adicionar-skill.sh: baixa em pasta temporária, audita
# e só instala o commit auditado em .claude/skills/.
#
# Uso:
#   ./scripts/setup-skills.sh inicial       # 1º passo: grill-me + grilling (antes da entrevista)
#   ./scripts/setup-skills.sh obrigatorias  # depois da entrevista: as demais obrigatórias
#   ./scripts/setup-skills.sh animacao      # só se o projeto tiver animações ou vídeos
set -euo pipefail

INICIAL=(
  "https://github.com/mattpocock/skills grill-me"
  "https://github.com/mattpocock/skills grilling"   # a grill-me só chama a grilling
)
OBRIGATORIAS=(
  "https://github.com/anthropics/skills frontend-design"
  "https://github.com/vercel-labs/agent-skills web-design-guidelines"
  "https://github.com/leonxlnx/taste-skill image-to-code"
  "https://github.com/leonxlnx/taste-skill design-taste-frontend"
  "https://github.com/microsoft/playwright-cli playwright-cli"
  "https://github.com/cathrynlavery/diagram-design diagram-design"
)
ANIMACAO=(
  "https://github.com/remotion-dev/skills remotion-best-practices"
  "https://github.com/lottiefiles/motion-design-skill motion-design"
)

case "${1:-}" in
  inicial)      LISTA=("${INICIAL[@]}") ;;
  obrigatorias) LISTA=("${OBRIGATORIAS[@]}") ;;
  animacao)     LISTA=("${ANIMACAO[@]}") ;;
  *) sed -n '2,9p' "$0"; exit 1 ;;
esac

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
FALHAS=()
for item in "${LISTA[@]}"; do
  read -r repo skill <<< "$item"
  echo
  echo "════ $skill ════"
  "$RAIZ/scripts/adicionar-skill.sh" "$repo" "$skill" || FALHAS+=("$skill")
done

echo
if [ ${#FALHAS[@]} -eq 0 ]; then
  echo "✅ Todas as skills instaladas. Registre-as na tabela do CLAUDE.md e reinicie o Claude Code."
else
  echo "⚠️  Não instaladas: ${FALHAS[*]} — veja os relatórios em auditorias/."
  exit 1
fi
