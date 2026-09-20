"""统一 Source 创建契约 → `SourceIngestor` 内部请求的归一化。

设计对齐成熟方案：**locator = URI**（仿 ``fsspec``/``smart_open`` 与 Apache Nutch 的
scheme 分派，``file://`` 本地 / ``http(s)://`` 远程 / ``data:`` 内联），**kind = 语义类别**
（仿 Apache Tika / LangChain Loader 的"格式/读取器"轴，保留既有 ``source_type`` 语义，
SRC-002 只加不改名）。归一化只重排入参，产出的**内部请求形状不变**，交给既有
``SourceIngestor.ingest``——快照/归档/哈希口径完全不变（可回滚、SRC-002 安全）。

统一契约字段：``{locator?, content?, kind?, domain, source_id?, options?}``
- ``locator``：外部来源 URI；``content``：内联正文（personal-note），二者取其一。
- ``allowed_schemes`` 是**按入口的安全门禁**：不含 ``file`` 时，``file://`` 与任何
  携带 ``input_path`` 的（legacy）请求一律拒绝——堵住 agent/HTTP 读本地盘。
"""

from __future__ import annotations

from typing import Any
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

# 语义类别（走远程抓取）——对应既有 SOURCE_TYPES 里的语义值（SRC-002）。
_FETCH_KINDS = {"blog", "doc", "book", "contest", "pr"}
# 归一化认识的 URI scheme。
_KNOWN_SCHEMES = {"http", "https", "file", "data"}
# 统一创建契约的合法顶层字段（见 content-crud-repository.md §12）；其余一律拒，
# 不接受"被接受但被忽略"的入参（与 backend/schemas.py 的 extra=forbid 一致）。
_UNIFIED_KEYS = {"locator", "content", "kind", "domain", "source_id", "options"}


class LocatorError(ValueError):
    """归一化失败；``code ∈ {locator_invalid, locator_scheme_not_allowed}``（已登记词表）。"""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _is_unified(request: dict) -> bool:
    """统一契约：带 locator/content/kind 之一；否则视为既有内部 request。"""
    return any(key in request for key in ("locator", "content", "kind"))


def _reject_unknown_unified_keys(request: dict) -> None:
    """统一契约下拒绝未知顶层字段（拼错的 domain、错放顶层的 media_type 等）。

    否则会被静默忽略、悄悄退化成 doc/None domain。附加参数应放进 ``options``。
    """
    if set(request) - _UNIFIED_KEYS:
        raise LocatorError("locator_invalid")


def normalize_source_request(
    request: dict, *, allowed_schemes: set[str] | None = None
) -> dict:
    """统一契约 → 内部 request；非统一（含 source_type）按 file 门禁后原样返回。

    ``allowed_schemes=None`` 表示不限制（受信编程入口，如 registry 直调）。
    """
    file_allowed = allowed_schemes is None or "file" in allowed_schemes

    if not _is_unified(request):
        if not file_allowed and (
            request.get("input_path") or request.get("source_type") == "local-file"
        ):
            raise LocatorError("locator_scheme_not_allowed")
        return request

    _reject_unknown_unified_keys(request)
    base: dict[str, Any] = {"domain": request.get("domain")}
    if request.get("source_id"):
        base["source_id"] = request["source_id"]
    kind = request.get("kind")
    options = dict(request.get("options") or {})
    content = request.get("content")
    locator = request.get("locator")

    # 内联正文（无 locator）→ personal-note
    if content is not None and not locator:
        return {
            **base,
            "source_type": "personal-note",
            "origin": "personal",
            "body": str(content),
            **options,
        }

    if not isinstance(locator, str) or not locator:
        raise LocatorError("locator_invalid")
    scheme = (urlparse(locator).scheme or "").lower()
    if scheme not in _KNOWN_SCHEMES:
        raise LocatorError("locator_invalid")
    if allowed_schemes is not None and scheme not in allowed_schemes:
        raise LocatorError("locator_scheme_not_allowed")

    if scheme == "data":
        # data:[<mediatype>][;base64],<data> —— 仅取文本内联（personal-note）
        after = locator[len("data:") :]
        text = unquote(after.split(",", 1)[1]) if "," in after else ""
        return {
            **base,
            "source_type": "personal-note",
            "origin": "personal",
            "body": text,
            **options,
        }

    if scheme == "file":
        path = url2pathname(urlparse(locator).path)
        if kind == "video-transcript":
            return {**base, "source_type": "video", "transcript_path": path, **options}
        return {**base, "source_type": "local-file", "input_path": path, **options}

    # http / https
    if kind == "video-transcript":
        return {**base, "source_type": "video", "url": locator, **options}
    source_type = kind if kind in _FETCH_KINDS else "doc"
    return {**base, "source_type": source_type, "url": locator, **options}
