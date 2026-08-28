"""本地 API 的请求模型（F006）。

全部 ``extra="forbid"``：未知字段必须显式失败，不接受"被接受但被忽略"的入参。
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=4000)
    scope: str = "public"
    vault_ids: list[str] | None = None
    top_k: int = Field(default=8, ge=1, le=50)
    include_sources: bool = False
    include_archive: bool = False


class WritePreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    files: dict[str, str] = Field(min_length=1)
    vault_id: str = "public"


class ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirmed: bool = False
    actor_id: str = Field(default="local-user", min_length=1, max_length=128)
    confirmation: dict[str, Any] | None = None


class CitationReplayRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    citation: dict[str, Any]
    snapshot: str = Field(min_length=1, max_length=2_000_000)
