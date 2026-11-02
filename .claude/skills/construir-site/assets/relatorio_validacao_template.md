# Validation report — <Project>

> Validated on: <date> · against `plano_construcao.md` (confirmed on <date>)
> Legend: ✅ passed · ❌ failed · ⚠️ not verified (reason)

## Summary
- **Plan sections:** <x of y> ✅
- **Checklist:** <x> ✅ · <y> ❌ · <z> ⚠️
- **Build:** <✅/❌> · **Docker:** <✅/❌/not applicable> · **Lighthouse:** <scores or ⚠️>
- **Open items for the user:** <n placeholders, n unverified items>

## 1. Plan item by item
| Page | Section | Result | Note |
|------|---------|--------|------|
| home | HEADER | ✅ | |
| home | HERO | ❌ → fixed | secondary button missing |

| Feature / delivery | Result | Note |
|--------------------|--------|------|
| Contact form | | |
| Dockerfile | | |

## 2. Checklist
### Design system
| Item | Result | Note |
|------|--------|------|
| No values outside the tokens | | search for loose `#`, `px`, `rgb(` |

### Responsiveness
| Item | 375px | 768px | 1280px |
|------|-------|-------|--------|
| No horizontal scrolling | | | |
| Working menu | | | |

### Accessibility
| Item | Result | Note |
|------|--------|------|
| One h1 per page / hierarchy | | |
| AA contrast | | |
| Visible focus and keyboard | | |
| alt / labels | | |
| prefers-reduced-motion | | |

### Performance and SEO
| Item | Result | Note |
|------|--------|------|
| title and meta description | | |
| Images with dimensions and lazy loading | | |
| Lighthouse | | |

### Content and rights
| Item | Result | Note |
|------|--------|------|
| Nothing copied from the references | | |

## 3. Browser
Screenshots in `etapas/06_construcao/screenshots/`.
| Page | 375px | 768px | 1280px | Console errors |
|------|-------|-------|--------|----------------|
| home | `home-375.png` | | | none |

## 4. Build and Docker
```
<commands run and result>
```

## Open items
- [ ] <placeholder or unverified item>
