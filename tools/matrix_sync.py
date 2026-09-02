"""追踪矩阵完成度自动校验与同步（matrix sync）。

背景：`docs/traceability-matrix.md` 的「完成度」列此前由人工维护，会随代码
演进而滞后（2026-09-02 实测：12 条 Designed 实际已实现，另有人工改写引入
不存在的测试文件引用）。本模块把「完成度」变成机器派生列，人的职责收敛为
维护两个语义列：「状态」（Designed / Implemented（部分）/ Implemented，粗粒度
人工判断）与「测试」（描述证据文件，语义性必须人写）。「完成度」四档由
「状态 × 引用文件存在性」机械派生，任何人工改写都会在下次 check/sync 时被
纠正。

派生规则（与矩阵「完成度列说明」对齐）：

+---------------------------+--------------+-------------------------------+
| 状态列（人维护）            | 引用文件      | 完成度（机器派生）             |
+---------------------------+--------------+-------------------------------+
| Designed                  | 无关         | 未开始                        |
| Implemented（部分）        | 全部存在      | 主体完成                      |
| Implemented（部分）        | 有缺失       | 悬空引用（check 报硬错误）      |
| Implemented               | 全部存在      | 完成                          |
| Implemented               | 有缺失       | 悬空引用（check 报硬错误）      |
+---------------------------+--------------+-------------------------------+

语义边界：完成度列只表达「状态列 × 证据文件是否全部真实存在」这一可机器判定
的事实；「还有多少功能缺口」属于语义判断，由状态列（Implemented（部分））
与测试列正文承载，不在此列重复表达。

引用解析：

- 完整路径（``tests/xxx.py``、``tools/xxx.py``）直接按仓库根校验；
- 裸文件名（``test_wiki_schema.py``）在已知测试前缀下查找唯一命中；
- 合并写法（``test_inventory.py/test_migration.py``）拆分为两个引用。

例外与边界：

- 测试列为纯描述性文字（如 WEB-001「frontend 工程骨架…」，不含 .py 引用）
  时无法派生，保留原值并在报告中标记 ``no_refs``，不强行改写；
- 状态列为 Designed 但引用文件全部存在时报告 ``status_drift`` warning：
  疑似状态滞后（代码已存在），但升级状态属语义判断，工具不自动改；
- check 是硬门禁（pre-commit 消费，stale/悬空引用即失败）；sync 是生成
  命令（重写完成度列，保留状态列与测试列原文）。
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.common import atomic_write, is_contained_regular_file

MATRIX_REL = "docs/traceability-matrix.md"

# 裸文件名查找的已知前缀（与仓库测试布局一致）
_TEST_PREFIXES = ("tests", "tests/validation", "tests/ingest", "tests/anchor")

# 完整路径前缀（resolve_ref 与 _split_merged 共用，二者必须一致）
_PATH_PREFIXES = ("tests/", "tools/", "backend/", "frontend/", "scripts/")

# 完成度档位（与矩阵说明一致）
NOT_STARTED = "未开始"
PARTIAL = "部分"
MOSTLY = "主体完成"
DONE = "完成"

_REF_RE = re.compile(r"([\w./-]+\.py)")


def parse_rows(text: str) -> tuple[list[dict], int]:
    """解析矩阵数据行 → (rows, skipped)。

    ``skipped`` 是矩阵表内形似数据行但解析失败的行数（列数 != 8 或 ID 不合法），
    用于检测矩阵格式漂移。用状态机只统计「规范 ID」表头之后的 8 列数据行：
    文档中的其它表（前缀表、完成度说明表、验收场景覆盖表等）不在状态内不误计。
    """
    rows: list[dict] = []
    skipped = 0
    in_matrix = False
    for line in text.splitlines():
        # 章节标题退出矩阵状态：矩阵只存在于连续表格内，遇 ## 即结束
        if line.startswith("## "):
            in_matrix = False
            continue
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # 表头：规范 ID 表（8 列）进入矩阵状态；其它表头不进入
        if cells and cells[0] == "规范 ID":
            in_matrix = len(cells) == 8
            continue
        if not in_matrix:
            continue
        if len(cells) == 8 and re.match(r"^:?-+:?$", cells[1] or ""):
            continue  # 分隔行
        if len(cells) != 8:
            skipped += 1
            continue
        ident = cells[0]
        # 规范 ID 前缀最长 6 字母（SKILL），最短 2（如 SCH）；不存在非 ASCII 连字符
        if not re.match(r"^[A-Z]{2,6}-\d{3}$", ident):
            skipped += 1
            continue
        rows.append(
            {
                "id": ident,
                "feature": cells[1],
                "adr": cells[2],
                "design": cells[3],
                "ac": cells[4],
                "test": cells[5],
                "status": cells[6],
                "completion": cells[7],
            }
        )
    return rows, skipped


def _split_merged(refs: list[str]) -> list[str]:
    """拆分合并写法：``test_a.py/test_b.py`` → [test_a.py, test_b.py]。"""
    out = []
    for ref in refs:
        if "/" in ref and not ref.startswith(_PATH_PREFIXES):
            out.extend(ref.split("/"))
        else:
            out.append(ref)
    return out


def resolve_ref(ref: str, root: Path) -> str | None:
    """解析单个引用为仓库内路径；不存在返回 None。"""
    ref = ref.strip()
    if not ref.endswith(".py"):
        return None
    if ref.startswith(_PATH_PREFIXES):
        # 完整路径：用 is_contained_regular_file 判定，拒绝符号链接逃逸（C004）
        return ref if is_contained_regular_file(root, root / ref) else None
    # 裸文件名：在已知前缀下查找唯一命中（多命中视为无法唯一解析）
    hits = [
        f"{p}/{ref}"
        for p in _TEST_PREFIXES
        if is_contained_regular_file(root, root / f"{p}/{ref}")
    ]
    return hits[0] if len(hits) == 1 else None


def extract_refs(test_cell: str) -> list[str]:
    """从测试列提取去重后的 .py 引用（含合并写法拆分）。"""
    refs = _REF_RE.findall(test_cell)
    refs = _split_merged(refs)
    seen, out = set(), []
    for r in refs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def derive_completion(status: str, missing: list[str]) -> str | None:
    """按状态列 + 引用缺失情况派生完成度；无法判定返回 None。

    语义边界：完成度列只表达「状态列 × 证据文件是否全部真实存在」这一可机器
    判定的事实；「还有多少功能缺口」属于语义判断，由状态列（Implemented
    （部分））与测试列正文承载，不在此列重复表达。引用缺失一律由 check 的
    dangling 分支按硬错误处理，不派生为「部分」。
    """
    if status == "Designed":
        return NOT_STARTED
    if status == "Implemented":
        return DONE if not missing else None  # 缺失时由调用方报悬空引用
    if status == "Implemented（部分）":
        return MOSTLY if not missing else None  # 缺失 = 悬空，报错而非降档
    return None  # 未知状态，保留原值


def _read_matrix(root: Path) -> tuple[str | None, dict | None]:
    """读取矩阵文本；失败返回 (None, error 报告)（读路径统一异常边界）。

    缺失与编码损坏都映射为结构化 ``matrix_unreadable``，调用方（check/sync）
    据此决定降级策略，不裸抛。
    """
    matrix_path = root / MATRIX_REL
    try:
        return matrix_path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, {
            "state": "error",
            "reason": f"matrix_unreadable:{type(exc).__name__}",
        }


def _judge_row(root: Path, row: dict) -> list[tuple[str, object]]:
    """单行判定 → [(bucket, entry)] 增量列表；空 = 无问题。

    check 与 sync 共用同一判定：行 → 需要处理的一批「桶 + 条目」。桶包括
    stale / dangling / drift / no_refs / unknown_status；sync 只消费 stale
    （其 derived 即替换值），其余桶留给 check 报告，天然避免两处重复分支。
    """
    refs = extract_refs(row["test"])
    resolved = [r for r in refs if resolve_ref(r, root)]
    missing = [r for r in refs if r not in resolved]
    if missing:
        return [("dangling", {"id": row["id"], "missing": missing})]
    if row["status"] == "Designed":
        out: list[tuple[str, object]] = []
        if row["completion"] != NOT_STARTED:
            out.append(
                (
                    "stale",
                    {
                        "id": row["id"],
                        "matrix": row["completion"],
                        "derived": NOT_STARTED,
                    },
                )
            )
        if resolved:
            out.append(("drift", {"id": row["id"], "resolved": resolved}))
        return out
    if not refs:
        return [("no_refs", row["id"])]
    derived = derive_completion(row["status"], missing)
    if derived is None:
        return [("unknown_status", {"id": row["id"], "status": row["status"]})]
    if derived != row["completion"]:
        return [
            (
                "stale",
                {"id": row["id"], "matrix": row["completion"], "derived": derived},
            )
        ]
    return []


def check(root: Path) -> dict:
    """校验矩阵完成度与文件证据一致；返回 doctor 风格报告。"""
    root = Path(root).resolve()
    text, read_error = _read_matrix(root)
    if read_error is not None:
        return read_error

    rows, skipped = parse_rows(text)
    buckets: dict[str, list] = {
        "stale": [],
        "dangling": [],
        "drift": [],
        "no_refs": [],
        "unknown_status": [],
    }
    for row in rows:
        for bucket, entry in _judge_row(root, row):
            buckets[bucket].append(entry)

    fields: dict = {"rows": len(rows)}
    if skipped:
        fields["skipped"] = (
            skipped  # 格式漂移信号，报告但由 rows==0 或调用方决定是否阻断
        )
    if buckets["no_refs"]:
        fields["no_refs"] = buckets["no_refs"]
    if buckets["drift"]:
        fields["status_drift"] = buckets["drift"]  # 语义判断，不自动改
    if buckets["unknown_status"]:
        fields["unknown_status"] = buckets[
            "unknown_status"
        ]  # 状态列拼写漂移，不静默跳过
    # 悬空是比 stale 更硬的事实错误：同时存在时优先暴露悬空，避免门禁多次往返
    if buckets["dangling"]:
        fields["dangling_refs"] = buckets["dangling"]
        if buckets["stale"]:
            fields["stale"] = buckets["stale"]
        fields["next_action"] = "修复矩阵「测试」列悬空引用"
        return {"state": "error", **fields}
    if buckets["stale"]:
        fields["stale"] = buckets["stale"]
        fields["next_action"] = "python -m tools.cli matrix sync"
        return {"state": "error", **fields}
    if not rows:
        return {"state": "error", "reason": "matrix_format_drift", "rows": 0}
    return {"state": "ok", **fields}


def sync(root: Path, *, dry_run: bool = False) -> dict:
    """按状态列 + 文件证据重写矩阵「完成度」列；dry_run 只报告不写盘。"""
    root = Path(root).resolve()
    matrix_path = root / MATRIX_REL
    text, read_error = _read_matrix(root)
    if read_error is not None:
        return read_error

    rows, _ = parse_rows(text)
    replacements: dict[str, str] = {}
    for row in rows:
        for bucket, entry in _judge_row(root, row):
            # 只有 stale 携带 derived 替换值；dangling/no_refs/unknown 留给 check
            if bucket == "stale" and isinstance(entry, dict):
                replacements[row["id"]] = entry["derived"]

    changed: list[dict] = []
    if replacements:
        lines = text.splitlines(keepends=True)
        new_lines = []
        for line in lines:
            m = re.match(r"^\| ([A-Z]{3,4}-\d{3}) \|", line)
            if m and m.group(1) in replacements:
                parts = line.split("|")
                if len(parts) == 10:
                    parts[8] = f" {replacements[m.group(1)]} "
                    updated_line = "|".join(parts)
                    changed.append(
                        {"id": m.group(1), "completion": replacements[m.group(1)]}
                    )
                else:
                    updated_line = line
                new_lines.append(updated_line)
            else:
                new_lines.append(line)
        new_text = "".join(new_lines)  # keepends 保留每行行尾，含末尾换行
        if not dry_run:
            atomic_write(matrix_path, new_text.encode("utf-8"))

    result: dict = {"state": "ok", "changed": changed}
    if dry_run:
        result["dry_run"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    """matrix sync CLI 入口：check 硬门禁、sync 重写完成度列；返回进程退出码。"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Traceability matrix completion sync")
    parser.add_argument("action", choices=("check", "sync"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.action == "check":
        result = check(args.root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["state"] == "ok" else 2
    result = sync(args.root, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 生成了改动 → 退出码 1（pre-commit 惯例：让提交被阻止、用户重新 add 后再提交）
    return 1 if result.get("changed") else 0


if __name__ == "__main__":
    raise SystemExit(main())
