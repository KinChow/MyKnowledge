# 证据锚定实现设计（anchor_evidence）

- 状态：Draft
- 相关 Feature：F001、F003
- 相关规范：SRC、ARC、EVD
- 相关 ADR：ADR-0003、ADR-0005
- 相关验收：[F001](../acceptance/F001-source-ingestion.md)、[F003](../acceptance/F003-evidence-validation.md)

## 为什么需要这个工具

主规范 §5.1 要求 source 携带 `evidence_items`，§6.4 要求每条 claim 的 target 指向一个已解析的 evidence item，§6.9 要求 `supporting_quotes.exact` 能在 selector 范围内逐字匹配。这三条都假设「selector 已经存在」，但整套设计里没有任何一处说明 selector 是怎么产生的。

手写不可行：`TextPositionSelector` 是 Unicode code-point 半开区间，人不可能数出正确的 `[start, end)`；`selector_sha256` / `quote_sha256` 也无法手算。缺了这个入口，claim 级证据在实践上不可写——这既是当前设计的最大缺口，也是全部存量迁移工作量的主项。

## 目标与非目标

目标是把「我在这篇归档正文里看到了这段话」变成一条可校验、可失效、可重放的 evidence item。

非目标：不做 claim 抽取、不做语义判断、不联网、不修改 wiki。它只在 source 侧生成锚点；claim 与 target 的绑定由 `create_wiki.py` 完成。

## 数据流

```text
source_id + evidence_id（可选，缺省自动分配）
  -> 从 archive/manifest.jsonl 解析 (vault_id, snapshot_sha256)
  -> 解压读取 archive/text/<sha>.md.zst，得到 canonical snapshot 文本
  -> 交互式定位候选片段（--query 关键字 / --range 行号 / stdin 粘贴）
  -> 用户确认唯一片段
  -> 生成 TextQuoteSelector + TextPositionSelector
  -> 计算 selector_sha256 / quote_sha256
  -> preview：输出待写入的 evidence item 与 diff，不改工作树
  -> apply：经 operation 协议写回 source 的 evidence_items
```

工具**只读** snapshot，永不改写归档；snapshot 是不可变内容寻址对象。

## Selector 生成规则

`TextPositionSelector` 的 `start`/`end` 是 canonical snapshot 文本上的 Unicode code-point 半开区间。计算必须在解码后的字符串上进行，不能用 UTF-8 字节偏移，也不能用 UTF-16 code unit（否则 emoji、CJK 扩展区字符会算错）。

`TextQuoteSelector` 同时生成 `exact`、`prefix`、`suffix`：

- `exact` 是用户确认的片段原文，逐字取自 snapshot，不做任何规范化后再写回；
- `prefix` / `suffix` 各取相邻 32 个 code point（不足则取到边界），只用于 snapshot 轻微变动后恢复位置，**不能单独作为匹配依据**；
- 若 `exact` 在 snapshot 中出现多次且 `prefix`/`suffix` 仍无法唯一确定，返回 `ambiguous_selector`，要求用户扩大选区，不允许工具自行选第一个。

最小长度门槛来自 policy（`normalization` / `granularity` 段）。过短引文（例如单个标识符）会大量误匹配，直接拒绝并提示扩大选区。

## Hash 契约

- `quote_sha256`：对 `canonical_quote(exact)` 的结果取 sha256。使用与验证器**同一个** `canonical_quote()` 实现（NFKC → 全角标点归一 → markup projection → 空白折叠，保留大小写与数字），不得在工具侧另写一份归一逻辑——两份实现必然漂移，而漂移的表现是「工具生成的引文验证器匹配不上」。
- `selector_sha256`：对 `{snapshot_sha256, start, end, exact, prefix, suffix}` 的 canonical JSON 取 sha256。
- 两个 hash 连同 `snapshot_sha256` 写入 evidence item，构成 §6.6 失效规则的绑定三元组。

snapshot 漂移（重新抓取产生新 `snapshot_sha256`）后，旧 evidence item 不自动迁移：工具报告 `stale`，要求在新 snapshot 上重新锚定。自动迁移偏移量是不安全的——原文可能已经改写了这段话。

## 与写入协议的关系

写回 source 走 §9 的 preview/apply 两阶段与 per-vault 排他锁，和 `create_source.py` 完全一致：preview 不改工作树、apply 原子写入并记录 operation record。它不是「小改动所以可以直接写文件」的例外。

同一 `(source_id, snapshot_sha256, start, end)` 重复锚定时返回既有 `evidence_id`，不产生重复条目。

## 交互与批量

交互模式是主用途：`--query` 给关键字，工具列出带上下文的候选，用户选序号确认。

批量模式（`--from-jsonl`）用于迁移：输入每行 `{source_id, exact}`，工具逐条定位，唯一命中即生成，歧义或未命中的行进入 `unresolved` 报告供人工处理。批量模式不降低任何校验标准——它只是省掉逐条敲命令，不省掉唯一性判定。

## 失败处理

| 情况 | 行为 |
| --- | --- |
| source 不存在或无归档 snapshot | 拒绝，提示先 `archive_source.py` |
| snapshot 解压失败或 hash 不匹配 | `snapshot_hash_mismatch`，不写入 |
| `exact` 在 snapshot 中找不到 | `selector_unresolved`，提示引文可能来自别的来源 |
| `exact` 多处命中且无法消歧 | `ambiguous_selector`，要求扩大选区 |
| 引文短于 policy 最小长度 | 拒绝，要求扩大选区 |
| 目标 vault 不可用 | `vault_unavailable`，不写入 |

## 测试策略

覆盖：CJK 与 emoji 的 code-point 偏移正确性、`exact` 唯一/多重命中/未命中、prefix/suffix 恢复、短引文拒绝、跨段落选区、代码块内选区（标点与空白不得被归一掉）、snapshot 漂移后报 `stale`、重复锚定幂等、批量模式的 `unresolved` 报告完整性。

关键一致性测试：本工具生成的 `quote_sha256` 与验证器对同一 snapshot/selector 独立算出的值必须相同。这条测试是防止两份归一实现漂移的唯一保障，必须在 CI 中常驻。
