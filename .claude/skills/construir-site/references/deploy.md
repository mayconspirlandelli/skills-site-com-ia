# Delivery: Docker and hosting

Choose according to the briefing (block F). All files live inside `site/`. Never deploy, push or publish without the user asking — here you only prepare the files and test locally.

## Docker

### Static site without a build (HTML + CSS / Tailwind via CDN)
`site/Dockerfile`:
```dockerfile
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
EXPOSE 80
```

### Site with a build (Vite, Astro)
Two-stage `site/Dockerfile` — Node only exists during the build; the final image is just Nginx:
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
    # Multi-page HTML site. For an SPA (React/Vue with browser routing), replace =404 with /index.html
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

### Test locally
```bash
cd site
docker build -t my-site .
docker run --rm -p 8080:80 my-site
# open http://localhost:8080
```

### Next.js in Docker
Next.js with a server isn't static: use `output: 'standalone'` in `next.config.js` and a Node image (not Nginx), following Next.js's official `with-docker` example. If the site doesn't need a server, prefer `output: 'export'` and the site-with-build Dockerfile above (`out` folder instead of `dist`).

## GitHub Pages

`site/` usually sits inside the repository; the workflow goes at the repo root: `.github/workflows/deploy.yml`.
```yaml
name: Deploy to GitHub Pages
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
      # With a build (Vite/Astro): uncomment
      # - uses: actions/setup-node@v4
      #   with: { node-version: 20, cache: npm, cache-dependency-path: site/package-lock.json }
      # - run: npm ci && npm run build
      #   working-directory: site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site          # with a build: site/dist
      - id: deployment
        uses: actions/deploy-pages@v4
```
- In Settings → Pages, choose "GitHub Actions" as the source.
- Project repository (`user.github.io/repo/`): in Vite, `base: '/repo/'`; in Astro, `base: '/repo'`.
- GitHub Pages doesn't run a server: static sites only.

## Netlify
`site/netlify.toml`:
```toml
[build]
  base = "site"
  command = "npm run build"   # remove if there is no build
  publish = "dist"            # without a build: "."
```
Simple forms can use Netlify Forms (`data-netlify="true"` on the `<form>`).

## Vercel
Detects Vite, Astro and Next.js on its own; set the root directory to `site` in the dashboard. `vercel.json` only if you need redirects or headers.

## Cloudflare Pages
Root directory `site`, build command `npm run build`, output `dist` (or `.` without a build).

## VPS / own server
Use the Docker image above behind a proxy with HTTPS (Caddy, Traefik or Nginx with Let's Encrypt). Without Docker: copy the build to the folder served by the server's Nginx.
