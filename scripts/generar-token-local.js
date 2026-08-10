const http = require('http');
const https = require('https');
const url = require('url');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '..', '.config.json');
let config = {};
try { config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); } catch (e) {
  console.error("No se pudo leer .config.json");
  process.exit(1);
}

const APP_ID = config.APP_ID;
const APP_SECRET = config.APP_SECRET;
const PAGE_ID = config.PAGE_ID;
const REDIRECT_URI = 'http://localhost:8888/callback';

if (!APP_ID || !APP_SECRET) {
  console.error("APP_ID y APP_SECRET deben estar en .config.json");
  process.exit(1);
}

function request(reqUrl) {
  return new Promise((resolve, reject) => {
    https.get(reqUrl, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
      });
    }).on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  if (parsedUrl.pathname === '/callback') {
    const code = parsedUrl.query.code;
    
    if (!code) {
      res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>Error</h1><p>No se recibió el código de autorización.</p>');
      return;
    }
    
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.write('<h1>Autorización recibida</h1><p>Procesando token... revisa la terminal.</p>');
    
    console.log('\n⏳ Intercambiando código por Token...');
    const exchangeUrl = `https://graph.facebook.com/v19.0/oauth/access_token?client_id=${APP_ID}&redirect_uri=${REDIRECT_URI}&client_secret=${APP_SECRET}&code=${code}`;
    
    try {
      const tokenRes = await request(exchangeUrl);
      if (tokenRes.error) throw new Error(tokenRes.error.message);
      
      const shortToken = tokenRes.access_token;
      
      console.log('⏳ Obteniendo Token Permanente de la Página Cráneo Noble...');
      const accountsUrl = `https://graph.facebook.com/v19.0/me/accounts?access_token=${shortToken}`;
      const accountsRes = await request(accountsUrl);
      
      if (accountsRes.error) throw new Error(accountsRes.error.message);
      
      const page = accountsRes.data.find(p => p.id === PAGE_ID);
      if (!page) {
        throw new Error(`No se encontró la página ${PAGE_ID} en las cuentas autorizadas.`);
      }
      
      config.PAGE_TOKEN = page.access_token;
      fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
      
      console.log(`\n🎉 ¡ÉXITO! Token permanente de la página "${page.name}" guardado en .config.json`);
      res.end('<script>document.body.innerHTML += "<h2>¡ÉXITO! Ya puedes cerrar esta ventana.</h2>";</script>');
      
      setTimeout(() => process.exit(0), 1000);
      
    } catch (e) {
      console.error('\n❌ Error:', e.message);
      res.end(`<script>document.body.innerHTML += "<h2 style='color:red'>Error: ${e.message}</h2>";</script>`);
      process.exit(1);
    }
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(8888, () => {
  console.log('=========================================================');
  console.log('🤖 GENERADOR DE TOKENS LOCAL — CRÁNEO NOBLE');
  console.log('=========================================================');
  console.log('\nPASO 1: Configurar Redirect URI en Facebook Developers');
  console.log(`Ve a la configuración de 'Inicio de sesión con Facebook' de tu app y agrega EXACTAMENTE esto en 'URI de redireccionamiento de OAuth válidos':`);
  console.log(`\x1b[33m${REDIRECT_URI}\x1b[0m`);
  console.log('Guarda los cambios en Facebook.\n');
  
  console.log('PASO 2: Autorizar');
  const oauthUrl = `https://www.facebook.com/v19.0/dialog/oauth?client_id=${APP_ID}&redirect_uri=${REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement,business_management,instagram_basic,instagram_content_publish&response_type=code`;
  console.log('Haz clic en el siguiente enlace:');
  console.log(`\n\x1b[36m${oauthUrl}\x1b[0m\n`);
  console.log('Servidor escuchando en puerto 8888... Esperando callback de Facebook...');
});
