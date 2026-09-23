# Notas por stack

## HTML + CSS puro
- `index.html` + `css/tokens.css` + `css/base.css` + `css/components.css`.
- Classes com prefixo por componente (`.btn`, `.btn--primary`, `.card`, `.hero__title`).
- Um arquivo por página; header/footer repetidos (ou incluídos via build simples).

## HTML + Tailwind
- Incluir `tokens.css` e estender o tema com `tailwind.tokens.js` (`theme.extend`).
- Usar as classes do tema (`bg-primary`, `p-6`, `rounded-md`), não valores arbitrários (`bg-[#1A56DB]`).
- Via CDN (prototipação): `<script src="https://cdn.tailwindcss.com"></script>` + `tailwind.config = { theme: { extend: {...} } }` inline.

## React / Next.js
- Um componente por seção (`Hero.jsx`, `Features.jsx`) e componentes de UI reutilizáveis (`Button`, `Card`).
- Conteúdo em um arquivo de dados (`content.js`) separado dos componentes, facilitando trocar textos.
- `tokens.css` importado no layout raiz.
- Next.js: `next/font` para as fontes do design system; `next/image` para imagens.

## WordPress
- Gerar tema de blocos (`theme.json`) mapeando os tokens para `settings.color.palette`, `settings.typography` e `settings.spacing`.
- Padrões de bloco (block patterns) para cada seção do wireframe.
