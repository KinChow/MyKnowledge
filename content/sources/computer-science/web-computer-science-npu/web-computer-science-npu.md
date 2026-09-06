---
archive_policy: text-only
attachments:
- filename: web-computer-science-npu.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-1954a2deedbb
  position:
    end: 356
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:3ff6b64a3cc166394e2560677b772fe54df3a755ea3e6edfd0ba4e11094899a5
  selector:
    exact: A neural processing unit (NPU), also known as an AI accelerator or deep
      learning processor, is a class of specialized hardware accelerator or computer
      system designed to accelerate artificial intelligence and machine learning applications,
      including artificial neural networks and computer vision. NPU can be standalone,
      a part of a CPU or a part of a GPU.
    prefix: ''
    suffix: '


      Their purpose is either to eff'
    type: TextQuoteSelector
  selector_sha256: sha256:d3bfa709ba358bda17c03a0265ccbb033c86856669a85f0b194db32d17893052
  snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
- evidence_id: evidence-5df13bc15608
  position:
    end: 542
    start: 358
    type: TextPositionSelector
  quote_sha256: sha256:d9f2006eda016aae0014f1680c43637dd3affb112d0f069eabee2a1e307b2103
  selector:
    exact: Their purpose is either to efficiently execute already trained AI models
      like LLMs (inference) or to train AI models. NPUs can be more efficient in terms
      of speed or power consumption.
    prefix: 't of a CPU or a part of a GPU.


      '
    suffix: '


      An operating system or a highe'
    type: TextQuoteSelector
  selector_sha256: sha256:204b4b29fc7e67879f70b2bb18d6151cd74991cfa607875b82fbc5013d8df0f3
  snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
- evidence_id: evidence-e867730dc7d6
  position:
    end: 1329
    start: 1026
    type: TextPositionSelector
  quote_sha256: sha256:9b9245a8658aca9d899aba562548a4e9d1d2ed4f72ee15bfd48ec5cbf9b9e13f
  selector:
    exact: Since the late 2010s, graphics processing units designed by companies such
      as Nvidia and AMD often include AI-specific hardware in the form of dedicated
      functional units for low-precision matrix-multiplication operations. These GPUs
      are commonly used as AI accelerators, both for training and inference.
    prefix: 'pon by a higher-level library.


      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:218c5601f2c529c2e4d5bb3385e34a2b97c5353fb7874792f0507aa7d153b1c9
  snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
extractor: utf8/1
id: web-computer-science-npu
local:
  file_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
  path_ref: local-sidecar:public/web-computer-science-npu
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe.txt
  sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
source_type: local-file
vault_id: public
---
A neural processing unit (NPU), also known as an AI accelerator or deep learning processor, is a class of specialized hardware accelerator or computer system designed to accelerate artificial intelligence and machine learning applications, including artificial neural networks and computer vision. NPU can be standalone, a part of a CPU or a part of a GPU.

Their purpose is either to efficiently execute already trained AI models like LLMs (inference) or to train AI models. NPUs can be more efficient in terms of speed or power consumption.

An operating system or a higher-level library may provide application programming interfaces such as TensorFlow with LiteRT Next (Android), CoreML (iOS, macOS) or DirectML (Windows). Formats such as ONNX are used to represent trained neural networks.

Consumer CPU-integrated NPUs are accessible through vendor-specific APIs. AMD (Ryzen AI), Intel (OpenVINO), Apple silicon (CoreML), and Qualcomm (SNPE) each have their own APIs, which can be built upon by a higher-level library.

Since the late 2010s, graphics processing units designed by companies such as Nvidia and AMD often include AI-specific hardware in the form of dedicated functional units for low-precision matrix-multiplication operations. These GPUs are commonly used as AI accelerators, both for training and inference.
