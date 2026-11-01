# Notas por stack

Todo o código fica em `site/`. Em qualquer stack, `tokens.css` é gerado pelo `gerar_tokens.py` direto no caminho indicado abaixo — nunca copiado à mão.

## HTML + CSS puro
- `site/index.html`, uma página por arquivo (`sobre.html`, `contato.html`).
- `site/css/tokens.css` (gerado) + `base.css` + `components.css`.
- Classes por componente (`.btn`, `.btn--primary`, `.card`, `.hero__title`).
- Header e footer repetidos em cada página (ou um build simples, se forem muitas páginas).

## HTML + Tailwind
- Mesmo arranjo de páginas; `tokens.css` incluído e o tema estendido com `tailwind.tokens.js` (`theme.extend`).
- Use as classes do tema (`bg-primary`, `p-6`, `rounded-md`), não valores arbitrários (`bg-[#1A56DB]`).
- Produção: Tailwind CLI ou Vite. CDN (`cdn.tailwindcss.com`) só para protótipo.

## Vite (+ Tailwind, com ou sem React/Vue/Svelte)
- `npm create vite@latest site` e escolha o template; o build sai em `site/dist`.
- `site/src/styles/tokens.css` (gerado), importado no ponto de entrada (`main.js`/`main.jsx`).
- Várias páginas sem framework: liste cada HTML em `build.rollupOptions.input` no `vite.config.js`.
- Com React/Vue: um componente por seção (`Hero.jsx`) e componentes de UI (`Button`, `Card`); conteúdo num arquivo de dados (`content.js`) separado.

## Astro
- `npm create astro@latest site`; páginas em `src/pages/`, seções em `src/components/`.
- `src/styles/tokens.css` (gerado) importado no layout base (`src/layouts/Base.astro`).
- Bom para sites com várias páginas e foco em SEO: gera HTML estático por padrão (`dist/`).

## Next.js
- App Router: seções em `app/components/`, `tokens.css` importado em `app/layout.js`.
- `next/font` para as fontes do design system; `next/image` para imagens.
- Estático (`output: 'export'`) se não precisar de servidor — funciona em qualquer hospedagem estática.

## PWA (app instalável)
Se o briefing pediu PWA: `manifest.webmanifest` (nome, cores do design system, ícones 192 e 512px), `<link rel="manifest">` e um service worker. Com Vite, use o plugin `vite-plugin-pwa`. Teste a instalação no Lighthouse (categoria PWA / "Installable").

## WordPress
- Tema de blocos (`theme.json`) mapeando os tokens para `settings.color.palette`, `settings.typography` e `settings.spacing`.
- Block patterns para cada seção dos wireframes.
