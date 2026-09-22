import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';

const root = fs.realpathSync(process.env.MYK_E2E_DIST || 'dist');
if (!fs.existsSync(path.join(root, 'generated/catalog.json'))) throw new Error('Build a real public release first');
const prefix = '/MyKnowledge/';
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.png': 'image/png', '.webp': 'image/webp', '.xml': 'application/xml' };
const server = http.createServer((req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (!pathname.startsWith(prefix)) { res.writeHead(404).end(); return; }
    let file = path.resolve(root, pathname.slice(prefix.length));
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    file = fs.realpathSync(file);
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  } catch {
    res.writeHead(404).end();
  }
});
server.listen(Number(process.env.MYK_E2E_PORT || 14322), '127.0.0.1');
process.on('SIGTERM', () => server.close(() => process.exit(0)));
