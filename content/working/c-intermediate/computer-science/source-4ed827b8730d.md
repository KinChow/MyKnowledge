---
domain: computer-science
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/software-engineering/design/software-design/design-principles/正交四原则.md
snapshot_sha256: sha256:c6ab6f9d0fa9a163eadc2ce44de2db6e8aaaba44e33350a2f9dbe3e4ed3220e9
title: 正交四原则
---
# 正交四原则

## 最小化重复

重复意味着耦合；当重复的代码需要修改时，容易出现漏改的情景



## 分离变化

识别变化方向并对变化预留扩展接口。而这个扩展接口必须反映变化方向的本质特点（稳定接口），为了更好复用和使用的简洁性，多个接口不能纠缠在一起



## 缩小依赖范围

最小化知识原则；依赖接口，不要依赖实现；接口应该尽可能包含少的知识



## 向稳定方向依赖

定义API时应该关注what，而不是how，站在需求的角度去定义API，而不是实现的方式定义API。要站在用户的角度去定义API，而不是站在实现者的角度。因为接口是抽象的，是稳定的，实现是不稳定的
