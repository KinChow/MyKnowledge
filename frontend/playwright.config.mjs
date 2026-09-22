import { defineConfig } from '@playwright/test';

const local = process.env.MYK_E2E_SUITE === 'local';
const port = Number(process.env.MYK_E2E_PORT || (local ? 14321 : 14322));
const channel = process.env.MYK_E2E_CHANNEL;
const suite = local ? 'local' : 'public';
if (channel && channel !== 'chrome') throw new Error('Use chrome or omit MYK_E2E_CHANNEL for Chromium');

export default defineConfig({
  testDir: './e2e',
  testMatch: local ? 'local.spec.mjs' : 'public.spec.mjs',
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: 0,
  timeout: 45_000,
  expect: { timeout: 12_000 },
  reporter: [['list'], ['html', { open: 'never', outputFolder: `playwright-report/${suite}` }]],
  outputDir: `test-results/${suite}`,
  use: {
    browserName: 'chromium',
    ...(channel ? { channel } : {}),
    baseURL: `http://127.0.0.1:${port}`,
    viewport: { width: 1440, height: 1000 },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: `node e2e/helpers/${local ? 'local-server' : 'public-server'}.mjs`,
    url: `http://127.0.0.1:${port}/${local ? 'practice/' : 'MyKnowledge/'}`,
    reuseExistingServer: false,
    timeout: 120_000,
    env: { MYK_E2E_PORT: String(port), PUBLIC_BASE_PATH: local ? '/' : '/MyKnowledge/' },
    gracefulShutdown: { signal: 'SIGTERM', timeout: 10_000 },
  },
});
