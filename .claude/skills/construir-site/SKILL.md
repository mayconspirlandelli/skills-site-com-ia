---
name: construir-site
description: Constrói o código de um site seção por seção seguindo design_system.md, tokens.css, wireframes e especificação de componentes, e depois valida responsividade, acessibilidade e conteúdo. Use sempre que for gerar ou editar páginas, seções ou componentes de um site que já tenha design system ou wireframes, quando o usuário pedir "agora cria o site", "monta a página", "cria o hero/header/footer", ou pedir para revisar/validar o site gerado.
---

# Construir o site

## Antes de escrever qualquer código

Leia sempre, nesta ordem:
1. `04_design_system/design_system.md` e `tokens.css`
2. `03_wireframes/wireframe_<pagina>.md`
3. `03_wireframes/especificacao_componentes.md`
4. `00_briefing/briefing.md` (stack, conteúdo real)

Se o design system não existir, pare e avise: sem ele o site fica genérico e inconsistente. Ofereça rodar `gerar-design-system` rapidamente.

## Regras de código

- **Só tokens.** Cores, fontes, tamanhos, espaços, raios e sombras vêm de `tokens.css` (ou das classes Tailwind geradas a partir dele). Nada de hex ou px soltos. Se precisar de um valor novo, proponha adicioná-lo ao design system primeiro.
- **HTML semântico:** `header`, `nav`, `main`, `section` com `aria-labelledby`, `footer`, um único `h1` por página, hierarquia de títulos sem pular níveis.
- **Mobile-first**, seguindo o comportamento responsivo da especificação.
- **Acessibilidade:** foco visível, `alt` em imagens, labels em inputs, área de toque ≥ 44px, `prefers-reduced-motion`.
- **Conteúdo:** usar os textos do briefing. Onde faltar, usar placeholder claramente marcado (`[TEXTO: proposta de valor]`) — nunca textos, imagens ou logos das referências.
- Siga a stack do briefing. Para detalhes de cada stack, veja `references/stacks.md`.

## Ordem de construção

Gerar tudo de uma vez produz resultados genéricos. Construa em partes, conferindo cada uma:

1. **Base:** estrutura de arquivos, `tokens.css` importado, estilos globais (reset, tipografia base, container).
2. **Header e footer.**
3. **Uma seção por vez**, na ordem do wireframe. Ao terminar cada seção:
   - confira contra o wireframe (elementos, quantidades, alinhamento);
   - confira contra a especificação (tipografia, espaçamento, estados, responsivo);
   - mostre ao usuário e aplique ajustes antes da próxima.
   Se o usuário preferir velocidade, agrupe 2–3 seções por rodada, mas mantenha a conferência.
4. **Demais páginas**, reutilizando componentes já feitos.

Quando um ajuste do usuário for de estilo (cor, fonte, espaçamento), atualize o `design_system.md` e regenere os tokens, em vez de corrigir só no CSS.

## Validação final

Rode o checklist em `references/checklist_validacao.md` e entregue ao usuário o resultado com o que passou, o que falhou e o que foi corrigido. Se houver ferramentas disponíveis (navegador, Lighthouse, axe), use-as; caso contrário, faça a revisão pelo código e indique ao usuário como rodar o Lighthouse (DevTools → aba Lighthouse → Analyze).
