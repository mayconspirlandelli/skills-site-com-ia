---
name: referencias-briefing
description: Conduz o briefing de um novo site e a coleta estruturada de sites de referência, gerando briefing.md e referencias.md. Use quando o usuário estiver começando um projeto de site, listar URLs de inspiração, disser "quero um site parecido com X", ou quando for preciso definir objetivo, público, páginas e stack antes de desenhar ou codificar um site.
---

# Briefing e referências

Objetivo: sair desta etapa com dois arquivos que respondem "o que vamos construir" e "de onde vem a inspiração, e por quê".

## Parte 1 — Briefing

Sem briefing, a IA mistura estilos das referências sem critério. Colete as informações abaixo. Pergunte de forma conversacional, em blocos pequenos (no máximo 3 perguntas por vez), e aproveite o que o usuário já disse na conversa — não pergunte de novo.

Informações necessárias:
- Objetivo do site (vender, captar leads, portfólio, institucional, blog)
- Público-alvo
- Páginas e, para cada uma, as seções previstas
- Conteúdo disponível (textos, logo, fotos, depoimentos)
- Stack de saída (HTML/CSS, Tailwind, React, Next.js, WordPress...). Se o usuário não souber, sugira HTML + Tailwind para sites simples.
- Tom da marca (sério, divertido, minimalista, premium, técnico)
- Restrições (cores obrigatórias da marca, acessibilidade, prazo)

Se `etapas/00_briefing/entrevista.md` existir (entrevista feita com a `grill-me` no setup), use-o como base e pergunte apenas o que ainda faltar.

Se o usuário não souber algo, registre como "a definir" e siga em frente — não trave o processo.

Gere `etapas/00_briefing/briefing.md` usando o modelo em `assets/briefing_template.md`.

## Parte 2 — Referências

Peça **3 a 5 sites de referência**. Para cada um, o usuário precisa dizer **o que aproveitar** e **o que evitar**. Isso é o mais importante desta etapa: uma URL sem justificativa faz a IA copiar tudo, inclusive o que o usuário não gosta.

Se o usuário mandar só URLs, pergunte o que ele gosta em cada uma. Se ele não souber explicar, ofereça opções concretas: "é o layout, a tipografia, as cores, o espaçamento, as animações ou a forma de apresentar o conteúdo?"

Boas práticas para orientar o usuário:
- Referências por aspecto funcionam melhor (uma para layout, outra para tipografia, outra para cor).
- Preferir sites do mesmo segmento ou com o mesmo objetivo.
- Indicar páginas específicas (`/precos`, `/sobre`), não só a home.
- Pedir prints das seções que ele mais gosta — eles serão usados na etapa de wireframe.

Gere `etapas/00_briefing/referencias.md` usando `assets/referencias_template.md`.

## Validação antes de avançar

- Toda referência tem "aproveitar" e "evitar" preenchidos.
- Nenhuma contradição óbvia (ex.: tom "minimalista" + referência escolhida pelo excesso de animações). Se houver, aponte ao usuário.
- Cada página do briefing tem pelo menos uma referência de layout associada.

Próxima etapa: `extrair-html-referencia`.
