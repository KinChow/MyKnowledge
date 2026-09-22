#!/usr/bin/env bash
# MyKnowledge 一键引导：Python venv + 依赖 + 前端依赖 + 自检。
# 用法：bash scripts/bootstrap.sh（在仓库根执行）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== 1/6 Python venv =="
if [ ! -x ".venv/bin/python" ]; then
  python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" || {
    echo "需要 Python >= 3.12"; exit 1; }
  python3 -m venv .venv
fi

echo "== 2/6 Python 依赖 =="
.venv/bin/python -m pip install --quiet --upgrade pip
echo "    注：requirements.txt 含 marker-pdf[full]（PDF/PPT/DOCX → Markdown）及其 torch 依赖，体积较大（~GB 级），首次安装需耐心。"
.venv/bin/python -m pip install --quiet -r requirements.txt

echo "== 3/6 Marker 模型（可选，首次文档转换前需下载 ~2-4GB）=="
if command -v python3 >/dev/null 2>&1; then
  echo "    Marker 首次转换 PDF/PPT/DOCX 时会自动从 HuggingFace 下载 Surya 模型（~2-4GB，缓存于 ~/.cache/huggingface）。"
  echo "    如需预下载避免首次转换等待，可执行：.venv/bin/python -c \"from marker.models import create_model_dict; create_model_dict()\""
fi

echo "== 4/6 前端依赖（可选，仅静态站构建需要）=="
if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install --silent)
else
  echo "跳过：未安装 npm（静态站构建时再装）"
fi

echo "== 5/6 中文分词扩展（可选，缺失回退 unicode61 并告警）=="
SIMPLE_LIB_DIR="${ROOT}/var/state/lib"
if [ ! -f "$SIMPLE_LIB_DIR/libsimple.dylib" ] && [ ! -f "$SIMPLE_LIB_DIR/libsimple.so" ]; then
  SIMPLE_VER=v0.7.1
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64) ASSET=libsimple-osx-arm64.zip ;;
    Darwin-x86_64) ASSET=libsimple-osx-x64.zip ;;
    Linux-x86_64) ASSET=libsimple-linux-ubuntu-latest.zip ;;
    Linux-aarch64) ASSET=libsimple-linux-ubuntu-24.04-arm.zip ;;
    *) ASSET="" ;;
  esac
  if [ -n "$ASSET" ] && command -v curl >/dev/null 2>&1; then
    SIMPLE_TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/myknowledge-simple.XXXXXX")"
    cleanup_simple() { rm -r -- "$SIMPLE_TMP_DIR"; }
    trap cleanup_simple EXIT
    SIMPLE_ARCHIVE="$SIMPLE_TMP_DIR/libsimple.zip"
    SIMPLE_EXTRACT_DIR="$SIMPLE_TMP_DIR/extracted"
    SIMPLE_OK=false
    if curl -fsSL "https://github.com/wangfenjin/simple/releases/download/${SIMPLE_VER}/${ASSET}" -o "$SIMPLE_ARCHIVE" \
      && mkdir -p "$SIMPLE_EXTRACT_DIR" \
      && unzip -o -q "$SIMPLE_ARCHIVE" -d "$SIMPLE_EXTRACT_DIR"; then
      SIMPLE_DIR="$(find "$SIMPLE_EXTRACT_DIR" -maxdepth 1 -type d -name 'libsimple*' -print -quit)"
      if [ -n "$SIMPLE_DIR" ] && [ -d "$SIMPLE_DIR/dict" ] \
        && { [ -f "$SIMPLE_DIR/libsimple.dylib" ] || [ -f "$SIMPLE_DIR/libsimple.so" ]; }; then
        mkdir -p "$SIMPLE_LIB_DIR"
        cp "$SIMPLE_DIR"/libsimple.* "$SIMPLE_LIB_DIR"/
        cp -R "$SIMPLE_DIR/dict" "$SIMPLE_LIB_DIR"/
        chmod +x "$SIMPLE_LIB_DIR"/libsimple.* 2>/dev/null || true
        SIMPLE_OK=true
      fi
    fi
    trap - EXIT
    cleanup_simple
    if [ "$SIMPLE_OK" = true ]; then
      echo "simple: $(ls "$SIMPLE_LIB_DIR"/libsimple* 2>/dev/null)"
    else
      echo "simple: 下载或安装失败，回退 unicode61"
    fi
  else
    echo "simple: 平台不支持或无 curl，回退 unicode61"
  fi
else
  echo "simple: 已安装"
fi

echo "== 6/6 自检 =="
.venv/bin/python -m pytest -q 2>&1 | tail -1

echo
echo "可选外部依赖（按需安装，缺失时对应能力自动降级并显式告警）："
echo "  qmd      - 语义/向量检索（缺失 -> FTS5 降级）"
echo "  git lfs  - PDF/source 原件与 archive/raw 二进制快照必需；缺失时拒绝导入"
echo "  marker   - PDF/PPT/DOCX → 结构化 Markdown（已随 requirements 安装；模型 ~2-4GB 首次使用下载）"
echo "完成。日常入口：python -m tools.cli（查看命令列表）/ python -m tools.cli doctor"
