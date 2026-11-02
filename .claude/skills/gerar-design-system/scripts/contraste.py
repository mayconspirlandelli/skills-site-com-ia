#!/usr/bin/env python3
"""
Computes the WCAG contrast ratio between pairs of hex colors.

Usage:
  python contraste.py "#111827:#FFFFFF" "#FFFFFF:#1A56DB"
Format of each pair: TEXT:BACKGROUND
"""
import sys


def lum(hexcor):
    h = hexcor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    canais = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        canais.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


if __name__ == "__main__":
    # Avoids garbled characters on Windows consoles (cp1252).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print("| Text | Background | Ratio | AA text (4.5) | AA large (3.0) |")
    print("|------|------------|-------|---------------|----------------|")
    for par in sys.argv[1:]:
        t, f = par.split(":")
        r = razao(t, f)
        print(f"| {t} | {f} | {r:.2f}:1 | {'✅' if r >= 4.5 else '❌'} | {'✅' if r >= 3 else '❌'} |")
