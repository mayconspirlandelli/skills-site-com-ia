# Relatório de validação — <Projeto>

> Validado em: <data> · contra `plano_construcao.md` (confirmado em <data>)
> Legenda: ✅ passou · ❌ falhou · ⚠️ não verificado (motivo)

## Resumo
- **Seções do plano:** <x de y> ✅
- **Checklist:** <x> ✅ · <y> ❌ · <z> ⚠️
- **Build:** <✅/❌> · **Docker:** <✅/❌/não se aplica> · **Lighthouse:** <notas ou ⚠️>
- **Pendências para o usuário:** <n placeholders, n itens não verificados>

## 1. Plano item a item
| Página | Seção | Resultado | Observação |
|--------|-------|-----------|------------|
| home | HEADER | ✅ | |
| home | HERO | ❌ → corrigido | botão secundário faltando |

| Funcionalidade / entrega | Resultado | Observação |
|--------------------------|-----------|------------|
| Formulário de contato | | |
| Dockerfile | | |

## 2. Checklist
### Design system
| Item | Resultado | Observação |
|------|-----------|------------|
| Nenhum valor fora dos tokens | | busca por `#`, `px`, `rgb(` soltos |

### Responsividade
| Item | 375px | 768px | 1280px |
|------|-------|-------|--------|
| Sem rolagem horizontal | | | |
| Menu funcional | | | |

### Acessibilidade
| Item | Resultado | Observação |
|------|-----------|------------|
| Um h1 por página / hierarquia | | |
| Contraste AA | | |
| Foco visível e teclado | | |
| alt / labels | | |
| prefers-reduced-motion | | |

### Performance e SEO
| Item | Resultado | Observação |
|------|-----------|------------|
| title e meta description | | |
| Imagens com dimensões e lazy | | |
| Lighthouse | | |

### Conteúdo e direitos
| Item | Resultado | Observação |
|------|-----------|------------|
| Nada copiado das referências | | |

## 3. Navegador
Screenshots em `etapas/06_construcao/screenshots/`.
| Página | 375px | 768px | 1280px | Erros no console |
|--------|-------|-------|--------|------------------|
| home | `home-375.png` | | | nenhum |

## 4. Build e Docker
```
<comandos rodados e resultado>
```

## Pendências
- [ ] <placeholder ou item não verificado>
