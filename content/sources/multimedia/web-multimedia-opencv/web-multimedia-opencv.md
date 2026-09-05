---
archive_policy: text-only
attachments:
- filename: web-multimedia-opencv.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:46cfce64675433f62618e520e774b897b45da59f2c716f987abc770265403ce5
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-7e6069f3047b
  position:
    end: 287
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:9c091ae29215e78834a8f8c0708a65949deb8680fcdd2b949ede1c10a745e3da
  selector:
    exact: 'OpenCV documentation#

      OpenCV (Open Source Computer Vision Library) is an open-source computer vision
      and machine learning software library. It has more than 2,500 optimised algorithms,
      a comprehensive mix of both classic and state-of-the-art computer vision and
      machine learning methods.'
    prefix: ''
    suffix: ' These can be used to detect and'
    type: TextQuoteSelector
  selector_sha256: sha256:e9ab3f7e064186bd1bc49f2d63a13049aad25926f39947d84fa2884b6b0c8d88
  snapshot_sha256: sha256:0a0221fc82e90f9017e097dfbf9ac952e269d04f29899da3da12f71f59f5571a
extractor: trafilatura/2.2.0
id: web-multimedia-opencv
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/46cfce64675433f62618e520e774b897b45da59f2c716f987abc770265403ce5.html
  sha256: sha256:46cfce64675433f62618e520e774b897b45da59f2c716f987abc770265403ce5
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://docs.opencv.org/5.0/
  url: https://docs.opencv.org/
schema_version: source/v1
snapshot_sha256: sha256:0a0221fc82e90f9017e097dfbf9ac952e269d04f29899da3da12f71f59f5571a
source_type: doc
vault_id: public
---
OpenCV documentation#
OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. It has more than 2,500 optimised algorithms, a comprehensive mix of both classic and state-of-the-art computer vision and machine learning methods. These can be used to detect and recognise faces, identify objects, classify human actions in video, track camera and object motion, extract 3D models, stitch images together to produce high-resolution panoramas, and much more. The library has interfaces for C++, Python, Java, and JavaScript, runs on Windows, Linux, macOS, Android, and iOS, and accelerates work on CPU (SIMD), CUDA, OpenCL, and Vulkan.
OpenCV 5.0 is a major release built on OpenCV 4.x. C++17 is now the minimum required standard, Python 2 support has been dropped (Python 3.6+ is required), and the legacy C API has been fully removed. New data types (CV_16BF, CV_32U, CV_64U, CV_64S, CV_Bool) and proper 0D/1D array support extend the core, while the former calib3d module is split into the geometry, calib, stereo, and ptcloud modules. A next-generation DNN engine now covers over 80% of the ONNX specification (up from under 23%), with ONNX Runtime integration and models hosted on Hugging Face. Performance gains include Universal Intrinsics 2.0 (SSE/AVX/NEON/SVE/RISC-V), Vulkan compute support, image-warping speed-ups of 10% to over 300%, and USAC as the default framework for robust estimation.