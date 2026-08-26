import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const lockDir=path.resolve('../state');
const lockPath=path.join(lockDir,'public-release.lock');
fs.mkdirSync(lockDir,{recursive:true,mode:0o700});
let lockFd;
try {
  lockFd=fs.openSync(lockPath,'wx',0o600);
  fs.writeFileSync(lockFd,JSON.stringify({pid:process.pid,created_at:Date.now()})+'\n');
} catch (error) {
  if(error?.code==='EEXIST') { console.error('release_lock_held'); process.exit(2); }
  throw error;
}

if(fs.existsSync('dist')) fs.cpSync('dist','dist.previous',{recursive:true});
try {
  execFileSync('node',['scripts/prepare-content.mjs'],{stdio:'inherit'});
  execFileSync('node',['scripts/build-graph.mjs'],{stdio:'inherit'});
  execFileSync('npx',['astro','build','--outDir','dist.next'],{stdio:'inherit'});
  execFileSync('node',['scripts/validate-build.mjs','dist.next'],{stdio:'inherit'});
  execFileSync('node',['scripts/leak-gate.mjs','dist.next'],{stdio:'inherit'});
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
