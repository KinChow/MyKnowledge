import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';

const lockDir=path.resolve('../var/state');
const lockPath=path.join(lockDir,'public-release.lock');
fs.mkdirSync(lockDir,{recursive:true,mode:0o700});
let lockFd;
try {
  lockFd=fs.openSync(lockPath,'wx',0o600);
  const lockRecord={schema_version:'release-lock/v1',pid:process.pid,created_at:Date.now(),fencing_token:crypto.randomBytes(24).toString('hex')};
  fs.writeFileSync(lockFd,JSON.stringify(lockRecord)+'\n');
  fs.fsyncSync(lockFd);
} catch (error) {
  if(error?.code==='EEXIST') { console.error('release_lock_held'); process.exit(2); }
  throw error;
}

if(fs.existsSync('dist')) fs.cpSync('dist','dist.previous',{recursive:true});
try {
  execFileSync('node',['scripts/prepare-content.mjs'],{stdio:'inherit'});
  execFileSync('node',['scripts/leak-gate.mjs','--scope','input-tree','../var/queries/public','../release/public-confirmations'],{stdio:'inherit'});
  execFileSync('node',['scripts/build-graph.mjs'],{stdio:'inherit'});
  execFileSync('node',['scripts/leak-gate.mjs','--scope','staging','src/content','public/generated'],{stdio:'inherit'});
  execFileSync('npx',['astro','build','--outDir','dist.next'],{stdio:'inherit'});
  const catalog = JSON.parse(fs.readFileSync('public/generated/catalog.json', 'utf8'));
  const routes = new Set(['/','/graph/']);
  for (const item of catalog.items || []) {
    const route = String(item.route || '').replace(/^\//, '').replace(/\/$/, '');
    if (route) routes.add(`/${route}/`);
  }
  const sitemap = [...routes].sort().map((route) => `  <url><loc>${route}</loc></url>`).join('\n');
  fs.writeFileSync('dist.next/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${sitemap}\n</urlset>\n`, { mode: 0o600 });
  execFileSync('node',['scripts/validate-build.mjs','dist.next'],{stdio:'inherit'});
  execFileSync('node',['scripts/leak-gate.mjs','--scope','dist','dist.next'],{stdio:'inherit'});
  fs.rmSync('dist',{recursive:true,force:true});
  fs.renameSync('dist.next','dist');
} catch(error) {
  fs.rmSync('dist.next',{recursive:true,force:true});
  if(fs.existsSync('dist.previous')) { fs.rmSync('dist',{recursive:true,force:true}); fs.renameSync('dist.previous','dist'); }
  process.exitCode=1;
} finally {
  if(lockFd!==undefined) fs.closeSync(lockFd);
  try { fs.unlinkSync(lockPath); } catch {}
}
