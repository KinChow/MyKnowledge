---
archive_policy: text-only
attachments:
- filename: wiki-array-cs.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-c4b9fe95c672
  position:
    end: 253
    start: 0
    type: TextPositionSelector
  selector:
    exact: In computer science, an array is a data structure consisting of a collection
      of elements (values or variables), of the same memory size, each identified
      by at least one array index or key, the collection of which may be a tuple,
      known as an index tuple.
    prefix: ''
    suffix: '

      In general, an array is a mutab'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-48aee0cfd4dd
  position:
    end: 577
    start: 254
    type: TextPositionSelector
  selector:
    exact: In general, an array is a mutable and linear collection of elements with
      the same data type. An array is stored such that the position (memory address)
      of each element can be computed from its index tuple by a mathematical formula.
      The simplest type of data structure is a linear array, also called a one-dimensional
      array.
    prefix: 'tuple, known as an index tuple.

      '
    suffix: '

      Arrays are useful mostly becaus'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-3a0f8a1c609d
  position:
    end: 659
    start: 578
    type: TextPositionSelector
  selector:
    exact: Arrays are useful mostly because the element indices can be computed at
      run time.
    prefix: 'called a one-dimensional array.

      '
    suffix: ' For that reason, the elements o'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-966acca3186e
  position:
    end: 796
    start: 660
    type: TextPositionSelector
  selector:
    exact: For that reason, the elements of an array data structure are required to
      have the same size and should use the same data representation.
    prefix: 'es can be computed at run time. '
    suffix: ' The set of valid index tuples a'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-158a9b77e84c
  position:
    end: 1233
    start: 966
    type: TextPositionSelector
  selector:
    exact: In systems which use processor cache or virtual memory, scanning an array
      is much faster if successive elements are stored in consecutive positions in
      memory, rather than sparsely scattered. This is known as spatial locality, which
      is a type of locality of reference.
    prefix: 'ixed while the array is in use.

      '
    suffix: '

      Many algorithms that use multid'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-4ae1136a3f28
  position:
    end: 1451
    start: 1234
    type: TextPositionSelector
  selector:
    exact: Many algorithms that use multidimensional arrays will scan them in a predictable
      order. A programmer (or a sophisticated compiler) may use this information to
      choose between row- or column-major layout for each array.
    prefix: ' type of locality of reference.

      '
    suffix: ' For example, when computing the'
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-45144fe6c9df
  position:
    end: 1595
    start: 1452
    type: TextPositionSelector
  selector:
    exact: For example, when computing the product A·B of two matrices, it would be
      best to have A stored in row-major order, and B in column-major order.
    prefix: 'mn-major layout for each array. '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
extractor: utf8/1
id: wiki-array-cs
local:
  file_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
  path_ref: local-sidecar:public/wiki-array-cs
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
source_type: local-file
vault_id: public
---
In computer science, an array is a data structure consisting of a collection of elements (values or variables), of the same memory size, each identified by at least one array index or key, the collection of which may be a tuple, known as an index tuple.
In general, an array is a mutable and linear collection of elements with the same data type. An array is stored such that the position (memory address) of each element can be computed from its index tuple by a mathematical formula. The simplest type of data structure is a linear array, also called a one-dimensional array.
Arrays are useful mostly because the element indices can be computed at run time. For that reason, the elements of an array data structure are required to have the same size and should use the same data representation. The set of valid index tuples and the addresses of the elements (and hence the element addressing formula) are usually, but not always, fixed while the array is in use.
In systems which use processor cache or virtual memory, scanning an array is much faster if successive elements are stored in consecutive positions in memory, rather than sparsely scattered. This is known as spatial locality, which is a type of locality of reference.
Many algorithms that use multidimensional arrays will scan them in a predictable order. A programmer (or a sophisticated compiler) may use this information to choose between row- or column-major layout for each array. For example, when computing the product A·B of two matrices, it would be best to have A stored in row-major order, and B in column-major order.
