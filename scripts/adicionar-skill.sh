#!/usr/bin/env bash
# Audita e copia uma skill de um repositório Git para .claude/skills/ deste projeto.
#
# Uso:
#   ./scripts/adicionar-skill.sh <url-do-repo> <caminho-ou-nome-da-skill> [--commit <sha>] [--global] [--forcar]
#
# Exemplos:
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills skills/frontend-design
#   ./scripts/adicionar-skill.sh https://github.com/anthropics/skills frontend-design
#
# --commit  instala exatamente esse commit (o que foi auditado), não o mais recente
# --global  instala em ~/.claude/skills/ (vale para todos os projetos)
# --forcar  permite instalar mesmo com veredito BLOQUEAR (não recomendado)
#
# Exceções revisadas: etapas/auditorias/excecoes.txt lista "<skill> <commit> <motivo>" de skills com
# veredito REVISAR/BLOQUEAR aprovadas pelo usuário após revisão manual. Para elas, o script mostra
# os achados e pede confirmação em vez de bloquear.
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
[ -f "$AUDITOR" ] || { echo "Erro: auditor não encontrado em $AUDITOR"; exit 1; }

NOME="$(basename "$CAMINHO")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "→ Baixando $REPO${FIXO:+ @ $FIXO} (pasta temporária, nada é instalado ainda)..."
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
  # Aceita só o nome da skill: procura uma pasta com esse nome ou um SKILL.md com "name: <nome>".
  ACHADO="$(find "$TMP/repo" -path "*/$NOME/SKILL.md" -not -path "*/.git/*" | head -n 1 || true)"
  [ -n "$ACHADO" ] || ACHADO="$(grep -rlx --include=SKILL.md "name: *$NOME *" "$TMP/repo" | head -n 1 || true)"
  [ -n "$ACHADO" ] || { echo "Erro: skill '$CAMINHO' não encontrada no repositório."; exit 1; }
  ORIGEM="$(dirname "$ACHADO")"
  echo "→ Skill encontrada em ${ORIGEM#$TMP/repo/}"
fi

RELATORIO="$RAIZ/etapas/auditorias/${NOME}_${COMMIT}.md"
mkdir -p "$RAIZ/etapas/auditorias"
echo "→ Auditando '$NOME' (commit $COMMIT)..."
# Lê o veredito impresso (não o código de saída), para um erro do Python nunca virar "REVISAR".
VEREDITO="$(python3 "$AUDITOR" "$ORIGEM" --md "$RELATORIO" --silencioso | tail -n 1 | tr -d '[:space:]' || true)"

EXCECAO="$(grep -E "^$NOME $COMMIT " "$RAIZ/etapas/auditorias/excecoes.txt" 2>/dev/null | head -n 1 || true)"
if [ -n "$EXCECAO" ] && { [ "$VEREDITO" = "REVISAR" ] || [ "$VEREDITO" = "BLOQUEAR" ]; }; then
  echo "⚠️  Veredito: $VEREDITO — com exceção revisada registrada em etapas/auditorias/excecoes.txt:"
  echo "   ${EXCECAO#"$NOME $COMMIT "}"
  grep -E '^\- \*\*(CRÍTICO|ALTO)' "$RELATORIO" | sed 's/^/   /' | head -n 12
  echo "   Relatório completo: $RELATORIO"
  read -r -p "   Instalar com base na revisão registrada? [s/N] " r
  [ "$r" = "s" ] || { echo "Instalação cancelada."; exit 1; }
  VEREDITO="EXCECAO"
fi

case $VEREDITO in
  EXCECAO) ;;
  OK) echo "✅ Veredito: OK" ;;
  REVISAR) echo "⚠️  Veredito: REVISAR — achados que precisam da sua avaliação:"
     grep -E '^\- \*\*(CRÍTICO|ALTO|MÉDIO)' "$RELATORIO" | sed 's/^/   /'
     echo "   Relatório completo: $RELATORIO"
     read -r -p "   Você leu os achados e quer instalar mesmo assim? [s/N] " r
     [ "$r" = "s" ] || { echo "Instalação cancelada."; exit 1; } ;;
  BLOQUEAR) echo "⛔ Veredito: BLOQUEAR — achados críticos:"
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
