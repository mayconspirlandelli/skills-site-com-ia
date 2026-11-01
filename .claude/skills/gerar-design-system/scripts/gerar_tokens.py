#!/usr/bin/env python3
"""
Gera tokens.css (e opcionalmente tailwind.tokens.js) a partir do design_system.md.

Lê toda linha de tabela Markdown cuja primeira célula seja um token no formato `--nome`
e cuja segunda célula seja o valor.

Uso:
  python gerar_tokens.py design_system.md --saida tokens.css [--tailwind tailwind.tokens.js]
"""
import argparse
import json
import re
import sys
from pathlib import Path

LINHA = re.compile(r"^\|\s*`?(--[a-zA-Z][\w-]*)`?\s*\|\s*([^|]+?)\s*\|")


def ler_tokens(md: str):
    tokens, secao = [], "geral"
    for linha in md.splitlines():
        if linha.startswith("## "):
            secao = linha[3:].strip()
        m = LINHA.match(linha.strip())
        if m:
            tokens.append((secao, m.group(1), m.group(2).strip().strip("`")))
    return tokens


def gerar_css(tokens):
    out = ["/* Gerado a partir de design_system.md — não edite à mão. */", ":root {"]
    secao_atual = None
    vistos = set()
    for secao, nome, valor in tokens:
        if nome in vistos:
            print(f"[aviso] token duplicado ignorado: {nome}", file=sys.stderr)
            continue
        vistos.add(nome)
        if secao != secao_atual:
            out.append(f"\n  /* {secao} */")
            secao_atual = secao
        out.append(f"  {nome}: {valor};")
    out.append("}")
    return "\n".join(out) + "\n"


def gerar_tailwind(tokens):
    grupos = {"colors": "--color-", "spacing": "--space-", "borderRadius": "--radius-",
              "boxShadow": "--shadow-", "fontFamily": "--font-", "fontSize": "--text-"}
    tema = {k: {} for k in grupos}
    for _, nome, _ in tokens:
        for chave, prefixo in grupos.items():
            if nome.startswith(prefixo):
                valor = f"var({nome})"
                tema[chave][nome[len(prefixo):]] = [valor] if chave == "fontFamily" else valor
    corpo = json.dumps({k: v for k, v in tema.items() if v}, indent=2, ensure_ascii=False)
    return ("// Gerado a partir de design_system.md. Use em tailwind.config.js:\n"
            "// theme: { extend: require('./tailwind.tokens.js') }\n"
            f"module.exports = {corpo};\n")


def main():
    # Evita UnicodeEncodeError em consoles Windows (cp1252) ao imprimir acentos e símbolos.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("design_system")
    ap.add_argument("--saida", default="tokens.css")
    ap.add_argument("--tailwind")
    a = ap.parse_args()

    tokens = ler_tokens(Path(a.design_system).read_text(encoding="utf-8"))
    if not tokens:
        sys.exit("Nenhum token encontrado. As tabelas precisam ter a 1ª coluna no formato `--nome`.")
    Path(a.saida).write_text(gerar_css(tokens), encoding="utf-8")
    print(f"OK → {a.saida} ({len(tokens)} tokens)")
    if a.tailwind:
        Path(a.tailwind).write_text(gerar_tailwind(tokens), encoding="utf-8")
        print(f"OK → {a.tailwind}")


if __name__ == "__main__":
    main()
