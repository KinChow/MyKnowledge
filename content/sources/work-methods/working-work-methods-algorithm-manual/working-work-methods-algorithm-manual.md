---
archive_policy: text-only
confidentiality: public
domain: work-methods
evidence_items:
- evidence_id: evidence-f1053c0967ab
  position:
    end: 85
    start: 9
    type: TextPositionSelector
  quote_sha256: sha256:e486dd5ebcd47e165b3c604732afbc392a5f00b00fdd73744db1a2861812540d
  selector:
    exact: 算法说明书（Algorithm Manual）是描述软件算法模块从需求到交付全流程的设计文档模板，覆盖简介、概要设计、详细设计、测试用例、问题总结与附录
    prefix: '# 算法说明书


      '
    suffix: "，作为算法开发者编写设计文档的统一规范。\n\n* 简介\n    *"
    type: TextQuoteSelector
  selector_sha256: sha256:6bf4770b04988e4366870ac83965810ec182a7bff3facf25366dcc7a3d28dea3
  snapshot_sha256: sha256:1849422188e7f44aebcc0b6b987212a128249100220f1cd3ddba171a6bbffefd
extractor: personal-note/1
id: working-work-methods-algorithm-manual
media_type: text/markdown
origin: personal
read_status: retrieved
retrieval:
  acquisition: personal-note
schema_version: source/v1
snapshot_sha256: sha256:1849422188e7f44aebcc0b6b987212a128249100220f1cd3ddba171a6bbffefd
source_type: personal-note
vault_id: public
---
# 算法说明书

算法说明书（Algorithm Manual）是描述软件算法模块从需求到交付全流程的设计文档模板，覆盖简介、概要设计、详细设计、测试用例、问题总结与附录，作为算法开发者编写设计文档的统一规范。

* 简介
    * 目的
    * 范围
        * 软件名称
        * 功能
    * 缩略图
    * 使用场景
    * 需求分解
* 概要设计
    * 总体设计思路
    * pipeline链路设计
    * 模块划分
    * 模块关系图
* 详细设计
    * 数据接口定义
        * 新增变量定义
        * 模块设计
        * 算法原理
    * 算法后处理策略
        * 算法链路
        * 算法接口
        * 性能与内存
        * 效果类问题
        * 风险
* 测试用例
* 问题总结
* 附录
