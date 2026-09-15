---
archive_policy: text-only
attachments:
- filename: wiki-queue-adt.txt
  kind: document
  media_type: text/plain
  role: original
  sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-321ef16388c5
  position:
    end: 103
    start: 0
    type: TextPositionSelector
  selector:
    exact: In computer science, a queue is an abstract data type that serves as an
      ordered collection of entities.
    prefix: ''
    suffix: ' By convention, the end of the q'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-0b3f314368e0
  position:
    end: 302
    start: 104
    type: TextPositionSelector
  selector:
    exact: By convention, the end of the queue where elements are added is called
      the back, tail, or rear of the queue. The end of the queue where elements are
      removed is called the head or front of the queue.
    prefix: 'ordered collection of entities. '
    suffix: ' The name queue is an analogy to'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-5fbba192da65
  position:
    end: 497
    start: 441
    type: TextPositionSelector
  selector:
    exact: Enqueue, which adds one element to the rear of the queue
    prefix: 't supports two main operations.

      '
    suffix: '

      Dequeue, which removes one elem'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-63df362c3908
  position:
    end: 561
    start: 498
    type: TextPositionSelector
  selector:
    exact: Dequeue, which removes one element from the front of the queue.
    prefix: 'lement to the rear of the queue

      '
    suffix: '

      Other operations may also be al'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-8bb17fb652f7
  position:
    end: 721
    start: 562
    type: TextPositionSelector
  selector:
    exact: Other operations may also be allowed, often including a peek or front operation
      that returns the value of the next element to be dequeued without dequeuing
      it.
    prefix: 'nt from the front of the queue.

      '
    suffix: '

      The operations of a queue make '
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-a8fcff8045f3
  position:
    end: 864
    start: 722
    type: TextPositionSelector
  selector:
    exact: The operations of a queue make it a first-in-first-out (FIFO) data structure
      as the first element added to the queue is the first one removed.
    prefix: ' dequeued without dequeuing it.

      '
    suffix: ' This is equivalent to the requi'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-2ae223870aea
  position:
    end: 1124
    start: 1031
    type: TextPositionSelector
  selector:
    exact: A queue is an example of a linear data structure, or more abstractly a
      sequential collection.
    prefix: 'the new element can be removed. '
    suffix: '

      Queues are common in computer p'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-2bcf59757f6a
  position:
    end: 1436
    start: 1315
    type: TextPositionSelector
  selector:
    exact: A queue may be implemented as circular buffers and linked lists, or by
      using both the stack pointer and the base pointer.
    prefix: '-oriented languages as classes. '
    suffix: '

      Time complexity in big O notati'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-4db305b3ca1c
  position:
    end: 1681
    start: 1619
    type: TextPositionSelector
  selector:
    exact: A bounded queue is a queue limited to a fixed number of items.
    prefix: 't case. Space complexity: O(n).

      '
    suffix: '

      There are several efficient imp'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-55c74d7a1fd6
  position:
    end: 1848
    start: 1682
    type: TextPositionSelector
  selector:
    exact: There are several efficient implementations of FIFO queues. An efficient
      implementation is one that can perform the operations—en-queuing and de-queuing—in
      O(1) time.
    prefix: 'ted to a fixed number of items.

      '
    suffix: '

      A doubly linked list has O(1) i'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-01e0dc35da5b
  position:
    end: 1953
    start: 1849
    type: TextPositionSelector
  selector:
    exact: A doubly linked list has O(1) insertion and deletion at both ends, so it
      is a natural choice for queues.
    prefix: 'ng and de-queuing—in O(1) time.

      '
    suffix: '

      A regular singly linked list on'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-98db9ed161b0
  position:
    end: 2178
    start: 1954
    type: TextPositionSelector
  selector:
    exact: A regular singly linked list only has efficient insertion and deletion
      at one end. However, a small modification—keeping a pointer to the last node
      in addition to the first one—will enable it to implement an efficient queue.
    prefix: 'is a natural choice for queues.

      '
    suffix: '

      A deque implemented using a mod'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-a6281e47fc6b
  position:
    end: 2229
    start: 2179
    type: TextPositionSelector
  selector:
    exact: A deque implemented using a modified dynamic array
    prefix: 'o implement an efficient queue.

      '
    suffix: '

      '
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-8d8f51a56142
  position:
    end: 1030
    start: 865
    type: TextPositionSelector
  selector:
    exact: This is equivalent to the requirement that once a new element is added,
      all elements that were added before have to be removed before the new element
      can be removed.
    prefix: 'queue is the first one removed. '
    suffix: ' A queue is an example of a line'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
- evidence_id: evidence-3612bdfaecca
  position:
    end: 864
    start: 748
    type: TextPositionSelector
  selector:
    exact: make it a first-in-first-out (FIFO) data structure as the first element
      added to the queue is the first one removed.
    prefix: 'g it.

      The operations of a queue '
    suffix: ' This is equivalent to the requi'
    type: TextQuoteSelector
  snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
extractor: utf8/1
id: wiki-queue-adt
local:
  file_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
  path_ref: local-sidecar:public/wiki-queue-adt
media_type: text/plain
origin: external
raw_ref:
  path: archive/raw/59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7.txt
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:59e1aece957ba5df3292e05265c2b20977be1ab8ca87c0d03b0122fd85d2abd7
source_type: local-file
vault_id: public
---
In computer science, a queue is an abstract data type that serves as an ordered collection of entities. By convention, the end of the queue where elements are added is called the back, tail, or rear of the queue. The end of the queue where elements are removed is called the head or front of the queue. The name queue is an analogy to the words used to describe people in line to wait for goods or services. It supports two main operations.
Enqueue, which adds one element to the rear of the queue
Dequeue, which removes one element from the front of the queue.
Other operations may also be allowed, often including a peek or front operation that returns the value of the next element to be dequeued without dequeuing it.
The operations of a queue make it a first-in-first-out (FIFO) data structure as the first element added to the queue is the first one removed. This is equivalent to the requirement that once a new element is added, all elements that were added before have to be removed before the new element can be removed. A queue is an example of a linear data structure, or more abstractly a sequential collection.
Queues are common in computer programs, where they are implemented as data structures coupled with access routines, as an abstract data structure or in object-oriented languages as classes. A queue may be implemented as circular buffers and linked lists, or by using both the stack pointer and the base pointer.
Time complexity in big O notation: Search O(n) average and O(n) worst case; Insert O(1) average and O(1) worst case; Delete O(1) average and O(1) worst case. Space complexity: O(n).
A bounded queue is a queue limited to a fixed number of items.
There are several efficient implementations of FIFO queues. An efficient implementation is one that can perform the operations—en-queuing and de-queuing—in O(1) time.
A doubly linked list has O(1) insertion and deletion at both ends, so it is a natural choice for queues.
A regular singly linked list only has efficient insertion and deletion at one end. However, a small modification—keeping a pointer to the last node in addition to the first one—will enable it to implement an efficient queue.
A deque implemented using a modified dynamic array
