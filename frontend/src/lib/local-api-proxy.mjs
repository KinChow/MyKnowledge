import fs from 'node:fs';

// Server-only: the credential is injected by Vite, never serialized to the client.
export function localApiProxy(target, tokenPath) {
  const url = new URL(target);
  if (url.protocol !== 'http:' || !['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname)) {
    throw new Error('local_api_requires_loopback');
  }
  return {
    target,
    rewrite: (requestPath) => requestPath.replace(/^\/local-api/, '/api'),
    configure(proxy) {
      proxy.on('proxyReq', (request) => {
        if (fs.existsSync(tokenPath)) {
          request.setHeader('X-MyKnowledge-Capability', fs.readFileSync(tokenPath, 'utf8').trim());
        }
      });
    },
  };
}
