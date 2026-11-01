# Auditoria do servidor MCP `nanobanana-mcp-server`

- **Repositório:** https://github.com/zhongweili/nanobanana-mcp-server
- **Commit auditado:** `062b9c6fc95efbc457563fa14ff5ea5cb66f4d06` (versão 0.4.6, licença MIT)
- **Data:** 2026-11-02
- **Método:** leitura manual do código em pasta temporária, sem executar nada (~8 mil linhas de Python)
- **Veredito:** ⚠️ **REVISAR → aprovado com restrições** (abaixo)

## O que o servidor faz

Gera e edita imagens com os modelos de imagem do Google Gemini ("Nano Banana"). Ferramentas expostas:
`generate_image`, `upload_file`, `output_stats` e `maintenance`.

## Achados

| Item | Resultado |
|------|-----------|
| Rede | Só pelo SDK oficial `google-genai` (APIs do Google). Nenhuma outra URL, nenhum `requests`/`httpx`/`socket` direto. |
| Execução de comandos | Nenhum `subprocess`, `os.system`, `eval`, `exec` ou `pickle`. |
| Telemetria | Nenhuma. ("tracker" no código é só progresso interno.) |
| Variáveis de ambiente | Lê `GEMINI_API_KEY`/`GOOGLE_API_KEY`, configurações do próprio servidor e `GEMINI_BASE_URL`. |
| `GEMINI_BASE_URL` | Se definida, a chave da API passa a ser enviada para outro endereço. **Nunca defina.** |
| Imagens de entrada | Validadas: só arquivos com extensão de imagem. |
| `maintenance` | Apaga imagens antigas, mas só dentro da pasta de saída (`IMAGE_OUTPUT_DIR`). Aceitável. |
| **`upload_file`** | **Aceita qualquer arquivo** (não só imagens) e envia para a API de arquivos do Google. A validação só barra `..` e caminhos iniciados por `/` — caminhos do Windows (`C:\...`) passam. Uma instrução maliciosa vinda de uma página poderia levar a IA a enviar um `.env`. |
| Transporte | `stdio` por padrão; no modo HTTP escuta só em `127.0.0.1`. |
| Pacote no PyPI | O autor é o mesmo, mas o link do repositório no PyPI dá 404 — não há como garantir que o pacote publicado é igual ao código lido. |

## Restrições para uso neste projeto

1. **Instalar a partir do commit auditado no GitHub**, não do PyPI:
   `uvx --from git+https://github.com/zhongweili/nanobanana-mcp-server@062b9c6fc95efbc457563fa14ff5ea5cb66f4d06 nanobanana-mcp-server`
2. **Bloquear a ferramenta `upload_file`** — feito em `.claude/settings.json` (`permissions.deny`). O fluxo não precisa dela.
3. **Nunca definir `GEMINI_BASE_URL`.**
4. **Chave da API fora do git:** variável de ambiente do sistema; nunca em arquivo versionado.
5. Atualizou o commit? Audite de novo.

Guia de configuração: `docs/nano-banana.md`.
