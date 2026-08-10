const https = require('https');
const fs = require('fs');
const path = require('path');

const config = require('../.config.json');
const PAGE_ID = config.PAGE_ID;
const PAGE_TOKEN = process.env.PAGE_TOKEN || config.PAGE_TOKEN;
const USER_TOKEN = process.env.USER_TOKEN || null;
const FB_GROUPS = config.FB_GROUPS || [];

function graphPost(endpoint, data, isMultipart = false) {
  return new Promise((resolve, reject) => {
    const url = new URL(`https://graph.facebook.com/v19.0${endpoint}`);
    const options = { method: 'POST', headers: {} };
    if (isMultipart) {
      options.headers = data.headers;
      const req = https.request(url, options, res => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => { try { resolve(JSON.parse(body)); } catch { resolve(body); } });
      });
      req.write(data.body);
      req.end();
    } else {
      const body = new URLSearchParams(data).toString();
      options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.headers['Content-Length'] = Buffer.byteLength(body);
      const req = https.request(url, options, res => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => { try { resolve(JSON.parse(body)); } catch { resolve(body); } });
      });
      req.write(body);
      req.end();
    }
  });
}

function makeMultipart(fields, filePath) {
  const boundary = '----Boundary' + Math.random().toString(36).slice(2);
  const fileData = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);
  let body = '';
  for (const [k, v] of Object.entries(fields)) {
    body += `--${boundary}\r\nContent-Disposition: form-data; name="${k}"\r\n\r\n${v}\r\n`;
  }
  body += `--${boundary}\r\nContent-Disposition: form-data; name="source"; filename="${fileName}"\r\nContent-Type: image/jpeg\r\n\r\n`;
  const buffer = Buffer.concat([Buffer.from(body), fileData, Buffer.from(`\r\n--${boundary}--\r\n`)]);
  return {
    headers: { 'Content-Type': `multipart/form-data; boundary=${boundary}`, 'Content-Length': buffer.length },
    body: buffer
  };
}

async function postToFacebook(imagePath, message) {
  const fullPath = path.resolve(imagePath);
  if (!fs.existsSync(fullPath)) { console.error(`Archivo no encontrado: ${fullPath}`); process.exit(1); }
  const multipart = makeMultipart({ message, access_token: PAGE_TOKEN }, fullPath);
  const result = await graphPost(`/${PAGE_ID}/photos`, multipart, true);
  if (result.error) { console.error('Error en página:', result.error.message); process.exit(1); }
  console.log(`✅ Publicada en página! ID: ${result.id}`);
  return result.id;
}

async function postText(message) {
  const result = await graphPost(`/${PAGE_ID}/feed`, { message, access_token: PAGE_TOKEN });
  if (result.error) { console.error('Error en página:', result.error.message); process.exit(1); }
  console.log(`✅ Publicado en página! ID: ${result.id}`);
  return result.id;
}

async function postToGroup(groupId, imagePath, message, token) {
  const fullPath = path.resolve(imagePath);
  const endpoint = imagePath ? `/${groupId}/photos` : `/${groupId}/feed`;
  if (imagePath && fs.existsSync(fullPath)) {
    const multipart = makeMultipart({ message, access_token: token }, fullPath);
    const result = await graphPost(endpoint, multipart, true);
    if (result.error) throw new Error(result.error.message);
    return result.id;
  } else {
    const result = await graphPost(endpoint, { message, access_token: token });
    if (result.error) throw new Error(result.error.message);
    return result.id;
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help') {
    console.log(`Uso: node scripts/post.js "mensaje" [imagen] [--groups]`);
    console.log(`  --groups    También publicar en los grupos configurados`);
    process.exit(0);
  }
  const message = args[0];
  const imagePath = args[1] && !args[1].startsWith('--') ? args[1] : null;
  const postToGroups = args.includes('--groups');

  if (imagePath) await postToFacebook(imagePath, message);
  else await postText(message);

  if (postToGroups) {
    if (!USER_TOKEN) {
      console.log('⚠️  No hay USER_TOKEN — no se puede publicar en grupos.');
      console.log('   Configura USER_TOKEN en entorno o agrega userToken en .config.json');
      process.exit(0);
    }
    if (FB_GROUPS.length === 0) {
      console.log('⚠️  No hay grupos configurados en FB_GROUPS.');
      process.exit(0);
    }
    for (const group of FB_GROUPS) {
      const gid = typeof group === 'string' ? group : group.id;
      try {
        const id = await postToGroup(gid, imagePath, message, USER_TOKEN);
        console.log(`✅ Publicado en grupo ${gid}! ID: ${id}`);
      } catch (e) {
        console.error(`❌ Error en grupo ${gid}: ${e.message}`);
      }
    }
  }
}

main().catch(console.error);
