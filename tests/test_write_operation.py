from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.common import sha256_bytes
from tools.vault_lock import LockBusyError, VaultLock, VaultLockGroup
from tools.write_operation import WriteOperation


class WriteOperationTests(unittest.TestCase):
    def test_private_vault_write_uses_owner_checkout_root(self):
        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d)
            public = workspace / "public"
            private = workspace / "private"
            public.mkdir()
            private.mkdir()
            subprocess.run(["git", "init", "-q", str(public)], check=True)
            subprocess.run(["git", "init", "-q", str(private)], check=True)
            manifest = workspace / "vaults.yaml"
            manifest.write_text(
                f"schema_version: 1\nlayout: superproject\nworkspace_root: {workspace}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n",
                encoding="utf-8",
            )
            registry = __import__(
                "tools.vault_registry", fromlist=["VaultRegistry"]
            ).VaultRegistry(public, manifest)
            # DIP：注入 vault root 解析器，无需 mock.patch 具体类
            service = WriteOperation(
                public, vault_root_resolver=registry.resolve_vault_path
            )
            preview = service.preview({"wiki/private.md": "secret"}, vault_id="private")
            self.assertEqual(preview["state"], "previewed")
            self.assertEqual(
                service.apply(preview["operation_id"], confirmed=True)["state"],
                "applied",
            )
            self.assertEqual(
                (private / "wiki" / "private.md").read_text(encoding="utf-8"), "secret"
            )
            self.assertFalse((public / "wiki" / "private.md").exists())

    def test_preview_is_read_only_and_apply_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"wiki/a.md": "hello"})
            self.assertEqual(preview["state"], "previewed")
            self.assertFalse((root / "wiki/a.md").exists())
            self.assertEqual(
                service.apply(preview["operation_id"])["state"], "awaiting_confirmation"
            )
            self.assertEqual(
                service.apply(preview["operation_id"], confirmed=True)["state"],
                "applied",
            )

    def test_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            service = WriteOperation(Path(d))
            op = service.preview({"a.md": "one"})["operation_id"]
            first = service.apply(op, confirmed=True)
            second = service.apply(op, confirmed=True)
            self.assertEqual(first, second)

    def test_hash_change_blocks_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "a.md"
            target.write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            target.write_text("other", encoding="utf-8")
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "hash_mismatch")
            self.assertEqual(target.read_text(encoding="utf-8"), "other")

    def test_apply_path_race_returns_structured_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            op = service.preview({"nested/a.md": "new"})["operation_id"]
            (root / "nested").mkdir(parents=True)
            (root / "outside").mkdir()
            (root / "nested").rmdir()
            (root / "nested").symlink_to(root / "outside", target_is_directory=True)
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["state"], "expired")
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertIn("path_symlink", result["detail"])
            self.assertFalse((root / "outside" / "a.md").exists())

    def test_tampered_durable_audit_blocks_apply(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            audit = root / "audit" / "operations" / f"{op}.json"
            value = json.loads(audit.read_text(encoding="utf-8"))
            value["state"] = "applied"
            audit.write_text(json.dumps(value), encoding="utf-8")
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "hash_mismatch")
            self.assertFalse((root / "a.md").exists())

    def test_path_escape_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            result = WriteOperation(Path(d)).preview({"../escape.md": "x"})
            self.assertEqual(result["error_code"], "path_outside_repo")

    def test_symlink_and_hardlink_targets_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "real.md"
            target.write_text("old", encoding="utf-8")
            (root / "alias.md").symlink_to(target)
            service = WriteOperation(root)
            self.assertEqual(
                service.preview({"alias.md": "new"})["error_code"], "path_symlink"
            )
            linked = root / "linked.md"
            linked.hardlink_to(target)
            self.assertEqual(
                service.preview({"linked.md": "new"})["error_code"], "path_hardlink"
            )

    def test_lock_busy_is_structured(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            op = service.preview({"a.md": "x"})["operation_id"]
            lock = VaultLock(root, "public", "other")
            with lock:
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "lock_busy")

    def test_fencing_token_rejects_replaced_owner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = VaultLock(root, "public", "op-one")
            with lock:
                lock._owner_file.write_text(
                    json.dumps({"operation_id": "op-two", "lock_token": "stolen"}),
                    encoding="utf-8",
                )
                with self.assertRaises(LockBusyError):
                    lock.assert_owner()

    def test_stale_lock_recovery_requires_free_kernel_lock_and_writes_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = VaultLock(root, "public", "op-old")
            lock._owner_file.parent.mkdir(parents=True, exist_ok=True)
            lock._owner_file.write_text(
                json.dumps({"operation_id": "op-old", "lock_token": "stale"}),
                encoding="utf-8",
            )
            result = VaultLock.recover(root, "public", "op-recover", "alice")
            self.assertEqual(result["state"], "recovered")
            self.assertFalse(lock._owner_file.exists())
            records = list((root / "audit" / "operations").glob("lock-recovery-*.json"))
            self.assertEqual(len(records), 1)
            record = json.loads(records[0].read_text(encoding="utf-8"))
            self.assertEqual(record["record_type"], "lock-recovery")
            self.assertEqual(record["old_operation_id"], "op-old")

    def test_stale_lock_recovery_does_not_break_live_lock(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLock(root, "public", "op-live"):
                result = VaultLock.recover(root, "public", "op-recover")
                self.assertEqual(result["error_code"], "lock_busy")

    def test_multi_vault_lock_group_orders_and_releases_all(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLockGroup(root, ["zeta", "alpha", "alpha"], "op-group") as group:
                self.assertEqual(group.vault_ids, ("alpha", "zeta"))
                group.assert_owner()
                self.assertTrue((root / "state" / "locks" / "alpha.owner").exists())
                self.assertTrue((root / "state" / "locks" / "zeta.owner").exists())
            self.assertFalse((root / "state" / "locks" / "alpha.owner").exists())
            self.assertFalse((root / "state" / "locks" / "zeta.owner").exists())

    def test_multi_vault_lock_group_releases_acquired_locks_on_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLock(root, "zeta", "other"):
                with self.assertRaises(LockBusyError):
                    with VaultLockGroup(root, ["alpha", "zeta"], "op-group"):
                        pass
                self.assertFalse((root / "state" / "locks" / "alpha.owner").exists())

    def test_multi_file_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.md").write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new", "b.md": "created"})["operation_id"]
            original = service._path
            calls = {"n": 0}

            def fail_once(name):
                calls["n"] += 1
                if calls["n"] == 2:
                    raise OSError("injected")
                return original(name)

            with mock.patch.object(service, "_path", side_effect=fail_once):
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "old")
            self.assertFalse((root / "b.md").exists())

    def test_failed_apply_keeps_intent_for_explicit_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.md").write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new", "b.md": "created"})["operation_id"]
            original = service._path
            calls = {"n": 0}

            def fail_after_first(name):
                calls["n"] += 1
                if calls["n"] == 3:
                    raise OSError("injected")
                return original(name)

            with mock.patch.object(service, "_path", side_effect=fail_after_first):
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertTrue((root / "state" / "commit-intents" / f"{op}.json").exists())
            self.assertEqual(service.recover(op)["state"], "recovery_required")
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "old")

    def test_projection_failure_keeps_canonical_and_recovers(self):
        """AC-F004-009: projection failure is pending, never a false full apply."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            calls = []

            def fail_projection(record):
                calls.append(record["operation_id"])
                raise OSError("index unavailable")

            service = WriteOperation(root, projection_rebuilder=fail_projection)
            op = service.preview({"wiki.md": "new canonical"})["operation_id"]
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["state"], "applied_index_pending")
            self.assertEqual(result["error_code"], "projection_failed")
            self.assertEqual(
                (root / "wiki.md").read_text(encoding="utf-8"), "new canonical"
            )
            self.assertEqual(service.store.load(op)["state"], "applied_index_pending")

            rebuilt = []
            recovered = service.recover(
                op,
                projection_rebuilder=lambda record: rebuilt.append(
                    record["operation_id"]
                ),
            )
            self.assertEqual(recovered["state"], "applied")
            self.assertEqual(rebuilt, [op])
            self.assertEqual(service.store.load(op)["state"], "applied")
            self.assertFalse(
                (root / "state" / "commit-intents" / f"{op}.json").exists()
            )

    def test_rename_and_retire_have_distinct_operation_types(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "old.md").write_text("body", encoding="utf-8")
            service = WriteOperation(root)
            renamed = service.rename("old.md", "new.md")
            self.assertEqual(renamed["operation_id"].startswith("op_"), True)
            record = service.store.load(renamed["operation_id"])
            self.assertEqual(record["operation_type"], "rename")
            retired = service.retire("old.md")
            self.assertEqual(
                service.store.load(retired["operation_id"])["operation_type"], "retire"
            )
            result = service.apply(retired["operation_id"], confirmed=True)
            self.assertEqual(result["state"], "applied")
            marker = root / "audit" / "retire" / f"{retired['operation_id']}.json"
            self.assertTrue(marker.exists())
            self.assertEqual(
                json.loads(marker.read_text())["schema_version"], "retire-marker/v1"
            )

    def test_rename_source_drift_blocks_without_deleting_source(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "old.md"
            source.write_text("original", encoding="utf-8")
            service = WriteOperation(root)
            preview = service.rename("old.md", "new.md")
            source.write_text("user edit", encoding="utf-8")
            result = service.apply(preview["operation_id"], confirmed=True)
            self.assertEqual(result["error_code"], "hash_mismatch")
            self.assertEqual(source.read_text(encoding="utf-8"), "user edit")
            self.assertFalse((root / "new.md").exists())

    def test_commit_intent_is_removed_after_apply(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            self.assertEqual(service.apply(op, confirmed=True)["state"], "applied")
            self.assertFalse(
                (root / "state" / "commit-intents" / f"{op}.json").exists()
            )

    def test_purge_requires_verified_owner_backup(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "wiki.md"
            target.write_text("sensitive", encoding="utf-8")
            result = WriteOperation(root).purge("wiki.md")
            self.assertEqual(result["error_code"], "backup_not_verified")
            self.assertTrue(target.exists())

    def test_recover_commit_intent_marks_fully_written_files_applied(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"a.md": "new"})
            op = preview["operation_id"]
            service.store.load(op)
            from tools.common import atomic_write, canonical_json

            intent = {
                "schema_version": "commit-intent/v1",
                "operation_id": op,
                "operation_type": "write",
                "vault_id": "public",
                "files": [
                    {
                        "path": "a.md",
                        "before_hash": None,
                        "after_hash": sha256_bytes(b"new"),
                    }
                ],
            }
            from tools.common import hash_canonical

            intent["intent_sha256"] = hash_canonical(intent)
            atomic_write(
                root / "state" / "commit-intents" / f"{op}.json",
                canonical_json(intent) + b"\n",
                0o600,
            )
            (root / "a.md").write_text("new", encoding="utf-8")
            result = service.recover(op)
            self.assertEqual(result["state"], "applied")

    def test_recover_rejects_tampered_commit_intent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"a.md": "new"})
            op = preview["operation_id"]
            intent_path = root / "state" / "commit-intents" / f"{op}.json"
            intent_path.parent.mkdir(parents=True, exist_ok=True)
            intent = {
                "schema_version": "commit-intent/v1",
                "operation_id": op,
                "operation_type": "write",
                "vault_id": "public",
                "files": [
                    {
                        "path": "a.md",
                        "before_hash": None,
                        "after_hash": sha256_bytes(b"new"),
                    }
                ],
            }
            from tools.common import atomic_write, canonical_json, hash_canonical

            intent["intent_sha256"] = hash_canonical(intent)
            intent["files"][0]["after_hash"] = sha256_bytes(b"forged")
            atomic_write(intent_path, canonical_json(intent) + b"\n", 0o600)
            result = service.recover(op)
            self.assertEqual(result["error_code"], "recovery_invalid")


def _confirmation_event(preview: dict, **overrides) -> dict:
    """构造与 preview 结果 hash 绑定的 operation-confirmation/v1 事件。"""
    from tools.common import hash_canonical

    event = {
        "schema_version": "operation-confirmation/v1",
        "operation_id": preview["operation_id"],
        "scope": "apply",
        "actor_type": "human",
        "actor_id": "alice",
        "input_hash": preview["input_hash"],
        "diff_hash": preview["diff_hash"],
    }
    event.update(overrides)
    event.setdefault("event_sha256", hash_canonical(event))
    return event


class ApplyConfirmationTests(unittest.TestCase):
    """AC-F004-006：确认事件绑定（human actor + hash 匹配 + 一次性消费）。"""

    def test_confirmation_event_applies_and_binds_durable_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            event = _confirmation_event(preview)
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=event
            )
            self.assertEqual(result["state"], "applied")
            audit = json.loads(
                (
                    root / "audit" / "operations" / f"{preview['operation_id']}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(
                audit["confirmation"]["event_sha256"], event["event_sha256"]
            )
            self.assertEqual(audit["confirmation"]["actor_type"], "human")
            # 事件只消费一次：重复 apply 幂等返回原结果
            self.assertEqual(
                service.apply(
                    preview["operation_id"], confirmed=True, confirmation=event
                )["state"],
                "applied",
            )

    def test_confirmation_wrong_hash_fails_closed_without_writes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            forged = _confirmation_event(preview, input_hash="sha256:forged")
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=forged
            )
            self.assertEqual(result["state"], "blocked")
            self.assertEqual(result["error_code"], "confirmation_hash_mismatch")
            self.assertFalse((root / "a.md").exists())

    def test_confirmation_rejects_agent_actor(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            agent = _confirmation_event(preview, actor_type="agent")
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=agent
            )
            self.assertEqual(result["error_code"], "confirmation_actor_invalid")
            self.assertFalse((root / "a.md").exists())


class ConfirmationBoundaryTests(unittest.TestCase):
    """AC-F004-011：确认事件 3→2 合并后的词表边界。"""

    def test_public_release_is_not_a_legal_scope_value(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            masquerade = _confirmation_event(preview, scope="public_release")
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=masquerade
            )
            self.assertEqual(result["error_code"], "confirmation_scope_invalid")

    def test_publish_private_scope_requires_publish_fields(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"wiki/secret.md": "internal"})
            partial = _confirmation_event(
                preview, scope="publish_private"
            )  # 缺 content/evidence/target_vault
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=partial
            )
            self.assertEqual(result["error_code"], "confirmation_fields_missing")
            complete = _confirmation_event(
                preview,
                scope="publish_private",
                content_sha256="sha256:c",
                evidence_sha256="sha256:e",
                target_vault="public",
            )
            self.assertEqual(
                service.apply(
                    preview["operation_id"], confirmed=True, confirmation=complete
                )["state"],
                "applied",
            )


class RealProjectionRebuildTests(unittest.TestCase):
    """AC-F004-009：public apply 默认重建真实 public projection。"""

    def test_public_apply_rewrites_public_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"a.md": "new"})
            self.assertEqual(
                service.apply(preview["operation_id"], confirmed=True)["state"],
                "applied",
            )
            self.assertTrue((root / "queries" / "public" / "manifest.json").is_file())

    def test_projection_failure_pending_then_real_recover(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"a.md": "new"})
            obstacle = root / "queries" / "public" / "manifest.json"
            obstacle.parent.mkdir(parents=True)
            obstacle.mkdir()  # 目录占位使 manifest 原子写失败
            result = service.apply(preview["operation_id"], confirmed=True)
            self.assertEqual(result["state"], "applied_index_pending")
            self.assertEqual(result["error_code"], "projection_failed")
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "new")
            obstacle.rmdir()
            recovered = service.recover(preview["operation_id"])
            self.assertEqual(recovered["state"], "applied")
            self.assertTrue((root / "queries" / "public" / "manifest.json").is_file())
            self.assertEqual(
                service.store.load(preview["operation_id"])["state"], "applied"
            )


class ConcurrentApplyTests(unittest.TestCase):
    """AC-F004-003：并发 apply 只有一个胜者，仓库无半成品。"""

    def test_two_concurrent_applies_produce_single_consistent_result(self):
        import sys

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            ops = [
                service.preview({"shared.md": body})["operation_id"]
                for body in ("first", "second")
            ]
            runner = (
                "import sys, json; from pathlib import Path; "
                "from tools.write_operation import WriteOperation; "
                f"print(json.dumps(WriteOperation(Path({str(root)!r}), projection_rebuilder=lambda r: None)"
                ".apply(sys.argv[1], confirmed=True)))"
            )
            procs = [
                subprocess.Popen(
                    [sys.executable, "-c", runner, op],
                    cwd=Path(__file__).resolve().parents[1],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for op in ops
            ]
            outputs = []
            for proc in procs:
                out, err = proc.communicate(timeout=30)
                outputs.append(json.loads(out.strip().splitlines()[-1]))
            applied = [o for o in outputs if o.get("state") == "applied"]
            self.assertEqual(len(applied), 1)
            for output in outputs:
                self.assertIn(
                    output.get("state"), {"applied", "expired", "blocked"}
                )  # 全部结构化，无崩溃
                self.assertNotIn(
                    output.get("error_code"), {"apply_failed"}
                )  # 无半成品失败
            content = (root / "shared.md").read_text(encoding="utf-8")
            self.assertIn(content, {"first", "second"})
            self.assertEqual(
                len(content.encode()), len(content)
            )  # 单一完整内容，非交叠


class ReviewFixTests(unittest.TestCase):
    """2026-08-28 复审修复：F-1 状态翻转、F-2 event_sha256 必填。"""

    def test_intent_cleanup_failure_keeps_applied_state_with_warning(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            op = preview["operation_id"]
            event = _confirmation_event(preview)

            class BoomIntentPath(
                type(root / "state" / "commit-intents" / f"{op}.json")
            ):
                def unlink(self, missing_ok: bool = False) -> None:
                    raise OSError("permission")  # 仅 intent 清理失败，不波及锁清理

            real_intent = service.store.paths.commit_intent_file
            service.store.paths.commit_intent_file = lambda operation_id: (
                BoomIntentPath(str(real_intent(operation_id)))
            )
            result = service.apply(op, confirmed=True, confirmation=event)
            self.assertEqual(result["state"], "applied")  # F-1：不再翻转为 expired
            self.assertEqual(result.get("warnings"), ["intent_cleanup_failed"])
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "new")
            self.assertEqual(service.store.load(op)["state"], "applied")

    def test_confirmation_without_event_sha256_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "new"})
            stripped = _confirmation_event(preview)
            stripped.pop("event_sha256")
            result = service.apply(
                preview["operation_id"], confirmed=True, confirmation=stripped
            )
            self.assertEqual(result["error_code"], "confirmation_fields_missing")  # F-2
            self.assertFalse((root / "a.md").exists())


if __name__ == "__main__":
    unittest.main()


class ConfirmApplyCliTests(unittest.TestCase):
    """② confirm-apply：hash 从 durable record 派生，生成与使用分离。"""

    def test_confirm_apply_generates_validatable_event_end_to_end(self):
        import subprocess
        import sys
        import tempfile as td

        from tools.operation_store import (
            OperationStore,
            build_apply_confirmation,
            validate_apply_confirmation,
        )

        with td.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "hello"})
            op = preview["operation_id"]
            store = OperationStore(root)
            # 缺 content hash 的 publish_private 拒绝
            event, err = build_apply_confirmation(
                store, op, "alice", scope="publish_private"
            )
            self.assertEqual(err, "confirmation_fields_missing")
            # 非 previewed / 不存在 fail-closed
            self.assertEqual(
                build_apply_confirmation(store, "op_missing", "alice")[1],
                "operation_not_found",
            )
            # 正常生成 + 自校验
            event, err = build_apply_confirmation(store, op, "alice")
            self.assertIsNone(err)
            self.assertEqual(event["input_hash"], preview["input_hash"])
            record = store.load(op)
            self.assertIsNone(validate_apply_confirmation(record, event))
            # CLI 端到端：confirm-apply 生成 -> write --apply --confirmation 消费
            repo = Path(__file__).resolve().parents[1]
            out = root / "event.json"
            gen = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.cli",
                    "confirm-apply",
                    op,
                    "--root",
                    str(root),
                    "--actor-id",
                    "alice",
                    "--out",
                    str(out),
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(gen.returncode, 0, gen.stderr)
            applied = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.cli",
                    "write",
                    "--root",
                    str(root),
                    "--apply",
                    op,
                    "--confirm",
                    "--confirmation",
                    str(out),
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertIn('"state": "applied"', applied.stdout)
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "hello")

    def test_confirm_apply_rejects_expired_operation(self):
        import tempfile as td

        from tools.operation_store import OperationStore, build_apply_confirmation

        with td.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root, projection_rebuilder=lambda r: None)
            preview = service.preview({"a.md": "x"})
            store = OperationStore(root)
            record = store.load(preview["operation_id"])
            record["created_at"] = 0  # 强制过期
            from tools.common import atomic_write, canonical_json

            atomic_write(
                root / "state" / "operations" / f"{preview['operation_id']}.json",
                canonical_json(record),
                0o600,
            )
            self.assertEqual(
                build_apply_confirmation(store, preview["operation_id"], "alice")[1],
                "operation_expired",
            )


class IndexAutoRebuildTests(unittest.TestCase):
    """F005 接线：public apply 自动重建默认 FTS5 索引。"""

    def test_public_apply_rebuilds_default_index(self):
        with tempfile.TemporaryDirectory() as d:
            from tools.indexing import default_public_index_path

            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"wiki/x.md": "# x\n正文"})
            result = service.apply(preview["operation_id"], confirmed=True)
            self.assertEqual(result["state"], "applied", result)
            idx = default_public_index_path(root)
            self.assertTrue(idx.exists())  # 写入后索引自动重建，无需手动 rebuild
