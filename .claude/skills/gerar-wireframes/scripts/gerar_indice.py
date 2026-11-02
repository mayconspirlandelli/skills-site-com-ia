#!/usr/bin/env python3
"""
Generates an index.html to review all wireframes at once (used for step 6 approval).

Usage:
  python gerar_indice.py etapas/04_wireframes

Groups the wireframe_<page>-desktop.svg and wireframe_<page>-mobile.svg files by page,
shows desktop and mobile side by side and lists each page's sections read from the
data-nome / data-layout / data-mobile attributes of the <g class="secao"> elements.

No external dependencies.
"""
import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://www.w3.org/2000/svg}"
RE_NOME = re.compile(r"^wireframe_(.+?)-(desktop|mobile)\.svg$")


def esc(t):
    return html.escape(str(t), quote=True)


def secoes(caminho):
    try:
        raiz = ET.parse(caminho).getroot()
    except ET.ParseError:
        return []
    return [g for g in raiz.iter(NS + "g") if "secao" in (g.get("class") or "").split()]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Generates index.html with all wireframes")
    ap.add_argument("pasta", help="wireframes folder (e.g. etapas/04_wireframes)")
    a = ap.parse_args()

    pasta = Path(a.pasta)
    paginas = {}
    for svg in sorted(pasta.glob("wireframe_*.svg")):
        m = RE_NOME.match(svg.name)
        if m:
            paginas.setdefault(m.group(1), {})[m.group(2)] = svg
    if not paginas:
        sys.exit(f"No wireframe_<page>-desktop|mobile.svg in {pasta}")

    blocos = []
    for pagina, arquivos in paginas.items():
        desk, mob = arquivos.get("desktop"), arquivos.get("mobile")
        lista = ""
        if desk:
            itens = "".join(
                f"<li><strong>{esc(g.get('data-nome', g.get('id', '?')))}</strong> — {esc(g.get('data-layout', ''))}"
                f"{' · mobile: ' + esc(g.get('data-mobile')) if g.get('data-mobile') else ''}</li>"
                for g in secoes(desk)
            )
            lista = f"<ol>{itens}</ol>"
        img = lambda f, cls: (f'<figure class="{cls}"><img src="{esc(f.name)}" alt="Wireframe {esc(pagina)} {cls}">'
                              f'<figcaption>{esc(f.name)}</figcaption></figure>') if f else f'<p class="falta">no {cls} version</p>'
        blocos.append(
            f'<section id="{esc(pagina)}"><h2>{esc(pagina)}</h2>{lista}'
            f'<div class="telas">{img(desk, "desktop")}{img(mob, "mobile")}</div></section>'
        )

    menu = " · ".join(f'<a href="#{esc(p)}">{esc(p)}</a>' for p in paginas)
    pagina_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wireframes</title>
<style>
body{{font-family:system-ui,sans-serif;background:#f4f4f4;color:#222;margin:0;padding:32px 24px}}
main{{max-width:1600px;margin:0 auto}} h1{{font-size:1.6rem}} nav{{margin:8px 0 24px;color:#666}}
section{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:20px;margin-bottom:32px}}
h2{{margin:0 0 8px;text-transform:capitalize}} ol{{color:#444;font-size:.9rem;columns:2;margin:0 0 16px}}
.telas{{display:flex;gap:24px;align-items:flex-start;overflow-x:auto}}
figure{{margin:0}} figure img{{display:block;border:1px solid #ccc;background:#fff}}
.desktop img{{width:900px}} .mobile img{{width:280px}}
figcaption{{font:12px ui-monospace,monospace;color:#777;margin-top:6px}} .falta{{color:#999;font-style:italic}}
</style></head>
<body><main><h1>Wireframes — {len(paginas)} page(s)</h1>
<nav>{menu}</nav>
<p>Review the structure of each page. Once approved, record it in <code>etapas/aprovacoes.md</code>.</p>
{''.join(blocos)}
</main></body></html>
"""
    destino = pasta / "index.html"
    destino.write_text(pagina_html, encoding="utf-8")
    print(f"OK → {destino} ({len(paginas)} page(s))")


if __name__ == "__main__":
    main()
