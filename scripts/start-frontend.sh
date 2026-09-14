#!/usr/bin/env bash
# 启动 Astro 本地开发服务（projection 输入 + /local-api 代理到 127.0.0.1:8765）。
# 用法：bash scripts/start-frontend.sh
# 与 start-backend.sh 解耦：可单独启动；练习页在后端起来后自动重连。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
frontend="$ROOT/frontend"
host="${MYKNOWLEDGE_FRONTEND_HOST:-127.0.0.1}"
port="${MYKNOWLEDGE_FRONTEND_PORT:-4321}"

# GitHub Desktop / GUI 终端不一定继承交互 shell 的 PATH。
if ! command -v node >/dev/null 2>&1; then
  node_dirs=(
    "/opt/homebrew/bin"
    "/usr/local/bin"
  )
  if [[ -n "${HOME:-}" ]]; then
    node_dirs+=(
      "$HOME/.volta/bin"
      "$HOME/.fnm/aliases/default/bin"
      "$HOME/.nvm/current/bin"
    )
  fi
  for node_dir in "${node_dirs[@]}"; do
    if [[ -x "$node_dir/node" ]]; then
      PATH="$node_dir:$PATH"
      export PATH
      break
    fi
  done
fi

if ! command -v node >/dev/null 2>&1; then
  printf '%s\n' "start-frontend requires Node.js, but 'node' is not on PATH." >&2
  exit 1
fi

astro="$frontend/node_modules/.bin/astro"
if [[ ! -x "$astro" ]]; then
  printf '%s\n' "start-frontend requires $astro; run scripts/bootstrap.sh first." >&2
  exit 1
fi

manifest="$ROOT/var/queries/public/manifest.json"
if [[ ! -f "$manifest" ]]; then
  printf '%s\n' "public projection missing: $manifest" >&2
  printf '%s\n' "run: $ROOT/.venv/bin/python -m tools.cli projection generate" >&2
  exit 1
fi

export MYKNOWLEDGE_ROOT="${MYKNOWLEDGE_ROOT:-$ROOT}"
export MYKNOWLEDGE_CONTENT_MODE="${MYKNOWLEDGE_CONTENT_MODE:-projection}"

cd "$frontend"
printf '%s\n' "== prepare-content (${MYKNOWLEDGE_CONTENT_MODE}) =="
node scripts/prepare-content.mjs
printf '%s\n' "== build-graph =="
node scripts/build-graph.mjs

printf '%s\n' "MyKnowledge UI   http://${host}:${port}/"
printf '%s\n' "practice         http://${host}:${port}/practice/  （后端稍后启动也会自动接上）"
printf '%s\n' "API proxy        /local-api -> http://127.0.0.1:8765/api"

exec "$astro" dev --host "$host" --port "$port" "$@"
