// Measures the styles the browser actually applied to the page (after the site's JavaScript runs).
// It's a single expression: run it with
//   playwright-cli --raw eval "$(cat .claude/skills/extrair-html-referencia/scripts/estilos_computados.js)" > computados-desktop.json
// and then summarize with scripts/resumir_computados.py.
// Only reads the page; changes nothing and sends no data anywhere.
(() => {
  const LIMITE_ELEMENTOS = 5000;
  const visivel = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0;
  };
  const transparente = (c) => !c || c === 'transparent' || /rgba?\([^)]*[,/]\s*0(\.0+)?\s*\)$/.test(c);
  const somar = (mapa, chave, peso = 1) => { if (chave) mapa[chave] = (mapa[chave] || 0) + peso; };
  const ranking = (mapa, n) => Object.entries(mapa).sort((a, b) => b[1] - a[1]).slice(0, n);

  const corTexto = {}, corFundo = {}, corBorda = {}, fontes = {}, tamanhos = {};
  const raios = {}, sombras = {}, largurasMax = {}, gaps = {};

  const elementos = [...document.body.querySelectorAll('*')].filter(visivel).slice(0, LIMITE_ELEMENTOS);
  for (const el of elementos) {
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const texto = [...el.childNodes]
      .filter((n) => n.nodeType === Node.TEXT_NODE)
      .map((n) => n.textContent.trim())
      .join('');
    if (texto) {
      somar(corTexto, s.color, texto.length);
      somar(fontes, s.fontFamily, texto.length);
      somar(tamanhos, `${s.fontSize} / ${s.fontWeight} / ${s.lineHeight}`, texto.length);
    }
    if (!transparente(s.backgroundColor)) {
      somar(corFundo, s.backgroundColor, Math.max(1, Math.round((r.width * r.height) / 1000)));
    }
    if (parseFloat(s.borderTopWidth) > 0 && s.borderTopStyle !== 'none' && !transparente(s.borderTopColor)) {
      somar(corBorda, s.borderTopColor);
    }
    if (s.borderRadius && s.borderRadius !== '0px') somar(raios, s.borderRadius);
    if (s.boxShadow && s.boxShadow !== 'none') somar(sombras, s.boxShadow);
    if (s.maxWidth && s.maxWidth.endsWith('px')) somar(largurasMax, s.maxWidth);
    if (s.gap && s.gap !== 'normal' && s.gap !== '0px') somar(gaps, s.gap);
  }

  // Page background: body or html, whichever isn't transparent.
  const fundoPagina = [document.body, document.documentElement]
    .map((el) => getComputedStyle(el).backgroundColor)
    .find((c) => !transparente(c)) || 'rgb(255, 255, 255)';

  // Style of a representative element for each role.
  const papeis = {
    body: 'body',
    h1: 'h1', h2: 'h2', h3: 'h3', h4: 'h4',
    paragraph: 'main p, p',
    link: 'main a, a',
    button: 'button, [role="button"], a[class*="btn"], a[class*="button"], .btn, .button',
    input: 'input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]), textarea, select',
    header: 'header',
    nav: 'nav',
    footer: 'footer',
    section: 'main section, section',
  };
  const estiloPapel = {};
  for (const [papel, seletor] of Object.entries(papeis)) {
    const el = [...document.querySelectorAll(seletor)].find(visivel);
    if (!el) continue;
    const s = getComputedStyle(el);
    estiloPapel[papel] = {
      tag: el.tagName.toLowerCase(),
      fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight,
      lineHeight: s.lineHeight, letterSpacing: s.letterSpacing, textTransform: s.textTransform,
      color: s.color, backgroundColor: s.backgroundColor,
      borderRadius: s.borderRadius, padding: s.padding, boxShadow: s.boxShadow,
    };
  }

  // CSS variables (:root) and breakpoints from the accessible stylesheets.
  const variaveis = {}, breakpoints = {};
  let folhasBloqueadas = 0;
  const raiz = getComputedStyle(document.documentElement);
  const percorrer = (regras) => {
    for (const regra of regras) {
      if (regra.selectorText && /(^|,)\s*(:root|html)\s*(,|$)/.test(regra.selectorText)) {
        for (const prop of regra.style) {
          if (prop.startsWith('--') && Object.keys(variaveis).length < 300) {
            variaveis[prop] = raiz.getPropertyValue(prop).trim() || regra.style.getPropertyValue(prop).trim();
          }
        }
      }
      if (regra.media) {
        const m = regra.media.mediaText.match(/(min|max)-width:\s*([\d.]+)(px|em|rem)/);
        if (m) somar(breakpoints, `${m[1]}-width: ${m[2]}${m[3]}`);
      }
      if (regra.cssRules) percorrer(regra.cssRules);
    }
  };
  for (const folha of document.styleSheets) {
    try { percorrer(folha.cssRules); } catch (e) { folhasBloqueadas += 1; }
  }

  return JSON.stringify({
    url: location.href,
    titulo: document.title,
    viewport: { largura: innerWidth, altura: innerHeight },
    elementos_analisados: elementos.length,
    fundo_pagina: fundoPagina,
    papeis: estiloPapel,
    cores_texto: ranking(corTexto, 15),
    cores_fundo: ranking(corFundo, 15),
    cores_borda: ranking(corBorda, 10),
    fontes: ranking(fontes, 10),
    tamanhos: ranking(tamanhos, 20),
    raios: ranking(raios, 10),
    sombras: ranking(sombras, 8),
    larguras_max: ranking(largurasMax, 8),
    gaps: ranking(gaps, 10),
    variaveis,
    breakpoints: ranking(breakpoints, 12),
    folhas_bloqueadas: folhasBloqueadas,
  });
})()
