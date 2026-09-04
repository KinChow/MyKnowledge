---
archive_policy: text-only
attachments:
- filename: arm-b27-caches.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b118c048c8bb
  position:
    end: 348
    start: 197
    type: TextPositionSelector
  quote_sha256: sha256:42c36b6b242a9316194a567d298b1eac1c6f38f6826970c0e92c19e45c907bbd
  selector:
    exact: The Arm architecture defines the application level interface to the memory
      system, including a hierarchical memory system with multiple levels of cache
    prefix: 'tem are IMPLEMENTATION DEFINED. '
    suffix: . This section describes an appl
    type: TextQuoteSelector
  selector_sha256: sha256:66b0391adb148236287dc9633edfc69f6daa9d16fbdd0079ca351cf57c93de31
  snapshot_sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
- evidence_id: evidence-0881edb1b41c
  position:
    end: 348
    start: 42
    type: TextPositionSelector
  quote_sha256: sha256:fa88e7ceae81f677a597585a9d2b0f9a060ba07a3cbe15d329794c01e1d9c003
  selector:
    exact: The implementation of a memory system depends heavily on the microarchitecture
      and therefore many details of the memory system are IMPLEMENTATION DEFINED.
      The Arm architecture defines the application level interface to the memory system,
      including a hierarchical memory system with multiple levels of cache
    prefix: "Caches and memory hierarchy\n \n  "
    suffix: . This section describes an appl
    type: TextQuoteSelector
  selector_sha256: sha256:4b95df27c185a582ebee496041641e3989011b46a0d7f77147ae3abcd231bf7b
  snapshot_sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
extractor: utf8/1
id: arm-b27-caches
local:
  file_sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
  path_ref: local-sidecar:public/arm-b27-caches
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28.txt
  sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
source_type: local-file
vault_id: public
---
#### B2.7 Caches and memory hierarchy
 
  The implementation of a memory system depends heavily on the microarchitecture and therefore many details of the memory system are IMPLEMENTATION DEFINED. The Arm architecture defines the application level interface to the memory system, including a hierarchical memory system with multiple levels of cache. This section describes an application level view of this system. It contains the subsections: 
   
   Introduction to caches. 
   Memory hierarchy. 
   Application level access to functionality related to caches 
   Implication of caches for the application programmer. 
   Prefetching into cache.