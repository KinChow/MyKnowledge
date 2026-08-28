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
