# Source 导入与归档实现设计

- 状态：Draft
- 相关 Feature：F001
- 相关规范：SRC、ARC、SEC
- 相关 ADR：ADR-0001、ADR-0003
- 相关验收：[F001](../acceptance/F001-source-ingestion.md)

## 目标与非目标

目标是实现 URL、local-file 和 personal-note 三类来源的统一导入、来源完备性校验、不可变 snapshot/evidence item 归档和 hash 生成。Private Vault 使用同一导入器，但由 vault registry 决定落盘位置；本设计不复制第二套 source schema。

## 模块边界

- `source_parser`：解析输入和 front matter；
- `archive_source`：抓取、不可变 snapshot、压缩和 hash；
- `evidence_builder`：从 snapshot 生成 TextQuote/TextPosition selector，并记录 extractor/normalization 版本；
- `vault_registry`：从 `public + 0..N` 个 vault 中解析明确的 target `vault_id`，阻止 internal 写入允许 public projection 的 vault，并返回逐 vault 可用性/备份状态；
- `source_validator`：确定性规则校验；
- `operation_store`：保存 preview/apply 状态。

## Canonical 数据契约

`archive/text` 的**逻辑内容**是 canonical、未压缩文本；物理存储可以按 policy 写成确定性的 zstd blob（例如 `.md.zst`）。`snapshot_sha256` 永远对解压后的 canonical 文本 UTF-8 字节计算，压缩格式只影响存储，不影响证据身份；resolver 在返回 snapshot 前必须解压并重新校验该 hash。`TextPositionSelector` 使用 canonical 文本的 Unicode code-point 半开区间，`normalization_version` 必须随 manifest 和 selector 保存。`local-file` 的原始路径只留在本机/private manifest，不能进入 public artifact。每个 snapshot 的逻辑引用是 `(vault_id, snapshot_sha256)`；相同 hash 可以共享物理 blob，但不能省略 owner 记录或仅凭 hash 跨 Vault 读取。

`archive/manifest.jsonl` 是 append-only，每行至少包含 `record_id`、`vault_id`、`owner_object_ref`（source ObjectRef）、`snapshot_sha256`、`archive_path`、`physical_blob_key`、`availability`/`availability_reason`、confidentiality、媒体类型、提取器/版本/options hash、normalization version、canonical byte length、compression name/version、raw hash（如有）和 `record_sha256`。`record_id` 使用 `sha256(canonical_json({vault_id, owner_object_ref, snapshot_sha256, extractor, extractor_version, normalization_version}))` 的完整值或稳定前缀，重复导入同一版本必须幂等。物理 blob 可按 hash 去重，但 owner record、备份清单和权限永远不合并；workspace shared blob cache 只是派生缓存，不能成为唯一备份。压缩器必须固定版本和确定性参数；恢复时先解压、重新计算 canonical snapshot hash，再允许 resolver 返回内容。`canonical byte length` 指解压后的逻辑文本长度，另可记录物理 blob length，不能用压缩后长度替代证据边界。

```python
class SourceIngestor(Protocol):
    def preview(self, request: SourceRequest) -> SourcePreview: ...
    def apply(self, operation_id: str, confirmation: Confirmation) -> ApplyResult: ...

class SourceRequest(TypedDict):
    target_vault: str
    source_type: Literal["blog", "doc", "book", "contest", "pr", "local-file", "personal-note"]
    input_path: str | None
    url: str | None
    original_type: str | None       # optional provenance for a local copy
    read_range: str | None          # provenance only; never an evidence selector

# `source_type: personal-note` uses `retrieval.acquisition: personal-note` and
# snapshots the canonical note body before Apply; it is not an unarchived bypass.
```

Preview 必须返回 `operation_id`、target Vault、input/file hash、`snapshot_sha256`、extractor/version/options hash、normalization version、evidence item 数量、network requirement 和阻断原因；Apply 重新读取并比较这些 preconditions。`snapshot_sha256` 始终指向 canonical 未压缩文本，不使用 `text_sha256` 作为第二个权威字段。

## 流程与失败处理

解析来源 → 判断 `fetch`/`local-file`/`personal-note` → 获取或读取正文 → 保存不可变 text snapshot → 按需保存 raw → 生成 evidence item/selector → 计算 hash → schema 校验 → 生成 Preview。输入是本机路径时强制 `source_type: local-file`；原始网页类型只能写入 provenance。

抓取失败、来源不完整、selector 无法绑定、vault 不可用、raw 超过 `raw_max_bytes` 或 raw 的 LFS 前置检查失败时，不得产生可发布 Source；允许的 text-only 降级必须记录原因，且不影响 snapshot 作为权威证据载体。`personal-note` 也必须从 canonical note body 生成 snapshot；它可以离线，但不能用可变 Markdown 正文替代快照。

### 网络抓取安全

URL 抓取只接受用户明确给出的单个 URL，且只允许 `http`/`https`、端口 `80/443`、无 userinfo。解析 URL、建立连接和处理每一次 redirect 时都必须重新解析 DNS/IP，并拒绝 loopback、RFC1918、link-local、IPv6 本地地址、`.local`/`.internal` 等内网目标；DNS 解析结果必须在本次连接中 pin 到已检查的 IP，同时保留原 Host/SNI，不能在连接后再次解析到另一地址。连接失败或重试时重新执行检查；不能用一个公共首跳 URL 绕过 redirect 或 DNS rebinding 检查。请求设置固定超时、最大响应字节数和最大 redirect 次数，解压后字节数和压缩比也有独立上限，拒绝异常 content-encoding，防止压缩炸弹。禁用凭据嵌入、Cookie、自动表单提交、脚本执行和站点爬取。响应头中的 `Set-Cookie`、Authorization、会话 token 和请求凭据不得进入 raw、manifest 或日志；抓取器需在归档前执行一次 secret/header 清理检查。任何 SSRF/大小/解压/超时命中都返回 `fetch_blocked`、`dns_rebinding_blocked` 或 `decompression_limit_exceeded`，不写入半成品。

### 本地文件一致性与竞态

local-file preview/apply 必须在同一次读取中记录 `file_sha256`、字节数、设备/inode（仅本机 precondition）和读取开始/结束时间；Apply 重新打开并重新计算 hash，发现文件替换、大小或 hash 变化即 `hash_mismatch`，不能继续使用 preview 结果。读取前后都要检查 realpath、symlink 和 hard-link 是否仍在允许范围内；不把用户提供的路径直接拼接进 archive 路径。sidecar 只保存 `vault_id + source_id` 到本机绝对路径的映射，canonical Source 只保留 `path_ref`（以 `local-sidecar:` 开头）、hash、媒体类型和读取范围。若 `input_path` 存在，`source_type` 必须是 `local-file`；不能用 `doc`/`blog` 等原始类型绕过统一入口。

### Local-file sidecar 契约

sidecar 是本机解析层，不是 Source 的第二个事实源。默认写入被忽略的 `state/local-sources/<vault_id>/<source_id>.json`，结构固定为：

```json
{
  "schema_version": "local-file-sidecar/v1",
  "vault_id": "public",
  "source_id": "source-llvm-loop-vectorize-pass",
  "path": "/absolute/path/known-only-to-this-machine",
  "realpath_sha256": "sha256:...",
  "device": 16777221,
  "inode": 12345,
  "file_sha256": "sha256:...",
  "byte_size": 412355,
  "media_type": "text/x-c++src",
  "observed_at": "2026-08-26T00:00:00Z"
}
```

sidecar 文件和父目录必须由当前用户拥有、不可被 symlink 替换，文件权限为 `0600`（目录 `0700`）；加载时校验 schema、`vault_id/source_id`、路径 realpath、device/inode、大小和 hash，任一不匹配返回 `path_unresolved`/`hash_mismatch`。sidecar 内容绝不进入 Git、共享 audit、日志、QueryResult 或 public leak-gate 输入；跨机器迁移只能重新绑定路径并重新 Preview，不能复制绝对路径或复用旧 inode precondition。Apply 使用“打开后 stat -> 读取 -> 再 stat/realpath -> hash”顺序，竞态时丢弃本次读取并保留旧 snapshot。

## 测试策略

覆盖 URL、local-file HTML/PDF/代码/日志、personal-note、抓取失败、重复导入、空正文、locator、Unicode offset/hash 稳定性、raw LFS 检查、多个 Vault 的明确 target、单 Vault unavailable 隔离和跨 Vault 同 snapshot 去重；增加文件 hash 变化不覆盖旧 snapshot 的回归。

## 离线 HTML/PDF 入口

离线 HTML、PDF 和其他本机已有副本统一通过 `local-file` source 导入。`local-file.path` 只存在于本机/private manifest，Source 保存 `file_sha256`、媒体类型、导入时间和不可变 `archive/text` snapshot；原始 URL（如有）只作为历史出处。PDF/HTML 的抽取器名称、版本、选项 hash 和页码/DOM 定位写入 snapshot manifest，selector 绑定 snapshot 而不是当前文件路径。`read_range`/页码/DOM 坐标只作 provenance，不能替代 TextQuote/TextPosition selector。文件 hash 变化时生成新 snapshot，不覆盖旧版本。抽取器升级只产生新 snapshot 和新 manifest owner，不修改旧 selector；规范化匹配必须保留 canonical code-point 到 normalized-text 的 offset map，避免 NFKC/空白折叠后无法回到权威范围。

对扫描 PDF 或 OCR 输出，若抽取器无法提供稳定文本和页级 provenance，Source 必须保持 `read_status: partial` 或 `evidence_status: metadata-only`，不能把 OCR 低置信度文本自动当作权威 claim 证据；人工确认后仍以归档的 canonical text snapshot 和 selector 为准。原始 PDF 的页码、区域框和 OCR 置信度可作为补充元数据，但不改变 snapshot/hash 规则。

该通道允许离线 apply，但仍必须经过 source schema、snapshot、evidence selector 和 hash 校验；`url_status: unknown` 不代表证据缺失。
