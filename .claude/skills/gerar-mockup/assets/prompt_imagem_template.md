# Prompt da imagem do site — <Projeto>

> Gerado a partir de: `etapas/02_previa/previa_site.md` (<data>)
> Gerador: <Nano Banana via MCP | SVG pelo Claude>

## Base comum (vai no início de todo prompt)

> Web design de alta qualidade para <tipo: landing page | site institucional> de <domínio de negócio>,
> voltado a <público>. Objetivo: <ação principal>. Clima: <três adjetivos da prévia>.
> Paleta: fundo <#hex>, texto <#hex>, cor principal <#hex>, apoio <#hex>.
> Tipografia: títulos em <categoria/fonte>, texto em <categoria/fonte>.
> Formas: <cantos, sombras, espaçamento>. Imagens: <fotos | ilustrações | ícones de linha>.
> Textos curtos e legíveis apenas nos títulos e botões; o resto como linhas de texto genéricas.
> Sem logos ou marcas reais de terceiros, sem marca-d'água.

## 1. Home — desktop
Formato: 16:10 (1440 × 900 visível; pode ser página longa, 1440 × ~3000)

```
<base comum>
Mockup frontal e plano da página inteira, tela desktop 1440px, sem moldura de navegador.
De cima para baixo:
1) HEADER — <da prévia>
2) HERO — <organização, título "<texto real ou curto>", botão "<CTA>", imagem de <assunto>>
3) <SEÇÃO> — <...>
...
N) FOOTER — <...>
Hierarquia clara, espaçamento <generoso>, alinhamento em grid de 12 colunas, contêiner de ~1200px.
```

## 2. Home — celular
Formato: 9:19.5 (390 × ~2400)

```
<base comum>
A mesma página em tela de celular 390px: menu hambúrguer, seções empilhadas em 1 coluna na mesma
ordem do desktop, botões com largura total, textos maiores que o normal para leitura no celular.
```

## 3. <Outra página> — desktop (opcional)
```
<base comum> ...
```

## Ajustes pedidos pelo usuário
| Versão | Pedido | Resultado |
|--------|--------|-----------|
| v1 → v2 | <ex.: hero com mais respiro, botão maior> | `mockup_home-desktop_v2.png` |

---

## Imagens de conteúdo (para usar no passo 8)

Imagens que entram no site — geradas depois, na construção, ou trocadas por fotos reais.
Destino: `site/` (pasta de imagens da stack). Sempre com texto alternativo (`alt`).

| # | Onde entra | Formato | Prompt |
|---|-----------|---------|--------|
| 1 | Hero | 16:9, 1920×1080 | `<base comum, sem a parte de layout> Fotografia/ilustração de <assunto>, <enquadramento>, <luz>, espaço livre à <esquerda/direita> para texto.` |
| 2 | <Seção> | 1:1, 800×800 | `<...>` |
| 3 | Ícones de <seção> | SVG | `conjunto de <n> ícones de linha, traço uniforme, estilo consistente` |

Pessoas reais que o site apresenta como reais (equipe, clientes, alunos) **não** são geradas por IA:
use fotos autorizadas ou `[FOTO: ...]`.
