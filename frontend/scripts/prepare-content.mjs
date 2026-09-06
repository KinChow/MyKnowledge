import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
const root = process.env.MYKNOWLEDGE_ROOT ? path.resolve(process.env.MYKNOWLEDGE_ROOT) : path.resolve('..'); const out = path.resolve('src/content/docs'); const manifestPath = path.join(root,'var/queries/public/manifest.json');
if (!fs.existsSync(manifestPath)) { if (process.env.MYKNOWLEDGE_CONTENT_MODE === 'projection') throw new Error('manifest_missing'); process.exit(0); }
const manifest = JSON.parse(fs.readFileSync(manifestPath,'utf8')); if (manifest.schema_version !== 'public-projection/v1' || manifest.projection !== 'public' || !Array.isArray(manifest.items)) throw new Error('manifest_invalid');
function canonical(value){ if(Array.isArray(value)) return '['+value.map(canonical).join(',')+']'; if(value&&typeof value==='object') return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}'; return JSON.stringify(value); }
// canonicalBody：与 tools.common.canonical_body 同一契约（§6.6：LF 统一、去行尾空白、
// 末尾空行折叠为单个换行）——content_sha256 对 canonical body 计算，不能 hash 原文。
// 行尾空白字符集与 Python str.rstrip()（str.isspace）对齐：注意 JS 的 \s 额外匹配
// U+FEFF，而 Python 不视其为空白——混用会让含 BOM 字符的行哈希不一致
function canonicalBody(body){ const lines=body.replace(/\r\n/g,'\n').replace(/\r/g,'\n').split('\n').map(l=>l.replace(/[\t\v\f \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+$/,'')); while(lines.length&&lines[lines.length-1]==='') lines.pop(); lines.push(''); return lines.join('\n'); }
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
    const dest=path.join(outDir, path.relative(path.dirname(bodyPath), src));
    fs.mkdirSync(path.dirname(dest),{recursive:true});
    fs.copyFileSync(src,dest);
  }
}
fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true}); const catalog=[]; const ids=new Set();
for (const item of manifest.items) { if (item.vault_id !== 'public' || item.public_publishable !== true || item.public_release !== true || item.status !== 'published' || item.effective_confidentiality !== 'public') throw new Error(`item_not_public:${item.id}`); if (ids.has(item.id)) throw new Error(`duplicate_id:${item.id}`); ids.add(item.id); const confirmation=item.public_confirmation_path; if(typeof confirmation!=='string'||!/^release[\\/]public-confirmations[\\/][a-z0-9-]+\.json$/i.test(confirmation)) throw new Error(`confirmation_path_invalid:${item.id}`); const eventPath=path.resolve(root,confirmation); if(!eventPath.startsWith(root+path.sep)||!fs.existsSync(eventPath)) throw new Error(`confirmation_missing:${item.id}`); const event=JSON.parse(fs.readFileSync(eventPath,'utf8')); if(event.schema_version!=='public-release-confirmation/v1'||event.actor_type!=='human'||event.decision!=='approve'||event.target_vault!=='public'||event.target_ref?.vault_id!=='public'||event.target_ref?.object_type!=='wiki'||event.target_ref?.object_id!==item.id) throw new Error(`confirmation_mismatch:${item.id}`); const eventHash='sha256:'+crypto.createHash('sha256').update(canonical(Object.fromEntries(Object.entries(event).filter(([key])=>key!=='event_sha256')))).digest('hex'); if(event.event_sha256!==eventHash) throw new Error(`confirmation_hash_mismatch:${item.id}`); if(item.public_confirmation_sha256&&item.public_confirmation_sha256!==eventHash) throw new Error(`confirmation_manifest_hash_mismatch:${item.id}`); if(item.release_input_sha256!==event.release_input_sha256||item.content_sha256!==event.reviewed_content_sha256||item.evidence_sha256!==event.reviewed_evidence_sha256) throw new Error(`confirmation_precondition_mismatch:${item.id}`); const bodyPath=path.resolve(root,item.body_path); const rel=path.relative(root,bodyPath); if (!bodyPath.startsWith(root+path.sep) || /(^|[\\/])(sources|archive|practice|state|queries[\\/]local)([\\/]|$)/i.test(rel) || !fs.existsSync(bodyPath)) throw new Error(`body_unresolved:${item.id}`); const raw=fs.readFileSync(bodyPath,'utf8'); // body 提取与 tools.front_matter.FrontMatter.parse 对齐：
// 只剥 `---\\n...\\n---\\n` 前缀，保留其后内容（含紧随的空行）——该换行参与
// validator 的 content_sha256，多剥会让近期批次（FM 后有空行）哈希校验必失败
const body=raw.replace(/^---\n[\s\S]*?\n---\n/,''); const hash='sha256:'+crypto.createHash('sha256').update(canonicalBody(body)).digest('hex'); if (item.content_sha256 && item.content_sha256 !== hash) throw new Error(`body_hash_mismatch:${item.id}`); const route=(item.route||item.id).replace(/^\/+|\/+$/g,''); const target=path.join(out,route+'.md'); fs.mkdirSync(path.dirname(target),{recursive:true}); fs.writeFileSync(target,`---\ntitle: ${JSON.stringify(item.title||item.id)}\n---\n\n${raw.replace(/^---\n[\s\S]*?\n---\n/,'')}`); copyBodyImages(item.id,bodyPath,raw.replace(/^---\n[\s\S]*?\n---\n/,''),path.dirname(target)); catalog.push({id:item.id,title:item.title,route,links:item.links||[],domain:item.domain||null,kind:item.kind||null,tags:item.tags||[],content_sha256:hash}); }
fs.mkdirSync('public/generated',{recursive:true}); fs.writeFileSync('public/generated/catalog.json',JSON.stringify({schema_version:'catalog/v1',generated_from:manifest.generated_from||'manifest',items:catalog},null,2));
if (catalog.length === 0) fs.writeFileSync(path.join(out, 'index.md'), '---\ntitle: MyKnowledge\ndescription: Evidence-driven public knowledge\n---\n\nPublic knowledge projection.\n');
