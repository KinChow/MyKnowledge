"""MyKnowledge 工具统一 CLI 入口。

用法（仓库根目录执行）：``python -m tools.cli <command> [options...]``

各工具模块只保留包内相对导入，不再支持单独直跑；本入口负责分派子命令。
每个子命令 glue 保持轻量：解析参数 -> 调用 domain 服务 -> 输出 JSON；
编排逻辑一律下沉到 ``tools/`` 的 domain 模块，不在此处展开。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tools.backup import BackupManager
from tools.doctor import main as doctor_main
from tools.evidence_anchor import main as anchor_main
from tools.ingest.source_ingestor import main as source_main
from tools.ingest.video_batch import main as video_batch_main
from tools.ingest.video_frames import main as video_frames_main
from tools.ingest.video_inventory import main as video_inventory_main
from tools.matrix_sync import main as matrix_main
from tools.public_projection import PublicProjectionGenerator
from tools.question_cli import question_main
from tools.validation.audit import main as audit_main
from tools.validation.confirm import main as confirm_main
from tools.validation.validator import main as validate_main
from tools.vault_registry import VaultRegistry
from tools.vault_registry import main as vault_main


def _print_json(result: dict, *, compact: bool = False) -> None:
    if compact:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def local_projection_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Materialize the owner-aware local/private projection"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--scope", choices=["local", "private"], default="local")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    _print_json(
        VaultRegistry(args.root, args.manifest).write_local_projection(
            args.scope, args.output
        )
    )
    return 0


def query_main(argv: list[str]) -> int:
    """Offline query entry point sharing the API projection and Retriever."""
    from tools.indexing import Retriever, default_public_index_path
    from tools.projection import PublicProjectionStore

    parser = argparse.ArgumentParser(
        description="Query the validated public projection"
    )
    parser.add_argument("query")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--scope", choices=["public", "local", "private"], default="public"
    )
    parser.add_argument("--vault-ids", default=None)
    parser.add_argument(
        "--index",
        type=Path,
        default=None,
        help="FTS5 index path (default: var/state/index/public.sqlite3 when present)",
    )
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args(argv)
    if args.scope != "public":
        _print_json(
            {"state": "blocked", "error_code": "query_scope_requires_api"}, compact=True
        )
        return 2
    items = PublicProjectionStore(args.root).public_items(with_body=True)
    index_path = args.index or default_public_index_path(args.root)
    _print_json(
        Retriever(items, index_path=index_path).search(
            args.query, "public", args.top_k
        ),
        compact=True,
    )
    return 0


def index_main(argv: list[str]) -> int:
    from tools.indexing import SQLiteIndex
    from tools.projection import PublicProjectionStore

    parser = argparse.ArgumentParser(
        description="Build or recover the projection SQLite index"
    )
    parser.add_argument("action", choices=["rebuild", "recover"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--scope", choices=["public", "local", "private"], default="public"
    )
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.scope == "public":
        items = PublicProjectionStore(args.root).public_items(with_body=True)
    else:
        items = VaultRegistry(args.root).local_projection(args.scope)["items"]
    index = SQLiteIndex(args.index)
    result = (
        index.rebuild(items, args.scope)
        if args.action == "rebuild"
        else index.recover(items, args.scope)
    )
    _print_json(result)
    return 0 if result.get("status") == "ok" else 2


def projection_read_main(argv: list[str]) -> int:
    from tools.skill_runtime import dispatch

    parser = argparse.ArgumentParser(
        description="Read one object from the validated public projection"
    )
    parser.add_argument("object_id")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-id", default="public")
    args = parser.parse_args(argv)
    result = dispatch(
        "read", {"vault_id": args.vault_id, "object_id": args.object_id}, root=args.root
    )
    _print_json(result, compact=True)
    return 0 if result.get("status") == "ok" else 2


def projection_backlinks_main(argv: list[str]) -> int:
    from tools.skill_runtime import dispatch

    parser = argparse.ArgumentParser(
        description="List backlinks from the validated public projection"
    )
    parser.add_argument("object_id")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-id", default="public")
    args = parser.parse_args(argv)
    result = dispatch(
        "backlinks",
        {"vault_id": args.vault_id, "object_id": args.object_id},
        root=args.root,
    )
    _print_json(result, compact=True)
    return 0 if result.get("status") == "ok" else 2


def backup_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Local backup status/manifest")
    parser.add_argument(
        "action",
        choices=[
            "status",
            "manifest",
            "verify",
            "restore",
            "export",
            "export-bundle",
            "restore-bundle",
        ],
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-id", default="public")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--target-vault-id")
    args = parser.parse_args(argv)
    from tools.question import practice_integrity_check

    manager = BackupManager(
        args.root, extra_verifiers={"practice": practice_integrity_check}
    )
    if args.action == "status":
        result = manager.status()
    elif args.action == "manifest":
        result = manager.create_manifest(args.vault_id)
    else:
        if not args.manifest:
            parser.error("--manifest is required for verify/restore/export-bundle")
        if args.action == "verify":
            result = manager.verify_manifest(args.manifest)
        elif args.action == "export":
            if not args.target:
                parser.error("--target is required for export")
            result = manager.export_manifest(args.manifest, args.target)
        elif args.action == "export-bundle":
            if not args.target:
                parser.error("--target is required for export-bundle")
            result = manager.export_bundle(args.manifest, args.target)
        elif args.action == "restore-bundle":
            if not args.target:
                parser.error("--target is required for restore-bundle")
            if not args.target_vault_id:
                parser.error("--target-vault-id is required for restore-bundle")
            result = manager.restore_bundle_to_vault(
                args.manifest, args.target, args.target_vault_id
            )
        else:
            if not args.target:
                parser.error("--target is required for restore")
            result = manager.restore_manifest(args.manifest, args.target)
    _print_json(result)
    # 退出码按契约 status 判据：ok=0，blocked/unavailable=2（原来无条件 return 0
    # 会把校验失败/阻断当成功回报）。
    return 0 if result.get("status") == "ok" else 2


def projection_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the validated public projection manifest"
    )
    parser.add_argument("action", choices=["generate"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    _print_json(PublicProjectionGenerator(args.root).generate(args.output))
    return 0


def override_main(argv: list[str]) -> int:
    """人工复议：声明某份 LLM `fail` 报告为误判（VAL-003，只能由人执行）。

    `list` 只读，列出绑定当前内容的 fail 报告及其标识与判定，供人核对后再签；
    `write` 写入复议记录，任何前置不满足一律结构化阻断。
    """
    from tools.validation.override import OverrideBlocked, write_override

    parser = argparse.ArgumentParser(description="Human review of a failed LLM audit")
    parser.add_argument("mode", choices=("list", "write"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--object-id", required=True)
    parser.add_argument("--report")
    parser.add_argument("--actor-id")
    parser.add_argument("--reason")
    parser.add_argument("--claims", nargs="*", default=[])
    args = parser.parse_args(argv)

    if args.mode == "list":
        _print_json(_failed_reports(args.root, args.object_id))
        return 0
    missing = [
        name
        for name, value in (
            ("--report", args.report),
            ("--actor-id", args.actor_id),
            ("--reason", args.reason),
        )
        if not value
    ]
    if missing:
        parser.error(f"write 模式必须提供 {' '.join(missing)}")
    try:
        record = write_override(
            args.root,
            object_id=args.object_id,
            report_sha256=args.report,
            actor_id=args.actor_id,
            reason=args.reason,
            claim_ids=list(args.claims),
        )
    except OverrideBlocked as exc:
        _print_json({"state": "blocked", "error_code": exc.code, "detail": exc.message})
        return 2
    _print_json({"state": "written", **record})
    return 0


def _failed_reports(root: Path, object_id: str) -> dict:
    """列出绑定当前内容的 fail 报告（只读，供人核对）。"""
    from tools.common import safe_id
    from tools.paths import RepoPaths
    from tools.validation.derived import read_json_dict
    from tools.validation.override import SUPPORTED_VERDICTS, overridden_report_ids
    from tools.validation.validator import WikiValidator

    try:
        object_id = safe_id(object_id)
    except ValueError:
        return {"state": "blocked", "error_code": "object_id_invalid"}
    paths = RepoPaths(root)
    matches = list(paths.wiki_root.rglob(f"{object_id}.md"))
    if not matches:
        return {"state": "blocked", "error_code": "object_not_found"}
    hashes = WikiValidator(root).validate(matches[0]).get("hashes") or {}
    overridden = overridden_report_ids(object_id, hashes or None, paths)
    items = []
    for path in sorted(paths.audit_validation("wiki", object_id).glob("*.json")):
        record = read_json_dict(path)
        if record is None or record.get("schema_version") != "validation-report/v1":
            continue
        if hashes and (
            record.get("wiki_content_sha256") != hashes.get("content_sha256")
            or record.get("wiki_evidence_sha256") != hashes.get("evidence_sha256")
        ):
            continue
        items.append(
            {
                "report_sha256": f"sha256:{path.stem}",
                "verdict": record.get("verdict"),
                "provider_identity": record.get("provider_identity"),
                "overridden": f"sha256:{path.stem}" in overridden,
                "disputed_claims": sorted(
                    str(c.get("claim_id"))
                    for c in record.get("claims") or []
                    if c.get("verdict") not in SUPPORTED_VERDICTS
                ),
            }
        )
    return {"object_id": object_id, "hashes": hashes, "reports": items}


def release_main(argv: list[str]) -> int:
    """发布输入的计算与人工确认事件写入（§6.8 / ADR-0010）。

    `input` 只读：打印参与 `release_input_sha256` 的全部材料与结果，供人核对——
    只给一个 hash 让人签，人无法核对。`confirm` 由人在本地终端显式执行，
    不得接入自动化脚本。
    """
    from tools.public_projection import PublicProjectionGenerator
    from tools.release_confirmation import write_event
    from tools.release_input import compute

    parser = argparse.ArgumentParser(
        description="Public release input and confirmation"
    )
    parser.add_argument("mode", choices=("input", "confirm"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--object-id", required=True)
    parser.add_argument("--operation-id", required=True)
    parser.add_argument("--actor-id")
    parser.add_argument("--reason")
    parser.add_argument("--nonce")
    parser.add_argument("--event-id")
    parser.add_argument("--leak-gate-report-sha256")
    args = parser.parse_args(argv)

    candidate, error = PublicProjectionGenerator(args.root).release_candidate(
        args.object_id
    )
    if candidate is None:
        _print_json({"state": "blocked", "error_code": error})
        return 2
    digest, material = compute(
        args.root,
        item=candidate["item"],
        content_sha256=candidate["content_sha256"],
        operation_id=args.operation_id,
    )
    if args.mode == "input":
        _print_json(
            {
                "schema_version": "release-input/v1",
                "object_id": args.object_id,
                "operation_id": args.operation_id,
                "release_input_sha256": digest,
                "material": material,
                "reviewed_content_sha256": candidate["content_sha256"],
                "reviewed_evidence_sha256": candidate["evidence_sha256"],
            }
        )
        return 0
    missing = [
        name
        for name, value in (
            ("--actor-id", args.actor_id),
            ("--reason", args.reason),
            ("--nonce", args.nonce),
            ("--event-id", args.event_id),
            ("--leak-gate-report-sha256", args.leak_gate_report_sha256),
        )
        if not value
    ]
    if missing:
        parser.error("confirm 模式必须提供：" + ", ".join(missing))
    result = write_event(
        args.root,
        {
            "schema_version": "public-release-confirmation/v1",
            "event_id": args.event_id,
            "operation_id": args.operation_id,
            "target_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": args.object_id,
            },
            "target_vault": "public",
            "actor_type": "human",
            "actor_id": args.actor_id,
            "decision": "approve",
            "release_input_sha256": digest,
            "reviewed_content_sha256": candidate["content_sha256"],
            "reviewed_evidence_sha256": candidate["evidence_sha256"],
            "leak_gate_report_sha256": args.leak_gate_report_sha256,
            "leak_gate_report_scope": "input-tree",
            "reason": args.reason,
            "confirmation_nonce": args.nonce,
        },
    )
    _print_json(result)
    # created 与幂等重复（changed=False）同为"目标状态已达成"，退出码 0；只有
    # status != ok（blocked）才是失败——原来无条件 return 0 会把阻断当成功回报。
    return 0 if result["status"] == "ok" else 2


def skill_main(argv: list[str]) -> int:
    from tools.skill_runtime import ALLOWED_ACTIONS, dispatch

    parser = argparse.ArgumentParser(description="Controlled MyKnowledge Skill runtime")
    parser.add_argument("action", choices=sorted(ALLOWED_ACTIONS))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--payload", type=Path)
    args = parser.parse_args(argv)
    payload = (
        json.loads(args.payload.read_text(encoding="utf-8")) if args.payload else {}
    )
    _print_json(dispatch(args.action, payload, root=args.root))
    return 0


COMMANDS = {
    "source": source_main,
    "video-inventory": video_inventory_main,
    "video-frames": video_frames_main,
    "video-batch": video_batch_main,
    "anchor": anchor_main,
    "validate": validate_main,
    "audit": audit_main,
    "override": override_main,
    "confirm": confirm_main,
    "vault": vault_main,
    "local-projection": local_projection_main,
    "query": query_main,
    "index": index_main,
    "read": projection_read_main,
    "backlinks": projection_backlinks_main,
    "backup": backup_main,
    "question": question_main,
    "doctor": doctor_main,
    "projection": projection_main,
    "release": release_main,
    "matrix": matrix_main,
    "skill": skill_main,
}

USAGE = """usage: python -m tools.cli <command> [options...]
commands:
  source           Source 导入与归档（local-file / personal-note / url）
  video-inventory  Bilibili/YouTube metadata inventory（不下载媒体）
  video-frames     抽取视频关键帧（单次直接写，无 operation/确认）
  video-batch      Resumable per-item video Source batch archive
  anchor           Evidence 锚定（在快照中定位引文生成 selector）
  validate         Wiki 确定性校验（schema + 跨字段规则 + 派生字段）
  audit            LLM 证据审计（provider 调用 + 覆盖义务 + 报告写入）
  confirm          人工审计确认（operation-confirmation/v1 写入）
  override         人工复议：声明某份 LLM fail 报告为误判（VAL-003，list/write）
  vault            Vault Registry 只读检查（F011）
  local-projection 生成 owner-aware local/private projection（F011）
  query            离线检索 public projection（F005）
  index            重建/恢复 projection SQLite 索引（F005）
  read             从 public projection 读取单个对象（F005）
  backlinks        从 public projection 列出反链（F005）
  backup           备份状态与 durable manifest（F012）
  question         Question 创建、作答与复习（F008）
  doctor           健康自检（projection/索引/sources/备份，ADR-0011 降级显性化）
  projection       生成 public projection manifest（F007）
  release          发布输入计算与 public release 人工确认（§6.8/ADR-0010）
  matrix           追踪矩阵完成度机器派生（check / sync，勿手改完成度列）
  skill            Agent Skill 受控 action 分发（F009）"""


def main(argv: list[str] | None = None) -> int:
    """分派子命令到对应工具模块；usage 覆盖 COMMANDS 的全部命令。"""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in COMMANDS:
        print(USAGE, file=sys.stderr)
        return 2
    return COMMANDS[args[0]](args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
