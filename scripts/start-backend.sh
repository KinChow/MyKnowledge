#!/usr/bin/env bash
# 启动本地 FastAPI（loopback only）。
# 用法：bash scripts/start-backend.sh [--port 8765] [--host 127.0.0.1]
# 写入/练习接口需要 capability token：进程启动后写在 var/state/capability-token（0600）。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python="$ROOT/.venv/bin/python"
if [[ ! -x "$python" ]]; then
  printf '%s\n' "start-backend requires $python; run scripts/bootstrap.sh first." >&2
  exit 1
fi

host="${MYKNOWLEDGE_API_HOST:-127.0.0.1}"
port="${MYKNOWLEDGE_API_PORT:-8765}"

printf '%s\n' "MyKnowledge API  http://${host}:${port}/api/health"
printf '%s\n' "capability token  var/state/capability-token（进程退出后删除）"

exec "$python" -m backend.server --root "$ROOT" --host "$host" --port "$port" "$@"
