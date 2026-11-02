#!/usr/bin/env python3
"""
Extracts the color palette from website screenshots.

Usage:
  python extrair_cores.py etapas/00_briefing/prints --saida etapas/01_extracao/prints
  python extrair_cores.py ref1_hero.png ref2_footer.jpg --saida etapas/01_extracao/prints --cores 10

For each image: dimensions and likely screenshot scale (1x or retina), dominant colors with
area percentage, likely accent color (the most saturated one with relevant area) and contrast
of the most likely text/background pairs. At the end, a combined palette of all screenshots.

Writes to the output folder: cores.md and cores.json.
All values are ESTIMATED: JPEG compression, antialiasing and shadows change the colors.

Dependency: Pillow (pip install pillow)
"""
import argparse
import colorsys
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Install the dependency: pip install pillow")

EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
LADO_MAX = 480          # shrinks the image before quantizing (speed; the palette doesn't change)
CORES_INTERNAS = 32     # quantizes loosely so small colors (buttons, links) aren't swallowed
DISTANCIA_FUSAO = 18    # colors closer than this (Euclidean RGB) merge into one
AREA_MIN_DESTAQUE = 0.8  # minimum area % for a saturated color to count as an accent


def hex_de(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def luminancia(rgb):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def saturacao(rgb):
    _, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    # Very dark or very light colors don't count as saturated (e.g. a navy background).
    return 0 if l < 0.15 or l > 0.92 else s


def distancia(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def escala_provavel(largura):
    if largura >= 2400:
        return "desktop retina 2x (divide measurements by 2)"
    if largura >= 1200:
        return "desktop 1x (measurements in px directly)"
    if largura >= 700:
        return "mobile 2x/3x or tablet (check by the content; probably divide by 2 or 3)"
    return "mobile 1x (measurements in px directly)"


def paleta(img):
    img = img.convert("RGB")
    img.thumbnail((LADO_MAX, LADO_MAX))
    q = img.quantize(colors=CORES_INTERNAS, method=Image.Quantize.FASTOCTREE)
    pal = q.getpalette()
    contagem = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in contagem)
    cores = []
    for qtd, idx in contagem:
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        for c in cores:
            if distancia(c["rgb"], rgb) < DISTANCIA_FUSAO:
                c["area"] += qtd / total * 100
                break
        else:
            cores.append({"rgb": rgb, "area": qtd / total * 100})
    for c in cores:
        c["hex"] = hex_de(c["rgb"])
        c["area"] = round(c["area"], 1)
        c["saturacao"] = round(saturacao(c["rgb"]), 2)
        c["luminancia"] = round(luminancia(c["rgb"]), 3)
    return sorted(cores, key=lambda c: -c["area"])


def analisar(cores):
    fundo = cores[0]
    # Likely text: the color with the highest contrast against the background, among those with relevant area.
    candidatas = [c for c in cores[1:] if c["area"] >= 0.5] or cores[1:]
    texto = max(candidatas, key=lambda c: contraste(c["rgb"], fundo["rgb"])) if candidatas else None
    saturadas = [c for c in cores[1:] if c["saturacao"] >= 0.35 and c["area"] >= AREA_MIN_DESTAQUE]
    destaque = max(saturadas, key=lambda c: (c["saturacao"], c["area"])) if saturadas else None
    pares = []
    if texto:
        pares.append(("likely text", texto, fundo))
    if destaque:
        pares.append(("accent on background", destaque, fundo))
        branco_ou_texto = max((c for c in cores if c is not destaque),
                              key=lambda c: contraste(c["rgb"], destaque["rgb"]), default=None)
        if branco_ou_texto:
            pares.append(("text on accent (e.g. button)", branco_ou_texto, destaque))
    return {
        "fundo": fundo["hex"],
        "texto": texto["hex"] if texto else None,
        "destaque": destaque["hex"] if destaque else None,
        "contrastes": [
            {"par": nome, "frente": a["hex"], "fundo": b["hex"], "razao": round(contraste(a["rgb"], b["rgb"]), 2)}
            for nome, a, b in pares
        ],
    }


def resumir(cores, n):
    """The n colors with the largest area, plus any relevant saturated color left out."""
    topo = cores[:n]
    extras = [c for c in cores[n:] if c["saturacao"] >= 0.35 and c["area"] >= AREA_MIN_DESTAQUE / 2]
    return topo + extras


def listar_imagens(entradas):
    arquivos = []
    for e in entradas:
        p = Path(e)
        if p.is_dir():
            arquivos += sorted(f for f in p.iterdir() if f.suffix.lower() in EXTENSOES)
        elif p.suffix.lower() in EXTENSOES:
            arquivos.append(p)
    return arquivos


def selo_aa(razao):
    return "✅" if razao >= 4.5 else ("large text only" if razao >= 3 else "❌")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Extracts the color palette from website screenshots")
    ap.add_argument("entradas", nargs="+", help="images or folders with images")
    ap.add_argument("--saida", required=True, help="output folder")
    ap.add_argument("--cores", type=int, default=8, help="colors listed per image (default 8; relevant saturated colors are always included)")
    a = ap.parse_args()

    imagens = listar_imagens(a.entradas)
    if not imagens:
        sys.exit("No images found (png, jpg, jpeg, webp, bmp, gif).")

    resultados, combinada = [], []
    for caminho in imagens:
        try:
            with Image.open(caminho) as img:
                largura, altura = img.size
                cores = paleta(img)
        except OSError as e:
            print(f"[warning] could not open {caminho}: {e}")
            continue
        resultados.append({
            "arquivo": caminho.name,
            "largura": largura, "altura": altura,
            "escala": escala_provavel(largura),
            "cores": [{k: c[k] for k in ("hex", "area", "saturacao", "luminancia")} for c in resumir(cores, a.cores)],
            **analisar(cores),
        })
        for c in resumir(cores, a.cores):
            for k in combinada:
                if distancia(k["rgb"], c["rgb"]) < DISTANCIA_FUSAO:
                    k["area"] += c["area"]
                    k["prints"].add(caminho.name)
                    break
            else:
                combinada.append({"rgb": c["rgb"], "area": c["area"], "prints": {caminho.name}})

    if not resultados:
        sys.exit("No image could be analyzed.")

    n = len(resultados)
    combinada = sorted(combinada, key=lambda c: -c["area"])[:12]
    paleta_comb = [{"hex": hex_de(c["rgb"]), "area_media": round(c["area"] / n, 1),
                    "saturacao": round(saturacao(c["rgb"]), 2), "prints": len(c["prints"])} for c in combinada]

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "cores.json").write_text(json.dumps({"prints": resultados, "combinada": paleta_comb},
                                                 ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# Colors extracted from screenshots", "",
          "Values **estimated** from the images (compression and antialiasing change the colors).", "",
          "## Combined palette", "",
          "| Color | Average area | Saturation | Appears in |", "|---|---|---|---|"]
    md += [f"| `{c['hex']}` | {c['area_media']}% | {c['saturacao']} | {c['prints']} of {n} screenshot(s) |" for c in paleta_comb]
    md.append("")
    for r in resultados:
        md += [f"## {r['arquivo']}", "",
               f"- Size: {r['largura']}×{r['altura']} px — likely scale: {r['escala']}",
               f"- Likely background: `{r['fundo']}` · likely text: `{r['texto']}` · likely accent: `{r['destaque']}`", "",
               "| Color | Area | Saturation |", "|---|---|---|"]
        md += [f"| `{c['hex']}` | {c['area']}% | {c['saturacao']} |" for c in r["cores"]]
        if r["contrastes"]:
            md += ["", "| Pair | Foreground | Background | Contrast | AA |", "|---|---|---|---|---|"]
            md += [f"| {c['par']} | `{c['frente']}` | `{c['fundo']}` | {c['razao']}:1 | {selo_aa(c['razao'])} |"
                   for c in r["contrastes"]]
        md.append("")
    (saida / "cores.md").write_text("\n".join(md), encoding="utf-8")
    print(f"OK → {saida / 'cores.md'} ({len(resultados)} screenshot(s))")


if __name__ == "__main__":
    main()
