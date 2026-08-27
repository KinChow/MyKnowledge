"""MyKnowledge 工具统一 CLI 入口。

用法（仓库根目录执行）：``python -m tools.cli <source|anchor|validate|audit|confirm> [options...]``

各工具模块只保留包内相对导入，不再支持单独直跑；本入口负责分派子命令。
"""

from __future__ import annotations

import sys

from tools.evidence_anchor import main as anchor_main
from tools.ingest.source_ingestor import main as source_main
from tools.validation.audit import main as audit_main
from tools.validation.confirm import main as confirm_main
from tools.validation.validator import main as validate_main
from tools.write_operation import WriteOperation
from tools.vault_registry import main as vault_main
from tools.backup import BackupManager
from tools.question import QuestionStore
from tools.inventory_legacy import main as inventory_main
from tools.migrate_legacy import main as migrate_main
from tools.vault_lock import VaultLock
from tools.vault_transfer import VaultTransfer
from tools.public_projection import PublicProjectionGenerator

COMMANDS = {
    "source": source_main,
    "anchor": anchor_main,
    "validate": validate_main,
    "audit": audit_main,
    "confirm": confirm_main,
}


def write_main(argv: list[str]) -> int:
    """Minimal JSON interface for generic F004 write operations."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Preview/apply generic writes")
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--files", type=__import__("pathlib").Path, help="JSON object mapping relative paths to UTF-8 content")
    parser.add_argument("--apply")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)
    service = WriteOperation(args.root)
    if args.apply:
        print(json.dumps(service.apply(args.apply, confirmed=args.confirm), ensure_ascii=False, indent=2))
    elif args.files:
        print(json.dumps(service.preview(json.loads(args.files.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))
    else:
        parser.error("--files or --apply is required")
    return 0


COMMANDS["write"] = write_main
COMMANDS["vault"] = vault_main

def local_projection_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Materialize the owner-aware local/private projection")
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--manifest", type=__import__("pathlib").Path)
    parser.add_argument("--scope", choices=["local", "private"], default="local")
    parser.add_argument("--output", type=__import__("pathlib").Path)
    args = parser.parse_args(argv)
    result = __import__("tools.vault_registry", fromlist=["VaultRegistry"]).VaultRegistry(args.root, args.manifest).write_local_projection(args.scope, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0

COMMANDS["local-projection"] = local_projection_main

def query_main(argv: list[str]) -> int:
    """Offline query entry point sharing the API projection and Retriever."""
    import argparse, json
    from backend.app import _load_public_projection
    from tools.indexing import Retriever
    parser = argparse.ArgumentParser(description="Query the validated public projection")
    parser.add_argument("query")
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--scope", choices=["public", "local", "private"], default="public")
    parser.add_argument("--vault-ids", default=None)
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args(argv)
    if args.scope != "public":
        print(json.dumps({"state": "blocked", "error_code": "query_scope_requires_api"}, ensure_ascii=False))
        return 2
    items = _load_public_projection(args.root)
    result = Retriever(items).search(args.query, "public", args.top_k)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0

COMMANDS["query"] = query_main

def index_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Build or recover the projection SQLite index")
    parser.add_argument("action", choices=["rebuild", "recover"])
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--scope", choices=["public", "local", "private"], default="public")
    parser.add_argument("--index", type=__import__("pathlib").Path, required=True)
    args = parser.parse_args(argv)
    from backend.app import _load_public_projection
    from tools.indexing import IndexBuilder, SQLiteIndex
    if args.scope == "public":
        items = _load_public_projection(args.root)
    else:
        from tools.vault_registry import VaultRegistry
        items = VaultRegistry(args.root).local_projection(args.scope)["items"]
    result = (SQLiteIndex(args.index).rebuild(items, args.scope) if args.action == "rebuild" else SQLiteIndex(args.index).recover(items, args.scope))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("state") not in {"failed"} else 2

COMMANDS["index"] = index_main

def projection_read_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Read one object from the validated public projection")
    parser.add_argument("object_id")
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--vault-id", default="public")
    args = parser.parse_args(argv)
    from tools.skill_runtime import dispatch
    result = dispatch("read", {"vault_id": args.vault_id, "object_id": args.object_id}, root=args.root)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result.get("state") not in {"blocked", "unavailable"} else 2

def projection_backlinks_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="List backlinks from the validated public projection")
    parser.add_argument("object_id")
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--vault-id", default="public")
    args = parser.parse_args(argv)
    from tools.skill_runtime import dispatch
    result = dispatch("backlinks", {"vault_id": args.vault_id, "object_id": args.object_id}, root=args.root)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result.get("state") not in {"blocked", "unavailable"} else 2

COMMANDS["read"] = projection_read_main
COMMANDS["backlinks"] = projection_backlinks_main

def lock_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Recover an orphaned vault lock")
    parser.add_argument("action", choices=["recover"]); parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--vault-id", required=True); parser.add_argument("--operation-id", required=True); parser.add_argument("--actor-id", default="local-user")
    args = parser.parse_args(argv)
    print(json.dumps(VaultLock.recover(args.root, args.vault_id, args.operation_id, args.actor_id), ensure_ascii=False, indent=2)); return 0

COMMANDS["lock"] = lock_main

def backup_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Local backup status/manifest")
    parser.add_argument("action", choices=["status", "manifest", "verify", "restore", "export", "export-bundle", "restore-bundle"])
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--vault-id", default="public")
    parser.add_argument("--manifest", type=__import__("pathlib").Path)
    parser.add_argument("--target", type=__import__("pathlib").Path)
    args = parser.parse_args(argv)
    manager = BackupManager(args.root)
    if args.action == "status": result = manager.status()
    elif args.action == "manifest": result = manager.create_manifest(args.vault_id)
    else:
        if not args.manifest: parser.error("--manifest is required for verify/restore/export-bundle")
        if args.action == "verify": result = manager.verify_manifest(args.manifest)
        elif args.action == "export":
            if not args.target: parser.error("--target is required for export")
            result = manager.export_manifest(args.manifest, args.target)
        elif args.action == "export-bundle":
            if not args.target: parser.error("--target is required for export-bundle")
            result = manager.export_bundle(args.manifest, args.target)
        elif args.action == "restore-bundle":
            if not args.target: parser.error("--target is required for restore-bundle")
            result = manager.restore_bundle(args.manifest, args.target)
        else:
            if not args.target: parser.error("--target is required for restore")
            result = manager.restore_manifest(args.manifest, args.target)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0

COMMANDS["backup"] = backup_main

def question_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="F008 question practice")
    parser.add_argument("action", choices=["create", "answer", "review"])
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--question-id"); parser.add_argument("--spec", type=__import__("pathlib").Path); parser.add_argument("--wiki", type=__import__("pathlib").Path); parser.add_argument("--response"); parser.add_argument("--rating", type=int)
    args = parser.parse_args(argv); store = QuestionStore(args.root)
    if args.action == "create":
        if not args.spec: parser.error("--spec is required")
        result = store.create(json.loads(args.spec.read_text(encoding="utf-8")), wiki_path=args.wiki)
    elif args.action == "answer": result = store.answer(args.question_id, json.loads(args.response))
    else: result = store.review(args.question_id, args.rating)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0

COMMANDS["question"] = question_main
COMMANDS["inventory"] = inventory_main
COMMANDS["migrate"] = migrate_main

def transfer_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Preview/apply explicit cross-vault copy or move")
    parser.add_argument("action", choices=["preview", "apply"])
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--manifest", type=__import__("pathlib").Path)
    parser.add_argument("--source-vault"); parser.add_argument("--source-path")
    parser.add_argument("--target-vault"); parser.add_argument("--target-path")
    parser.add_argument("--operation-id"); parser.add_argument("--move", action="store_true"); parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv); service = VaultTransfer(args.root, args.manifest)
    if args.action == "preview":
        required = (args.source_vault, args.source_path, args.target_vault, args.target_path)
        if any(value is None for value in required): parser.error("preview requires source/target vault and path")
        result = service.preview(args.source_vault, args.source_path, args.target_vault, args.target_path, move=args.move)
    else:
        if not args.operation_id: parser.error("apply requires --operation-id")
        result = service.apply(args.operation_id, confirmed=args.confirm)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result.get("state") not in {"blocked", "expired"} else 2

COMMANDS["transfer"] = transfer_main

def projection_main(argv: list[str]) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Generate the validated public projection manifest")
    parser.add_argument("action", choices=["generate"])
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--output", type=__import__("pathlib").Path)
    args = parser.parse_args(argv)
    result = PublicProjectionGenerator(args.root).generate(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0

COMMANDS["projection"] = projection_main

def skill_main(argv: list[str]) -> int:
    import argparse, json
    from tools.skill_runtime import dispatch
    parser = argparse.ArgumentParser(description="Controlled MyKnowledge Skill runtime")
    parser.add_argument("action", choices=sorted(__import__("tools.skill_runtime", fromlist=["ALLOWED_ACTIONS"]).ALLOWED_ACTIONS))
    parser.add_argument("--root", type=__import__("pathlib").Path, default=__import__("pathlib").Path.cwd())
    parser.add_argument("--payload", type=__import__("pathlib").Path)
    args = parser.parse_args(argv)
    payload = json.loads(args.payload.read_text(encoding="utf-8")) if args.payload else {}
    print(json.dumps(dispatch(args.action, payload, root=args.root), ensure_ascii=False, indent=2)); return 0

COMMANDS["skill"] = skill_main


def main(argv: list[str] | None = None) -> int:
    """分派子命令到对应工具：source 导入归档，anchor 证据锚定，validate Wiki
    校验，audit LLM 证据审计，confirm 人工审计确认。"""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in COMMANDS:
        print(
            "usage: python -m tools.cli <command> [options...]\n"
            "commands:\n"
            "  source    Source 导入与归档（local-file / personal-note / url）\n"
            "  anchor    Evidence 锚定（在快照中定位引文生成 selector）\n"
            "  validate  Wiki 确定性校验（schema + 跨字段规则 + 派生字段）\n"
            "  audit     LLM 证据审计（provider 调用 + 覆盖义务 + 报告写入）\n"
            "  confirm   人工审计确认（operation-confirmation/v1 写入）\n"
            "  write     通用 Preview/Apply 写入（F004）",
            "  vault     Vault Registry 只读检查（F011）",
            "  backup    备份状态与 durable manifest（F012）",
            "  question  Question 创建、作答与复习（F008）",
            "  inventory 生成 legacy 内容迁移清单（F010）",
            file=sys.stderr,
        )
        return 2
    return COMMANDS[args[0]](args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
