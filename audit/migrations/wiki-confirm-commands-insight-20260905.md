# insight 审计与 confirm 记录（2026-09-05）

本次确定性校验通过。审计改用 `ducc` 并显式指定 `gpt-5.6-terra`。此前 `ducx` 的 LLM 证据审计因 HTTP 403 未运行，因此 `insight` 尚未审计通过，不能执行 confirm。

当前 hash：

- content：`sha256:abe20d7041188397540c25ddb168bae2b519b31f27faa29e68c089124b58326e`
- evidence：`sha256:58f1b101d09aa3bc9fd80850b86e7c62aa3314ba8687b0f7b92e6e453b90e45b`

接口恢复后先重新审计：

```bash
.venv/bin/python -m tools.cli audit content/wiki/work-methods/insight.md --root . --provider agent-cli --cli /Users/zhouzijian01/.comate/baidu-cc/bin/ducc --model gpt-5.6-terra
```

只有返回 `verdict: pass` 且报告 hash 与上面当前 hash 一致时，才可人工阅读并执行：

```bash
.venv/bin/python -m tools.cli confirm content/wiki/work-methods/insight.md --root . --actor-id zhouzijian01 --decision approve
```

本文件只记录命令，不执行 confirm。
