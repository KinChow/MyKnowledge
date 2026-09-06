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
  quote_sha256: sha256:0525fed2bde1f942a26a0c469714aae617b233e58d17bd83a5b8be4c13b6821c
  selector:
    exact: In computer science, an array is a data structure consisting of a collection
      of elements (values or variables), of the same memory size, each identified
      by at least one array index or key, the collection of which may be a tuple,
      known as an index tuple.
    prefix: ''
    suffix: '

      In general, an array is a mutab'
    type: TextQuoteSelector
  selector_sha256: sha256:6432931b377d774f76da09af53d22840a7160480f27f2442548524a64bfd6d28
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-48aee0cfd4dd
  position:
    end: 577
    start: 254
    type: TextPositionSelector
  quote_sha256: sha256:29bd4c839236f915399e0f59c58855061507256c8a23173167bf4e4e358256ac
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
  selector_sha256: sha256:bcca4094cc4039db33457c7874156826f54f789fc56b1019e5b41b755a8f18c3
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-3a0f8a1c609d
  position:
    end: 659
    start: 578
    type: TextPositionSelector
  quote_sha256: sha256:a72abbe3039ded88373a1509d7f50f8a79dbcc51fb4f48b23acea75004e37a22
  selector:
    exact: Arrays are useful mostly because the element indices can be computed at
      run time.
    prefix: 'called a one-dimensional array.

      '
    suffix: ' For that reason, the elements o'
    type: TextQuoteSelector
  selector_sha256: sha256:bc0326888b96473c2d39205b98f0645fd82dca5d29688c3fe27a67a8ce20277e
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-966acca3186e
  position:
    end: 796
    start: 660
    type: TextPositionSelector
  quote_sha256: sha256:20d12cacde31b3e3313dd1f23766b00a72c8639784a1342fca69dddf3a6d5c55
  selector:
    exact: For that reason, the elements of an array data structure are required to
      have the same size and should use the same data representation.
    prefix: 'es can be computed at run time. '
    suffix: ' The set of valid index tuples a'
    type: TextQuoteSelector
  selector_sha256: sha256:56b79fbc79aa19962880949f36f79d7f504349adda6a23dea3b43c390c5e8c75
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-158a9b77e84c
  position:
    end: 1233
    start: 966
    type: TextPositionSelector
  quote_sha256: sha256:8e97a422e8e8999a488187af17c5c46fb608f1df201dd4c165b8f3fb40077add
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
  selector_sha256: sha256:6e0822acc40d4f253abda0fa988092f3cc7b31a3d56f4dfff684009ad8369ef1
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-4ae1136a3f28
  position:
    end: 1451
    start: 1234
    type: TextPositionSelector
  quote_sha256: sha256:cf975b67d87c69e60c81dc08f83cb7b5a9d06759757a59acb347f818959e3ff2
  selector:
    exact: Many algorithms that use multidimensional arrays will scan them in a predictable
      order. A programmer (or a sophisticated compiler) may use this information to
      choose between row- or column-major layout for each array.
    prefix: ' type of locality of reference.

      '
    suffix: ' For example, when computing the'
    type: TextQuoteSelector
  selector_sha256: sha256:17d97f78d6f545c846890dd244aaaec26bc7f2fddba19564c8562e55b8cfb256
  snapshot_sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
- evidence_id: evidence-45144fe6c9df
  position:
    end: 1595
    start: 1452
    type: TextPositionSelector
  quote_sha256: sha256:3536ff28f4fb0759baa0821f09e4c19ab64ba240c7be1463cd1e9c6e9ed17c94
  selector:
    exact: For example, when computing the product A·B of two matrices, it would be
      best to have A stored in row-major order, and B in column-major order.
    prefix: 'mn-major layout for each array. '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:e85e373d6ddcd9917587ac87ac1a193211958dd21901f11081378d2bcb60e4ce
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
  sha256: sha256:07830b09cbaeb16ee68dd178dac24d58fbf4754bdd0f36bc0f541c8377b9ecfb
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
