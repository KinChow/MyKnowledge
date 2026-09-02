#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# GitHub Desktop does not always inherit the interactive shell PATH. Keep the
# test command usable there while still honoring an explicitly configured PATH.
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
  printf '%s\n' "pre-push pytest requires Node.js, but 'node' is not on PATH." >&2
  printf '%s\n' "Install Node.js or configure PATH before pushing." >&2
  exit 1
fi

python="$repo_root/.venv/bin/python"
if [[ ! -x "$python" ]]; then
  printf '%s\n' "pre-push pytest requires $python; run scripts/bootstrap.sh first." >&2
  exit 1
fi

exec "$python" -m pytest -q
