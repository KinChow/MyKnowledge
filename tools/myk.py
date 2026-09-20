"""MyKnowledge porcelain：给人用的高层入口（对应 ``tools.cli`` 的 plumbing 层）。

术语来源：git 的 porcelain / plumbing 分层
（https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain）。
``tools.cli`` 是 **plumbing**——22 条细粒度命令，供 CI / skill / 测试链式调用；
本模块是 **porcelain**——把其中 20 条面向人的命令归类到 7 个名词，人只需记住
``source / wiki / question / query / build / doctor / backup``。

命令面收敛参照 ADR-0017 §命令面（`gh` 少量名词 + 第二层动词、`kubectl` 少量动词 +
资源作参数）：``read``/``backlinks`` 并入 ``query``、``projection``/``index`` 合并为
``build``、``vault`` 并入 ``doctor``；``matrix``（pre-commit 钩子）与 ``skill``（agent 面）
不进人输入面，仍只在 ``tools.cli`` 暴露。

本模块只做名词/动词分派与转调，不复制任何 domain 逻辑；新增能力一律加在 plumbing，
porcelain 只重排入口。用法：``python -m tools.myk <名词> [动词] [选项...]``。
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys

from tools.cli import COMMANDS

# 名词 -> {动词: plumbing 命令名}。键为 ``None`` 时是该名词的默认动作（无动词时执行）。
NOUNS: dict[str, dict[str | None, str]] = {
    "source": {
        "add": "source",
        "video-inventory": "video-inventory",
        "video-frames": "video-frames",
        "video-batch": "video-batch",
        "list": "list",
        "retire": "retire",
        "update": "source-update",
    },
    "wiki": {
        "anchor": "anchor",
        "validate": "validate",
        "audit": "audit",
        "confirm": "confirm",
        "override": "override",
        "publish": "release",
        "list": "list",
        "retire": "retire",
        "deprecate": "retire",
    },
    "query": {
        None: "query",
        "read": "read",
        "backlinks": "backlinks",
    },
    "build": {
        "projection": "projection",
        "index": "index",
        "local-projection": "local-projection",
    },
    "doctor": {
        None: "doctor",
        "vault": "vault",
    },
}

# 整体透传的名词：对应 plumbing 命令自己已有子动词，porcelain 不再包一层。
PASSTHROUGH: dict[str, str] = {
    "question": "question",
    "backup": "backup",
}

# 需要 --actor-id 的 plumbing 命令：forward 未显式给出时从 git 身份自填。单人仓库
# actor 恒为本人，确认语义由显式 confirm/publish 动词承载，不因省略 id 而削弱。
ACTOR_ID_COMMANDS = {"confirm", "release", "override"}

# 泛型内容动词（list/retire 是 ContentRegistry 全动词，object_type 作首个位置参数）。
# porcelain 是 noun-first，故把名词（object_type）前置注入到 forward——对齐 kubectl 的
# ``get <resource>`` / ``delete <resource> <name>``。question 走自己的 plumbing（passthrough）。
_CONTENT_TYPE_NOUNS = {"source", "wiki"}
_TYPED_CONTENT_COMMANDS = {"list", "retire"}

# 单结果 action 命令：默认打印一行人类摘要（--json 反选原始 JSON）。其余为 browse
# 命令（query/read/backlinks/doctor/backup/question），输出原样透传。
ACTION_COMMANDS = {
    "source",
    "video-inventory",
    "video-frames",
    "video-batch",
    "anchor",
    "validate",
    "audit",
    "confirm",
    "override",
    "release",
    "projection",
    "index",
    "local-projection",
}

# 只用于人可读的帮助文本；名词顺序即帮助里的展示顺序。
NOUN_HELP: dict[str, str] = {
    "source": "采集与原件（add / update / list / retire / video-inventory / video-frames / video-batch）",
    "wiki": "wiki 生命周期（anchor / validate / audit / confirm / override / publish / list / retire / deprecate）",
    "question": "题库（create / list / session / answer / review / queue / ...）",
    "query": "检索一体（<文本> / read / backlinks）",
    "build": "派生重建（projection / index / local-projection）",
    "doctor": "健康自检（含 vault）",
    "backup": "本地备份（status / manifest / verify / restore / ...）",
}


def _usage() -> str:
    lines = [
        "usage: python -m tools.myk <名词> [动词] [选项...]",
        "",
        "名词（人输入面，porcelain）：",
    ]
    lines += [f"  {noun:<9} {NOUN_HELP[noun]}" for noun in NOUN_HELP]
    lines += [
        "",
        "机器 / agent 面（plumbing）见 python -m tools.cli。",
    ]
    return "\n".join(lines)


def _noun_usage(noun: str) -> str:
    if noun in PASSTHROUGH:
        return (
            f"'{noun}' 透传到 plumbing；动词见 "
            f"python -m tools.cli {PASSTHROUGH[noun]} -h"
        )
    verbs = sorted(v for v in NOUNS[noun] if v is not None)
    head = f"usage: python -m tools.myk {noun} <动词> [选项...]"
    body = "动词：" + ", ".join(verbs)
    if None in NOUNS[noun]:
        body += "（省略动词时执行默认动作）"
    return head + "\n" + body


def _default_actor_id() -> str:
    """人性化默认 actor-id：优先 git 身份，回退 $USER。"""
    try:
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            check=False,
        )
        email = result.stdout.strip()
    except OSError:
        email = ""
    return email or os.environ.get("USER") or "local-user"


def _summarize(obj: dict) -> str:
    """把单结果 action 的 JSON 压成一行人类摘要（通用字段，不做 per-command 格式化）。"""
    bits: list[str] = []
    if "valid" in obj:
        bits.append("valid=" + ("true" if obj["valid"] else "false"))
    if obj.get("status"):
        bits.append("status=" + str(obj["status"]))
    if obj.get("error_code"):
        bits.append("error=" + str(obj["error_code"]))
    for key in ("operation_id", "object_id", "source_id", "id"):
        if obj.get(key):
            bits.append(f"{key}={obj[key]}")
            break
    head = " ".join(bits) if bits else "done"
    return head + "（--json 看完整输出）"


def _render_summary(raw: str) -> str:
    """action 结果：摘要可解析的单 dict；解析失败或非 dict 时原样返回。"""
    text = raw.strip()
    if not text:
        return ""
    try:
        obj = json.loads(text)
    except ValueError:
        return raw
    return _summarize(obj) + "\n" if isinstance(obj, dict) else raw


def _render_pretty(raw: str) -> str:
    """browse 结果：缩进重排 JSON（query/read/backlinks 原本是 compact，难读）。

    通用做法，不做 per-command 格式化；解析失败/空时原样返回，`--json` 仍走原始透传。
    """
    text = raw.strip()
    if not text:
        return ""
    try:
        obj = json.loads(text)
    except ValueError:
        return raw
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def _dispatch(command: str, forward: list[str]) -> int:
    """转调 plumbing 命令，附加 porcelain 人性化：actor-id 自填 + 人类可读输出。

    `--json` 走原始透传；否则捕获输出后按类别渲染——action 命令给一行摘要，
    browse 命令（query/read/backlinks/doctor/backup/question）缩进重排。
    """
    json_flag = "--json" in forward
    forward = [arg for arg in forward if arg != "--json"]
    if command in ACTOR_ID_COMMANDS and "--actor-id" not in forward:
        forward = [*forward, "--actor-id", _default_actor_id()]
    if json_flag:
        return COMMANDS[command](forward)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = COMMANDS[command](forward)
    raw = buffer.getvalue()
    rendered = (
        _render_summary(raw) if command in ACTION_COMMANDS else _render_pretty(raw)
    )
    if rendered:
        print(rendered, end="")
    return code


def main(argv: list[str] | None = None) -> int:
    """分派 <名词> [动词] 到对应 plumbing 命令；其余参数原样转发。"""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(_usage(), file=sys.stderr)
        return 0 if args else 2
    noun, rest = args[0], args[1:]

    if noun in PASSTHROUGH:
        return _dispatch(PASSTHROUGH[noun], rest)
    if noun not in NOUNS:
        print(_usage(), file=sys.stderr)
        return 2

    verbs = NOUNS[noun]
    if rest and rest[0] in verbs:
        command, forward = verbs[rest[0]], rest[1:]
    elif None in verbs:
        # 默认动作：无动词、或首参数不是已知动词（例如 `query <文本>`）时走它，
        # 并把首参数一并转发（它是 plumbing 命令的位置参数，不是动词）。
        command, forward = verbs[None], rest
    else:
        print(_noun_usage(noun), file=sys.stderr)
        return 2
    # 泛型内容动词把名词（object_type）前置为首位置参数（kubectl 式 verb + resource）。
    if command in _TYPED_CONTENT_COMMANDS and noun in _CONTENT_TYPE_NOUNS:
        forward = [noun, *forward]
    return _dispatch(command, forward)


if __name__ == "__main__":
    raise SystemExit(main())
