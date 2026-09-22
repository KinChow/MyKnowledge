import path from 'node:path';
import config from '../../astro.config.mjs';
import { localApiProxy } from '../../src/lib/local-api-proxy.mjs';

if (!process.env.MYK_E2E_ROOT || !process.env.MYK_E2E_API_PORT) throw new Error('Start through local-server.mjs');
export default {
  ...config,
  base: '/',
  cacheDir: path.join(process.env.MYK_E2E_ROOT, 'astro-cache'),
  vite: {
    ...config.vite,
    server: {
      strictPort: true,
      proxy: {
        '/local-api': localApiProxy(
          `http://127.0.0.1:${process.env.MYK_E2E_API_PORT}`,
          path.join(process.env.MYK_E2E_ROOT, 'var/state/capability-token'),
        ),
      },
    },
  },
};
