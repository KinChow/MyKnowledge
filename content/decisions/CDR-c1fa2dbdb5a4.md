---
actor_id: local-user
content_verdict: downgrade
duplicate_legacy_paths:
- legacy_path: docs/computer-science/applied-computer-science/software-engineering/implementation/c++/compilation/compilers-on-linux.md
  source_ids:
  - compilers-on-linux
  - linux-compilers
- legacy_path: docs/computer-science/applied-computer-science/software-engineering/implementation/c++/feature/key-words/key-words.md
  source_ids:
  - cpp-key-words
  - key-words
- legacy_path: docs/computer-science/applied-computer-science/software-engineering/performance-optimization/a-guide-of-compiler-vectorization/a-guide-of-compiler-vectorization.md
  source_ids:
  - a-guide-of-compiler-vectorization
  - compiler-vectorization-guide
- legacy_path: docs/computer-science/applied-computer-science/software-engineering/tools/git/commands/commands.md
  source_ids:
  - git-commands
  - git-commands
- legacy_path: docs/computer-science/computer-systems/computer-architecture-and-organization/processor/types/cpu/arm/neon/neon.md
  source_ids:
  - arm-neon
  - neon
- legacy_path: docs/computer-science/computer-systems/computer-architecture-and-organization/processor/types/cpu/overview/history.md
  source_ids:
  - cpu-history
  - history
id: CDR-c1fa2dbdb5a4
plan_sha256: sha256:c1fa2dbdb5a4ecd1d752a9a0d35d810bf8d116afbb25582ee1ad37687d75d2d8
relocated_count: 158
relocated_source_ids:
- a-guide-of-compiler-vectorization
- adb
- android-camera-architecture
- architecture-and-organization
- arm-neon
- arm-software-optimization
- arrays
- auto-focus
- auto-white-balance
- avl-tree
- b-tree
- bad-smells-in-code
- basic-of-color
- binary-search-tree
- binary-tree
- black-level-correction
- c-class-and-raii
- c-concurrent-programming-and-cuda
- c-vs-c
- c-vs-java
- c-vs-python
- calculate-mode
- circular-linked-list
- cl-mem
- class-and-structure
- class-diagram
- collaboration-diagram
- color-aberration-correction
- color-correction-and-3d-lut
- color-enhancement
- common-performance-design-patterns
- compilation-and-runtime-optimization
- compilation-principle
- compiler-vectorization-guide
- compilers-on-linux
- compilers-on-windows
- component-diagram
- computer-performance-and-power-consumption
- configuration
- conversion
- cpp-key-words
- cpp-overview
- cpp
- cpu-and-memory
- cpu-cache-optimization
- cpu-history
- data-structure-optimization
- davinci
- defective-pixel-correction
- deployment-diagram
- developer-test
- device-frequency
- doubly-circular-linked-list
- doubly-linked-list
- dumpsys
- dynamic-range-compression
- example
- fastboot
- feature
- flash
- four-rules-of-simple-desgin
- frequency-domain-noise-reduction
- gamma
- gcc
- gdb
- general-principles
- generic-tree
- git-commands
- gpu-overview
- green-balance-correction
- harvard-architecture
- hdr
- highgui
- history
- huawei-camera
- ifconfig
- image-scaling
- image-sharpening
- image-stabilization
- instructions
- ips
- key-words
- kirin-9000s
- lens-vignetting-correction
- limitations-of-local-work-size-and-global-work-size
- linux-commands
- linux-compilers
- linux-performance-tools
- lod
- loop-optimization
- mali-bifrost-gpu-compute
- mali-gpu-overview
- matrix
- metrics-and-optimization-processes
- multi-core-software-design
- neon-intrinsics-checklist
- neon
- noise-evaluation
- object-diagram
- object-oriented
- opencl-optimization-guideline
- opencl-optimizations-list
- opencl
- opencv
- operations
- optimizing-opencl-for-maleoon-gpus
- optimizing-opencl-for-mali-gpus
- overview-of-3a
- overview-of-opencl
- performance-indicator
- process-and-thread
- process-optimization
- queue
- random
- red-black-tree
- refactoring-concepts-and-principles
- refactoring-techniques
- reference
- requirements-analysis
- sequence-diagram
- significance
- simpleperf
- singly-linked-list
- snapdragon-8gen1
- soc
- software-design
- software-modeling
- solid
- source-4ed827b8730d
- space-domain-noise-reduction
- stack
- start-a-opencl-project-on-visual-studio-using-nvidia-gpu
- statechart-diagram
- statement-optimization
- systrace
- time-domain-noise-reduction
- tonemapping
- transformer
- types
- uml
- use-case-diagram
- von-neumann-architecture
- auto-exposure
- demosaic
- image-file-format
- image-quality-assessment
- isp-system
- optical-fundamentals
- sensor
- terminology
- code-server
- git-commands
- a-day-of-a-programmer
- insight
- ipd
- model
- reading-notes
- report
retained_source_ids:
- aar
- how-to-read-a-book
---
# 存量 source 整批降级落位

## 判定

158 篇被误登记为 `source/v1` 的加工文档整批降级到 `content/working/`。它们不是外部来源的快照，而是本人整理的加工内容——登记为 source 会让引用它们的 wiki 看起来有外部证据支撑（可派生 `verified`/`attested`），这是失真。

## 保留项

aar, how-to-read-a-book：被保留的 wiki 通过 `sources`/`evidence.targets` 实际引用，搬走会让那些页面 `evidence_state` 变 `unresolved`。

## 重复导入

6 组同一 `legacy_path` 被导入成多个 source（清单见 front matter `duplicate_legacy_paths`）。降级阶段两份都落位、不做内容取舍：去重属于逐篇升级时的判断，批量阶段替人选一份等于替人做内容决策。

## 不做的事

- `archive/` 快照与 `manifest.jsonl` 一律不动：曾经导入过是事实，append-only 账目不因改判而重写；
- 不批量升级进 `content/wiki/`：升级是逐篇人工动作（CHN-001）。
