/**
 * PUBLICADOR PROGRAMADO — Hera / Cráneo Noble
 * 
 * Lee el día actual (1-7), busca la imagen y el copy correspondiente,
 * y publica en Facebook.
 * 
 * Modo de uso:
 *   node scripts/publicar-programado.js              # publica hoy
 *   node scripts/publicar-programado.js --reset      # reinicia al día 1
 *   node scripts/publicar-programado.js --status     # muestra en qué día va
 * 
 * Automatización (cron):
 *   0 12 * * * cd /ruta && node scripts/publicar-programado.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const STATE_FILE = path.join(__dirname, '..', '.campana-state.json');
const COPYS_FILE = path.join(__dirname, '..', 'marketing', 'campana-hera.md');
const DAYS = 7;
const DST = path.join(__dirname, '..', 'contenido');

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
  const content = fs.readFileSync(COPYS_FILE, 'utf8');
  const marker = `### Día ${day} —`;
  const start = content.indexOf(marker);
  if (start === -1) return '';
  const section = content.substring(start);
  const end = section.indexOf('### Día ', 10);
  const text = end === -1 ? section : section.substring(0, end);
  const copyMatch = text.match(/\*\*Copy:\*\*\n([\s\S]*?)(?=\n#|$)/);
  return copyMatch ? copyMatch[1].trim() : '';
}

async function main() {
  const args = process.argv.slice(2);
  const state = getState();

  if (args.includes('--reset')) {
    state.currentDay = 1;
    state.publishedDays = [];
    state.startedAt = new Date().toISOString();
    saveState(state);
    console.log('🔄 Campaña reiniciada al día 1');
    return;
  }

  if (args.includes('--status')) {
    console.log(`📅 Día actual: ${state.currentDay}/${DAYS}`);
    console.log(`📌 Publicados: [${state.publishedDays.join(', ')}]`);
    console.log(`🗓️ Iniciada: ${state.startedAt}`);
    if (state.currentDay > DAYS) console.log('✅ Campaña completada — todas las piezas publicadas');
    return;
  }

  if (state.currentDay > DAYS) {
    console.log('✅ Campaña completada. Todas las piezas han sido publicadas.');
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
    console.error(`❌ No se encontró el copy para el día ${day}`);
    process.exit(1);
  }

  console.log(`📅 Publicando día ${day}/${DAYS}...`);

  // Publish using post.js
  const postScript = path.join(__dirname, 'post.js');
  const cmd = `node "${postScript}" "${copy.replace(/"/g, '\\"')}" "${imagePath}"`;

  try {
    execSync(cmd, { stdio: 'inherit', timeout: 30000 });
    state.publishedDays.push(day);
    state.currentDay = day + 1;
    saveState(state);
    console.log(`\n✅ Día ${day} publicado exitosamente.`);
    
    if (state.currentDay > DAYS) {
      console.log('\n🎉 Campaña completada! Todas las publicaciones están en Facebook.');
    }
  } catch (e) {
    console.error(`\n❌ Error publicando día ${day}: ${e.message.substring(0, 100)}`);
  }
}

main().catch(console.error);
