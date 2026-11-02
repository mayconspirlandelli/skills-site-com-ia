# Validation checklist

## Fidelity
- [ ] Every wireframe section exists, in the right order
- [ ] Quantities match (cards, menu items, logos)
- [ ] Typography and spacing follow the specification

## Design system
- [ ] No color, size or spacing outside the tokens (search for loose `#`, `px` and `rgb(` in CSS/JSX)
- [ ] Buttons with every state (hover, focus, active, disabled)
- [ ] At most 2 font families loaded

## Responsiveness
- [ ] 375px (mobile), 768px (tablet), 1280px (desktop)
- [ ] No horizontal scrolling
- [ ] Working mobile menu
- [ ] Images don't overflow the container

## Accessibility
- [ ] A single `h1` per page; correct heading hierarchy
- [ ] AA contrast (use `contraste.py` from the gerar-design-system skill)
- [ ] Visible focus and full keyboard navigation
- [ ] `alt` on images; labels on inputs
- [ ] `prefers-reduced-motion` respected

## Performance and SEO
- [ ] `title` and `meta description` per page
- [ ] Images with `width`/`height` and `loading="lazy"` below the fold
- [ ] Fonts with `display=swap`
- [ ] Lighthouse: Performance, Accessibility, Best Practices and SEO ≥ 90

## Delivery
- [ ] Build without errors (`npm run build`, if there is a build)
- [ ] Docker (if requested): `docker build` passes and the container serves the site at `http://localhost:8080`
- [ ] Deploy files for the chosen hosting created (workflow, `netlify.toml`...)
- [ ] `site/` contains only production files (no `etapas/`, `.env` or drafts)

## Content and rights
- [ ] No text, image, logo or code copied from the references
- [ ] `[TEXT: ...]` placeholders listed for the user to fill in
