"""pytest 共享配置：显式将 tests/ 根加入 sys.path。

pytest 默认 prepend 模式会把 conftest.py 所在目录隐式加入 sys.path，但该机制
对 --import-mode=importlib 或直接运行单文件不成立；子目录测试（ingest/validation/
anchor）依赖此路径 import wiki_fixtures，故显式声明。
"""

import sys
from pathlib import Path

import pytest

TESTS_ROOT = Path(__file__).resolve().parent
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))


@pytest.fixture
def real_import():
    """真实导入工厂：跑一遍 SourceIngestor preview+apply，返回落盘的 manifest 条目。

    manifest / archive / source 三者的形态都由生产代码产生——手写 fixture 一旦
    与生产结构漂移，测试会继续通过（伪绿）。
    """

    def _import(root: Path, body: str, source_id: str) -> dict:
        import json

        from tools.archive_manifest import ArchiveManifest
        from tools.ingest.source_ingestor import SourceIngestor

        ingestor = SourceIngestor(root)
        operation = ingestor.preview(
            {
                "source_type": "personal-note",
                "domain": "tools",
                "origin": "personal",
                "body": body,
                "source_id": source_id,
            }
        )
        applied = ingestor.apply(operation["operation_id"], confirmed=True)
        assert applied["state"] == "applied", applied
        manifest = ArchiveManifest(root)
        return json.loads(
            manifest.path.read_text(encoding="utf-8").strip().splitlines()[-1]
        )

    return _import
