import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { dev } from 'astro';

const repo = path.resolve('..');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'myk-browser-'));
fs.chmodSync(root, 0o700);
fs.writeFileSync(path.join(root, '.browser-fixture'), '');
const python = process.env.MYKNOWLEDGE_PYTHON || (fs.existsSync(path.join(repo, '.venv/bin/python')) ? path.join(repo, '.venv/bin/python') : 'python3');
const children = [];
let closing = false;
let astro;
async function shutdown(code = 0) {
  if (closing) return;
  closing = true;
  if (astro) await astro.stop();
  await Promise.all(children.map(async (child) => {
    if (child.exitCode !== null || child.signalCode) return;
    const exited = once(child, 'exit');
    child.kill('SIGTERM');
    const timer = setTimeout(() => child.kill('SIGKILL'), 5000);
    await exited;
    clearTimeout(timer);
  }));
  fs.rmSync(root, { recursive: true, force: true });
  process.exit(code);
}
process.on('SIGTERM', () => shutdown());
process.on('SIGINT', () => shutdown());
function start(command, args, options = {}) {
  const child = spawn(command, args, { stdio: 'inherit', ...options });
  children.push(child);
  child.on('error', (error) => { console.error(error.message); shutdown(1); });
  child.on('exit', () => { if (!closing) shutdown(1); });
  return child;
}
try {
  const probe = net.createServer();
  probe.listen(0, '127.0.0.1');
  await once(probe, 'listening');
  const apiPort = probe.address().port;
  await new Promise((resolve) => probe.close(resolve));
  start(python, ['-m', 'tests.browser_fixture', '--root', root, '--port', String(apiPort)], { cwd: repo });
  let ready = false;
  for (let i = 0; i < 200 && !closing; i++) {
    try { ready = (await fetch(`http://127.0.0.1:${apiPort}/api/health`)).ok; } catch {}
    if (ready) break;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  if (!ready) throw new Error('fixture_api_startup_failed');
  Object.assign(process.env, { PUBLIC_BASE_PATH: '/', MYK_E2E_ROOT: root, MYK_E2E_API_PORT: String(apiPort) });
  // Programmatic lifecycle avoids Astro CLI agent auto-background behavior.
  astro = await dev({
    configFile: 'e2e/helpers/local-astro.config.mjs',
    server: { host: '127.0.0.1', port: Number(process.env.MYK_E2E_PORT || 14321) },
  });
} catch (error) {
  console.error(error.message);
  await shutdown(1);
}
