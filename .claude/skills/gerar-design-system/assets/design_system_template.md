# Design System — <Site name>

> Single visual source of truth. Any style change is made here first.
> Tokens in tables whose **Token** column uses the `--name` format are converted
> automatically into `tokens.css` by `scripts/gerar_tokens.py`.

## Principles
- <e.g. generous space, little color, focus on content>
- References: <Ref 2 (typography), Ref 3 (colors)>

## Color palette
| Token | Value | Use |
|-------|-------|-----|
| `--color-primary` | #1A56DB | Primary buttons, links |
| `--color-primary-hover` | #1E429F | Primary hover |
| `--color-secondary` | #0E9F6E | Highlights |
| `--color-text` | #111827 | Main text |
| `--color-text-muted` | #6B7280 | Secondary text |
| `--color-bg` | #FFFFFF | Background |
| `--color-surface` | #F9FAFB | Cards, alternating sections |
| `--color-border` | #E5E7EB | Borders |
| `--color-error` | #DC2626 | Errors |
| `--color-success` | #16A34A | Success |

Verified contrast (WCAG AA ≥ 4.5:1 for text):
| Combination | Ratio | OK? |
|-------------|-------|-----|
| text on bg | | |
| white on primary | | |

## Typography
| Token | Value | Use |
|-------|-------|-----|
| `--font-heading` | 'Inter', system-ui, sans-serif | Headings |
| `--font-body` | 'Inter', system-ui, sans-serif | Body |

Import: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`

| Token | Value | Weight | Line height | Use |
|-------|-------|--------|-------------|-----|
| `--text-h1` | clamp(2.25rem, 5vw, 3rem) | 700 | 1.1 | Hero heading |
| `--text-h2` | 2.25rem | 700 | 1.2 | Section heading |
| `--text-h3` | 1.5rem | 600 | 1.3 | Card heading |
| `--text-body` | 1rem | 400 | 1.6 | Body |
| `--text-sm` | 0.875rem | 400 | 1.5 | Captions, menu |

## Spacing (4px scale)
| Token | Value |
|-------|-------|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-12` | 48px |
| `--space-16` | 64px |
| `--space-24` | 96px |

Vertical space between sections: `--space-24` desktop, `--space-16` mobile.

## Layout and breakpoints
| Token | Value |
|-------|-------|
| `--container-max` | 1200px |
| `--container-padding` | 24px |
| `--bp-sm` | 640px |
| `--bp-md` | 768px |
| `--bp-lg` | 1024px |

Grid: 12 columns, gap `--space-6`. Mobile-first approach.

## Borders and shadows
| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 4px | Inputs |
| `--radius-md` | 8px | Buttons, cards |
| `--radius-full` | 999px | Pills, avatars |
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,.05) | Inputs |
| `--shadow-md` | 0 4px 12px rgba(0,0,0,.08) | Cards |

## Components
### Button
| Variant | Background | Text | Border | Hover | Focus |
|---------|------------|------|--------|-------|-------|
| Primary | primary | white | — | primary-hover | 2px primary ring, 2px offset |
| Secondary | transparent | primary | 1px primary | surface background | same |
Padding `--space-3` × `--space-6`, `--radius-md`, `--text-body` 600.

### Card
bg background, border border, `--radius-md`, `--shadow-md`, padding `--space-6`.

### Input
...

## Motion
150–200ms ease-out transitions. Respect `prefers-reduced-motion`.

## Rules
- Don't use colors, sizes or spacing outside the tokens.
- Every interactive element has a visible focus state.
- Images with descriptive `alt`.
