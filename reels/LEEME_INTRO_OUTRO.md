# Reels Cráneo Noble — Intro y Outro de Marca (2 opciones)

Intro y outro generados con HyperFrames (1080×1920 · 30fps · sin voz · música ambiental).

## Logo oficial

El logo correcto es `reels/intro/assets/logo-correcto.svg` (cráneo con gradiente dorado + "CRÁNEO NOBLE" + "by ARCT" + tagline). Copias en `intro-dibujo/assets/logo-completo.svg`.

---

## Intros (2 opciones)

| Opción | Archivo | Duración | Descripción |
|---|---|---|---|
| **1 · Shimmer** | `reels/intro/renders/intro-craneo-noble.mp4` | 4.5s | Logo con glow dorado, barrido de luz (shimmer), wordmark + tagline |
| **2 · Dibujado** | `reels/intro-dibujo/renders/intro-dibujo-craneo-noble.mp4` | 6.2s | El cráneo se **traza como dibujado a mano** (SVG stroke animation de 27 paths) + wordmark |

## Outro de venta

| Archivo | Duración | Contenido |
|---|---|---|
| `reels/outro/renders/outro-craneo-noble.mp4` | 5.5s | **COMPRA AHORA** + "Pieza única · Solo una disponible" + WhatsApp **+52 444 510 1553** + URL |

---

## Videos completos (intro + reel + outro)

### V1 — Intro shimmer (4.5s) → 36s totales (`reels/finales/`)
- `hera-con-intro-outro.mp4`
- `alma-con-intro-outro.mp4`
- `espiritu-con-intro-outro.mp4`

### V2 — Intro dibujado (6.2s) → 37.7s totales (`reels/finales-v2/`)
- `hera-intro-dibujado.mp4`
- `alma-intro-dibujado.mp4`
- `espiritu-intro-dibujado.mp4`

---

## Re-renderizar un intro/outro

```bash
cd reels/intro && npx hyperframes render . --output renders/intro-craneo-noble.mp4 --quality high
cd reels/intro-dibujo && npx hyperframes render . --output renders/intro-dibujo-craneo-noble.mp4 --quality high
cd reels/outro && npx hyperframes render . --output renders/outro-craneo-noble.mp4 --quality high
```

## Re-concatenar

```bash
cd reels && ffmpeg -y -f concat -safe 0 -i <lista.txt> -c copy <salida.mp4>
# lista.txt:
#   file 'intro-dibujo/renders/intro-dibujo-craneo-noble.mp4'
#   file 'reel-hera/renders/hera-reel-final.mp4'
#   file 'outro/renders/outro-craneo-noble.mp4'
```

## Notas

- Los reels base (sin intro/outro) siguen en `reels/reel-*/renders/*-reel-final.mp4`.
- Drafts de baja calidad: `reels/reel-*/renders/drafts/`.
- Los intros/outros son reutilizables en cualquier video futuro de Cráneo Noble.
- Los textos de publicación de cada pieza están en `reels/TEXTOS_PUBLICACION.md`.
