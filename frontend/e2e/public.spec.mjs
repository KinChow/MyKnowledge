import { test, expect } from '@playwright/test';

const base = '/MyKnowledge/';
test.beforeEach(async ({ page }) => {
  page.runtimeErrors = [];
  page.on('pageerror', (error) => page.runtimeErrors.push(error.message));
  page.on('response', (response) => {
    if (response.status() >= 400) page.runtimeErrors.push(`${response.status()} ${response.url()}`);
  });
  page.on('requestfailed', (request) => {
    if (!request.failure()?.errorText.includes('ERR_ABORTED')) page.runtimeErrors.push(request.url());
  });
});
test.afterEach(async ({ page }) => {
  expect(page.runtimeErrors).toEqual([]);
});

test('home article navigation and deep refresh retain project base', async ({ page }) => {
  await page.goto(base);
  const first = page.locator('[data-article-row] a[href*="/wiki/"]').first();
  const href = await first.getAttribute('href');
  expect(href).toMatch(/^\/MyKnowledge\/wiki\//);
  await first.click();
  await expect(page.locator('h1#_top')).toBeVisible();
  expect(new URL(page.url()).pathname).toBe(href);
  await page.reload();
  await expect(page.locator('[data-article-runtime]')).toBeVisible();
  await expect(page.locator('a[href^="/wiki/"]')).toHaveCount(0);
  await page.getByRole('link', { name: 'MyKnowledge', exact: true }).first().click();
  await expect(page).toHaveURL(new RegExp(`${base}$`));
});

test('body link and heading anchor are navigable', async ({ page, request }) => {
  const catalog = await (await request.get(`${base}generated/catalog.json`)).json();
  // Pick a real linked article, rather than a synthetic page that bypasses publication.
  let target;
  for (const item of catalog.items) {
    const route = `${base}${item.route.replace(/^\/+|\/+$/g, '')}/`;
    const html = await (await request.get(route)).text();
    const linked = await page.evaluate((text) => !!new DOMParser().parseFromString(text, 'text/html').querySelector('.sl-markdown-content a[href^="/MyKnowledge/wiki/"]'), html);
    if (linked) { target = route; break; }
  }
  expect(target, 'Published corpus must exercise at least one body wikilink').toBeTruthy();
  await page.goto(target);
  const body = page.locator('.sl-markdown-content');
  const anchor = body.locator('a[href^="#"]').first();
  await expect(anchor).toBeAttached();
  await anchor.click({ force: true });
  expect(new URL(page.url()).hash).not.toBe('');
  await body.locator('a[href^="/MyKnowledge/wiki/"]').first().click();
  await expect(page.locator('h1#_top')).toBeVisible();
  expect(new URL(page.url()).pathname).toMatch(/^\/MyKnowledge\/wiki\//);
});

test('Pagefind loads its real index and opens a result (no fallback)', async ({ page }) => {
  await page.goto(base);
  await page.locator('#open-search').click();
  await page.locator('#dialog-search-input').fill('CPU');
  const index = page.waitForResponse((r) => r.url().includes('/pagefind/') && r.ok());
  await page.locator('#dialog-search-form').evaluate((form) => form.requestSubmit());
  await index;
  await expect(page.locator('#search-status')).toContainText('找到');
  const result = page.locator('#search-results a').first();
  await expect(result).toHaveAttribute('href', /^\/MyKnowledge\/wiki\//);
  await result.click();
  await expect(page.locator('h1#_top')).toBeVisible();
});

test('graph renders canvas, focuses a node and opens the article', async ({ page }) => {
  await page.goto(`${base}graph/`);
  await expect(page.locator('#cy canvas').first()).toBeVisible();
  await expect(page.locator('#graph-status')).toContainText('条关系');
  await page.locator('#local-mode').click();
  await expect(page.locator('#graph-status')).toContainText('一跳局部图谱');
  await expect(page.locator('#node-panel h2')).toBeVisible();
  const link = page.locator('#node-panel a');
  await expect(link).toHaveAttribute('href', /^\/MyKnowledge\/wiki\//);
  await link.click();
  await expect(page.locator('[data-article-runtime]')).toBeVisible();
});

test('release never contacts the local API and excludes practice', async ({ page, request, baseURL }) => {
  const forbidden = [];
  page.on('request', (req) => {
    const url = new URL(req.url());
    // Static test server itself is loopback: reject other origins and API paths.
    if ((['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) && url.origin !== new URL(baseURL).origin)
      || /\/(?:local-api|api|practice)(?:\/|$)/.test(url.pathname)) forbidden.push(req.url());
  });
  await page.goto(base);
  await expect(page.locator('#practice-nav')).toBeHidden();
  await page.waitForTimeout(3500); // exceeds the previous 3s accidental polling interval
  expect(forbidden).toEqual([]);
  expect((await request.get(`${base}practice/`)).status()).toBe(404);
  expect(await page.evaluate(() => JSON.stringify({ ...localStorage, ...sessionStorage }))).not.toMatch(/capability|token/i);
});

test('narrow-screen navigation/search and theme remain usable', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(base);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  const previous = await page.locator('html').getAttribute('data-theme');
  await page.locator('#theme-toggle').click();
  await expect(page.locator('html')).not.toHaveAttribute('data-theme', previous);
  await page.locator('#open-search').click();
  await expect(page.locator('#dialog-search-input')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('#search-dialog')).not.toBeVisible();
});
