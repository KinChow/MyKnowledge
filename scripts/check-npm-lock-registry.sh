#!/usr/bin/env bash
# frontend/package-lock.json 的 resolved URL 必须指向公共 registry。
# 背景：lockfile 曾整份指向内网镜像 registry.npm.baidu-int.com，导致
# GitHub Actions 的 `npm ci` 全部失败（runner 不可达），且把内网主机名
# 写进了公开仓库。修复方式：
#   cd frontend && npm install --package-lock-only --registry=https://registry.npmjs.org
set -euo pipefail

lock="frontend/package-lock.json"
[[ -f "$lock" ]] || exit 0

if grep -n 'registry\.npm\.[a-z0-9.-]*-int\.[a-z]*' "$lock" >/dev/null; then
  echo "lock_registry_internal: $lock 含内网 registry URL，CI 无法安装" >&2
  grep -no 'registry\.npm\.[a-z0-9.-]*-int\.[a-z]*' "$lock" | head -3 >&2
  exit 1
fi
