---
archive_policy: text-only
attachments:
- filename: wiki-linked-list.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-fbc7b862da58
  position:
    end: 276
    start: 0
    type: TextPositionSelector
  selector:
    exact: In computer science, a linked list is a linear collection of data elements
      whose order is not given by their physical placement in memory. Instead, each
      element points to the next. It is a data structure consisting of a collection
      of nodes which together represent a sequence.
    prefix: ''
    suffix: '

      In its most basic form, each no'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-6f9055c4a223
  position:
    end: 521
    start: 277
    type: TextPositionSelector
  selector:
    exact: In its most basic form, each node contains data, and a reference (in other
      words, a link) to the next node in the sequence. This structure allows for efficient
      insertion or removal of elements from any position in the sequence during iteration.
    prefix: ' together represent a sequence.

      '
    suffix: '

      A drawback of linked lists is t'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-e1c0317667fd
  position:
    end: 632
    start: 522
    type: TextPositionSelector
  selector:
    exact: A drawback of linked lists is that data access time is linear with respect
      to the number of nodes in the list.
    prefix: ' the sequence during iteration.

      '
    suffix: ' Because nodes are serially link'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-debf304f8906
  position:
    end: 856
    start: 633
    type: TextPositionSelector
  selector:
    exact: Because nodes are serially linked, accessing any node requires that the
      prior node be accessed beforehand (which introduces difficulties in pipelining).
      Faster access, such as random access (direct access), is not possible.
    prefix: 'he number of nodes in the list. '
    suffix: '

      Arrays have better cache locali'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-5f4608cd28e0
  position:
    end: 916
    start: 857
    type: TextPositionSelector
  selector:
    exact: Arrays have better cache locality compared to linked lists.
    prefix: 'irect access), is not possible.

      '
    suffix: '

      The principal benefit of a link'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-816e76e0295f
  position:
    end: 1264
    start: 917
    type: TextPositionSelector
  selector:
    exact: The principal benefit of a linked list over a conventional array is that
      the list elements can be easily inserted or removed without reallocation or
      reorganization of the entire structure because the data items do not need to
      be stored contiguously in memory or on disk, while restructuring an array at
      run-time is a much more expensive operation.
    prefix: 'ality compared to linked lists.

      '
    suffix: '

      In a doubly linked list, each n'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-b70e16480b71
  position:
    end: 1411
    start: 1265
    type: TextPositionSelector
  selector:
    exact: In a doubly linked list, each node contains, besides the link to the next
      node, a second link field pointing to the previous node in the sequence.
    prefix: ' much more expensive operation.

      '
    suffix: ' The two links may be called for'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-662ca96b80b6
  position:
    end: 1835
    start: 1492
    type: TextPositionSelector
  selector:
    exact: In a circularly linked list, all nodes are linked in a continuous circle,
      without using null. For lists with a front and a back (such as a queue), one
      stores a reference to the last node in the list. The next node after the last
      node is the first node. Elements can be added to the back of the list and removed
      from the front in constant time.
    prefix: 's, or next and prev (previous).

      '
    suffix: '

      Circularly linked lists can be '
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-3ac0049e1914
  position:
    end: 1898
    start: 1836
    type: TextPositionSelector
  selector:
    exact: Circularly linked lists can be either singly or doubly linked.
    prefix: 'rom the front in constant time.

      '
    suffix: '

      With a circular list, a pointer'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-d0a6e5f269a8
  position:
    end: 2214
    start: 1899
    type: TextPositionSelector
  selector:
    exact: With a circular list, a pointer to the last node gives easy access also
      to the first node, by following one link. Thus, in applications that require
      access to both ends of the list (e.g., in the implementation of a queue), a
      circular structure allows one to handle the structure by a single pointer, instead
      of two.
    prefix: 'either singly or doubly linked.

      '
    suffix: '

      A circularly linked list may be'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-2a0d730d509f
  position:
    end: 2496
    start: 2215
    type: TextPositionSelector
  selector:
    exact: A circularly linked list may be a natural option to represent arrays that
      are naturally circular, e.g. the corners of a polygon, a pool of buffers that
      are used and released in FIFO (first in, first out) order, or a set of processes
      that should be time-shared in round-robin order.
    prefix: 'single pointer, instead of two.

      '
    suffix: '

      Double-linked lists require mor'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-9ef0e141f101
  position:
    end: 2750
    start: 2497
    type: TextPositionSelector
  selector:
    exact: Double-linked lists require more space per node (unless one uses XOR-linking),
      and their elementary operations are more expensive; but they are often easier
      to manipulate because they allow fast and easy sequential access to the list
      in both directions.
    prefix: 'me-shared in round-robin order.

      '
    suffix: '

      In a doubly linked list, one ca'
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-8c7e9f4376d8
  position:
    end: 3083
    start: 2751
    type: TextPositionSelector
  selector:
    exact: In a doubly linked list, one can insert or delete a node in a constant
      number of operations given only that node's address. To do the same in a singly
      linked list, one must have the address of the pointer to that node, which is
      either the handle for the whole list (in case of the first node) or the link
      field in the previous node.
    prefix: 'to the list in both directions.

      '
    suffix: '

      Some algorithms require access '
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
- evidence_id: evidence-5d91e2bb22e8
  position:
    end: 3134
    start: 3084
    type: TextPositionSelector
  selector:
    exact: Some algorithms require access in both directions.
    prefix: 'ink field in the previous node.

      '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
extractor: utf8/1
id: wiki-linked-list
local:
  file_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
  path_ref: local-sidecar:public/wiki-linked-list
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:43199aaeea1c5cf30104d7fdc33c9e672b28c33687d3c92dd9f3bb2b4db37b8c
source_type: local-file
vault_id: public
---
In computer science, a linked list is a linear collection of data elements whose order is not given by their physical placement in memory. Instead, each element points to the next. It is a data structure consisting of a collection of nodes which together represent a sequence.
In its most basic form, each node contains data, and a reference (in other words, a link) to the next node in the sequence. This structure allows for efficient insertion or removal of elements from any position in the sequence during iteration.
A drawback of linked lists is that data access time is linear with respect to the number of nodes in the list. Because nodes are serially linked, accessing any node requires that the prior node be accessed beforehand (which introduces difficulties in pipelining). Faster access, such as random access (direct access), is not possible.
Arrays have better cache locality compared to linked lists.
The principal benefit of a linked list over a conventional array is that the list elements can be easily inserted or removed without reallocation or reorganization of the entire structure because the data items do not need to be stored contiguously in memory or on disk, while restructuring an array at run-time is a much more expensive operation.
In a doubly linked list, each node contains, besides the link to the next node, a second link field pointing to the previous node in the sequence. The two links may be called forward and backwards, or next and prev (previous).
In a circularly linked list, all nodes are linked in a continuous circle, without using null. For lists with a front and a back (such as a queue), one stores a reference to the last node in the list. The next node after the last node is the first node. Elements can be added to the back of the list and removed from the front in constant time.
Circularly linked lists can be either singly or doubly linked.
With a circular list, a pointer to the last node gives easy access also to the first node, by following one link. Thus, in applications that require access to both ends of the list (e.g., in the implementation of a queue), a circular structure allows one to handle the structure by a single pointer, instead of two.
A circularly linked list may be a natural option to represent arrays that are naturally circular, e.g. the corners of a polygon, a pool of buffers that are used and released in FIFO (first in, first out) order, or a set of processes that should be time-shared in round-robin order.
Double-linked lists require more space per node (unless one uses XOR-linking), and their elementary operations are more expensive; but they are often easier to manipulate because they allow fast and easy sequential access to the list in both directions.
In a doubly linked list, one can insert or delete a node in a constant number of operations given only that node's address. To do the same in a singly linked list, one must have the address of the pointer to that node, which is either the handle for the whole list (in case of the first node) or the link field in the previous node.
Some algorithms require access in both directions.
