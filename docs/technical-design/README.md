# Technical Design 实现设计

Technical Design 回答“如何实现”，不取代系统规范，也不记录长期决策历史。

## 必须编写的情况

- 跨越两个以上模块；
- 修改持久化 schema；
- 涉及失败恢复、幂等、锁或原子性；
- 引入外部依赖；
- 涉及公开/私有边界；
- 存在不可逆迁移或多个合理实现。

## 模板

每份实现设计应包含：目标与非目标、当前基线、模块边界、数据模型、接口契约、正常流程、失败流程、幂等与并发、安全边界、可观测性、测试策略、迁移回滚和未决问题。

## P0 设计

- [Source 导入与归档](./source-ingestion-and-archive.md)
- [Wiki Claim 验证](./wiki-claim-validation.md)
- [写操作与锁](./write-operation-and-locking.md)
