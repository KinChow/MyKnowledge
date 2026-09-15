"""porcelain 入口 ``python -m tools.myk`` 的分派契约。

只验证"名词/动词 → 正确的 plumbing 命令 + 原样转发参数"，不重复校验各 plumbing
命令自身的行为（那些在各自的测试里）。COMMANDS 被 spy 替换，因此这里也不触发真实
domain 逻辑。
"""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from unittest import mock

from tools import myk


class _Spy:
    """记录被调用的 plumbing 命令名与转发的 argv，返回哨兵退出码。"""

    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def for_name(self, name: str):
        def _call(argv: list[str]) -> int:
            self.calls.append((name, argv))
            return 7  # 哨兵：断言 main 原样透传 plumbing 的退出码

        return _call

    def patched(self):
        replacement = {name: self.for_name(name) for name in myk.COMMANDS}
        return mock.patch.dict(myk.COMMANDS, replacement, clear=False)


class MappingContractTests(unittest.TestCase):
    """映射表本身的完整性——防止未来改名/漏项静默漂移。"""

    def _mapped_commands(self) -> set[str]:
        mapped = set(myk.PASSTHROUGH.values())
        for verbs in myk.NOUNS.values():
            mapped.update(verbs.values())
        return mapped

    def test_every_target_exists_in_plumbing(self):
        """每个映射目标都必须是 tools.cli.COMMANDS 的真实命令。"""
        for command in self._mapped_commands():
            self.assertIn(command, myk.COMMANDS, command)

    def test_human_surface_is_all_but_machine_commands(self):
        """porcelain 覆盖 = 全部 plumbing 命令减去不进人输入面的 matrix / skill。"""
        expected = set(myk.COMMANDS) - {"matrix", "skill"}
        self.assertEqual(self._mapped_commands(), expected)

    def test_noun_help_matches_dispatch_nouns(self):
        """帮助文本覆盖且仅覆盖真实名词（含透传名词）。"""
        self.assertEqual(set(myk.NOUN_HELP), set(myk.NOUNS) | set(myk.PASSTHROUGH))


class RoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spy = _Spy()

    def _run(self, argv: list[str]) -> int:
        with self.spy.patched():
            return myk.main(argv)

    def test_noun_verb_routes_and_forwards_rest(self):
        rc = self._run(["wiki", "validate", "content/wiki/x.md", "--root", "."])
        self.assertEqual(rc, 7)
        self.assertEqual(
            self.spy.calls, [("validate", ["content/wiki/x.md", "--root", "."])]
        )

    def test_source_second_level_video_verb(self):
        self._run(["source", "video-inventory", "--url", "u"])
        self.assertEqual(self.spy.calls, [("video-inventory", ["--url", "u"])])

    def test_wiki_publish_maps_to_release(self):
        # release ∈ ACTOR_ID_COMMANDS：未显式给 --actor-id 时会自填，故断言前缀 + 注入。
        with mock.patch.object(myk, "_default_actor_id", return_value="tester"):
            self._run(["wiki", "publish", "input", "--object-id", "x"])
        self.assertEqual(len(self.spy.calls), 1)
        name, forward = self.spy.calls[0]
        self.assertEqual(name, "release")
        self.assertEqual(forward[:3], ["input", "--object-id", "x"])
        self.assertEqual(forward[-2:], ["--actor-id", "tester"])

    def test_default_verb_forwards_positional(self):
        """query 无动词时，首参数是检索文本（位置参数），必须一并转发。"""
        self._run(["query", "transformer", "--top-k", "3"])
        self.assertEqual(self.spy.calls, [("query", ["transformer", "--top-k", "3"])])

    def test_doctor_default_verb(self):
        self._run(["doctor"])
        self.assertEqual(self.spy.calls, [("doctor", [])])

    def test_doctor_vault_verb(self):
        self._run(["doctor", "vault", "--root", "."])
        self.assertEqual(self.spy.calls, [("vault", ["--root", "."])])

    def test_build_index_verb(self):
        self._run(["build", "index", "rebuild", "--index", "i"])
        self.assertEqual(self.spy.calls, [("index", ["rebuild", "--index", "i"])])

    def test_passthrough_forwards_all(self):
        self._run(["question", "list", "--domain", "cs"])
        self.assertEqual(self.spy.calls, [("question", ["list", "--domain", "cs"])])
        self.spy.calls.clear()
        self._run(["backup", "status"])
        self.assertEqual(self.spy.calls, [("backup", ["status"])])


class ErgonomicsTests(unittest.TestCase):
    """A2 人性化默认：actor-id 自填、--json 剥离/透传、人类摘要输出。"""

    def test_actor_id_injected_when_absent(self):
        spy = _Spy()
        with (
            mock.patch.object(myk, "_default_actor_id", return_value="tester"),
            spy.patched(),
        ):
            myk.main(["wiki", "confirm", "content/wiki/x.md"])
        name, forward = spy.calls[0]
        self.assertEqual(name, "confirm")
        self.assertIn("--actor-id", forward)
        self.assertEqual(forward[forward.index("--actor-id") + 1], "tester")

    def test_actor_id_not_overridden_when_present(self):
        spy = _Spy()
        with (
            mock.patch.object(myk, "_default_actor_id", return_value="tester"),
            spy.patched(),
        ):
            myk.main(["wiki", "confirm", "x", "--actor-id", "me"])
        _, forward = spy.calls[0]
        self.assertEqual(forward.count("--actor-id"), 1)
        self.assertEqual(forward[forward.index("--actor-id") + 1], "me")

    def _run_capturing(self, argv: list[str], payload: dict) -> str:
        def _cmd(_argv: list[str]) -> int:
            print(json.dumps(payload))
            return 0

        buffer = io.StringIO()
        with (
            mock.patch.dict(myk.COMMANDS, {"validate": _cmd}, clear=False),
            contextlib.redirect_stdout(buffer),
        ):
            myk.main(argv)
        return buffer.getvalue()

    def test_human_summary_is_default_for_action(self):
        out = self._run_capturing(
            ["wiki", "validate", "x"], {"valid": True, "state": "ok"}
        )
        self.assertIn("valid=true", out)
        self.assertIn("--json 看完整输出", out)
        self.assertNotIn('"state"', out)  # 不是原始 JSON

    def test_json_flag_passes_through_raw_and_is_stripped(self):
        spy = _Spy()
        with spy.patched():
            myk.main(["wiki", "validate", "x", "--json"])
        _, forward = spy.calls[0]
        self.assertNotIn("--json", forward)  # myk 层消费，不下传 plumbing

    def test_json_flag_emits_raw_json(self):
        out = self._run_capturing(
            ["wiki", "validate", "x", "--json"], {"valid": False, "state": "blocked"}
        )
        self.assertIn('"valid"', out)  # 原始 JSON 透传

    def _run_browse(self, argv: list[str], payload: dict) -> str:
        def _cmd(_argv: list[str]) -> int:
            print(
                json.dumps(payload, separators=(",", ":"))
            )  # plumbing 的 compact 输出
            return 0

        buffer = io.StringIO()
        with (
            mock.patch.dict(myk.COMMANDS, {"query": _cmd}, clear=False),
            contextlib.redirect_stdout(buffer),
        ):
            myk.main(argv)
        return buffer.getvalue()

    def test_browse_output_is_pretty_printed_by_default(self):
        out = self._run_browse(["query", "x"], {"items": [1, 2], "scope": "public"})
        self.assertIn('"items"', out)
        self.assertIn("\n  ", out)  # 缩进重排，不再是 compact 单行

    def test_browse_json_flag_stays_compact(self):
        out = self._run_browse(["query", "x", "--json"], {"items": [1, 2]})
        self.assertNotIn("\n  ", out)  # --json 原样透传 plumbing 的 compact


class GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spy = _Spy()

    def _run(self, argv: list[str]) -> int:
        with self.spy.patched():
            return myk.main(argv)

    def test_no_args_prints_usage_returns_2(self):
        self.assertEqual(self._run([]), 2)
        self.assertEqual(self.spy.calls, [])

    def test_top_level_help_returns_0(self):
        self.assertEqual(self._run(["-h"]), 0)
        self.assertEqual(self.spy.calls, [])

    def test_unknown_noun_returns_2(self):
        self.assertEqual(self._run(["frobnicate"]), 2)
        self.assertEqual(self.spy.calls, [])

    def test_unknown_verb_without_default_returns_2(self):
        """source 没有默认动作：未知动词必须报错、且不误当位置参数转发出去。"""
        self.assertEqual(self._run(["source", "bogus"]), 2)
        self.assertEqual(self.spy.calls, [])

    def test_matrix_and_skill_are_not_reachable(self):
        """matrix / skill 不在人输入面：作为名词一律未知。"""
        self.assertEqual(self._run(["matrix"]), 2)
        self.assertEqual(self._run(["skill"]), 2)
        self.assertEqual(self.spy.calls, [])


if __name__ == "__main__":
    unittest.main()
