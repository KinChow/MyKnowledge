---
name: myknowledge
description: Controlled Source/Wiki/query/publish operations for the MyKnowledge checkout.
---

# MyKnowledge Skill

This checkout is the canonical Skill source. Use the repository's domain tools
and local API; do not edit Markdown, JSONL manifests, generated indexes, Vault
directories, or Git state directly.

## Routing

- Query/read/ask: `python -m tools.cli query` or the local API `/api/retrieve` and `/api/ask`; ask remains unavailable when no provider is configured and never treats retrieval hits as a generated answer.
- Source/Wiki changes: call the domain preview operation, show operation ID,
  target vault, hashes and warnings, then wait for explicit human confirmation
  before Apply.
- Validation/audit: call `python -m tools.cli validate` or `audit`; provider
  failures are `not_run`, never a validation pass.
- Publish: require the appropriate confirmation event and current content,
  evidence and release-input hashes. Public release is never implied.
- Question practice (F008): use the dedicated question service only; question
  answers, explanations and review state are local/private and never public.

## Security rules

Never reveal capability tokens, API keys, absolute private paths, private
provider endpoints, selector exact text, archive bodies or review state. Never
expand a query scope, infer a Vault owner, bypass a writer, or run
`git commit/push/reset` or `git submodule update`. Missing provider, Vault or index must be
reported with its structured unavailable reason.
