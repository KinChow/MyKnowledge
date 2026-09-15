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
  selector:
    exact: The Arm architecture defines the application level interface to the memory
      system, including a hierarchical memory system with multiple levels of cache
    prefix: 'tem are IMPLEMENTATION DEFINED. '
    suffix: . This section describes an appl
    type: TextQuoteSelector
  snapshot_sha256: sha256:11071521d18f596ea751490332161a64c8c9966caad45a72b943af5187c99a28
- evidence_id: evidence-0881edb1b41c
  position:
    end: 348
    start: 42
    type: TextPositionSelector
  selector:
    exact: The implementation of a memory system depends heavily on the microarchitecture
      and therefore many details of the memory system are IMPLEMENTATION DEFINED.
      The Arm architecture defines the application level interface to the memory system,
      including a hierarchical memory system with multiple levels of cache
    prefix: "Caches and memory hierarchy\n \n  "
    suffix: . This section describes an appl
    type: TextQuoteSelector
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