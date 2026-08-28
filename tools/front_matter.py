"""Markdown YAML front matter 的解析与渲染（python-frontmatter 库薄适配）。

来源：https://github.com/rafaelmardojai/python-frontmatter（MIT License，v1.3.0）
适配层归一库的异常面，保持调用方"仅捕获 ValueError/OSError"契约不变：
- 未闭合的 front matter → ValueError("front_matter_unterminated")
- 语法损坏的 YAML → ValueError("front_matter_invalid_yaml")
- 空 front matter（metadata 为 None）→ {}（不抛 AttributeError）
- 空 body 渲染时补闭合分隔符后的换行（库默认省略）
"""

from __future__ import annotations

import frontmatter
import yaml


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects ambiguous duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
):
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
        """解析 front matter 为 (metadata, body)；无 front matter 时返回 ({}, text)。

        body 用精确切片保留原文（含结尾换行）——python-frontmatter 的
        ``Post.content`` 会 strip 结尾换行，曾导致 render→parse roundtrip
        不保真、source 文件与 snapshot 的 hash 一致性校验系统性失败。
        metadata 解析仍复用库与重复键拒绝构造器。
        """
        if not text.startswith("---\n"):
            return {}, text
        close = text.find("\n---\n", 4)
        if close < 0:
            raise ValueError("front_matter_unterminated")
        try:
            # noqa 理由：_UniqueKeyLoader 继承 yaml.SafeLoader，仅覆写映射构造以拒绝重复键
            metadata = yaml.load(text[4:close], Loader=_UniqueKeyLoader) or {}  # noqa: S506
        except (yaml.YAMLError, ValueError) as exc:
            raise ValueError("front_matter_invalid_yaml") from exc
        if not isinstance(metadata, dict):
            raise ValueError("front_matter_invalid_yaml")
        return metadata, text[close + 5 :]

    @staticmethod
    def render(metadata: dict, body: str) -> str:
        """将 metadata 与 body 渲染为 front matter 格式的 Markdown 文本。

        header 序列化复用库输出；body 由适配层原样拼接——库的
        ``dumps`` 会在闭合分隔符后额外插入空行并剥 body 结尾换行，
        曾导致 render→parse roundtrip 不保真、source 文件与 snapshot
        的 hash 一致性校验系统性失败。body 原样保证与 acquired.body
        字节一致。
        """
        # 占位正文确保库输出完整闭合分隔符（空 content 时库会省略）
        header = frontmatter.dumps(frontmatter.Post("X", **metadata))
        prefix = header.split("\n---\n", 1)[0] + "\n---\n"
        return prefix + body
