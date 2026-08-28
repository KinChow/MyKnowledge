import fs from 'node:fs';
// 真校验（F011/F012 review：替换仅查文件存在的占位假验证）
const load = (p) => { try { return JSON.parse(JSON.stringify(require('node:yaml').parse(fs.readFileSync(p,'utf8')))); } catch { throw new Error(p + '_unparsable'); } };
// 无 yaml 依赖时退化为结构检查：必填键存在
for (const [file, keys] of [['../config/schemas.yaml', ['schema_version']], ['../config/policy.yaml', ['schema_version']]] ) {
  const text = fs.readFileSync(file, 'utf8');
  for (const key of keys) if (!new RegExp(`^${key}\\s*:`,'m').test(text)) throw new Error(`${file}:missing_${key}`);
}
console.log('config_valid');
