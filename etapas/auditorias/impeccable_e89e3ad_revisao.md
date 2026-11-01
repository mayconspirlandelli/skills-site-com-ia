# Revisão manual da skill `impeccable`

- **Repositório:** https://github.com/pbakaus/impeccable (≈99 mil estrelas, Apache-2.0)
- **Caminho instalado:** `.claude/skills/impeccable` (o repositório traz uma variante por ferramenta; esta é a do Claude Code)
- **Commit revisado:** `e89e3ad` (versão 4.8.0)
- **Data:** 2026-11-02
- **Veredito automático:** ⛔ BLOQUEAR · **Decisão do usuário:** ✅ incluir completa, como obrigatória, aceitando o binário

## O que a skill faz

Guias de design de interface (crítica, auditoria, polimento, tipografia, cor, layout, movimento, acessibilidade, design system) e um motor de linha de comando com detector de problemas de design, modo "live" de variantes no navegador e hooks pós-edição.

## Achados

| Item | Avaliação |
|------|-----------|
| 8 alertas CRÍTICOS em `reference/*.md` | Falsos positivos: frases como "não diga ao usuário que precisa invocar `craft`", "não mostre os achados antes da síntese", "não desative a segurança do navegador". |
| `modern-screenshot.umd.js` "ofuscado" | Biblioteca de terceiros minificada (captura de tela no navegador), não ofuscação maliciosa. |
| Rede nos scripts JS | Só `http://localhost` (o servidor local da própria skill). Sem telemetria. |
| **Binário do motor** | O launcher `scripts/impeccable` baixa da página de releases do GitHub um binário compilado (Go) para o sistema e o executa, guardando em cache. Há `engine-checksums.txt` no commit (o checksum fixa o binário), mas **binário não é auditável pela leitura**. |
| **Hooks** | O comando `hooks` grava hooks pós-edição em `.claude/settings.local.json` (ou `~/.claude/settings.json`). Pede consentimento antes. |
| **Modo live** | Injeta um script na página aberta no navegador e orienta a IA a seguir o campo `_instructions` devolvido pela própria ferramenta. Restrito a servidores locais. |

## Condições de uso no projeto

1. Instalar sempre o commit fixo `e89e3ad` (o `setup-skills.sh` faz isso), o que também fixa a versão e o checksum do binário.
2. Exceção registrada em `auditorias/excecoes.txt`; o script ainda pede confirmação na instalação.
3. Ativar os hooks só quando o usuário pedir (o comando pede consentimento).
4. Atualizar para outro commit exige nova revisão.
