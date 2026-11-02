#!/usr/bin/env python3
"""
Generates tokens.css (and optionally tailwind.tokens.js) from design_system.md.

Reads every Markdown table row whose first cell is a token in the `--name` format
and whose second cell is the value.

Usage:
  python gerar_tokens.py design_system.md --saida tokens.css [--tailwind tailwind.tokens.js]
"""
import argparse
import json
import re
import sys
from pathlib import Path

LINHA = re.compile(r"^\|\s*`?(--[a-zA-Z][\w-]*)`?\s*\|\s*([^|]+?)\s*\|")


def ler_tokens(md: str):
    tokens, secao = [], "general"
    for linha in md.splitlines():
        if linha.startswith("## "):
            secao = linha[3:].strip()
        m = LINHA.match(linha.strip())
        if m:
            tokens.append((secao, m.group(1), m.group(2).strip().strip("`")))
    return tokens


def gerar_css(tokens):
    out = ["/* Generated from design_system.md — do not edit by hand. */", ":root {"]
    secao_atual = None
    vistos = set()
    for secao, nome, valor in tokens:
        if nome in vistos:
            print(f"[warning] duplicate token ignored: {nome}", file=sys.stderr)
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
    return ("// Generated from design_system.md. Use in tailwind.config.js:\n"
            "// theme: { extend: require('./tailwind.tokens.js') }\n"
            f"module.exports = {corpo};\n")


def main():
    # Avoids UnicodeEncodeError on Windows consoles (cp1252) when printing accents and symbols.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("design_system")
    ap.add_argument("--saida", default="tokens.css")
    ap.add_argument("--tailwind")
    a = ap.parse_args()

    tokens = ler_tokens(Path(a.design_system).read_text(encoding="utf-8"))
    if not tokens:
        sys.exit("No tokens found. Tables need their 1st column in the `--name` format.")
    Path(a.saida).write_text(gerar_css(tokens), encoding="utf-8")
    print(f"OK → {a.saida} ({len(tokens)} tokens)")
    if a.tailwind:
        Path(a.tailwind).write_text(gerar_tailwind(tokens), encoding="utf-8")
        print(f"OK → {a.tailwind}")


if __name__ == "__main__":
    main()
