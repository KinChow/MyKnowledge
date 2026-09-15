# F001 Source 导入与归档验收

- Feature：F001
- 相关规范：SRC、ARC、SEC
- 状态：Implemented（2026-08-26；58/58 验收测试通过，含进程级崩溃注入与异常路径）
- 测试运行：`.venv/bin/python -m pytest tests/ -v`

## AC-F001-001 网络来源成功归档

- Given：URL 可访问且正文非空；
- When：执行 Source 导入（`SourceIngestor.ingest` 一次调用完成校验 → 采集 → 落盘）；
- Then：生成合法 Source、不可变 text snapshot 和 `snapshot_sha256`（若保留本地原件再记录 `file_sha256`）；
- 失败时不变量：不能生成无来源或无 hash 的可发布对象；
- 自动化级别：Integration。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_url_fetch_success_archives_with_origin_url`（正路径：source/snapshot/manifest 全部落盘且出处 URL 写入 `retrieval.url`/`resolved_url`）、`tests/ingest/test_source_ingestor.py::test_url_ingest_not_schema_blocked`
- 当前状态：通过。真实网络抓取由 AC-007/010 的策略测试覆盖。

## AC-F001-002 来源不完整时拒绝

- Given：URL 不可访问且没有 local-file 或 personal-note 兜底；
- When：执行导入；
- Then：操作失败且不产生半成品；
- 自动化级别：Integration。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_url_ingest_not_schema_blocked`（私网 URL → `fetch_blocked:private_network`）、`tests/ingest/test_source_ingestor.py::test_invalid_cross_fields_are_rejected`、`test_non_string_body_blocked`
- 当前状态：通过。导入失败不写半成品——`ingest` 的校验/采集阶段失败即结构化返回，无 operation 与确认态残留。

## AC-F001-003 raw 归档遵守 LFS 门禁

- Given：尝试写入 raw 快照；
- When：检查 `.gitattributes` 和 Git LFS；
- Then：规则生效才允许 raw，否则拒写或按契约降级 text-only，并记录原因；
- 自动化级别：Repository。
- 对应测试：无（当前无 raw 写入路径）
- 当前状态：待界定。当前实现只写 `archive/text`（metadata 硬编码 `archive_policy: text-only`），不存在 raw 写入路径，故无 LFS 门禁需求；raw 归档功能启用时随 archive_source 实现 `.gitattributes`/LFS 检测与降级原因记录。

## AC-F001-004 local-file HTML/PDF 统一入口

- Given：本地 HTML、PDF、代码或日志文件，可能带有已失效的原始 URL；
- When：通过 `tools.cli source --from-file` 执行 Source 导入；
- Then：Source 使用 `source_type: local-file`、`retrieval.acquisition: local-file`，记录 `file_sha256`、extractor/version、不可变 text snapshot 和 evidence selector；原 URL 仅作为历史出处；
- 失败时不变量：缺少文件 hash、snapshot 或 selector 时不得写入可发布 Source，文件变化不得覆盖旧 snapshot；
- 自动化级别：Integration。
- 对应测试：`tests/ingest/test_extractor.py::test_html_extraction_omits_active_content`、`tests/ingest/test_extractor.py::test_pdf_extraction`、`tests/ingest/test_extractor.py::test_extractor_register_open_for_extension`
- 当前状态：通过。`local.file_sha256`/`local.path_ref`/snapshot 写入由 `tests/ingest/test_source_ingestor.py::test_personal_note_ingest_and_anchor` 与 `validate_source_file` 校验；原 URL 历史出处经 `retrieval.url` 字段承载（AC-001 测试覆盖）。

## AC-F001-005 personal-note 也有权威 snapshot

- Given：用户创建 `origin: personal` 的 personal-note，正文非空但没有外部 URL；
- When：执行 Source 导入；
- Then：工具以 canonical note body 生成不可变 `archive/text` snapshot，写入 `retrieval.acquisition: personal-note`、`snapshot_sha256` 和可选 evidence item；
- 失败时不变量：不能用当前可变 Markdown 正文替代 snapshot，也不能把 personal-note 当成 external source；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_personal_note_ingest_and_anchor`
- 当前状态：通过（含 emoji/代码标点的锚定与 evidence 写回）。

## AC-F001-006 snapshot manifest 追加且 owner 可追溯

- Given：两个 Source 或两个 Vault 生成相同 `snapshot_sha256`，或同一 Source 后续生成新版本；
- When：更新 archive manifest 和 snapshot index；
- Then：物理内容可以去重，但每个 `(vault_id, source_id, snapshot_sha256)` 的 owner、路径、可用性和 hash 记录保留；旧 manifest 行不被原地覆盖；
- 失败时不变量：不能因去重丢失 owner、把新版本覆盖旧证据或仅凭 snapshot hash 绕过 Vault 权限；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_manifest_deduplicates_snapshot_keeps_owners`（相同内容 → archive 去重 1 个、manifest 2 行 owner 各自保留）、`tests/ingest/test_source_ingestor.py::test_manifest_corrupt_line_tolerated`、`tests/ingest/test_source_ingestor.py::test_manifest_invalid_utf8_tolerated`
- 当前状态：通过。

## AC-F001-007 URL 抓取防 SSRF 与大小边界

- Given：用户提供的 URL、redirect 链或 DNS 解析最终指向 loopback、RFC1918、link-local、`.local`/`.internal` 主机，或响应超过大小/时间/redirect 限制；
- When：执行 Source 导入；
- Then：操作返回 `fetch_blocked`，记录脱敏原因，不写入 source、snapshot、raw 或任何半成品；
- 失败时不变量：不能通过 redirect、DNS rebinding、Cookie 或嵌入凭据访问内网，也不能把响应正文/凭据写入日志；
- 自动化级别：Security/Integration。
- 对应测试：`tests/ingest/test_fetcher.py::test_url_policy_rejects_private_and_unsafe_targets`（file scheme、127.0.0.1）、`tests/ingest/test_fetcher.py::test_invalid_port_url_blocked`、`tests/ingest/test_source_ingestor.py::test_url_ingest_not_schema_blocked`
- 当前状态：通过。`tests/ingest/test_fetcher.py` 覆盖 redirect 链逐跳校验、`response_limit`、`max_redirects`、timeout 和连接关闭；`.local`/`.internal` 主机策略由 `test_local_domain_suffix_is_blocked_before_dns_resolution` 覆盖。

## AC-F001-008 local-file 读取稳定性

> 状态：部分退场（ADR-0019，2026-09-15）。本条原先钉的是"Preview 读取 → Apply 重读"之间的 TOCTOU 窗口（`test_local_file_hash_mismatch_blocks_apply`、`test_local_file_deleted_returns_path_unresolved`、`test_target_change_does_not_leave_snapshot`、`test_local_file_symlink_retarget_blocks_apply`）。ingest 收敛为一次调用后该窗口已不存在——采集与校验在同一遍读取内完成，未确认的中间态没有落盘位置。**存活的子断言**（稳定读、路径不可解析、落盘失败回滚、崩溃后幂等收敛）仍须通过，见下。

- Given：本地文件在单次采集读取期间被替换、改写、改名或删除，或路径已不可解析；
- When：执行 Source 导入；
- Then：采集阶段返回 `hash_mismatch`（`tools/common.read_stable` 的 stat 前后比对）或 `path_unresolved`（`FileNotFoundError` 映射），不写入 source 与 snapshot；
- 失败时不变量：读取必须是"稳定读"而非一次 `read_bytes`，不能把绝对路径写入 canonical/public artifact；落盘阶段任何 I/O 失败都必须回滚，且崩溃后重跑必须幂等收敛；
- 自动化级别：Security/Integration/Failure injection。
- 对应测试（存活子断言）：`tests/ingest/test_source_ingestor.py::test_ingest_failure_rolls_back_source`、`::test_ingest_failure_keeps_existing_source`、`::test_failure_at_the_last_write_rolls_back_the_new_source`、`::test_overwrite_failure_keeps_content_and_ledger_consistent`、`::test_failure_before_source_write_leaves_only_a_harmless_extra_record`（注入 `apply_failed` 后旧内容完好）、`::test_crash_injection_ingest_converges`（3 个落盘提交点 SIGKILL 后重跑收敛为 `applied` 且 manifest 单一账目）
- 当前状态：通过。绝对路径仅写入 `state/local-sources` sidecar（0600、被 git 忽略），不进 canonical/public artifact。`hash_mismatch`/`path_unresolved` 两个错误码仍由 `read_stable` 与 `_block_error_code` 产生，但**当前无直接用例钉住**（原用例随两阶段协议一并删除）——属未决项。

## AC-F001-009 Source acquisition 交叉字段

- Given：请求带 `input_path` 却声明为 `doc/blog`，或 `source_type: local-file` 缺少 `retrieval.acquisition: local-file`、`local.file_sha256`、`local-sidecar:` path ref 或 snapshot；personal note 声明为 external；
- When：执行 Source schema 校验与导入；
- Then：返回字段级 `schema_invalid`，不产生半成品；
- 失败时不变量：不能通过原始资料类型、可变当前文件或空 URL 绕过 local-file/personal-note snapshot 契约；
- 自动化级别：Unit/Security。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_invalid_cross_fields_are_rejected`；发布后文件校验由 `SourceValidator.validate_source_file` 提供（含 `local.file_sha256`/`path_ref`/`snapshot_sha256`/`retrieval.acquisition`）
- 当前状态：通过。

## AC-F001-010 URL scheme、DNS pinning 与解压上限

- Given：输入 URL 使用非 HTTP(S) scheme、包含 userinfo/非 80/443 端口、redirect 后解析到另一 IP，或压缩响应的解压大小/压缩比超出 policy；
- When：执行 Source 导入；
- Then：分别返回 `fetch_blocked`、`dns_rebinding_blocked` 或 `decompression_limit_exceeded`，连接只使用已检查并 pin 的 IP，Host/SNI 与 URL 一致；
- 失败时不变量：不能以重试、代理、编码路径或重定向绕过目标检查，也不能在归档前产生正文/raw/凭据半成品；
- 自动化级别：Security/Integration/Failure injection。
- 对应测试：`tests/ingest/test_fetcher.py::test_invalid_port_url_blocked`、`tests/ingest/test_fetcher.py::test_bounded_gzip_rejects_expansion`、`tests/ingest/test_fetcher.py::test_url_policy_rejects_private_and_unsafe_targets`
- 当前状态：通过。解析全部地址→任一私网即拒→连接直连已校验 IP，Host/SNI 使用原主机名；`test_dns_rebinding_is_reported_separately` 覆盖同 hostname IP 漂移，`test_userinfo_url_is_blocked` 覆盖凭据 URL。重定向到私网按 `private_network` 返回是预期的逐跳目标策略，不影响阻断结论。

## AC-F001-011 Evidence 锚定生成 selector 与 hash

- Given：某 source 已有归档 snapshot；用户在 snapshot 正文中选取一段包含 CJK、emoji 和代码标点的片段；
- When：执行 `evidence_anchor`（一次落盘，`EvidenceAnchor.anchor()` 纯计算 + `apply_evidence()` 幂等写回）；
- Then：生成 `TextQuoteSelector`（`exact` 逐字取自 snapshot，`prefix`/`suffix` 各取相邻 32 个 code point）和 `TextPositionSelector`（Unicode code-point 半开区间 `[start, end)`），计算 `selector_sha256` 与 `quote_sha256`，直接幂等写回 source 的 `evidence_items`；
- 失败时不变量：偏移量不得按 UTF-8 字节或 UTF-16 code unit 计算；`prefix`/`suffix` 不得单独作为匹配依据；工具不得改写归档 snapshot；锚定工具不得另取写锁或写 operation 记录（ADR-0019）；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_personal_note_ingest_and_anchor`（含 emoji 的 code-point 偏移断言）、`tests/anchor/test_evidence_anchor.py::test_anchor_does_not_touch_disk`（`anchor()` 为纯计算，不写盘）、`tests/anchor/test_evidence_anchor.py::test_anchor_evidence_writes_directly_without_operation_record`（直写且无 operation 记录）
- 当前状态：通过。原 `test_anchor_evidence_ttl_expires` / `test_anchor_lock_busy_returns_structured` 随 TTL 与 per-vault 锁退场一并删除（ADR-0019）——锚定不再有 TTL 与锁，故这两个断言已无对象。

## AC-F001-012 锚定的歧义、短引文与漂移

- Given：`exact` 分别为 snapshot 中未出现、多处出现且 prefix/suffix 无法消歧、短于 policy 最小长度，或所属 snapshot 已重新抓取产生新 `snapshot_sha256`；
- When：执行 `evidence_anchor`；
- Then：分别返回 `selector_unresolved`、`ambiguous_selector`（要求扩大选区）、长度拒绝、以及 `stale` 并要求在新 snapshot 上重新锚定；同一 `(source_id, snapshot_sha256, start, end)` 重复锚定返回既有 `evidence_id`；
- 失败时不变量：多处命中时不得自行选取第一个；snapshot 漂移后不得自动迁移偏移量；批量模式（`--from-jsonl`）不得降低唯一性与长度标准，未解析行必须进入 `unresolved` 报告；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/anchor/test_evidence_anchor.py::test_ambiguous_and_short_quotes`、`tests/anchor/test_evidence_anchor.py::test_anchor_selector_unresolved`、`tests/anchor/test_evidence_anchor.py::test_anchor_evidence_stale_when_snapshot_mismatches_source`、`tests/anchor/test_evidence_anchor.py::test_anchor_evidence_is_idempotent`
- 当前状态：通过。`--from-jsonl` 批量模式已实现（CLI 冒烟验证：ok 1 行 + unresolved 1 行，退出码 2）。

## AC-F001-013 锚定工具与验证器共用同一归一实现

- Given：同一 snapshot 与同一 selector；
- When：`evidence_anchor` 生成 `quote_sha256`，验证器独立重新计算 `quote_sha256`；
- Then：两个值必须相同；该一致性测试常驻 CI；
- 失败时不变量：工具侧不得另写一份 `canonical_quote()`；两份实现漂移时必须由该测试失败暴露，而不是等到引文匹配不上时才发现；
- 自动化级别：Unit。
- 对应测试：`tests/ingest/test_source_ingestor.py::test_personal_note_ingest_and_anchor`（`evidence["quote_sha256"] == SourceValidator.quote_sha256(...)` 常驻断言）
- 当前状态：通过。`canonical_quote()` 为 `tools/common.py` 单一实现；`SourceValidator.quote_sha256` 走独立调用路径重算，锚定与验证两条路径由断言锁死。

---

## 验收记录

- 测试：58/58 通过（2026-08-26，Python 3.14.2 / pytest 8.4.2；F001 37 + F002 18 + 守卫 3）
- 崩溃注入：source 落盘 3 个提交点（`after_archive`/`after_manifest`/`after_source`）真实 SIGKILL 后重跑 `ingest` 收敛为 `applied`，manifest 保持单一账目（幂等去重靠 `record_id` + 内容寻址快照）
- 人工验证：`--from-jsonl` 批量锚定 CLI 冒烟——ok 1 行（生成 evidence）+ unresolved 1 行（snapshot 缺失归入报告，退出码 2）
- 复核人：zhouzijian01
- 基线垂直切片：`tests/test_end_to_end.py::test_source_to_wiki_evidence_chain_is_replayable` 串联 Source 导入（一次调用）、snapshot、EvidenceAnchor selector、Wiki validation 和 evidence hash replay；原始输入与 canonical 事实链均可复核。
- 未决项（不影响 Implemented，阻却 Accepted）：
- AC-003：raw 归档/LFS 门禁随 raw 功能启用时落地；当前实现固定 text-only，无 raw 写入路径。

## URL redirect/response 门禁证据（2026-08-27）

## Append-only manifest 字段增量证据（2026-08-27）

- `tests/ingest/test_source_ingestor.py::SourceIngestorTests::test_personal_note_ingest_and_anchor` 直接断言 manifest 每行包含 `record_id`、owner ObjectRef、snapshot/archive/extractor、normalization、canonical length 和 `record_sha256`；重复导入仍只有一行。

- `tests/ingest/test_fetcher.py::FetcherTests::test_redirect_is_rechecked_and_response_limit_is_enforced` 验证 redirect 后逐跳重新解析，并在响应超过 `max_bytes` 时返回 `fetch_blocked:response_limit`。
- `test_redirect_limit_is_explicit` 验证超过 `max_redirects` 返回 `fetch_blocked:redirect_limit`；连接仍只使用通过公网 IP 校验的 pin。

## DNS rebinding/userinfo 增量证据（2026-08-27）

- `test_dns_rebinding_is_reported_separately` 验证同一 hostname 在 redirect 链中解析到不同 IP 时返回 `fetch_blocked:dns_rebinding_blocked`。
- `test_userinfo_url_is_blocked` 验证 URL 中包含 username/password 时返回 `fetch_blocked:url_policy`，不会建立连接。

## Timeout 增量证据（2026-08-27）

- `tests/ingest/test_fetcher.py::FetcherTests::test_request_timeout_is_structured_and_connection_is_closed` 注入连接超时，验证统一返回 `fetch_blocked:request_failed` 并执行连接关闭；不会生成响应正文或归档半成品。

## 本地域名策略增量证据（2026-08-27）

- `tests/ingest/test_fetcher.py::FetcherTests::test_local_domain_suffix_is_blocked_before_dns_resolution` 验证 `.internal`/`.local` 主机在 DNS 解析前返回 `fetch_blocked:host_policy`；不建立连接、不触发解析，降低内网名称探测风险。

## P0 垂直切片验收证据（2026-08-27）

- `tests/test_end_to_end.py::test_source_to_wiki_evidence_chain_is_replayable` 实际串联 Source 导入（一次落盘）、不可变 text snapshot、EvidenceAnchor selector/写回、Wiki claim/evidence validation 和 evidence hash replay，测试通过（1 passed）。
- 该报告证明 Source→Wiki→Claim→Evidence 的事实链可回放；public release 人工确认、projection 和静态发布仍需按 F007 独立门禁验收，不能由本测试单独推导为 `Accepted`。
