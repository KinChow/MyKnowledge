"""config 声明的路径与 `RepoPaths` 实际派生路径的一致性门禁（LAY-001）。

为什么保留两份而不是消除冗余：`config/*.yaml` 里的路径是给人 review 的**规范
声明**，`tools/paths.py` 是代码执行的**事实**。两份独立事实互证比一份"唯一真相"
更可靠——唯一真相写错了没有任何人会发现。本模块把"两处漂移"从事故降级为门禁报错。

实测动机（2026-09-01 owner review）：批次 1 把 `state/` 迁到 `var/state/` 时，
`capability_token.storage_path` 跟着改了，同一段里的 `parent_directory` 没改；
`tools/indexing.py` 的 root 反推也漏改并且**算出了错的 root 而不报错**。批次 3
（`archive|audit|release` → `ledger/`）要手工改 config 十余处，漏一处同样无人发现。

表是**显式**的，不从 config 正则扫路径：`field_contracts.operation.required_fields`
里的 `state` 是字段名、`audit.record_types` 里的 `release` 是记录类型名，扫出来
只会是噪声。占位符段（`<event_id>` 等）不参与比对——比对的是目录前缀。
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from .paths import RepoPaths

# (来源文件, 键路径, 期望目录的派生方式)。用于**单值**声明。
Rule = tuple[str, tuple[str, ...], Callable[[RepoPaths], Path]]

# 列表型声明（allowlist / roots 清单）只做**成员判定**，不绑下标。
# owner review（2026-09-01）问"门禁会不会太严"——绑下标就是过严的一例：
# 调换 YAML 列表顺序在语义上什么都没变，却会报漂移。允许列表变长（allowlist
# 本来会增长），但声明里必须仍包含代码实际使用的那个路径。
MemberRule = tuple[str, tuple[str, ...], Callable[[RepoPaths], Path]]

MEMBER_RULES: tuple[MemberRule, ...] = (
    ("policy", ("layers", "vault_content_roots"), lambda p: p.sources_root),
    ("policy", ("layers", "vault_content_roots"), lambda p: p.wiki_root),
    ("policy", ("layers", "vault_store_roots"), lambda p: p.archive_root),
    ("policy", ("layers", "vault_store_roots"), lambda p: p.audit_root),
    ("policy", ("layers", "vault_store_roots"), lambda p: p.release_root),
    ("policy", ("layers", "derived_roots"), lambda p: p.queries_root),
    ("policy", ("layers", "derived_roots"), lambda p: p.state_root),
    ("policy", ("layers", "derived_roots"), lambda p: p.reports_root),
    ("policy", ("layers", "unmanaged_paths"), lambda p: p.working_root),
    ("policy", ("layers", "unmanaged_paths"), lambda p: p.journal_root),
    ("policy", ("layers", "unmanaged_paths"), lambda p: p.decisions_root),
    ("policy", ("projection", "body_path_prefixes"), lambda p: p.queries_public),
    ("policy", ("projection", "body_path_prefixes"), lambda p: p.wiki_root),
    ("policy", ("projection", "attachment_path_prefixes"), lambda p: p.queries_public),
    ("policy", ("projection", "attachment_path_prefixes"), lambda p: p.wiki_root),
)

RULES: tuple[Rule, ...] = (
    # ---- policy.yaml ----
    (
        "policy",
        ("paths", "local_source_sidecar"),
        lambda p: p.state_local_sources("_").parent,
    ),
    ("policy", ("layers", "journal", "path_pattern"), lambda p: p.journal_root),
    (
        "policy",
        ("security", "local_api", "capability_token", "path"),
        lambda p: p.capability_token,
    ),
    (
        "policy",
        ("security", "local_api", "capability_token", "parent_directory"),
        lambda p: p.state_root,
    ),
    (
        "policy",
        ("release", "public_confirmation_path"),
        lambda p: p.release_confirmations,
    ),
    ("policy", ("release", "durable_audit_path"), lambda p: p.audit_root),
    (
        "policy",
        ("release", "public_release_authority", "confirmation_event_path"),
        lambda p: p.release_confirmations,
    ),
    (
        "policy",
        ("release", "public_release_authority", "target_operation_path"),
        lambda p: p.audit_operations,
    ),
    ("policy", ("backup", "durable_manifest_path"), lambda p: p.audit_backup),
    (
        "policy",
        ("projection", "public_confirmation_path_prefix"),
        lambda p: p.release_confirmations,
    ),
    ("policy", ("build", "release_lock_path"), lambda p: p.release_lock),
    # ---- schemas.yaml ----
    (
        "schemas",
        ("field_contracts", "capability_token", "storage_path"),
        lambda p: p.capability_token,
    ),
    (
        "schemas",
        ("field_contracts", "capability_token", "parent_directory"),
        lambda p: p.state_root,
    ),
    (
        "schemas",
        ("field_contracts", "backup_manifest", "durable_path"),
        lambda p: p.audit_backup,
    ),
    (
        "schemas",
        ("validation", "override", "durable_path"),
        lambda p: p.audit_validation("wiki", "_").parent,
    ),
    (
        "schemas",
        ("public_release_authority", "authoritative_records", "confirmation_event"),
        lambda p: p.release_confirmations,
    ),
    (
        "schemas",
        ("public_release_authority", "authoritative_records", "target_operation"),
        lambda p: p.audit_operations,
    ),
    ("schemas", ("backup", "durable_manifest_path"), lambda p: p.audit_backup),
    ("schemas", ("durable_records", "operation_path"), lambda p: p.audit_operations),
    (
        "schemas",
        ("durable_records", "validation_path"),
        lambda p: p.audit_root / "validation",
    ),
    (
        "schemas",
        ("durable_records", "public_confirmation_path"),
        lambda p: p.release_confirmations,
    ),
    ("schemas", ("durable_records", "backup_manifest_path"), lambda p: p.audit_backup),
)


def declared_directory(value: str) -> str:
    """把声明值归一成"目录前缀"：去掉占位符段与文件名、去掉首尾斜杠。

    `audit/operations/<operation_id>.json` → `audit/operations`
    `content/journal/<YYYY>/<MM>/`         → `content/journal`
    `var/state/capability-token`           → 原样（无占位符时不猜哪段是文件名）
    """
    text = str(value).strip().replace("\\", "/").strip("/")
    parts: list[str] = []
    for segment in text.split("/"):
        if segment.startswith("<"):
            break
        parts.append(segment)
    if parts and parts[-1].startswith("<"):
        parts.pop()
    return "/".join(parts)


def _dig(node: object, keys: tuple[str | int, ...]) -> object:
    """按键路径取值；缺失或类型不符时返回 `_MISSING`（不抛异常、不静默给默认值）。"""
    current = node
    for key in keys:
        if isinstance(key, int):
            if not isinstance(current, list) or not -len(current) <= key < len(current):
                return _MISSING
            current = current[key]
        else:
            if not isinstance(current, dict) or key not in current:
                return _MISSING
            current = current[key]
    return current


_MISSING = object()


def _check_value_rules(
    paths: RepoPaths, documents: dict[str, dict]
) -> tuple[list[dict], int, int]:
    """比对单值声明（等值判定）：声明段与代码派生目录必须逐字一致。"""
    drifted: list[dict] = []
    checked = 0
    skipped = 0
    for source, keys, derive in RULES:
        if source not in documents:
            continue
        key_text = f"{source}:" + ".".join(str(k) for k in keys)
        # 整段缺失（例如临时树只写了 `layers.working`）不算漂移：那时代码走
        # `policy_value` 的默认值，属"配置完整性"问题，不是"两处声明不一致"。
        # 段存在而叶子缺失才是漂移——改名/漏改就是这么发生的。
        if _dig(documents[source], keys[:-1]) is _MISSING:
            skipped += 1
            continue
        checked += 1
        declared = _dig(documents[source], keys)
        if declared is _MISSING:
            drifted.append({"key": key_text, "reason": "declaration_missing"})
            continue
        if not isinstance(declared, str):
            drifted.append(
                {
                    "key": key_text,
                    "reason": "declaration_not_a_path",
                    "declared": declared,
                }
            )
            continue
        expected = derive(paths).relative_to(paths.root).as_posix()
        actual = declared_directory(declared)
        if actual != expected:
            drifted.append(
                {
                    "key": key_text,
                    "reason": "path_declaration_drift",
                    "declared": declared,
                    "expected_prefix": expected,
                }
            )
    return drifted, checked, skipped


def _check_member_rules(
    paths: RepoPaths, documents: dict[str, dict]
) -> tuple[list[dict], int, int]:
    """比对列表型声明（成员判定）：声明必须包含代码实际使用的路径。"""
    drifted: list[dict] = []
    checked = 0
    skipped = 0
    for source, keys, derive in MEMBER_RULES:
        if source not in documents:
            continue
        key_text = f"{source}:" + ".".join(keys)
        declared = _dig(documents[source], keys)
        if declared is _MISSING:
            skipped += 1
            continue
        checked += 1
        if not isinstance(declared, list):
            drifted.append(
                {
                    "key": key_text,
                    "reason": "declaration_not_a_list",
                    "declared": declared,
                }
            )
            continue
        expected = derive(paths).relative_to(paths.root).as_posix()
        members = {declared_directory(v) for v in declared if isinstance(v, str)}
        if expected not in members:
            drifted.append(
                {
                    "key": key_text,
                    "reason": "path_declaration_missing_member",
                    "expected_prefix": expected,
                    "declared": sorted(members),
                }
            )
    return drifted, checked, skipped


def check(root: Path) -> tuple[str, dict]:
    """逐条比对 config 声明与 `RepoPaths` 派生值；返回 doctor 检查项的 (state, fields)。

    三种失败都是 error，不是 warning——声明与实现不一致时，看规范的人和跑代码的
    机器会得到不同的结论，这比"某个目录不存在"严重：后者会立刻报错，前者会一直
    静默错下去（`indexing` 的 root 反推就是这么错了整个批次 1 的窗口）。
    """
    from .policy import load_policy, policy_path
    from .schemas import load_schemas, schemas_path

    paths = RepoPaths(root)
    present = {
        "policy": policy_path(root).is_file(),
        "schemas": schemas_path(root).is_file(),
    }
    if not any(present.values()):
        # 配置整体不存在（最小化的临时树/新克隆）：可见地跳过，不装作比对通过。
        # 与 working TTL 的 `ttl_disabled` 同型——"没检查"必须和"检查通过"区分开。
        return "ok", {"checked": 0, "reason": "config_absent"}
    documents = {}
    if present["policy"]:
        documents["policy"] = load_policy(root)
    if present["schemas"]:
        documents["schemas"] = load_schemas(root)
    drifted, checked, skipped = _check_value_rules(paths, documents)
    member_drifted, member_checked, member_skipped = _check_member_rules(
        paths, documents
    )
    drifted.extend(member_drifted)
    checked += member_checked
    skipped += member_skipped
    summary = {"checked": checked, "sources": sorted(documents)}
    if skipped:
        summary["skipped_absent_sections"] = skipped
    if not drifted:
        return "ok", summary
    return "error", {
        **summary,
        "drifted": drifted[:12],
        "drifted_count": len(drifted),
        "next_action": "改布局要同时改 tools/paths.py 与 config/*.yaml；本项指出的是两者已经不一致",
    }
