# Estrategia de Publicación — Cráneo Noble

## Producto
- **Pieza:** Hera (colección Cráneo Noble #01)
- **Artista:** Patricia Torres
- **Precio debut:** $1,800 MXN
- **Próximas piezas:** desde $4,500 MXN
- **WhatsApp:** +52 444 510 1553

## Estado actual
- Campaña de 7 posts en Facebook
- 1 post/día
- Publicación automática via `scripts/publicar-programado.js`
- Estado guardado en `.campana-state.json`
- La campaña se detiene cuando el usuario dice que Hera se vendió

## Estructura
```
37-craneo-nobles/
├── .config.json                 # Token de Facebook
├── .campana-state.json          # Estado de la campaña (día actual)
├── contenido/dia{1-7}/          # Imagen para cada día
├── marketing/
│   ├── campana-hera.md          # Los 7 copys completos
│   └── respuestas-comerciales.md # Respuestas para leads
├── scripts/
│   ├── post.js                  # Publicador vía API
│   └── publicar-programado.js   # Programador diario
└── sales/
    └── leads.md                 # Seguimiento de leads
```

## Cómo operar
```bash
# Ver estado
node scripts/publicar-programado.js --status

# Publicar el siguiente día
node scripts/publicar-programado.js

# Reiniciar campaña (si se vendió y hay nueva pieza)
node scripts/publicar-programado.js --reset
```

## Reglas
- Cuando Hera se venda: actualizar `.campana-state.json` → `estado: "VENDIDA"`
- No detener la campaña hasta instrucción explícita del usuario
- Cada post es único, no repetir copys aunque la imagen se repita
- Tono: premium, artístico, de colección
