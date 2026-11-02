# Build plan — <Project>

> Based on: briefing (approved <date>) · wireframes (approved <date>) · design system (approved <date>)
> Status: <draft | confirmed by the user on <date>>

## Stack and structure
- **Stack:** <e.g. Vite + Tailwind>
- **Node / package manager:** <e.g. Node 20, npm>

```
site/
├── <the stack's folder structure>
└── ...
```

## Tokens
- `tokens.css` generated at `site/<path>/tokens.css` by `gerar_tokens.py` (regenerate when the design system changes)
- <Tailwind: `tailwind.tokens.js` in `theme.extend`>
- Fonts: <family — how to load (Google Fonts with display=swap / self-host)>

## Pages and sections (validation checklist)
| Page | # | Section | Layout (wireframe) | Components | Done |
|------|---|---------|--------------------|------------|------|
| home | 1 | HEADER | 3 zones | Logo, Menu, Button | [ ] |
| home | 2 | HERO | 2 columns 50/50 | Primary/secondary button | [ ] |

## Reusable components
| Component | Variants / states | Where it appears |
|-----------|-------------------|------------------|
| Button | primary, secondary · hover, focus, disabled | header, hero, CTA |

## Content
| Page / section | Content | Source |
|----------------|---------|--------|
| home / hero | heading, subheading | briefing |

**Placeholders for the user to fill in**
- [ ] `[TEXT: ...]` — <where>
- [ ] `[PHOTO: ...]` — <where>

## Features
| Feature | How it will be done |
|---------|---------------------|
| <Contact form> | <e.g. Formspree / Netlify Forms / own backend> |

## Delivery
- **Hosting:** <...>
- **Docker:** <no | yes — Nginx serving the static build>
- **Files:** <Dockerfile, nginx.conf, .dockerignore, .github/workflows/deploy.yml, netlify.toml...>
- **Automatic deploy:** <...>

## Acceptance criteria
- Every section above exists, in order and with the wireframes' quantities
- Tokens only in the code; AA contrast
- No horizontal scrolling at 375 / 768 / 1280px; working mobile menu
- Build without errors <and `docker build` + container serving the site>
- Lighthouse ≥ 90 in Performance, Accessibility, Best Practices and SEO

## Build order
1. Base (folders, tokens, global styles)
2. Header and footer
3. Home sections, one at a time
4. Other pages
5. Features
6. Delivery files
7. Validation

## Assumptions
- <e.g. About page text not provided yet — placeholders>
