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
import uuid
from pathlib import Path
from typing import Any

import yaml

SOURCE_TYPES = {"blog", "doc", "book", "contest", "pr", "local-file", "personal-note"}
ACQUISITIONS = {"fetch", "local-file", "personal-note"}
DOMAINS = {"computer-science", "multimedia", "reading-notes", "tools", "work-methods"}
SAFE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OPERATION_ID = re.compile(r"^op[-_][a-z0-9][a-z0-9-]{0,62}$")


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


def new_operation_id() -> str:
    """生成 operation_id（唯一生成端口径：``op_<32位hex>``）。"""
    return "op_" + uuid.uuid4().hex


def safe_operation_id(value: str) -> str:
    """校验 operation_id（唯一校验端口径），不合法时抛 ValueError。

    与 ``safe_id`` 分开是因为生产形态 ``op_<hex>`` 含下划线，``safe_id`` 会
    直接拒掉——每个调用点各自 ``removeprefix("op_")`` 后再 ``safe_id`` 的写法
    曾让 ``release confirm`` 对**每一个**真实 operation 都返回 event_id_invalid。

    校验只约束"前缀 + 安全字符集 + 长度上限"，不复刻生成端的 32 位 hex：
    operation_id 会成为 ``audit/operations/<id>.json`` 的文件名，校验要挡的是
    路径穿越与文件名注入；把校验收紧到生成端格式只会再制造一次"合法 ID 被拒"。
    """
    if not OPERATION_ID.fullmatch(value):
        raise ValueError("invalid_operation_id")
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


def injection_point(point: str) -> None:
    """命名故障注入点（仅测试用）：按环境变量在指定提交点触发一种动作。

    设计照搬 FreeBSD fail(9)（https://man.freebsd.org/cgi/man.cgi?query=fail）
    的"命名点 + 运行期选择动作"模型，激活方式取自 etcd/gofail 的环境变量开关
    （GOFAIL_FAILPOINTS，https://github.com/etcd-io/gofail，Apache-2.0）：

    - ``MYKNOWLEDGE_CRASH_AFTER=<point>``：SIGKILL 自身（fail(9) 的 panic 动作）
      ——验证进程级崩溃后的 WAL 重放与 flock 内核自动释放。
    - ``MYKNOWLEDGE_FAIL_AT=<point>``：抛 OSError（fail(9) 的 return 动作）
      ——验证进程存活时的 I/O 失败回滚路径，这条路走的是 except OSError，
      与 SIGKILL 是两类完全不同的失败，必须分别覆盖。

    刻意不移植 fail(9)/gofail 的概率、次数、级联与 HTTP 激活端点：单元测试要
    的是确定性触发，那些机制服务于长跑服务的随机故障注入。
    生产环境无这两个环境变量时为零开销 no-op。
    """
    import os
    import signal

    if os.environ.get("MYKNOWLEDGE_CRASH_AFTER") == point:
        os.kill(os.getpid(), signal.SIGKILL)
    if os.environ.get("MYKNOWLEDGE_FAIL_AT") == point:
        raise OSError(f"injected_io_error:{point}")


def load_config_yaml(path: Path, error_code: str) -> dict[str, Any]:
    """读取一份 config YAML：缺失返回 {}，损坏抛 ValueError(error_code)。

    `config/policy.yaml` 与 `config/schemas.yaml` 的加载语义完全相同
    （缺失=合法空覆盖层、损坏=结构化阻断不静默降级），收敛为一处，
    避免两个模块各写一份 `safe_load` 逐步漂移。
    """
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(error_code) from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(error_code)
    return data


def config_value(document: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """按键路径从配置映射取值；中途非映射节点或缺失返回 default。"""
    node: Any = document
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


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


def safe_relative_path(value: str) -> str:
    """append-only 记录里写下的相对路径的唯一校验口径（C004）。

    记录本身不可改写，但它是**外部可改写的输入**：`archive_path` 写成
    `../../etc/passwd` 或 `/etc/passwd` 时，按记录原样拼路径就会读到仓库外的文件。
    因此在拼接之前先归一并拒绝：绝对路径、Windows 盘符、`..` 段、空串。

    返回归一化后的 POSIX 相对路径；非法输入抛 `ValueError("unsafe_record_path")`，
    由调用侧映射成结构化错误码——不静默当成"文件不存在"，那会把一次越界尝试
    伪装成一条正常的缺失账目。
    """
    text = str(value).replace("\\", "/").strip()
    if not text or text.startswith("/") or ":" in text.split("/")[0]:
        raise ValueError("unsafe_record_path")
    parts = [seg for seg in text.split("/") if seg not in ("", ".")]
    if not parts or any(seg == ".." for seg in parts):
        raise ValueError("unsafe_record_path")
    return "/".join(parts)


def is_contained_regular_file(base: Path, candidate: Path) -> bool:
    """candidate 是否为 base 内的普通文件（符号链接必须解析后仍落在 base 内）。

    与 `glob_without_symlinks` 同一条控制（C004），但判据不同：那里是遍历，广度
    未知，只能一律不穿透；这里是一条已知路径，真正的威胁是**逃出仓库**而不是
    "用了符号链接"。把 archive 目录 symlink 到外挂盘是合理布局，一律禁会让全部
    快照报缺失——那是门禁过严，且给出的原因还是错的。
    """
    try:
        base_real = base.resolve(strict=False)
        target = candidate.resolve(strict=False)
    except OSError:
        return False
    if target != base_real and base_real not in target.parents:
        return False
    return target.is_file()


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
