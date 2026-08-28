"""corroboration-v1：多 source 一致性/冲突的确定性检查（AC-F003-004/005/012）。

对应 wiki-claim-validation.md "Multi-source corroboration/conflict 算法"。
参照 FEVER/AVeriTeC 的 claim-evidence 判定语义（SUPPORTED/REFUTED/
conflicting-evidence，https://fever.ai），但坚持逐字引文而非近似匹配。

流程：结构归一（去重 + independence group）→ observation 规范化 →
成对判定 → 聚合。任何多数票都不能覆盖一个未解释的冲突；同组转载、
摘要与 derived_from 链永远不能贡献第二个独立组。

纯函数式：输入 resolution（确定性解析结果）+ provider observation（LLM
结构化输出），输出 corroboration 结果 dict，无实例状态。
"""

from __future__ import annotations

import datetime
import unicodedata
from dataclasses import dataclass

from ..common import hash_canonical

CORROBORATION_VERSION = "corroboration-v1"

# 常见单位换算表（corroboration-v1 normalizer 的 canonical unit 声明）
# 仅覆盖二进制/十进制字节与时间；无法转换的 unit 一律 unresolved（fail-closed）
UNIT_TABLE: dict[str, tuple[str, float]] = {
    "b": ("byte", 1.0),
    "byte": ("byte", 1.0),
    "bytes": ("byte", 1.0),
    "kb": ("byte", 1024.0),
    "mb": ("byte", 1024.0**2),
    "gb": ("byte", 1024.0**3),
    "tb": ("byte", 1024.0**4),
    "ms": ("second", 1e-3),
    "s": ("second", 1.0),
    "sec": ("second", 1.0),
    "second": ("second", 1.0),
    "seconds": ("second", 1.0),
    "min": ("second", 60.0),
    "minute": ("second", 60.0),
    "minutes": ("second", 60.0),
    "h": ("second", 3600.0),
    "hour": ("second", 3600.0),
    "hours": ("second", 3600.0),
}

# 简单谓词取反表（自然语言归一后的小写形式）
OPPOSITE_PREDICATES: dict[str, str] = {
    "是": "不是",
    "等于": "不等于",
    "支持": "反对",
    "存在": "不存在",
    "包含": "不包含",
    "允许": "禁止",
    "is": "is not",
    "equals": "does not equal",
    "supports": "opposes",
    "exists": "does not exist",
    "contains": "does not contain",
}


def _nfkc_label(value: str) -> str:
    """observation 规范化：NFC + 自然语言标签折叠空白；保留代码标识符与标点。"""
    return " ".join(unicodedata.normalize("NFC", value).split())


def _parse_number(text: str) -> tuple[float | None, str | None]:
    """解析 "1.5" 或 "1.5 MB" 形式的数值；返回 (数值, canonical unit) 或 (None, None)。"""
    parts = text.strip().split()
    if not parts:
        return None, None
    try:
        number = float(parts[0])
    except ValueError:
        return None, None
    if len(parts) == 1:
        return number, None  # 无单位：只能与同样无单位的 observation 比较
    unit = parts[1].lower().strip(".")
    entry = UNIT_TABLE.get(unit)
    if entry is None:
        return None, None  # 无法转换 → unresolved（AC-F003-012）
    canonical, factor = entry
    return number * factor, canonical


def _version_key(value: str):
    """版本解析：packaging.version（PyPI 标准）；无法解析返回 None（unresolved）。"""
    try:
        from packaging.version import Version

        return Version(value)
    except (ImportError, ValueError, TypeError):
        # InvalidVersion 继承 ValueError；解析不了就是 unresolved，不猜
        return None


def _date_key(value: str):
    """时间范围解析：ISO 8601 日期（2024-01-01）；无法解析返回 None（unresolved）。"""
    try:
        return datetime.date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


# 显式边界解析失败的哨兵（区别于"无边界"的 None）
_UNPARSEABLE = object()


def _interval_overlap(
    a_start: str | None,
    a_end: str | None,
    b_start: str | None,
    b_end: str | None,
    key_fn,
) -> bool | None:
    """半开区间 [start, end) 是否相交（TD 第 3/4 步）。

    - None 边界 = 无约束（该侧不判断）；
    - 显式提供的边界无法解析（版本/日期格式非法）→ 返回 None（无法判定，
      由调用方置 unresolved，**不得**当作无边界放行——⑤ time_range 修复）；
    - 返回 False 表示不相交（version_scoped）。
    """

    def _key(value: str | None):
        if value is None:
            return None
        key = key_fn(value)
        return key if key is not None else _UNPARSEABLE

    # 先校验全部显式边界的可解析性：任一无法解析 → 无法判定（unresolved），
    # 不得先返回"不相交"而绕过不可解析边界的检查（⑤ 修复）
    a_start_key = _key(a_start)
    a_end_key = _key(a_end)
    b_start_key = _key(b_start)
    b_end_key = _key(b_end)
    if _UNPARSEABLE in (a_start_key, a_end_key, b_start_key, b_end_key):
        return None
    # a 的 end ≤ b 的 start → 不相交；反之 b 的 end ≤ a 的 start → 不相交
    if a_end_key is not None and b_start_key is not None and a_end_key <= b_start_key:
        return False
    return not (
        b_end_key is not None and a_start_key is not None and b_end_key <= a_start_key
    )


@dataclass
class Observation:
    """规范化后的 observation（provider 输出的结构化描述 + 确定性规范）。"""

    subject: str
    predicate: str
    object: str
    qualifiers: dict
    observation_sha256: str
    version_range: tuple[str | None, str | None] = (None, None)
    time_range: tuple[str | None, str | None] = (None, None)
    numeric: tuple[float | None, str | None] | None = None
    unresolved: bool = False
    note: str | None = None


def normalize_observation(raw: dict | None) -> Observation | None:
    """把 provider 的 observation 规范化为可比较形式（corroboration-v1）。

    规则（TD 第 3 步）：Unicode NFC、自然语言标签折叠空白；单位先转换到
    canonical unit；没有明确单位或转换规则 → unresolved；数值默认精确比较，
    无隐含容差；版本/时间范围使用半开区间。
    """
    if not isinstance(raw, dict):
        return None
    subject = raw.get("subject")
    predicate = raw.get("predicate")
    object_ = raw.get("object")
    if not all(isinstance(v, str) and v for v in (subject, predicate, object_)):
        return None
    qualifiers = (
        raw.get("qualifiers") if isinstance(raw.get("qualifiers"), dict) else {}
    )
    version_range = _range_pair(qualifiers.get("version_range"))
    time_range = _range_pair(qualifiers.get("time_range"))
    # 数值：object 或 qualifiers.number；带单位时必须可转换
    numeric = None
    number_source = object_
    if isinstance(qualifiers.get("number"), str):
        number_source = qualifiers["number"]
    if number_source:
        number, unit = _parse_number(number_source)
        numeric = (number, unit) if number is not None else None
    unresolved = False
    note = None
    if isinstance(qualifiers.get("number"), str):
        # 显式声明数值 → 必须可解析，否则 unresolved（fail-closed）
        if numeric is None:
            unresolved = True
            note = "number_unparseable"
    elif numeric is None and _looks_numeric(number_source):
        # 疑似数值（首 token 为数字）但单位不可转换 → 只记 note 不置
        # unresolved：文本全等的命题仍可判 supports_same，仅数值比较不可行
        note = "unit_unconvertible"
    obs = Observation(
        subject=_nfkc_label(subject),
        predicate=_nfkc_label(predicate),
        object=_nfkc_label(object_),
        qualifiers=qualifiers,
        observation_sha256="",
        version_range=version_range,
        time_range=time_range,
        numeric=numeric,
        unresolved=unresolved,
        note=note,
    )
    obs.observation_sha256 = hash_canonical(
        {
            "subject": obs.subject,
            "predicate": obs.predicate,
            "object": obs.object,
            "qualifiers": qualifiers,
            "version_range": version_range,
            "time_range": time_range,
            "numeric": numeric,
            "unresolved": unresolved,
            "note": note,
        }
    )
    return obs


def _range_pair(value) -> tuple[str | None, str | None]:
    """接受 [start, end] / {"start":.., "end":..} / None；非法返回 (None, None)。"""
    if isinstance(value, list) and len(value) == 2:
        return (
            value[0] if isinstance(value[0], str) else None,
            value[1] if isinstance(value[1], str) else None,
        )
    if isinstance(value, dict):
        return (
            value.get("start") if isinstance(value.get("start"), str) else None,
            value.get("end") if isinstance(value.get("end"), str) else None,
        )
    return (None, None)


def _looks_numeric(text: str) -> bool:
    """首 token 是否为数字（用于识别"疑似数值但单位不可转换"的 object）。"""
    first = text.strip().split(maxsplit=1)[0] if text.strip() else ""
    try:
        float(first)
        return True
    except ValueError:
        return False


def structure_dedup(
    resolved_targets: list[dict], sources: dict[str, dict]
) -> tuple[list[dict], list[dict]]:
    """结构归一：按 (vault_id, source_id, evidence_id, snapshot, selector) 去重。

    返回 (去重后 targets, 告警列表)。independence_group 优先取 Source 声明；
    缺失或互相矛盾时退回唯一 source ObjectRef 并写 independence_unknown
    （禁止以域名/URL 相似度推断独立性，AC-F003-005）。
    """
    seen: set[tuple] = set()
    deduped: list[dict] = []
    warnings: list[dict] = []
    for target in resolved_targets:
        key = (
            target.get("resolved_object_ref", {}).get("vault_id"),
            target.get("source_id"),
            target.get("evidence_id"),
            target.get("snapshot_sha256"),
            hash_canonical(target.get("selector") or {}),
        )
        if key in seen:
            warnings.append(
                {
                    "code": "duplicate_target",
                    "source_id": target.get("source_id"),
                    "evidence_id": target.get("evidence_id"),
                }
            )
            continue
        seen.add(key)
        source = sources.get(target.get("source_id"))
        source_meta = source.get("metadata", {}) if source else {}
        provenance = source_meta.get("provenance") or {}
        independence_group = provenance.get("independence_group")
        if not isinstance(independence_group, str) or not independence_group:
            independence_group = f"source:{target.get('source_id')}"
            warnings.append(
                {
                    "code": "independence_unknown",
                    "source_id": target.get("source_id"),
                    "reason": (
                        "source 未声明 independence_group，退回唯一 source "
                        "ObjectRef；禁止以域名/URL 推断独立（AC-F003-005）"
                    ),
                }
            )
        deduped.append({**target, "independence_group": independence_group})
    return deduped, warnings


def pair_compare(a: Observation, b: Observation) -> dict:
    """成对判定：supports_same / conflicts / version_scoped / unresolved。

    规则（TD 第 4 步）：相同 normalized proposition 且适用范围相交 →
    supports_same；谓词相反、数值/单位不一致或前提互斥 → conflicts；
    范围不相交 → version_scoped（不算冲突，但要求 claim 写出范围）；
    无法比较 → unresolved。比较结果保存双方与 comparator version。
    """
    if a.unresolved or b.unresolved:
        return {"result": "unresolved", "reason": a.note or b.note or "unresolved"}
    # 数值可比较：双方 canonical unit 相同（含均无单位）时才按数值判等/判冲突
    # （"2 GB" ≡ "2048 MB" 换算后 unit 同为 byte；"1.5" 与 "1.5 s" 不可比）
    numeric_comparable = bool(a.numeric and b.numeric and a.numeric[1] == b.numeric[1])
    numeric_equal = bool(numeric_comparable and a.numeric[0] == b.numeric[0])
    object_same = a.object == b.object or numeric_equal
    same_proposition = (
        a.subject == b.subject and object_same and a.predicate == b.predicate
    )
    opposite = (
        a.subject == b.subject
        and object_same
        and (
            OPPOSITE_PREDICATES.get(a.predicate) == b.predicate
            or OPPOSITE_PREDICATES.get(b.predicate) == a.predicate
        )
    )
    # 文本全等的命题优先判定：即使单位不可转换，命题一致即 supports_same
    # （未知单位只影响数值比较，不影响命题一致性）
    if same_proposition:
        return {
            "result": "supports_same",
            "reason": "相同规范化命题且范围相交",
            "comparator": CORROBORATION_VERSION,
        }
    # 数值/单位不一致：双方数值可比时按数值判冲突（subject 相同即可）；
    # 一侧可比一侧不可比（单位不一致/无法转换）→ 无法比较（unresolved）
    numeric_conflict = False
    numeric_incomparable = False
    if a.subject == b.subject:
        if numeric_comparable:
            numeric_conflict = a.numeric[0] != b.numeric[0]
        elif a.numeric or b.numeric:
            numeric_incomparable = True
    v_overlap = _interval_overlap(
        a.version_range[0],
        a.version_range[1],
        b.version_range[0],
        b.version_range[1],
        _version_key,
    )
    t_overlap = _interval_overlap(
        a.time_range[0],
        a.time_range[1],
        b.time_range[0],
        b.time_range[1],
        _date_key,
    )
    if v_overlap is None or t_overlap is None:
        return {
            "result": "unresolved",
            "reason": "适用范围边界无法解析，无法判定是否相交",
            "comparator": CORROBORATION_VERSION,
        }
    if not (v_overlap and t_overlap):
        return {
            "result": "version_scoped",
            "reason": "适用范围不相交（半开区间），不构成冲突",
            "comparator": CORROBORATION_VERSION,
        }
    if opposite or numeric_conflict:
        return {
            "result": "conflicts",
            "reason": ("谓词相反" if opposite else "数值/单位不一致"),
            "comparator": CORROBORATION_VERSION,
        }
    if numeric_incomparable:
        return {
            "result": "unresolved",
            "reason": "数值单位无法转换，无法比较",
            "comparator": CORROBORATION_VERSION,
        }
    return {
        "result": "unresolved",
        "reason": "命题无法比较（subject/predicate/object 不同）",
        "comparator": CORROBORATION_VERSION,
    }


def compute_corroboration(
    resolved_targets: list[dict],
    sources: dict[str, dict],
    observations: dict[str, Observation | None],
    model_groups: dict[tuple[str, str], str] | None = None,
) -> dict:
    """corroboration-v1 聚合：输出 evidence_state 与冲突/佐证明细。

    model_groups：LLM 独立性判定的 per-target group 覆盖（AC-F003-005，
    key=(source_id, evidence_id)）。模型经 provenance 举证识别出的转载关系
    优先于 source 声明；``independence_unknown`` 值忽略（退回 source 默认，
    按单一 source 处理）。未举证/未判定的 target 仍用 source 声明。

    聚合规则（TD 第 5 步）：
    - 任一 conflicts（不同 independence group、范围相交）→ conflicting；
    - 无冲突且 ≥2 个不同独立组的 supports_same → corroborated；
    - 只有 1 个组支持 → supported；部分覆盖 → partial；无法比较 → unresolved。
    """
    targets, warnings = structure_dedup(resolved_targets, sources)
    if model_groups:
        for target in targets:
            group = model_groups.get((target["source_id"], target["evidence_id"]))
            if group is not None and group != "independence_unknown":
                target["independence_group"] = group
    pairs: list[dict] = []
    groups_support: dict[str, int] = {}
    conflict_pairs: list[dict] = []
    any_unresolved = False
    any_version_scoped = False
    same_group_conflicts = False
    for i in range(len(targets)):
        for j in range(i + 1, len(targets)):
            ta, tb = targets[i], targets[j]
            obs_a = observations.get(ta["evidence_id"])
            obs_b = observations.get(tb["evidence_id"])
            # 无法结构化的 target 不参与 corroboration（TD 第 2 步）
            if obs_a is None or obs_b is None:
                any_unresolved = True
                continue
            verdict = pair_compare(obs_a, obs_b)
            entry = {
                "target_a": {
                    "source_id": ta["source_id"],
                    "evidence_id": ta["evidence_id"],
                    "independence_group": ta["independence_group"],
                    "observation_sha256": obs_a.observation_sha256,
                },
                "target_b": {
                    "source_id": tb["source_id"],
                    "evidence_id": tb["evidence_id"],
                    "independence_group": tb["independence_group"],
                    "observation_sha256": obs_b.observation_sha256,
                },
                **verdict,
            }
            pairs.append(entry)
            if verdict["result"] == "conflicts":
                if ta["independence_group"] != tb["independence_group"]:
                    conflict_pairs.append(entry)
                else:
                    # ④ 同组冲突：同源转载的两条相反命题不得落 supported——
                    # 置 same_group_conflicts（unresolved 而非 supported，AC-F003-012）
                    same_group_conflicts = True
                    any_unresolved = True
            elif verdict["result"] == "supports_same":
                if ta["independence_group"] == tb["independence_group"]:
                    continue  # 同组转载不贡献独立佐证（AC-F003-005）
                groups_support[ta["independence_group"]] = (
                    groups_support.get(ta["independence_group"], 0) + 1
                )
                groups_support[tb["independence_group"]] = (
                    groups_support.get(tb["independence_group"], 0) + 1
                )
            elif verdict["result"] == "version_scoped":
                any_version_scoped = True
            else:
                any_unresolved = True

    if conflict_pairs:
        evidence_state = "conflicting"
        status = "review"
    elif len(groups_support) >= 2:
        evidence_state = "corroborated"
        status = None
    elif len(groups_support) == 1:
        evidence_state = "supported"
        status = None
    elif any_unresolved:
        evidence_state = "unresolved"
        status = None
    else:
        evidence_state = "supported"
        status = None

    return {
        "version": CORROBORATION_VERSION,
        "evidence_state": evidence_state,
        "status": status,
        "independent_groups": sorted(groups_support.keys()),
        "conflict_pairs": conflict_pairs,
        "same_group_conflicts": same_group_conflicts,
        "pairs": pairs,
        "warnings": warnings,
        "duplicate_targets": [w for w in warnings if w["code"] == "duplicate_target"],
        "version_scoped_targets": any_version_scoped,
    }
