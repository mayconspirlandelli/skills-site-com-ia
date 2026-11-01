# Imagem do site com Nano Banana (opcional)

No passo 5, a skill `gerar-mockup` escreve um prompt e gera a imagem do site. Com o servidor MCP do
**Nano Banana** (modelos de imagem do Google Gemini) configurado, a imagem sai em PNG, mais criativa.
Sem ele, o Claude desenha um mockup em SVG — o fluxo funciona dos dois jeitos.

O servidor foi auditado: veja `auditorias/nanobanana-mcp-server_062b9c6.md`.

## Requisitos

- [uv](https://docs.astral.sh/uv/) (traz o `uvx`) e Python 3.11+.
- Uma chave da API do Gemini, criada no [Google AI Studio](https://aistudio.google.com/apikey).
  A geração de imagens pode ter custo na sua conta Google — confira os limites do seu plano.

## 1. Guarde a chave numa variável de ambiente

Nunca coloque a chave num arquivo versionado.

- **Windows:** Configurações → Sistema → Sobre → Configurações avançadas do sistema → Variáveis de
  ambiente → Nova variável de usuário `GEMINI_API_KEY`. Abra um terminal novo depois.
- **macOS/Linux:** acrescente `export GEMINI_API_KEY="sua-chave"` ao `~/.bashrc` ou `~/.zshrc`.

## 2. Adicione o servidor ao Claude Code

Na pasta do projeto, instalando **o commit auditado** (não a versão do PyPI):

```bash
claude mcp add nanobanana --scope local -e IMAGE_OUTPUT_DIR="$(pwd)/etapas/03_mockup" -- uvx --from git+https://github.com/zhongweili/nanobanana-mcp-server@062b9c6fc95efbc457563fa14ff5ea5cb66f4d06 nanobanana-mcp-server
```

- `--scope local` grava a configuração só na sua máquina, fora do git.
- `IMAGE_OUTPUT_DIR` faz as imagens caírem direto em `etapas/03_mockup/`.
- O servidor lê `GEMINI_API_KEY` do ambiente. Se ele reclamar que não achou a chave, remova
  (`claude mcp remove nanobanana`) e adicione de novo com `-e GEMINI_API_KEY="$GEMINI_API_KEY"`
  antes do `--` (a chave fica no seu `~/.claude.json`, local).

Reinicie o Claude Code e confira com `claude mcp list`.

## Restrições de segurança (já aplicadas no template)

- A ferramenta `upload_file` do servidor está **bloqueada** em `.claude/settings.json`: ela aceita
  qualquer arquivo e poderia enviar, por exemplo, um `.env` para o Google. O fluxo não precisa dela.
- **Nunca** defina `GEMINI_BASE_URL`: ela redireciona a chave da API para outro endereço.
- Para atualizar o servidor para um commit mais novo, audite de novo antes.
