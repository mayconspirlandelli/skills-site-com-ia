# Publishing on agensi.io

Material for selling the **Site from References** skill on agensi.io. This folder is versioned only
on the `agensi` branch; on `main` it is in `.gitignore`.

| File | Purpose |
|------|---------|
| `anuncio_en.md` | Every form field, ready to paste |
| `montar_zip.py` | Builds the upload ZIP at `dist/site-com-referencias.zip` (ignored by git) |
| `zip/INSTALL.md` | Installation guide that goes inside the ZIP |
| `logo.svg` | 512×512 logo (export to PNG) |

## Publishing checklist

1. **Build the ZIP:** `python docs_agensi/montar_zip.py` (from the repository root). It takes only
   git-tracked files and only the 10 project skills — never third-party ones.
2. **Logo:** open `logo.svg` in the browser or in Figma/Inkscape and export a 512×512 PNG.
3. **Fill in the form** field by field with `anuncio_en.md`.
4. **Demo (step 3):** the example is representative. Run a real session (e.g. the pilates studio)
   and replace it with the real numbers and files — it's what converts best.
5. **Screenshots:** the suggested list is at the end of the listing; `docs/diagrama-processo.png` already exists.
6. **30 s video** (optional, the site says it doubles conversion): script at the end of the listing.
7. Submit for review.

## ⚠️ Decide before setting the price

- **The repository is public and MIT-licensed.** Anyone can download the same content for free on
  GitHub, and MIT allows resale. Options:
  - make the repository private (and remove the documentation link from the listing);
  - keep the template public and free, and sell on agensi a version with something extra
    (e.g. a complete real example session, extra templates, support);
  - publish on agensi as **Free** for visibility.
  The LICENSE (MIT) goes inside the ZIP; if you change the license of the paid version, replace the file before building the ZIP.
- **Price suggestion** (one-time purchase): US$ 19–29, considering the 10-skill bundle and the niche.
