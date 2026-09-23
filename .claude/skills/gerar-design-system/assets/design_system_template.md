# Design System — <Nome do site>

> Fonte única da verdade visual. Qualquer mudança de estilo é feita aqui primeiro.
> Tokens em tabelas com a coluna **Token** no formato `--nome` são convertidos
> automaticamente em `tokens.css` por `scripts/gerar_tokens.py`.

## Princípios
- <ex.: espaço generoso, pouca cor, foco no conteúdo>
- Referências: <Ref 2 (tipografia), Ref 3 (cores)>

## Paleta de cores
| Token | Valor | Uso |
|-------|-------|-----|
| `--color-primary` | #1A56DB | Botões primários, links |
| `--color-primary-hover` | #1E429F | Hover do primário |
| `--color-secondary` | #0E9F6E | Destaques |
| `--color-text` | #111827 | Texto principal |
| `--color-text-muted` | #6B7280 | Texto secundário |
| `--color-bg` | #FFFFFF | Fundo |
| `--color-surface` | #F9FAFB | Cards, seções alternadas |
| `--color-border` | #E5E7EB | Bordas |
| `--color-error` | #DC2626 | Erros |
| `--color-success` | #16A34A | Sucesso |

Contrastes verificados (WCAG AA ≥ 4.5:1 para texto):
| Combinação | Razão | OK? |
|------------|-------|-----|
| text sobre bg | | |
| branco sobre primary | | |

## Tipografia
| Token | Valor | Uso |
|-------|-------|-----|
| `--font-heading` | 'Inter', system-ui, sans-serif | Títulos |
| `--font-body` | 'Inter', system-ui, sans-serif | Texto |

Import: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`

| Token | Valor | Peso | Altura de linha | Uso |
|-------|-------|------|-----------------|-----|
| `--text-h1` | clamp(2.25rem, 5vw, 3rem) | 700 | 1.1 | Título do hero |
| `--text-h2` | 2.25rem | 700 | 1.2 | Título de seção |
| `--text-h3` | 1.5rem | 600 | 1.3 | Título de card |
| `--text-body` | 1rem | 400 | 1.6 | Texto |
| `--text-sm` | 0.875rem | 400 | 1.5 | Legendas, menu |

## Espaçamento (escala de 4px)
| Token | Valor |
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

Espaço vertical entre seções: `--space-24` desktop, `--space-16` mobile.

## Layout e breakpoints
| Token | Valor |
|-------|-------|
| `--container-max` | 1200px |
| `--container-padding` | 24px |
| `--bp-sm` | 640px |
| `--bp-md` | 768px |
| `--bp-lg` | 1024px |

Grid: 12 colunas, gap `--space-6`. Abordagem mobile-first.

## Bordas e sombras
| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-sm` | 4px | Inputs |
| `--radius-md` | 8px | Botões, cards |
| `--radius-full` | 999px | Pílulas, avatares |
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,.05) | Inputs |
| `--shadow-md` | 0 4px 12px rgba(0,0,0,.08) | Cards |

## Componentes
### Botão
| Variante | Fundo | Texto | Borda | Hover | Foco |
|----------|-------|-------|-------|-------|------|
| Primário | primary | branco | — | primary-hover | anel 2px primary, offset 2px |
| Secundário | transparente | primary | 1px primary | fundo surface | idem |
Padding `--space-3` × `--space-6`, `--radius-md`, `--text-body` 600.

### Card
Fundo bg, borda border, `--radius-md`, `--shadow-md`, padding `--space-6`.

### Input
...

## Movimento
Transições 150–200ms ease-out. Respeitar `prefers-reduced-motion`.

## Regras
- Não usar cores, tamanhos ou espaçamentos fora dos tokens.
- Todo elemento interativo tem estado de foco visível.
- Imagens com `alt` descritivo.
