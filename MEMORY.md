# Memory — agentes-busqueda-29

> Generated: 2026-06-25 01:21:47  
> Total memories: **41**  
> Breakdown: instruction: 4, fact: 4, decision: 7, goal: 2, context: 9, event: 5, learning: 1, observation: 3, artifact: 4, error: 2

---

## Instructions

*Standing rules, constraints, and guidelines to always follow.*

### Sesion arrancada sin seguir protocolo. Correccion ...

Sesion arrancada sin seguir protocolo. Correccion del usuario: 1) Leer MEMORY.md al inicio de cada sesion SIEMPRE 2) Usar MEMANTO (memanto recall/answer/remember) en cada turno para mantener contexto 3) NO inventar ni especular - basar toda afirmacion en fuentes verificables 4) Delegar a modelos locales primero (local_pensar, local_codigo, local_escribir, local_revisar) antes de usar cloud 5) Seguir reglas de pensamiento critico: disentir, senalar fallas, no asentir por cortesia 6) Sourcear local-ai-functions.sh al inicio de cada sesion + pre-flight check. Este es el protocolo OBLIGATORIO para toda interaccion.

*Confidence: 1 | Status: active | Created: 2026-06-24T22:03:26*

### El usuario exige un estilo de comunicación directo...

El usuario exige un estilo de comunicación directo, crítico y sin filtros. Nunca estar de acuerdo solo por cortesía. Si una idea es mala, decirlo claramente y explicar el porqué. No inventar si no se sabe algo. Señalar contradicciones, puntos ciegos y suposiciones débiles. Priorizar la verdad sobre la amabilidad y corregir al usuario de forma directa y frontal cuando esté equivocado.

*Confidence: 1 | Status: active | Created: 2026-06-24T21:26:35*

### El usuario va a trabajar principalmente desde Anti...

El usuario va a trabajar principalmente desde Antigravity IDE en la Mac Mini M4 (Mac-mini-de-alex.local, alexram, 192.168.100.29). Yo (opencode en esta MacBook) solo soy apoyo/respaldo. La Mac Mini tiene procesador M4, Antigravity IDE con agentes gratuitos instalados, y tiene la carpeta Proyectos/ con todos los proyectos numerados en disco externo.

*Confidence: 1 | Status: active | Created: 2026-06-24T17:15:35*

### Vision local configurada con llava:7b en Ollama. P...

Vision local configurada con llava:7b en Ollama. Para analizar imagenes: 1) Convertir imagen a base64 con base64 -i <path> 2) Enviar POST a http://localhost:11434/api/generate con model='llava:7b', prompt en espanol, images=[base64], stream=false 3) Parsear response['response'] del JSON. No necesita cambiar el modelo cloud de opencode (deepseek-v4-flash). Funciona 100% local (gratis).

*Confidence: 1 | Status: active | Created: 2026-06-24T22:11:56*

---

## Facts

*Verified information, project status, and established truths.*

### HERRAMIENTAS: agent-browser, Puppeteer (instalado ...

HERRAMIENTAS: agent-browser, Puppeteer (instalado en proyecto), Chrome profile en agent_chrome_profile/, Claude Code, Gemini CLI, webfetch.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:23:58*

### Mac Mini M4 (alexram@192.168.100.29) IP pública: 1...

Mac Mini M4 (alexram@192.168.100.29) IP pública: 187.190.176.36 (Telmex/Dish SLP), IPv6: 2806:2f0:41a4:bd4d:ddca:1590:4e44:78c4. No tiene DDNS configurado. n8n tunnel via Cloudflare por ahora.

*Confidence: 1 | Status: active | Created: 2026-06-24T17:05:47*

### Bose SoundTouch 30 en reparacion - WiFi no detecta...

Bose SoundTouch 30 en reparacion - WiFi no detectado (sin interfaz wlan0), ethernet eth0 down, solo usb0 funciona. Firmware 27.0.6 estable, modo AUX funcionando. Posible reemplazo de modulo WiFi WL1271 necesitado.

*Confidence: 1 | Status: active | Created: 2026-06-23T20:51:02 | Tags: `bose`, `soundtouch30`, `wifi`, `reparacion`*

### En NoMachine (Windows a Mac Mini): Ctrl + Shift + ...

En NoMachine (Windows a Mac Mini): Ctrl + Shift + 3 = pantalla completa, Ctrl + Shift + 4 = selección de área, Ctrl + Shift + 5 = herramienta captura. Ctrl en teclado Windows funciona como Command en Mac.

*Confidence: 1 | Status: active | Created: 2026-06-24T07:15:36*

---

## Decisions

*Architectural choices, approach selections, and their rationale.*

### Added Option 4 to respuestas-comerciales.md to fra...

Added Option 4 to respuestas-comerciales.md to frame the 1,800 MXN price of Hera as an introductory debut offer, protecting the 4,500 MXN target price of the second piece

*Confidence: 1 | Status: active | Created: 2026-06-24T21:35:46*

### Generación de renderizado 3D de lujo del cráneo He...

Generación de renderizado 3D de lujo del cráneo Hera completada usando ComfyUI (SDXL img2img, denoise 0.5, seed 1382977115351459797). El resultado se guardó en assets/comfy_outputs/

*Confidence: 1 | Status: active | Created: 2026-06-25T07:21:35*

### Changed the global model in ~/.config/opencode/ope...

Changed the global model in ~/.config/opencode/opencode.jsonc from opencode-go/deepseek-v4-flash to opencode/gemini-3.5-flash to support image/vision input.

*Confidence: 1 | Status: active | Created: 2026-06-24T20:05:16*

### Configured local Ollama provider and ollama/qwen2....

Configured local Ollama provider and ollama/qwen2.5:7b model in ~/.config/opencode/opencode.jsonc to resolve CreditsError / insufficient balance.

*Confidence: 1 | Status: active | Created: 2026-06-24T20:14:23*

### Registered DeepSeek agent (ollama/deepseek-r1:8b) ...

Registered DeepSeek agent (ollama/deepseek-r1:8b) and Ollama/DeepSeek models in OpenClaw config to allow running local reasoning models.

*Confidence: 1 | Status: active | Created: 2026-06-24T20:14:19*

### Changed default model in ~/.config/opencode/openco...

Changed default model in ~/.config/opencode/opencode.jsonc and opencode.json to opencode-go/deepseek-v4-flash per user request

*Confidence: 1 | Status: active | Created: 2026-06-24T21:10:26*

### Repaired Cráneo Noble SVG logo (V2) to fully prese...

Repaired Cráneo Noble SVG logo (V2) to fully preserve horn tips and snout (beard), which were cut off by Y-axis crop. Now calculated and centered mathematically using SVG path bounding boxes.

*Confidence: 1 | Status: active | Created: 2026-06-25T00:15:35*

---

## Goals

*Objectives, targets, and milestones to track progress.*

### PENDIENTE: 1) Completar KYC MercadoPago + obtener ...

PENDIENTE: 1) Completar KYC MercadoPago + obtener APP_ID 2) Registrar eBay Developers 3) Integrar APIs en scripts 4) Probar busqueda completa multi-sitio 5) Probar Facebook Marketplace

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:23:57*

### Meta: reparar el bucle de boot loop del Bose Sound...

Meta: reparar el bucle de boot loop del Bose SoundTouch 30 y dejarlo funcionando. Prioridad maxima.

*Confidence: 1 | Status: active | Created: 2026-06-23T20:53:05 | Tags: `bose`, `reparacion`, `meta`*

---

## Commitments

*Promises, obligations, and TODOs that need follow-through.*

*No memories of this type.*

---

## Preferences

*User and entity preferences for personalization.*

*No memories of this type.*

---

## Relationships

*Entity connections, team context, and collaboration patterns.*

*No memories of this type.*

---

## Context

*Session summaries, status updates, and conversation state.*

### Created sales leads tracking file leads.md in 37-c...

Created sales leads tracking file leads.md in 37-craneo-nobles/sales/ based on Facebook Marketplace screenshot listing 10 active leads for Hera cow skull

*Confidence: 1 | Status: active | Created: 2026-06-24T21:29:49*

### CHECKPOINT: API ML registrada con Client ID 863732...

CHECKPOINT: API ML registrada con Client ID 8637322934683839. Redirect URI https://localhost:3000/auth/ml/callback agregada. Pendiente: ejecutar autorizar_ml.sh para OAuth flow -> obtener Access Token. eBay sigue pendiente.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:56:58*

### CHECKPOINT 9 JUNIO: Subiendo INE en MercadoPago KY...

CHECKPOINT 9 JUNIO: Subiendo INE en MercadoPago KYC para registro de app MercadoLibre Developers. URL del KYC guardada en STATUS.md. Pendiente: completar verificacion, obtener APP_ID + SECRET_KEY.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:23:54*

### PROYECTO: 29-agentes-busqueda-posteo. Buscador mul...

PROYECTO: 29-agentes-busqueda-posteo. Buscador multi-sitio de productos con Agent-Browser + Puppeteer. Ruta: /Users/macbook/Proyectos/29-agentes-busqueda-posteo/.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:23:52*

### CHECKPOINT COMPLETO: API de MercadoLibre registrad...

CHECKPOINT COMPLETO: API de MercadoLibre registrada y token obtenido. Client ID: 8637322934683839. Access Token y Refresh Token guardados en .env (expira 6h). Search API restringida (403), fallback a webfetch. Buscador multi-sitio funcionando: python3 scripts/buscador/buscar_productos.py <query>. Pendiente: eBay Developers, mejorar parsing HTML.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T05:12:03*

### Mac Mini M4 at 192.168.100.29 (Mac-mini-de-alex.lo...

Mac Mini M4 at 192.168.100.29 (Mac-mini-de-alex.local). macOS 26.5.1. User: alexram. SSH key auth configured. Desktop has MAC-MINI-ANTIGRAVITY-CONTEXT.md with QNAP/n8n context for Antigravity IDE.

*Confidence: 1 | Status: active | Created: 2026-06-24T17:04:41*

### QNAP NAS (192.168.100.10, hostname Aldukehome) n8n...

QNAP NAS (192.168.100.10, hostname Aldukehome) n8n configurado con Cloudflare Tunnel. URL pública: https://recipes-moore-arabic-enormous.trycloudflare.com/ . WEBHOOK_URL actualizada. Timezone: America/Mexico_City. Encryption key configurada. n8n versión 0.124.1 funcionando (ARM v7, no soporta 1.x, upgrade a 0.218.0 pendiente de descargar). Docker via Container Station 3.1.2.1742 en /share/CACHEDEV1_DATA/.qpkg/container-station/ . n8n compose en /share/CACHEDEV1_DATA/n8n/docker-compose.yml . Datos en /share/CACHEDEV1_DATA/n8n/data/ . Contenedor ID: 9a4b6081468d. Admin user: admin / bot123

*Confidence: 1 | Status: active | Created: 2026-06-24T16:48:37*

### Contexto de sesion: opencode ejecutandose en MacBo...

Contexto de sesion: opencode ejecutandose en MacBook (macbook, /Volumes/MiDisco1TB/Proyectos/). El usuario trabaja PRINCIPALMENTE desde Antigravity IDE en Mac Mini M4 (alexram@192.168.100.29). Yo (opencode MacBook) soy SOLO apoyo/respaldo. No debo asumir que soy el agente principal.

*Confidence: 1 | Status: active | Created: 2026-06-24T22:03:34*

### SESION COMPLETA 9 JUN 2026. Logros: (1) KYC Mercad...

SESION COMPLETA 9 JUN 2026. Logros: (1) KYC MercadoPago completado con INE subida para verification de identidad. (2) App 'Buscador Multi-Sitio' creada en MercadoLibre Developers con Client ID 8637322934683839 y Secret guardado en .env. (3) Redirect URI configurada como https://whatsapp-restaurant-iox6.onrender.com/auth/ml/callback. (4) PKCE desactivado en OAuth flows. (5) Authorization Code flow completado y Access Token obtenido (APP_USR-8637322934683839-061001-c2a1bcb0a549dd356cecf7bd57e7ac8a-134201545) con Refresh Token. Token expira en 6h. (6) Se agrego endpoint temporal /auth/ml/callback al bot de Render y luego se elimino. (7) Search API de ML devuelve 403 incluso con token autenticado - endpoint restringido. (8) Creado scripts/buscador/buscar_productos.py - orquestador multi-sitio que busca en Amazon MX (webfetch) y MercadoLibre MX (intenta API, fallback webfetch). Resultados en /tmp/resultados_busqueda.json. Pendientes: eBay Developers, mejorar parsing HTML, configurar renovacion automatica de refresh token. URL del proyecto: /Users/macbook/Proyectos/29-agentes-busqueda-posteo/. Config en AGENTS.md y STATUS.md.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T05:28:26*

---

## Events

*Important conversations, milestones, and temporal occurrences.*

### Bose SoundTouch 30 reparado exitosamente - boot lo...

Bose SoundTouch 30 reparado exitosamente - boot loop roto con factory reset + configuracion completa (idioma, nombre, modo AUX). Firmware 27.0.6 estable. WiFi no disponible por hardware. Funciona por AUX.

*Confidence: 1 | Status: active | Created: 2026-06-23T21:06:15 | Tags: `bose`, `soundtouch30`, `reparado`, `aux`*

### Sesion completa 23 Jun 2026. Setup Mac Mini M4 com...

Sesion completa 23 Jun 2026. Setup Mac Mini M4 completado: Homebrew, Node 26, Ollama (DeepSeek-R1:8b, Qwen2.5:7b), Open WebUI, AnythingLLM, LM Studio/llmster, OpenClaw v2026.6.9, Antigravity IDE con MCP Firebase reparado, Opencode Go configurado con skills y MEMANTO, Syncthing bidireccional, NoMachine, Fusion 360, NoMachine. Proyectos (21GB) en MiDisco1TB sincronizados.

*Confidence: 1 | Status: active | Created: 2026-06-24T07:34:00*

### Mac Mini (Mac-mini-de-alex.local, alexram) tiene o...

Mac Mini (Mac-mini-de-alex.local, alexram) tiene opencode 1.17.9 instalado via npm. Node 26.3.1 via Homebrew 6.0.3 en /opt/homebrew/bin/ (PATH fijado en .zshrc). opencode tiene vision-server_vision_analyze integrado para leer imagenes. Contexto de infraestructura guardado en ~/.config/opencode/AGENTS.md. El usuario ahora puede usar 'cd ~/Proyectos/[proyecto] && opencode' para trabajar con las mismas capacidades que yo.

*Confidence: 1 | Status: active | Created: 2026-06-24T20:02:49*

### Los modelos de Ollama se movieron al disco externo...

Los modelos de Ollama se movieron al disco externo. Ruta: /Volumes/MiDisco1TB/ollama/models/. Se uso symlink: ~/.ollama/models -> /Volumes/MiDisco1TB/ollama/models/. Se liberaron ~23GB del SSD interno de la Mac Mini. La config esta en ~/.zshrc con la variable OLLAMA_MODELS como referencia (aunque el symlink la hace innecesaria). Esto aplica para todos los modelos: llava:7b, moondream, qwen2.5:7b, qwen:7b, deepseek-r1:8b.

*Confidence: 1 | Status: active | Created: 2026-06-24T22:47:49*

### iPhone 6 Plus (iOS 12.5.8) con iCloud activation l...

iPhone 6 Plus (iOS 12.5.8) con iCloud activation lock bypassed via checkra1n + SSH manual method. Funciona con WiFi, sin celular. Si se reinicia, repetir: DFU → checkra1n -c -s → SSH → bypass. UDID: 28c15b8cd3f742d58ac4a24bddc9e39ac4976ae2

*Confidence: 1 | Status: active | Created: 2026-06-21T22:28:19*

---

## Learnings

*Knowledge acquired from experience, corrections, and insights.*

### Use negated flat-field division (negating image be...

Use negated flat-field division (negating image before flat-fielding) to normalize light features on dark backgrounds before thresholding for potrace, preventing outline/background inversion and cut-offs due to shadow

*Confidence: 1 | Status: active | Created: 2026-06-25T01:05:04*

---

## Observations

*Patterns noticed, behavioral notes, and recurring themes.*

### Analisis de IMG_1810.PNG (37-craneo-nobles/assets/...

Analisis de IMG_1810.PNG (37-craneo-nobles/assets/) con moondream: la imagen muestra un craneo decorado con acentos verdes y azules sobre fondo negro. Parece de piedra o ceramica. Texto interpretado como 'CRANE ART' o 'CRANIO ART'. Es una pieza artistica/decorativa, posiblemente un craneo de ganado vacuno pintado a mano.

*Confidence: 0.85 | Status: active | Created: 2026-06-24T22:57:04*

### User shared Facebook Marketplace stats: Hera cow s...

User shared Facebook Marketplace stats: Hera cow skull is a highly attractive piece receiving multiple inquiries (at least 10 active leads) shortly after listing

*Confidence: 1 | Status: active | Created: 2026-06-24T21:31:18*

### AMAZON MX: Funciona via webfetch. Probado con 'ven...

AMAZON MX: Funciona via webfetch. Probado con 'ventilador macbook pro' - 315 resultados reales.

*Confidence: 0.8 | Status: active | Created: 2026-06-10T04:23:55*

---

## Artifacts

*Tool outputs, files, reports, and external references.*

### Bose SoundTouch 30 reparación - Serial K4067882804...

Bose SoundTouch 30 reparación - Serial K4067882804625125000410 - WiFi y Ethernet dañados, solo funciona por AUX. Firmware 27.0.2 instalado.

*Confidence: 1 | Status: active | Created: 2026-06-23T20:22:37*

### Vectorized the Cráneo Noble cow skull logo from up...

Vectorized the Cráneo Noble cow skull logo from uploaded Marketplace design screenshot, creating clean, scalable SVG files (both with premium dark metallic background and transparent versions) in 37-craneo-nobles/assets/

*Confidence: 1 | Status: active | Created: 2026-06-25T00:08:55*

### Generated final deliverables in 37-craneo-nobles/a...

Generated final deliverables in 37-craneo-nobles/assets/: logo-craneo-noble-refinado.svg (luxury circular emblem), logo-craneo-noble.png (1024x1024 square profile picture rendered via Chrome/Puppeteer), and nano-banana-prompt.txt (optimized prompts)

*Confidence: 1 | Status: active | Created: 2026-06-25T01:18:53*

### Vision local configurada. Modelos disponibles en O...

Vision local configurada. Modelos disponibles en Ollama: llava:7b (7B, vision general), moondream:latest (1.8B, ligero). Configurados en ~/.config/opencode/opencode.jsonc bajo provider.ollama.models. Para analizar imagenes localmente sin cambiar modelo cloud: 1) Usar Python con urllib.request a POST http://localhost:11434/api/generate 2) Body: model, prompt, images:[base64], stream:false 3) Parsear response['response']. Todo 100% local/gratis.

*Confidence: 1 | Status: active | Created: 2026-06-24T22:19:26*

---

## Errors

*Failure records, bugs, and lessons learned from mistakes.*

### Error corregido: responder sin verificar datos. El...

Error corregido: responder sin verificar datos. El usuario pregunto 'donde esta guardado' y respondi asumiendo MacBook sin checar primero hostname. Leccion: SIEMPRE verificar con comandos (hostname, whoami, ls) antes de responder preguntas de localizacion/configuracion. No asumir. No inventar.

*Confidence: 1 | Status: active | Created: 2026-06-24T22:22:48*

### Fixed bug in SVG generator where unscaled image he...

Fixed bug in SVG generator where unscaled image height caused negative Y translation. The skull and monogram are now fully visible and centered.

*Confidence: 1 | Status: active | Created: 2026-06-25T00:17:06*

---

*End of memory export.*
