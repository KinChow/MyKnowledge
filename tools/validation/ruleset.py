"""规则集抽取：按 spec ID 从规范文档实时取文并计算 ruleset_sha256（F003）。

对应 §18 阶段三与 wiki-claim-validation.md：规则集是**引用**而非副本——
`rule_refs` 每条含 ``doc``（规范文档路径）、``section``（spec ID/章节）、
``extract_sha256``（当次抽取的规则原文片段 hash）；``ruleset_sha256`` 为
``rule_refs`` 的 canonical JSON hash，随审计结论持久化用于重放。

规则原文不落第二份副本：抽取器按 ``(doc, section)`` 从规范文档实时取文，
章节重排/措辞变更会改变 ``extract_sha256``，届时既有 LLM 结论标记
``stale_ruleset``（AC-F003-015），不使人工确认失效。
"""

from __future__ import annotations

from pathlib import Path

from ..common import hash_canonical, sha256_text

# 规范文档相对仓库根的路径（§21：规范是唯一事实源）
SPEC_DOC = "docs/myknowledge-system-design.md"

# spec ID → (章节标题前缀, 覆盖章节说明)。标题前缀按文档层级匹配：
# 前缀以 "## " 开头是顶层章节，以 "### " 开头是子章节。
# 来源：§21 规范 ID 基线表 + 章节标题实测。
SPEC_SECTIONS: dict[str, tuple[str, str]] = {
    "SRC-001": ("### 5.9 写入的联网要求与来源完备性", "§5.9"),
    "ARC-001": ("### 5.6 原文快照归档与来源漂移", "§5.6"),
    "ARC-002": ("### 6.4 Claim 和 Evidence", "§6.4"),
    "WIKI-001": ("## 6. Wiki 严格规范", "§6"),
    "EVD-001": ("### 6.4 Claim 和 Evidence", "§6.4"),
    "VAL-001": ("### 6.9 引文规范化与逐字匹配", "§6.9"),
    "VAL-002": ("## 8. LLM 证据验证", "§8"),
}

DEFAULT_RULE_IDS = (
    "WIKI-001",
    "EVD-001",
    "VAL-001",
    "VAL-002",
    "ARC-002",
)


def _fence_marker(line: str) -> str | None:
    """行是否为 Markdown 围栏边界（``` / ~~~）；是则返回 marker，否则 None。"""
    stripped = line.strip()
    for marker in ("```", "~~~"):
        if stripped.startswith(marker):
            return marker
    return None


def extract_section(text: str, heading_prefix: str) -> str | None:
    """从规范文档正文中抽取指定标题起、到下一个同级/更高级标题止的原文。

    标题行按 Markdown ``#`` 层级解析；代码围栏（``` / ~~~）内的 ``#``
    行（YAML 注释、模板文本）不算标题，不得截断抽取（AC-F003-015 依赖
    extract_sha256 反映章节措辞变化）。找不到标题返回 None（调用方按
    ``ruleset_section_missing`` 处理，fail-closed 不静默跳过）。
    """
    lines = text.splitlines()
    target_level = len(heading_prefix) - len(heading_prefix.lstrip("#"))
    start: int | None = None
    in_fence: str | None = None  # 当前围栏 marker；None=围栏外
    for i, line in enumerate(lines):
        marker = _fence_marker(line)
        if marker is not None:
            in_fence = None if in_fence == marker else marker
            continue
        if in_fence:
            continue
        if line.strip().startswith(heading_prefix):
            start = i
            break
    if start is None:
        return None
    chunks: list[str] = []
    for line in lines[start + 1 :]:
        marker = _fence_marker(line)
        if marker is not None:
            in_fence = None if in_fence == marker else marker
            continue
        if not in_fence and line.strip().startswith("#"):
            level = len(line.strip()) - len(line.strip().lstrip("#"))
            if level <= target_level:
                break
        chunks.append(line)
    return "\n".join(chunks).strip()


def load_spec_doc(root: Path) -> str:
    """读取规范文档全文；缺失/不可读抛 OSError（fail-closed，由调用方映射错误码）。"""
    return (root / SPEC_DOC).read_text(encoding="utf-8")


def build_rule_refs(
    root: Path, rule_ids: list[str] | None = None
) -> tuple[list[dict], list[dict]]:
    """按 spec ID 组装 rule_refs；返回 (rule_refs, errors)。

    每条 ref: ``{"doc", "section", "spec_id", "extract_sha256"}``；
    章节定位失败时返回 ``ruleset_section_missing`` 错误并跳过该条（fail-closed：
    参与审计的规则条目缺失时不允许静默继续，由调用方决定阻断）。
    """
    errors: list[dict] = []
    rule_ids = rule_ids or list(DEFAULT_RULE_IDS)
    try:
        doc_text = load_spec_doc(root)
    except OSError as exc:
        return [], [{"code": "ruleset_doc_unreadable", "reason": str(exc)}]
    refs: list[dict] = []
    for spec_id in rule_ids:
        entry = SPEC_SECTIONS.get(spec_id)
        if entry is None:
            errors.append(
                {
                    "code": "ruleset_spec_unknown",
                    "spec_id": spec_id,
                    "reason": f"spec ID 不在映射表: {spec_id}",
                }
            )
            continue
        heading, section_label = entry
        extract = extract_section(doc_text, heading)
        if extract is None:
            errors.append(
                {
                    "code": "ruleset_section_missing",
                    "spec_id": spec_id,
                    "heading": heading,
                    "reason": f"规范文档中找不到章节: {heading}",
                }
            )
            continue
        refs.append(
            {
                "doc": SPEC_DOC,
                "section": section_label,
                "spec_id": spec_id,
                "extract_sha256": sha256_text(extract),
            }
        )
    return refs, errors


def ruleset_sha256(rule_refs: list[dict]) -> str:
    """ruleset_sha256 = hash_canonical(rule_refs)（与结论持久化，用于重放/失效判断）。"""
    return hash_canonical(rule_refs)


def policy_rule_ids(root: Path) -> list[str] | None:
    """从 config/policy.yaml 读取 validation.ruleset.rule_ids（运行时配置）。

    policy 缺失/字段非法返回 None，由调用方回退 DEFAULT_RULE_IDS；
    读取异常不抛（配置问题不应阻断确定性校验路径）。
    """
    try:
        import yaml

        policy_path = root / "config" / "policy.yaml"
        if not policy_path.exists():
            return None
        data = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        rule_ids = (
            (data or {}).get("validation", {}).get("ruleset", {}).get("rule_ids")
        )
        if isinstance(rule_ids, list) and all(
            isinstance(item, str) for item in rule_ids
        ):
            return rule_ids
        return None
    except Exception:
        return None


def load_ruleset(root: Path, rule_ids: list[str] | None = None) -> dict:
    """完整规则集：抽取 + 计算 sha256；任一规则条目缺失即返回错误（fail-closed）。

    rule_ids 缺省时优先读 ``config/policy.yaml`` 的 ``validation.ruleset.rule_ids``
    （运行时配置，README 声明的一致来源），缺失回退 DEFAULT_RULE_IDS。

    返回: {"rule_refs": [...], "ruleset_sha256": "sha256:...", "errors": [...]}
    """
    if rule_ids is None:
        rule_ids = policy_rule_ids(root) or list(DEFAULT_RULE_IDS)
    refs, errors = build_rule_refs(root, rule_ids)
    if errors:
        return {"rule_refs": [], "ruleset_sha256": None, "errors": errors}
    return {
        "rule_refs": refs,
        "ruleset_sha256": ruleset_sha256(refs),
        "errors": [],
    }
