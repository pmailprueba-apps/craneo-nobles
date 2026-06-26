#!/bin/bash
# PUBLICADOR CAMPAÑA HERA - CRÁNEO NOBLE
# Funciona con curl (no requiere Node.js, Python ni Docker)
# Se ejecuta desde QNAP (cron), GitHub Actions, o cualquier servidor

cd "$(dirname "$0")/.." || exit 1
LOG="cron-campana.log"
echo "[$(date)] Iniciando..." >> "$LOG"

# Leer día actual del estado
DIA=$(python3 -c "import json; print(json.load(open('.campana-state.json'))['currentDay'])" 2>/dev/null)
[ -z "$DIA" ] && { echo "[$(date)] ERROR: No se puede leer estado" >> "$LOG"; exit 1; }
[ "$DIA" -gt 7 ] && { echo "[$(date)] Campaña completada" >> "$LOG"; exit 0; }

# Leer token
TOKEN=$(python3 -c "import json; print(json.load(open('.config.json'))['PAGE_TOKEN'])" 2>/dev/null)
PAGE_ID="1237040242820189"
[ -z "$TOKEN" ] && { echo "[$(date)] ERROR: No hay token" >> "$LOG"; exit 1; }

# Buscar imagen
IMGDIR="contenido/dia${DIA}"
IMAGEN=$(ls "$IMGDIR" 2>/dev/null | grep -iE '\.(png|jpg|jpeg|webp)$' | head -1)

# Extraer copy
python3 -c "
import re
with open('marketing/campana-hera.md') as f:
    content = f.read()
marker = f'### Día $DIA —'
start = content.find(marker)
if start == -1: exit(1)
section = content[start:]
end = section.find('### Día ', 10)
text = section[:end] if end != -1 else section
match = re.search(r'\*\*Copy:\*\*\n([\s\S]*?)(?=\n#|\$)', text)
if match:
    with open('/tmp/_copia_hera.txt', 'w') as out:
        out.write(match.group(1).strip())
else:
    exit(1)
" 2>/dev/null || { echo "[$(date)] ERROR: No se pudo extraer copy dia $DIA" >> "$LOG"; exit 1; }

COPY=$(cat /tmp/_copia_hera.txt)

echo "[$(date)] Publicando día $DIA..." >> "$LOG"

if [ -n "$IMAGEN" ] && [ -f "$IMGDIR/$IMAGEN" ]; then
    RESULT=$(curl -s -X POST "https://graph.facebook.com/v19.0/$PAGE_ID/photos" \
        -F "message=$COPY" \
        -F "access_token=$TOKEN" \
        -F "source=@$IMGDIR/$IMAGEN")
else
    RESULT=$(curl -s -X POST "https://graph.facebook.com/v19.0/$PAGE_ID/feed" \
        -d "message=$COPY" \
        -d "access_token=$TOKEN")
fi

FB_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','ERROR'))" 2>/dev/null)

if [ "$FB_ID" != "ERROR" ]; then
    echo "[$(date)] ✅ Día $DIA publicado: $FB_ID" >> "$LOG"
    python3 -c "
import json
with open('.campana-state.json') as f:
    s = json.load(f)
s['publishedDays'].append(s['currentDay'])
s['currentDay'] += 1
with open('.campana-state.json', 'w') as f:
    json.dump(s, f, indent=2)
"
    # Telegram notify via secret (si está configurado en GitHub Actions)
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=✅ Cráneo Noble: Día $DIA publicado ($FB_ID)" > /dev/null 2>&1
    fi
else
    echo "[$(date)] ❌ Error: $RESULT" >> "$LOG"
fi
