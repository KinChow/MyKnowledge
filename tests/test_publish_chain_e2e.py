"""发布链端到端验收：从干净页面走到 `public_release: true`（Task 8.0 的回归锁）。

为什么必须有这条测试（2026-09-01 实测教训）：12 个 Feature、408 个单测全绿，
但整条发布链**从来没有人从头走到尾**——`release input` 的判据曾是
`public_publishable`，而该字段本身要求发布确认事件已存在，形成
「算不出待审材料 → 签不了确认 → 算不出待审材料」的循环。历史上唯一"成功
发布过"的那份确认事件是手工编造的，编造动机正是这个循环。

单测没能发现它，因为每个测试为了跳过人工签名，都**直接注入一份现成的确认
事件**作为 fixture——而那一步恰恰是真实链路走不到的地方。所以这条测试的
纪律是：

- **可以 mock 的**：LLM provider（外部服务）与签名者身份（`actor_id` 用测试账号）；
- **不可以 mock 的**：任何一步的**产物**。每份记录都必须由真实命令写出，
  顺序也必须是真实顺序。mock 掉产物就等于把顺序约束一起 mock 掉。

leak gate 报告 hash 在此按 node 脚本的确定性输出字节计算（该脚本不落盘，
projection 侧目前也不重算——这是已记录的开放缺口，不在本测试范围内）。
"""

from __future__ import annotations

import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path

from wiki_fixtures import WIKI_BODY, _install_spec_doc

from tools.cli import release_main
from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.public_projection import PublicProjectionGenerator
from tools.validation.audit import run_audit
from tools.validation.confirm import main as confirm_main
from tools.validation.provider import ProviderResult, build_input_hash

QUOTE = "端到端发布链的可验证引文片段。"
SOURCE_ID = "e2e-release-source"
WIKI_ID = "e2e-release-wiki"
ACTOR = "e2e-owner"
# node scripts/leak-gate.mjs --scope input-tree 的确定性输出（findings 为空时）
LEAK_GATE_REPORT = '{"schema_version":"public-input-leak-gate/v1","scope":"input-tree","findings":[]}\n'


class PassProvider:
    """只 mock LLM 这一个外部服务：固定返回全 supported 的合法输出。"""

    def __init__(self, evidence_id: str) -> None:
        self.evidence_id = evidence_id

    def audit(self, request: dict, response_schema: dict) -> ProviderResult:
        """固定返回全 supported 的合法审计输出（只 mock 外部 LLM 这一层）。"""
        payload = {
            "wiki_id": WIKI_ID,
            "verdict": "pass",
            "call_id": "call_e2e",
            "claims": [
                {
                    "claim_id": "e2e-claim",
                    "verdict": "supported",
                    "targets": [
                        {"source_id": SOURCE_ID, "evidence_id": self.evidence_id}
                    ],
                    "supporting_quotes": [
                        {"evidence_id": self.evidence_id, "exact": QUOTE}
                    ],
                    "applied_rule_refs": ["VAL-001"],
                    "rationale": "引文逐字支撑该 claim。",
                    "rationale_offsets": [
                        {
                            "source_id": SOURCE_ID,
                            "evidence_id": self.evidence_id,
                            "start": 0,
                            "end": len(QUOTE),
                        }
                    ],
                }
            ],
        }
        return ProviderResult(
            "e2e-fake", "call_e2e", build_input_hash(request), payload=payload
        )


def _capture(fn, argv: list[str]) -> dict:
    """跑真实 CLI main 并解析它打印的 JSON（不 mock 编排层）。"""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        exit_code = fn(argv)
    assert exit_code == 0, buffer.getvalue()
    return json.loads(buffer.getvalue())


def _ingest_and_anchor(root: Path) -> str:
    body = f"来源正文开头。{QUOTE}来源正文结尾。"
    source_input = root / "incoming.md"
    source_input.write_text(body, encoding="utf-8")
    ingestor = SourceIngestor(root)
    preview = ingestor.preview(
        {
            "source_type": "local-file",
            "input_path": str(source_input),
            "domain": "tools",
            "source_id": SOURCE_ID,
            "media_type": "text/markdown",
        }
    )
    assert preview["state"] == "previewed", preview
    applied = ingestor.apply(preview["operation_id"], confirmed=True, actor_id=ACTOR)
    assert applied["state"] == "applied", applied

    source_path = root / "content" / "sources" / "tools" / f"{SOURCE_ID}.md"
    snapshot = (
        root
        / "archive"
        / "text"
        / f"{applied['snapshot_sha256'].removeprefix('sha256:')}.md"
    )
    anchor = EvidenceAnchor(root)
    previewed = anchor.preview(source_path, snapshot, QUOTE, min_chars=12)
    assert previewed["state"] == "previewed", previewed
    anchored = anchor.apply(previewed["operation_id"], confirmed=True)
    assert anchored["state"] == "applied", anchored
    metadata, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
    return str(metadata["evidence_items"][0]["evidence_id"])


def _write_published_wiki(root: Path, evidence_id: str) -> Path:
    path = root / "content" / "wiki" / "tools" / f"{WIKI_ID}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": "wiki/v1",
        "id": WIKI_ID,
        "title": "端到端发布链",
        "domain": "tools",
        "kind": "knowledge",
        "status": "published",
        "publication_scope": "public",
        "confidentiality": "public",
        "tags": ["e2e"],
        "aliases": [],
        "related": [],
        "sources": [SOURCE_ID],
        "updated_at": "2026-09-01",
        "evidence": [
            {
                "claim_id": "e2e-claim",
                "claim": "发布链可以从干净页面走到 public_release。",
                "targets": [{"source_id": SOURCE_ID, "evidence_id": evidence_id}],
                "support": "direct",
                "supporting_quotes": [{"evidence_id": evidence_id, "exact": QUOTE}],
            }
        ],
    }
    path.write_text(FrontMatter.render(metadata, WIKI_BODY), encoding="utf-8")
    return path


def _publish_operation_id(root: Path) -> str:
    """从真实 operation 记录里取 publish_wiki 的 id（不自造 operation_id）。"""
    for candidate in sorted((root / "audit" / "operations").glob("*.json")):
        record = json.loads(candidate.read_text(encoding="utf-8"))
        if record.get("operation_type") == "publish_wiki":
            return str(record["operation_id"])
    raise AssertionError("publish_wiki operation 记录不存在")


def test_publish_chain_runs_from_clean_page_to_public_release(tmp_path: Path):
    """发布链全流程回归锁：干净页面走到 public release 只 mock LLM 这一层。"""
    _install_spec_doc(tmp_path)
    evidence_id = _ingest_and_anchor(tmp_path)
    wiki = _write_published_wiki(tmp_path, evidence_id)

    # ① LLM 审计：唯一被 mock 的外部服务
    audited = run_audit(tmp_path, wiki, PassProvider(evidence_id))
    assert audited["validation_state"] == "pass", audited

    # ② 人工审计确认：真实 CLI main，只有签名者身份是测试账号
    confirmed = _capture(
        confirm_main,
        [
            "--root",
            str(tmp_path),
            "--actor-id",
            ACTOR,
            "--decision",
            "approve",
            str(wiki),
        ],
    )
    assert confirmed["decision"] == "approve", confirmed
    operation_id = _publish_operation_id(tmp_path)

    # ③ 待审材料必须能在发布确认签署之前算出来（本测试存在的理由：
    #    判据曾是 public_publishable，导致这一步永远 blocked）
    material = _capture(
        release_main,
        [
            "input",
            "--root",
            str(tmp_path),
            "--object-id",
            WIKI_ID,
            "--operation-id",
            operation_id,
        ],
    )
    assert material["release_input_sha256"].startswith("sha256:"), material
    assert material["material"]["route"] == f"/wiki/{WIKI_ID}"

    # ④ 人工发布确认：真实写入器 + 真实 leak gate 报告字节
    leak_gate_sha256 = (
        "sha256:" + hashlib.sha256(LEAK_GATE_REPORT.encode("utf-8")).hexdigest()
    )
    event = _capture(
        release_main,
        [
            "confirm",
            "--root",
            str(tmp_path),
            "--object-id",
            WIKI_ID,
            "--operation-id",
            operation_id,
            "--actor-id",
            ACTOR,
            "--reason",
            "end to end release chain check",
            "--event-id",
            "evt-e2e-release",
            "--nonce",
            "e2enonce0123456789abcdef",
            "--leak-gate-report-sha256",
            leak_gate_sha256,
        ],
    )
    assert event["state"] == "created", event

    # ⑤ projection 独立重算 release_input 并比对 7 项 → public_release 派生为 true
    result = PublicProjectionGenerator(tmp_path).generate()
    assert result["item_count"] == 1, result
    manifest = json.loads(
        (tmp_path / "var" / "queries" / "public" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    item = manifest["items"][0]
    assert item["id"] == WIKI_ID
    assert item["public_release"] is True, item
    assert item["release_input_sha256"] == material["release_input_sha256"]
    assert item["leak_gate_report_sha256"] == leak_gate_sha256
    assert item["strength"] == "attested"  # 单一 source：pass 也只到 attested
