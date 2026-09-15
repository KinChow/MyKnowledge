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
  selector:
    exact: The order in which elements are added to or removed from a stack is described
      as last in, first out, referred to by the acronym LIFO.
    prefix: ''
    suffix: '

      As with a stack of physical obj'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-d10e607c26e6
  position:
    end: 332
    start: 134
    type: TextPositionSelector
  selector:
    exact: As with a stack of physical objects, this structure makes it easy to take
      an item off the top of the stack, but accessing a datum deeper in the stack
      may require removing multiple other items first.
    prefix: 'eferred to by the acronym LIFO.

      '
    suffix: '

      Additionally, a peek operation '
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4593be24621b
  position:
    end: 476
    start: 333
    type: TextPositionSelector
  selector:
    exact: Additionally, a peek operation can, without modifying the stack, return
      the value of the last element added (the item at the top of the stack).
    prefix: 'ing multiple other items first.

      '
    suffix: '

      The name stack is an analogy to'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-07bc9ab45465
  position:
    end: 585
    start: 477
    type: TextPositionSelector
  selector:
    exact: The name stack is an analogy to a set of physical items stacked one atop
      another, such as a stack of plates.
    prefix: ' item at the top of the stack).

      '
    suffix: '

      Considered a sequential collect'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-13a035e39fcd
  position:
    end: 781
    start: 586
    type: TextPositionSelector
  selector:
    exact: Considered a sequential collection, a stack has one end which is the only
      position at which the push and pop operations may occur, the top of the stack,
      and is fixed at the other end, the bottom.
    prefix: 'her, such as a stack of plates.

      '
    suffix: '

      A stack may be implemented as, '
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-78c22ee5ee5f
  position:
    end: 881
    start: 782
    type: TextPositionSelector
  selector:
    exact: A stack may be implemented as, for example, a singly linked list with a
      pointer to the top element.
    prefix: 'd at the other end, the bottom.

      '
    suffix: '

      A stack may be implemented to h'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4dc02e593e5a
  position:
    end: 1061
    start: 882
    type: TextPositionSelector
  selector:
    exact: A stack may be implemented to have a bounded capacity. If the stack is
      full and does not contain enough space to accept another element, the stack
      is in a state of stack overflow.
    prefix: 'h a pointer to the top element.

      '
    suffix: '

      A stack can be easily implement'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-322b64c2a9f2
  position:
    end: 1397
    start: 1062
    type: TextPositionSelector
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
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-1fae9bf0b3f4
  position:
    end: 1491
    start: 1398
    type: TextPositionSelector
  selector:
    exact: 'The push operation adds an element and increments the top index, after
      checking for overflow:'
    prefix: 'th few other helper operations.

      '
    suffix: '

      Similarly, pop decrements the t'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-57bb10891387
  position:
    end: 1615
    start: 1492
    type: TextPositionSelector
  selector:
    exact: 'Similarly, pop decrements the top index after checking for underflow,
      and returns the item that was previously the top one:'
    prefix: 'x, after checking for overflow:

      '
    suffix: '

      Calculators that employ reverse'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-63eafcee671c
  position:
    end: 1928
    start: 1616
    type: TextPositionSelector
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
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-4fe264776635
  position:
    end: 1985
    start: 1929
    type: TextPositionSelector
  selector:
    exact: Another important application of stacks is backtracking.
    prefix: 'ranslation into low-level code.

      '
    suffix: '

      This can be achieved through th'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-a7ae1699eb8d
  position:
    end: 2143
    start: 1986
    type: TextPositionSelector
  selector:
    exact: This can be achieved through the use of stacks, as a last correct point
      can be pushed onto the stack, and popped from the stack in case of an incorrect
      path.
    prefix: 'tion of stacks is backtracking.

      '
    suffix: '

      There is also a number of small'
    type: TextQuoteSelector
  snapshot_sha256: sha256:69ec989da81e899aa87cd4ceb1f81e49dd48e31f25ae96fd706eb1d65d3c82a4
- evidence_id: evidence-def936ce83dc
  position:
    end: 2320
    start: 2144
    type: TextPositionSelector
  selector:
    exact: There is also a number of small microprocessors that implement a stack
      directly in hardware, and some microcontrollers have a fixed-depth stack that
      is not directly accessible.
    prefix: 'k in case of an incorrect path.

      '
    suffix: '

      '
    type: TextQuoteSelector
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
