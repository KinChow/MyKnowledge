"""Markdown YAML front matter 的解析与渲染（python-frontmatter 库薄适配）。

来源：https://github.com/rafaelmardojai/python-frontmatter（MIT License，v1.3.0）
适配层归一库的异常面，保持调用方"仅捕获 ValueError/OSError"契约不变：
- 未闭合的 front matter → ValueError("front_matter_unterminated")
- 语法损坏的 YAML → ValueError("front_matter_invalid_yaml")
- 空 front matter（metadata 为 None）→ {}（不抛 AttributeError）
- 空 body 渲染时补闭合分隔符后的换行（库默认省略）
"""

from __future__ import annotations

import yaml
import frontmatter


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects ambiguous duplicate mapping keys."""


def _construct_unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate_yaml_key:{key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


class FrontMatter:
    """Markdown YAML front matter 的解析与渲染（``---`` 包裹头部）。"""

    @staticmethod
    def parse(text: str) -> tuple[dict, str]:
        """解析 front matter 为 (metadata, body)；无 front matter 时返回 ({}, text)。"""
        if not text.startswith("---\n"):
            return {}, text
        if text.find("\n---\n", 4) < 0:
            raise ValueError("front_matter_unterminated")
        try:
            header = text[4 : text.find("\n---\n", 4)]
            yaml.load(header, Loader=_UniqueKeyLoader)
            post = frontmatter.loads(text)
        except (yaml.YAMLError, ValueError) as exc:
            raise ValueError("front_matter_invalid_yaml") from exc
        return post.metadata or {}, post.content

    @staticmethod
    def render(metadata: dict, body: str) -> str:
        """将 metadata 与 body 渲染为 front matter 格式的 Markdown 文本。

        空 body 时 python-frontmatter 省略闭合分隔符 ``---`` 后的换行，
        会破坏 :meth:`parse` 的闭合检查；适配层补一个换行保证契约恒定。
        """
        rendered = frontmatter.dumps(frontmatter.Post(body, **metadata))
        if not rendered.endswith("\n---\n") and rendered.endswith("---"):
            rendered += "\n"
        return rendered
