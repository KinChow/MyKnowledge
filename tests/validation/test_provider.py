from __future__ import annotations

import subprocess
from unittest import mock

from tools.validation.provider import AgentCliAdapter


def test_agent_cli_timeout_maps_to_context_exceeded_without_pid_attribute():
    adapter = AgentCliAdapter(cli="ducc", timeout_seconds=1)
    timeout = subprocess.TimeoutExpired(["ducc"], 1)
    assert not hasattr(timeout, "pid")
    with (
        mock.patch("tools.validation.provider.subprocess.run", side_effect=timeout),
        mock.patch.object(adapter, "_kill_group") as kill,
    ):
        result = adapter.audit({"wiki_id": "w", "claims": []}, {})
    assert result.error_code == "context_exceeded"
    kill.assert_called_once_with(None)


def test_provider_profile_resolves_to_the_repo_config_dir(tmp_path):
    """profile 路径写错一层会让凭据档案永远静默失效（2026-09-01 实测）。

    `_load_provider_profile` 曾解析到不存在的 `tools/config/`，于是
    `MYKNOWLEDGE_LLM_PROFILE` 无论怎么配都返回空 dict，只有环境变量路径可用。
    这里断言解析基准是仓库根的 `config/`（与 `.gitignore` 声明的位置一致）。
    """
    import os
    from pathlib import Path

    import yaml

    from tools.validation import provider as provider_module
    from tools.validation.provider import _load_provider_profile

    config_dir = Path(provider_module.__file__).resolve().parents[2] / "config"
    assert config_dir.is_dir(), config_dir
    assert (config_dir / "policy.yaml").is_file()  # 确认这是仓库根的 config/

    target = config_dir / "providers.local.yaml"
    if target.exists():  # 本机已有真实凭据档案：不触碰，只验证解析基准
        return
    profile = {"base_url": "https://example.invalid/v1", "model": "m", "api_key": "k"}
    target.write_text(
        yaml.safe_dump({"profiles": {"smoke": profile}}), encoding="utf-8"
    )
    try:
        with mock.patch.dict(os.environ, {"MYKNOWLEDGE_LLM_PROFILE": "smoke"}):
            assert _load_provider_profile() == profile
    finally:
        target.unlink()


# ducx `exec --json` 的真实事件流（2026-09-01 实测抓取，未改写）
DUCX_STDOUT = (
    "Reading additional input from stdin...\n"
    '{"type":"thread.started","thread_id":"01a05939-ef3f-7f82-a421-29e0fd8c7fcd"}\n'
    '{"type":"turn.started"}\n'
    '{"type":"item.completed","item":{"id":"item_0","type":"agent_message",'
    '"text":"{\\"wiki_id\\": \\"w\\", \\"verdict\\": \\"pass\\", \\"claims\\": [], '
    '\\"call_id\\": \\"c\\"}"}}\n'
    '{"type":"turn.completed","usage":{"input_tokens":10795,"output_tokens":9}}\n'
)


def test_ducx_payload_comes_from_the_agent_message_not_the_event_envelope():
    """事件流的首个 JSON 是 `thread.started`，当成模型输出必然 malformed_output。"""
    from tools.validation.provider import _extract_json

    adapter = AgentCliAdapter(cli="ducx")
    assert adapter._payload(DUCX_STDOUT) == {
        "wiki_id": "w",
        "verdict": "pass",
        "claims": [],
        "call_id": "c",
    }
    # 修复前的行为：抓到事件信封（回归锁——换回 _extract_json 立刻失败）
    assert _extract_json(DUCX_STDOUT).get("type") == "thread.started"


def test_ducc_json_schema_argument_drops_the_unresolvable_meta_refs():
    """带 `$schema` 时 ducc 直接拒收（`no schema with key or ref ...`，2026-09-01 实测）。"""
    import json

    from tools.validation.schema import load_json_schema

    schema = load_json_schema("validation-response-v1.json")
    assert "$schema" in schema and "$id" in schema  # 契约文件本身保留元信息

    argv = AgentCliAdapter(cli="ducc")._command("prompt", schema)
    passed = json.loads(argv[argv.index("--json-schema") + 1])
    assert "$schema" not in passed and "$id" not in passed
    # 约束本身逐字保留：剥掉的只是元信息
    for key in ("type", "required", "properties", "additionalProperties"):
        assert passed[key] == schema[key], key
