import { test, expect } from '@playwright/test';

async function connect(page, topic) {
  await page.goto('/practice/');
  await expect(page.locator('#connection-status')).toContainText('已连接');
  await page.locator('#topic').fill(topic);
  await page.locator('#start-session').click();
  await expect(page.locator('.mk-practice-question h2')).toContainText(`E2E ${topic}`);
}
test.beforeEach(async ({ page }) => {
  page.runtimeErrors = [];
  page.on('pageerror', (e) => page.runtimeErrors.push(e.message));
});
test.afterEach(async ({ page }) => { expect(page.runtimeErrors).toEqual([]); });

test('proxy connects without exposing capability to browser storage or headers', async ({ page }) => {
  const headers = [];
  page.on('request', (req) => {
    if (req.url().includes('/local-api/')) headers.push(req.headers());
  });
  await page.goto('/practice/');
  await expect(page.locator('#connection-status')).toContainText('5 道题');
  expect(headers.length).toBeGreaterThan(0);
  expect(headers.every((h) => !h['x-myknowledge-capability'])).toBe(true);
  expect(await page.evaluate(() => JSON.stringify({ ...localStorage, ...sessionStorage }))).not.toMatch(/capability|token/i);
});

test('backend unavailable has a clear recoverable state', async ({ page }) => {
  await page.route('**/local-api/**', (route) => route.abort('connectionrefused'));
  await page.goto('/practice/');
  await expect(page.getByRole('heading', { name: '等待本地 API' })).toBeVisible();
  await expect(page.locator('#control-status')).toContainText('未启动');
  await page.unroute('**/local-api/**');
  await expect(page.locator('#connection-status')).toContainText('已连接');
});

test('single choice answer -> FSRS review -> completed session persists', async ({ page }) => {
  await connect(page, 'single');
  await page.locator('input[value="a"]').check();
  await page.getByRole('button', { name: '提交答案', exact: true }).click();
  await expect(page.locator('.mk-practice-feedback')).toContainText('回答正确');
  const sessionId = await page.evaluate(() => sessionStorage.getItem('myknowledge:practice:session:v1'));
  const reviewed = page.waitForResponse((r) => r.url().includes('/review?') && r.request().method() === 'POST');
  await page.getByRole('button', { name: '良好', exact: true }).click();
  expect((await (await reviewed).json()).schedule.state).toBe('scheduled');
  await expect(page.locator('.mk-practice-feedback')).toContainText('复习计划已更新');
  await page.getByRole('button', { name: '完成练习', exact: true }).click();
  await expect(page.getByRole('heading', { name: '这一轮完成' })).toBeVisible();
  const persisted = await page.evaluate(async (id) => (await fetch(`/local-api/practice/sessions/${id}?scope=local`)).json(), sessionId);
  expect(persisted.session.completed).toBe(true);
});

test('multi choice submits list of IDs and shows grading', async ({ page }) => {
  await connect(page, 'multi');
  await page.locator('input[value="a"]').check();
  await page.locator('input[value="b"]').check();
  const answer = page.waitForRequest((r) => r.url().includes('/answer?'));
  await page.getByRole('button', { name: '提交答案', exact: true }).click();
  expect((await answer).postDataJSON().sort()).toEqual(['a', 'b']);
  await expect(page.locator('.mk-practice-feedback')).toContainText('回答正确');
});

test('session refresh resumes the saved next question', async ({ page }) => {
  await connect(page, 'resume');
  await expect(page.locator('#progress')).toContainText('1 / 2');
  await page.getByRole('button', { name: '跳过', exact: true }).click();
  await expect(page.locator('#progress')).toContainText('2 / 2');
  const prompt = await page.locator('.mk-practice-question h2').textContent();
  await page.reload();
  await expect(page.locator('#control-status')).toContainText('已恢复');
  await expect(page.locator('#progress')).toContainText('2 / 2');
  await expect(page.locator('.mk-practice-question h2')).toHaveText(prompt);
});

test('structured answer rejection is visible and retryable', async ({ page }) => {
  await connect(page, 'error');
  await page.route('**/practice/*/answer?*', (route) => route.fulfill({
    status: 422, contentType: 'application/json',
    body: JSON.stringify({ detail: { code: 'response_option_unknown' } }),
  }));
  await page.locator('input[value="a"]').check();
  await page.getByRole('button', { name: '提交答案', exact: true }).click();
  await expect(page.locator('.mk-practice-feedback')).toContainText('提交失败：response_option_unknown');
  await expect(page.getByRole('button', { name: '提交答案', exact: true })).toBeEnabled();
  await page.unroute('**/practice/*/answer?*');
  // The real domain API returns HTTP 200 + status=blocked for malformed answers.
  // Do not let the UI misrepresent this as an accepted ungraded answer.
  await page.route('**/practice/*/answer?*', (route) => route.continue({
    postData: JSON.stringify({ malformed: true }),
  }));
  const blocked = page.waitForResponse((r) => r.url().includes('/answer?'));
  await page.getByRole('button', { name: '提交答案', exact: true }).click();
  expect((await (await blocked).json()).status).toBe('blocked');
  await expect(page.locator('.mk-practice-feedback')).toContainText('提交失败：response_option_unknown');
  await expect(page.getByRole('button', { name: '提交答案', exact: true })).toBeEnabled();
  await page.unroute('**/practice/*/answer?*');
  await page.getByRole('button', { name: '提交答案', exact: true }).click();
  await expect(page.locator('.mk-practice-feedback')).toContainText('回答正确');
});
