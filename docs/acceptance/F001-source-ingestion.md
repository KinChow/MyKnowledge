# F001 Source 导入与归档验收

- Feature：F001
- 相关规范：SRC、ARC、SEC
- 状态：Not Implemented

## AC-F001-001 网络来源成功归档

- Given：URL 可访问且正文非空；
- When：执行 Source Preview；
- Then：生成合法 Source、不可变 text snapshot 和 `snapshot_sha256`（若保留本地原件再记录 `file_sha256`）；
- 失败时不变量：不能生成无来源或无 hash 的可发布对象；
- 自动化级别：Integration。

## AC-F001-002 来源不完整时拒绝

- Given：URL 不可访问且没有 local-file 或 personal-note 兜底；
- When：执行导入；
- Then：操作失败且不产生半成品；
- 自动化级别：Integration。

## AC-F001-003 raw 归档遵守 LFS 门禁

- Given：尝试写入 raw 快照；
- When：检查 `.gitattributes` 和 Git LFS；
- Then：规则生效才允许 raw，否则拒写或按契约降级 text-only，并记录原因；
- 自动化级别：Repository。

## AC-F001-004 local-file HTML/PDF 统一入口

- Given：本地 HTML、PDF、代码或日志文件，可能带有已失效的原始 URL；
- When：通过 `archive_source.py --from-file` 执行 Source Preview/Apply；
- Then：Source 使用 `source_type: local-file`、`retrieval.acquisition: local-file`，记录 `file_sha256`、extractor/version、不可变 text snapshot 和 evidence selector；原 URL 仅作为历史出处；
- 失败时不变量：缺少文件 hash、snapshot 或 selector 时不得写入可发布 Source，文件变化不得覆盖旧 snapshot；
- 自动化级别：Integration。

## AC-F001-005 personal-note 也有权威 snapshot

- Given：用户创建 `origin: personal` 的 personal-note，正文非空但没有外部 URL；
- When：执行 Source Preview/Apply；
- Then：工具以 canonical note body 生成不可变 `archive/text` snapshot，写入 `retrieval.acquisition: personal-note`、`snapshot_sha256` 和可选 evidence item；
- 失败时不变量：不能用当前可变 Markdown 正文替代 snapshot，也不能把 personal-note 当成 external source；
- 自动化级别：Unit/Integration。

## AC-F001-006 snapshot manifest 追加且 owner 可追溯

- Given：两个 Source 或两个 Vault 生成相同 `snapshot_sha256`，或同一 Source 后续生成新版本；
- When：更新 archive manifest 和 snapshot index；
- Then：物理内容可以去重，但每个 `(vault_id, source_id, snapshot_sha256)` 的 owner、路径、可用性和 hash 记录保留；旧 manifest 行不被原地覆盖；
- 失败时不变量：不能因去重丢失 owner、把新版本覆盖旧证据或仅凭 snapshot hash 绕过 Vault 权限；
- 自动化级别：Unit/Integration。

## AC-F001-007 URL 抓取防 SSRF 与大小边界

- Given：用户提供的 URL、redirect 链或 DNS 解析最终指向 loopback、RFC1918、link-local、`.local`/`.internal` 主机，或响应超过大小/时间/redirect 限制；
- When：执行 Source Preview/Apply；
- Then：操作返回 `fetch_blocked`，记录脱敏原因，不写入 source、snapshot、raw 或 operation 半成品；
- 失败时不变量：不能通过 redirect、DNS rebinding、Cookie 或嵌入凭据访问内网，也不能把响应正文/凭据写入日志；
- 自动化级别：Security/Integration。

## AC-F001-008 local-file 读取竞态

- Given：Preview 后本地文件被替换、改写、改名，或通过 symlink/hard-link 指向允许根目录之外；
- When：执行 Apply；
- Then：重新计算 hash 后返回 `hash_mismatch` 或 `path_unresolved`，旧 snapshot 保持不变且不写入新 Source；
- 失败时不变量：不能使用 preview 读取的旧/未知内容继续 Apply，不能把绝对路径写入 canonical/public artifact；
- 自动化级别：Security/Integration/Failure injection。

## AC-F001-009 Source acquisition 交叉字段

- Given：请求带 `input_path` 却声明为 `doc/blog`，或 `source_type: local-file` 缺少 `retrieval.acquisition: local-file`、`local.file_sha256`、`local-sidecar:` path ref 或 snapshot；personal note 声明为 external；
- When：执行 Source schema/preview；
- Then：返回字段级 `schema_invalid`，不创建 operation 或半成品；
- 失败时不变量：不能通过原始资料类型、可变当前文件或空 URL 绕过 local-file/personal-note snapshot 契约；
- 自动化级别：Unit/Security。

## AC-F001-010 URL scheme、DNS pinning 与解压上限

- Given：输入 URL 使用非 HTTP(S) scheme、包含 userinfo/非 80/443 端口、redirect 后解析到另一 IP，或压缩响应的解压大小/压缩比超出 policy；
- When：执行 Source Preview/Apply；
- Then：分别返回 `fetch_blocked`、`dns_rebinding_blocked` 或 `decompression_limit_exceeded`，连接只使用已检查并 pin 的 IP，Host/SNI 与 URL 一致；
- 失败时不变量：不能以重试、代理、编码路径或重定向绕过目标检查，也不能在归档前产生正文/raw/凭据半成品；
- 自动化级别：Security/Integration/Failure injection。

## AC-F001-011 Evidence 锚定生成 selector 与 hash

- Given：某 source 已有归档 snapshot；用户在 snapshot 正文中选取一段包含 CJK、emoji 和代码标点的片段；
- When：执行 `anchor_evidence` preview/apply；
- Then：生成 `TextQuoteSelector`（`exact` 逐字取自 snapshot，`prefix`/`suffix` 各取相邻 32 个 code point）和 `TextPositionSelector`（Unicode code-point 半开区间 `[start, end)`），计算 `selector_sha256` 与 `quote_sha256`，经 preview/apply 与 per-vault 写锁写回 source 的 `evidence_items`；
- 失败时不变量：偏移量不得按 UTF-8 字节或 UTF-16 code unit 计算；`prefix`/`suffix` 不得单独作为匹配依据；工具不得改写归档 snapshot；不得绕过 preview/apply 直接写文件；
- 自动化级别：Unit/Integration。

## AC-F001-012 锚定的歧义、短引文与漂移

- Given：`exact` 分别为 snapshot 中未出现、多处出现且 prefix/suffix 无法消歧、短于 policy 最小长度，或所属 snapshot 已重新抓取产生新 `snapshot_sha256`；
- When：执行 `anchor_evidence`；
- Then：分别返回 `selector_unresolved`、`ambiguous_selector`（要求扩大选区）、长度拒绝、以及 `stale` 并要求在新 snapshot 上重新锚定；同一 `(source_id, snapshot_sha256, start, end)` 重复锚定返回既有 `evidence_id`；
- 失败时不变量：多处命中时不得自行选取第一个；snapshot 漂移后不得自动迁移偏移量；批量模式（`--from-jsonl`）不得降低唯一性与长度标准，未解析行必须进入 `unresolved` 报告；
- 自动化级别：Unit/Integration。

## AC-F001-013 锚定工具与验证器共用同一归一实现

- Given：同一 snapshot 与同一 selector；
- When：`anchor_evidence` 生成 `quote_sha256`，验证器独立重新计算 `quote_sha256`；
- Then：两个值必须相同；该一致性测试常驻 CI；
- 失败时不变量：工具侧不得另写一份 `canonical_quote()`；两份实现漂移时必须由该测试失败暴露，而不是等到引文匹配不上时才发现；
- 自动化级别：Unit。
