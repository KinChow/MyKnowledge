import fs from 'node:fs'; if(!fs.existsSync('../config/schemas.yaml')||!fs.existsSync('../config/policy.yaml')) throw new Error('config_missing'); console.log('config_valid');
