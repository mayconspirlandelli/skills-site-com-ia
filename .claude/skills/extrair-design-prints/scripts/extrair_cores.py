#!/usr/bin/env python3
"""
Extrai a paleta de cores de prints de tela de sites.

Uso:
  python extrair_cores.py etapas/00_briefing/prints --saida etapas/01_extracao/prints
  python extrair_cores.py ref1_hero.png ref2_footer.jpg --saida etapas/01_extracao/prints --cores 10

Para cada imagem: dimensões e escala provável do print (1x ou retina), cores dominantes com
percentual de área, cor de destaque provável (a mais saturada com área relevante) e contraste
dos pares texto/fundo mais prováveis. No fim, uma paleta combinada de todos os prints.

Gera na pasta de saída: cores.md e cores.json.
Todos os valores são ESTIMADOS: compressão JPEG, antialiasing e sombras alteram as cores.

Dependência: Pillow (pip install pillow)
"""
import argparse
import colorsys
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Instale a dependência: pip install pillow")

EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
LADO_MAX = 480          # reduz a imagem antes de quantizar (velocidade; a paleta não muda)
CORES_INTERNAS = 32     # quantiza com folga para não engolir cores pequenas (botões, links)
DISTANCIA_FUSAO = 18    # cores mais próximas que isso (RGB euclidiano) viram uma só
AREA_MIN_DESTAQUE = 0.8  # % mínima de área para uma cor saturada contar como destaque


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
    # Cores muito escuras ou muito claras não contam como saturadas (ex.: azul-marinho de fundo).
    return 0 if l < 0.15 or l > 0.92 else s


def distancia(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def escala_provavel(largura):
    if largura >= 2400:
        return "retina 2x de desktop (divida as medidas por 2)"
    if largura >= 1200:
        return "desktop 1x (medidas em px direto)"
    if largura >= 700:
        return "celular 2x/3x ou tablet (confira pelo conteúdo; provavelmente divida por 2 ou 3)"
    return "celular 1x (medidas em px direto)"


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
    # Texto provável: a cor com maior contraste em relação ao fundo, entre as que têm área relevante.
    candidatas = [c for c in cores[1:] if c["area"] >= 0.5] or cores[1:]
    texto = max(candidatas, key=lambda c: contraste(c["rgb"], fundo["rgb"])) if candidatas else None
    saturadas = [c for c in cores[1:] if c["saturacao"] >= 0.35 and c["area"] >= AREA_MIN_DESTAQUE]
    destaque = max(saturadas, key=lambda c: (c["saturacao"], c["area"])) if saturadas else None
    pares = []
    if texto:
        pares.append(("texto provável", texto, fundo))
    if destaque:
        pares.append(("destaque sobre o fundo", destaque, fundo))
        branco_ou_texto = max((c for c in cores if c is not destaque),
                              key=lambda c: contraste(c["rgb"], destaque["rgb"]), default=None)
        if branco_ou_texto:
            pares.append(("texto sobre o destaque (ex.: botão)", branco_ou_texto, destaque))
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
    """As n cores de maior área, mais qualquer cor saturada relevante que tenha ficado de fora."""
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
    return "✅" if razao >= 4.5 else ("só texto grande" if razao >= 3 else "❌")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Extrai a paleta de cores de prints de sites")
    ap.add_argument("entradas", nargs="+", help="imagens ou pastas com imagens")
    ap.add_argument("--saida", required=True, help="pasta de saída")
    ap.add_argument("--cores", type=int, default=8, help="cores listadas por imagem (padrão 8; cores saturadas relevantes sempre entram)")
    a = ap.parse_args()

    imagens = listar_imagens(a.entradas)
    if not imagens:
        sys.exit("Nenhuma imagem encontrada (png, jpg, jpeg, webp, bmp, gif).")

    resultados, combinada = [], []
    for caminho in imagens:
        try:
            with Image.open(caminho) as img:
                largura, altura = img.size
                cores = paleta(img)
        except OSError as e:
            print(f"[aviso] não foi possível abrir {caminho}: {e}")
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
        sys.exit("Nenhuma imagem pôde ser analisada.")

    n = len(resultados)
    combinada = sorted(combinada, key=lambda c: -c["area"])[:12]
    paleta_comb = [{"hex": hex_de(c["rgb"]), "area_media": round(c["area"] / n, 1),
                    "saturacao": round(saturacao(c["rgb"]), 2), "prints": len(c["prints"])} for c in combinada]

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "cores.json").write_text(json.dumps({"prints": resultados, "combinada": paleta_comb},
                                                 ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# Cores extraídas dos prints", "",
          "Valores **estimados** a partir das imagens (compressão e antialiasing alteram as cores).", "",
          "## Paleta combinada", "",
          "| Cor | Área média | Saturação | Aparece em |", "|---|---|---|---|"]
    md += [f"| `{c['hex']}` | {c['area_media']}% | {c['saturacao']} | {c['prints']} de {n} print(s) |" for c in paleta_comb]
    md.append("")
    for r in resultados:
        md += [f"## {r['arquivo']}", "",
               f"- Tamanho: {r['largura']}×{r['altura']} px — escala provável: {r['escala']}",
               f"- Fundo provável: `{r['fundo']}` · texto provável: `{r['texto']}` · destaque provável: `{r['destaque']}`", "",
               "| Cor | Área | Saturação |", "|---|---|---|"]
        md += [f"| `{c['hex']}` | {c['area']}% | {c['saturacao']} |" for c in r["cores"]]
        if r["contrastes"]:
            md += ["", "| Par | Frente | Fundo | Contraste | AA |", "|---|---|---|---|---|"]
            md += [f"| {c['par']} | `{c['frente']}` | `{c['fundo']}` | {c['razao']}:1 | {selo_aa(c['razao'])} |"
                   for c in r["contrastes"]]
        md.append("")
    (saida / "cores.md").write_text("\n".join(md), encoding="utf-8")
    print(f"OK → {saida / 'cores.md'} ({len(resultados)} print(s))")


if __name__ == "__main__":
    main()
