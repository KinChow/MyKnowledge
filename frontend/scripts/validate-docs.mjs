import fs from 'node:fs'; if(!fs.existsSync('../docs/traceability-matrix.md')) throw new Error('traceability_missing'); console.log('docs_valid');
