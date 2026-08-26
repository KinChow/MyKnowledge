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

COMMANDS = {
    "source": source_main,
    "anchor": anchor_main,
    "validate": validate_main,
    "audit": audit_main,
    "confirm": confirm_main,
}


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
            "  confirm   人工审计确认（operation-confirmation/v1 写入）",
            file=sys.stderr,
        )
        return 2
    return COMMANDS[args[0]](args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
