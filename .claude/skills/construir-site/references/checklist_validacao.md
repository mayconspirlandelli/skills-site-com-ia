# Checklist de validação

## Fidelidade
- [ ] Todas as seções do wireframe existem, na ordem certa
- [ ] Quantidades batem (cards, itens de menu, logos)
- [ ] Tipografia e espaçamentos seguem a especificação

## Design system
- [ ] Nenhuma cor, tamanho ou espaçamento fora dos tokens (buscar `#`, `px` e `rgb(` soltos no CSS/JSX)
- [ ] Botões com todos os estados (hover, foco, ativo, desabilitado)
- [ ] Máximo de 2 famílias tipográficas carregadas

## Responsividade
- [ ] 375px (mobile), 768px (tablet), 1280px (desktop)
- [ ] Sem rolagem horizontal
- [ ] Menu mobile funcional
- [ ] Imagens não estouram o container

## Acessibilidade
- [ ] Um único `h1` por página; hierarquia de títulos correta
- [ ] Contraste AA (usar `contraste.py` da skill gerar-design-system)
- [ ] Foco visível e navegação completa por teclado
- [ ] `alt` em imagens; labels em inputs
- [ ] `prefers-reduced-motion` respeitado

## Performance e SEO
- [ ] `title` e `meta description` por página
- [ ] Imagens com `width`/`height` e `loading="lazy"` abaixo da dobra
- [ ] Fontes com `display=swap`
- [ ] Lighthouse: Performance, Acessibilidade, Boas práticas e SEO ≥ 90

## Conteúdo e direitos
- [ ] Nenhum texto, imagem, logo ou código copiado das referências
- [ ] Placeholders `[TEXTO: ...]` listados para o usuário preencher
