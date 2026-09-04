---
archive_policy: text-only
attachments:
- filename: aosp-camera-hal3.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-fe448cb00526
  position:
    end: 502
    start: 373
    type: TextPositionSelector
  quote_sha256: sha256:6d17c52bf99af4cb1b6895209119ed6966b5c0e4512f5cb80b7d9ad3216d74ac
  selector:
    exact: The API models the camera subsystem as a pipeline that converts incoming
      requests for frame captures into frames, on a 1:1 basis.
    prefix: 'rated for each set of results.


      '
    suffix: ' The requests encapsulate all co'
    type: TextQuoteSelector
  selector_sha256: sha256:b4c058c5fe7e5b2883fcb7dbdea30909809d4967d74407796eed417db7efa6b5
  snapshot_sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
- evidence_id: evidence-cf017f340ff1
  position:
    end: 1151
    start: 942
    type: TextPositionSelector
  quote_sha256: sha256:275b32dccc703ff483be8860ab7f6ed7972c4a47826074e446f07bdc343ea4aa
  selector:
    exact: Starting with Android 13, camera HAL interface development uses AIDL. Android
      8.0 introduced Treble, switching the Camera HAL API to a stable interface defined
      by the HAL interface description language (HIDL).
    prefix: 'ing camera driver and hardware. '
    suffix: '


      For devices running Android 13'
    type: TextQuoteSelector
  selector_sha256: sha256:7798b42ef635cb223001ec8551e3746eb42062d6d97a145bd0477b9cbf1b28ef
  snapshot_sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
extractor: utf8/1
id: aosp-camera-hal3
local:
  file_sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
  path_ref: local-sidecar:public/aosp-camera-hal3
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e.txt
  sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:0af89a0d88a8cc96e421a6df8a86ce222b8c0b83312547a9eb747c04c3eadd2e
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/camera/camera3 (Camera HAL3, retrieved 2026-09-04)

In simple terms, the application framework requests a frame from the camera subsystem, and the camera subsystem returns results to an output stream. In addition, metadata that contains information such as color spaces and lens shading is generated for each set of results.

The API models the camera subsystem as a pipeline that converts incoming requests for frame captures into frames, on a 1:1 basis. The requests encapsulate all configuration information about the capture and processing of a frame. This includes resolution and pixel format; manual sensor, lens and flash control; 3A operating modes; RAW->YUV processing control; statistics generation; and so on.

Android's camera hardware abstraction layer (HAL) connects the higher level camera framework APIs in android.hardware.camera2 to your underlying camera driver and hardware. Starting with Android 13, camera HAL interface development uses AIDL. Android 8.0 introduced Treble, switching the Camera HAL API to a stable interface defined by the HAL interface description language (HIDL).

For devices running Android 13 or higher, the camera framework includes support for AIDL camera HALs. The camera framework also supports HIDL camera HALs, however camera features added in Android 13 or higher are available only through the AIDL camera HAL interfaces. To implement such features on devices upgrading to Android 13 or higher, device manufacturers must migrate their HAL process from using HIDL camera interfaces to AIDL camera interfaces.
