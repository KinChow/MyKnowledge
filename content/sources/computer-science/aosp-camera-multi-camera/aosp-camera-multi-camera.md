---
archive_policy: text-only
attachments:
- filename: aosp-camera-multi-camera.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-260cce4b839f
  position:
    end: 441
    start: 113
    type: TextPositionSelector
  quote_sha256: sha256:171198795476c478d05b64fc8255b155db2de8e8bb0d3e707522a8e706ac83a4
  selector:
    exact: Android 9 introduced API support for multi-camera devices through a new
      logical camera device composed of two or more physical camera devices pointing
      in the same direction. The logical camera device is exposed as a single CameraDevice/CaptureSession
      to an app allowing for interaction with HAL-integrated multi-camera features.
    prefix: 'support, retrieved 2026-09-04)


      '
    suffix: ' Apps can optionally access and '
    type: TextQuoteSelector
  selector_sha256: sha256:33cca5f3ce4b45c4c538f918d82b0360f4f120718ef829b6184ec57448ed7224
  snapshot_sha256: sha256:0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10
extractor: utf8/1
id: aosp-camera-multi-camera
local:
  file_sha256: sha256:0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10
  path_ref: local-sidecar:public/aosp-camera-multi-camera
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10.txt
  sha256: sha256:0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:0e586bcdd84f6ddc992c2d753009dd41ceb57dd69a0bd22bb4dc72537cac6f10
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/camera/multi-camera (Multi-camera support, retrieved 2026-09-04)

Android 9 introduced API support for multi-camera devices through a new logical camera device composed of two or more physical camera devices pointing in the same direction. The logical camera device is exposed as a single CameraDevice/CaptureSession to an app allowing for interaction with HAL-integrated multi-camera features. Apps can optionally access and control underlying physical camera streams, metadata, and controls.

In the multi-camera diagram, different camera IDs are color coded. The app can stream raw buffers from each physical camera at the same time. It is also possible to set separate controls and receive separate metadata from different physical cameras.

A logical camera device should operate in the same way as a physical camera device based on its hardware level and capabilities. It's recommended that its feature set is a superset of that of individual physical cameras.
