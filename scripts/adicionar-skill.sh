#!/usr/bin/env bash
# Audita e copia uma skill de um repositório Git para .claude/skills/ deste projeto.
#
# Uso:
#   ./scripts/adicionar-skill.sh <url-do-repo> <caminho-da-skill-no-repo> [--global] [--forcar]
#
# Exemplo:
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills skills/frontend-design
#
# --global  instala em ~/.claude/skills/ (vale para todos os projetos)
# --forcar  permite instalar mesmo com veredito BLOQUEAR (não recomendado)
set -euo pipefail

if [ $# -lt 2 ]; then sed -n '2,13p' "$0"; exit 1; fi

REPO="$1"; CAMINHO="${2%/}"; shift 2
DESTINO_BASE=".claude/skills"; FORCAR=0
for arg in "$@"; do
  case "$arg" in
    --global) DESTINO_BASE="$HOME/.claude/skills" ;;
    --forcar) FORCAR=1 ;;
  esac
done

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
AUDITOR="$RAIZ/.claude/skills/auditar-skill/scripts/auditar_skill.py"
[ -f "$AUDITOR" ] || { echo "Erro: auditor não encontrado em $AUDITOR"; exit 1; }

NOME="$(basename "$CAMINHO")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "→ Baixando $REPO (pasta temporária, nada é instalado ainda)..."
git clone --depth 1 --quiet "$REPO" "$TMP/repo"
COMMIT="$(git -C "$TMP/repo" rev-parse --short HEAD)"
ORIGEM="$TMP/repo/$CAMINHO"
[ -f "$ORIGEM/SKILL.md" ] || { echo "Erro: $CAMINHO/SKILL.md não encontrado no repositório."; exit 1; }

RELATORIO="$RAIZ/auditorias/${NOME}_${COMMIT}.md"
mkdir -p "$RAIZ/auditorias"
echo "→ Auditando '$NOME' (commit $COMMIT)..."
set +e
python3 "$AUDITOR" "$ORIGEM" --md "$RELATORIO" > /dev/null
STATUS=$?
set -e

case $STATUS in
  0) echo "✅ Veredito: OK" ;;
  1) echo "⚠️  Veredito: REVISAR — achados que precisam da sua avaliação:"
     grep -E '^\- \*\*(CRÍTICO|ALTO|MÉDIO)' "$RELATORIO" | sed 's/^/   /'
     echo "   Relatório completo: $RELATORIO"
     read -r -p "   Você leu os achados e quer instalar mesmo assim? [s/N] " r
     [ "$r" = "s" ] || { echo "Instalação cancelada."; exit 1; } ;;
  2) echo "⛔ Veredito: BLOQUEAR — achados críticos:"
     grep -E '^\- \*\*CRÍTICO' "$RELATORIO" | sed 's/^/   /'
     echo "   Relatório completo: $RELATORIO"
     if [ $FORCAR -ne 1 ]; then echo "Instalação bloqueada. (Use --forcar só se tiver certeza absoluta.)"; exit 2; fi
     read -r -p "   ATENÇÃO: instalar skill bloqueada? Digite INSTALAR para confirmar: " r
     [ "$r" = "INSTALAR" ] || { echo "Instalação cancelada."; exit 2; } ;;
  *) echo "Erro na auditoria."; exit 1 ;;
esac

echo "   Dica: mesmo com OK, leia o SKILL.md e os scripts — a varredura não pega tudo."

mkdir -p "$DESTINO_BASE"
if [ -d "$DESTINO_BASE/$NOME" ]; then
  read -r -p "A skill '$NOME' já existe em $DESTINO_BASE. Sobrescrever? [s/N] " r
  [ "$r" = "s" ] || exit 0
  rm -rf "$DESTINO_BASE/$NOME"
fi
cp -r "$ORIGEM" "$DESTINO_BASE/$NOME"

echo "✅ Skill '$NOME' instalada em $DESTINO_BASE/$NOME (commit $COMMIT)"
echo "   Registre no CLAUDE.md: | $NOME | $REPO @ $COMMIT | <quando usar> |"
echo "   Reinicie o Claude Code para ela ser carregada."
