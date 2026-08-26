import fs from 'node:fs'; import path from 'node:path';
const p=process.argv[2]||'../queries/public/manifest.json';
if(!fs.existsSync(p)) throw new Error('manifest_missing');
const manifest=JSON.parse(fs.readFileSync(p,'utf8'));
if(manifest.schema_version!=='public-projection/v1'||manifest.projection!=='public'||!Array.isArray(manifest.items)) throw new Error('manifest_invalid');
const ids=new Set();
for(const item of manifest.items){
  if(!item||typeof item.id!=='string'||ids.has(item.id)) throw new Error('duplicate_or_invalid_id');
  ids.add(item.id);
  if(item.vault_id!=='public'||item.public_publishable!==true||item.public_release!==true||item.status!=='published'||item.effective_confidentiality!=='public') throw new Error(`item_not_public:${item.id}`);
  if(typeof item.body_path!=='string'||path.isAbsolute(item.body_path)||/%(?:2f|5c|2e)/i.test(item.body_path)) throw new Error(`body_path_invalid:${item.id}`);
  const normalized=path.posix.normalize(item.body_path.replaceAll('\\','/'));
  if(normalized.startsWith('../')||/(^|\/)(sources|archive|practice|state|queries\/local)(\/|$)/i.test(normalized)) throw new Error(`body_path_forbidden:${item.id}`);
}
console.log('projection_input_valid');
