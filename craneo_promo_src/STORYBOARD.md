# STORYBOARD

**Format:** 1080×1920 (Vertical for TikTok/Reels)
**Audio:** TTS voiceover (female, deep, elegant, slow pace) + Dark/ambient underscore
**VO direction:** Solemne, misteriosa, elegante. Pausas marcadas entre frases para dejar respirar lo visual.
**Style basis:** DESIGN.md (Fondo negro #0C0C0C, Acentos #C9A96E, Playfair Display y Outfit).

---

### BEAT 1 — HOOK (0:00 - 0:04)

**VO:** "Arte. Raíz. Carácter. Trascendencia."

**Mood:** Misterio, aparición desde la oscuridad.
**Visual:** El lienzo inicia completamente en negro (The Void). Aparecen las cuatro palabras clave de forma secuencial, sincronizadas con el VO y con efecto de desvanecimiento suave. La tipografía es `Playfair Display` en color plata/hueso (`#E8E6E3`). Cada palabra emerge del negro absoluto mediante una transición sutil de opacidad (0 a 1) y un ligero escalado (0.95 a 1). En la palabra "Trascendencia", el título se desliza suavemente hacia arriba.
**Transition OUT:** Difuminado lento a negro absoluto (Opacity 1 a 0) en 0.8s.

---

### BEAT 2 — LA REVELACIÓN (0:04 - 0:08)

**VO:** "Cráneos naturales transformados en obras de arte."

**Mood:** Impacto visual, textura y materialidad.
**Visual:** La imagen principal de Hera (`IMG_1810.PNG`) aparece del fondo negro con un leve acercamiento constante (Ken Burns 1.0 -> 1.05). Un haz de luz radial dorado (`#C9A96E`) ilumina la imagen sutilmente por detrás, dándole una sensación tridimensional y mística. Texto en `Outfit` con tracking alto (espaciado de letras ancho), flotando delicadamente por debajo del cráneo.
**Transition IN:** Fade-in lento desde negro (0.8s).
**Transition OUT:** Transición dura (Hard Cut) sincronizada con el inicio de la siguiente frase.

---

### BEAT 3 — EL DETALLE Y EL ARTISTA (0:08 - 0:13)

**VO:** "Intervenidas a mano por Patricia Torres. Piezas únicas. Irrepetibles."

**Mood:** Exclusividad y detalle.
**Visual:** Acercamiento a texturas de plata y cristales de *Alma de Plata* (`alma-hero.jpg`). La imagen está ligeramente oscurecida (brightness: 0.8) y tiene un Ken Burns de paneo horizontal leve. El texto "Patricia Torres" aparece en `Playfair Display` dorado (`#C9A96E`) cursiva, como si fuera una firma luminosa, superpuesto sobre la imagen con un efecto de escritura a mano (SVG path drawing o clip-path animado de izquierda a derecha). Las palabras "Únicas. Irrepetibles." aparecen secuencialmente en seco (staggered text) en color `#E8E6E3`.
**Transition IN:** Hard cut.
**Transition OUT:** Flash blanco/plata sutil (0.2s) que funde a la siguiente escena.

---

### BEAT 4 — LA COLECCIÓN (0:13 - 0:17)

**VO:** "Hera. Alma de Plata. Espíritu Libre."

**Mood:** Magnificencia, ritmo acelerado pero elegante.
**Visual:** Tríptico vertical (o secuencia rápida). Se muestran imágenes de las tres piezas (`IMG_1810.PNG`, `alma-hero.jpg`, `alma-libre-01.jpg`) de forma secuencial o rotativa. En el centro, el nombre de la colección en tipografía masiva (`Playfair Display` Bold). Usamos un efecto de resplandor oscuro o *glow* suave alrededor del texto dorado.
**Transition IN:** Flash de 0.2s.
**Transition OUT:** Zoom-through hacia la letra central, haciendo que todo se vuelva negro nuevamente.

---

### BEAT 5 — EL CIERRE (0:17 - 0:20)

**VO:** "Cráneo Noble. Una declaración de trascendencia."

**Mood:** Silencio reverencial y autoridad.
**Visual:** Fondo completamente negro (`#0C0C0C`). El logo de Cráneo Noble (o en su defecto el texto majestuoso "CRÁNEO NOBLE" en mayúsculas `Playfair Display` dorado `#C9A96E`) se materializa en el centro mediante un efecto difuminado de destello cruzado (cross-flare o blur). Debajo, en tipografía `Outfit` gris sutil (`#8A8885`), aparece suavemente el texto "Una declaración de trascendencia".
**SFX:** Silencio absoluto de la música de fondo antes de pronunciar el nombre, dejando la resonancia final del eco vocal.
**Transition OUT:** Fade to black (0.5s).

---

### ARQUITECTURA DEL PROYECTO

```
craneo_promo/
├── index.html                    root — VO orchestration
├── DESIGN.md
├── SCRIPT.md
├── STORYBOARD.md
├── transcript.json
├── narration.wav
├── capture/                      
└── compositions/
    ├── beat-1-hook.html
    ├── beat-2-revelacion.html
    ├── beat-3-detalle.html
    ├── beat-4-coleccion.html
    └── beat-5-cierre.html
```
