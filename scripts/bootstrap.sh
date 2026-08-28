#!/usr/bin/env bash
# MyKnowledge 一键引导：Python venv + 依赖 + 前端依赖 + 自检。
# 用法：bash scripts/bootstrap.sh（在仓库根执行）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== 1/4 Python venv =="
if [ ! -x ".venv/bin/python" ]; then
  python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" || {
    echo "需要 Python >= 3.12"; exit 1; }
  python3 -m venv .venv
fi

echo "== 2/4 Python 依赖 =="
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt

echo "== 3/4 前端依赖（可选，仅静态站构建需要）=="
if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install --silent)
else
  echo "跳过：未安装 npm（静态站构建时再装）"
fi

echo "== 4/5 中文分词扩展（可选，缺失回退 unicode61 并告警）=="
if [ ! -f state/lib/libsimple.dylib ] && [ ! -f state/lib/libsimple.so ]; then
  SIMPLE_VER=v0.7.1
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64) ASSET=libsimple-osx-arm64.zip ;;
    Darwin-x86_64) ASSET=libsimple-osx-x64.zip ;;
    Linux-x86_64) ASSET=libsimple-linux-ubuntu-latest.zip ;;
    Linux-aarch64) ASSET=libsimple-linux-ubuntu-24.04-arm.zip ;;
    *) ASSET="" ;;
  esac
  if [ -n "$ASSET" ] && command -v curl >/dev/null 2>&1; then
    curl -sL "https://github.com/wangfenjin/simple/releases/download/${SIMPLE_VER}/${ASSET}" -o /tmp/libsimple.zip \
      && mkdir -p state/lib && cd /tmp && unzip -o -q libsimple.zip && cd - >/dev/null \
      && cp /tmp/libsimple*/libsimple.* state/lib/ 2>/dev/null; cp -r /tmp/libsimple*/dict state/lib/ 2>/dev/null; chmod +x state/lib/libsimple* 2>/dev/null
    echo "simple: $(ls state/lib/libsimple* 2>/dev/null || echo 下载失败，回退 unicode61)"
  else
    echo "simple: 平台不支持或无 curl，回退 unicode61"
  fi
else
  echo "simple: 已安装"
fi

echo "== 5/5 自检 =="
.venv/bin/python -m pytest -q 2>&1 | tail -1

echo
echo "可选外部依赖（按需安装，缺失时对应能力自动降级并显式告警）："
echo "  qmd      - 语义/向量检索（缺失 -> FTS5 降级）"
echo "  git lfs  - archive/raw 二进制快照（缺失 -> text-only 归档）"
echo "完成。日常入口：python -m tools.cli（查看命令列表）/ python -m tools.cli doctor"
