#!/usr/bin/env python3
"""
Summarizes the computed styles (measured in the browser by estilos_computados.js) into computados.md.

Usage:
  python resumir_computados.py --entrada computados-desktop.json [computados-mobile.json] --saida etapas/01_extracao/codigo/site-a

Each input is the output of:
  playwright-cli --raw eval "$(cat .claude/skills/extrair-html-referencia/scripts/estilos_computados.js)"

Generates computados.md with: page background, style of each role (h1, paragraph, button...),
most used colors (text, background, border) in hex, fonts, size scale, radii, shadows,
container widths, gaps, CSS variables and breakpoints. With two inputs (desktop and mobile),
compares the roles' typography between the two viewports.

No external dependencies.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RE_RGB = re.compile(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)")


def carregar(caminho):
    texto = Path(caminho).read_text(encoding="utf-8-sig").strip()
    dado = json.loads(texto)
    # eval may return the JSON as a (quoted) string: decode it again.
    while isinstance(dado, str):
        dado = json.loads(dado)
    return dado


def hex_cor(valor):
    """rgb()/rgba() -> #rrggbb (alpha noted). Other formats (oklch, color()) stay as they came."""
    m = RE_RGB.fullmatch(valor.strip())
    if not m:
        return valor
    r, g, b = (round(float(x)) for x in m.groups()[:3])
    hx = f"#{r:02x}{g:02x}{b:02x}"
    alfa = m.group(4)
    if alfa is not None:
        a = float(alfa[:-1]) / 100 if alfa.endswith("%") else float(alfa)
        if a == 0:
            return "transparent"
        if a < 1:
            return f"{hx} ({round(a * 100)}% opaque)"
    return hx


def tabela_ranking(titulo, itens, coluna, conv=lambda x: x, peso="occurrences"):
    if not itens:
        return [f"### {titulo}", "", "_Nothing found._", ""]
    linhas = [f"### {titulo}", "", f"| {coluna} | {peso} |", "|---|---|"]
    for valor, qtd in itens:
        linhas.append(f"| `{conv(valor)}` | {qtd} |")
    return linhas + [""]


def secao_viewport(d):
    vp = d.get("viewport", {})
    out = [
        f"## Viewport {vp.get('largura', '?')}×{vp.get('altura', '?')}",
        "",
        f"- Visible elements analyzed: {d.get('elementos_analisados', '?')}",
        f"- Page background: `{hex_cor(d.get('fundo_pagina', ''))}`",
    ]
    if d.get("folhas_bloqueadas"):
        out.append(
            f"- {d['folhas_bloqueadas']} stylesheet(s) from another domain could not be read "
            "(their variables and breakpoints are left out; the measured colors and fonts still apply)."
        )
    out.append("")

    papeis = d.get("papeis", {})
    if papeis:
        out += [
            "### Style by role",
            "",
            "| Role | Tag | Font | Size | Weight | Line height | Color | Background | Radius |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for papel, s in papeis.items():
            out.append(
                f"| {papel} | `{s.get('tag', '')}` | {s.get('fontFamily', '')} | {s.get('fontSize', '')} "
                f"| {s.get('fontWeight', '')} | {s.get('lineHeight', '')} | `{hex_cor(s.get('color', ''))}` "
                f"| `{hex_cor(s.get('backgroundColor', ''))}` | {s.get('borderRadius', '')} |"
            )
        out.append("")

    out += tabela_ranking("Text colors", d.get("cores_texto"), "Color", hex_cor, "weight (characters)")
    out += tabela_ranking("Background colors", d.get("cores_fundo"), "Color", hex_cor, "weight (area)")
    out += tabela_ranking("Border colors", d.get("cores_borda"), "Color", hex_cor)
    out += tabela_ranking("Fonts", d.get("fontes"), "font-family", peso="weight (characters)")
    out += tabela_ranking("Text sizes", d.get("tamanhos"), "size / weight / line height", peso="weight (characters)")
    out += tabela_ranking("Border radii", d.get("raios"), "border-radius")
    out += tabela_ranking("Shadows", d.get("sombras"), "box-shadow")
    out += tabela_ranking("Maximum widths (containers)", d.get("larguras_max"), "max-width")
    out += tabela_ranking("Spacing (gap)", d.get("gaps"), "gap")
    out += tabela_ranking("Breakpoints", d.get("breakpoints"), "media query")

    variaveis = d.get("variaveis") or {}
    out += ["### CSS variables (:root)", ""]
    if variaveis:
        out += ["| Variable | Value |", "|---|---|"]
        out += [f"| `{k}` | `{v}` |" for k, v in list(variaveis.items())[:120]]
        if len(variaveis) > 120:
            out.append(f"| … | {len(variaveis) - 120} more variables |")
    else:
        out.append("_No variables found in the accessible stylesheets._")
    return out + [""]


def comparar(dados):
    """Roles' typography side by side across viewports (desktop x mobile)."""
    papeis = []
    for d in dados:
        for p in d.get("papeis", {}):
            if p not in papeis:
                papeis.append(p)
    cab = " | ".join(f"{d.get('viewport', {}).get('largura', '?')}px" for d in dados)
    out = ["## Typography by viewport", "", f"| Role | {cab} |", "|---|" + "---|" * len(dados)]
    for p in papeis:
        cels = []
        for d in dados:
            s = d.get("papeis", {}).get(p)
            cels.append(f"{s['fontSize']} / {s['fontWeight']}" if s else "—")
        out.append(f"| {p} | " + " | ".join(cels) + " |")
    return out + [""]


def main():
    # Avoids UnicodeEncodeError on Windows consoles (cp1252) when printing accents and symbols.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Summarizes computed styles into computados.md")
    ap.add_argument("--entrada", nargs="+", required=True, help="JSON file(s) generated by estilos_computados.js")
    ap.add_argument("--saida", required=True, help="output folder")
    a = ap.parse_args()

    try:
        dados = [carregar(c) for c in a.entrada]
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Error reading the input: {e}")

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    primeiro = dados[0]
    linhas = [
        f"# Computed styles — {primeiro.get('titulo') or primeiro.get('url', '')}",
        "",
        f"Source: {primeiro.get('url', '')}",
        "",
        "Values **measured in the browser** after the page's JavaScript runs. Weights show how much",
        "each value appears: text colors and fonts by number of characters, background colors by area.",
        "",
    ]
    if len(dados) > 1:
        linhas += comparar(dados)
    for d in dados:
        linhas += secao_viewport(d)

    destino = saida / "computados.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Generated: {destino}")


if __name__ == "__main__":
    main()
