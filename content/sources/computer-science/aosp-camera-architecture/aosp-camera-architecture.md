---
archive_policy: text-only
attachments:
- filename: aosp-camera-architecture.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d937f440c251
  position:
    end: 619
    start: 442
    type: TextPositionSelector
  selector:
    exact: The HAL sits between the camera driver and the higher-level Android framework
      and defines an interface that you must implement so apps can correctly operate
      the camera hardware.
    prefix: 'r version of these components.


      '
    suffix: ' The HIDL interfaces for the Cam'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
- evidence_id: evidence-8a33cfacf842
  position:
    end: 264
    start: 108
    type: TextPositionSelector
  selector:
    exact: Android's camera hardware abstraction layer (HAL) connects the higher-level
      camera framework APIs in Camera 2 to your underlying camera driver and hardware.
    prefix: 'verview, retrieved 2026-09-04)


      '
    suffix: ' The camera subsystem includes i'
    type: TextQuoteSelector
  snapshot_sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
extractor: utf8/1
id: aosp-camera-architecture
local:
  file_sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
  path_ref: local-sidecar:public/aosp-camera-architecture
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/camera (Camera architecture overview, retrieved 2026-09-04)

Android's camera hardware abstraction layer (HAL) connects the higher-level camera framework APIs in Camera 2 to your underlying camera driver and hardware. The camera subsystem includes implementations for camera pipeline components while the camera HAL provides interfaces for use in implementing your version of these components.

The HAL sits between the camera driver and the higher-level Android framework and defines an interface that you must implement so apps can correctly operate the camera hardware. The HIDL interfaces for the Camera HAL are defined in hardware/interfaces/camera.
