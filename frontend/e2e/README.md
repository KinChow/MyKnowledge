# Browser regression gates

12 tests, two surfaces; one implementation runs in Chromium (CI) or Google Chrome.
No external model/service calls and no writes to personal practice data.

## Run

From the repository root:

```bash
npm --prefix frontend ci
npm --prefix frontend exec -- playwright install chromium
.venv/bin/python -m pip install -r requirements-browser.txt

# Recommended before push: committed release inputs required.
PUBLIC_BASE_PATH=/MyKnowledge/ npm --prefix frontend run check:browser

# Repeat against an already built release, or local fixture only:
npm --prefix frontend run test:browser:public
npm --prefix frontend run test:browser:local

# Use installed Google Chrome rather than Playwright's pinned Chromium:
MYK_E2E_CHANNEL=chrome npm --prefix frontend run check:browser
```

`test:browser:public` alone does not prove dist belongs to current Git HEAD;
`check:browser` rebuilds first and is the CI/pre-push authority. Dirty release inputs
are intentionally blocked. Do not bypass the gate or use an old dist as new evidence.
For development of tests, `MYK_E2E_DIST=/absolute/path/to/validated/dist` selects an
explicit artifact; disclose that artifact's source revision in the report.

## Coverage

- Public: homepage/article/deep reload, body link/heading anchor, real Pagefind index
  (fallback is not a pass), Cytoscape rendering/node detail/navigation, no local API
  traffic or public practice route, narrow viewport/search/theme.
- Local: shared Vite proxy with server-injected credentials, offline/recovery,
  single-choice/FSRS/completion persistence, multi-choice list payload, session
  refresh, structured HTTP and domain errors with retry.

The local helper creates a private temporary root and a five-question synthetic
fixture. FastAPI and Astro run only on loopback and are stopped at teardown; the
temporary root is removed. It never reads the checkout's capability token and never
writes `content/practice`. The shared production `localApiProxy` is used unchanged
with a test-only backend port and token path. Only network-failure/error scenarios
intercept requests; normal learning flows use real HTTP and disk persistence.

Ports default to 14321 (local) / 14322 (public). `MYK_E2E_PORT` may override them.
Existing servers are never reused or killed; occupied ports fail the run. The API
fixture chooses an ephemeral loopback port. `MYKNOWLEDGE_PYTHON` overrides Python.

## Submission and CI

- Existing pre-commit fast checks remain; pre-push now runs pytest, real release,
  and both browser suites. Install the hook with `pre-commit install --hook-type pre-push`.
- PR/push `frontend-gates` runs both suites after the `/MyKnowledge/` build.
- Pages upload/deploy requires the public browser suite after build.
- No scheduled local monitoring or cron/heartbeat task.
- Failures retain trace/screenshot/HTML report under `test-results/<suite>` and
  `playwright-report/<suite>` (gitignored); CI uploads these for seven days.
- No automatic retries conceal instability. No full-page screenshot baselines,
  multi-browser matrix, or custom test framework.
