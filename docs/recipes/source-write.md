# 写入 Source：create / update / delete / purge

> 任务导向配方。精确字段与失败码见 [Source 导入与归档](../technical-design/source-ingestion-and-archive.md)
> 与 [内容 CRUD：Repository 契约](../technical-design/content-crud-repository.md)（§12 两阶段删除、
> §12.4 统一创建契约）。source 是目前 CRUD 全动词的实体。

## 0. 写操作总览

| 动词 | 语义 | 关键约束 |
| --- | --- | --- |
| **create** | 采集并落盘一个新 source（统一契约） | local/remote/inline 由 locator 决定；覆盖式（同 id 重跑覆盖） |
| **update** | 重导入同一 source | 按 `snapshot_sha256` **幂等**；**保留已锚定 `evidence_items`** |
| **delete**（软删） | 登记删除墓碑，可恢复，不删盘 | **RESTRICT**：被活跃 wiki 引用则 `object_referenced` 阻断 |
| **purge**（硬删） | 物理回收目录（含 LFS 原件） | **两阶段**：须先 delete + 过宽限期（默认 14 天）+ RESTRICT 复查 |

## 1. 统一创建契约（create / update 的入参）

```jsonc
{ "locator": "file://…  |  http(s)://…  |  data:…",   // 外部来源；与 content 二选一
  "content": "内联正文",                                // personal-note 内联
  "kind":    "doc|blog|book|contest|pr|note|video-transcript",
  "domain":  "computer-science|tools|multimedia|reading-notes|work-methods",
  "source_id": "可选（update 必填，用于定位）",
  "options": { "asr_engine": "…", "subtitle_mode": "…", "media_type": "…" } }
```

- **本地 / 远程 / 内联 = locator 的 URI scheme**：`file://` 本地、`http(s)://` 远程抓取、
  `data:` 内联，或直接给 `content`。
- `kind` = 语义类别（保留既有 `source_type`，SRC-002 只加不改名）。

## 2. 四入口用法

### A) 人用 CLI / porcelain `myk`（允许全部 scheme，含 `file://`）

```bash
# create —— 内联 / 远程 / 本地 / 视频转录 四态一致
myk source add --content "# 笔记\n正文" --kind note --domain tools --source-id my-note
myk source add --from https://example.com/post --kind doc --domain computer-science --source-id some-post
myk source add --from file:///abs/paper.pdf --kind doc --domain computer-science --source-id paper
myk source add --from https://www.bilibili.com/video/BVxxx --kind video-transcript --domain multimedia --source-id lec1

# update（重导入，幂等 + 保留证据）；request.json 是上面的契约，须含 source_id
myk source update request.json

# 软删 / 硬删
myk source delete <source_id>
myk source purge  <source_id>
```

底层 plumbing：`python -m tools.cli source | source-update | delete | purge`。

### B) 后端 HTTP（对外 / agent；需写能力 token；仅 `http(s)`/`data`，拒 `file://`）

```
POST   /api/source                              # create（body = 统一契约）
POST   /api/source/update                       # update（body = 契约，含 source_id）
DELETE /api/object/{vault}/source/{id}          # 软删
POST   /api/object/{vault}/source/{id}/purge    # 硬删
```

```bash
curl -X POST http://127.0.0.1:PORT/api/source \
  -H 'X-MyKnowledge-Capability: <token>' \
  -d '{"content":"内联正文","kind":"note","domain":"tools","source_id":"http-note"}'
```

- `file://` 经 HTTP 一律 **403 `locator_scheme_not_allowed`**（不许网络侧读本地盘）。

### C) Agent Skill（`dispatch(action, payload, root=)`；仅 `http(s)`/`data`）

- create：`source_ingest {request:<统一契约>}`
- update：`source_update {request:<契约>}`
- 软删：`delete {object_type:"source", vault_id, object_id}`
- 硬删：`purge  {object_type:"source", vault_id, object_id}`
- 安全：`file://` 或 legacy `input_path` → blocked `locator_scheme_not_allowed`。

### D) 编程 / registry（受信，全 scheme）

```python
r = ContentRegistry(root)
r.create("source", request={"locator": "https://…", "kind": "doc", "domain": "computer-science", "source_id": "x"})
r.update("source", request={"locator": "https://…", "kind": "doc", "domain": "computer-science", "source_id": "x"})
r.delete("source", vault_id="public", object_id="x")   # 软删
r.purge ("source", vault_id="public", object_id="x")   # 硬删（须先 delete + 过宽限期）
```

## 3. 关键规则（避免踩坑）

1. **改内容用 `update`，不要"删了重建"**：update 幂等（同 body = noop）且**保留已锚定的
   `evidence_items`**（早期缺陷是重导入会清空证据，已修）。
2. **删有引用保护（RESTRICT）**：被任一"未退休且 `status != disabled`"的 wiki 经
   `sources`/`evidence.targets` 引用时，`delete` 与 `purge` 都会 `object_referenced` 阻断。
3. **两阶段删**：`delete` = 墓碑可恢复（不删盘）；`purge` 才物理回收
   `content/sources/<domain>/<id>/`（含 LFS 原件），且必须"先 delete → 过宽限期
   （`policy.delete.purge_grace_days`，默认 14 天，对齐 git `gc.pruneExpire`）"。
4. **create 是覆盖式**：同 `source_id` 再 create 会重跑采集覆盖；要"改且不丢证据"用 `update`。
5. **降体积**：purge 只回收工作树；真正降 `.git`/LFS 占用需配套 `git lfs prune`，
   彻底历史擦除走 `git filter-repo` + force push 的授权 runbook（见 content-crud §12.3）。

## 4. 典型生命周期

```
create（采集入库）
  → [被 wiki 引用 / 锚定 evidence]
  → update（来源更新时重导入，保留证据）
  → delete（软删，RESTRICT 挡引用）
  → （过宽限期）purge（物理回收 + git lfs prune 降体积）
```

## 5. 写效果与失败

- 成功信封：`source-create/v1`{changed, source_id, snapshot_sha256}、`source-update/v1`{changed}、
  `source-retire/v1`{retired}、`source-purge/v1`{purged}。
- 失败：`status=blocked` + `error_code`（如 `object_referenced`/`not_deleted`/
  `retention_not_elapsed`/`locator_scheme_not_allowed`/`source_ingest_failed`）。
- 写盘安全：`atomic_write`（临时文件+fsync+rename）、per-vault `filelock`、`safe_id`/越界/
  symlink 防护，均复用既有实现。
