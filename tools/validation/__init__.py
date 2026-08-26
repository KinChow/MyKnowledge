"""校验职责域（F002 Wiki 契约校验；未来 F003 证据验证等校验器也归入本包）。

命名对齐 kernelwiki-kunlun/scripts 的职责域组织方式（validation/ingest/gates），
避免与仓库内容目录 ``wiki/`` 撞名。对外接口：``WikiValidator``（validate 门面）、
``WIKI_SCHEMA_VERSION``、``OWNER_VAULT_ID``。内部按职责分层，与 tools 其他模块解耦：

- ``schema``：可执行 JSON Schema 层（加载/执行/手写派生字段拒绝）
- ``rules``：domain rule 层（状态组合、kind 分支、来源矩阵、正文模板）
- ``resolution``：引用解析与 supporting_quotes 逐字校验（§6.9）
- ``derived``：派生字段计算（evidence_state/strength/publishable）与确认读取
- ``validator``：门面编排（validate 入口与 CLI）

包内模块通过显式参数传递（paths/resolution），不共享可变实例状态。
"""

from .validator import OWNER_VAULT_ID, WIKI_SCHEMA_VERSION, WikiValidator

__all__ = ["WikiValidator", "WIKI_SCHEMA_VERSION", "OWNER_VAULT_ID"]
