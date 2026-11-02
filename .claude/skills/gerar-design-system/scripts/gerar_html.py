#!/usr/bin/env python3
"""
Generates design_system.html — the visual version of design_system.md — for the user to review and approve.

Usage:
  python gerar_html.py etapas/05_design_system/design_system.md --saida etapas/05_design_system/design_system.html

Reads the same tokens as gerar_tokens.py (tables with the 1st column `--name`) and builds a
self-contained page with: palette (swatches + computed contrast), typography (families and rendered scale),
spacing, radii, shadows, layout/breakpoints and sample components (buttons, card, input)
drawn only with the tokens. Rules and explanations stay in design_system.md.

Don't edit the HTML by hand: change design_system.md and run it again.
No external dependencies.
"""
import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_tokens import gerar_css, ler_tokens  # noqa: E402

RE_HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RE_LINHA = re.compile(r"^\|\s*`?(--[a-zA-Z][\w-]*)`?\s*\|(.+)\|\s*$")
RE_FONTES = re.compile(r'<link[^>]+href="(https://fonts\.googleapis\.com/[^"]+)"[^>]*>')


def esc(t):
    return html.escape(str(t), quote=True)


def rgb(hx):
    hx = hx.lstrip("#")
    if len(hx) == 3:
        hx = "".join(c * 2 for c in hx)
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def lum(hx):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb(hx))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def selo(r):
    return "AA" if r >= 4.5 else ("AA large" if r >= 3 else "fail")


def colunas_extras(md):
    """For each token, the cells after the value (use, weight, line height...)."""
    extras = {}
    for linha in md.splitlines():
        m = RE_LINHA.match(linha.strip())
        if m:
            celulas = [c.strip().strip("`") for c in m.group(2).split("|")]
            extras.setdefault(m.group(1), celulas[1:])
    return extras


def secao_cores(cores, extras, fundo, texto):
    if not cores:
        return ""
    cards = []
    for nome, valor in cores:
        uso = extras.get(nome, [""])[0] if extras.get(nome) else ""
        medidas = ""
        if RE_HEX.match(valor):
            pares = []
            if fundo and RE_HEX.match(fundo) and nome != "--color-bg":
                r = contraste(valor, fundo)
                pares.append(f"on background {r:.2f}:1 · {selo(r)}")
            r_branco = contraste(valor, "#ffffff")
            r_texto = contraste(valor, texto) if texto and RE_HEX.match(texto) else None
            melhor = ("white", r_branco) if r_texto is None or r_branco >= r_texto else ("text", r_texto)
            pares.append(f"{melhor[0]} text on it {melhor[1]:.2f}:1 · {selo(melhor[1])}")
            medidas = "".join(f"<li>{esc(p)}</li>" for p in pares)
        cards.append(
            f'<figure class="cor"><div class="amostra" style="background:var({esc(nome)})"></div>'
            f'<figcaption><code>{esc(nome)}</code><span>{esc(valor)}</span>'
            f'<em>{esc(uso)}</em><ul>{medidas}</ul></figcaption></figure>'
        )
    return '<section><h2>Palette</h2><div class="grade-cores">' + "".join(cards) + "</div></section>"


def secao_tipografia(fontes, textos, extras, tem_heading):
    if not fontes and not textos:
        return ""
    partes = ['<section><h2>Typography</h2>']
    for nome, valor in fontes:
        uso = extras.get(nome, [""])[0] if extras.get(nome) else ""
        partes.append(
            f'<div class="familia" style="font-family:var({esc(nome)})"><code>{esc(nome)}</code>'
            f'<p class="especime">Aa Bb Cc 123 — {esc(uso or valor)}</p><small>{esc(valor)}</small></div>'
        )
    if textos:
        partes.append('<div class="escala">')
        for nome, valor in textos:
            ex = extras.get(nome, [])
            peso = ex[0] if len(ex) >= 3 and ex[0].isdigit() else "400"
            altura = ex[1] if len(ex) >= 3 else "1.3"
            uso = ex[-1] if ex else ""
            familia = "var(--font-heading)" if tem_heading and re.search(r"-h\d|display|title", nome) else "var(--font-body, inherit)"
            partes.append(
                f'<div class="linha-escala"><code>{esc(nome)}<br><small>{esc(valor)} · {esc(peso)} · {esc(altura)}</small></code>'
                f'<p style="font-size:var({esc(nome)});font-weight:{esc(peso)};line-height:{esc(altura)};font-family:{familia}">'
                f'{esc(uso or "Sample text")}</p></div>'
            )
        partes.append("</div>")
    return "".join(partes) + "</section>"


def secao_espacos(espacos):
    if not espacos:
        return ""
    linhas = "".join(
        f'<div class="linha-espaco"><code>{esc(n)}</code><span class="barra" style="width:var({esc(n)})"></span><small>{esc(v)}</small></div>'
        for n, v in espacos
    )
    return f"<section><h2>Spacing</h2>{linhas}</section>"


def secao_formas(raios, sombras):
    if not raios and not sombras:
        return ""
    itens = "".join(
        f'<div class="forma" style="border-radius:var({esc(n)})"><code>{esc(n)}</code><small>{esc(v)}</small></div>' for n, v in raios
    ) + "".join(
        f'<div class="forma sombra" style="box-shadow:var({esc(n)})"><code>{esc(n)}</code><small>{esc(v)}</small></div>' for n, v in sombras
    )
    return f'<section><h2>Radii and shadows</h2><div class="grade-formas">{itens}</div></section>'


def secao_layout(layout):
    if not layout:
        return ""
    linhas = "".join(f"<tr><td><code>{esc(n)}</code></td><td>{esc(v)}</td></tr>" for n, v in layout)
    return f"<section><h2>Layout and breakpoints</h2><table>{linhas}</table></section>"


def secao_componentes(nomes):
    if "--color-primary" not in nomes:
        return ""
    return """<section><h2>Sample components</h2>
<p class="nota">Built only with the tokens. The full specification (states, variants) is in design_system.md.</p>
<div class="demo">
  <button class="btn btn-prim">Primary button</button>
  <button class="btn btn-sec">Secondary button</button>
  <a href="#" class="link">Text link</a>
</div>
<div class="demo">
  <article class="card"><h3>Card title</h3><p>Card supporting text, with two lines to show the body text line height.</p></article>
  <label class="campo">Form field<input type="text" placeholder="Type here"></label>
</div>
</section>"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Generates design_system.html from design_system.md")
    ap.add_argument("design_system")
    ap.add_argument("--saida", default="design_system.html")
    a = ap.parse_args()

    md = Path(a.design_system).read_text(encoding="utf-8")
    tokens = ler_tokens(md)
    if not tokens:
        sys.exit("No tokens found. Tables need their 1st column in the `--name` format.")
    vistos, unicos = set(), []
    for _, n, v in tokens:
        if n not in vistos:
            vistos.add(n)
            unicos.append((n, v))
    valor = dict(unicos)
    extras = colunas_extras(md)
    titulo = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "Design System")
    fontes_link = RE_FONTES.search(md)

    grupo = lambda *pref: [(n, v) for n, v in unicos if n.startswith(pref)]
    corpo = "".join([
        secao_cores(grupo("--color-"), extras, valor.get("--color-bg"), valor.get("--color-text")),
        secao_tipografia(grupo("--font-"), grupo("--text-"), extras, "--font-heading" in valor),
        secao_espacos(grupo("--space-")),
        secao_formas(grupo("--radius-"), grupo("--shadow-")),
        secao_layout(grupo("--container-", "--bp-", "--grid-")),
        secao_componentes(valor),
    ])

    pagina = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(titulo)}</title>
{f'<link rel="stylesheet" href="{esc(fontes_link.group(1))}">' if fontes_link else ''}
<style>
{gerar_css(tokens)}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font-body,system-ui,sans-serif);background:var(--color-bg,#fff);color:var(--color-text,#111);line-height:1.5;padding:48px 24px}}
main{{max-width:1100px;margin:0 auto}}
header.topo{{margin-bottom:40px}} header.topo h1{{font-family:var(--font-heading,inherit);font-size:2rem;line-height:1.2}}
header.topo p,.nota{{color:var(--color-text-muted,#666);font-size:.875rem;margin-top:6px}}
section{{margin-top:48px}} h2{{font-family:var(--font-heading,inherit);font-size:1.25rem;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--color-border,#ddd)}}
code{{font-family:ui-monospace,monospace;font-size:.8rem}} small{{color:var(--color-text-muted,#666);font-size:.75rem}}
.grade-cores{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}}
.cor{{border:1px solid var(--color-border,#ddd);border-radius:8px;overflow:hidden;background:var(--color-surface,#fff)}}
.amostra{{height:88px;border-bottom:1px solid var(--color-border,#ddd)}}
.cor figcaption{{padding:10px 12px;display:grid;gap:2px;font-size:.8rem}} .cor em{{color:var(--color-text-muted,#666)}}
.cor ul{{list-style:none;font-size:.72rem;color:var(--color-text-muted,#666);margin-top:4px}}
.familia{{margin-bottom:16px}} .especime{{font-size:1.75rem;margin:4px 0}}
.linha-escala{{display:grid;grid-template-columns:200px 1fr;gap:16px;align-items:baseline;padding:10px 0;border-bottom:1px dashed var(--color-border,#ddd)}}
.linha-espaco{{display:grid;grid-template-columns:140px auto 1fr;gap:12px;align-items:center;padding:4px 0}}
.barra{{display:block;height:14px;background:var(--color-primary,#888);border-radius:2px}}
.grade-formas{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:20px}}
.forma{{height:96px;border:1px solid var(--color-border,#ccc);background:var(--color-surface,#fafafa);display:grid;place-content:center;text-align:center;gap:2px}}
.forma.sombra{{border-color:transparent;border-radius:var(--radius-md,8px)}}
table{{border-collapse:collapse}} td{{padding:6px 16px 6px 0;border-bottom:1px solid var(--color-border,#ddd);font-size:.875rem}}
.demo{{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-top:16px}}
.btn{{font:inherit;font-weight:600;cursor:pointer;padding:var(--space-3,12px) var(--space-6,24px);border-radius:var(--radius-md,8px);border:1px solid var(--color-primary)}}
.btn-prim{{background:var(--color-primary);color:#fff}} .btn-prim:hover{{background:var(--color-primary-hover,var(--color-primary))}}
.btn-sec{{background:transparent;color:var(--color-primary)}} .btn-sec:hover{{background:var(--color-surface,transparent)}}
.btn:focus-visible,.link:focus-visible,.campo input:focus-visible{{outline:2px solid var(--color-primary);outline-offset:2px}}
.link{{color:var(--color-primary)}}
.card{{max-width:320px;padding:var(--space-6,24px);background:var(--color-bg,#fff);border:1px solid var(--color-border,#ddd);border-radius:var(--radius-md,8px);box-shadow:var(--shadow-md,none)}}
.card h3{{font-family:var(--font-heading,inherit);font-size:var(--text-h3,1.25rem);margin-bottom:8px}}
.campo{{display:grid;gap:6px;font-size:var(--text-sm,.875rem);font-weight:500}}
.campo input{{font:inherit;font-weight:400;padding:var(--space-3,12px);border:1px solid var(--color-border,#ccc);border-radius:var(--radius-sm,4px);min-width:260px;background:var(--color-bg,#fff);color:inherit}}
@media (max-width:640px){{.linha-escala{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<main>
<header class="topo"><h1>{esc(titulo)}</h1>
<p>Visual version generated from <code>design_system.md</code> — don't edit this file; change the .md and generate again.</p></header>
{corpo}
</main>
</body>
</html>
"""
    Path(a.saida).write_text(pagina, encoding="utf-8")
    print(f"OK → {a.saida} ({len(unicos)} tokens)")


if __name__ == "__main__":
    main()
