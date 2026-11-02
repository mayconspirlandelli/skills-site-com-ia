#!/usr/bin/env python3
"""
Static audit of a third-party skill BEFORE installing.

Usage:
  python auditar_skill.py <skill-folder> [--json report.json] [--md report.md]

Runs nothing from the skill: only reads the files and looks for risk patterns.

Exit codes:
  0 = no relevant findings (OK)
  1 = findings that need human review (REVIEW)
  2 = critical findings (BLOCK)
  3 = usage error (invalid folder, no SKILL.md)
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

CRITICO, ALTO, MEDIO, INFO = "CRITICAL", "HIGH", "MEDIUM", "INFO"
PESO = {CRITICO: 3, ALTO: 2, MEDIO: 1, INFO: 0}

EXT_CODIGO = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl",
              ".php", ".ps1", ".bat", ".cmd", ".go", ".rs", ".lua"}
EXT_TEXTO = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".xml", ".csv", ".ini", ".cfg"}
EXT_BINARIO_SUSPEITO = {".exe", ".dll", ".so", ".dylib", ".bin", ".elf", ".jar", ".pyc", ".class", ".app", ".msi", ".deb", ".dmg"}
LIMITE_ARQUIVO = 2_000_000  # 2 MB

# (severity, regex, explanation) — applied to code AND text files
REGRAS_CODIGO = [
    # Remote execution / download-and-run
    (CRITICO, r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b", "Downloads and runs remote code (curl | sh)."),
    (CRITICO, r"(curl|wget|Invoke-WebRequest|iwr)[^\n]*(\||;|&&)\s*(python|node|perl|ruby|iex|Invoke-Expression)", "Downloads and runs remote code."),
    (CRITICO, r"/dev/tcp/|\bnc\b[^\n]*\s-e\s|\bncat\b[^\n]*--exec|socat[^\n]*exec:|bash\s+-i\s+>&", "Reverse shell pattern."),
    # Obfuscation
    (CRITICO, r"(exec|eval)\s*\(\s*(base64|b64decode|codecs\.decode|bytes\.fromhex|zlib\.decompress|marshal\.loads)", "Runs obfuscated code (eval/exec of decoded content)."),
    (CRITICO, r"base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh", "Decodes base64 and runs it in the shell."),
    (CRITICO, r"\batob\s*\([^)]*\)[^\n]*(eval|Function\s*\()|(eval|new\s+Function)\s*\(\s*atob", "Runs obfuscated JavaScript."),
    # Credentials and sensitive data
    (CRITICO, r"(~|\$HOME|HOME\"?\]?|expanduser\([\"']~)[/\"' +]*\.(ssh|aws|gnupg|kube|docker/config|netrc|npmrc|pypirc|git-credentials)", "Accesses the user's credentials folder/file."),
    (CRITICO, r"id_rsa|id_ed25519|\.pem\b|Login Data|Cookies\.binarycookies|keychain|Local State|wallet\.dat", "Reference to private keys, cookies or password vaults."),
    (ALTO, r"(os\.environ|process\.env|getenv|\$ENV)[^\n]{0,40}(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE|CREDENTIAL)", "Reads environment variables with secrets."),
    (ALTO, r"(open|read_text|readFileSync|cat)\s*\(?[^\n]*\.env\b", "Reads a .env file."),
    # Persistence / changes to the system or to Claude itself
    (CRITICO, r"\.(bashrc|zshrc|bash_profile|profile|zprofile)\b[^\n]*(>>|write|append|open\([^)]*[\"']a)", "Changes shell startup files (persistence)."),
    (CRITICO, r"crontab\s|/etc/cron|launchctl\s+load|LaunchAgents|systemctl\s+enable|schtasks|HKEY_|reg\s+add", "Creates a scheduled task/service (persistence)."),
    (CRITICO, r"\.claude/(settings(\.local)?\.json|CLAUDE\.md)|~/\.claude\b|CLAUDE\.md[^\n]*(>>|write)", "Touches the Claude/Claude Code configuration."),
    (ALTO, r"\.claude/skills|\.claude/plugins", "Touches other installed skills/plugins."),
    (CRITICO, r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME|\*|\.\.)(\s|$|/)|shutil\.rmtree\(\s*[\"']?(/|~)|Remove-Item[^\n]*-Recurse[^\n]*(C:\\|~)", "Dangerous recursive deletion."),
    (ALTO, r"\bsudo\b|chmod\s+(-R\s+)?777|chown\s+-R|Set-ExecutionPolicy", "Elevates privileges or loosens permissions."),
    (ALTO, r"git\s+(push|config\s+--global)|gh\s+(auth|repo\s+delete|secret)", "Runs git actions with external effects."),
    # Network
    (ALTO, r"\b(requests|httpx|aiohttp)\.(post|put|patch)|urllib\.request\.urlopen\([^)]*data=|fetch\([^)]*method\s*:\s*[\"'](POST|PUT)|curl[^\n]*\s(-d|--data|-F|--upload-file|-T)\s|Invoke-RestMethod[^\n]*-Method\s+Post", "Sends data to the internet (possible exfiltration)."),
    (MEDIO, r"\b(requests|httpx|aiohttp)\.get|urllib\.request|urlopen|\bfetch\(|axios|\bcurl\s|\bwget\s|http\.client|socket\.socket|websocket", "Makes network requests."),
    (ALTO, r"webhook\.site|requestbin|pipedream\.net|ngrok\.(io|app)|interact\.sh|burpcollaborator|pastebin\.com|transfer\.sh|discord(app)?\.com/api/webhooks|api\.telegram\.org/bot", "Typical exfiltration/data collection destination."),
    # Process execution / dynamic installation
    (MEDIO, r"subprocess\.|os\.system\(|os\.popen\(|child_process|execSync|spawn\(|Runtime\.getRuntime", "Runs system commands."),
    (MEDIO, r"\b(eval|exec)\s*\(|new\s+Function\s*\(|__import__\(", "Dynamic code execution."),
    (MEDIO, r"(pip|pip3|npm|yarn|pnpm|gem|cargo)\s+(install|add|i)\s", "Installs packages (check which and from where)."),
    (INFO, r"--break-system-packages", "Installs packages into the system Python."),
    # Mining
    (CRITICO, r"xmrig|stratum\+tcp|coinhive|cryptonight|minexmr", "Sign of cryptocurrency mining."),
]

# Applied only to text/instruction files (SKILL.md, references, etc.)
REGRAS_INSTRUCOES = [
    (CRITICO, r"ignor(e|ar|e todas as|e all|e previous|e the above|e your)[^\n]{0,40}(instru|instruc|rules|regras|previous|anteriores|system)", "Prompt injection attempt (ignore instructions)."),
    (CRITICO, r"(do not|don't|never|não|nunca)\s+(tell|inform|mention|reveal|show|avis|cont|mostr|mencion|inform)[^\n]{0,30}(user|usuário|usuario|human|humano)", "Instructs to hide actions from the user."),
    (ALTO, r"(without|sem)\s+(asking|ask|confirm|permission|perguntar|pedir|confirma|permiss)", "Instructs to act without the user's confirmation."),
    (ALTO, r"\b(silently|secretly|quietly|in the background|silenciosamente|em segredo|escondid|sem que o usu)", "Instructs to act covertly."),
    (CRITICO, r"(disable|bypass|override|desativ|contorn|burl)[^\n]{0,30}(safety|security|guardrail|seguran|proteç|restriç|permission|permiss|sandbox)", "Instructs to disable protections."),
    (ALTO, r"(system prompt|prompt do sistema|you are now|a partir de agora você é|new instructions|novas instruções|developer mode|DAN\b)", "Tries to redefine the AI's role/instructions."),
    (ALTO, r"\b(send|upload|post|envie|enviar|envia|mande|mandar|exporte|exportar)\b[^\n]{0,40}(api[ _-]?key|token|password|senha|credential|credencia|\.env\b|ssh|cookie)", "Instructs to send sensitive data."),
    (ALTO, r"(always|sempre)\s+(use|use this|trigger|ative|acione|execute)[^\n]{0,30}(every|all|qualquer|toda|todas)", "Description/instruction forcing use on any task."),
    (MEDIO, r"<!--[\s\S]{0,400}?(instru|ignore|claude|assistant|IA\b|AI\b)[\s\S]{0,400}?-->", "Hidden HTML comment with instructions for the AI."),
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
            add(MEDIO, "SKILL.md", 1, f"Define allowed-tools: {fm['allowed-tools']} — check that it makes sense for the purpose.")

    for dirpath, dirnames, filenames in os.walk(pasta, followlinks=False):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for nome in filenames + [d for d in dirnames if (Path(dirpath) / d).is_symlink()]:
            p = Path(dirpath) / nome
            rel = str(p.relative_to(pasta))
            ext = p.suffix.lower()

            if p.is_symlink():
                alvo = os.path.realpath(p)
                if not alvo.startswith(str(raiz)):
                    add(CRITICO, rel, 0, f"Symlink pointing outside the skill: {alvo}")
                else:
                    add(INFO, rel, 0, "Internal symlink.")
                continue

            try:
                tamanho = p.stat().st_size
            except OSError:
                continue
            arquivos.append({"arquivo": rel, "bytes": tamanho})

            if nome.startswith(".") and nome not in (".gitignore", ".gitkeep"):
                add(MEDIO, rel, 0, "Arquivo oculto.")
            if ext in EXT_BINARIO_SUSPEITO:
                add(CRITICO, rel, 0, f"Executable/compiled binary ({ext}) — its content cannot be reviewed.")
                continue
            # On Windows every file looks executable; the bit only makes sense on POSIX systems.
            if os.name != "nt" and os.access(p, os.X_OK) and ext not in EXT_CODIGO:
                add(MEDIO, rel, 0, "File with execute permission and no known script extension.")
            if tamanho > LIMITE_ARQUIVO:
                add(MEDIO, rel, 0, f"Arquivo grande ({tamanho:,} bytes) — revise manualmente.")
                continue
            if eh_binario(p):
                if ext not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".zip"}:
                    add(ALTO, rel, 0, "Unknown binary file.")
                elif ext == ".zip":
                    add(ALTO, rel, 0, "Compressed file inside the skill — content not audited.")
                continue

            texto = p.read_text(encoding="utf-8", errors="replace")
            eh_codigo = ext in EXT_CODIGO or texto.startswith("#!")
            eh_instrucao = ext in EXT_TEXTO or nome == "SKILL.md"

            # Code blocks inside markdown are also checked with code rules
            if eh_codigo or eh_instrucao:
                for sev, rx, motivo in REGRAS_CODIGO:
                    for m in re.finditer(rx, texto, re.I):
                        s = sev
                        if eh_instrucao and not eh_codigo and sev == CRITICO and "remoto" not in motivo:
                            s = ALTO  # in documentation it may be just a mention; still needs review
                        add(s, rel, linha_de(texto, m.start()), motivo, trecho(texto, m.start()))
                        break  # one finding per rule per file
            if eh_instrucao:
                for sev, rx, motivo in REGRAS_INSTRUCOES:
                    m = re.search(rx, texto, re.I)
                    if m:
                        add(sev, rel, linha_de(texto, m.start()), motivo, trecho(texto, m.start()))

            invis = [c for c in texto if c in CHARS_INVISIVEIS and not (c == "\ufeff" and texto.startswith(c))]
            if invis:
                add(ALTO, rel, 0, f"{len(invis)} invisible character(s) — they can hide instructions.")
            bidi = [c for c in texto if c in CHARS_BIDI]
            if bidi:
                add(CRITICO, rel, 0, "Caracteres de controle bidirecional (ataque 'Trojan Source').")
            tags = [c for c in texto if 0xE0000 <= ord(c) <= 0xE007F]
            if tags:
                add(CRITICO, rel, 0, "Invisible Unicode 'tag' characters — a technique used to hide prompt injection.")
            for m in RE_BASE64_LONGO.finditer(texto):
                add(ALTO, rel, linha_de(texto, m.start()), "Long base64 block (possible obfuscated code).", m.group(0)[:60] + "…")
                break
            if RE_HEX_LONGO.search(texto):
                add(ALTO, rel, 0, "Long hexadecimal sequence (possible obfuscated code).")

            for u in RE_URL.findall(texto):
                u = u.rstrip(".,;:`")
                urls.setdefault(u, set()).add(rel)

    externas = {}
    for u, arqs in urls.items():
        dominio = re.sub(r"^https?://", "", u).split("/")[0].lower()
        if not any(dominio == d or dominio.endswith("." + d) for d in DOMINIOS_CONFIAVEIS):
            externas[u] = sorted(arqs)
    if externas:
        add(INFO, "-", 0, f"{len(externas)} URL(s) from unrecognized domains — check the URL list.")

    maior = max((PESO[a["severidade"]] for a in achados), default=0)
    veredito = "BLOCK" if maior >= 3 else "REVIEW" if maior >= 1 else "OK"
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
    icone = {"OK": "✅", "REVIEW": "⚠️", "BLOCK": "⛔"}[r["veredito"]]
    out = [f"# Audit of skill `{r['skill']}`", "",
           f"**Automatic verdict: {icone} {r['veredito']}**", "",
           f"Declared description: {r['descricao'] or '(empty)'}", "",
           "| Critical | High | Medium | Info |", "|---|---|---|---|",
           "| " + " | ".join(str(r["resumo"][s]) for s in (CRITICO, ALTO, MEDIO, INFO)) + " |", "",
           "## Files", ""]
    out += [f"- `{a['arquivo']}` ({a['bytes']:,} bytes)" for a in r["arquivos"]]
    out += ["", "## Findings", ""]
    if not r["achados"]:
        out.append("None.")
    for a in r["achados"]:
        loc = f"{a['arquivo']}:{a['linha']}" if a["linha"] else a["arquivo"]
        out.append(f"- **{a['severidade']}** `{loc}` — {a['motivo']}")
        if a["evidencia"]:
            out.append(f"  - `{a['evidencia'].replace('`', 'ˋ')}`")
    if r["urls_externas"]:
        out += ["", "## URLs from unrecognized domains", ""]
        out += [f"- {u} (in {', '.join(f)})" for u, f in r["urls_externas"].items()]
    out += ["", "> Automatic static audit: reduces the risk but does not guarantee safety. "
            "Read SKILL.md and every script before installing."]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Static audit of a third-party skill.")
    ap.add_argument("pasta")
    ap.add_argument("--json")
    ap.add_argument("--md")
    ap.add_argument("--silencioso", action="store_true", help="prints only the verdict")
    a = ap.parse_args()
    # Avoids UnicodeEncodeError on Windows consoles (cp1252) when printing the report.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    pasta = Path(a.pasta)
    if not pasta.is_dir():
        print(f"Error: folder not found: {pasta}", file=sys.stderr)
        sys.exit(3)
    r = auditar(pasta)
    if r is None:
        print(f"Error: {pasta}/SKILL.md not found — this is not a skill.", file=sys.stderr)
        sys.exit(3)

    md = para_markdown(r)
    if a.json:
        Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.md:
        Path(a.md).write_text(md, encoding="utf-8")
    print(r["veredito"] if a.silencioso else md)
    sys.exit({"OK": 0, "REVIEW": 1, "BLOCK": 2}[r["veredito"]])


if __name__ == "__main__":
    main()
