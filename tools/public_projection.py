"""Generate the public projection from validated public Wiki objects (F007)."""

from __future__ import annotations

import json
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any

from .common import atomic_write, canonical_json, hash_canonical
from .front_matter import FrontMatter
from .paths import RepoPaths
from .policy import policy_value
from .release_confirmation import validate_event
from .release_input import compute as compute_release_input
from .release_input import lineage_commitment
from .validation.validator import WikiValidator

# 默认必须**全部**比对（与 policy.yaml 的 release.public_release_authority 声明同集合）。
# 默认值放在代码里而不是"policy 缺失就为空"：否则没有 policy.yaml 的 checkout 会把
# 发布门禁降级成只比对正文与证据——这正是 fail-open。policy 只能覆盖，不能取消。
REQUIRED_MATCH_FIELDS = (
    "release_input_sha256",
    "reviewed_content_sha256",
    "reviewed_evidence_sha256",
    "leak_gate_report_sha256",
    "target_ref",
    "operation_id",
    "confirmation_nonce",
)


class PublicProjectionGenerator:
    """Public-only manifest generator with an explicit allowlist boundary."""

    def __init__(self, root: Path, validator: Any | None = None) -> None:
        self.root = Path(root).resolve()
        self.paths = RepoPaths(self.root)
        self.validator = validator or WikiValidator(self.root, vault_id="public")

    def _release_input_sha256(
        self, item: dict, content_sha256: str, operation_id: str
    ) -> str:
        """候选条目在指定 lineage 下的 `release_input_sha256`（供确认比对复用）。"""
        return compute_release_input(
            self.root,
            item=item,
            content_sha256=content_sha256,
            operation_id=operation_id,
        )[0]

    def _confirmation(
        self,
        object_id: str,
        content_hash: str,
        evidence_hash: str,
        release_input: Callable[[str], str],
    ) -> tuple[dict | None, str | None]:
        """按 `release.public_release_authority.required_match_fields` 全项比对。

        实测（2026-09-01）：此前只比对 content/evidence 两项，声明的 7 项里
        `release_input_sha256`、`leak_gate_report_sha256`、`operation_id`、
        `confirmation_nonce` 从未校验——人工批准因此不覆盖 route/body_path/
        attachments/links，改动后页面仍以"已批准"发布。
        """
        directory = self.paths.release_confirmations
        if not directory.is_dir():
            return None, "confirmation_missing"
        required = set(
            policy_value(
                self.root,
                "release",
                "public_release_authority",
                "required_match_fields",
                default=REQUIRED_MATCH_FIELDS,
            )
            or REQUIRED_MATCH_FIELDS
        )
        reason = "confirmation_mismatch"
        for path in sorted(directory.glob("*.json"), reverse=True):
            try:
                event = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            result = validate_event(event)
            ref = event.get("target_ref") or {}
            if not result.get("valid") or ref.get("object_id") != object_id:
                continue
            if (
                event.get("reviewed_content_sha256") != content_hash
                or event.get("reviewed_evidence_sha256") != evidence_hash
            ):
                continue
            operation_id = str(event.get("operation_id") or "")
            if "operation_id" in required and not self._lineage_record_exists(
                operation_id
            ):
                # missing_record_behavior: derive-false-and-block-publish
                reason = "lineage_record_missing"
                continue
            if "release_input_sha256" in required and event.get(
                "release_input_sha256"
            ) != release_input(operation_id):
                reason = "release_input_mismatch"
                continue
            if "leak_gate_report_sha256" in required and not event.get(
                "leak_gate_report_sha256"
            ):
                reason = "leak_gate_report_missing"
                continue
            if "confirmation_nonce" in required and not event.get("confirmation_nonce"):
                reason = "confirmation_nonce_missing"
                continue
            return {
                "event": event,
                "path": str(path.relative_to(self.root)),
                "event_sha256": result["event_sha256"],
            }, None
        return None, reason

    def _lineage_record_exists(self, operation_id: str) -> bool:
        """§6.8：只有匹配的人工事件**且**存在 owner durable operation record 才放行。"""
        if not operation_id:
            return False
        try:
            return self.paths.operation_file(operation_id).is_file()
        except (OSError, ValueError):
            return False

    def _item(
        self,
        object_id: str,
        relative: str,
        metadata: dict,
        derived: dict,
        hashes: dict,
        links: Any,
    ) -> dict[str, Any]:
        """按 `public_projection.required_item_fields` 构造条目（确认相关字段稍后补）。

        此前 manifest 只写 15 个键，声明的 28 个必填字段缺 11 个——其中 `strength`
        是 §6.7 要求"必须同时出现在页面、查询结果和 Agent 输出契约"的证据强度标识，
        而 `public_metadata` 又是 release_input 的输入，因此缺字段会连带让签名失真。
        """
        return {
            "id": object_id,
            "object_type": "wiki",
            "vault_id": "public",
            "title": metadata.get("title", object_id),
            "domain": metadata.get("domain"),
            "kind": metadata.get("kind"),
            "strength": derived.get("strength"),
            "route": "/wiki/" + object_id,
            "body_path": relative,
            "attachments": [],
            "status": "published",
            "publication_scope": metadata.get("publication_scope"),
            "public_publishable": True,
            "public_release": True,
            "public_lineage_commitment": None,
            "effective_confidentiality": derived.get(
                "effective_confidentiality", "public"
            ),
            "validation_state": derived.get("validation_state"),
            "evidence_state": derived.get("evidence_state"),
            "links": links if isinstance(links, list) else [],
            "content_sha256": hashes.get("content_sha256"),
            "evidence_sha256": hashes.get("evidence_sha256"),
        }

    def release_candidate(
        self, object_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """待发布条目的确定性材料（供 `release input/confirm` 与 projection 共用）。

        签名命令必须拿到与 projection 逐字一致的 item，否则算出来的
        `release_input_sha256` 永远配不上——这正是"两处各算一份必然漂移"的地方。
        """
        wiki_root = self.paths.wiki_root
        paths = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
        for path in paths:
            if path.is_symlink() or not path.is_file():
                continue
            try:
                report = self.validator.validate(path)
            except (OSError, UnicodeError, ValueError):
                continue
            current = str(
                (report.get("object_ref") or {}).get("object_id") or path.stem
            )
            if current != object_id:
                continue
            derived = report.get("derived") or {}
            hashes = report.get("hashes") or {}
            if not report.get("valid") or not derived.get("public_release_ready"):
                # 判据用 public_release_ready 而不是 public_publishable：待审材料
                # 必须能在发布确认签署**之前**算出来，否则链路自锁（见 derived
                # 的 public_release_ready 注释）。真正的发布门禁在 projection
                # 侧独立校验确认事件与 7 项 hash，不因此放宽。
                return None, "not_public_publishable"
            metadata: dict = {}
            try:
                metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                metadata = {}
            links = metadata.get("related", []) if isinstance(metadata, dict) else []
            return {
                "item": self._item(
                    object_id,
                    str(path.relative_to(self.root)),
                    metadata,
                    derived,
                    hashes,
                    links,
                ),
                "content_sha256": hashes.get("content_sha256"),
                "evidence_sha256": hashes.get("evidence_sha256"),
            }, None
        return None, "object_not_found"

    def generate(self, output: Path | None = None) -> dict[str, Any]:
        output = (
            Path(output)
            if output is not None
            else self.paths.queries_public / "manifest.json"
        )
        if not output.is_absolute():
            output = self.root / output
        items: list[dict[str, Any]] = []
        skipped: list[dict[str, str]] = []
        wiki_root = self.paths.wiki_root
        paths = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
        for path in paths:
            if path.is_symlink() or not path.is_file():
                continue
            try:
                report = self.validator.validate(path)
            except (OSError, UnicodeError, ValueError) as exc:
                # 读文件/front matter 层面的失败是对象级阻断；validator 自身的
                # 编程错误不在此吞掉，否则未发布会被伪装成"跳过一篇"
                skipped.append(
                    {
                        "path": str(path.relative_to(self.root)),
                        "reason": type(exc).__name__,
                    }
                )
                continue
            object_id = str(
                (report.get("object_ref") or {}).get("object_id") or path.stem
            )
            derived = report.get("derived") or {}
            hashes = report.get("hashes") or {}
            if not report.get("valid") or not derived.get("public_publishable"):
                skipped.append(
                    {"object_id": object_id, "reason": "not_public_publishable"}
                )
                continue
            relative = str(path.relative_to(self.root))
            metadata = {}
            try:
                metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                metadata = {}
            links = metadata.get("related", []) if isinstance(metadata, dict) else []
            candidate = self._item(
                object_id, relative, metadata, derived, hashes, links
            )
            confirmation, reason = self._confirmation(
                object_id,
                hashes.get("content_sha256"),
                hashes.get("evidence_sha256"),
                partial(
                    self._release_input_sha256, candidate, hashes.get("content_sha256")
                ),
            )
            if confirmation is None:
                skipped.append(
                    {"object_id": object_id, "reason": reason or "confirmation_missing"}
                )
                continue
            event = confirmation["event"]
            items.append(
                {
                    **candidate,
                    "public_lineage_commitment": lineage_commitment(
                        self.root, str(event.get("operation_id") or "")
                    ),
                    "release_input_sha256": event.get("release_input_sha256"),
                    "leak_gate_report_sha256": event.get("leak_gate_report_sha256"),
                    "leak_gate_report_scope": event.get("leak_gate_report_scope"),
                    "public_confirmation_path": confirmation["path"],
                    "public_confirmation_sha256": confirmation["event_sha256"],
                }
            )
        items.sort(key=lambda item: item["id"])
        manifest = {
            "schema_version": "public-projection/v1",
            "projection": "public",
            "generated_from": hash_canonical(items),
            "items": items,
        }
        atomic_write(output, canonical_json(manifest) + b"\n", 0o600)
        return {
            "state": "generated",
            "path": str(output.relative_to(self.root))
            if output.is_relative_to(self.root)
            else str(output),
            "item_count": len(items),
            "skipped": skipped,
            "manifest_sha256": hash_canonical(manifest),
        }
