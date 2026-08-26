"""Wiki 契约校验门面：validate 编排与 CLI（F002）。

对外 API 不变（``WikiValidator.validate(wiki_path) -> report``）；各层实现
（schema/rules/resolution/derived）在 tools/validation/ 包内解耦，本模块只做编排：
读取 → schema 层 → rules 层 → derived 层，resolution 沿调用链传递。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..common import canonical_body, sha256_text
from ..front_matter import FrontMatter
from ..paths import RepoPaths
from . import derived, rules, schema

__all__ = ["WikiValidator", "WIKI_SCHEMA_VERSION", "OWNER_VAULT_ID"]

WIKI_SCHEMA_VERSION = schema.WIKI_SCHEMA_VERSION
OWNER_VAULT_ID = schema.OWNER_VAULT_ID


class WikiValidator:
    """Wiki 契约校验器（owner Vault 上下文内只读校验，实例无状态）。"""

    def __init__(self, root: Path, *, quote_min_chars: int = 12) -> None:
        self.root = root
        self.paths = RepoPaths(root)
        # 钳制下限（R011）：负值/0 会静默禁用 §6.9 引文长度门槛（fail-open）
        self.quote_min_chars = max(1, quote_min_chars)
        self._schema = schema.load_schema()

    def validate(self, wiki_path: Path) -> dict:
        """校验单个 Wiki 文件，返回确定性校验报告（不修改任何文件）。"""
        try:
            text = wiki_path.read_text(encoding="utf-8")
            metadata, body = FrontMatter.parse(text)
        except (OSError, UnicodeError):
            return self._report(
                wiki_path,
                errors=[{"code": "path_unresolved", "path": str(wiki_path)}],
            )
        except (ValueError, TypeError) as exc:
            return self._report(
                wiki_path,
                errors=[{"code": "front_matter_invalid", "path": str(wiki_path),
                         "reason": str(exc)}],
            )
        errors: list[dict] = []
        warnings: list[dict] = []

        # 1. 手写派生字段（先于 schema，独立错误码，fail-closed）
        errors.extend(schema.check_derived_fields(metadata))

        # 2. schema version（AC-F002-007：错误 version 拒绝）
        schema_version = metadata.get("schema_version")
        if schema_version is not None and schema_version != WIKI_SCHEMA_VERSION:
            errors.append(
                {
                    "code": "wrong_schema_version",
                    "path": "schema_version",
                    "reason": str(schema_version),
                }
            )

        # 3. 可执行 JSON Schema（未知字段/类型/枚举/必填）
        errors.extend(schema.check_schema(metadata, self._schema))

        # 4. domain rule layer（结构合法后才运行，避免下游 KeyError）；
        #    jsonschema 不可用同样阻断（R005：fail-closed）
        structural_blocked = any(
            e["code"]
            in {
                "schema_invalid",
                "unknown_field",
                "wrong_schema_version",
                "validator_unavailable",
            }
            for e in errors
        )
        resolution: dict = {}
        if not structural_blocked:
            domain_errors, domain_warnings, resolution = rules.domain_rules(
                metadata, body, self.paths, self.quote_min_chars
            )
            errors.extend(domain_errors)
            warnings.extend(domain_warnings)

        report = self._report(wiki_path, errors=errors, warnings=warnings)
        report["object_ref"]["object_id"] = metadata.get("id")
        if not report["valid"]:
            return report

        # 5. 派生字段与 hash（仅结构/规则全部通过时计算）
        hashes = {
            "content_sha256": sha256_text(canonical_body(body)),
            "evidence_sha256": derived.evidence_sha256(metadata, resolution),
        }
        # 验证报告只读取一次（F016）：hash 绑定校验（F003）与派生计算共用同一份
        validation_report = derived.load_validation_report(
            str(metadata.get("id", "")), hashes, self.paths
        )
        report["derived"] = derived.compute_derived(
            metadata, body, resolution, validation_report, hashes, self.paths
        )
        report["hashes"] = hashes
        report["validation_report"] = validation_report
        # F003：确定性 resolution（resolved_targets/sources/provenance）对审计层可见
        report["resolution"] = resolution
        return report

    def _report(
        self,
        wiki_path: Path,
        *,
        errors: list[dict],
        warnings: list[dict] | None = None,
    ) -> dict:
        return {
            "schema_version": WIKI_SCHEMA_VERSION,
            "validator": "wiki-validator",
            "object_ref": {"vault_id": OWNER_VAULT_ID, "object_type": "wiki",
                           "object_id": None},
            "valid": not errors,
            "errors": errors,
            "warnings": warnings or [],
            "derived": None,
            "hashes": None,
            "validation_report": None,
            "resolution": None,
        }


def main(argv: list[str] | None = None) -> int:
    """wiki validate CLI：对单个 Wiki 文件执行确定性校验并输出报告。"""
    parser = argparse.ArgumentParser(
        description="Deterministic validation of a Wiki canonical file"
    )
    parser.add_argument("wiki", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--min-chars", type=int, default=12)
    args = parser.parse_args(argv)
    report = WikiValidator(args.root, quote_min_chars=args.min_chars).validate(
        args.wiki
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 2
