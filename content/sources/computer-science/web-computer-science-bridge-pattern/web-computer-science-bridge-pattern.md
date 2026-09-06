---
archive_policy: text-only
attachments:
- filename: web-computer-science-bridge-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b14e9e7ce7de
  position:
    end: 200
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:d46a74f87b94419e2f9b17a001f696a2dfc8cfec7bf8b954fd94e00a70bad92f
  selector:
    exact: The bridge pattern is a design pattern used in software engineering that
      is meant to "decouple an abstraction from its implementation so that the two
      can vary independently", introduced by the Gang of
    prefix: ''
    suffix: ' Four. The bridge uses encapsula'
    type: TextQuoteSelector
  selector_sha256: sha256:212fc3611c7a3baf6de7d5077cc7e05d38e46b1544e70fa5877d15af34f8cbf8
  snapshot_sha256: sha256:d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca
extractor: utf8/1
id: web-computer-science-bridge-pattern
local:
  file_sha256: sha256:d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca
  path_ref: local-sidecar:public/web-computer-science-bridge-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca.txt
  sha256: sha256:d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:d0ab773a50af90f11a491569985a6374d1fae4e9c4bf8279315c4e3871732bca
source_type: local-file
vault_id: public
---
The bridge pattern is a design pattern used in software engineering that is meant to "decouple an abstraction from its implementation so that the two can vary independently", introduced by the Gang of Four. The bridge uses encapsulation, aggregation, and can use inheritance to separate responsibilities into different classes. The bridge pattern can also be thought of as two layers of abstraction. When there is only one fixed implementation, this pattern is known as the Pimpl idiom in the C++ world.
