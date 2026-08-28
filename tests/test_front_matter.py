"""F001 front matter 边界（共享基础设施）。"""

from __future__ import annotations

import unittest

from tools.front_matter import FrontMatter


class FrontMatterTests(unittest.TestCase):
    def test_front_matter_error_normalization(self):
        """坏 YAML → front_matter_invalid_yaml；空 front matter → {}（不穿透库异常）。"""
        with self.assertRaisesRegex(ValueError, "front_matter_invalid_yaml"):
            FrontMatter.parse("---\na: [unclosed\n---\nbody")
        metadata, body = FrontMatter.parse("---\n\n---\nbody")
        self.assertEqual(metadata, {})
        self.assertEqual(body, "body")

    def test_duplicate_yaml_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "front_matter_invalid_yaml"):
            FrontMatter.parse("---\nid: first\nid: second\n---\nbody")
