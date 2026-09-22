import fs from 'node:fs';
import path from 'node:path';
const args=process.argv.slice(2);
const scopeIndex=args.indexOf('--scope');
const scope=scopeIndex>=0?args[scopeIndex+1]:'dist';
if(!['input-tree','staging','dist'].includes(scope)) throw new Error('leak_gate_scope_invalid');
const targets=args.filter((_,i)=>scopeIndex<0 || (i!==scopeIndex&&i!==scopeIndex+1));
const schema=scope==='input-tree'?'public-input-leak-gate/v1':'public-leak-gate/v1';
const pathLeak=/(^|\/)(sources|archive|practice|queries\/local)(\/|$)/i;
const sensitive=/confidentiality["']?\s*:\s*["']?internal\b|\bprivate\s+(?:key|vault|token|credential|password|secret|repo|data|information|content)\b|question\/v1|\breview_state\b|\bcorrect_option_ids\b/i;
const localPaths=/(?:content[\/\\](?:sources|practice)|var[\/\\](?:state|queries[\/\\]local)|\/Users\/[^/\s]+\/)/i;
const markup=/javascript:|<script[^>]*src=["'][^"']*file:|<iframe\b|\bon[a-z]+\s*=|\b(?:callback|click)\s+[^\n]*(?:https?:\/\/|javascript:|href)/i;
const contentExt=new Set(['.html','.htm','.json','.md','.css','.txt','.xml','.yaml','.yml','.js','.mjs','.map']);
const scripts=new Set(['.js','.mjs','.map']);
const findings=[];
function walk(p, root) {
  if(!fs.existsSync(p)) throw new Error(`leak_gate_input_missing:${p}`);
  const st=fs.lstatSync(p);
  if(st.isSymbolicLink()) throw new Error(`leak_gate_symlink:${p}`);
  if(st.isDirectory()) { for(const n of fs.readdirSync(p)) walk(path.join(p,n),root); return; }
  const rel=path.relative(root,p);
  if(pathLeak.test(rel)){ findings.push(rel); return; }
  const ext=path.extname(p).toLowerCase();
  if(!contentExt.has(ext))return;
  const text=fs.readFileSync(p,'utf8');
  // Vendor scripts contain literal HTML parsers and DOM handlers: do not apply
  // markup syntax rules to JavaScript. Data/credential rules still apply.
  if(sensitive.test(text) || localPaths.test(text) || (!scripts.has(ext) && markup.test(text))) findings.push(rel || path.basename(p));
}
for(const p of targets) walk(p,fs.existsSync(p)&&fs.statSync(p).isDirectory()?p:path.dirname(p));
if(findings.length){console.error(JSON.stringify({schema_version:schema,scope,findings}));process.exit(2);}
console.log(JSON.stringify({schema_version:schema,scope,findings:[]}));
