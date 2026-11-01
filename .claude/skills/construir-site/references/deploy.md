# Entrega: Docker e hospedagem

Escolha conforme o briefing (bloco F). Todos os arquivos ficam dentro de `site/`. Nunca faça deploy, push ou publicação sem o usuário pedir — aqui só se preparam os arquivos e se testa localmente.

## Docker

### Site estático sem build (HTML + CSS / Tailwind via CDN)
`site/Dockerfile`:
```dockerfile
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
EXPOSE 80
```

### Site com build (Vite, Astro)
`site/Dockerfile` em dois estágios — o Node só existe no build; a imagem final é só o Nginx:
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

### `site/nginx.conf`
```nginx
server {
  listen 80;
  root /usr/share/nginx/html;
  index index.html;

  gzip on;
  gzip_types text/css application/javascript image/svg+xml application/json;

  location / {
    # Site com várias páginas HTML. Para SPA (React/Vue com rotas no navegador), troque =404 por /index.html
    try_files $uri $uri/ $uri.html =404;
  }

  location ~* \.(css|js|woff2|png|jpg|jpeg|webp|avif|svg)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
  }
}
```

### `site/.dockerignore`
```
node_modules
dist
.git
*.log
.env
```

### Testar localmente
```bash
cd site
docker build -t meu-site .
docker run --rm -p 8080:80 meu-site
# abrir http://localhost:8080
```

### Next.js em Docker
Next.js com servidor não é estático: use `output: 'standalone'` no `next.config.js` e uma imagem Node (não Nginx), seguindo o exemplo oficial `with-docker` do Next.js. Se o site não precisa de servidor, prefira `output: 'export'` e o Dockerfile de site com build acima (pasta `out` em vez de `dist`).

## GitHub Pages

`site/` costuma estar dentro do repositório; o workflow fica na raiz do repo: `.github/workflows/deploy.yml`.
```yaml
name: Deploy no GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      # Com build (Vite/Astro): descomente
      # - uses: actions/setup-node@v4
      #   with: { node-version: 20, cache: npm, cache-dependency-path: site/package-lock.json }
      # - run: npm ci && npm run build
      #   working-directory: site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site          # com build: site/dist
      - id: deployment
        uses: actions/deploy-pages@v4
```
- Em Settings → Pages, escolha "GitHub Actions" como fonte.
- Repositório de projeto (`usuario.github.io/repo/`): no Vite, `base: '/repo/'`; no Astro, `base: '/repo'`.
- GitHub Pages não roda servidor: só sites estáticos.

## Netlify
`site/netlify.toml`:
```toml
[build]
  base = "site"
  command = "npm run build"   # remova se não houver build
  publish = "dist"            # sem build: "."
```
Formulários simples podem usar Netlify Forms (`data-netlify="true"` no `<form>`).

## Vercel
Detecta Vite, Astro e Next.js sozinho; defina o diretório raiz como `site` no painel. `vercel.json` só se precisar de redirecionamentos ou cabeçalhos.

## Cloudflare Pages
Diretório raiz `site`, comando de build `npm run build`, saída `dist` (ou `.` sem build).

## VPS / servidor próprio
Use a imagem Docker acima atrás de um proxy com HTTPS (Caddy, Traefik ou Nginx com Let's Encrypt). Sem Docker: copie o build para a pasta servida pelo Nginx do servidor.
