---
archive_policy: text-only
attachments:
- filename: aosp-camera-metadata.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-ec5493ad2bf0
  position:
    end: 495
    start: 329
    type: TextPositionSelector
  quote_sha256: sha256:54ab4ca3ab9e0c7b7daf98d18573a1fb76feeda70dab1ee97ec52bfb9108e672
  selector:
    exact: Most of this information is a static property of the camera subsystem and
      can therefore be queried before configuring any output pipelines or submitting
      any requests.
    prefix: 'ces and lens shading functions. '
    suffix: '


      In addition, manual control of'
    type: TextQuoteSelector
  selector_sha256: sha256:4dd428b8f20ceebd47fc8bf4491090ea1c75cd0d3c2a2a9137f9c099e4b2872d
  snapshot_sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
- evidence_id: evidence-ccd5ac3651b7
  position:
    end: 1499
    start: 1246
    type: TextPositionSelector
  quote_sha256: sha256:b0ea99e1d013e49f40c54b5370273fd57ba13eedf2eda94572990999672ca677
  selector:
    exact: the new camera API adds a substantial amount of dynamic metadata to each
      captured frame. This includes the requested and actual parameters used for the
      capture, as well as additional per-frame metadata such as timestamps and statistics
      generator output.
    prefix: 'or the next request. Therefore, '
    suffix: '


      For most settings, the expecta'
    type: TextQuoteSelector
  selector_sha256: sha256:5bf435efc9292c9ce5dac5ba7fcb08c3194da9b2ae266f6f434dd44198eb7508
  snapshot_sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
- evidence_id: evidence-5fc4b7551293
  position:
    end: 1653
    start: 1501
    type: TextPositionSelector
  quote_sha256: sha256:2b7ae9b08681db8d13405d07923735e4f8ef8ce7ca5e9d6407b3203336b24411
  selector:
    exact: For most settings, the expectation is that they can be changed every frame,
      without introducing significant stutter or delay to the output frame stream.
    prefix: 'd statistics generator output.


      '
    suffix: ' Ideally, the output frame rate '
    type: TextQuoteSelector
  selector_sha256: sha256:053506ed4373aeaae3c43361b1e4fb3b17201ea2dab38eaa8320d01ce5ee1543
  snapshot_sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
extractor: utf8/1
id: aosp-camera-metadata
local:
  file_sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
  path_ref: local-sidecar:public/aosp-camera-metadata
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a.txt
  sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:fa6fc0f34df798eb3778d189bc634c84eee14db0dda752823f9e3d63877cf37a
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/camera/camera3_metadata (Metadata and controls, retrieved 2026-09-04)

To support the saving of raw image files by the Android framework, substantial metadata is required about the sensor's characteristics. This includes information such as color spaces and lens shading functions. Most of this information is a static property of the camera subsystem and can therefore be queried before configuring any output pipelines or submitting any requests.

In addition, manual control of the camera subsystem requires feedback from the assorted devices about their current state, and the actual parameters used in capturing a given frame. The actual values of the controls (exposure time, frame duration, and sensitivity) as actually used by the hardware must be included in the output metadata. This is essential so that apps know when either clamping or rounding took place, and so that the app can compensate for the real settings used for image capture.

So if an app needs to implement a custom 3A routine (for example, to properly meter for an HDR burst), it needs to know the settings used to capture the latest set of results it has received to update the settings for the next request. Therefore, the new camera API adds a substantial amount of dynamic metadata to each captured frame. This includes the requested and actual parameters used for the capture, as well as additional per-frame metadata such as timestamps and statistics generator output.

For most settings, the expectation is that they can be changed every frame, without introducing significant stutter or delay to the output frame stream. Ideally, the output frame rate should solely be controlled by the capture request's frame duration field, and be independent of any changes to processing blocks' configuration. In reality, some specific controls are known to be slow to change; these include the output resolution and output format of the camera pipeline, as well as controls that affect physical devices, such as lens focus distance.
