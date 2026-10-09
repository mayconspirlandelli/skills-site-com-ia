# Prompts de imagens — <Projeto>

Gerado a partir de: `00_briefing/entrevista.md` (versão de <data>)
Ferramenta sugerida: <ChatGPT/DALL·E, Midjourney, Gemini/Imagen, Ideogram, Firefly...>

## Base comum (cole no início de cada prompt)

> Site <tipo: landing page | site institucional> para <público>, objetivo <objetivo>.
> Estilo: <tom da marca — ex.: moderno, acadêmico, acolhedor>. Paleta: <cores da marca ou "a definir">.
> Tipografia: <sans-serif geométrica | serifada...>. Sem textos legíveis inventados: use linhas de texto
> genéricas (lorem) e títulos curtos. Sem logos ou marcas de terceiros.

---

## 1. Mockups das páginas (referência visual)

Salvar as imagens geradas em `01_referencias/prints/gerados/`. Elas entram na etapa
`print-para-wireframe` como qualquer outro print — **nunca são a referência final**.

### <Página> — desktop
```
<base comum> Mockup de página web em tela desktop 1440px, vista frontal, flat, alta resolução.
Seções de cima para baixo: 1) HEADER com logo à esquerda, menu com <n> itens e botão <CTA>;
2) HERO <layout, ex.: 2 colunas, texto à esquerda e foto à direita>; 3) <SEÇÃO> <descrição>;
... ; N) FOOTER <descrição>. Espaçamento generoso, hierarquia clara, aparência profissional.
```

### <Página> — mobile
```
<base comum> Mockup da mesma página em tela de celular 390px, vista frontal.
Menu hambúrguer, seções empilhadas em 1 coluna na mesma ordem do desktop.
```

---

## 2. Imagens de conteúdo do site

Salvar em `05_site/assets/img/` (ou a pasta de imagens da stack). Use texto alternativo (`alt`) ao inserir.

| # | Onde entra | Formato | Prompt |
|---|-----------|---------|--------|
| 1 | HERO | 16:9, 1920×1080 | `<base comum> Fotografia/ilustração de <assunto>, <enquadramento>, <luz>, espaço livre à <esquerda/direita> para texto.` |
| 2 | <SEÇÃO> | 1:1, 800×800 | `<...>` |
| 3 | Ícones de <seção> | SVG/PNG transparente | `<...> conjunto de <n> ícones de linha, traço uniforme, estilo consistente.` |

---

## Observações

- Pessoas reais (ex.: egressos, equipe) **não** devem ser geradas por IA quando o site
  as apresenta como reais — use fotos autorizadas ou placeholders `[FOTO: ...]`.
- Itens marcados como "a definir" na entrevista ficam genéricos aqui e são revisados depois
  do design system.
