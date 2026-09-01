# ADR-0015：审计分歧取 fail，唯一推翻路径是留痕的人工复议

- 状态：Accepted
- 日期：2026-09-01
- 相关规范：§6.7（证据强度标识）、§6.8（派生字段与 strength 映射）、VAL-003、ARC-005
- 相关 Feature：F003

## 背景

F003 的 LLM 规范审计报告落在 `audit/validation/wiki/<id>/` 下，按内容 hash 绑定。原实现在同一 `(content_sha256, evidence_sha256)` 下有多份报告时**按 mtime 取最新**。

2026-09-01 在 `content/wiki/reading-notes/how-to-read-a-book.md` 上实测三条 provider 通路（OpenAI 兼容 API、ducc、ducx），暴露两个事实：

1. **不同 provider 对同一页给出相反结论**：一次 `pass`、一次 `fail`；
2. **同一 provider 对同一条 claim 两次判定不一致**（`supported` / `partially_supported`）。

在"取最新"的规则下，这意味着只要反复换 provider 或重跑，出现一次 `pass` 就能过门禁——门禁强度退化为"最后跑的模型说了算"，这是审计洗牌（audit shuffling）。同时也发现另一侧的风险：模型判定有随机性，一旦改成 fail 优先，**任何一次误判都能永久卡住一页**，而作者除了改内容之外没有任何出路，实际会导致规范被绕过（直接手改 status 或关掉审计）。

## 候选方案

- A. 保留"取最新"：零成本，但门禁可被重跑刷过，等于没有门禁。
- B. 多数表决（N 份报告取多数）：直觉上稳，但只是把刷票门槛从 1 次抬到 ⌈N/2⌉ 次，攻击面不变；且要求每次都跑满 N 个 provider，成本高、可用性差。
- C. 全部报告必须一致才 pass：最严，但两个模型天然有分歧，实际等于永久 `fail`，页面永远无法发布。
- D.（选定）**fail 优先 + owner 签署的人工复议出口**：分歧取更保守一侧；误判由人显式推翻，且推翻本身是 append-only 审计记录。

## 决策

1. **fail 优先**：绑定当前 hash 的多份 `validation-report/v1` 分歧时取 `fail`，不按时间取最新。要过门禁只能改内容，不能换模型。
2. **复议记录**：新增 `validation-override/v1`，落在 `audit/validation/wiki/<object_id>/overrides/<record_sha256>.json`（放子目录，避免被报告目录的顶层 glob 误读为报告）。记录声明"owner 读过这份 fail，判定它是误判"。
3. **复议的五条 fail-closed 约束**：
   - 只有 `actor_type: human` 能签，Agent 不得代签（与 ADR-0010 同一原则）；
   - `reason` 必填——没有理由的复议等于静默绕过；
   - `reviewed_claim_ids` 必须覆盖该报告里**全部**非 `supported` 的 claim，只复议一条不能整份翻案；
   - 绑定被复议报告的稳定标识与当前 `(content_sha256, evidence_sha256)`，内容一改复议自动失效；
   - `record_sha256` 自证，篡改即视为无效记录。
4. **复议后不自动 pass**：被复议的报告退出派生。若当前 hash 下**所有** verdict 报告都被复议掉，`validation_state` 回落 `not_run`，而不是变成 `pass`——`not_run` 同样不满足发布门禁，需要重新跑审计。
5. **不引入表决**：不做多数表决、不做 provider 权重、不区分"两个模型不一致"与"两个模型都 fail"。分歧的裁决权归人，不归计票规则。

## 后果

- 门禁不再可被重跑刷过：`validation_state: pass` 意味着"当前内容下没有任何未被复议的 fail 报告"。
- 误判有出路，但出路留痕：复议记录带 `actor_id`、理由、逐条 claim 与内容绑定，事后可审。
- 代价一：复议是逐报告的，同一页多份 fail 需要逐份复议。这是有意的——批量复议等于一键放行。
- 代价二：内容修改会同时失效旧报告与旧复议，改一个字就要重跑审计。这与 §6.4 的 hash 绑定语义一致，不额外让步。
- `strength` 的语义同步收紧（同日决策）：LLM `pass` 只证明转述忠实于所引原文，不证明原文正确，因此单一 source 页面上限为 `attested`，`verified` 只授予 ≥2 个独立 source 支撑的论断。

## 重新评估条件

- 出现可度量的审计稳定性指标（同一页多次重跑的判定方差），使"分歧"可以从随机性中区分出真实规则违反；
- 复议记录在实际使用中数量显著上升（说明模型误判率过高，应先换审计策略而不是继续签复议）；
- 引入多个具备独立责任主体的审计通路时，重新评估是否需要按通路加权而非一律 fail 优先。
