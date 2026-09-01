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
from tools.inventory_legacy import main as inventory_main
from tools.migrate_legacy import main as migrate_main
from tools.public_projection import PublicProjectionGenerator
from tools.question import QuestionStore
from tools.validation.audit import main as audit_main
from tools.validation.confirm import main as confirm_main
from tools.validation.validator import main as validate_main
from tools.vault_lock import VaultLock
from tools.vault_registry import VaultRegistry
from tools.vault_registry import main as vault_main
from tools.vault_transfer import VaultTransfer
from tools.write_operation import WriteOperation


def _print_json(result: dict, *, compact: bool = False) -> None:
    if compact:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def write_main(argv: list[str]) -> int:
    """Minimal JSON interface for generic F004 write operations."""
    parser = argparse.ArgumentParser(description="Preview/apply generic writes")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--files", type=Path, help="JSON object mapping relative paths to UTF-8 content"
    )
    parser.add_argument("--apply")
    parser.add_argument(
        "--recover",
        metavar="OPERATION_ID",
        help="重跑被中断的提交收尾（applied_index_pending 的 projection/索引重建）",
    )
    parser.add_argument(
        "--confirmation",
        type=Path,
        help="operation-confirmation/v1 event JSON (see confirm-apply)",
    )
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)
    service = WriteOperation(args.root)
    confirmation = (
        json.loads(args.confirmation.read_text(encoding="utf-8"))
        if args.confirmation
        else None
    )
    if args.recover:
        _print_json(service.recover(args.recover))
    elif args.apply:
        _print_json(
            service.apply(args.apply, confirmed=args.confirm, confirmation=confirmation)
        )
    elif args.files:
        _print_json(service.preview(json.loads(args.files.read_text(encoding="utf-8"))))
    else:
        parser.error("--files / --apply / --recover is required")
    return 0


def confirm_apply_main(argv: list[str]) -> int:
    """人工确认事件生成（只读不写；hash 从 durable record 派生）。"""
    from tools.operation_store import OperationStore, build_apply_confirmation

    parser = argparse.ArgumentParser(
        description="Generate an operation-confirmation/v1 event for a human to review (prints JSON; never applies)",
        epilog="信任边界：本命令标记 actor_type=human 的依据是它运行在人的本地交互终端并由人显式执行（与 ADR-0010 同一信任模型，非密码学认证）。不得接入自动化脚本。",
    )
    parser.add_argument("operation_id")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--actor-id", required=True)
    parser.add_argument(
        "--scope", choices=["apply", "publish_private"], default="apply"
    )
    parser.add_argument("--content-sha256", help="required for publish_private")
    parser.add_argument("--evidence-sha256", help="required for publish_private")
    parser.add_argument(
        "--out", type=Path, help="optional: write event JSON to file instead of stdout"
    )
    args = parser.parse_args(argv)
    event, error = build_apply_confirmation(
        OperationStore(args.root),
        args.operation_id,
        args.actor_id,
        scope=args.scope,
        content_sha256=args.content_sha256,
        evidence_sha256=args.evidence_sha256,
    )
    if error is not None:
        _print_json({"state": "blocked", "error_code": error})
        return 2
    payload = json.dumps(event, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
        _print_json(
            {
                "state": "created",
                "path": str(args.out),
                "event_sha256": event["event_sha256"],
            }
        )
    else:
        print(payload, end="")
    return 0


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
    return 0 if result.get("state") not in {"failed"} else 2


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
    return 0 if result.get("state") not in {"blocked", "unavailable"} else 2


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
    return 0 if result.get("state") not in {"blocked", "unavailable"} else 2


def lock_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Recover an orphaned vault lock")
    parser.add_argument("action", choices=["recover"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-id", required=True)
    parser.add_argument("--operation-id", required=True)
    parser.add_argument("--actor-id", default="local-user")
    args = parser.parse_args(argv)
    _print_json(
        VaultLock.recover(args.root, args.vault_id, args.operation_id, args.actor_id)
    )
    return 0


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
    return 0


def question_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="F008 question practice")
    parser.add_argument("action", choices=["create", "answer", "review"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--question-id")
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--wiki", type=Path)
    parser.add_argument("--response")
    parser.add_argument("--rating", type=int)
    args = parser.parse_args(argv)
    store = QuestionStore(args.root)
    if args.action == "create":
        if not args.spec:
            parser.error("--spec is required")
        result = store.create(
            json.loads(args.spec.read_text(encoding="utf-8")), wiki_path=args.wiki
        )
    elif args.action == "answer":
        result = store.answer(args.question_id, json.loads(args.response))
    else:
        result = store.review(args.question_id, args.rating)
    _print_json(result)
    return 0


def transfer_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Preview/apply explicit cross-vault copy or move"
    )
    parser.add_argument("action", choices=["preview", "apply"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--source-vault")
    parser.add_argument("--source-path")
    parser.add_argument("--target-vault")
    parser.add_argument("--target-path")
    parser.add_argument("--operation-id")
    parser.add_argument("--move", action="store_true")
    parser.add_argument(
        "--confirmation", type=Path, help="operation-confirmation/v1 event JSON"
    )
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)
    service = VaultTransfer(args.root, args.manifest)
    if args.action == "preview":
        required = (
            args.source_vault,
            args.source_path,
            args.target_vault,
            args.target_path,
        )
        if any(value is None for value in required):
            parser.error("preview requires source/target vault and path")
        result = service.preview(
            args.source_vault,
            args.source_path,
            args.target_vault,
            args.target_path,
            move=args.move,
        )
    else:
        if not args.operation_id:
            parser.error("apply requires --operation-id")
        result = service.apply(
            args.operation_id,
            confirmed=args.confirm,
            confirmation=json.loads(args.confirmation.read_text(encoding="utf-8"))
            if args.confirmation
            else None,
        )
    _print_json(result)
    return 0 if result.get("state") not in {"blocked", "expired"} else 2


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


def reposition_main(argv: list[str]) -> int:
    """存量 source 的定位判定与改判（classify 只读；apply 需 owner 确认过的清单）。"""
    from tools.reposition import Thresholds, classify
    from tools.reposition import apply as reposition_apply

    parser = argparse.ArgumentParser(description="Reposition legacy sources")
    parser.add_argument("mode", choices=("classify", "apply"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--plan", type=Path, help="apply 模式必填：owner 确认过的清单")
    parser.add_argument("--final-min-chars", type=int, default=1500)
    parser.add_argument("--final-min-headings", type=int, default=3)
    args = parser.parse_args(argv)
    if args.mode == "classify":
        _print_json(
            classify(
                args.root,
                Thresholds(
                    final_min_chars=args.final_min_chars,
                    final_min_headings=args.final_min_headings,
                ),
            )
        )
        return 0
    if not args.plan:
        parser.error("apply 模式必须提供 --plan")
    result = reposition_apply(args.root, args.plan)
    _print_json(result)
    return 0 if result.get("schema_version") == "reposition-result/v1" else 2


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
    # already_applied 与 created 同为"目标状态已达成"，退出码 0；只有 blocked
    # 是失败——原来无条件 return 0 会把阻断当成功回报给调用方。
    return 0 if result["state"] in ("created", "already_applied") else 2


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
    "anchor": anchor_main,
    "validate": validate_main,
    "audit": audit_main,
    "override": override_main,
    "confirm": confirm_main,
    "write": write_main,
    "confirm-apply": confirm_apply_main,
    "vault": vault_main,
    "local-projection": local_projection_main,
    "query": query_main,
    "index": index_main,
    "read": projection_read_main,
    "backlinks": projection_backlinks_main,
    "lock": lock_main,
    "backup": backup_main,
    "question": question_main,
    "doctor": doctor_main,
    "inventory": inventory_main,
    "migrate": migrate_main,
    "transfer": transfer_main,
    "projection": projection_main,
    "release": release_main,
    "reposition": reposition_main,
    "skill": skill_main,
}

USAGE = """usage: python -m tools.cli <command> [options...]
commands:
  source           Source 导入与归档（local-file / personal-note / url）
  anchor           Evidence 锚定（在快照中定位引文生成 selector）
  validate         Wiki 确定性校验（schema + 跨字段规则 + 派生字段）
  audit            LLM 证据审计（provider 调用 + 覆盖义务 + 报告写入）
  confirm          人工审计确认（operation-confirmation/v1 写入）
  write            通用 Preview/Apply 写入（F004）
  confirm-apply    人工确认事件生成（operation-confirmation/v1，只读不写）
  vault            Vault Registry 只读检查（F011）
  local-projection 生成 owner-aware local/private projection（F011）
  query            离线检索 public projection（F005）
  index            重建/恢复 projection SQLite 索引（F005）
  read             从 public projection 读取单个对象（F005）
  backlinks        从 public projection 列出反链（F005）
  lock             恢复孤儿 vault 锁（F004）
  backup           备份状态与 durable manifest（F012）
  question         Question 创建、作答与复习（F008）
  doctor           健康自检（projection/索引/QMD/sources/备份，ADR-0011 降级显性化）
  inventory        生成 legacy 内容迁移清单（F010）
  migrate          legacy 内容迁移（F010）
  transfer         跨 vault 复制/移动的 preview/apply（F011）
  projection       生成 public projection manifest（F007）
  release          发布输入计算与 public release 人工确认（§6.8/ADR-0010）
  reposition       存量 source 定位判定与改判（classify / apply，F013）
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
