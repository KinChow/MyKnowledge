---
actor_id: zhouzijian01
content_verdict: retire
id: CDR-code-server-retire-20260905
reason_code: obsolete
target_object_id: code-server
target_path: content/wiki/tools/code-server.md
---
# code-server 退役决定

## 判定

`code-server` 文档已过时，退出当前 Wiki 的可发布范围。该决定只针对 canonical Wiki 对象，不删除 `content/working/` 原文、Source 快照、archive、manifest 或审计记录。

## 后续删除边界

物理 purge 需要 public owner backup 处于 `verified`，当前状态为 `unconfigured`，因此本次只执行退役，不绕过门禁删除文件。
