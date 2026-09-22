import fs from 'node:fs'; import path from 'node:path';
import {pythonBridge} from './python-bridge.mjs';
import {routePath} from '../src/lib/routes.js';
const base = process.env.PUBLIC_BASE_PATH || '/';
const root = process.env.MYKNOWLEDGE_ROOT ? path.resolve(process.env.MYKNOWLEDGE_ROOT) : path.resolve('..'); const out = path.resolve('src/content/docs'); const manifestPath = process.env.MYKNOWLEDGE_MANIFEST || path.join(root,'var/queries/public/manifest.json');
if (!fs.existsSync(manifestPath)) { if (process.env.MYKNOWLEDGE_CONTENT_MODE === 'projection') throw new Error('manifest_missing'); throw new Error('manifest_missing'); }
const manifest = pythonBridge('export', root, manifestPath);
// body 引用的本地图片（Typora 式 `X.assets/...`）随 md 复制到相同相对路径——
// 附件与正文同属发布物；缺图/路径越界/禁区目录一律 fail-closed，不做静默降级
function copyBodyImages(objectId, bodyPath, body, outDir){
  const refs=new Set();
  for(const m of body.matchAll(/!\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)) refs.add(m[1]);
  for(const m of body.matchAll(/<img[^>]+src=["']([^"']+)["']/g)) refs.add(m[1]);
  for(const ref of refs){
    if(/^(https?:)?\/\//i.test(ref) || ref.startsWith('data:')) continue;
    const clean=ref.replace(/^\.\//,'');
    const src=path.resolve(path.dirname(bodyPath),clean);
    const rel=path.relative(root,src);
    if(!src.startsWith(root+path.sep) || /(^|[\\/])(sources|archive|practice|state|queries[\\/]local)([\\/]|$)/i.test(rel)) throw new Error(`image_path_forbidden:${objectId}:${ref}`);
    if(!fs.existsSync(src) || !fs.statSync(src).isFile()) throw new Error(`image_unresolved:${objectId}:${ref}`);
    let cursor=root;
    for (const part of rel.split(path.sep)) { cursor=path.join(cursor,part); if(fs.lstatSync(cursor).isSymbolicLink()) throw new Error(`image_path_forbidden:${objectId}:${ref}`); }
    if(fs.statSync(src).nlink!==1) throw new Error(`image_path_forbidden:${objectId}:${ref}`);
    const dest=path.resolve(outDir, path.relative(path.dirname(bodyPath), src));
    if(!dest.startsWith(out+path.sep)) throw new Error(`image_output_forbidden:${objectId}:${ref}`);
    fs.mkdirSync(path.dirname(dest),{recursive:true});
    fs.copyFileSync(src,dest);
  }
}
fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true}); const catalog=[]; const ids=new Set();
// 已发布页 id 集合 + 标题：用于把正文里的 [[slug]] 与相对 *.md 链接解析成 /wiki/<id>/ 路由。
// 仅在目标是已发布页时改写，未知目标一律原样保留（不制造新的 404）。
const validIds=new Set(manifest.items.map(i=>i.id)); const titleOf=new Map(manifest.items.map(i=>[i.id,i.title||i.id]));
// 内链解析（对齐 Obsidian/Quartz 的成熟三层：归一化 + 声明式别名 + 坏链兜底/报告）：
// 1) 大小写归一：[[Name]] 与相对 *.md 文件名可能与已发布 id 仅大小写不同（UML→uml、SOLID→solid）；仅小写唯一时接受，避免碰撞误链。
// 2) 声明式别名：读已发布对象 front-matter 的 aliases，建立 alias→id 映射（源=对象本身，不经受哈希门禁的 manifest；aliases 不入 release_input，故加别名不破坏发布确认）。
// 3) 坏链兜底：仍解析不到的目标一律不显示原始 [[]] / 不留相对 .md 死链，降级为纯文本，并汇总到 link-report.json，暴露给作者决定建页/删链。
// 全程只改写到"已发布页"，绝不猜后缀式别名（Quartz "shortest" 猜链有已知误链坑）。
const lowerToId=new Map(); const ambiguousLower=new Set();
for(const it of manifest.items){ const lk=it.id.toLowerCase(); if(lowerToId.has(lk)&&lowerToId.get(lk)!==it.id){ambiguousLower.add(lk);} else {lowerToId.set(lk,it.id);} }
const aliasToId=new Map(); const ambiguousAlias=new Set();
for(const it of manifest.items){ for(const a of it.aliases || []){ const lk=String(a).trim().toLowerCase(); if(!lk||validIds.has(lk)||lowerToId.has(lk))continue; if(aliasToId.has(lk)&&aliasToId.get(lk)!==it.id){ambiguousAlias.add(lk);} else {aliasToId.set(lk,it.id);} } }
function canonicalId(raw){ if(validIds.has(raw))return raw; const lk=String(raw).toLowerCase(); if(!ambiguousLower.has(lk)&&lowerToId.has(lk))return lowerToId.get(lk); if(!ambiguousAlias.has(lk)&&aliasToId.has(lk))return aliasToId.get(lk); return null; }
const unresolvedLinks=[];
function resolveLinks(md, ownerId){
  md=md.replace(/\[\[([A-Za-z0-9][A-Za-z0-9_-]*)\]\]/g,(m,raw)=>{ const id=canonicalId(raw); return id?`[${titleOf.get(id)}](${routePath(base, `wiki/${id}`)})`:m; });
  md=md.replace(/\[([^\]]*)\]\(([^)\s]+?)\)/g,(m,text,url)=>{ if(/^(https?:|\/|#|mailto:)/i.test(url))return m; const mm=url.match(/([^/]+?)\.md(#.*)?$/i); if(!mm)return m; const id=canonicalId(mm[1]); if(id)return `[${text}](${routePath(base, `wiki/${id}`)}${mm[2]||''})`; unresolvedLinks.push({id:ownerId,kind:'md',target:url}); return text; });
  md=md.replace(/\[\[([^\[\]\n\\]+)\]\]/g,(m,inner)=>{ unresolvedLinks.push({id:ownerId,kind:'wikilink',target:inner}); return inner; });
  md=md.replace(/(\]\(|href=["'])(\/wiki\/[^)\s"']+)/g, (_, lead, url) => `${lead}${routePath(base, url)}`);
  return md;
}
for (const item of manifest.items) {
  if (ids.has(item.id)) throw new Error(`duplicate_id:${item.id}`);
  ids.add(item.id);
  const bodyPath=path.resolve(root,item.body_path);
  const body=item.body;
  const hash=item.content_sha256;
  const route=(item.route||item.id).replace(/^\/+|\/+$/g,'');
  if (!route || route.split('/').includes('..')) throw new Error(`route_invalid:${item.id}`);
  const target=path.join(out,route+'.md');
  fs.mkdirSync(path.dirname(target),{recursive:true});
  const rendered=resolveLinks(body,item.id);
  fs.writeFileSync(target,`---\ntitle: ${JSON.stringify(item.title||item.id)}\n---\n\n${rendered}`);
  copyBodyImages(item.id,bodyPath,body,path.dirname(target));
  catalog.push({id:item.id,title:item.title,route,links:item.links||[],domain:item.domain||null,kind:item.kind||null,tags:item.tags||[],content_sha256:hash});
}
// 链接完整性报告（Route 3）：汇总解析不到的内链，非致命（不破坏 fail-closed），供作者决定建页/删链/补别名。
// 写入 gitignore 的 var/state（运行态诊断），不污染受跟踪的 public projection 目录。
try{ const reportDir=path.join(root,'var/state'); fs.mkdirSync(reportDir,{recursive:true}); fs.writeFileSync(path.join(reportDir,'link-report.json'), JSON.stringify({schema_version:'link-report/v1', generated_at:new Date().toISOString(), total:unresolvedLinks.length, unresolved:unresolvedLinks},null,2)); }catch{}
if(unresolvedLinks.length){ const targets=[...new Set(unresolvedLinks.map(x=>x.target))]; console.warn(`[prepare-content] 未解析内链 ${unresolvedLinks.length} 处、去重 ${targets.length} 个（已降级为纯文本）：${targets.slice(0,12).join(', ')}${targets.length>12?' …':''}`); }
fs.mkdirSync('public/generated',{recursive:true}); fs.writeFileSync('public/generated/catalog.json',JSON.stringify({schema_version:'catalog/v1',generated_from:manifest.generated_from||'manifest',items:catalog},null,2));
if (catalog.length === 0) fs.writeFileSync(path.join(out, 'index.md'), '---\ntitle: MyKnowledge\ndescription: Evidence-driven public knowledge\n---\n\nPublic knowledge projection.\n');
