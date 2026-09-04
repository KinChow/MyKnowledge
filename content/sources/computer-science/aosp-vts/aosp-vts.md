---
archive_policy: text-only
attachments:
- filename: aosp-vts.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-21f66837f09c
  position:
    end: 193
    start: 119
    type: TextPositionSelector
  quote_sha256: sha256:f970509b3e17802874a6d84ed316d749e2ae04c532c0f85b4086c98de6597af5
  selector:
    exact: Most tests in VTS are GTest-style tests that check the HAL implementation.
    prefix: 'ructure, retrieved 2026-09-04)


      '
    suffix: ' The test is written in C++ and '
    type: TextQuoteSelector
  selector_sha256: sha256:a4f423777b2072a4de9874407e4970972c78abc43eacba4a0714ff8c7e1556a7
  snapshot_sha256: sha256:baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81
extractor: utf8/1
id: aosp-vts
local:
  file_sha256: sha256:baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81
  path_ref: local-sidecar:public/aosp-vts
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81.txt
  sha256: sha256:baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:baf5fc8575c835a6cb12f631e0934ec3d1e6545928915481af5145ba38dbda81
source_type: local-file
vault_id: public
---
# Source: https://source.android.com/docs/core/tests/vts (Vendor Test Suite and infrastructure, retrieved 2026-09-04)

Most tests in VTS are GTest-style tests that check the HAL implementation. The test is written in C++ and runs on the device. A typical VTS GTest iterates through each instance of a given interface, and runs all the test cases against it.

Linux kernel tests: Kselftest is a collection of tests included within the Linux kernel repository at tools/testing/selftests, of which 23 are included in VTS to run on ARM. Linux Test Project (LTP) tests validate the reliability, robustness, and stability of the Linux kernel.

A small set of host-driven tests in VTS are JUnit-style tests. Some VTS tests, such as vts_treble_sys_prop_test, are written in Python3. The Python-based tests are implemented as unittest.TestCase and each test case can interact with the device through shell commands.
