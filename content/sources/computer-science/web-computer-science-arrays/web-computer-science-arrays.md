---
archive_policy: text-only
attachments:
- filename: web-computer-science-arrays.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:aa9e9f669604d25eb3cff9455eddf8a57a84be2e1af20ed5963c0647c7712adc
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-b59e7612c5bd
  position:
    end: 94
    start: 0
    type: TextPositionSelector
  selector:
    exact: An array is a fundamental and linear data structure that stores items at
      contiguous locations.
    prefix: ''
    suffix: ' Note that in case of C/C++ and '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-36bd13818eb8
  position:
    end: 494
    start: 365
    type: TextPositionSelector
  selector:
    exact: '- Random Access : i-th item can be accessed in O(1) Time as we have the
      base address and every item or reference is of same size.'
    prefix: 'ges over other data structures.

      '
    suffix: '

      - Cache Friendliness : Since it'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-607b7c3bda98
  position:
    end: 625
    start: 495
    type: TextPositionSelector
  selector:
    exact: '- Cache Friendliness : Since items / references are stored at contiguous
      locations, we get the advantage of locality of reference.'
    prefix: 'm or reference is of same size.

      '
    suffix: '

      Arrays are used to build other '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-2a1b432e458b
  position:
    end: 721
    start: 626
    type: TextPositionSelector
  selector:
    exact: Arrays are used to build other data structures like Stack Queue, Deque,
      Graph, Hash Table, etc.
    prefix: 'ntage of locality of reference.

      '
    suffix: ' An array is not useful in place'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-74c5ebb3931e
  position:
    end: 494
    start: 367
    type: TextPositionSelector
  selector:
    exact: 'Random Access : i-th item can be accessed in O(1) Time as we have the
      base address and every item or reference is of same size.'
    prefix: 's over other data structures.

      - '
    suffix: '

      - Cache Friendliness : Since it'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-74db51a83add
  position:
    end: 625
    start: 497
    type: TextPositionSelector
  selector:
    exact: 'Cache Friendliness : Since items / references are stored at contiguous
      locations, we get the advantage of locality of reference.'
    prefix: 'or reference is of same size.

      - '
    suffix: '

      Arrays are used to build other '
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
- evidence_id: evidence-49d49a2a0411
  position:
    end: 856
    start: 722
    type: TextPositionSelector
  selector:
    exact: An array is not useful in places where we have operations like insert in
      the middle, delete from middle and search in a unsorted data.
    prefix: ' Deque, Graph, Hash Table, etc. '
    suffix: '

      Basics

      In Different Language

      Ba'
    type: TextQuoteSelector
  snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
extractor: trafilatura/2.2.0
id: web-computer-science-arrays
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/aa9e9f669604d25eb3cff9455eddf8a57a84be2e1af20ed5963c0647c7712adc.html
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://www.geeksforgeeks.org/dsa/array-data-structure-guide/
  url: https://www.geeksforgeeks.org/array-data-structure/
schema_version: source/v1
snapshot_sha256: sha256:2f4d9e38975156387979cdacae8c1e22ef4eae427dea58c9e8ba02fec61796cc
source_type: doc
vault_id: public
---
An array is a fundamental and linear data structure that stores items at contiguous locations. Note that in case of C/C++ and Java-Primitive-Arrays, actual elements are stored at contiguous locations. And in case of Python, JS, Java-Non-Primitive, references are stored at contiguous locations. It offers mainly the following advantages over other data structures.
- Random Access : i-th item can be accessed in O(1) Time as we have the base address and every item or reference is of same size.
- Cache Friendliness : Since items / references are stored at contiguous locations, we get the advantage of locality of reference.
Arrays are used to build other data structures like Stack Queue, Deque, Graph, Hash Table, etc. An array is not useful in places where we have operations like insert in the middle, delete from middle and search in a unsorted data.
Basics
In Different Language
Basic Problems
Easy Problems
Prerequisite for the Remaining Problems
- Binary Search
- Selection Sort, Insertion Sort, Binary Search, QuickSort, MergeSort, CycleSort, and HeapSort
- Sort in C++ / Sort in Java / Sort in Python / Sort in JavaScript
- Two Pointers Technique
- Prefix Sum Technique
- Basics of Hashing
- Window Sliding Technique
Medium Problems
Hard Problems
Expert Problems for Competitive Programmers
Quick Links :