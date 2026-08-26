"""pytest 共享配置：显式将 tests/ 根加入 sys.path。

pytest 默认 prepend 模式会把 conftest.py 所在目录隐式加入 sys.path，但该机制
对 --import-mode=importlib 或直接运行单文件不成立；子目录测试（ingest/validation/
anchor）依赖此路径 import wiki_fixtures，故显式声明。
"""

import sys
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))
