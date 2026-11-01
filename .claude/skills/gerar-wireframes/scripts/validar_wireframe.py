#!/usr/bin/env python3
"""Valida um wireframe SVG gerado pela skill gerar-wireframes.

Uso:
    python3 validar_wireframe.py etapas/04_wireframes/wireframe_home-desktop.svg [outros.svg ...]

Verifica:
  - XML válido com raiz <svg>, viewBox, data-pagina e data-viewport;
  - <title> e <desc> presentes;
  - cada seção é um <g class="secao"> com id, data-nome, data-layout e data-elementos;
  - ids de seção únicos;
  - nada copiado ou externo: sem <image>, <script>, <foreignObject>, href externo
    ou imagens embutidas em base64.

Saída: 0 = ok, 1 = problemas encontrados.
"""
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
PROIBIDOS = {"image", "script", "foreignObject"}
ATRIBUTOS_SECAO = ("data-nome", "data-layout", "data-elementos")


def tag(el):
    return el.tag.replace(NS, "")


def validar(caminho):
    erros, avisos = [], []
    try:
        raiz = ET.parse(caminho).getroot()
    except (ET.ParseError, OSError) as e:
        return [f"não foi possível ler o SVG: {e}"], []

    if tag(raiz) != "svg":
        erros.append("a raiz não é <svg>")
    for attr in ("viewBox", "data-pagina", "data-viewport"):
        if not raiz.get(attr):
            erros.append(f"<svg> sem atributo {attr}")
    for filho in ("title", "desc"):
        if raiz.find(NS + filho) is None:
            erros.append(f"falta <{filho}> no início do arquivo")

    ids = set()
    secoes = [g for g in raiz.iter(NS + "g") if "secao" in (g.get("class") or "").split()]
    if not secoes:
        erros.append('nenhuma seção encontrada (<g class="secao">)')
    for g in secoes:
        sid = g.get("id")
        if not sid:
            erros.append(f"seção sem id ({g.get('data-nome', '?')})")
        elif sid in ids:
            erros.append(f"id de seção repetido: {sid}")
        ids.add(sid)
        for attr in ATRIBUTOS_SECAO:
            if not g.get(attr):
                erros.append(f"seção '{sid}' sem {attr}")
        if not g.get("data-mobile") and raiz.get("data-viewport") == "desktop":
            avisos.append(f"seção '{sid}' sem data-mobile (comportamento responsivo)")

    for el in raiz.iter():
        if tag(el) in PROIBIDOS:
            erros.append(f"elemento proibido <{tag(el)}> (sem imagens, scripts ou HTML embutido)")
        href = el.get("href") or el.get(XLINK) or ""
        if href.startswith(("http:", "https:", "data:", "//")):
            erros.append(f"referência externa ou embutida proibida: {href[:60]}")

    return erros, avisos


def main():
    # Evita UnicodeEncodeError em consoles Windows (cp1252) ao imprimir acentos e símbolos.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    falhou = False
    for caminho in sys.argv[1:]:
        erros, avisos = validar(caminho)
        status = "OK" if not erros else "PROBLEMAS"
        print(f"{caminho}: {status}")
        for e in erros:
            print(f"  ✗ {e}")
        for a in avisos:
            print(f"  ! {a}")
        falhou = falhou or bool(erros)
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
