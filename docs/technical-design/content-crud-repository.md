# 内容 CRUD：Repository 契约 + 各实体实现（实现 ADR-0017 能力层）

- 状态：Draft
- 相关 Feature：F001、F002、F008、F011
- 相关 ADR：ADR-0017（内容实体模型 = 共享 metadata + 统一动词 + 能力接口探测，本设计是其“如何实现”）、ADR-0011（入口层消费共享 domain service）、ADR-0019（git 作为审批）、ADR-0020（晋升是转换作业）、ADR-0021（porcelain 人用入口）
- 相关验收：[F001](../acceptance/F001-source-ingestion.md)、[F002](../acceptance/F002-wiki-contract.md)、[F008](../acceptance/F008-question-practice.md)

## 1. 目标与非目标

### 目标

- 把 `sources` / `wiki` / `questions` 三类对象的**增删改查**收敛为「统一契约 + 各自实现」：查（Read/List）、删（Delete）机制、写原语共享一份；增（Create）、改（Update/生命周期）各实体保留领域实现。
- 消除 `source` 读取的 4 份不一致实现，补齐 `source` 缺失的删除与安全更新。
- **优先复用成熟模式与已有库，不自研持久化框架、不引入数据库/ORM**（保持“Markdown/JSON 文件即事实源、projection/索引可重建”的设计根基）。

### 非目标

- 不给 `working` 层建对象级 CRUD（§4.5/LAY-002：unmanaged、无 object 身份；见 §11）。
- 不改变 `create` 的门禁强度：`source` 仍走采集流水线、`wiki` 仍走通道 A（校验→审计→确认→release）。
- 不实现 ADR-0017 的 `claim` 一等对象化与 CAS 存储去重（属独立工作项，本设计不依赖也不阻塞它）。

## 2. 成熟方案复用边界（不自研）

| 关注点 | 采用的成熟模式/库 | 出处 | 替代掉的自研 |
| --- | --- | --- | --- |
| 统一契约 + 各自实现 | **Repository 模式**（集合式接口中介领域层与存储层） | Fowler PoEAA `Repository` | 自研 ObjectStore 框架 |
| 按实体探测能力 | **能力 Protocol + 运行时探测**（API-server 资源能力模型） | ADR-0017 决策 C（K8s）、`typing.Protocol` PEP 544 `@runtime_checkable` | 父子类继承（脆弱基类） |
| 前置解析/渲染 | **python-frontmatter**（经 `tools/front_matter.py` 薄适配） | `requirements.txt` | 手写 front matter 解析 |
| 对象 schema 校验 | **jsonschema** + `config/json-schema/*.json` | 已用于 wiki 校验 | 逐字段手写校验 |
| 请求/DTO 模型 | **pydantic**（`extra="forbid"`） | 后端 `schemas.py` 已用 | 手写 dict 校验 |
| per-vault 写锁 | **filelock** | `requirements.txt` | 自研锁 |
| 原子写/崩溃安全 | `common.atomic_write`（临时文件+fsync+rename） | 现有 | — |
| 删除的引用完整性 | **SQL 外键语义 `ON DELETE RESTRICT / CASCADE`** | 关系数据库通用语义 | 临时的 block/warn 规则 |
| 软删/退休记录 | **tombstone + append-only event log** | 落已有 `audit/retire` ledger | 自研删除流程 |
| provenance 关系边 | **W3C PROV-O** 术语 | ADR-0017 决策（`prov:wasQuotedFrom` 等） | 自造 `derived_from` |
| 心智模型对齐 | **Astro Content Collections**（typed collection + query） | 前端 Starlight 已用 | — |

## 3. 当前基线（实测）

- **查分散**：`source` 的“按 id 定位”有 4 份实现且语义不一致——`paths.source_file(domain,id)`（无存在性检查）、`backend/services.resolve_object_path`（rglob + `object_id_ambiguous`）、`validation/resolution.resolve_source`（`iter_source_files` 过滤 + `source_ambiguous`）、`doctor` 直接枚举。`wiki` 读散在 `projection`/`resolution`/后端 `read_object`。
- **`source` 改会毁证据**：唯一“更新”路径是同 id 重导入，`SourceIngestor._write_artifacts` 用重建的 front matter 整文件覆盖，`_source_metadata` 不保留 `evidence_items`，而 `evidence_anchor.apply_evidence` 恰把 `evidence_items` 写在同一份 front matter——重导入（含幂等重跑）会清空已锚定证据。
- **`source` 删缺失**：全仓无 source 删除/退休接口；手动 `rm` 会遗留 snapshot / manifest 条目 / sidecar / raw / wiki `evidence.targets` 悬挂引用。
- **`questions` 已具完整 CRUD**：`QuestionStore`（create/import/list/session/queue/errors/disable/enable/delete/answer/review/refresh），且删除在有复习历史时降级为 `disable`（保留历史）——本设计以它为范本。
- ADR-0017 已定“公共部分 = R/D/L + 校验编排 + 关系解析；C/U 各实体自持”，本设计是其接口级落地。

## 4. 模块边界

新增一个薄的能力层，领域实现全部**委托现有代码**，不重写：

```
tools/content_repository.py         # 能力 Protocol + FileObjectMixin（R/D/L + resolve 单份实现）
  ├─ SourceRepository               # + create → 委托 SourceIngestor.ingest
  │                                 # + update → 幂等 + 保留 evidence_items
  │                                 # + delete → retire(RESTRICT: 被活跃 wiki 引用则拒)
  ├─ WikiRepository                 # R/D/L 复用；create/promote → 委托通道 A（WikiValidator/audit/confirm/release）
  │                                 # + delete → deprecate(CASCADE: 级联 QuestionStore.refresh_status；写 CDR 到 content/decisions/)
  └─ QuestionStore（既有）           # 适配能力 Protocol（补 read/exists/resolve 别名，delete↔retire 命名对齐）
```

- `backend/services.resolve_object_path`、`validation/resolution.resolve_source`、`doctor` 的 source 枚举**改为调用** `FileObjectMixin.resolve/list`，各自在边界把统一码适配回既有契约码（见 §5、§12）。
- `working` 不在本模块内（§11）。

## 5. 数据模型与接口契约

### 5.1 object_ref 与能力矩阵（对齐 ADR-0017）

`ObjectRef = (vault_id, object_type, object_id)`；`object_type ∈ {source, wiki, question}`。能力用 `@runtime_checkable` Protocol 表达，实体声明实现哪些：

| 实体 | Readable | Listable | Deletable | Updatable | Creatable | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| source | ✅ | ✅ | ✅(RESTRICT) | ✅(幂等/保留证据) | ✅(采集流水线) | Create=Collector |
| wiki | ✅ | ✅ | ✅(CASCADE+CDR) | ✅(生命周期) | ✅(通道 A) | draft→published→retire/deprecate |
| question | ✅ | ✅ | ✅(有历史降 disable) | ✅(状态/SRS) | ✅(绑定 claim) | 既有实现 |

### 5.2 能力 Protocol（共享契约）

```python
@runtime_checkable
class Readable(Protocol):
    def read(self, ref: ObjectRef) -> dict: ...          # {schema_version, object_ref, path, body/metadata}

@runtime_checkable
class Listable(Protocol):
    def list(self, **spec) -> dict: ...                  # {schema_version, total, items, invalid}

@runtime_checkable
class Deletable(Protocol):
    def delete(self, ref: ObjectRef, *, reason: str, actor_id: str) -> dict: ...  # 软删/retire

@runtime_checkable
class Updatable(Protocol):
    def update(self, ref: ObjectRef, patch: dict) -> dict: ...
```

- 返回体沿用项目“带 `schema_version` 的结构化结果”约定（如既有 `read-result/v1`、`backlinks-result/v1`）；新增 `object-list/v1`、`retire-result/v1`。
- `FileObjectMixin` 提供 `resolve(ref)->Path`（存在性 + 歧义 + `safe_id` + symlink/越界防护单份实现）、`read`、`list`、以及写原语 `_save(path, bytes)`（`atomic_write` + 载入即校验 `content_sha256`）。

### 5.3 删除语义：RESTRICT / CASCADE（借 SQL 外键）

- **source.delete = RESTRICT**：被任一 `status != disabled` 的 wiki 通过 `evidence.targets`/`sources` 引用时返回 `{status: blocked, error_code: object_referenced}`；无引用时执行 retire。
- **wiki.delete = CASCADE(deprecate)**：级联把绑定它的 question 经 `QuestionStore.refresh_status` 置 `disabled`，并**必须**在 `content/decisions/` 写一条 CDR（§4.5 强制），再 retire。
- **question.delete**：叶子；有复习历史→`disable`（现状），无历史→删除文件（现状）。
- retire 一律**软删**：不物理删 `archive/manifest`（append-only），向 `audit/retire`（`RepoPaths.audit_retire` 已预留）追加一条 append-only 记录；重复 retire 幂等为 `noop`。

## 6. 正常流程

- **查**：入口 → `resolve(ref)` 定位 → `read`/`list`（managed 用 `FrontMatter.parse`，question 用 `json + content_sha256` 校验）→ 结构化返回。
- **增**：`SourceRepository.create` → `SourceIngestor.ingest`；`WikiRepository.create/promote` → 通道 A；`QuestionStore.create` → 绑定已验证 claim。
- **改**：`source.update` 先算 body 的 `snapshot_sha256`，与现有相同则 `noop` 且**保留 `evidence_items`**；否则合并元数据、保留 `evidence_items`、`_save`。
- **删**：见 §5.3。

## 7. 失败流程

- 不存在→`object_not_found`；多命中→`object_id_ambiguous`；非法 id/越界/symlink→`invalid_object_ref`（复用现 `safe_id`/路径守卫）。
- `content_sha256` 不符→`question_hash_mismatch`（现状回归）；front matter 损坏→`list` 计入 `invalid` 不中断。
- retire 被引用阻断→`object_referenced`（结构化，含引用者清单）。

## 8. 幂等与并发

- per-vault 写用既有 **filelock**；写盘用 `atomic_write`。
- `source.update` 按 `snapshot_sha256` 幂等；retire 幂等；这两条纳入测试（§10 AC-C1/AC-D4）。

## 9. 安全边界

- 复用既有 `safe_id`、`safe_relative_path`、`is_contained_regular_file`、symlink 段拒绝；capability token、loopback 门禁不变（本设计不触碰鉴权层）。
- retire 记录经 `redact` 脱敏敏感字段后再落 ledger。

## 10. 测试策略与验收

新增 `tests/test_content_repository.py`、`tests/test_source_repository.py`、`tests/test_wiki_repository.py`；既有 `tests/ingest/test_source_ingestor.py`、`tests/test_question.py`、`tests/validation/test_wiki_resolution.py`、`tests/test_vault_registry.py` 必须保持绿。

**A 统一 Read/Resolve**
- AC-R1 三类经同一 `resolve`：不存在→`object_not_found`，多命中→`object_id_ambiguous`。
- AC-R2 越界路径、路径段含 symlink 一律拒绝（恶意 id / 软链用例）。
- AC-R3 `read` 形状统一；question `content_sha256` 不符→`question_hash_mismatch`。
- AC-R4 注入一个损坏文件时它进 `list.invalid`，其余正常返回。

**B 统一软删/retire**
- AC-D1 source 被启用 wiki 引用时 `delete`=`blocked`(`object_referenced`)；wiki `deprecate` 后其绑定 question 变 `disabled` 且 `content/decisions/` 新增 CDR。
- AC-D2 retire 后 `archive/manifest` 条目仍在，`audit/retire` 新增一条 append-only 记录。
- AC-D3 question 有复习历史 `delete`→`disabled`（现状回归）。
- AC-D4 重复 retire 幂等为 `noop`。

**C 各自 Create/Update**
- AC-C1 source：同 body `update`=`noop` 且 `evidence_items` 保持不变（锁死修复）。
- AC-C2 source：`test_source_ingestor.py` 全绿（create 行为不变）。
- AC-C3 wiki：绕过通道 A 直接 publish 的尝试被拒。
- AC-C4 question：`test_question.py` 全绿。

**D 回归/契约（关键：不破外部约定）**
- AC-G1 后端 `read_object`/`resolve_object_path` 外部错误码与响应形状不变（`object_not_found`/`object_id_ambiguous`）。
- AC-G2 `resolution.resolve_source` 的 `source_not_found`/`source_ambiguous`（wiki 校验报告用）不变——边界适配器负责映射。
- AC-G3 全量 `pytest` 绿。

## 11. working 层的处置（不进 CRUD 契约）

`working` 不退役、也不建对象级 CRUD。它是 §4.5 的 unmanaged 暂存层（对应 Zettelkasten 的 fleeting note / BASB 的 Capture-Distill），靠“低摩擦入口 + 出口封锁”成立；建 CRUD-with-identity 会同时破坏这两个前提。它需要的接口是：文件级读写 + 枚举（`layers.iter_unmanaged_files`）+ TTL 报告（`doctor`）+ 一个**流转动作** `promote(working→wiki)`（走通道 A，见 ADR-0020），流转不是 CRUD。真正待退役的是 `working` 的临时前身 `docs/<domain>/`（§16），勿混淆。

## 12. 迁移与回滚（分阶段，每步独立可回滚、独立跑测试）

| 阶段 | 内容 | 回滚点 |
| --- | --- | --- |
| P1 共享层 | 新建 `tools/content_repository.py`，**先只落有消费者的 `locate_managed_object`（按 id 定位单份实现）**；`services.resolve_object_path` 与 `resolution.resolve_source` 改为复用 + 边界码适配。能力 Protocol 与 `FileObjectRepository`（read/list）不在 P1 提前引入，随 P2 首个真实调用点一起落地（避免无消费者的抽象）。 | 保留旧函数为适配薄壳，可整体回退 |
| P2 SourceRepository | create 委托 `SourceIngestor`；update 幂等+保留 `evidence_items`；delete=RESTRICT+`audit/retire` | 新增文件，删除即回退 |
| P3 WikiRepository | R/D/L 复用；delete=CASCADE(deprecate)+CDR+级联 refresh | 同上 |
| P4 Question 适配 | 补能力 Protocol 别名 | 极小改动 |
| P5（可选） | porcelain/CLI 暴露统一 `read/list/retire`；doctor 用统一 list | 纯增量 |

**回滚原则**：P1 通过“旧读函数改为调用新 resolve 的薄壳”实现，任何一步失败可 `git revert` 单个 commit；ledger append-only，retire 不物理删，天然可逆。

### 12.1 落地状态（2026-09-20：全动词注册表接入闭环）

P1–P5 已落地：`ContentRegistry` 从"只路由 public wiki 读"扩为**全动词路由表**
（read/list/create/update/delete），移植 K8s apiserver `registry/rest` 的能力发现——
`tools/content_repository.py` 定义 `@runtime_checkable` 的 `Readable/Listable/Creatable/
Updatable/Deletable`（对标 `rest.Getter/Lister/Creater/Updater/GracefulDeleter`），注册表用
`issubclass` 探测每个实体支持的动词后建能力表（`_probe`），**不给不支持的动词写硬编码分支**。

- **探测结果**：`source`=R/L/C/U/D、`wiki`=R/L/D（create/update 仍走通道 A）、
  `question`=R/L/C/D（update 走生命周期动词 disable/enable/review）。
- **失败语义**：未知 `object_type` → `object_type_not_found`；已知但动词不支持 →
  `capability_not_supported`（HTTP 405，已登记 `contract._LOCATE_CODES`）。
- **读 scope 分流**：wiki `vault_id=public` 走 projection（免 token），其余走 repository；
  source 恒走 repository；question 用 `vault_id="local"` 约定（单一本地 practice 根）。
- **三入口接入**：backend 新增 `GET /api/list/{vault}/{type}`、
  `DELETE /api/object/{vault}/{type}/{id}`、`POST /api/source/update`，practice 删除改经注册表；
  skill 新增 `list`/`retire`/`source_update` action 且 `question_*` 改经注册表；
  plumbing `tools.cli` 增 `list`/`retire`/`source-update`，porcelain `myk` 增
  `source list/retire/update`、`wiki list/retire/deprecate`（object_type 前置注入，kubectl 式）。

## 13. 未决问题

- 边界错误码要不要统一为一套（`object_not_found`）并让后端/resolution 一起改契约，还是保留各边界既有码只在内部统一实现？（本设计默认后者，AC-G1/G2 守旧契约。）
- `source.update` 的“只改元数据”是否需要独立命令，还是并入重导入的幂等路径即可？
- ~~是否借本次落地把 ADR-0017 从 Proposed 提升为 Accepted~~ → 已决：2026-09-18 ADR-0017 由 Proposed 提为 Accepted。

## 14. 内容对象统一规范（规范 / 激进版：全项目归一）

> 治理决策（2026-09-18，用户选定激进版 + 尽量简单）：全项目结果信封归一到本节，
> 由 `tools/contract.py` 强制（未知 status / 缺 schema_version / 未登记 error_code 一律
> `ValueError` fail-closed）。迁移用 TDD 推进，全量 `pytest` 全程绿。
>
> 设计对齐 gRPC status codes、Kubernetes `metav1.Status`、Rust `Result`：**只有一根
> status 轴 + 细分 error_code + 结果全进 payload**；不设独立 effect 轴（该轴不主流，
> HTTP 折进成功码、gRPC/K8s 放 payload）。“created/updated/noop 之类写效果”按需作为
> 该写接口 payload 里的领域字段，不进信封。

### 14.1 结果信封（尽量简单）

所有领域函数返回 `dict`，必带两字段，另在失败时带错误：

- `schema_version`：形如 `name/vN`（正则 `[a-z0-9-]+/v\d+`）。
- `status`：**唯一状态轴**，取自 3 值 `STATUSES`（见 14.2）。
- `error_code`（仅 `status != ok`）：取自 `ERROR_CODES` 单一词表；字段级细分用可选
  `errors: [{code, path?, reason?}]`。
- 其余全部是领域 payload（`body`/`items`/`report`/`grading`/写效果字段等）。

### 14.2 status 词汇（3 值，唯一状态轴）

| status | 语义 | retryable（边界派生，不落信封） |
| --- | --- | --- |
| `ok` | 调用成功（读/写/校验跑通都算 ok；“做了什么”看 payload） | false |
| `blocked` | 调用方/输入错误导致拒绝（非法 ref、越权、校验失败） | false |
| `unavailable` | 外部/环境不可用（provider、IO、依赖缺失） | true |

**一切领域结果不进 status**：作答判分放 `grading`，校验结论放 `report.valid`，
写效果（新建/更新/幂等）按需放该接口的领域字段（如 `created: true`）——status 只回答
“这次调用成没成”。`retryable` 是 status 的派生属性（仅 `unavailable` 为真），由边界层
（HTTP）计算，不冗余进信封。

### 14.3 单一 `error_code` 词汇

`status != ok` 必带 `error_code`，取自 `tools/contract.ERROR_CODES` 单一词表。**A 线已闭环**
（2026-09-19）：全部生产者模块均已归一，词表由 15 个「按域子集」union 而成，共 **147** 个已登记码
（各 agent 只追加自己那块的字面量、改不同代码行，避免并行合并冲突）。构造器对未登记码
**fail-closed**（`ValueError: error_code_not_registered:*`），杜绝手写字面量漂移。

**登记原则（防词表膨胀）**：只把「操作层 `status != ok` 的顶层码」登记进词表；字段级/动态明细码
（如 `fetch_blocked:*`、异常类名、逐行解析失败等）一律落 `payload.errors[]` 或专用 payload 字段
（`unresolved[].error_code` 等），**不进词表**。故若干模块只登记少数「伞码」（如
`source_ingest_failed`/`video_frame_failed`/`validator_unavailable`），明细下沉 payload。

当前各域子集（见 `tools/contract.py`，均为该文件内可核对的单一事实源）：

| 子集 | 覆盖生产者 | 码数 |
| --- | --- | --- |
| `_LOCATE_CODES` | 内容对象定位 + wiki resolution 历史码 | 10 |
| `_QUESTION_CODES` | `question.py` / `question_quality`（编题/导入/生命周期/判分/调度） | 19 |
| `_SOURCE_CODES` | `ingest/source_ingestor`（输入/校验类伞码） | 2 |
| `_ENTRY_CODES` | `backend/*` / `skill_runtime` / `mcp_server`（通道门禁 + capability 令牌） | 26 |
| `_MISC_CODES` | release_confirmation / vault_registry / indexing 顶层码 | 17 |
| `_CRUD_CODES` | source/wiki CRUD 能力层（采集委派伞码） | 1 |
| `_BACKUP_CODES` | `backup.py`（status/manifest/verify/restore 状态机） | 28 |
| `_VALIDATION_CODES` | `validation/*`（validator 不可用伞码） | 1 |
| `_INGEST_CODES` | `ingest/*`（video_frames / video_inventory，不含 source_ingestor） | 10 |
| `_DOCTOR_CODES` | `doctor.py`（顶层恒 `ok`，故为空集） | 0 |
| `_ANCHOR_CODES` | `evidence_anchor.py`（定位/落盘/批量锚定） | 7 |
| `_AUDIT_CODES` | `validation/audit.py`（LLM 证据审计编排的操作层码） | 7 |
| `_CONFIRM_CODES` | `validation/confirm.py`（人工确认前置门禁） | 6 |
| `_MATRIX_CODES` | `matrix_sync.py`（追踪矩阵/feature-list/文档索引一致性） | 6 |
| `_CLI_CODES` | `cli.py` 内联生产者（override 复议 + release 发布） | 8 |

> union 去重后为 147（`deterministic_blocked` 同时属于 audit/confirm 两域，语义一致，故子集码数之和
> 148 − 1 重叠 = 147）。字段级细分继续用可选 `errors: [{code, path?, reason?}]`。

### 14.4 边界适配（保外部契约）

- HTTP：`backend/errors.py` 把 `error_code` 映射到 `HTTPException(detail={code,stage,retryable,next_action})`，`status` 码与 `retryable` 由 `error_code`/`status` 在边界派生；成功体透传 `schema_version`/`status`。
- wiki 校验报告：`resolution` 等历史 `code`（`source_not_found` 等）已纳入统一词表，语义不变。
- 迁移期字段**同源**：由 `contract` 构造器产出，杜绝手写字面量漂移。

### 14.5 provenance 与软删

关系边用 W3C PROV-O（`prov:wasQuotedFrom`/`wasRevisionOf`/`wasDerivedFrom`）；软删=tombstone + `audit/retire` append-only；删除策略 `RESTRICT`/`CASCADE`（§5.3）。

## 15. 统领入口：content registry

`tools/content_registry.py` 暴露一个按 `object_type` 路由到实体 repository 的注册表；
每个实体用 §5.2 的 `@runtime_checkable` 能力 Protocol 声明其实现的 CRUD。三个物理入口
（`backend` HTTP / `skill_runtime` / `tools.cli`）的内容读写**都经此注册表**取得能力，
不再各自接线到领域函数——这消除“各自为战”的入口层。注册表只做路由与能力探测，不含领域逻辑。

## 16. 迁移清单（激进版，TDD，全程全量绿）——**已闭环（A 线，2026-09-19）**

全部步骤已落地，全程全量 `pytest` 绿。清单与对应实现/测试锚点：

1. ✅ `tools/contract.py`（3 值 `status` + `error_code` 词表 + `result/ok/blocked/unavailable` 构造器 + 校验；`status!=ok` 强制带已登记 `error_code`）——先写 `tests/test_contract.py`。
2. ✅ `tools/content_repository.py` 与 P2/P3/P4 实体 repository 一律经 `contract` 构造结果。
3. ✅ 逐模块把 `question.py`/`ingest/source_ingestor.py`/`skill_runtime.py`/`backend/*`/`validation/*`/`indexing.py`/`vault_registry.py`/`backup.py`/`release_*`/`doctor.py`/`evidence_anchor.py`/`matrix_sync.py`/`cli.py` 的手写信封替换为 `contract` 构造器：旧的成功态（created/applied/listed/enabled…）统一为 `status=ok` + 按需领域字段，失败态统一为 `blocked`/`unavailable`+`error_code`；作答/校验结论下沉 typed 字段；每换一处**同步改其测试断言**，跑对应测试→再跑全量。
4. ✅ `tools/content_registry.py` 接入三入口（边界保 HTTP 契约）。
5. ✅ 收尾：一致性防回潮测试 `tests/test_contract_consistency.py`——断言 `STATUSES` 恰 3 值、`ERROR_CODES` = 15 个域子集之并、真实入口返回信封满足 `status ∈ STATUSES ∧ (status != ok ⇒ error_code ∈ ERROR_CODES)`，并**显式禁止顶层再出现与 `status` 并列的第二根状态轴 `state`**（backup/doctor/video 的历史 `state` 已下沉/改名，见 commit `58eb488`）。
