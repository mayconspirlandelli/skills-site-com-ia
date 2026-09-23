#!/usr/bin/env bash
# Copia uma skill de um repositório Git para .claude/skills/ deste projeto.
#
# Uso:
#   ./scripts/adicionar-skill.sh <url-do-repo> <caminho-da-skill-no-repo> [--global]
#
# Exemplo:
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills skills/frontend-design
#
# --global instala em ~/.claude/skills/ (vale para todos os projetos).
set -euo pipefail

if [ $# -lt 2 ]; then
  sed -n '2,11p' "$0"; exit 1
fi

REPO="$1"; CAMINHO="${2%/}"; DESTINO_BASE=".claude/skills"
[ "${3:-}" = "--global" ] && DESTINO_BASE="$HOME/.claude/skills"

NOME="$(basename "$CAMINHO")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 --quiet "$REPO" "$TMP/repo"
[ -f "$TMP/repo/$CAMINHO/SKILL.md" ] || { echo "Erro: $CAMINHO/SKILL.md não encontrado no repositório."; exit 1; }

mkdir -p "$DESTINO_BASE"
if [ -d "$DESTINO_BASE/$NOME" ]; then
  read -r -p "A skill '$NOME' já existe em $DESTINO_BASE. Sobrescrever? [s/N] " r
  [ "$r" = "s" ] || exit 0
  rm -rf "$DESTINO_BASE/$NOME"
fi
cp -r "$TMP/repo/$CAMINHO" "$DESTINO_BASE/$NOME"

echo "✅ Skill '$NOME' instalada em $DESTINO_BASE/$NOME"
echo "   Revise o SKILL.md antes de usar, registre a skill na tabela do CLAUDE.md"
echo "   e reinicie o Claude Code para ela ser carregada."
