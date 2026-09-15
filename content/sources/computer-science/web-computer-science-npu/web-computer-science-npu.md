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
  snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
- evidence_id: evidence-5df13bc15608
  position:
    end: 542
    start: 358
    type: TextPositionSelector
  selector:
    exact: Their purpose is either to efficiently execute already trained AI models
      like LLMs (inference) or to train AI models. NPUs can be more efficient in terms
      of speed or power consumption.
    prefix: 't of a CPU or a part of a GPU.


      '
    suffix: '


      An operating system or a highe'
    type: TextQuoteSelector
  snapshot_sha256: sha256:be20178b6fa0b3dcfe94063b454866388c10058280e69fb495308f9c119e73fe
- evidence_id: evidence-e867730dc7d6
  position:
    end: 1329
    start: 1026
    type: TextPositionSelector
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
