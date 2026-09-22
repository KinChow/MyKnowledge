import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const codeRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export function pythonBridge(action, root, manifest) {
  const local = path.join(codeRoot, '.venv/bin/python');
  const python = process.env.MYKNOWLEDGE_PYTHON || (fs.existsSync(local) ? local : 'python3');
  const args = ['-m', 'tools.release_build', action, '--root', root];
  if (manifest) args.push('--manifest', manifest);
  try {
    return JSON.parse(execFileSync(python, args, {
      cwd: codeRoot, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024,
      env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'},
    }));
  } catch (error) {
    throw new Error(error.stdout?.toString() || 'release_python_failed');
  }
}
