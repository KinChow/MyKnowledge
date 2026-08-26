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
            file=sys.stderr,
        )
        return 2
    return COMMANDS[args[0]](args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
