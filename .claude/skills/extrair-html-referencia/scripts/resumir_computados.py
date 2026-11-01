#!/usr/bin/env python3
"""
Resume os estilos computados (medidos no navegador por estilos_computados.js) em computados.md.

Uso:
  python resumir_computados.py --entrada computados-desktop.json [computados-mobile.json] --saida etapas/01_extracao/codigo/site-a

Cada entrada é a saída de:
  playwright-cli --raw eval "$(cat .claude/skills/extrair-html-referencia/scripts/estilos_computados.js)"

Gera computados.md com: fundo da página, estilo de cada papel (h1, parágrafo, botão...),
cores mais usadas (texto, fundo, borda) em hex, fontes, escala de tamanhos, raios, sombras,
larguras de container, gaps, variáveis CSS e breakpoints. Com duas entradas (desktop e mobile),
compara a tipografia dos papéis entre os dois viewports.

Sem dependências externas.
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
    # O eval pode devolver o JSON como string (com aspas): decodifica de novo.
    while isinstance(dado, str):
        dado = json.loads(dado)
    return dado


def hex_cor(valor):
    """rgb()/rgba() -> #rrggbb (alfa anotado). Outros formatos (oklch, color()) ficam como vieram."""
    m = RE_RGB.fullmatch(valor.strip())
    if not m:
        return valor
    r, g, b = (round(float(x)) for x in m.groups()[:3])
    hx = f"#{r:02x}{g:02x}{b:02x}"
    alfa = m.group(4)
    if alfa is not None:
        a = float(alfa[:-1]) / 100 if alfa.endswith("%") else float(alfa)
        if a == 0:
            return "transparente"
        if a < 1:
            return f"{hx} ({round(a * 100)}% opaco)"
    return hx


def tabela_ranking(titulo, itens, coluna, conv=lambda x: x, peso="ocorrências"):
    if not itens:
        return [f"### {titulo}", "", "_Nada encontrado._", ""]
    linhas = [f"### {titulo}", "", f"| {coluna} | {peso} |", "|---|---|"]
    for valor, qtd in itens:
        linhas.append(f"| `{conv(valor)}` | {qtd} |")
    return linhas + [""]


def secao_viewport(d):
    vp = d.get("viewport", {})
    out = [
        f"## Viewport {vp.get('largura', '?')}×{vp.get('altura', '?')}",
        "",
        f"- Elementos visíveis analisados: {d.get('elementos_analisados', '?')}",
        f"- Fundo da página: `{hex_cor(d.get('fundo_pagina', ''))}`",
    ]
    if d.get("folhas_bloqueadas"):
        out.append(
            f"- {d['folhas_bloqueadas']} folha(s) de estilo de outro domínio não puderam ser lidas "
            "(variáveis e breakpoints delas ficam de fora; as cores e fontes medidas continuam valendo)."
        )
    out.append("")

    papeis = d.get("papeis", {})
    if papeis:
        out += [
            "### Estilo por papel",
            "",
            "| Papel | Tag | Fonte | Tamanho | Peso | Altura de linha | Cor | Fundo | Raio |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for papel, s in papeis.items():
            out.append(
                f"| {papel} | `{s.get('tag', '')}` | {s.get('fontFamily', '')} | {s.get('fontSize', '')} "
                f"| {s.get('fontWeight', '')} | {s.get('lineHeight', '')} | `{hex_cor(s.get('color', ''))}` "
                f"| `{hex_cor(s.get('backgroundColor', ''))}` | {s.get('borderRadius', '')} |"
            )
        out.append("")

    out += tabela_ranking("Cores de texto", d.get("cores_texto"), "Cor", hex_cor, "peso (caracteres)")
    out += tabela_ranking("Cores de fundo", d.get("cores_fundo"), "Cor", hex_cor, "peso (área)")
    out += tabela_ranking("Cores de borda", d.get("cores_borda"), "Cor", hex_cor)
    out += tabela_ranking("Fontes", d.get("fontes"), "font-family", peso="peso (caracteres)")
    out += tabela_ranking("Tamanhos de texto", d.get("tamanhos"), "tamanho / peso / altura de linha", peso="peso (caracteres)")
    out += tabela_ranking("Raios de borda", d.get("raios"), "border-radius")
    out += tabela_ranking("Sombras", d.get("sombras"), "box-shadow")
    out += tabela_ranking("Larguras máximas (containers)", d.get("larguras_max"), "max-width")
    out += tabela_ranking("Espaçamentos (gap)", d.get("gaps"), "gap")
    out += tabela_ranking("Breakpoints", d.get("breakpoints"), "media query")

    variaveis = d.get("variaveis") or {}
    out += ["### Variáveis CSS (:root)", ""]
    if variaveis:
        out += ["| Variável | Valor |", "|---|---|"]
        out += [f"| `{k}` | `{v}` |" for k, v in list(variaveis.items())[:120]]
        if len(variaveis) > 120:
            out.append(f"| … | mais {len(variaveis) - 120} variáveis |")
    else:
        out.append("_Nenhuma variável encontrada nas folhas acessíveis._")
    return out + [""]


def comparar(dados):
    """Tipografia dos papéis lado a lado entre viewports (desktop x mobile)."""
    papeis = []
    for d in dados:
        for p in d.get("papeis", {}):
            if p not in papeis:
                papeis.append(p)
    cab = " | ".join(f"{d.get('viewport', {}).get('largura', '?')}px" for d in dados)
    out = ["## Tipografia por viewport", "", f"| Papel | {cab} |", "|---|" + "---|" * len(dados)]
    for p in papeis:
        cels = []
        for d in dados:
            s = d.get("papeis", {}).get(p)
            cels.append(f"{s['fontSize']} / {s['fontWeight']}" if s else "—")
        out.append(f"| {p} | " + " | ".join(cels) + " |")
    return out + [""]


def main():
    # Evita UnicodeEncodeError em consoles Windows (cp1252) ao imprimir acentos e símbolos.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Resume estilos computados em computados.md")
    ap.add_argument("--entrada", nargs="+", required=True, help="JSON(s) gerados por estilos_computados.js")
    ap.add_argument("--saida", required=True, help="pasta de saída")
    a = ap.parse_args()

    try:
        dados = [carregar(c) for c in a.entrada]
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Erro ao ler a entrada: {e}")

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    primeiro = dados[0]
    linhas = [
        f"# Estilos computados — {primeiro.get('titulo') or primeiro.get('url', '')}",
        "",
        f"Fonte: {primeiro.get('url', '')}",
        "",
        "Valores **medidos no navegador** depois do JavaScript da página rodar. Os pesos indicam o quanto",
        "cada valor aparece: cores de texto e fontes por quantidade de caracteres, cores de fundo por área.",
        "",
    ]
    if len(dados) > 1:
        linhas += comparar(dados)
    for d in dados:
        linhas += secao_viewport(d)

    destino = saida / "computados.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Gerado: {destino}")


if __name__ == "__main__":
    main()
