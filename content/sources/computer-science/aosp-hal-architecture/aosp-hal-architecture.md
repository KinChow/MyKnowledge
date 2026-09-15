---
archive_policy: text-only
attachments:
- filename: aosp-hal-architecture.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d8e44be806f4
  position:
    end: 390
    start: 125
    type: TextPositionSelector
  selector:
    exact: A hardware abstraction layer (HAL) is type of abstraction layer with a
      standard interface for hardware vendors to implement. A HAL allows hardware
      vendors to implement lower-level, device-specific features without affecting
      or modifying code in higher-level layers.
    prefix: 'verview, retrieved 2026-09-04)


      '
    suffix: '


      The hardware-specific code, su'
    type: TextQuoteSelector
  snapshot_sha256: sha256:854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0
- evidence_id: evidence-ffb3b59c768e
  position:
    end: 778
    start: 714
    type: TextPositionSelector
  selector:
    exact: HIDL enables communication between HAL clients and HAL services.
    prefix: 'rogramming language being used. '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0
extractor: utf8/1
id: aosp-hal-architecture
local:
  file_sha256: sha256:854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0
  path_ref: local-sidecar:public/aosp-hal-architecture
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:854c19736c36a644ee60e5fcb93eb2a644eb6a597ac6d8c03d9690e73a6b8fc0
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/architecture/hal (Hardware abstraction layer overview, retrieved 2026-09-04)

A hardware abstraction layer (HAL) is type of abstraction layer with a standard interface for hardware vendors to implement. A HAL allows hardware vendors to implement lower-level, device-specific features without affecting or modifying code in higher-level layers.

The hardware-specific code, such as the code that talks to your specific device's camera. You must implement all required HALs listed in the compatibility matrix for the release you target in your vendor partition.

A language used to define interfaces in a way that is independent of the programming language being used. HIDL enables communication between HAL clients and HAL services.
