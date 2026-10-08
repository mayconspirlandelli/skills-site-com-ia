#!/usr/bin/env python3
"""
Auditoria estática de uma skill de terceiros ANTES de instalar.

Uso:
  python auditar_skill.py <pasta-da-skill> [--json relatorio.json] [--md relatorio.md]

Não executa nada da skill: apenas lê os arquivos e procura padrões de risco.

Códigos de saída:
  0 = nenhum achado relevante (OK)
  1 = achados que exigem revisão humana (REVISAR)
  2 = achados críticos (BLOQUEAR)
  3 = erro de uso (pasta inválida, sem SKILL.md)
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

CRITICO, ALTO, MEDIO, INFO = "CRÍTICO", "ALTO", "MÉDIO", "INFO"
PESO = {CRITICO: 3, ALTO: 2, MEDIO: 1, INFO: 0}

EXT_CODIGO = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl",
              ".php", ".ps1", ".bat", ".cmd", ".go", ".rs", ".lua"}
EXT_TEXTO = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".xml", ".csv", ".ini", ".cfg"}
EXT_BINARIO_SUSPEITO = {".exe", ".dll", ".so", ".dylib", ".bin", ".elf", ".jar", ".pyc", ".class", ".app", ".msi", ".deb", ".dmg"}
LIMITE_ARQUIVO = 2_000_000  # 2 MB

# (severidade, regex, explicação) — aplicados a arquivos de código E texto
REGRAS_CODIGO = [
    # Execução remota / download-and-run
    (CRITICO, r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b", "Baixa e executa código remoto (curl | sh)."),
    (CRITICO, r"(curl|wget|Invoke-WebRequest|iwr)[^\n]*(\||;|&&)\s*(python|node|perl|ruby|iex|Invoke-Expression)", "Baixa e executa código remoto."),
    (CRITICO, r"/dev/tcp/|\bnc\b[^\n]*\s-e\s|\bncat\b[^\n]*--exec|socat[^\n]*exec:|bash\s+-i\s+>&", "Padrão de reverse shell."),
    # Obfuscação
    (CRITICO, r"(exec|eval)\s*\(\s*(base64|b64decode|codecs\.decode|bytes\.fromhex|zlib\.decompress|marshal\.loads)", "Executa código ofuscado (eval/exec de conteúdo decodificado)."),
    (CRITICO, r"base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh", "Decodifica base64 e executa no shell."),
    (CRITICO, r"\batob\s*\([^)]*\)[^\n]*(eval|Function\s*\()|(eval|new\s+Function)\s*\(\s*atob", "Executa JavaScript ofuscado."),
    # Credenciais e dados sensíveis
    (CRITICO, r"(~|\$HOME|HOME\"?\]?|expanduser\([\"']~)[/\"' +]*\.(ssh|aws|gnupg|kube|docker/config|netrc|npmrc|pypirc|git-credentials)", "Acessa pasta/arquivo de credenciais do usuário."),
    (CRITICO, r"id_rsa|id_ed25519|\.pem\b|Login Data|Cookies\.binarycookies|keychain|Local State|wallet\.dat", "Referência a chaves privadas, cookies ou cofres de senha."),
    (ALTO, r"(os\.environ|process\.env|getenv|\$ENV)[^\n]{0,40}(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE|CREDENTIAL)", "Lê variáveis de ambiente com segredos."),
    (ALTO, r"(open|read_text|readFileSync|cat)\s*\(?[^\n]*\.env\b", "Lê arquivo .env."),
    # Persistência / alteração do sistema ou do próprio Claude
    (CRITICO, r"\.(bashrc|zshrc|bash_profile|profile|zprofile)\b[^\n]*(>>|write|append|open\([^)]*[\"']a)", "Altera arquivos de inicialização do shell (persistência)."),
    (CRITICO, r"crontab\s|/etc/cron|launchctl\s+load|LaunchAgents|systemctl\s+enable|schtasks|HKEY_|reg\s+add", "Cria tarefa agendada/serviço (persistência)."),
    (CRITICO, r"\.claude/(settings(\.local)?\.json|CLAUDE\.md)|~/\.claude\b|CLAUDE\.md[^\n]*(>>|write)", "Mexe na configuração do Claude/Claude Code."),
    (ALTO, r"\.claude/skills|\.claude/plugins", "Mexe em outras skills/plugins instalados."),
    (CRITICO, r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME|\*|\.\.)(\s|$|/)|shutil\.rmtree\(\s*[\"']?(/|~)|Remove-Item[^\n]*-Recurse[^\n]*(C:\\|~)", "Apagamento recursivo perigoso."),
    (ALTO, r"\bsudo\b|chmod\s+(-R\s+)?777|chown\s+-R|Set-ExecutionPolicy", "Eleva privilégios ou afrouxa permissões."),
    (ALTO, r"git\s+(push|config\s+--global)|gh\s+(auth|repo\s+delete|secret)", "Executa ações git com efeito externo."),
    # Rede
    (ALTO, r"\b(requests|httpx|aiohttp)\.(post|put|patch)|urllib\.request\.urlopen\([^)]*data=|fetch\([^)]*method\s*:\s*[\"'](POST|PUT)|curl[^\n]*\s(-d|--data|-F|--upload-file|-T)\s|Invoke-RestMethod[^\n]*-Method\s+Post", "Envia dados para a internet (possível exfiltração)."),
    (MEDIO, r"\b(requests|httpx|aiohttp)\.get|urllib\.request|urlopen|\bfetch\(|axios|\bcurl\s|\bwget\s|http\.client|socket\.socket|websocket", "Faz requisições de rede."),
    (ALTO, r"webhook\.site|requestbin|pipedream\.net|ngrok\.(io|app)|interact\.sh|burpcollaborator|pastebin\.com|transfer\.sh|discord(app)?\.com/api/webhooks|api\.telegram\.org/bot", "Destino típico de exfiltração/coleta de dados."),
    # Execução de processos / instalação dinâmica
    (MEDIO, r"subprocess\.|os\.system\(|os\.popen\(|child_process|execSync|spawn\(|Runtime\.getRuntime", "Executa comandos do sistema."),
    (MEDIO, r"\b(eval|exec)\s*\(|new\s+Function\s*\(|__import__\(", "Execução dinâmica de código."),
    (MEDIO, r"(pip|pip3|npm|yarn|pnpm|gem|cargo)\s+(install|add|i)\s", "Instala pacotes (verifique quais e de onde)."),
    (INFO, r"--break-system-packages", "Instala pacotes no Python do sistema."),
    # Mineração
    (CRITICO, r"xmrig|stratum\+tcp|coinhive|cryptonight|minexmr", "Indício de mineração de criptomoeda."),
]

# Aplicadas só a arquivos de texto/instruções (SKILL.md, references, etc.)
REGRAS_INSTRUCOES = [
    (CRITICO, r"ignor(e|ar|e todas as|e all|e previous|e the above|e your)[^\n]{0,40}(instru|instruc|rules|regras|previous|anteriores|system)", "Tentativa de prompt injection (ignorar instruções)."),
    (CRITICO, r"(do not|don't|never|não|nunca)\s+(tell|inform|mention|reveal|show|avis|cont|mostr|mencion|inform)[^\n]{0,30}(user|usuário|usuario|human|humano)", "Instrui a esconder ações do usuário."),
    (ALTO, r"(without|sem)\s+(asking|ask|confirm|permission|perguntar|pedir|confirma|permiss)", "Instrui a agir sem confirmação do usuário."),
    (ALTO, r"\b(silently|secretly|quietly|in the background|silenciosamente|em segredo|escondid|sem que o usu)", "Instrui a agir de forma oculta."),
    (CRITICO, r"(disable|bypass|override|desativ|contorn|burl)[^\n]{0,30}(safety|security|guardrail|seguran|proteç|restriç|permission|permiss|sandbox)", "Instrui a desativar proteções."),
    (ALTO, r"(system prompt|prompt do sistema|you are now|a partir de agora você é|new instructions|novas instruções|developer mode|DAN\b)", "Tenta redefinir o papel/instruções da IA."),
    (ALTO, r"\b(send|upload|post|envie|enviar|envia|mande|mandar|exporte|exportar)\b[^\n]{0,40}(api[ _-]?key|token|password|senha|credential|credencia|\.env\b|ssh|cookie)", "Instrui a enviar dados sensíveis."),
    (ALTO, r"(always|sempre)\s+(use|use this|trigger|ative|acione|execute)[^\n]{0,30}(every|all|qualquer|toda|todas)", "Descrição/instrução forçando uso em qualquer tarefa."),
    (MEDIO, r"<!--[\s\S]{0,400}?(instru|ignore|claude|assistant|IA\b|AI\b)[\s\S]{0,400}?-->", "Comentário HTML oculto com instruções para a IA."),
]

RE_URL = re.compile(r"https?://[^\s)\"'<>\]]+")
RE_BASE64_LONGO = re.compile(r"[A-Za-z0-9+/]{200,}={0,2}")
RE_HEX_LONGO = re.compile(r"(\\x[0-9a-fA-F]{2}){40,}")
CHARS_INVISIVEIS = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\u00ad"}
CHARS_BIDI = {"\u202a", "\u202b", "\u202c", "\u202d", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069"}
DOMINIOS_CONFIAVEIS = ("github.com", "githubusercontent.com", "anthropic.com", "claude.com", "claude.ai",
                       "python.org", "pypi.org", "npmjs.com", "mozilla.org", "w3.org", "google.com",
                       "googleapis.com", "cdnjs.cloudflare.com", "jsdelivr.net", "wikipedia.org")


def eh_binario(caminho: Path) -> bool:
    try:
        return b"\x00" in caminho.read_bytes()[:4096]
    except OSError:
        return False


def linha_de(texto: str, pos: int) -> int:
    return texto.count("\n", 0, pos) + 1


def trecho(texto: str, pos: int) -> str:
    ini = texto.rfind("\n", 0, pos) + 1
    fim = texto.find("\n", pos)
    return texto[ini: fim if fim != -1 else None].strip()[:160]


def ler_frontmatter(texto: str):
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    if not m:
        return None
    dados = {}
    for linha in m.group(1).splitlines():
        if ":" in linha and not linha.startswith(" "):
            k, v = linha.split(":", 1)
            dados[k.strip()] = v.strip()
    return dados


def auditar(pasta: Path):
    achados, urls, arquivos = [], {}, []
    raiz = pasta.resolve()

    def add(sev, arq, linha, motivo, evid=""):
        achados.append({"severidade": sev, "arquivo": arq, "linha": linha, "motivo": motivo, "evidencia": evid})

    skill_md = pasta / "SKILL.md"
    if not skill_md.is_file():
        return None

    fm = ler_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
    if fm is None:
        add(ALTO, "SKILL.md", 1, "SKILL.md sem frontmatter YAML (name/description).")
    else:
        if not fm.get("name") or not fm.get("description"):
            add(MEDIO, "SKILL.md", 1, "Frontmatter sem name ou description.")
        extras = set(fm) - {"name", "description", "license", "compatibility", "allowed-tools", "metadata", "version"}
        if extras:
            add(INFO, "SKILL.md", 1, f"Campos extras no frontmatter: {', '.join(sorted(extras))}.")
        if "allowed-tools" in fm:
            add(MEDIO, "SKILL.md", 1, f"Define allowed-tools: {fm['allowed-tools']} — confira se faz sentido para o propósito.")

    for dirpath, dirnames, filenames in os.walk(pasta, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for nome in filenames + [d for d in dirnames if (Path(dirpath) / d).is_symlink()]:
            p = Path(dirpath) / nome
            rel = str(p.relative_to(pasta))
            ext = p.suffix.lower()

            if p.is_symlink():
                alvo = os.path.realpath(p)
                if not alvo.startswith(str(raiz)):
                    add(CRITICO, rel, 0, f"Link simbólico apontando para fora da skill: {alvo}")
                else:
                    add(INFO, rel, 0, "Link simbólico interno.")
                continue

            try:
                tamanho = p.stat().st_size
            except OSError:
                continue
            arquivos.append({"arquivo": rel, "bytes": tamanho})

            if nome.startswith(".") and nome not in (".gitignore", ".gitkeep"):
                add(MEDIO, rel, 0, "Arquivo oculto.")
            if ext in EXT_BINARIO_SUSPEITO:
                add(CRITICO, rel, 0, f"Binário executável/compilado ({ext}) — não é possível revisar o conteúdo.")
                continue
            # No Windows todo arquivo parece executável; o bit só tem sentido em sistemas POSIX.
            if os.name != "nt" and os.access(p, os.X_OK) and ext not in EXT_CODIGO:
                add(MEDIO, rel, 0, "Arquivo com permissão de execução sem extensão de script conhecida.")
            if tamanho > LIMITE_ARQUIVO:
                add(MEDIO, rel, 0, f"Arquivo grande ({tamanho:,} bytes) — revise manualmente.")
                continue
            if eh_binario(p):
                if ext not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".zip"}:
                    add(ALTO, rel, 0, "Arquivo binário desconhecido.")
                elif ext == ".zip":
                    add(ALTO, rel, 0, "Arquivo compactado dentro da skill — conteúdo não auditado.")
                continue

            texto = p.read_text(encoding="utf-8", errors="replace")
            eh_codigo = ext in EXT_CODIGO or texto.startswith("#!")
            eh_instrucao = ext in EXT_TEXTO or nome == "SKILL.md"

            # Blocos de código dentro de markdown também são verificados com regras de código
            if eh_codigo or eh_instrucao:
                for sev, rx, motivo in REGRAS_CODIGO:
                    for m in re.finditer(rx, texto, re.I):
                        s = sev
                        if eh_instrucao and not eh_codigo and sev == CRITICO and "remoto" not in motivo:
                            s = ALTO  # em documentação pode ser só menção; ainda exige revisão
                        add(s, rel, linha_de(texto, m.start()), motivo, trecho(texto, m.start()))
                        break  # um achado por regra por arquivo
            if eh_instrucao:
                for sev, rx, motivo in REGRAS_INSTRUCOES:
                    m = re.search(rx, texto, re.I)
                    if m:
                        add(sev, rel, linha_de(texto, m.start()), motivo, trecho(texto, m.start()))

            invis = [c for c in texto if c in CHARS_INVISIVEIS and not (c == "\ufeff" and texto.startswith(c))]
            if invis:
                add(ALTO, rel, 0, f"{len(invis)} caractere(s) invisível(is) — podem esconder instruções.")
            bidi = [c for c in texto if c in CHARS_BIDI]
            if bidi:
                add(CRITICO, rel, 0, "Caracteres de controle bidirecional (ataque 'Trojan Source').")
            tags = [c for c in texto if 0xE0000 <= ord(c) <= 0xE007F]
            if tags:
                add(CRITICO, rel, 0, "Caracteres Unicode 'tag' invisíveis — técnica usada para esconder prompt injection.")
            for m in RE_BASE64_LONGO.finditer(texto):
                add(ALTO, rel, linha_de(texto, m.start()), "Bloco longo em base64 (possível código ofuscado).", m.group(0)[:60] + "…")
                break
            if RE_HEX_LONGO.search(texto):
                add(ALTO, rel, 0, "Sequência hexadecimal longa (possível código ofuscado).")

            for u in RE_URL.findall(texto):
                u = u.rstrip(".,;:`")
                urls.setdefault(u, set()).add(rel)

    externas = {}
    for u, arqs in urls.items():
        dominio = re.sub(r"^https?://", "", u).split("/")[0].lower()
        if not any(dominio == d or dominio.endswith("." + d) for d in DOMINIOS_CONFIAVEIS):
            externas[u] = sorted(arqs)
    if externas:
        add(INFO, "-", 0, f"{len(externas)} URL(s) de domínios não reconhecidos — confira na lista de URLs.")

    maior = max((PESO[a["severidade"]] for a in achados), default=0)
    veredito = "BLOQUEAR" if maior >= 3 else "REVISAR" if maior >= 1 else "OK"
    ordem = {CRITICO: 0, ALTO: 1, MEDIO: 2, INFO: 3}
    achados.sort(key=lambda a: (ordem[a["severidade"]], a["arquivo"], a["linha"]))
    return {
        "skill": fm.get("name") if fm else pasta.name,
        "descricao": (fm or {}).get("description", ""),
        "pasta": str(pasta),
        "veredito": veredito,
        "resumo": {s: sum(1 for a in achados if a["severidade"] == s) for s in (CRITICO, ALTO, MEDIO, INFO)},
        "arquivos": arquivos,
        "urls_externas": externas,
        "urls_todas": sorted(urls),
        "achados": achados,
    }


def para_markdown(r):
    icone = {"OK": "✅", "REVISAR": "⚠️", "BLOQUEAR": "⛔"}[r["veredito"]]
    out = [f"# Auditoria da skill `{r['skill']}`", "",
           f"**Veredito automático: {icone} {r['veredito']}**", "",
           f"Descrição declarada: {r['descricao'] or '(vazia)'}", "",
           "| Crítico | Alto | Médio | Info |", "|---|---|---|---|",
           "| " + " | ".join(str(r["resumo"][s]) for s in (CRITICO, ALTO, MEDIO, INFO)) + " |", "",
           "## Arquivos", ""]
    out += [f"- `{a['arquivo']}` ({a['bytes']:,} bytes)" for a in r["arquivos"]]
    out += ["", "## Achados", ""]
    if not r["achados"]:
        out.append("Nenhum.")
    for a in r["achados"]:
        loc = f"{a['arquivo']}:{a['linha']}" if a["linha"] else a["arquivo"]
        out.append(f"- **{a['severidade']}** `{loc}` — {a['motivo']}")
        if a["evidencia"]:
            out.append(f"  - `{a['evidencia'].replace('`', 'ˋ')}`")
    if r["urls_externas"]:
        out += ["", "## URLs de domínios não reconhecidos", ""]
        out += [f"- {u} (em {', '.join(f)})" for u, f in r["urls_externas"].items()]
    out += ["", "> Auditoria estática automática: reduz o risco, mas não garante segurança. "
            "Leia o SKILL.md e todos os scripts antes de instalar."]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Auditoria estática de skill de terceiros.")
    ap.add_argument("pasta")
    ap.add_argument("--json")
    ap.add_argument("--md")
    ap.add_argument("--silencioso", action="store_true", help="imprime só o veredito")
    a = ap.parse_args()
    # Evita UnicodeEncodeError em consoles Windows (cp1252) ao imprimir o relatório.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    pasta = Path(a.pasta)
    if not pasta.is_dir():
        print(f"Erro: pasta não encontrada: {pasta}", file=sys.stderr)
        sys.exit(3)
    r = auditar(pasta)
    if r is None:
        print(f"Erro: {pasta}/SKILL.md não encontrado — isto não é uma skill.", file=sys.stderr)
        sys.exit(3)

    md = para_markdown(r)
    if a.json:
        Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.md:
        Path(a.md).write_text(md, encoding="utf-8")
    print(r["veredito"] if a.silencioso else md)
    sys.exit({"OK": 0, "REVISAR": 1, "BLOQUEAR": 2}[r["veredito"]])


if __name__ == "__main__":
    main()
