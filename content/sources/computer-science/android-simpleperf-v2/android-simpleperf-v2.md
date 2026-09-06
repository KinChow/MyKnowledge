---
archive_policy: text-only
attachments:
- filename: android-simpleperf-v2.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-5962807915ae
  position:
    end: 145
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:f9770332d5bc8e1cf20c9c6e2619fb255377c6479947bfeb2908cff0a75310cd
  selector:
    exact: If you prefer to use the command line, Simpleperf is a versatile command-line
      CPU profiling tool included in the NDK for Mac, Linux, and Windows.
    prefix: ''
    suffix: '


      For full documentation, start '
    type: TextQuoteSelector
  selector_sha256: sha256:3f1723389a00fd3c7710d4561223e61c6705c7cc571146ae769bbf7ae1beb31d
  snapshot_sha256: sha256:6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a
extractor: utf8/1
id: android-simpleperf-v2
local:
  file_sha256: sha256:6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a
  path_ref: local-sidecar:public/android-simpleperf-v2
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a.txt
  sha256: sha256:6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a
read_status: retrieved
retrieval:
  acquisition: local-file
  url: https://developer.android.com/ndk/guides/simpleperf?hl=en
schema_version: source/v1
snapshot_sha256: sha256:6540368820500846673bc1968dc8a6aeccab0948337e6327f6d29b115a4a637a
source_type: local-file
vault_id: public
---
If you prefer to use the command line, Simpleperf is a versatile command-line CPU profiling tool included in the NDK for Mac, Linux, and Windows.

For full documentation, start with the Simpleperf README.

You can run this command to see which .so files take up the largest percentage of execution time (based on the number of CPU cycles). This is a good first command to run when starting your performance analysis session.
$ simpleperf report --sort dso
