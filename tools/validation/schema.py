"""Wiki schema 层：可执行 JSON Schema 的加载与执行（F002 AC-F002-007）。

来源：jsonschema 库（https://github.com/python-jsonschema/jsonschema，MIT）
与 config/schemas.yaml registry 分离：本层执行 config/json-schema/wiki-v1.json，
拒绝未知字段、错误 schema version 与手写派生字段；错误为
{"code", "path", "reason"} 结构（字段级、可重放）。
"""

from __future__ import annotations

import json
from pathlib import Path

WIKI_SCHEMA_VERSION = "wiki/v1"
# owner Vault（F002 单 vault 阶段；F011 挂载 private vault 前恒为 public）
OWNER_VAULT_ID = "public"

# 派生/运行字段：作者手写一律拒绝（§6.8 声明/派生/operation-controlled 分组）
FORBIDDEN_DERIVED_FIELDS = frozenset(
    {
        "vault_id",
        "evidence_state",
        "validation_state",
        "effective_confidentiality",
        "strength",
        "private_publishable",
        "public_publishable",
        "public_release",
        "public_confirmation_sha256",
        "publication_warning",
        "validation_attestation_ref",
        "semantic_sha256",  # 设计 §6.6 已废弃该字段，手写一律拒绝（fail-closed）
        "content_sha256",
        "evidence_sha256",
        "availability",
        "availability_reason",
    }
)


def load_schema() -> dict:
    """加载可执行 JSON Schema（代码资源，随包路径解析，与数据根 --root 解耦）。"""
    path = (
        Path(__file__).resolve().parent.parent.parent
        / "config"
        / "json-schema"
        / "wiki-v1.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def check_derived_fields(metadata: dict) -> list[dict]:
    """拒绝手写派生字段（先于 schema，独立错误码，fail-closed）。"""
    return [
        {"code": "derived_field_mismatch", "path": field}
        for field in sorted(FORBIDDEN_DERIVED_FIELDS & metadata.keys())
    ]


def check_schema(metadata: dict, schema: dict) -> list[dict]:
    """用 wiki-v1.json 执行结构校验，映射 jsonschema 错误为字段级错误。"""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return [{"code": "validator_unavailable", "path": "_schema"}]
    validator = Draft202012Validator(schema)
    errors: list[dict] = []
    for error in sorted(
        validator.iter_errors(metadata), key=lambda e: list(e.path)
    ):
        if error.validator == "additionalProperties":
            errors.append(
                {
                    "code": "unknown_field",
                    "path": ".".join(str(p) for p in error.path)
                    or error.message,
                    "reason": error.message,
                }
            )
        else:
            errors.append(
                {
                    "code": "schema_invalid",
                    "path": ".".join(str(p) for p in error.path) or error.validator,
                    "keyword": error.validator,
                    "reason": error.message,
                }
            )
    return errors
