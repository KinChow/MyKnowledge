import fs from 'node:fs';
// 真校验：追踪矩阵存在且含 AC 编号（替换占位假验证）
const text = fs.readFileSync('../docs/traceability-matrix.md', 'utf8');
const acs = [...text.matchAll(/AC-F\d{3}-\d{3}/g)].length;
if (acs < 50) throw new Error(`traceability_ac_count_suspicious:${acs}`);
console.log(`docs_valid (${acs} AC refs)`);
