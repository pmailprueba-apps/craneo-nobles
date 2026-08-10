/**
 * PUBLICADOR PROGRAMADO — Campañas Cráneo Noble
 * 
 * Lee el día actual (1-7), busca la imagen y el copy correspondiente,
 * y publica en Facebook.
 * 
 * Modo de uso:
 *   node scripts/publicar-programado.js --campana <nombre>             # publica hoy
 *   node scripts/publicar-programado.js --campana <nombre> --reset     # reinicia al día 1
 *   node scripts/publicar-programado.js --campana <nombre> --status    # muestra en qué día va
 * 
 * Automatización (cron/launchd):
 *   node scripts/publicar-programado.js --campana alma-de-plata
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

const DAYS = 7;

function graphPost(endpoint, data) {
  return new Promise((resolve, reject) => {
    const u = new URL(`https://graph.facebook.com/v19.0${endpoint}`);
    const body = new URLSearchParams(data).toString();
    const req = https.request(u.toString(), { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(body) } }, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => { try { resolve(JSON.parse(d)); } catch { resolve(d); } });
    });
    req.on('error', reject); req.write(body); req.end();
  });
}

function graphGet(endpoint) {
  return new Promise((resolve, reject) => {
    https.get(`https://graph.facebook.com/v19.0${endpoint}`, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => { try { resolve(JSON.parse(d)); } catch { resolve(d); } });
    }).on('error', reject);
  });
}

async function postToInstagram(token, imagePath, caption) {
  const config = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '.config.json'), 'utf8'));
  const igId = config.IG_USER_ID;
  if (!igId) { console.log('  ⏭️ Instagram: IG_USER_ID no configurado'); return false; }
  
  console.log('  📸 Publicando en Instagram...');
  
  // Upload photo to FB (unpublished) to get CDN URL
  const photoData = fs.readFileSync(imagePath);
  const boundary = '----Boundary' + Math.random().toString(36).slice(2);
  let body = `--${boundary}\r\nContent-Disposition: form-data; name="access_token"\r\n\r\n${token}\r\n`;
  body += `--${boundary}\r\nContent-Disposition: form-data; name="published"\r\n\r\nfalse\r\n`;
  body += `--${boundary}\r\nContent-Disposition: form-data; name="source"; filename="${path.basename(imagePath)}"\r\nContent-Type: image/jpeg\r\n\r\n`;
  const buffer = Buffer.concat([Buffer.from(body), photoData, Buffer.from(`\r\n--${boundary}--\r\n`)]);
  
  const fbRes = await new Promise((resolve, reject) => {
    const u = new URL(`https://graph.facebook.com/v19.0/${config.PAGE_ID}/photos`);
    const req = https.request(u.toString(), { method: 'POST', headers: { 'Content-Type': `multipart/form-data; boundary=${boundary}`, 'Content-Length': buffer.length } }, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => { try { resolve(JSON.parse(d)); } catch { resolve(d); } });
    });
    req.on('error', reject); req.write(buffer); req.end();
  });
  
  if (!fbRes.id) { console.log(`  ❌ Instagram: Error subiendo foto: ${fbRes.error?.message || '?'}`); return false; }
  
  // Get CDN URL
  const photoInfo = await graphGet(`/${fbRes.id}?fields=images&access_token=${token}`);
  const imageUrl = photoInfo?.images?.[0]?.source;
  if (!imageUrl) { console.log('  ❌ Instagram: No se pudo obtener CDN URL'); return false; }
  
  // Create IG container
  const container = await graphPost(`/${igId}/media`, { image_url: imageUrl, caption, access_token: token });
  if (!container.id) { console.log(`  ❌ Instagram: Error creando container: ${container.error?.message || '?'}`); return false; }
  console.log(`  📸 Container IG: ${container.id}`);
  
  // Wait for processing
  await new Promise(r => setTimeout(r, 5000));
  
  // Publish
  const publish = await graphPost(`/${igId}/media_publish`, { creation_id: container.id, access_token: token });
  if (!publish.id) { console.log(`  ❌ Instagram: Error publicando: ${publish.error?.message || '?'}`); return false; }
  console.log(`  ✅ Instagram: ${publish.id}`);
  return true;
}

function getCampanaArg() {
  const args = process.argv.slice(2);
  const idx = args.indexOf('--campana');
  if (idx !== -1 && args[idx + 1] && !args[idx + 1].startsWith('--')) {
    return args[idx + 1];
  }
  return 'hera'; // Fallback for backwards compatibility
}

const campana = getCampanaArg();
const STATE_FILE = path.join(__dirname, '..', `.campana-${campana === 'hera' ? 'state' : campana + '-state'}.json`);
const COPYS_FILE = path.join(__dirname, '..', 'marketing', `campana-${campana}.md`);
const DST = path.join(__dirname, '..', 'contenido', campana === 'hera' ? '' : campana);

function getState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { currentDay: 1, publishedDays: [], startedAt: new Date().toISOString() };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function getCopyForDay(day) {
  if (!fs.existsSync(COPYS_FILE)) return '';
  const content = fs.readFileSync(COPYS_FILE, 'utf8');
  // Match ## Día X or ### Día X
  const markerRegex = new RegExp(`^#{2,3} Día ${day} —`, 'm');
  const match = content.match(markerRegex);
  if (!match) return '';
  
  const start = match.index;
  const section = content.substring(start);
  // Find next heading
  const nextHeadingMatch = section.substring(match[0].length).match(/^#{2,3} /m);
  const end = nextHeadingMatch ? match[0].length + nextHeadingMatch.index : section.length;
  let text = section.substring(0, end);
  
  // Try to find **Copy:** marker, else just take text after the heading
  const copyMatch = text.match(/\*\*Copy:\*\*\n([\s\S]*?)$/);
  if (copyMatch) {
    return copyMatch[1].trim();
  } else {
    // Remove the heading line itself
    text = text.replace(markerRegex, '').trim();
    // Remove any trailing lines like ---
    text = text.replace(/^---$/m, '').trim();
    return text;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const state = getState();

  if (args.includes('--reset')) {
    state.currentDay = 1;
    state.publishedDays = [];
    state.startedAt = new Date().toISOString();
    saveState(state);
    console.log(`🔄 Campaña '${campana}' reiniciada al día 1`);
    return;
  }

  if (args.includes('--status')) {
    console.log(`🎯 Campaña: ${campana}`);
    console.log(`📅 Día actual: ${state.currentDay}/${DAYS}`);
    console.log(`📌 Publicados: [${state.publishedDays.join(', ')}]`);
    console.log(`🗓️ Iniciada: ${state.startedAt}`);
    if (state.currentDay > DAYS) console.log('✅ Campaña completada — todas las piezas publicadas');
    return;
  }

  if (state.currentDay > DAYS) {
    console.log(`✅ Campaña '${campana}' completada. Todas las piezas han sido publicadas.`);
    console.log('Usa --reset para reiniciar la campaña.');
    return;
  }

  const day = state.currentDay;
  const dayDir = path.join(DST, `dia${day}`);

  if (!fs.existsSync(dayDir)) {
    console.error(`❌ Directorio día ${day} no encontrado: ${dayDir}`);
    process.exit(1);
  }

  const images = fs.readdirSync(dayDir).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f));
  if (images.length === 0) {
    console.error(`❌ No hay imágenes en ${dayDir}`);
    process.exit(1);
  }

  const imagePath = path.join(dayDir, images[0]);
  const copy = getCopyForDay(day);

  if (!copy) {
    console.error(`❌ No se encontró el copy para el día ${day} en ${COPYS_FILE}`);
    process.exit(1);
  }

  console.log(`📅 Publicando día ${day}/${DAYS} de la campaña '${campana}'...`);

  // Publish using post.js
  const postScript = path.join(__dirname, 'post.js');
  const cmd = `node "${postScript}" "${copy.replace(/"/g, '\\"')}" "${imagePath}"`;

  try {
    execSync(cmd, { stdio: 'inherit', timeout: 30000 });
    console.log(`\n✅ Día ${day} publicado en Facebook.`);

    // Also publish to Instagram
    const config = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '.config.json'), 'utf8'));
    const igResult = await postToInstagram(config.PAGE_TOKEN, imagePath, copy);
    if (igResult) console.log(`  ✅ Instagram también publicado.`);
    
    state.publishedDays.push(day);
    state.currentDay = day + 1;
    saveState(state);
    
    if (state.currentDay > DAYS) {
      console.log(`\n🎉 Campaña '${campana}' completada!`);
    }
  } catch (e) {
    console.error(`\n❌ Error publicando día ${day}: ${e.message.substring(0, 100)}`);
  }
}

main().catch(console.error);
