---
archive_policy: text-only
attachments:
- filename: web-computer-science-proxy-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-5596c3d426d5
  position:
    end: 299
    start: 25
    type: TextPositionSelector
  quote_sha256: sha256:11eda962120991eedc4ad5ce4852104aa7cf903122d5f5a961ca0209423b17f2
  selector:
    exact: 'the proxy pattern is a software design pattern which is a class functioning
      as an interface to something else. The proxy could interface to anything: a
      network connection, a large object in memory, a file, or some other resource
      that is expensive or impossible to duplicate.'
    prefix: 'In computer programming, '
    suffix: ' In short, a proxy is a wrapper '
    type: TextQuoteSelector
  selector_sha256: sha256:7a3fdf539cf4a9c41672b5a54338778205e476665c2ca3810063f700f858c373
  snapshot_sha256: sha256:08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d
extractor: utf8/1
id: web-computer-science-proxy-pattern
local:
  file_sha256: sha256:08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d
  path_ref: local-sidecar:public/web-computer-science-proxy-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d.txt
  sha256: sha256:08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:08b9a33f69952eba1e2ee096f5950da973b6f839cf546dcb77826d649605ce2d
source_type: local-file
vault_id: public
---
In computer programming, the proxy pattern is a software design pattern which is a class functioning as an interface to something else. The proxy could interface to anything: a network connection, a large object in memory, a file, or some other resource that is expensive or impossible to duplicate. In short, a proxy is a wrapper or agent object that is being called by the client to access the real serving object behind the scenes. Use of the proxy can simply be forwarding to the real object, or can provide additional logic.
