---
archive_policy: text-only
attachments:
- filename: wiki-stack-adt.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-d286628a0b15
  position:
    end: 133
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:19772b2629a5bebd750949ccea5ddd35a4f259c32ce4303fc00005b3f181ce65
  selector:
    exact: The order in which elements are added to or removed from a stack is described
      as last in, first out, referred to by the acronym LIFO.
    prefix: ''
    suffix: '

      As with a stack of physical obj'
    type: TextQuoteSelector
  selector_sha256: sha256:9ea1577e846c7725aa3c3789ecc2892f87a90fdff5047eba08eeed20a91b8756
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-d10e607c26e6
  position:
    end: 332
    start: 134
    type: TextPositionSelector
  quote_sha256: sha256:d164388004377684dd12878f6d77d8fb494be388bb5285ef802628b63e8e8ebb
  selector:
    exact: As with a stack of physical objects, this structure makes it easy to take
      an item off the top of the stack, but accessing a datum deeper in the stack
      may require removing multiple other items first.
    prefix: 'eferred to by the acronym LIFO.

      '
    suffix: '

      Additionally, a peek operation '
    type: TextQuoteSelector
  selector_sha256: sha256:ef1bad39dfad124532614d4bf2bad2a3f230ac0186a8f6d9e8b3cfc64c609c0f
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4593be24621b
  position:
    end: 476
    start: 333
    type: TextPositionSelector
  quote_sha256: sha256:a0c6bbfd5e6fe7131c5e3c8c82baaa8ef0a16bd82a637cde29d874dcb0b74365
  selector:
    exact: Additionally, a peek operation can, without modifying the stack, return
      the value of the last element added (the item at the top of the stack).
    prefix: 'ing multiple other items first.

      '
    suffix: '

      The name stack is an analogy to'
    type: TextQuoteSelector
  selector_sha256: sha256:904da59bf53447a14f38e894030da15ac8b72f4bdd365b79fe57c53e2fbd91ee
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-07bc9ab45465
  position:
    end: 585
    start: 477
    type: TextPositionSelector
  quote_sha256: sha256:c3ecced3e11d76826b14a61d8c29b713d2928ad76251f5fca62beba376433f9d
  selector:
    exact: The name stack is an analogy to a set of physical items stacked one atop
      another, such as a stack of plates.
    prefix: ' item at the top of the stack).

      '
    suffix: '

      Considered a sequential collect'
    type: TextQuoteSelector
  selector_sha256: sha256:8d4e3108a22f62c3a1ad7d96ff06db937e6da0b1a52821c69e6d2a8ac34e51f4
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-13a035e39fcd
  position:
    end: 781
    start: 586
    type: TextPositionSelector
  quote_sha256: sha256:ed87d1d5d21f09819465607356cad6b73bf9bd63448e2294f834234726a43670
  selector:
    exact: Considered a sequential collection, a stack has one end which is the only
      position at which the push and pop operations may occur, the top of the stack,
      and is fixed at the other end, the bottom.
    prefix: 'her, such as a stack of plates.

      '
    suffix: '

      A stack may be implemented as, '
    type: TextQuoteSelector
  selector_sha256: sha256:1485da7f6bea6dc7f54118fe4a507e159624b906a5f71f71751208f6e61adb7a
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-78c22ee5ee5f
  position:
    end: 881
    start: 782
    type: TextPositionSelector
  quote_sha256: sha256:94304619e249312a8769fd8d48dcec0459fb457d6b5f3d0ee754bdee9804f38f
  selector:
    exact: A stack may be implemented as, for example, a singly linked list with a
      pointer to the top element.
    prefix: 'd at the other end, the bottom.

      '
    suffix: '

      A stack may be implemented to h'
    type: TextQuoteSelector
  selector_sha256: sha256:3eaa7ded48479443a4fbdea852311dd809b5f47b3879376c5c551b9fc79325cb
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4dc02e593e5a
  position:
    end: 1061
    start: 882
    type: TextPositionSelector
  quote_sha256: sha256:3eef310bb246bd1024272e88508dd65a792fc5ae2ac4348853237e625e8c5aa2
  selector:
    exact: A stack may be implemented to have a bounded capacity. If the stack is
      full and does not contain enough space to accept another element, the stack
      is in a state of stack overflow.
    prefix: 'h a pointer to the top element.

      '
    suffix: '

      A stack can be easily implement'
    type: TextQuoteSelector
  selector_sha256: sha256:b4dbd23d02962a2abe03d05fc031f1b9ebb0bc7b20465126ffda2a00c4919e86
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-322b64c2a9f2
  position:
    end: 1397
    start: 1062
    type: TextPositionSelector
  quote_sha256: sha256:8d24619609b257e30ae22dffe1341848b489a7b850420c3bdb25a9fd117efb7f
  selector:
    exact: 'A stack can be easily implemented either through an array or a linked
      list, as it is merely a special case of a list. In either case, what identifies
      the data structure as a stack is not the implementation but the interface: the
      user is only allowed to pop or push items onto the array or linked list, with
      few other helper operations.'
    prefix: 's in a state of stack overflow.

      '
    suffix: '

      The push operation adds an elem'
    type: TextQuoteSelector
  selector_sha256: sha256:83f20eb3947de7f8451ae7c855d47f128c8322cd6c17b39087a9145fed8eae1b
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-1fae9bf0b3f4
  position:
    end: 1491
    start: 1398
    type: TextPositionSelector
  quote_sha256: sha256:0be177bc22d0963b056adf56a0f36dea2cd0cbc076e7f85616e58a3023c26ae3
  selector:
    exact: 'The push operation adds an element and increments the top index, after
      checking for overflow:'
    prefix: 'th few other helper operations.

      '
    suffix: '

      Similarly, pop decrements the t'
    type: TextQuoteSelector
  selector_sha256: sha256:0ec9a0b6bf8155d607bb8e45771647517c365a6d856b720ef253fc394ed7b6aa
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-57bb10891387
  position:
    end: 1615
    start: 1492
    type: TextPositionSelector
  quote_sha256: sha256:16336ef587863febe770ce3cd769f11820535d0fa4423b66b7e17e76317311c4
  selector:
    exact: 'Similarly, pop decrements the top index after checking for underflow,
      and returns the item that was previously the top one:'
    prefix: 'x, after checking for overflow:

      '
    suffix: '

      Calculators that employ reverse'
    type: TextQuoteSelector
  selector_sha256: sha256:66e4a64ebfd8bbf5428133455a98aec0d0c0e2cb96344dfa2d35443c5ad1676d
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-63eafcee671c
  position:
    end: 1928
    start: 1616
    type: TextPositionSelector
  quote_sha256: sha256:7172a6619cac2af78ea314f73686c6163c0068fdba64ef2df954a32668b994d2
  selector:
    exact: Calculators that employ reverse Polish notation use a stack structure to
      hold values. Expressions can be represented in prefix, postfix or infix notations
      and conversion from one form to another may be accomplished using a stack. Many
      compilers use a stack to parse syntax before translation into low-level code.
    prefix: 'hat was previously the top one:

      '
    suffix: '

      Another important application o'
    type: TextQuoteSelector
  selector_sha256: sha256:752b621dff9680f1b07ef91b0a11ddef6d5a760e98291fca4875188dca7f8ae3
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4fe264776635
  position:
    end: 1985
    start: 1929
    type: TextPositionSelector
  quote_sha256: sha256:869e57ef5e2a2a322239d69638bedf9e3e8f68020dda142d9088c7c6cfcafc58
  selector:
    exact: Another important application of stacks is backtracking.
    prefix: 'ranslation into low-level code.

      '
    suffix: '

      This can be achieved through th'
    type: TextQuoteSelector
  selector_sha256: sha256:8d501301fe3279e03b7e0343d37f75b0a4b4c3593778b110d766735f16c4e45d
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-a7ae1699eb8d
  position:
    end: 2143
    start: 1986
    type: TextPositionSelector
  quote_sha256: sha256:56909a9b05f2aa167a0de8e69a68155f7614b1a4851969a857b875fa23c064ae
  selector:
    exact: This can be achieved through the use of stacks, as a last correct point
      can be pushed onto the stack, and popped from the stack in case of an incorrect
      path.
    prefix: 'tion of stacks is backtracking.

      '
    suffix: '

      There is also a number of small'
    type: TextQuoteSelector
  selector_sha256: sha256:85bd72feb3b32e597938621f5437081dc0c3d0f2d88437227fc2722a328e9f24
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-def936ce83dc
  position:
    end: 2320
    start: 2144
    type: TextPositionSelector
  quote_sha256: sha256:d2eb4490d67f99089adc71dcd249fa6d30e564a9f786813f49023ff21ded7702
  selector:
    exact: There is also a number of small microprocessors that implement a stack
      directly in hardware, and some microcontrollers have a fixed-depth stack that
      is not directly accessible.
    prefix: 'k in case of an incorrect path.

      '
    suffix: '

      '
    type: TextQuoteSelector
  selector_sha256: sha256:ffc01eef667fb57e902e21ecaf0577e8c17fac299ce506729d76efddc0511b91
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
extractor: utf8/1
id: wiki-stack-adt
local:
  file_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
  path_ref: local-sidecar:public/wiki-stack-adt
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4.txt
  sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
source_type: local-file
vault_id: public
---
The order in which elements are added to or removed from a stack is described as last in, first out, referred to by the acronym LIFO.
As with a stack of physical objects, this structure makes it easy to take an item off the top of the stack, but accessing a datum deeper in the stack may require removing multiple other items first.
Additionally, a peek operation can, without modifying the stack, return the value of the last element added (the item at the top of the stack).
The name stack is an analogy to a set of physical items stacked one atop another, such as a stack of plates.
Considered a sequential collection, a stack has one end which is the only position at which the push and pop operations may occur, the top of the stack, and is fixed at the other end, the bottom.
A stack may be implemented as, for example, a singly linked list with a pointer to the top element.
A stack may be implemented to have a bounded capacity. If the stack is full and does not contain enough space to accept another element, the stack is in a state of stack overflow.
A stack can be easily implemented either through an array or a linked list, as it is merely a special case of a list. In either case, what identifies the data structure as a stack is not the implementation but the interface: the user is only allowed to pop or push items onto the array or linked list, with few other helper operations.
The push operation adds an element and increments the top index, after checking for overflow:
Similarly, pop decrements the top index after checking for underflow, and returns the item that was previously the top one:
Calculators that employ reverse Polish notation use a stack structure to hold values. Expressions can be represented in prefix, postfix or infix notations and conversion from one form to another may be accomplished using a stack. Many compilers use a stack to parse syntax before translation into low-level code.
Another important application of stacks is backtracking.
This can be achieved through the use of stacks, as a last correct point can be pushed onto the stack, and popped from the stack in case of an incorrect path.
There is also a number of small microprocessors that implement a stack directly in hardware, and some microcontrollers have a fixed-depth stack that is not directly accessible.
