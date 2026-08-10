const fs = require('fs');
const path = require('path');
const readline = require('readline');
const https = require('https');

const CONFIG_FILE = path.join(__dirname, '..', '.config.json');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

function request(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
      });
    }).on('error', reject);
  });
}

async function main() {
  console.log('=========================================================');
  console.log('🤖 GENERADOR DE TOKENS — CRÁNEO NOBLE');
  console.log('=========================================================');
  console.log('\nPASO 1: Crear la App en Meta Developers');
  console.log('1. Ve a https://developers.facebook.com/apps/');
  console.log('2. Crea una app tipo "Empresa" (Business) llamada "Craneo Noble Publisher".');
  console.log('3. En Configuración de la App > Básica, copia el Identificador de la app (App ID) y la Clave secreta (App Secret).');
  console.log('4. En "Casos de uso" o "Productos", agrega "Inicio de sesión con Facebook".');
  console.log('5. En la configuración de Inicio de sesión, pon en "URI de redireccionamiento de OAuth válidos":');
  console.log('   https://www.facebook.com/connect/login_success.html');
  console.log('6. Guarda los cambios.\n');

  let config = {};
  try { config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); } catch (e) {}

  const appId = await question(`Introduce el nuevo APP_ID [Enter para dejar ${config.APP_ID || ''}]: `) || config.APP_ID;
  const appSecret = await question(`Introduce el nuevo APP_SECRET [Enter para mantener actual]: `) || config.APP_SECRET;

  config.APP_ID = appId;
  config.APP_SECRET = appSecret;
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));

  console.log('\n=========================================================');
  console.log('PASO 2: Autorizar la App');
  console.log('Abre el siguiente enlace en tu navegador (donde estés logueado en Facebook):');
  
  const oauthUrl = `https://www.facebook.com/v19.0/dialog/oauth?client_id=${appId}&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=pages_manage_posts,pages_read_engagement,business_management,instagram_basic,instagram_content_publish&response_type=token`;
  console.log(`\n\x1b[36m${oauthUrl}\x1b[0m\n`);
  
  console.log('Te redirigirá a una página en blanco o con un mensaje de éxito.');
  console.log('Copia la URL a la que te redirigió (debe contener "#access_token=...").');
  
  const redirectUrl = await question('\nPega aquí la URL completa a la que fuiste redirigido:\n> ');
  const tokenMatch = redirectUrl.match(/access_token=([^&]+)/);
  
  if (!tokenMatch) {
    console.error('❌ No se encontró access_token en la URL.');
    process.exit(1);
  }
  
  const shortToken = decodeURIComponent(tokenMatch[1]);
  console.log('\n⏳ Intercambiando por Token de Larga Duración...');
  
  const exchangeUrl = `https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${appId}&client_secret=${appSecret}&fb_exchange_token=${shortToken}`;
  const longTokenRes = await request(exchangeUrl);
  
  if (longTokenRes.error) {
    console.error('❌ Error obteniendo Long-Lived Token:', longTokenRes.error);
    process.exit(1);
  }
  
  const longToken = longTokenRes.access_token;
  console.log('✅ Long-Lived Token obtenido exitosamente.');
  
  console.log('\n⏳ Obteniendo Token Permanente de la Página Cráneo Noble...');
  const accountsUrl = `https://graph.facebook.com/v19.0/me/accounts?access_token=${longToken}`;
  const accountsRes = await request(accountsUrl);
  
  if (accountsRes.error) {
    console.error('❌ Error obteniendo cuentas:', accountsRes.error);
    process.exit(1);
  }
  
  const page = accountsRes.data.find(p => p.id === config.PAGE_ID);
  if (!page) {
    console.error(`❌ No se encontró la página ${config.PAGE_ID} en las cuentas autorizadas.`);
    console.log('Cuentas encontradas:', accountsRes.data.map(p => p.name).join(', '));
    process.exit(1);
  }
  
  config.PAGE_TOKEN = page.access_token;
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  
  console.log(`\n🎉 ¡ÉXITO! Token permanente de la página "${page.name}" guardado en .config.json`);
  console.log('✅ Ya no dependes de la app Glassitas. El publicador ahora es totalmente autónomo.');
  
  rl.close();
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
