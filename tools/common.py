"""MyKnowledge 工具共享基础：hash、canonical JSON、原子写与稳定读。

无状态纯函数工具集，供 tools 包各模块经 ``python -m tools.cli`` 统一入口使用。
front matter 与 Vault 锁等有状态对象见 front_matter.py / vault_lock.py。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from pathlib import Path

SOURCE_TYPES = {"blog", "doc", "book", "contest", "pr", "local-file", "personal-note"}
ACQUISITIONS = {"fetch", "local-file", "personal-note"}
DOMAINS = {"computer-science", "multimedia", "reading-notes", "tools", "work-methods"}
SAFE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def canonical_json(value: object) -> bytes:
    """将 JSON 可序列化值编码为字节形式 canonical JSON（键排序、紧凑分隔符）。"""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    """计算字节内容的 sha256 摘要，返回带 ``sha256:`` 前缀的十六进制字符串。"""
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    """计算 UTF-8 编码文本的 sha256 摘要（带前缀），与 sha256_bytes 保持一致。"""
    return sha256_bytes(value.encode("utf-8"))


def hash_canonical(value: object) -> str:
    """canonical_json + sha256_bytes 的组合：规范化 JSON 的摘要（带前缀）。

    消除 ``sha256_bytes(canonical_json(x))`` 重复模式（operation/manifest/
    evidence hash 共用）。
    """
    return sha256_bytes(canonical_json(value))


def strip_sha256_prefix(value: str) -> str:
    """剥离摘要字符串的 ``sha256:`` 前缀返回裸 hex（无前缀时原样返回）。"""
    return value.removeprefix("sha256:")


def canonical_quote(value: str) -> str:
    """归一化引文文本：NFKC 兼容分解、全角标点映射与空白折叠。

    映射表对齐设计规范 §6.9 第 2 步：`，。；：？！（）【】「」“”‘’、`
    → 半角等价符号；步骤 4 删除零宽字符 U+200B/U+FEFF（F014，\\s 类不覆盖）；
    锚定工具与验证器必须共用本实现（AC-F001-013），不得另写副本。
    """
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u200b", "").replace("\ufeff", "")
    value = value.translate(
        str.maketrans(
            {
                "，": ",",
                "。": ".",
                "：": ":",
                "；": ";",
                "？": "?",
                "！": "!",
                "（": "(",
                "）": ")",
                "【": "[",
                "】": "]",
                "「": "[",
                "」": "]",
                "“": '"',
                "”": '"',
                "‘": "'",
                "’": "'",
                "、": ",",
            }
        )
    )
    return re.sub(r"\s+", " ", value).strip()


def canonical_body(body: str) -> str:
    """规范化正文（§6.6）：LF 统一、去行尾空白、折叠文件末尾空行为单个换行。

    只做这四步，不做其他改写（不动大小写、标点、列表重排）。与 canonical_quote
    同为契约级规范化原语（F007 发布 authority 计算 content hash 时复用）。
    """
    lines = [
        line.rstrip()
        for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("")
    return "\n".join(lines)


def safe_id(value: str) -> str:
    """校验字符串是否为合法 ID（小写字母数字与连字符），不合法时抛 ValueError。"""
    if not SAFE_ID.fullmatch(value):
        raise ValueError("invalid_id")
    return value


def redact(value: object) -> object:
    """递归脱敏敏感字段（authorization/cookie/token/password 等），用于写入审计。"""
    if isinstance(value, dict):
        hidden = {
            "authorization",
            "cookie",
            "set-cookie",
            "api_key",
            "token",
            "password",
        }
        return {
            k: ("[REDACTED]" if k.lower() in hidden else redact(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def crash_injection_point(point: str) -> None:
    """崩溃注入点（仅测试用）：MYKNOWLEDGE_CRASH_AFTER 匹配时 SIGKILL 自身。

    用于真实进程级崩溃恢复测试（tests/test_f001.py 崩溃注入用例）——子进程
    在 apply 的指定提交点被杀，父进程重放验证 WAL 恢复语义与 flock 锁的
    内核自动释放。生产环境无该环境变量时为零开销 no-op。
    """
    import os
    import signal

    if os.environ.get("MYKNOWLEDGE_CRASH_AFTER") == point:
        os.kill(os.getpid(), signal.SIGKILL)


def atomic_write(path: Path, data: bytes, mode: int | None = None) -> None:
    """原子写入文件：临时文件 + fsync + rename，可选权限位，并 fsync 父目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(tmp_name, mode)
        os.replace(tmp_name, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def read_stable(path: Path) -> tuple[bytes, os.stat_result]:
    """稳定读取文件：stat 前后比对 dev/ino/size/mtime，读取期间变化时抛 RuntimeError。

    文件缺失或无法访问时抛 OSError 子类（如 FileNotFoundError），由调用方按需处理。
    """
    before = path.stat()
    real = path.resolve(strict=True)
    with real.open("rb") as handle:
        data = handle.read()
    after = real.stat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ):
        raise RuntimeError("hash_mismatch")
    return data, after

def glob_without_symlinks(base: Path, pattern: str) -> list[Path]:
    """glob 但不穿透符号链接目录（C004：防越界读取仓库外文件）。

    Python 3.14 的 Path.glob 尚无 follow_symlinks 参数，故手动校验
    glob 结果的祖先链：任一中间目录为 symlink 即排除该命中。
    """
    results: list[Path] = []
    for hit in base.glob(pattern):
        try:
            rel = hit.relative_to(base)
        except ValueError:
            continue
        current = base
        safe = True
        for part in rel.parts[:-1]:
            current = current / part
            if current.is_symlink():
                safe = False
                break
        if safe:
            results.append(hit)
    return results
