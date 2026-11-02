"""Builds the ZIP for upload to agensi.io.

Generated structure (SKILL.md at the root, required by the site):
  SKILL.md, INSTALL.md, LICENSE
  skills/<the other 9 skills>/
  template/  CLAUDE.md, .claude/settings.json, docs/, scripts/, etapas/, site/

Usage (from the repository root):
  python docs_agensi/montar_zip.py
Output: docs_agensi/dist/site-com-referencias.zip
"""
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AQUI = RAIZ / "docs_agensi"
SAIDA = AQUI / "dist" / "site-com-referencias.zip"
ORQUESTRADOR = "site-com-referencias"
IGNORAR = {"__pycache__", ".DS_Store"}
TEMPLATE = ["CLAUDE.md", ".claude/settings.json", "docs", "scripts", "etapas", "site"]


def versionados():
    """Git-tracked files only: leaves out the briefing, screenshots and site of projects in progress."""
    saida = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True)
    return {RAIZ / linha for linha in saida.stdout.splitlines()}


def arquivos(caminho: Path, git: set):
    candidatos = [caminho] if caminho.is_file() else sorted(caminho.rglob("*"))
    for p in candidatos:
        if p.is_file() and p in git and not (IGNORAR & set(p.parts)):
            yield p


def main():
    skills = RAIZ / ".claude" / "skills"
    orquestrador = skills / ORQUESTRADOR / "SKILL.md"
    if not orquestrador.exists():
        sys.exit(f"Could not find {orquestrador}")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    git = versionados()
    total = 0
    with zipfile.ZipFile(SAIDA, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(orquestrador, "SKILL.md")
        z.write(AQUI / "zip" / "INSTALL.md", "INSTALL.md")
        z.write(RAIZ / "LICENSE", "LICENSE")
        total += 3

        for pasta in sorted(p for p in skills.iterdir() if p.is_dir() and p.name != ORQUESTRADOR):
            if pasta.name not in SKILLS_PROPRIAS:
                continue  # never package third-party skills
            for f in arquivos(pasta, git):
                z.write(f, f"skills/{f.relative_to(skills).as_posix()}")
                total += 1

        for item in TEMPLATE:
            for f in arquivos(RAIZ / item, git):
                z.write(f, f"template/{f.relative_to(RAIZ).as_posix()}")
                total += 1

    print(f"{SAIDA.relative_to(RAIZ)}: {total} files, {SAIDA.stat().st_size / 1024:.0f} KB")


# Only this project's skills. Third-party skills (frontend-design, playwright-cli...) have
# their own licenses and are installed by the buyer via scripts/setup-skills.sh.
SKILLS_PROPRIAS = {
    "auditar-skill",
    "construir-site",
    "entrevista-site",
    "extrair-design-prints",
    "extrair-html-referencia",
    "gerar-design-system",
    "gerar-mockup",
    "gerar-previa",
    "gerar-wireframes",
}

if __name__ == "__main__":
    main()
