---
archive_policy: text-only
attachments:
- filename: web-computer-science-facade-pattern.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b410664f922a
  position:
    end: 388
    start: 188
    type: TextPositionSelector
  quote_sha256: sha256:cbfb051d82da8a9f23cb4c51f88c77375ae9b0aece3faa997a8e796658309b8f
  selector:
    exact: front-facing interface masking more complex underlying or structural code.
      This pattern hides the complexities of the larger system and provides a simpler
      interface to the client. It typically involve
    prefix: 't is an object that serves as a '
    suffix: s a single wrapper class that co
    type: TextQuoteSelector
  selector_sha256: sha256:a4c9834ff1d7e3232153aaa34e1c79293bb53e0dee405fada0915dd0830348ef
  snapshot_sha256: sha256:ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52
extractor: utf8/1
id: web-computer-science-facade-pattern
local:
  file_sha256: sha256:ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52
  path_ref: local-sidecar:public/web-computer-science-facade-pattern
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52.txt
  sha256: sha256:ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:ade8bb6bd1dc996f9a8159a0f77737f7795760d8b4216346e51ab374357c9f52
source_type: local-file
vault_id: public
---
The facade pattern (also spelled façade) is a software design pattern commonly used in object-oriented programming. Analogous to a façade in architecture, it is an object that serves as a front-facing interface masking more complex underlying or structural code. This pattern hides the complexities of the larger system and provides a simpler interface to the client. It typically involves a single wrapper class that contains a set of members required by the client. These members access the system on behalf of the facade client and hide the implementation details.
