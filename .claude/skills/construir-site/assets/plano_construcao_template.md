# Plano de construção — <Projeto>

> Baseado em: briefing (aprovado <data>) · wireframes (aprovados <data>) · design system (aprovado <data>)
> Status: <rascunho | confirmado pelo usuário em <data>>

## Stack e estrutura
- **Stack:** <ex.: Vite + Tailwind>
- **Node / gerenciador:** <ex.: Node 20, npm>

```
site/
├── <estrutura de pastas da stack>
└── ...
```

## Tokens
- `tokens.css` gerado em `site/<caminho>/tokens.css` por `gerar_tokens.py` (regenerar quando o design system mudar)
- <Tailwind: `tailwind.tokens.js` em `theme.extend`>
- Fontes: <família — como carregar (Google Fonts com display=swap / self-host)>

## Páginas e seções (checklist da validação)
| Página | # | Seção | Layout (wireframe) | Componentes | Feito |
|--------|---|-------|--------------------|-------------|-------|
| home | 1 | HEADER | 3 zonas | Logo, Menu, Botão | [ ] |
| home | 2 | HERO | 2 colunas 50/50 | Botão primário/secundário | [ ] |

## Componentes reutilizáveis
| Componente | Variantes / estados | Onde aparece |
|------------|---------------------|--------------|
| Botão | primário, secundário · hover, foco, desabilitado | header, hero, CTA |

## Conteúdo
| Página / seção | Conteúdo | Origem |
|----------------|----------|--------|
| home / hero | título, subtítulo | briefing |

**Placeholders a preencher pelo usuário**
- [ ] `[TEXTO: ...]` — <onde>
- [ ] `[FOTO: ...]` — <onde>

## Funcionalidades
| Funcionalidade | Como será feita |
|----------------|-----------------|
| <Formulário de contato> | <ex.: Formspree / Netlify Forms / backend próprio> |

## Entrega
- **Hospedagem:** <...>
- **Docker:** <não | sim — Nginx servindo o build estático>
- **Arquivos:** <Dockerfile, nginx.conf, .dockerignore, .github/workflows/deploy.yml, netlify.toml...>
- **Deploy automático:** <...>

## Critérios de aceite
- Todas as seções acima existem, na ordem e com as quantidades dos wireframes
- Só tokens no código; contraste AA
- Sem rolagem horizontal em 375 / 768 / 1280px; menu do celular funcional
- Build sem erros <e `docker build` + container servindo o site>
- Lighthouse ≥ 90 em Performance, Acessibilidade, Boas práticas e SEO

## Ordem de construção
1. Base (pastas, tokens, estilos globais)
2. Header e footer
3. Seções da Home, uma por vez
4. Demais páginas
5. Funcionalidades
6. Arquivos de entrega
7. Validação

## Suposições
- <ex.: textos da página Sobre ainda não fornecidos — placeholders>
