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
  quote_sha256: sha256:d72970201858a35ab1f6891c98470dfe6cbe3b5f590476622a01cbca899badd6
  selector:
    exact: The HAL sits between the camera driver and the higher-level Android framework
      and defines an interface that you must implement so apps can correctly operate
      the camera hardware.
    prefix: 'r version of these components.


      '
    suffix: ' The HIDL interfaces for the Cam'
    type: TextQuoteSelector
  selector_sha256: sha256:406b1e6d57dd2e77f1189c203d3929d82a6d640a580fb8b5e4bad10710f2986e
  snapshot_sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
- evidence_id: evidence-8a33cfacf842
  position:
    end: 264
    start: 108
    type: TextPositionSelector
  quote_sha256: sha256:a8220121c4dbeb220ac4133dbe912ea366406ff9f6474734fbdd4dece08bff84
  selector:
    exact: Android's camera hardware abstraction layer (HAL) connects the higher-level
      camera framework APIs in Camera 2 to your underlying camera driver and hardware.
    prefix: 'verview, retrieved 2026-09-04)


      '
    suffix: ' The camera subsystem includes i'
    type: TextQuoteSelector
  selector_sha256: sha256:a26e5b84e2ad6be26e214cffd4611cb98bccb33a2d4b55b5348c33ebf1b8c750
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
  sha256: sha256:1de539a835d27fd8a30a86ca5187cfe596452baa8fe000a38817e0a237b5f359
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
