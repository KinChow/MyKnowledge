"""Public projection 单一加载入口（结构收敛 Step0-1）。

此前同一份 ``queries/public/manifest.json`` 有两份平行实现：
``backend.app._load_public_projection``（宽松：不校验 ``public_release``，
不加载 body）与 ``tools.skill_runtime._public_projection_items``（严格）。
两份语义不一致本身就是泄露面差异；宽松版还导致 API 的 fallback 检索
只能匹配 title（manifest items 不含 body）。

本模块收敛为一个实现：
- 允许列表条件复用原 ``indexing._public_allowlisted`` 的完整谓词
  （vault_id/public_publishable/public_release/status/confidentiality），
  ``indexing`` 反向复用本模块，保证过滤条件单份；
- ``with_body=True`` 时执行 body path 防穿越与 symlink 拒绝，并读取
  正文（语义与原 skill_runtime 实现逐字一致，错误码不变）；
- manifest 缺失/非法时抛 ``ValueError("manifest_invalid")``，由调用方
  决定 fail-closed 形态（API 启动降级为空检索 = F006 离线设计）。

来源说明：借鉴 Django Settings/Manager 的"单事实源加载器"模式
（https://docs.djangoproject.com/en/stable/topics/settings/），
不引入第三方依赖。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import RepoPaths

SCHEMA_VERSION = "public-projection/v1"


def public_allowlisted(item: dict) -> bool:
    """Require the complete public projection allowlist, not one derived flag."""
    return (
        item.get("vault_id") == "public"
        and item.get("public_publishable") is True
        and item.get("public_release") is True
        and item.get("status") == "published"
        and item.get("effective_confidentiality", item.get("confidentiality", "public"))
        == "public"
    )


class PublicProjectionStore:
    """Read-only accessor for the validated public projection manifest."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()

    def manifest_path(self) -> Path:
        return RepoPaths(self.root).queries_public / "manifest.json"

    def load_manifest(self) -> dict[str, Any]:
        """Parse and schema-check the manifest; raise ValueError when invalid."""
        try:
            data = json.loads(self.manifest_path().read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError("manifest_invalid") from exc
        if (
            not isinstance(data, dict)
            or data.get("schema_version") != SCHEMA_VERSION
            or data.get("projection") != "public"
            or not isinstance(data.get("items"), list)
            or any(not isinstance(item, dict) for item in data["items"])
        ):
            raise ValueError("manifest_invalid")
        return data

    def public_items(self, *, with_body: bool = False) -> list[dict[str, Any]]:
        """Strictly allowlisted items; optionally load bodies (safe path join)."""
        items = [
            item for item in self.load_manifest()["items"] if public_allowlisted(item)
        ]
        if not with_body:
            return items
        loaded: list[dict[str, Any]] = []
        for item in items:
            rel = Path(str(item.get("body_path", "")))
            if (
                rel.is_absolute()
                or ".." in rel.parts
                or not rel.parts
                or rel.parts[0] != "wiki"
            ):
                raise ValueError("projection_path_invalid")
            body_path = self.root / rel
            if not body_path.is_file() or body_path.is_symlink():
                raise ValueError("projection_body_unavailable")
            loaded.append(
                {
                    **item,
                    "object_type": "wiki",
                    "object_id": item["id"],
                    "body": body_path.read_text(encoding="utf-8"),
                    "availability": "available",
                    "confidentiality": "public",
                }
            )
        return loaded

    def degraded_items(self) -> list[dict[str, Any]]:
        """Offline-tolerant variant: invalid/missing manifest yields no items.

        仅供 F006 API 启动路径使用（离线降级为空检索是设计行为）；
        CLI/Skill 等需要显式失败的入口必须直接使用 :meth:`public_items`。
        """
        try:
            return self.public_items(with_body=True)
        except (OSError, ValueError):
            return []
