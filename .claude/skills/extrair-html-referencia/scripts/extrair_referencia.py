#!/usr/bin/env python3
"""
Extrai e limpa o HTML de um site de referência e gera um resumo estruturado.

Uso:
  python extrair_referencia.py --html pagina.html --saida etapas/01_extracao/codigo/site-a
  python extrair_referencia.py --url https://exemplo.com --saida etapas/01_extracao/codigo/site-a
  python extrair_referencia.py --html pagina.html --css estilo1.css estilo2.css --saida ...

Gera na pasta de saída:
  limpo.html   HTML sem scripts, trackers, SVGs gigantes e comentários
  estilos.css  todo o CSS encontrado (inline + arquivos), concatenado
  resumo.md    estrutura de seções, títulos, fontes, cores, variáveis CSS, breakpoints
  dados.json   os mesmos dados do resumo em formato estruturado

Dependência: beautifulsoup4 (pip install beautifulsoup4)
"""
import argparse
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    sys.exit("Instale a dependência: pip install beautifulsoup4")

UA = {"User-Agent": "Mozilla/5.0 (referencia-design-extractor)"}

RE_HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
RE_FUNC_COLOR = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab)\([^)]*\)", re.I)
RE_VAR = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)")
RE_MEDIA = re.compile(r"@media[^{]*\(\s*(min|max)-width\s*:\s*([\d.]+)(px|em|rem)", re.I)
RE_FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}]+)", re.I)
RE_FONT_FACE = re.compile(r"@font-face\s*{[^}]*font-family\s*:\s*['\"]?([^;'\"]+)", re.I)
RE_FONT_SIZE = re.compile(r"font-size\s*:\s*([^;}]+)", re.I)
RE_RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)", re.I)
RE_SHADOW = re.compile(r"box-shadow\s*:\s*([^;}]+)", re.I)

REMOVER_TAGS = ["script", "noscript", "iframe", "template", "object", "embed"]
TRACKERS = ("googletagmanager", "google-analytics", "facebook", "hotjar", "gtag", "pixel", "clarity")
SECOES = ["header", "nav", "main", "section", "article", "aside", "footer"]


def baixar(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")


def coletar_css(soup, base_url, arquivos_css):
    partes = []
    for tag in soup.find_all("style"):
        partes.append(tag.get_text())
    for tag in soup.find_all(style=True):
        partes.append("x{" + tag["style"] + "}")
    fontes_links = []
    for link in soup.find_all("link", rel=lambda v: v and "stylesheet" in v):
        href = link.get("href", "")
        if "fonts.googleapis" in href or "use.typekit" in href:
            fontes_links.append(href)
        if base_url and href:
            try:
                partes.append(baixar(urljoin(base_url, href)))
            except Exception as e:  # rede bloqueada, 404 etc.
                print(f"[aviso] não baixou CSS {href}: {e}", file=sys.stderr)
    for caminho in arquivos_css or []:
        partes.append(Path(caminho).read_text(encoding="utf-8", errors="replace"))
    return "\n".join(partes), fontes_links


def limpar(soup):
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for nome in REMOVER_TAGS:
        for t in soup.find_all(nome):
            t.decompose()
    for link in soup.find_all("link"):
        href = link.get("href", "")
        if any(k in href for k in TRACKERS) or "preload" in (link.get("rel") or []):
            link.decompose()
    for svg in soup.find_all("svg"):
        if len(str(svg)) > 400:
            svg.clear()
            svg["data-svg-removido"] = "true"
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("data:"):
            img["src"] = "data:removido"
    for t in soup.find_all(True):
        for attr in list(t.attrs):
            if attr.startswith("on") or attr.startswith("data-v-") or attr in ("srcset", "sizes"):
                del t[attr]
    return soup


def descrever(tag):
    partes = [tag.name]
    if tag.get("id"):
        partes.append("#" + tag["id"])
    classes = tag.get("class") or []
    if classes:
        partes.append("." + ".".join(classes[:3]))
    return "".join(partes)


def estrutura(soup):
    body = soup.body or soup
    linhas = []

    def visitar(el, nivel):
        for filho in el.find_all(True, recursive=False):
            if filho.name in SECOES or (filho.name == "div" and nivel == 0):
                tem_subsecoes = bool(filho.find(["section", "article", "nav"]))
                headings = [] if tem_subsecoes else [f"{h.name.upper()}: {h.get_text(' ', strip=True)[:70]}"
                            for h in filho.find_all(re.compile("^h[1-6]$"))][:4]
                contagem = {
                    "botões": len(filho.find_all("button")) + len(filho.select("a[class*=btn], a[class*=button]")),
                    "links": len(filho.find_all("a")),
                    "imagens": len(filho.find_all(["img", "picture", "video"])),
                    "forms": len(filho.find_all("form")),
                }
                resumo_cont = ", ".join(f"{k}={v}" for k, v in contagem.items() if v)
                linhas.append(f"{'  ' * nivel}- [{descrever(filho)}] {resumo_cont}")
                for h in headings:
                    linhas.append(f"{'  ' * (nivel + 1)}· {h}")
                if nivel < 2:
                    visitar(filho, nivel + 1)
            elif nivel < 3:
                visitar(filho, nivel)

    visitar(body, 0)
    return linhas


def normalizar_cor(c):
    c = c.strip().lower()
    if re.fullmatch(r"#[0-9a-f]{3}", c):
        c = "#" + "".join(ch * 2 for ch in c[1:])
    return re.sub(r"\s+", " ", c)


def analisar_css(css):
    cores = Counter(normalizar_cor(c) for c in RE_HEX.findall(css) + RE_FUNC_COLOR.findall(css))
    variaveis = {}
    for nome, valor in RE_VAR.findall(css):
        variaveis.setdefault(nome, valor.strip())
    bps = Counter(f"{m}-width: {v}{u}" for m, v, u in RE_MEDIA.findall(css))
    familias = Counter(re.sub(r"['\"]", "", f).strip() for f in RE_FONT_FAMILY.findall(css) if "var(" not in f)
    font_faces = sorted(set(f.strip() for f in RE_FONT_FACE.findall(css)))
    tamanhos = Counter(s.strip() for s in RE_FONT_SIZE.findall(css))
    raios = Counter(r.strip() for r in RE_RADIUS.findall(css))
    sombras = Counter(s.strip() for s in RE_SHADOW.findall(css))
    return {
        "cores": cores.most_common(25),
        "variaveis_css": variaveis,
        "breakpoints": bps.most_common(10),
        "font_family": familias.most_common(10),
        "font_face": font_faces,
        "font_size": tamanhos.most_common(15),
        "border_radius": raios.most_common(8),
        "box_shadow": sombras.most_common(6),
    }


def gerar_resumo(meta, secoes, css_info, fontes_links, avisos):
    out = [f"# Resumo da referência: {meta['titulo'] or '(sem título)'}", ""]
    if meta.get("origem"):
        out.append(f"Origem: {meta['origem']}")
    if meta.get("descricao"):
        out.append(f"Descrição: {meta['descricao']}")
    out.append("")
    if avisos:
        out.append("## ⚠️ Avisos")
        out += [f"- {a}" for a in avisos] + [""]
    out.append("## Estrutura de seções (ordem no HTML)")
    out += (secoes or ["(nenhuma seção semântica encontrada)"]) + [""]

    out.append("## Tipografia")
    if fontes_links:
        out.append("Links de fontes: " + ", ".join(fontes_links))
    if css_info["font_face"]:
        out.append("@font-face: " + ", ".join(css_info["font_face"]))
    out += [f"- font-family `{f}` ({n}x)" for f, n in css_info["font_family"]]
    if css_info["font_size"]:
        out.append("Tamanhos mais usados: " + ", ".join(f"`{s}` ({n}x)" for s, n in css_info["font_size"]))
    out.append("")

    out.append("## Cores (por frequência)")
    out += [f"- `{c}` ({n}x)" for c, n in css_info["cores"]] or ["(nenhuma)"]
    out.append("")

    out.append("## Variáveis CSS")
    vars_ = list(css_info["variaveis_css"].items())
    out += [f"- `{k}: {v}`" for k, v in vars_[:60]] or ["(nenhuma)"]
    if len(vars_) > 60:
        out.append(f"- … e mais {len(vars_) - 60} variáveis (ver dados.json)")
    out.append("")

    out.append("## Breakpoints")
    out += [f"- `{b}` ({n}x)" for b, n in css_info["breakpoints"]] or ["(nenhum)"]
    out.append("")
    out.append("## Bordas e sombras")
    out += [f"- radius `{r}` ({n}x)" for r, n in css_info["border_radius"]]
    out += [f"- shadow `{s}` ({n}x)" for s, n in css_info["box_shadow"]]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    fonte = ap.add_mutually_exclusive_group(required=True)
    fonte.add_argument("--html", help="arquivo HTML salvo localmente")
    fonte.add_argument("--url", help="URL da página (requer acesso à rede)")
    ap.add_argument("--css", nargs="*", help="arquivos CSS extras salvos localmente")
    ap.add_argument("--base-url", help="URL original, para resolver CSS relativo ao usar --html")
    ap.add_argument("--saida", required=True, help="pasta de saída")
    a = ap.parse_args()

    base_url = a.url or a.base_url
    html = baixar(a.url) if a.url else Path(a.html).read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    avisos = []
    css, fontes_links = coletar_css(soup, base_url, a.css)
    titulo = soup.title.get_text(strip=True) if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    meta = {"titulo": titulo, "descricao": desc_tag.get("content", "") if desc_tag else "",
            "origem": a.url or a.base_url or a.html}

    soup = limpar(soup)
    texto_visivel = (soup.body.get_text(" ", strip=True) if soup.body else "")
    if len(texto_visivel) < 300:
        avisos.append("Pouco texto no HTML: a página provavelmente é renderizada por JavaScript "
                      "(React/Vue/Next). Salve o HTML renderizado pelo DevTools (Elements → Copy outerHTML).")
    if not css.strip():
        avisos.append("Nenhum CSS encontrado. Salve a página como 'completa' ou passe os arquivos com --css.")

    secoes = estrutura(soup)
    css_info = analisar_css(css)

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "limpo.html").write_text(soup.prettify(), encoding="utf-8")
    (saida / "estilos.css").write_text(css, encoding="utf-8")
    (saida / "resumo.md").write_text(gerar_resumo(meta, secoes, css_info, fontes_links, avisos), encoding="utf-8")
    (saida / "dados.json").write_text(json.dumps(
        {"meta": meta, "avisos": avisos, "secoes": secoes, "fontes_links": fontes_links, **css_info},
        ensure_ascii=False, indent=2), encoding="utf-8")

    tam_orig, tam_limpo = len(html), len(str(soup))
    print(f"OK → {saida}/  (HTML {tam_orig:,} → {tam_limpo:,} caracteres)")
    for av in avisos:
        print("[aviso]", av)


if __name__ == "__main__":
    main()
