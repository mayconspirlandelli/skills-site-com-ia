#!/usr/bin/env bash
# Audits and copies a skill from a Git repository into this project's .claude/skills/.
#
# Usage:
#   ./scripts/adicionar-skill.sh <repo-url> <skill-path-or-name> [--commit <sha>] [--global] [--forcar]
#
# Examples:
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills skills/frontend-design
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills frontend-design
#
# --commit  installs exactly this commit (the audited one), not the latest
# --global  installs into ~/.claude/skills/ (applies to all projects)
# --forcar  allows installing even with a BLOCK verdict (not recommended)
#
# Reviewed exceptions: etapas/auditorias/excecoes.txt lists "<skill> <commit> <reason>" for skills with
# a REVIEW/BLOCK verdict approved by the user after manual review. For them, the script shows
# the findings and asks for confirmation instead of blocking.
set -euo pipefail

if [ $# -lt 2 ]; then sed -n '2,19p' "$0"; exit 1; fi

REPO="$1"; CAMINHO="${2%/}"; shift 2
DESTINO_BASE=".claude/skills"; FORCAR=0; FIXO=""
while [ $# -gt 0 ]; do
  case "$1" in
    --global) DESTINO_BASE="$HOME/.claude/skills" ;;
    --forcar) FORCAR=1 ;;
    --commit) FIXO="${2:-}"; shift ;;
  esac
  shift
done

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
AUDITOR="$RAIZ/.claude/skills/auditar-skill/scripts/auditar_skill.py"
[ -f "$AUDITOR" ] || { echo "Error: auditor not found at $AUDITOR"; exit 1; }

NOME="$(basename "$CAMINHO")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "→ Downloading $REPO${FIXO:+ @ $FIXO} (temporary folder, nothing is installed yet)..."
if [ -n "$FIXO" ]; then
  git init --quiet "$TMP/repo"
  git -C "$TMP/repo" fetch --quiet --depth 1 "$REPO" "$FIXO"
  git -C "$TMP/repo" checkout --quiet FETCH_HEAD
else
  git clone --depth 1 --quiet "$REPO" "$TMP/repo"
fi
COMMIT="$(git -C "$TMP/repo" rev-parse --short=7 HEAD)"
ORIGEM="$TMP/repo/$CAMINHO"
if [ ! -f "$ORIGEM/SKILL.md" ]; then
  # Accepts just the skill name: looks for a folder with that name or a SKILL.md with "name: <name>".
  ACHADO="$(find "$TMP/repo" -path "*/$NOME/SKILL.md" -not -path "*/.git/*" | head -n 1 || true)"
  [ -n "$ACHADO" ] || ACHADO="$(grep -rlx --include=SKILL.md "name: *$NOME *" "$TMP/repo" | head -n 1 || true)"
  [ -n "$ACHADO" ] || { echo "Error: skill '$CAMINHO' not found in the repository."; exit 1; }
  ORIGEM="$(dirname "$ACHADO")"
  echo "→ Skill found at ${ORIGEM#$TMP/repo/}"
fi

RELATORIO="$RAIZ/etapas/auditorias/${NOME}_${COMMIT}.md"
mkdir -p "$RAIZ/etapas/auditorias"
echo "→ Auditing '$NOME' (commit $COMMIT)..."
# Reads the printed verdict (not the exit code), so a Python error never becomes "REVIEW".
VEREDITO="$(python3 "$AUDITOR" "$ORIGEM" --md "$RELATORIO" --silencioso | tail -n 1 | tr -d '[:space:]' || true)"

EXCECAO="$(grep -E "^$NOME $COMMIT " "$RAIZ/etapas/auditorias/excecoes.txt" 2>/dev/null | head -n 1 || true)"
if [ -n "$EXCECAO" ] && { [ "$VEREDITO" = "REVIEW" ] || [ "$VEREDITO" = "BLOCK" ]; }; then
  echo "⚠️  Verdict: $VEREDITO — with a reviewed exception recorded in etapas/auditorias/excecoes.txt:"
  echo "   ${EXCECAO#"$NOME $COMMIT "}"
  grep -E '^\- \*\*(CRITICAL|HIGH)' "$RELATORIO" | sed 's/^/   /' | head -n 12
  echo "   Full report: $RELATORIO"
  read -r -p "   Install based on the recorded review? [y/N] " r
  [ "$r" = "y" ] || { echo "Installation cancelled."; exit 1; }
  VEREDITO="EXCECAO"
fi

case $VEREDITO in
  EXCECAO) ;;
  OK) echo "✅ Verdict: OK" ;;
  REVIEW) echo "⚠️  Verdict: REVIEW — findings that need your assessment:"
     grep -E '^\- \*\*(CRITICAL|HIGH|MEDIUM)' "$RELATORIO" | sed 's/^/   /'
     echo "   Full report: $RELATORIO"
     read -r -p "   Did you read the findings and still want to install? [y/N] " r
     [ "$r" = "y" ] || { echo "Installation cancelled."; exit 1; } ;;
  BLOCK) echo "⛔ Verdict: BLOCK — critical findings:"
     grep -E '^\- \*\*CRITICAL' "$RELATORIO" | sed 's/^/   /'
     echo "   Full report: $RELATORIO"
     if [ $FORCAR -ne 1 ]; then echo "Installation blocked. (Use --forcar only if you are absolutely sure.)"; exit 2; fi
     read -r -p "   WARNING: install a blocked skill? Type INSTALL to confirm: " r
     [ "$r" = "INSTALL" ] || { echo "Installation cancelled."; exit 2; } ;;
  *) echo "Audit error."; exit 1 ;;
esac

echo "   Tip: even with OK, read SKILL.md and the scripts — the scan doesn't catch everything."

mkdir -p "$DESTINO_BASE"
if [ -d "$DESTINO_BASE/$NOME" ]; then
  read -r -p "Skill '$NOME' already exists in $DESTINO_BASE. Overwrite? [y/N] " r
  [ "$r" = "y" ] || exit 0
  rm -rf "$DESTINO_BASE/$NOME"
fi
cp -r "$ORIGEM" "$DESTINO_BASE/$NOME"

echo "✅ Skill '$NOME' installed at $DESTINO_BASE/$NOME (commit $COMMIT)"
echo "   Record it in CLAUDE.md: | $NOME | $REPO @ $COMMIT | <when to use> |"
echo "   Restart Claude Code for it to be loaded."
